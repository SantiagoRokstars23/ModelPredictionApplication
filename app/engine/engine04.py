"""Engine04 -- Índice de Caos (`engine/04-Chaos-Index.md`).

Referencias obligatorias revisadas antes de escribir este módulo:
`models/chaos-index.md`, `docs/17-Matriz-de-Consumo-de-Variables.md`,
`docs/06-Flujo-Operacional.md`, `docs/30-Contrato-Oficial-del-Prediction-
Context.md` (v2.0.0), `app/engine/engine03.py` (BUILD-012, mismo patrón de
manejo de contradicciones y placeholders).

BUILD-013: primer motor de la Capa 3. Implementa `Engine04Protocol`
(`app/engine/engine_runner.py`, BUILD-007). Su única dependencia dentro de
`app/` es el propio `PredictionContext`.

## Contradicción -- entradas del brief vs. `models/chaos-index.md` (reportada
## y resuelta por decisión explícita del usuario, no unilateralmente)

El brief de BUILD-013 restringía las entradas de Engine04 a únicamente
`context.engine.engine03`, prohibiendo "volver a consultar Variables
Oficiales". Eso contradice tres fuentes coincidentes:

- `models/chaos-index.md` §7.2: `Chaos = clip(Base_Caos + Δ_disponibilidad +
  Δ_fatiga + Δ_forma + Δ_externos, 0, 100)` -- los cuatro términos `Δ`
  requieren Variable001/006/007/012, que viven en `context.variables`, no en
  `context.engine.engine03`.
- `docs/06-Flujo-Operacional.md`, línea 183: "`engine/04`... consumen las
  salidas de Poisson y de las Fuerzas, **más Variables Oficiales
  contextuales ya preparadas**".
- `docs/17-Matriz-de-Consumo-de-Variables.md`: Variable006/007/012
  catalogadas como consumo **directo** de `engine/04`.

Mismo patrón que las dos contradicciones ya resueltas en `BUILD-012`
(Engine03/Localía, Engine03/μ_gol). El usuario autorizó explícitamente que
Engine04 lea `context.variables` además de `context.engine.engine03`.

## Hallazgo adicional -- Variable012 no existe en el esquema (documentado,
## no resuelto aquí)

`VariablesBlock` (`app/runtime/prediction_context.py`, §4.3) no tiene ningún
campo para Variable012 (Factores Externos), pese a que `docs/17` la asigna
como consumo directo de `engine/04` y `models/chaos-index.md` §7.2 la exige
para `Δ_externos`. Esto no depende de la contradicción anterior: aunque se
autorice leer `context.variables`, Variable012 no está ahí. `Δ_externos` se
implementa como término estructuralmente presente en la fórmula, fijo en
`0.0` (sin ajuste, nunca un valor inventado -- mismo principio ya aplicado
en `Engine01`/`Engine02`/`Engine03` para variables ausentes). **TODO
explícito:** requiere una futura misión `GR-`/`BUILD-` que agregue Variable012
a `VariablesBlock` (fuera de alcance de esta misión: "no modificar
PredictionContext").

## Hallazgo adicional -- Variable001 no captura "inestabilidad/varianza"

`models/chaos-index.md` §6 exige, para `Δ_forma`, "inestabilidad/varianza
reciente" de Variable001. Pero `VariablesBlock.forma_reciente` (como ya lo
usa `Engine01`) es un **valor puntual** (0-100, nivel de forma actual), no
una medida de varianza entre partidos recientes -- ese segundo momento
estadístico no existe en ningún dato ya preparado por `VariablePreparation`.
Aproximar "inestabilidad" a partir de la distancia de ese valor puntual
respecto de 50 sería inventar una semántica que ningún documento de
`models/`/`docs/` respalda (`CLAUDE.md`: "nunca inventar datos"). Se opta,
en su lugar, por la misma honestidad que `Δ_externos`: `Δ_forma` queda
estructuralmente presente, fijo en `0.0`. **TODO explícito:** requiere que
`VariablePreparation`/la Base de Conocimiento capturen una medida real de
varianza de Variable001 sobre una ventana de partidos (fuera de alcance de
este módulo).

## Términos implementados con dato real: `Δ_disponibilidad`, `Δ_fatiga`

Variable006 (Disponibilidad de Plantilla) y Variable007 (Fatiga) sí llegan
como valor puntual 0-100 con una semántica ya establecida por `Engine01`
(`docs/30` §4.3, `Engine01SalidaEquipo`): disponibilidad 100 = plantilla
completa, 0 = plantilla mínima; fatiga 0 = sin fatiga, 100 = fatiga máxima
(mismo comentario que `app/engine/engine01.py`, `_calcular_fuerza_ofensiva_
equipo`). Sobre esa base, sí es posible construir `Δ_disponibilidad`/
`Δ_fatiga` sin inventar semántica nueva.

**Combinación local/visitante -- decisión de diseño explícita:** ninguna de
las fuentes citadas dice cómo combinar el valor de ambos equipos en un único
`Δ` de partido (`engine04` es unipartito, `docs/30` §4.4/GR-009 §9.4). Se usa
el **promedio simple** de ambos equipos cuando los dos están disponibles, o
el valor del equipo disponible si solo uno lo está -- ponderación simbólica
igualitaria, mismo criterio ya usado en `Engine01`/`Engine02` cuando
"ninguna evidencia favorece un término sobre otro" (docstring de
`app/engine/engine01.py`). Si ninguno de los dos equipos tiene el dato, el
término queda en `0.0` y la variable se registra como no utilizada.

## Parámetros -- placeholders documentados (TODO), nunca valores "mágicos"

`models/chaos-index.md` §7.2 no propone, a diferencia de `models/offensive-
strength.md`, ningún valor de ejemplo citable para `Δ_max_x` ("rango
simbólico ±Δ_max_x, sin fijar el número") -- es, en ese sentido, un
placeholder incluso más débil que `LAMBDA_MAX` en `app/engine/engine03.py`.
`DELTA_MAX_DISPONIBILIDAD = DELTA_MAX_FATIGA = 10.0`: rango simétrico
simbólico (cada término puede mover el índice hasta ±10 puntos sobre 100),
elegido por ser una fracción moderada del rango total sin ninguna
pretensión de realismo estadístico. **TODO explícito:** calibración real
(`models/parameter-calibration.md` §7) en cuanto exista evidencia en
`data/results/`.

## Qué NO hace este módulo

No recalcula Poisson (`engine/03`) ni ninguna probabilidad -- las consume
de solo lectura desde `context.engine.engine03`. No accede a Persistence,
a `data/processed/` ni a ningún repositorio. No implementa Confidence ni
Expected Value. No modifica `Engine01`, `Engine02`, `Engine03`,
`PredictionContext`, el Runtime ni las Variables Oficiales.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone

from app.runtime.prediction_context import (
    Engine04Salida,
    ErrorEntry,
    PredictionContext,
    VariablesPorEquipo,
)

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- ver "Parámetros" en el docstring del módulo.
# ---------------------------------------------------------------------------

DELTA_MAX_DISPONIBILIDAD = 10.0
DELTA_MAX_FATIGA = 10.0

_BANDAS_NIVEL_CAOS = (
    (20.0, "Muy Bajo"),
    (40.0, "Bajo"),
    (60.0, "Moderado"),
    (80.0, "Alto"),
)
_NIVEL_CAOS_MAXIMO = "Muy Alto"


class EntradaFaltante(RuntimeError):
    """`context.engine.engine03` (o `context.variables`) no está disponible
    todavía -- Engine04 requiere la salida completa de la Capa 2
    (`docs/06`, "Capa 3... requiere Capa 1 + Capa 2"). Nunca se inventa un
    resultado parcial.
    """


def _clip(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


class Engine04:
    """Implementación de `Engine04Protocol` (`app/engine/engine_runner.py`,
    BUILD-007). Calcula el Índice de Caos (`models/chaos-index.md` §7) a
    partir de la entropía de Shannon de la distribución de `Engine03`, más
    ajustes contextuales de Variable006/007 (Variable001/012 quedan como
    términos estructurales sin dato real -- ver docstring del módulo).
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        if context.engine.engine03 is None:
            self._registrar_error(
                context,
                evento="Entrada de Capa 2 faltante",
                detalle=(
                    "context.engine.engine03 no está disponible -- Engine04 "
                    "requiere la distribución de probabilidad ya publicada "
                    "(docs/06, Capa 3 requiere Capa 2)."
                ),
            )
            raise EntradaFaltante("Engine04 requiere context.engine.engine03.")

        if context.variables is None:
            self._registrar_error(
                context,
                evento="Bloque variables ausente",
                detalle=(
                    "PredictionContext.variables es None -- VariablePreparation "
                    "no se ejecutó todavía. Engine04 no puede evaluar "
                    "Disponibilidad de Plantilla ni Fatiga sin él."
                ),
            )
            raise EntradaFaltante(
                "Engine04 requiere context.variables ya construido por VariablePreparation."
            )

        engine03 = context.engine.engine03
        base_caos = self._entropia_normalizada(
            engine03.probabilidad_local,
            engine03.probabilidad_empate,
            engine03.probabilidad_visitante,
        )

        delta_disponibilidad, usa_disponibilidad = self._delta_disponibilidad(
            context.variables.disponibilidad_plantilla
        )
        delta_fatiga, usa_fatiga = self._delta_fatiga(context.variables.fatiga)

        # Δ_forma (Variable001) y Δ_externos (Variable012): sin dato real
        # disponible hoy -- ver "Hallazgo adicional" en el docstring del
        # módulo. Estructuralmente presentes, nunca inventados.
        delta_forma = 0.0
        delta_externos = 0.0

        indice_caos = _clip(
            base_caos + delta_disponibilidad + delta_fatiga + delta_forma + delta_externos,
            0.0,
            100.0,
        )
        nivel_caos = self._nivel_caos(indice_caos)

        factores_aumentan, factores_reducen = self._factores(
            base_caos, delta_disponibilidad, delta_fatiga, usa_disponibilidad, usa_fatiga
        )

        justificacion = (
            f"Base entrópica de la distribución L/E/V (Engine03): {base_caos:.1f}/100. "
            f"Ajuste por Disponibilidad de Plantilla: {delta_disponibilidad:+.1f} "
            f"({'con dato' if usa_disponibilidad else 'sin dato -- variable descartada'}). "
            f"Ajuste por Fatiga: {delta_fatiga:+.1f} "
            f"({'con dato' if usa_fatiga else 'sin dato -- variable descartada'}). "
            "Forma Reciente (Variable001, sin medida de varianza disponible) y "
            "Factores Externos (Variable012, no existe en el esquema actual) "
            "quedan sin ajuste -- ver docstring de app/engine/engine04.py."
        )

        context.engine.engine04 = Engine04Salida(
            indice_caos=indice_caos,
            nivel_caos=nivel_caos,
            factores_aumentan=factores_aumentan,
            factores_reducen=factores_reducen,
            justificacion=justificacion,
        )

        return context

    # -- Base entrópica (models/chaos-index.md §7.1) -------------------------

    @staticmethod
    def _entropia_normalizada(p_local: float, p_empate: float, p_visitante: float) -> float:
        """`H = -Σ p·ln(p)`, normalizada por `H_max = ln(3)` y escalada a
        0-100. Términos con `p = 0` se omiten de la suma por convención
        (`0·ln(0) := 0`), evitando `math.log(0)`.
        """
        h = 0.0
        for p in (p_local, p_empate, p_visitante):
            if p > 0.0:
                h -= p * math.log(p)
        h_max = math.log(3)
        h_norm = _clip(h / h_max, 0.0, 1.0)
        return 100.0 * h_norm

    # -- Ajustes contextuales (models/chaos-index.md §7.2) --------------------

    @staticmethod
    def _promedio_disponible(variables_por_equipo: VariablesPorEquipo) -> tuple[float | None, bool, bool]:
        """Promedio simple de los valores disponibles de ambos equipos --
        ver "Combinación local/visitante" en el docstring del módulo.
        Devuelve `(promedio, disponible_local, disponible_visitante)`.
        """
        local = variables_por_equipo.local
        visitante = variables_por_equipo.visitante

        valores = []
        if local.disponible and local.valor is not None:
            valores.append(local.valor)
        if visitante.disponible and visitante.valor is not None:
            valores.append(visitante.valor)

        if not valores:
            return None, local.disponible and local.valor is not None, visitante.disponible and visitante.valor is not None

        promedio = sum(valores) / len(valores)
        return (
            promedio,
            local.disponible and local.valor is not None,
            visitante.disponible and visitante.valor is not None,
        )

    def _delta_disponibilidad(self, disponibilidad_plantilla: VariablesPorEquipo) -> tuple[float, bool]:
        """`Δ_disponibilidad`: menor disponibilidad → mayor caos
        (`models/chaos-index.md` §6). Convención 100 = plantilla completa,
        0 = plantilla mínima (misma que `Engine01`).
        """
        promedio, _, _ = self._promedio_disponible(disponibilidad_plantilla)
        if promedio is None:
            return 0.0, False

        proxy_desfavorable = 1.0 - (promedio / 100.0)  # 0 = plantilla completa, 1 = mínima
        delta = (proxy_desfavorable - 0.5) * 2.0 * DELTA_MAX_DISPONIBILIDAD
        return _clip(delta, -DELTA_MAX_DISPONIBILIDAD, DELTA_MAX_DISPONIBILIDAD), True

    def _delta_fatiga(self, fatiga: VariablesPorEquipo) -> tuple[float, bool]:
        """`Δ_fatiga`: mayor fatiga → mayor caos (`models/chaos-index.md`
        §6). Convención 0 = sin fatiga, 100 = fatiga máxima (misma que
        `Engine01`).
        """
        promedio, _, _ = self._promedio_disponible(fatiga)
        if promedio is None:
            return 0.0, False

        proxy_desfavorable = promedio / 100.0  # 0 = sin fatiga, 1 = fatiga máxima
        delta = (proxy_desfavorable - 0.5) * 2.0 * DELTA_MAX_FATIGA
        return _clip(delta, -DELTA_MAX_FATIGA, DELTA_MAX_FATIGA), True

    # -- Clasificación e interpretación (engine/04, sección "Escala") ---------

    @staticmethod
    def _nivel_caos(indice_caos: float) -> str:
        for limite, nivel in _BANDAS_NIVEL_CAOS:
            if indice_caos <= limite:
                return nivel
        return _NIVEL_CAOS_MAXIMO

    @staticmethod
    def _factores(
        base_caos: float,
        delta_disponibilidad: float,
        delta_fatiga: float,
        usa_disponibilidad: bool,
        usa_fatiga: bool,
    ) -> tuple[list[str], list[str]]:
        aumentan: list[str] = []
        reducen: list[str] = []

        if base_caos > 50.0:
            aumentan.append("Distribución de resultados equilibrada (alta entropía de Engine03)")
        elif base_caos < 50.0:
            reducen.append("Distribución de resultados concentrada (baja entropía de Engine03)")

        if usa_disponibilidad:
            if delta_disponibilidad > 0.0:
                aumentan.append("Baja disponibilidad de plantilla (Variable006)")
            elif delta_disponibilidad < 0.0:
                reducen.append("Plantilla mayormente disponible (Variable006)")

        if usa_fatiga:
            if delta_fatiga > 0.0:
                aumentan.append("Fatiga acumulada relevante (Variable007)")
            elif delta_fatiga < 0.0:
                reducen.append("Buen estado físico general (Variable007)")

        return aumentan, reducen

    # -- Errores --------------------------------------------------------------

    @staticmethod
    def _registrar_error(context: PredictionContext, evento: str, detalle: str) -> None:
        """Único punto de registro de anomalías de este motor (`docs/30`
        §4.8) -- mismo patrón que `Engine01`/`Engine02`/`Engine03`.
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="Engine04",
                capa_fase="Capa 3",
                timestamp=datetime.now(timezone.utc),
                detalle=detalle,
            )
        )
