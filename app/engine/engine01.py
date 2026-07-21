"""Engine01 -- Fuerza Ofensiva (`engine/01-Offensive-Strength.md`).

Referencias obligatorias revisadas antes de escribir este módulo:
`models/offensive-strength.md`, `models/defensive-strength.md`,
`models/poisson.md`, `models/parameter-calibration.md`,
`docs/03-Variables.md`, `docs/17-Matriz-de-Consumo-de-Variables.md`,
`docs/26-Runtime-del-Modelo.md`, `docs/29-Arquitectura-del-Runtime.md`,
`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`.

BUILD-009: primer motor con cálculo matemático real (no un *stub*).
Implementa `Engine01Protocol` (`app/engine/engine_runner.py`, BUILD-007)
mediante tipado estructural -- no importa nada de `app/persistence`,
`app/api` ni `app/schemas` (`docs/35` §6: "el Engine es lógica matemática
pura"). Su única dependencia dentro de `app/` es el propio
`PredictionContext` (`app/runtime/prediction_context.py`).

## Contradicción #1 -- alcance real vs. texto literal del brief (resuelta
## por decisión explícita del usuario, no unilateralmente)

El brief de BUILD-009 pedía que Engine01 calculara **tanto** Fuerza
Ofensiva **como** Fuerza Defensiva. Eso contradice: `docs/17` (Fuerza
Defensiva/Variable004 es entrada primaria exclusiva de `engine/02`, nunca de
`engine/01`), `app/runtime/prediction_context.py` (`Engine01Salida` y
`Engine02Salida` son subsecciones separadas del bloque `engine`, con la
regla explícita "nunca un motor escribe en la subsección de otro",
`docs/30` §5), y el propio "Fuera de alcance" del brief ("No implementar
Engine02"). El usuario confirmó explícitamente: este módulo calcula
**únicamente** Fuerza Ofensiva. Fuerza Defensiva pertenece, sin excepción, a
una futura implementación de `app/engine/engine02.py`.

## Contradicción #2 -- bloqueo arquitectónico de publicación (detectada en
## BUILD-009, RESUELTA en BUILD-010, tras GR-009)

`Engine01Salida.fuerza_ofensiva` (BUILD-004) era un único `float`, incapaz
de representar los dos equipos de un mismo partido, mientras
`models/poisson.md` §6 exige `FO_local` y `FO_visitante` como dos números
distintos. BUILD-009 detectó el bloqueo, calculó ambos valores
correctamente, pero no pudo publicarlos (no tenía autoridad para modificar
`PredictionContext`) -- registraba un `ErrorEntry` y lanzaba
`PublicacionBloqueadaPorEsquema`, deteniendo la ejecución.

**`GR-009` reconcilió el contrato** (`docs/30` v2.0.0, sección 4.4.1):
`Engine01Salida` ahora contiene dos instancias de `Engine01SalidaEquipo`
(`local`, `visitante`), con los mismos cinco campos ya declarados por
`engine/01-Offensive-Strength.md`. **`BUILD-010` aplica ese contrato ya
aprobado:** este módulo ya no bloquea la publicación -- construye
`Engine01Salida(local=..., visitante=...)` directamente a partir de los
mismos dos resultados que ya calculaba, y los escribe en
`context.engine.engine01`. `PublicacionBloqueadaPorEsquema` y el
`ErrorEntry` de bloqueo dejaron de ser necesarios y se eliminaron -- no
hay ninguna otra lógica de esta misión que dependiera de ellos. La clase
interna `_ResultadoEquipo` también se eliminó: `Engine01SalidaEquipo`
(`app/runtime/prediction_context.py`) ya tiene exactamente el mismo shape
y ahora es un objeto público del contrato, así que `_calcular_fuerza_ofensiva_equipo`
lo construye directamente, sin una clase intermedia redundante.

**Ningún cálculo cambia** (`BUILD-010`, "No modificar la matemática/el
algoritmo/los placeholders"): la fórmula, los pesos placeholder y la
lógica de disponibilidad de variables de `_calcular_fuerza_ofensiva_equipo`
son exactamente los mismos de `BUILD-009` -- el único cambio es qué se
hace con el resultado ya calculado (antes: bloquear; ahora: publicar).

## Parámetros -- placeholders documentados (TODO), nunca valores "mágicos"

Ningún peso de `models/offensive-strength.md` §6 tiene, todavía, un valor
calibrado con evidencia estadística real (`data/results/` sigue vacío,
`models/parameter-calibration.md`). Los símbolos de este módulo son
placeholders estructurales, no una calibración:

- `DELTA_MAX = 0.20` y `PEN_MAX = 0.30`: citados **literalmente** de los
  ejemplos que el propio `models/offensive-strength.md` propone (§6.2:
  "ej. 0.20 = ±20%"; §6.3: "ej. Pen_max = 0.30") -- no son un valor nuevo
  inventado por esta misión.
- `W_FORMA_RECIENTE`/`W_RENDIMIENTO_TORNEO` (0.5/0.5) y
  `W_DISPONIBILIDAD`/`W_FATIGA`/`W_CALIDAD_PLANTILLA` (1/3 cada uno):
  ningún documento de `models/` propone un valor de ejemplo para estos
  pesos -- se usa ponderación **igualitaria** como el único placeholder
  estructuralmente neutral (ninguna evidencia favorece a un término sobre
  otro todavía), no un valor arbitrario. **TODO:** reemplazar por
  calibración real (`models/parameter-calibration.md` §7) cuando exista
  suficiente historial en `data/results/`.

## Qué NO hace este módulo

No calcula Fuerza Defensiva (Contradicción #1). No implementa Poisson,
Chaos, Confidence ni Expected Value. No consulta SQL, HTTP ni CSV
directamente -- toda su entrada llega ya preparada en `context.variables`
(`app/preparation`, BUILD-006). No asigna valores numéricos calibrados a
ningún peso (sección de parámetros, arriba). No modifica
`app/runtime/prediction_context.py` ni ningún otro motor.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from app.runtime.prediction_context import (
    Engine01Salida,
    Engine01SalidaEquipo,
    ErrorEntry,
    PredictionContext,
    ValorVariable,
    VariablesBlock,
    VariablesPorEquipo,
)

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- ver "Parámetros" en el docstring del módulo.
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
    """Variable003 (Potencial Ofensivo, Nivel A) no disponible para uno o
    ambos equipos -- el cálculo se detiene, nunca se inventa un resultado
    parcial (`docs/06-Flujo-Operacional.md`, tabla "Manejo de errores").
    """


def _clip(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


class Engine01:
    """Implementación de `Engine01Protocol` (`app/engine/engine_runner.py`,
    BUILD-007). Calcula la Fuerza Ofensiva de ambos equipos siguiendo la
    fórmula de `models/offensive-strength.md` §6, y la publica en
    `context.engine.engine01` (`Engine01Salida`, `docs/30` v2.0.0 §4.4.1,
    `GR-009`/`BUILD-010`) -- ver "Contradicción #1" y "Contradicción #2" en
    el encabezado del módulo para el historial completo.
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        inicio = time.perf_counter()

        if context.variables is None:
            self._registrar_error(
                context,
                evento="Bloque variables ausente",
                detalle=(
                    "PredictionContext.variables es None -- VariablePreparation "
                    "no se ejecutó todavía. Engine01 no puede calcular nada sin "
                    "las Variables Oficiales ya preparadas."
                ),
                duracion_ms=self._duracion_ms(inicio),
            )
            raise VariableObligatoriaNoDisponible(
                "Engine01 requiere context.variables ya construido por VariablePreparation."
            )

        variables = context.variables

        faltantes = self._equipos_sin_variable_obligatoria(variables)
        if faltantes:
            self._registrar_error(
                context,
                evento="Variable obligatoria no disponible",
                detalle=(
                    f"Variable003 (Potencial Ofensivo) no disponible para: "
                    f"{', '.join(faltantes)}. Nivel A (docs/17) -- el cálculo se "
                    "detiene, no se produce un resultado parcial inventado "
                    "(docs/06, tabla 'Manejo de errores')."
                ),
                duracion_ms=self._duracion_ms(inicio),
            )
            raise VariableObligatoriaNoDisponible(
                f"Variable003 no disponible para: {', '.join(faltantes)}."
            )

        resultado_local = self._calcular_fuerza_ofensiva_equipo(variables, "local")
        resultado_visitante = self._calcular_fuerza_ofensiva_equipo(variables, "visitante")

        # Publicación (BUILD-010, tras GR-009): Engine01Salida ya admite un
        # valor por equipo -- se escribe directamente, sin bloqueo.
        context.engine.engine01 = Engine01Salida(local=resultado_local, visitante=resultado_visitante)

        return context

    # -- Cálculo (models/offensive-strength.md §6) --------------------------

    def _calcular_fuerza_ofensiva_equipo(
        self, variables: VariablesBlock, lado: str
    ) -> Engine01SalidaEquipo:
        """Fórmula completa de `models/offensive-strength.md` §6, para un
        equipo (`lado` = "local" | "visitante"). `P` ya llega como
        Variable003 preparada (0-100, obligatoria, ya validada por el
        llamador) -- este método no recalcula `Φ(Z/s)`; eso es
        responsabilidad de `VariablePreparation`/`docs/15` (el propio
        `models/offensive-strength.md` §6.1 lo aclara: "P es... el valor de
        Variable003 tal como lo entrega la Capa de Preparación de
        Variables").
        """
        variables_utilizadas = ["Variable003"]
        variables_descartadas: list[str] = []

        p = self._valor_obligatorio(variables.potencial_ofensivo, lado)

        # --- Modificador de forma (M_forma), §6.2 -----------------------
        forma = self._valor_opcional(variables.forma_reciente, lado)
        if forma is not None:
            r = (forma - 50) / 50
            variables_utilizadas.append("Variable001")
        else:
            r = 0.0  # sin ajuste -- nunca un valor inventado (offensive-strength.md §10)
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

        # --- Penalización de disponibilidad (Pen), §6.3 -----------------
        disponibilidad = self._valor_opcional(variables.disponibilidad_plantilla, lado)
        if disponibilidad is not None:
            termino_disponibilidad = W_DISPONIBILIDAD * (1 - disponibilidad / 100)
            variables_utilizadas.append("Variable006")
        else:
            termino_disponibilidad = 0.0
            variables_descartadas.append("Variable006")

        fatiga = self._valor_opcional(variables.fatiga, lado)
        if fatiga is not None:
            # Convención 0 = sin fatiga, 100 = fatiga máxima (offensive-strength.md §6.3)
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

        # --- Fórmula final, §6.4 -----------------------------------------
        fuerza_ofensiva = _clip(p * m_forma * (1 - pen), 0.0, 100.0)

        disponibles = _VARIABLES_OPCIONALES_TOTAL - len(variables_descartadas)
        nivel_confianza_calculo = disponibles / _VARIABLES_OPCIONALES_TOTAL
        calidad_datos = "completa" if not variables_descartadas else "parcial"

        return Engine01SalidaEquipo(
            fuerza_ofensiva=fuerza_ofensiva,
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
            valor_variable: ValorVariable = getattr(variables.potencial_ofensivo, lado)
            if not valor_variable.disponible or valor_variable.valor is None:
                faltantes.append(lado)
        return faltantes

    @staticmethod
    def _valor_obligatorio(variables_por_equipo: VariablesPorEquipo, lado: str) -> float:
        valor_variable: ValorVariable = getattr(variables_por_equipo, lado)
        if valor_variable.valor is None:
            raise VariableObligatoriaNoDisponible(
                f"Variable003 sin valor para '{lado}' -- invariante violado, "
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
        §4.8) -- incluye el tiempo de ejecución transcurrido en `detalle`
        (brief BUILD-009: "registrar tiempos de ejecución"), porque ni
        `ErrorEntry` ni `Engine01Salida` tienen un campo dedicado de
        duración (`docs/26` §7 lo trata como responsabilidad de logging del
        Runtime, no del `PredictionContext`).
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="Engine01",
                capa_fase="Capa 1",
                timestamp=datetime.now(timezone.utc),
                detalle=f"{detalle} (tiempo de cálculo: {duracion_ms:.3f} ms)",
            )
        )
