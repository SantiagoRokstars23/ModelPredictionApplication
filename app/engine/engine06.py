"""Engine06 -- Valor Esperado / Value Betting (`engine/06-Expected-Value.md`).

Referencias obligatorias releídas antes de escribir este módulo, en el
orden exigido por el brief de BUILD-015: `docs/00-Project-Tracker.md`,
`docs/30-Contrato-Oficial-del-Prediction-Context.md` (v2.0.0),
`docs/17-Matriz-de-Consumo-de-Variables.md`, `docs/06-Flujo-Operacional.md`
(el brief cita `docs/06-Arquitectura-del-Engine.md`, que no existe -- mismo
tipo de desliz de nombre ya documentado en `docs/30`/`BUILD-014`, no
bloqueante), `engine/06-Expected-Value.md` (el brief cita
`engine/06-Value.md`, inexistente), `models/expected-value.md` (el brief
cita `models/value.md`, inexistente -- verificado por listado directo antes
de escribir), `models/parameter-calibration.md`.

BUILD-015: último motor del Engine, cierra la Capa 4 (`docs/06`). Implementa
`Engine06Protocol` (`app/engine/engine_runner.py`, BUILD-007). Su única
dependencia dentro de `app/` es el propio `PredictionContext`.

## Ninguna contradicción bloqueante detectada -- análisis explícito

A diferencia de `BUILD-013`/`BUILD-014`, este módulo no encontró ninguna
contradicción real entre documentos que exija detener la misión. Los
hallazgos siguientes son **brechas de dato/calibración**, no conflictos
entre fuentes -- el propio brief instruye manejarlas como placeholders
documentados, no como bloqueos:

1. **Quién lee `cuotas.csv`:** `docs/17` documenta que `engine/06` consume
   "Cuotas del operador" directamente de `data/processed/` (excepción
   `INC-05`). Pero `docs/30` §4.6 ya resuelve **en código** quién ejecuta
   esa lectura: "las cuotas leídas directamente de `cuotas.csv` por
   `EngineRunner` al invocar `engine06`" -- no por `engine06` mismo. Como
   este módulo no puede modificar `EngineRunner` (fuera de alcance
   explícito del brief), Engine06 **nunca** toca `data/processed/` ni
   ningún archivo -- únicamente lee `context.market.cuotas`, ya poblado
   (o no) por quien invoque al Runtime. Sin contradicción: ambos documentos
   coinciden en que las cuotas son un dato de mercado externo; `docs/30` ya
   fija el punto de entrada correcto en código.
2. **Esquema de `context.market.cuotas`:** `MarketBlock.cuotas`
   (`app/runtime/prediction_context.py`) está tipado genéricamente como
   `list[dict[str, Any]]`, sin fijar las claves del diccionario. Se asumen
   las mismas columnas que `models/expected-value.md` §6 cita textualmente
   de `cuotas.csv` (verificadas ahí, no inventadas aquí): `mercado`,
   `seleccion_o_resultado`, `cuota_decimal`. Documentado como supuesto
   explícito, no como hecho verificado en código (no existe todavía ningún
   productor real de `context.market.cuotas` en este repositorio).
3. **Mercados sin `P_modelo` calculable:** `engine/06`, sección "Mercados
   Compatibles", lista nueve mercados. Pero ningún motor de este Engine
   calcula una probabilidad para siete de ellos (Doble oportunidad, Ambos
   anotan, Más/Menos goles, Hándicap, Tiros, Tarjetas, Corners) -- solo
   `engine/03` publica probabilidades para "Ganador del partido"
   (`probabilidad_local`/`empate`/`visitante`) y "Marcador exacto"
   (`probabilidad_marcador`). Los otros siete se descartan explícitamente
   (nunca se inventa una probabilidad), registrado como hallazgo, no como
   error bloqueante -- mismo tratamiento que Variable012/Δ_forma en
   `BUILD-013`/`BUILD-014`.
4. **Umbrales de clasificación EV:** `engine/06`, sección "Clasificación",
   nombra las cinco categorías (Muy Alto/Alto/Moderado/Bajo/Negativo) **sin
   ningún corte numérico** -- a diferencia de `engine/04`/`engine/05`, que sí
   fijan sus propias bandas en su sección "Escala". Ni `models/expected-
   value.md` ni ningún otro documento propone un valor de ejemplo citable.
   Se usan placeholders explícitos (`EV_UMBRAL_BAJO`/`MODERADO`/`ALTO`),
   documentados como el nivel de placeholder más débil de todo el Engine
   (ni siquiera un "ej." simbólico como `offensive-strength.md`). **TODO
   explícito:** calibración real (`models/parameter-calibration.md` §7).

## `EV` puro, `Recomendación` integra Confianza/Caos (models/expected-
## value.md §10, ya resuelto por ese documento -- no una decisión nueva)

`EV = (P_modelo · c) − 1` nunca incorpora `nivel_confianza` ni
`indice_caos_asociado` -- se publican como campos informativos, tal como
`engine/06` ya los declara en su "Salida". La integración cualitativa
ocurre únicamente en `recomendacion` (texto), reutilizando las bandas ya
oficiales de `engine/04`/`engine/05` (Caos > 60 ⇒ banda "Alto"/"Muy Alto";
Confianza < 60 ⇒ banda "Baja"/"No recomendable apostar") como criterio de
cautela -- no un umbral nuevo inventado, sino los ya fijados en las
"Escala" de esos dos motores (`BUILD-013`/`BUILD-014`).

## Flujo del Motor (engine/06) aplicado literalmente

Paso 7 ("Descartar mercados con valor esperado negativo") se aplica a la
**lista publicada** en `context.engine.engine06`: se calcula `EV` para
todo mercado resoluble, pero solo los de `EV ≥ 0` se publican, ordenados
descendentemente por `EV` (Paso 8, "lista priorizada"). Los mercados con
`EV < 0` no generan una entrada de `errors` (es un resultado normal, no una
anomalía) -- a diferencia de un mercado no soportado o una cuota inválida,
que sí se registran.

## Carácter condicional (docs/29 "Completa sin Valor Esperado")

Si `context.market` es `None` o `context.market.cuotas` está vacío, Engine06
no publica nada (`context.engine.engine06` permanece `None`) -- no es un
error, es el caso "Predicción simple (sin cuotas)" ya previsto por `docs/30`
§8. Si hay cuotas pero ninguna produce `EV ≥ 0`, se publica una lista vacía
(`[]`) -- distinto de `None`, para preservar la diferencia entre "no se
evaluó nada" y "se evaluó, pero no hubo oportunidades positivas".

## Qué NO hace este módulo

No recalcula Poisson, Chaos ni Confidence -- las consume de solo lectura.
No accede a Persistence, a `data/processed/` ni a ningún archivo. No
implementa Kelly Criterion ni gestión de bankroll (`engine/07`, futuro, no
implementado). No modifica `Engine01`-`05`, `PredictionContext`, el Runtime
ni `EngineRunner`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.runtime.prediction_context import (
    Engine03Salida,
    Engine06Salida,
    ErrorEntry,
    PredictionContext,
)

# ---------------------------------------------------------------------------
# Mercados soportados -- ver "Mercados sin P_modelo calculable" en el
# docstring del módulo. Nombres literales de engine/06, sección "Mercados
# Compatibles".
# ---------------------------------------------------------------------------

MERCADO_GANADOR_PARTIDO = "Ganador del partido"
MERCADO_MARCADOR_EXACTO = "Marcador exacto"

_SELECCIONES_GANADOR = {"local": "Victoria Local", "empate": "Empate", "visitante": "Victoria Visitante"}

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- ver "Umbrales de clasificación EV" en el
# docstring del módulo. Ninguna cita numérica en models/expected-value.md.
# ---------------------------------------------------------------------------

EV_UMBRAL_BAJO = 0.03
EV_UMBRAL_MODERADO = 0.08
EV_UMBRAL_ALTO = 0.15

# Umbrales de cautela para `recomendacion` -- reutilizan las bandas ya
# oficiales de engine/04 ("Alto" empieza en 61) y engine/05 ("Baja" termina
# en 59, "Moderada" empieza en 60) -- no son umbrales nuevos.
UMBRAL_CAOS_CAUTELA = 60.0
UMBRAL_CONFIANZA_CAUTELA = 60.0


class EntradaFaltante(RuntimeError):
    """`context.engine.engine03`/`engine04`/`engine05` no están disponibles
    todavía -- Engine06 requiere la Capa 2 y la Capa 3 completas (`docs/06`,
    "Capa 4... requiere Capa 1 + Capa 2 + Capa 3"). Nunca se inventa un
    resultado parcial.
    """


class Engine06:
    """Implementación de `Engine06Protocol` (`app/engine/engine_runner.py`,
    BUILD-007). Calcula Valor Esperado (`models/expected-value.md` §7) por
    cada cuota evaluable de `context.market.cuotas`, comparando `P_modelo`
    (`engine03`) contra la probabilidad implícita de la cuota, y publica una
    lista priorizada de oportunidades con `EV ≥ 0`.
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        if (
            context.engine.engine03 is None
            or context.engine.engine04 is None
            or context.engine.engine05 is None
        ):
            self._registrar_error(
                context,
                evento="Entrada de Capa 2/3 faltante",
                detalle=(
                    "context.engine.engine03/engine04/engine05 no están "
                    "disponibles -- Engine06 requiere Probabilidades, Índice "
                    "de Caos e Índice de Confianza ya publicados (docs/06, "
                    "Capa 4 requiere Capa 1 + Capa 2 + Capa 3)."
                ),
            )
            raise EntradaFaltante(
                "Engine06 requiere context.engine.engine03, engine04 y engine05."
            )

        if context.market is None or not context.market.cuotas:
            # Condicional -- sin cuotas, no hay nada que evaluar. No es un
            # error (docs/29, "Completa sin Valor Esperado").
            return context

        engine03 = context.engine.engine03
        nivel_confianza = context.engine.engine05.indice_confianza
        indice_caos = context.engine.engine04.indice_caos

        candidatos: list[Engine06Salida] = []
        for cuota in context.market.cuotas:
            resultado = self._evaluar_cuota(context, cuota, engine03, nivel_confianza, indice_caos)
            if resultado is not None:
                candidatos.append(resultado)

        # Paso 7 (engine/06): descartar EV negativo de la lista publicada.
        # Paso 8: lista priorizada, orden descendente por EV.
        publicables = sorted(
            (c for c in candidatos if c.valor_esperado >= 0.0),
            key=lambda c: c.valor_esperado,
            reverse=True,
        )
        context.engine.engine06 = publicables

        return context

    # -- Evaluación de una cuota (models/expected-value.md §7) ---------------

    def _evaluar_cuota(
        self,
        context: PredictionContext,
        cuota: dict[str, Any],
        engine03: Engine03Salida,
        nivel_confianza: float,
        indice_caos: float,
    ) -> Engine06Salida | None:
        mercado_raw = cuota.get("mercado")
        seleccion_raw = cuota.get("seleccion_o_resultado")

        p_modelo = self._resolver_probabilidad_modelo(mercado_raw, seleccion_raw, engine03)
        if p_modelo is None:
            self._registrar_error(
                context,
                evento="Mercado no soportado",
                detalle=(
                    f"mercado='{mercado_raw}', seleccion_o_resultado='{seleccion_raw}' -- "
                    "ningún motor de este Engine publica una probabilidad para "
                    "este mercado (ver 'Mercados sin P_modelo calculable', "
                    "docstring de app/engine/engine06.py). Cuota descartada."
                ),
            )
            return None

        cuota_decimal = self._extraer_cuota_decimal(cuota)
        if cuota_decimal is None:
            self._registrar_error(
                context,
                evento="Cuota inválida",
                detalle=(
                    f"cuota_decimal ausente o no positiva en la entrada "
                    f"{cuota!r} -- descartada, nunca se inventa un valor."
                ),
            )
            return None

        p_implicita = 1.0 / cuota_decimal
        valor_esperado = p_modelo * cuota_decimal - 1.0
        diferencia_porcentual = (p_modelo - p_implicita) * 100.0

        clasificacion = self._clasificar_ev(valor_esperado)
        recomendacion = self._recomendacion(clasificacion, nivel_confianza, indice_caos)

        return Engine06Salida(
            mercado=self._etiqueta_mercado(mercado_raw, seleccion_raw),
            valor_esperado=valor_esperado,
            probabilidad_modelo=p_modelo,
            probabilidad_implicita=p_implicita,
            diferencia_porcentual=diferencia_porcentual,
            nivel_confianza=nivel_confianza,
            indice_caos_asociado=indice_caos,
            recomendacion=recomendacion,
        )

    # -- Resolución de P_modelo (Paso 1/3, engine/06) -------------------------

    @staticmethod
    def _resolver_probabilidad_modelo(
        mercado: Any, seleccion: Any, engine03: Engine03Salida
    ) -> float | None:
        """Solo dos mercados tienen `P_modelo` disponible hoy -- ver
        "Mercados sin P_modelo calculable" en el docstring del módulo.
        Nunca inventa una probabilidad para un mercado no soportado.
        """
        if mercado == MERCADO_GANADOR_PARTIDO:
            if seleccion == "local":
                return engine03.probabilidad_local
            if seleccion == "empate":
                return engine03.probabilidad_empate
            if seleccion == "visitante":
                return engine03.probabilidad_visitante
            return None

        if mercado == MERCADO_MARCADOR_EXACTO:
            for entrada in engine03.probabilidad_marcador:
                if entrada.marcador == seleccion:
                    return entrada.probabilidad
            return None

        return None

    @staticmethod
    def _extraer_cuota_decimal(cuota: dict[str, Any]) -> float | None:
        valor = cuota.get("cuota_decimal")
        if valor is None:
            return None
        try:
            valor_float = float(valor)
        except (TypeError, ValueError):
            return None
        if valor_float <= 0.0:
            return None
        return valor_float

    @staticmethod
    def _etiqueta_mercado(mercado: Any, seleccion: Any) -> str:
        """`docs/30` §4.4 ("uno por mercado evaluado") y `GR-009` §9.6 ya
        establecen el patrón: mercados bipartitos se etiquetan por
        selección (ej. "Victoria Local"/"Victoria Visitante"), no como un
        único valor combinado.
        """
        if mercado == MERCADO_GANADOR_PARTIDO and seleccion in _SELECCIONES_GANADOR:
            return _SELECCIONES_GANADOR[seleccion]
        return f"{mercado}: {seleccion}"

    # -- Clasificación (engine/06, sección "Clasificación") -------------------

    @staticmethod
    def _clasificar_ev(valor_esperado: float) -> str:
        if valor_esperado < 0.0:
            return "EV Negativo"
        if valor_esperado < EV_UMBRAL_BAJO:
            return "EV Bajo"
        if valor_esperado < EV_UMBRAL_MODERADO:
            return "EV Moderado"
        if valor_esperado < EV_UMBRAL_ALTO:
            return "EV Alto"
        return "EV Muy Alto"

    # -- Recomendación (models/expected-value.md §10) -------------------------

    @staticmethod
    def _recomendacion(clasificacion: str, nivel_confianza: float, indice_caos: float) -> str:
        """`EV` numérico se mantiene puro (nunca incorpora Confianza/Caos,
        `models/expected-value.md` §10) -- la integración cualitativa ocurre
        únicamente aquí, en texto, reutilizando las bandas ya oficiales de
        `engine/04`/`engine/05` como criterio de cautela.
        """
        if clasificacion == "EV Negativo":
            return "No recomendable apostar (EV negativo, engine/06 'Restricciones')"

        cautelas: list[str] = []
        if nivel_confianza < UMBRAL_CONFIANZA_CAUTELA:
            cautelas.append("confianza del modelo baja")
        if indice_caos > UMBRAL_CAOS_CAUTELA:
            cautelas.append("partido de alta volatilidad (Índice de Caos)")

        base = f"{clasificacion} -- ventaja matemática frente al mercado"
        if cautelas:
            return f"{base}, con cautela: {', '.join(cautelas)}"
        return base

    # -- Errores --------------------------------------------------------------

    @staticmethod
    def _registrar_error(context: PredictionContext, evento: str, detalle: str) -> None:
        """Único punto de registro de anomalías de este motor (`docs/30`
        §4.8) -- mismo patrón que `Engine01`-`05`.
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="Engine06",
                capa_fase="Capa 4",
                timestamp=datetime.now(timezone.utc),
                detalle=detalle,
            )
        )
