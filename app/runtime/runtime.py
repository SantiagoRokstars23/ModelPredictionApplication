"""Runtime -- coordinador de una predicción del Modelo Santiago.

Ver docs/29-Arquitectura-del-Runtime.md — este módulo implementa el
coordinador (`PredictionRuntime`) que construye el `PredictionContext`
(docs/30, ya implementado en `prediction_context.py`, BUILD-004) e invoca, en
el orden fijo ya especificado, a `VariablePreparation`, `EngineRunner`, el
Assembler (dentro de este mismo paquete, docs/29 §2) y `Persistence`.

BUILD-005: única implementación de la coordinación de una predicción. No
implementa la lógica interna de `VariablePreparation`, `EngineRunner` ni
`Persistence` -- únicamente sus interfaces de invocación (`typing.Protocol`),
que una misión futura satisfará con implementaciones reales. El Runtime
nunca calcula, nunca prepara variables, nunca consulta la base de datos
directamente y nunca ejecuta lógica matemática (docs/29, sección 9,
"Separación de responsabilidades") -- su única responsabilidad es coordinar.
"""

from __future__ import annotations

from datetime import date, datetime, time, timezone
from typing import Any, Protocol

from app.runtime.prediction_context import (
    ErrorEntry,
    EstadoEjecucion,
    MatchBlock,
    MetadataBlock,
    PredictionContext,
)


class PredictionRequestLike(Protocol):
    """Interfaz mínima que debe cumplir la solicitud de entrada
    (`PredictionRequest`, docs/25 §1). No se implementa aquí el esquema real
    -- pertenece a `app/schemas`, explícitamente fuera de alcance de esta
    misión ("No implementar... Schemas HTTP").
    """

    id_partido: str
    seleccion_local: str
    seleccion_visitante: str
    competicion: str
    torneo: str
    fecha: date
    hora_local: time | None
    estadio: str | None
    arbitro: str | None


class VariablePreparationProtocol(Protocol):
    """Interfaz de invocación de la Capa de Preparación de Variables
    (docs/15). La implementación real (`app/preparation`) queda para una
    misión futura -- este módulo solo define cómo el Runtime la invoca.
    """

    def preparar(self, context: PredictionContext) -> None:
        """Debe agregar el bloque `variables` (docs/30 §4.3) al `context`."""
        ...


class EngineRunnerProtocol(Protocol):
    """Interfaz de invocación del EngineRunner (docs/29 §2/§4). La
    implementación real (los 6 motores, ejecutados por capas) queda para una
    misión futura -- bloqueada, además, hasta que exista al menos una
    fórmula calibrada en `models/`.
    """

    def ejecutar(self, context: PredictionContext) -> None:
        """Debe agregar las subsecciones de `engine` y el bloque
        `prediction` (docs/30 §4.4/§4.5) al `context`, por capas.
        """
        ...


class PersistenceProtocol(Protocol):
    """Interfaz de invocación de "guardar el resultado de esta ejecución".

    No debe confundirse con el paquete `app/persistence` (BUILD-003, acceso
    genérico a datos): esta interfaz representa específicamente la
    responsabilidad de persistencia de una predicción ya ensamblada; su
    implementación real (que internamente usará `app/persistence`) queda
    para una misión futura.
    """

    def guardar_prediccion(self, context: PredictionContext, reporte: dict[str, Any]) -> None:
        """Debe escribir `reporte` en `data/predictions/` (docs/14, Etapa 3)."""
        ...


class PredictionRuntime:
    """Coordinador de una predicción -- la única implementación oficial del
    Runtime (docs/26/docs/29). Nunca calcula, nunca prepara variables, nunca
    consulta la base de datos directamente, nunca ejecuta lógica matemática
    -- su única responsabilidad es coordinar (docs/29, sección 9).

    Recibe sus tres colaboradores (`VariablePreparation`, `EngineRunner`,
    `Persistence`) por inyección de dependencias, tipados como interfaces
    (`Protocol`) -- ninguna implementación concreta de esos tres componentes
    se importa ni se instancia aquí (restricción explícita de BUILD-005).
    """

    def __init__(
        self,
        preparation: VariablePreparationProtocol,
        engine_runner: EngineRunnerProtocol,
        persistence: PersistenceProtocol,
        version_modelo: str,
    ) -> None:
        self._preparation = preparation
        self._engine_runner = engine_runner
        self._persistence = persistence
        self._version_modelo = version_modelo

    def ejecutar(self, request: PredictionRequestLike) -> PredictionContext:
        """Recorre el flujo oficial (docs/29 §4): construye el Context e
        invoca Preparation -> EngineRunner -> Assembler -> Persistence, en
        ese orden fijo. Devuelve el `PredictionContext` final, completo o
        detenido -- nunca lanza la excepción original hacia quien llama
        (queda registrada en `context.errors`, docs/30 §4.8).
        """
        context = self._crear_contexto(request)

        if not self._invocar_preparation(context):
            context.metadata.estado_ejecucion = EstadoEjecucion.DETENIDA_ANTES_DEL_ENGINE
            context.metadata.timestamp_cierre = datetime.now(timezone.utc)
            return context

        if not self._invocar_engine_runner(context):
            context.metadata.estado_ejecucion = EstadoEjecucion.DETENIDA_DURANTE_EL_ENGINE
            context.metadata.timestamp_cierre = datetime.now(timezone.utc)
            return context

        reporte = self._ensamblar_reporte(context)
        self._invocar_persistence(context, reporte)

        context.metadata.estado_ejecucion = (
            EstadoEjecucion.COMPLETA
            if context.engine.engine06
            else EstadoEjecucion.COMPLETA_SIN_VALOR_ESPERADO
        )
        context.metadata.timestamp_cierre = datetime.now(timezone.utc)
        return context

    # -- Creación (docs/30, sección 3: "Creación") --------------------------

    def _crear_contexto(self, request: PredictionRequestLike) -> PredictionContext:
        """Construye el `PredictionContext` con los bloques `metadata` y
        `match` (docs/30, secciones 3, 4.1 y 4.2) -- la única responsabilidad
        del Runtime en la etapa de Creación.
        """
        ahora = datetime.now(timezone.utc)
        return PredictionContext(
            metadata=MetadataBlock(
                version_modelo=self._version_modelo, timestamp_creacion=ahora
            ),
            match=MatchBlock(
                id_partido=request.id_partido,
                seleccion_local=request.seleccion_local,
                seleccion_visitante=request.seleccion_visitante,
                competicion=request.competicion,
                torneo=request.torneo,
                fecha=request.fecha,
                hora_local=request.hora_local,
                estadio=request.estadio,
                arbitro=request.arbitro,
            ),
        )

    # -- Invocaciones -- cada fase con un único punto de entrada ------------

    def _invocar_preparation(self, context: PredictionContext) -> bool:
        """Único punto de entrada para invocar `VariablePreparation`.
        Devuelve `False` si falla, deteniendo el flujo antes del Engine
        (`docs/06`, "Manejo de errores") -- nunca sustituye el fallo por un
        valor estimado.
        """
        try:
            self._preparation.preparar(context)
        except Exception as exc:  # captura amplia intencional: todo fallo se
            # registra, nunca se propaga sin dejar rastro (docs/26 §7)
            self._registrar_error(context, "VariablePreparation", "Fase 3 (Preparación)", exc)
            return False
        return True

    def _invocar_engine_runner(self, context: PredictionContext) -> bool:
        """Único punto de entrada para invocar `EngineRunner`. Devuelve
        `False` si un motor falla -- "las capas siguientes tampoco se
        ejecutan" (`docs/26` §8).
        """
        try:
            self._engine_runner.ejecutar(context)
        except Exception as exc:  # ver nota de _invocar_preparation
            self._registrar_error(context, "EngineRunner", "Fase 3 (Engine)", exc)
            return False
        return True

    def _ensamblar_reporte(self, context: PredictionContext) -> dict[str, Any]:
        """Único punto de entrada para transformar el `PredictionContext`
        completo en el contrato de salida (docs/25 §6; docs/29 §5,
        Assembler). Transformación pura: lee campos ya calculados por
        `EngineRunner`, no calcula ningún valor nuevo.

        Devuelve un `dict` provisional -- el contrato tipado real
        (`PredictionReport`) pertenece a `app/schemas`, fuera del alcance de
        esta misión.
        """
        prediction = context.prediction
        return {
            "id_prediccion": context.metadata.id_prediccion,
            "partido": context.match.model_dump(),
            "probabilidades": (
                prediction.probabilidades.model_dump()
                if prediction and prediction.probabilidades
                else None
            ),
            "top_marcadores": (
                [marcador.model_dump() for marcador in prediction.top_marcadores]
                if prediction
                else []
            ),
            "variables_influyentes": prediction.variables_influyentes if prediction else [],
            "confianza": prediction.confianza if prediction else None,
            "indice_caos": prediction.indice_caos if prediction else None,
            "valor_esperado": prediction.valor_esperado if prediction else None,
            "version_modelo": context.metadata.version_modelo,
        }

    def _invocar_persistence(self, context: PredictionContext, reporte: dict[str, Any]) -> None:
        """Único punto de entrada para invocar la persistencia de una
        predicción ya ensamblada (`docs/14`, Etapa 3: siempre antes del
        inicio del partido).
        """
        self._persistence.guardar_prediccion(context, reporte)

    def _registrar_error(
        self, context: PredictionContext, componente: str, capa_fase: str, exc: Exception
    ) -> None:
        """Único punto de entrada para registrar una anomalía en el bloque
        `errors` (docs/30 §4.8) -- ningún error se descarta en silencio
        (`docs/26` §7).
        """
        context.errors.append(
            ErrorEntry(
                evento=f"Fallo en {componente}",
                componente_emisor=componente,
                capa_fase=capa_fase,
                timestamp=datetime.now(timezone.utc),
                detalle=str(exc),
            )
        )
