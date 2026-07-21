"""Engine02 -- Fuerza Defensiva (`engine/02-Defensive-Strength.md`).

Referencias obligatorias revisadas antes de escribir este módulo:
`docs/17-Matriz-de-Consumo-de-Variables.md`,
`engine/02-Defensive-Strength.md`, `models/defensive-strength.md`,
`docs/30-Contrato-Oficial-del-Prediction-Context.md` (v2.0.0), `BUILD-009`,
`BUILD-010`.

BUILD-011: segundo motor con cálculo matemático real, siguiendo
exactamente el mismo patrón arquitectónico que `Engine01`
(`app/engine/engine01.py`, `BUILD-009`/`BUILD-010`) -- ninguna decisión de
diseño nueva. Implementa `Engine02Protocol`
(`app/engine/engine_runner.py`, BUILD-007) mediante tipado estructural --
no importa nada de `app/persistence`, `app/api` ni `app/schemas`
(`docs/35` §6). Su única dependencia dentro de `app/` es el propio
`PredictionContext`.

## Contradicción detectada y ampliación de alcance autorizada explícitamente
## por el usuario (no resuelta unilateralmente)

El brief de BUILD-011 pedía publicar en `context.engine.engine02.local`/
`.visitante`, asumiendo que `Engine02Salida` ya era bipartita -- no lo
era: `BUILD-010` había aplicado ese patrón únicamente a `Engine01Salida`,
dejando `Engine02Salida` intacta a propósito (fuera de su propio alcance).
El "Alcance" original de BUILD-011 tampoco incluía
`app/runtime/prediction_context.py` y prohibía explícitamente modificar
`PredictionContext`. Se detuvo la misión, se reportó la contradicción, y
el usuario autorizó explícitamente ampliar el alcance a ese archivo,
aplicando el mismo cambio ya validado en `BUILD-010` (`Engine02SalidaEquipo`,
mismo patrón que `Engine01SalidaEquipo`) -- ver
`app/runtime/prediction_context.py`, sección "BUILD-011" de su docstring.

## Fórmula -- reutilización deliberada de `M_forma`/`Pen` (no redefinidas)

`models/defensive-strength.md` §6.1 es explícito: `M_forma` y `Pen` **se
reutilizan tal como los define `models/offensive-strength.md`**, mismos
símbolos (`w_R`, `w_T`, `δ_max`, `w_D`, `w_F`, `w_Q`, `Pen_max`), sin
redefinirlos -- "para no repetir [el] riesgo" de que cada motor calcule por
separado un ajuste a partir de las mismas variables compartidas
(`docs/17` §8). Por eso este módulo usa exactamente los mismos valores de
placeholder que `app/engine/engine01.py` (mismo origen, misma
justificación -- no se citan de nuevo aquí, ver ese módulo). Ningún peso
se redefine ni se recalibra en `BUILD-011`.

El término base (`P_def`, a partir de Variable004) ya llega preparado
(0-100) desde `VariablePreparation`/`docs/15`, con la convención de signo
ya fijada en `models/defensive-strength.md` §6.2 (`P_def` alto = buena
defensa) -- este módulo no recalcula ningún `Φ(Z_def/s)`, igual que
`engine01` no recalcula `Φ(Z/s)` para Variable003.

## Fórmula final (`models/defensive-strength.md` §6.3)

```
Fuerza Defensiva = clip( P_def · M_forma · (1 − Pen) , 0, 100 )
```

Misma estructura de tres niveles que `engine01` -- base × modificador de
forma × penalización de disponibilidad.

## Qué NO hace este módulo

No calcula Fuerza Ofensiva (pertenece a `engine01`, ya implementado). No
implementa Poisson, Chaos, Confidence ni Expected Value. No consulta SQL,
HTTP ni CSV directamente -- toda su entrada llega ya preparada en
`context.variables` (`app/preparation`, BUILD-006). No asigna valores
numéricos calibrados a ningún peso (son los mismos placeholders
documentados de `engine01`, ninguno nuevo). No modifica `Engine01`,
`Engine03`, el Runtime, `VariablePreparation`, `Persistence`, la API, los
`Schemas` ni ninguna fórmula matemática.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from app.runtime.prediction_context import (
    Engine02Salida,
    Engine02SalidaEquipo,
    ErrorEntry,
    PredictionContext,
    ValorVariable,
    VariablesBlock,
    VariablesPorEquipo,
)

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- reutilizados sin cambios de app/engine/engine01.py
# (models/defensive-strength.md §6.1: "se reutiliza M_forma y Pen tal como
# los define MODEL-001... sin redefinirlos"). Ver ese módulo para el origen
# y la justificación completa de cada valor -- no se repite aquí.
# ---------------------------------------------------------------------------

DELTA_MAX = 0.20
PEN_MAX = 0.30
W_FORMA_RECIENTE = 0.5
W_RENDIMIENTO_TORNEO = 0.5
W_DISPONIBILIDAD = 1 / 3
W_FATIGA = 1 / 3
W_CALIDAD_PLANTILLA = 1 / 3

_VARIABLES_OPCIONALES_TOTAL = 5  # Variable001, 002, 006, 007, 008


class VariableObligatoriaNoDisponible(RuntimeError):
    """Variable004 (Solidez Defensiva, Nivel A) no disponible para uno o
    ambos equipos -- el cálculo se detiene, nunca se inventa un resultado
    parcial (`docs/06-Flujo-Operacional.md`, tabla "Manejo de errores").
    """


def _clip(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


class Engine02:
    """Implementación de `Engine02Protocol` (`app/engine/engine_runner.py`,
    BUILD-007). Calcula la Fuerza Defensiva de ambos equipos siguiendo la
    fórmula de `models/defensive-strength.md` §6, y la publica en
    `context.engine.engine02` (`Engine02Salida`, `docs/30` v2.0.0 §4.4.1,
    `GR-009`/`BUILD-011`) -- mismo patrón exacto que `Engine01`
    (`app/engine/engine01.py`).
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        inicio = time.perf_counter()

        if context.variables is None:
            self._registrar_error(
                context,
                evento="Bloque variables ausente",
                detalle=(
                    "PredictionContext.variables es None -- VariablePreparation "
                    "no se ejecutó todavía. Engine02 no puede calcular nada sin "
                    "las Variables Oficiales ya preparadas."
                ),
                duracion_ms=self._duracion_ms(inicio),
            )
            raise VariableObligatoriaNoDisponible(
                "Engine02 requiere context.variables ya construido por VariablePreparation."
            )

        variables = context.variables

        faltantes = self._equipos_sin_variable_obligatoria(variables)
        if faltantes:
            self._registrar_error(
                context,
                evento="Variable obligatoria no disponible",
                detalle=(
                    f"Variable004 (Solidez Defensiva) no disponible para: "
                    f"{', '.join(faltantes)}. Nivel A (docs/17) -- el cálculo se "
                    "detiene, no se produce un resultado parcial inventado "
                    "(docs/06, tabla 'Manejo de errores')."
                ),
                duracion_ms=self._duracion_ms(inicio),
            )
            raise VariableObligatoriaNoDisponible(
                f"Variable004 no disponible para: {', '.join(faltantes)}."
            )

        resultado_local = self._calcular_fuerza_defensiva_equipo(variables, "local")
        resultado_visitante = self._calcular_fuerza_defensiva_equipo(variables, "visitante")

        context.engine.engine02 = Engine02Salida(local=resultado_local, visitante=resultado_visitante)

        return context

    # -- Cálculo (models/defensive-strength.md §6) ---------------------------

    def _calcular_fuerza_defensiva_equipo(
        self, variables: VariablesBlock, lado: str
    ) -> Engine02SalidaEquipo:
        """Fórmula completa de `models/defensive-strength.md` §6, para un
        equipo (`lado` = "local" | "visitante"). `P_def` ya llega como
        Variable004 preparada (0-100, obligatoria, ya validada por el
        llamador) -- este método no recalcula `Φ(Z_def/s)`; eso es
        responsabilidad de `VariablePreparation`/`docs/15` (mismo principio
        ya aplicado en `engine01` para Variable003).
        """
        variables_utilizadas = ["Variable004"]
        variables_descartadas: list[str] = []

        p_def = self._valor_obligatorio(variables.solidez_defensiva, lado)

        # --- Modificador de forma (M_forma), reutilizado sin cambios -----
        forma = self._valor_opcional(variables.forma_reciente, lado)
        if forma is not None:
            r = (forma - 50) / 50
            variables_utilizadas.append("Variable001")
        else:
            r = 0.0  # sin ajuste -- nunca un valor inventado
            variables_descartadas.append("Variable001")

        torneo = self._valor_opcional(variables.rendimiento_torneo, lado)
        if torneo is not None:
            t = (torneo - 50) / 50
            variables_utilizadas.append("Variable002")
        else:
            t = 0.0
            variables_descartadas.append("Variable002")

        m_forma = 1 + _clip(
            W_FORMA_RECIENTE * r + W_RENDIMIENTO_TORNEO * t, -DELTA_MAX, DELTA_MAX
        )

        # --- Penalización de disponibilidad (Pen), reutilizada sin cambios
        disponibilidad = self._valor_opcional(variables.disponibilidad_plantilla, lado)
        if disponibilidad is not None:
            termino_disponibilidad = W_DISPONIBILIDAD * (1 - disponibilidad / 100)
            variables_utilizadas.append("Variable006")
        else:
            termino_disponibilidad = 0.0
            variables_descartadas.append("Variable006")

        fatiga = self._valor_opcional(variables.fatiga, lado)
        if fatiga is not None:
            # Convención 0 = sin fatiga, 100 = fatiga máxima (offensive-strength.md §6.3,
            # reutilizada sin cambios por defensive-strength.md §6.1)
            termino_fatiga = W_FATIGA * (fatiga / 100)
            variables_utilizadas.append("Variable007")
        else:
            termino_fatiga = 0.0
            variables_descartadas.append("Variable007")

        calidad = self._valor_opcional(variables.calidad_plantilla, lado)
        if calidad is not None:
            termino_calidad = W_CALIDAD_PLANTILLA * (1 - calidad / 100)
            variables_utilizadas.append("Variable008")
        else:
            termino_calidad = 0.0
            variables_descartadas.append("Variable008")

        pen = _clip(termino_disponibilidad + termino_fatiga + termino_calidad, 0.0, PEN_MAX)

        # --- Fórmula final, §6.3 -----------------------------------------
        fuerza_defensiva = _clip(p_def * m_forma * (1 - pen), 0.0, 100.0)

        disponibles = _VARIABLES_OPCIONALES_TOTAL - len(variables_descartadas)
        nivel_confianza_calculo = disponibles / _VARIABLES_OPCIONALES_TOTAL
        calidad_datos = "completa" if not variables_descartadas else "parcial"

        return Engine02SalidaEquipo(
            fuerza_defensiva=fuerza_defensiva,
            variables_utilizadas=variables_utilizadas,
            variables_descartadas=variables_descartadas,
            nivel_confianza_calculo=nivel_confianza_calculo,
            calidad_datos=calidad_datos,
        )

    # -- Utilidades de lectura de variables ---------------------------------

    @staticmethod
    def _equipos_sin_variable_obligatoria(variables: VariablesBlock) -> list[str]:
        faltantes = []
        for lado in ("local", "visitante"):
            valor_variable: ValorVariable = getattr(variables.solidez_defensiva, lado)
            if not valor_variable.disponible or valor_variable.valor is None:
                faltantes.append(lado)
        return faltantes

    @staticmethod
    def _valor_obligatorio(variables_por_equipo: VariablesPorEquipo, lado: str) -> float:
        valor_variable: ValorVariable = getattr(variables_por_equipo, lado)
        if valor_variable.valor is None:
            raise VariableObligatoriaNoDisponible(
                f"Variable004 sin valor para '{lado}' -- invariante violado, "
                "ya debería haberse validado antes de invocar este método."
            )
        return valor_variable.valor

    @staticmethod
    def _valor_opcional(variables_por_equipo: VariablesPorEquipo, lado: str) -> float | None:
        valor_variable: ValorVariable = getattr(variables_por_equipo, lado)
        if not valor_variable.disponible or valor_variable.valor is None:
            return None
        return valor_variable.valor

    # -- Errores y tiempos de ejecución --------------------------------------

    @staticmethod
    def _duracion_ms(inicio: float) -> float:
        return (time.perf_counter() - inicio) * 1000

    @staticmethod
    def _registrar_error(
        context: PredictionContext, evento: str, detalle: str, duracion_ms: float
    ) -> None:
        """Único punto de registro de anomalías de este motor (`docs/30`
        §4.8) -- mismo patrón exacto que `Engine01._registrar_error`
        (`app/engine/engine01.py`, BUILD-009).
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="Engine02",
                capa_fase="Capa 1",
                timestamp=datetime.now(timezone.utc),
                detalle=f"{detalle} (tiempo de cálculo: {duracion_ms:.3f} ms)",
            )
        )
