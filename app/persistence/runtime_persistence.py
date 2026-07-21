"""`RuntimePersistence` -- persiste el resultado de una ejecución del Runtime.

Ver app/runtime/runtime.py (`PersistenceProtocol`, BUILD-005),
app/persistence/database.py + session.py + repositories/base_repository.py
(infraestructura genérica ya construida en BUILD-003), docs/33-Modelo-Fisico-PostgreSQL.md
(tabla `predicciones`, sección 4.12).

BUILD-008: implementa el único colaborador de persistencia que faltaba para
que `PredictionRuntime` (BUILD-005) pueda invocar sus tres puntos de
inyección con implementaciones reales. Reutiliza exclusivamente la
infraestructura ya construida en BUILD-003 (`get_session`, `BaseRepository`)
-- no crea ninguna conexión, sesión ni motor nuevos. No implementa lógica
del modelo, no ejecuta motores, no realiza consultas complejas, no crea
endpoints -- únicamente persistencia.

## Nota de nomenclatura (decisión documentada, no una redefinición)

`PersistenceProtocol` (`app/runtime/runtime.py`, BUILD-005) ya fija el
nombre de método `guardar_prediccion(context, reporte) -> None` -- ese
nombre **no se modifica** aquí (restricción explícita: "No modificar
Runtime"). El brief de BUILD-008 pide, además, un método `persist_prediction`.
Ambos nombres conviven: `persist_prediction` es la implementación real;
`guardar_prediccion` es un alias delgado que delega en ella, para que
`RuntimePersistence` siga satisfaciendo `PersistenceProtocol` estructuralmente
sin renombrar nada ya fijado.

## Brecha detectada y documentada, no resuelta en esta misión

Persistir una fila de `predicciones` exige `partido_id` -- la **clave
técnica UUID** de `partidos.id` (`docs/33` §4.12) --, mientras que
`context.match.id_partido` (`PredictionContext`, BUILD-004) es únicamente el
**código de negocio** (ej. `"PAR-000123"`). Resolver uno a partir del otro
requeriría una búsqueda específica (`SELECT ... WHERE id_partido = ...`),
explícitamente prohibida por esta misión ("No implementar búsquedas", "No
usar consultas específicas del negocio") y ya excluida desde BUILD-003
("No implementar... MatchRepository"). Por eso `persist_prediction` recibe
`partido_id` como parámetro explícito -- quien invoque este método debe
resolverlo por su cuenta (tarea de un futuro `MatchRepository`, todavía sin
mandato). No se inventa aquí una resolución alternativa.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any

from app.models import Auditoria, Prediccion
from app.persistence.repositories.base_repository import BaseRepository
from app.persistence.session import get_session
from app.runtime.prediction_context import PredictionContext


class RuntimePersistence:
    """Implementación de `PersistenceProtocol` (`app/runtime/runtime.py`,
    BUILD-005). Reutiliza exclusivamente `get_session`/`BaseRepository`
    (BUILD-003) -- nunca crea una sesión, un motor ni una conexión propios.
    """

    # -- Satisface PersistenceProtocol (BUILD-005) --------------------------

    def guardar_prediccion(self, context: PredictionContext, reporte: dict[str, Any]) -> None:
        """Nombre exigido por `PersistenceProtocol` -- delega en
        `persist_prediction` (ver "Nota de nomenclatura" del encabezado del
        módulo). No puede resolver `partido_id` (la clave técnica) por sí
        misma -- por eso este alias solo funciona si `reporte` ya la incluye
        (clave `"partido_id"`); si no está presente, propaga el error de
        `persist_prediction` sin ocultarlo.
        """
        partido_id = reporte.get("partido_id")
        if not isinstance(partido_id, uuid.UUID):
            raise ValueError(
                "guardar_prediccion requiere reporte['partido_id'] (UUID) -- "
                "ver 'Brecha detectada' en el encabezado de este módulo."
            )
        self.persist_prediction(context, reporte, partido_id=partido_id)

    # -- API propia de esta misión (BUILD-008) ------------------------------

    def persist_prediction(
        self,
        context: PredictionContext,
        reporte: dict[str, Any],
        partido_id: uuid.UUID,
    ) -> Prediccion:
        """Persiste el `PredictionReport` ya ensamblado como una fila de
        `predicciones` (`docs/33` §4.12), usando `BaseRepository`/`get_session`
        -- nunca SQL manual, nunca una consulta específica de negocio.

        `partido_id` debe resolverlo quien invoque este método (ver "Brecha
        detectada", encabezado del módulo). Exige que `reporte` ya contenga
        probabilidades -- si el Engine se detuvo antes de producirlas
        (`context.metadata.estado_ejecucion` distinto de "Completa"/"Completa
        sin Valor Esperado"), no hay nada válido que persistir todavía; se
        rechaza explícitamente en vez de guardar una fila incompleta.
        """
        probabilidades = reporte.get("probabilidades")
        if not probabilidades:
            raise ValueError(
                "persist_prediction requiere que el Engine ya haya producido "
                "probabilidades (context.prediction.probabilidades) -- nada "
                "que persistir todavía."
            )

        valor_esperado = reporte.get("valor_esperado")
        valor_esperado_numerico = (
            valor_esperado if isinstance(valor_esperado, (int, float, Decimal)) else None
        )

        estado_ejecucion = context.metadata.estado_ejecucion
        id_prediccion = reporte.get("id_prediccion") or (
            f"{context.match.id_partido}-{context.metadata.timestamp_creacion.isoformat()}"
        )

        entidad = Prediccion(
            id_prediccion=id_prediccion,
            partido_id=partido_id,
            version_modelo=reporte.get("version_modelo") or context.metadata.version_modelo,
            probabilidad_local=Decimal(str(probabilidades["local"])),
            probabilidad_empate=Decimal(str(probabilidades["empate"])),
            probabilidad_visitante=Decimal(str(probabilidades["visitante"])),
            top_marcadores=reporte.get("top_marcadores") or [],
            variables_influyentes=reporte.get("variables_influyentes") or [],
            confianza=Decimal(str(reporte["confianza"])) if reporte.get("confianza") is not None else None,
            indice_caos=Decimal(str(reporte["indice_caos"])) if reporte.get("indice_caos") is not None else None,
            valor_esperado=(
                Decimal(str(valor_esperado_numerico)) if valor_esperado_numerico is not None else None
            ),
            estado_ejecucion=estado_ejecucion.value if estado_ejecucion else "Completa",
        )

        with get_session() as session:
            repositorio = BaseRepository(session, Prediccion)
            repositorio.add(entidad)

        return entidad

    def persist_audit(
        self,
        prediccion_id: uuid.UUID,
        resultado_id: uuid.UUID,
        metricas: dict[str, Any],
    ) -> Auditoria:
        """Placeholder documentado -- BUILD-008 no implementa la Auditoría
        real (Fase 8, `docs/06`). Requeriría comparar una `Prediccion` y un
        `Resultado` ya persistidos (`docs/33` §4.14) y calcular métricas
        (`docs/09-Auditoria.md`) -- calcular una métrica es lógica de
        negocio, explícitamente fuera del alcance de esta misión ("No crear
        lógica de auditoría"). Queda como responsabilidad de una misión
        futura; esta firma solo reserva el punto de entrada, sin ejecutar
        ningún cálculo.
        """
        raise NotImplementedError(
            "persist_audit es un placeholder documentado (BUILD-008) -- la "
            "lógica de auditoría real (docs/06 Fase 8, docs/33 tabla "
            "'auditorias') pertenece a una misión futura."
        )

    def persist_learning(
        self,
        prediccion_id: uuid.UUID,
        diagnostico: dict[str, Any],
    ) -> None:
        """Placeholder documentado -- BUILD-008 no implementa Aprendizaje
        real (Fase 9, `docs/06`; `learning/README.md`). El bloque `learning`
        de `docs/30` §4.10 solo se agrega al registro ya persistido después
        de `audit`, y su contenido (patrones, calibración) es
        responsabilidad exclusiva del pipeline de `learning/`, nunca de esta
        clase ("No escribir aprendizaje automático"). Esta firma solo
        reserva el punto de entrada.
        """
        raise NotImplementedError(
            "persist_learning es un placeholder documentado (BUILD-008) -- "
            "el pipeline real de learning/ pertenece a una misión futura."
        )
