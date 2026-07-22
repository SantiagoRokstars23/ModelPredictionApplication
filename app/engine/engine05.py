"""Engine05 -- Índice de Confianza (`engine/05-Confidence.md`).

Referencias obligatorias releídas antes de escribir este módulo, en el orden
exigido por el brief de BUILD-014: `docs/00-Project-Tracker.md`,
`docs/30-Contrato-Oficial-del-Prediction-Context.md` (v2.0.0),
`docs/17-Matriz-de-Consumo-de-Variables.md`, `docs/06-Flujo-Operacional.md`
(el brief cita `docs/06-Arquitectura-del-Engine.md`, que no existe -- mismo
tipo de desliz de nombre ya documentado en `docs/30`, "Nota de verificación
previa"; se usa el archivo real, sin bloquear por ello), `engine/05-
Confidence.md`, `models/confidence.md`, `models/parameter-calibration.md`.

BUILD-014: segundo motor de la Capa 3. Implementa `Engine05Protocol`
(`app/engine/engine_runner.py`, BUILD-007). Su única dependencia dentro de
`app/` es el propio `PredictionContext`.

## Contradicción A -- `C_forma` exige varianza de Variable001, que `docs/17`
## clasifica como indirecta para `engine/05` (reportada y resuelta por
## decisión explícita del usuario, no unilateralmente)

`models/confidence.md` §5-6 exige, para `C_forma`, la "varianza reciente de
Variable001". Pero `docs/17-Matriz-de-Consumo-de-Variables.md` clasifica
Variable001 como consumo **indirecto** de `engine/05` (solo alcanzable vía
las salidas ya publicadas de `Engine01`/`Engine02`/`Engine03`, nunca
releyendo la variable original -- `docs/17` §1: "combinar... no variables
directamente"). Incluso si se autorizara la lectura directa, `VariablesBlock`
(`docs/30` §4.3) solo expone un valor puntual de Variable001, no una medida
de varianza -- mismo vacío de datos ya detectado para `Δ_forma` en
`BUILD-013` (Chaos Index).

**Decisión explícita del usuario:** Engine05 **nunca** lee
`context.variables.forma_reciente`. `C_forma` queda fijo en `1.0` (factor
neutral, no reduce la confianza) -- término estructuralmente presente en la
fórmula (`_CONFIANZA_C_FORMA_NEUTRAL`), documentado como pendiente. **TODO
explícito:** requiere que la Base de Conocimiento/`VariablePreparation`
capturen una medida real de varianza de Variable001 sobre una ventana de
partidos, y una futura reconciliación de `docs/17` que autorice su lectura
directa para `engine/05` (fuera de alcance de este módulo).

## Contradicción B -- `C_datos` exige el estado de "cada Variable Oficial",
## pero `docs/17` solo autoriza 3 variables directas (reportada y resuelta
## por decisión explícita del usuario, no unilateralmente)

`models/confidence.md` §5 exige, para `C_datos`, "el Estado de cada
Variable Oficial, ya expuesto en el Objeto de Contexto". Pero `docs/17`
solo autoriza como consumo **directo** de `engine/05` a Variable006,
Variable007 y Variable010 -- el resto (Variable001-004, 008, 009) son
indirectas.

**Decisión explícita del usuario:** `C_datos` combina (a) la disponibilidad
de las 3 variables directas leídas de `context.variables`, con (b) la
completitud ya publicada por `Engine01Salida`/`Engine02Salida`
(`variables_utilizadas`/`variables_descartadas`, por equipo, `docs/30`
§4.4.1) -- sin releer directamente ninguna variable indirecta desde
`context.variables`. Ver `_c_datos`.

## Reconciliación ya resuelta por el propio `models/confidence.md` (no una
## contradicción nueva, documentada por transparencia)

`engine/05-Confidence.md`, Paso 1: "Recibir las probabilidades calculadas
por el Motor de Poisson" -- sugiere consumir el valor numérico de
`engine03`. Pero `models/confidence.md` §8 aclara explícitamente: "no
consume el valor numérico de `λ` ni de las probabilidades -- solo necesita
saber que Poisson pudo ejecutarse". Este módulo sigue la aclaración de
`models/confidence.md` (documento de mayor especificidad matemática,
`CLAUDE.md`: "la investigación pertenece a `models/`"): verifica que
`context.engine.engine03` no sea `None` (confirma ejecución exitosa), pero
nunca lee `probabilidad_local`/`empate`/`visitante`.

## Términos implementados con dato real

- **`C_datos`**: completitud combinada de Variable006/007/010 (directas,
  `context.variables`) y de `variables_utilizadas`/`variables_descartadas`
  ya publicadas por `Engine01Salida`/`Engine02Salida` (indirectas, decisión
  B). Ver `_c_datos`.
- **`C_disponibilidad`**: función decreciente de Variable006/007
  (`context.variables`, autorizadas como directas por `docs/17`) -- cálculo
  propio de este motor, no una reutilización literal de `Pen`
  (`models/offensive-strength.md`/`defensive-strength.md`), porque `Pen` no
  se publica en `Engine01Salida`/`Engine02Salida` (solo el resultado final
  `fuerza_ofensiva`/`fuerza_defensiva`) y porque `models/confidence.md` §6
  solo dice "misma pareja de variables que Pen", no "mismo valor de Pen".
- **`C_diferencia`**: función creciente de la diferencia absoluta de
  `fuerza_ofensiva`/`fuerza_defensiva` entre ambos equipos
  (`context.engine.engine01`/`engine02`, indirectas autorizadas por
  `docs/17`).
- **`Δ_historial`**: ajuste aditivo acotado a partir de la magnitud de
  Variable010 (Historial Directo, `docs/16`: entero con signo, "diferencia
  neta de victorias", sin límite fijo). `models/confidence.md` no especifica
  la dirección del efecto (solo "ajuste fino, acotado, nunca decisivo") --
  se usa la **magnitud** (`|valor|`), no el signo: un historial con
  tendencia marcada (en cualquier dirección) se trata como evidencia
  adicional que sostiene levemente la confianza, nunca la reduce. Decisión
  de diseño explícita, análoga a la ponderación igualitaria ya usada en
  `Engine01`/`Engine02`/`Engine04` cuando "ninguna evidencia favorece una
  interpretación sobre otra".

## Términos sin dato real: `C_forma`

Fijo en `1.0` -- ver "Contradicción A".

## Parámetros -- placeholders documentados (TODO), nunca valores "mágicos"

`models/confidence.md` §6 no propone ningún valor de ejemplo citable para
los pesos de `C_disponibilidad` ni para el rango de `Δ_historial` -- mismo
nivel de placeholder que `models/chaos-index.md` (`BUILD-013`), más débil
que `models/offensive-strength.md`. `W_DISPONIBILIDAD_CONF =
W_FATIGA_CONF = 0.5`: ponderación igualitaria (ninguna evidencia favorece
un término sobre otro). `DELTA_HISTORIAL_MAX = 5.0`: rango pequeño y
acotado, conforme a la restricción textual de `docs/03-Variables.md` citada
en `engine/05-Confidence.md` ("nunca deberá dominar el cálculo"),
proporcionalmente pequeño frente al rango total de 100. **TODO explícito:**
calibración real (`models/parameter-calibration.md` §7) en cuanto exista
evidencia en `data/results/`.

## Qué NO hace este módulo

No recalcula Poisson, Fuerza Ofensiva ni Fuerza Defensiva -- las consume de
solo lectura. No accede a Persistence, a `data/processed/` ni a ningún
repositorio. No implementa Chaos Index ni Expected Value. No modifica
`Engine01`, `Engine02`, `Engine03`, `Engine04`, `PredictionContext`, el
Runtime ni las Variables Oficiales.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.runtime.prediction_context import (
    Engine01Salida,
    Engine01SalidaEquipo,
    Engine02Salida,
    Engine02SalidaEquipo,
    Engine05Salida,
    ErrorEntry,
    PredictionContext,
    ValorVariable,
    VariablesBlock,
    VariablesPorEquipo,
)

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- ver "Parámetros" en el docstring del módulo.
# ---------------------------------------------------------------------------

W_DISPONIBILIDAD_CONF = 0.5
W_FATIGA_CONF = 0.5
DELTA_HISTORIAL_MAX = 5.0

_CONFIANZA_C_FORMA_NEUTRAL = 1.0  # Contradicción A -- sin dato real, ver docstring

_BANDAS_NIVEL_CONFIANZA = (
    (59.999, "Confianza Baja"),
    (69.999, "Confianza Moderada"),
    (79.999, "Confianza Buena"),
    (89.999, "Confianza Alta"),
)
_NIVEL_CONFIANZA_MAXIMO = "Confianza Muy Alta"
_NIVEL_CONFIANZA_MINIMO = "No recomendable apostar"
_UMBRAL_CONFIANZA_MINIMA = 50.0


class EntradaFaltante(RuntimeError):
    """`context.engine.engine01`/`engine02`/`engine03` (o `context.variables`)
    no están disponibles todavía -- Engine05 requiere la salida completa de
    la Capa 1 y la confirmación de ejecución de la Capa 2 (`docs/06`,
    "Capa 3... requiere Capa 1 + Capa 2"). Nunca se inventa un resultado
    parcial.
    """


def _clip(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


class Engine05:
    """Implementación de `Engine05Protocol` (`app/engine/engine_runner.py`,
    BUILD-007). Calcula el Índice de Confianza (`models/confidence.md` §6)
    a partir de la completitud de datos, Variable006/007 (disponibilidad y
    fatiga), la diferencia de Fuerza Ofensiva/Defensiva entre equipos, y un
    ajuste menor de Historial Directo. `C_forma` queda sin dato real -- ver
    docstring del módulo.
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        if context.engine.engine01 is None or context.engine.engine02 is None:
            self._registrar_error(
                context,
                evento="Entrada de Capa 1 faltante",
                detalle=(
                    "context.engine.engine01/engine02 no están disponibles -- "
                    "Engine05 requiere Fuerza Ofensiva y Defensiva de ambos "
                    "equipos ya publicadas (docs/06, Capa 3 requiere Capa 1)."
                ),
            )
            raise EntradaFaltante(
                "Engine05 requiere context.engine.engine01 y context.engine.engine02."
            )

        if context.engine.engine03 is None:
            self._registrar_error(
                context,
                evento="Entrada de Capa 2 faltante",
                detalle=(
                    "context.engine.engine03 no está disponible -- Engine05 "
                    "requiere confirmación de que Poisson se ejecutó "
                    "(models/confidence.md §8: no se usa el valor numérico, "
                    "solo su ejecución exitosa; docs/06, Capa 3 requiere Capa 2)."
                ),
            )
            raise EntradaFaltante("Engine05 requiere context.engine.engine03.")

        if context.variables is None:
            self._registrar_error(
                context,
                evento="Bloque variables ausente",
                detalle=(
                    "PredictionContext.variables es None -- VariablePreparation "
                    "no se ejecutó todavía. Engine05 no puede evaluar "
                    "Disponibilidad de Plantilla, Fatiga ni Historial Directo "
                    "sin él."
                ),
            )
            raise EntradaFaltante(
                "Engine05 requiere context.variables ya construido por VariablePreparation."
            )

        engine01 = context.engine.engine01
        engine02 = context.engine.engine02

        c_datos = self._c_datos(context.variables, engine01, engine02)
        c_disponibilidad, usa_disponibilidad = self._c_disponibilidad(
            context.variables.disponibilidad_plantilla, context.variables.fatiga
        )
        c_forma = _CONFIANZA_C_FORMA_NEUTRAL
        c_diferencia = self._c_diferencia(engine01, engine02)
        delta_historial, usa_historial = self._delta_historial(context.variables.historial_directo)

        indice_confianza = _clip(
            100.0 * c_datos * c_disponibilidad * c_forma * c_diferencia + delta_historial,
            0.0,
            100.0,
        )
        nivel_confianza = self._nivel_confianza(indice_confianza)

        factores_positivos, factores_negativos = self._factores(
            c_datos, c_disponibilidad, c_diferencia, delta_historial, usa_disponibilidad, usa_historial
        )

        justificacion = (
            f"C_datos (completitud, directas + Engine01/02): {c_datos:.2f}. "
            f"C_disponibilidad (Variable006/007): {c_disponibilidad:.2f} "
            f"({'con dato' if usa_disponibilidad else 'sin dato -- neutral'}). "
            f"C_forma (Variable001): neutral -- sin medida de varianza disponible "
            "(ver docstring de app/engine/engine05.py, Contradicción A). "
            f"C_diferencia (Fuerza Ofensiva/Defensiva): {c_diferencia:.2f}. "
            f"Δ_historial (Variable010): {delta_historial:+.1f} "
            f"({'con dato' if usa_historial else 'sin dato -- sin ajuste'})."
        )

        context.engine.engine05 = Engine05Salida(
            indice_confianza=indice_confianza,
            nivel_confianza=nivel_confianza,
            factores_positivos=factores_positivos,
            factores_negativos=factores_negativos,
            justificacion=justificacion,
        )

        return context

    # -- C_datos (models/confidence.md §5-6, Contradicción B) ---------------

    @staticmethod
    def _completitud_equipo(salida_equipo: Engine01SalidaEquipo | Engine02SalidaEquipo) -> tuple[int, int]:
        """Devuelve `(disponibles, consideradas)` a partir de
        `variables_utilizadas`/`variables_descartadas`, ya publicados por
        `Engine01SalidaEquipo`/`Engine02SalidaEquipo` (`docs/30` §4.4.1).
        """
        disponibles = len(salida_equipo.variables_utilizadas)
        consideradas = disponibles + len(salida_equipo.variables_descartadas)
        return disponibles, consideradas

    def _c_datos(
        self, variables: VariablesBlock, engine01: Engine01Salida, engine02: Engine02Salida
    ) -> float:
        """`C_datos`: proporción combinada de variables "disponibles" --
        directas (Variable006/007/010, `context.variables`) más indirectas
        (completitud ya publicada por `Engine01`/`Engine02`, decisión B).
        """
        disponibles = 0
        consideradas = 0

        for variables_por_equipo in (variables.disponibilidad_plantilla, variables.fatiga):
            for lado in ("local", "visitante"):
                valor_variable = getattr(variables_por_equipo, lado)
                consideradas += 1
                if valor_variable.disponible and valor_variable.valor is not None:
                    disponibles += 1

        consideradas += 1  # historial_directo -- propio del partido, no por equipo
        if variables.historial_directo.disponible and variables.historial_directo.valor is not None:
            disponibles += 1

        for salida_equipo in (engine01.local, engine01.visitante, engine02.local, engine02.visitante):
            d, c = self._completitud_equipo(salida_equipo)
            disponibles += d
            consideradas += c

        if consideradas == 0:
            return 1.0  # nunca debería ocurrir -- Variable003/004 son obligatorias
        return _clip(disponibles / consideradas, 0.0, 1.0)

    # -- C_disponibilidad (models/confidence.md §6) --------------------------

    @staticmethod
    def _promedio_disponible(variables_por_equipo: VariablesPorEquipo) -> float | None:
        local = variables_por_equipo.local
        visitante = variables_por_equipo.visitante

        valores = []
        if local.disponible and local.valor is not None:
            valores.append(local.valor)
        if visitante.disponible and visitante.valor is not None:
            valores.append(visitante.valor)

        if not valores:
            return None
        return sum(valores) / len(valores)

    def _c_disponibilidad(
        self, disponibilidad_plantilla: VariablesPorEquipo, fatiga: VariablesPorEquipo
    ) -> tuple[float, bool]:
        """`C_disponibilidad`: función decreciente de Variable006/007 --
        misma pareja de variables que `Pen` (`MODEL-001`/`002`), cálculo
        propio (no reutiliza el valor de `Pen`, no publicado en
        `Engine01Salida`/`Engine02Salida` -- ver docstring del módulo).
        """
        promedio_disponibilidad = self._promedio_disponible(disponibilidad_plantilla)
        promedio_fatiga = self._promedio_disponible(fatiga)

        if promedio_disponibilidad is None and promedio_fatiga is None:
            return 1.0, False  # sin dato -- nunca se inventa una penalización

        termino_disponibilidad = (
            W_DISPONIBILIDAD_CONF * (1.0 - promedio_disponibilidad / 100.0)
            if promedio_disponibilidad is not None
            else 0.0
        )
        termino_fatiga = (
            W_FATIGA_CONF * (promedio_fatiga / 100.0) if promedio_fatiga is not None else 0.0
        )

        pen = _clip(termino_disponibilidad + termino_fatiga, 0.0, 1.0)
        return _clip(1.0 - pen, 0.0, 1.0), True

    # -- C_diferencia (models/confidence.md §6) -------------------------------

    @staticmethod
    def _c_diferencia(engine01: Engine01Salida, engine02: Engine02Salida) -> float:
        """`C_diferencia`: función creciente de la diferencia absoluta entre
        Fuerza Ofensiva/Defensiva de ambos equipos. Promedio simple de
        ambas diferencias (ninguna fuente indica ponderación distinta),
        normalizado sobre el rango 0-100 de cada índice.
        """
        diferencia_ofensiva = abs(engine01.local.fuerza_ofensiva - engine01.visitante.fuerza_ofensiva)
        diferencia_defensiva = abs(engine02.local.fuerza_defensiva - engine02.visitante.fuerza_defensiva)
        diferencia_combinada = (diferencia_ofensiva + diferencia_defensiva) / 2.0
        return _clip(diferencia_combinada / 100.0, 0.0, 1.0)

    # -- Δ_historial (models/confidence.md §6) --------------------------------

    @staticmethod
    def _delta_historial(historial_directo: ValorVariable) -> tuple[float, bool]:
        """`Δ_historial`: ajuste aditivo pequeño y acotado, a partir de la
        magnitud (no el signo -- ver docstring del módulo) de Variable010
        ("diferencia neta de victorias", `docs/16`). Nunca reduce la
        confianza -- solo puede sumar, acotado a `DELTA_HISTORIAL_MAX`.
        """
        if not historial_directo.disponible or historial_directo.valor is None:
            return 0.0, False

        magnitud = abs(historial_directo.valor)
        return _clip(magnitud, 0.0, DELTA_HISTORIAL_MAX), True

    # -- Clasificación e interpretación (engine/05, sección "Escala") ---------

    @staticmethod
    def _nivel_confianza(indice_confianza: float) -> str:
        if indice_confianza < _UMBRAL_CONFIANZA_MINIMA:
            return _NIVEL_CONFIANZA_MINIMO
        for limite, nivel in _BANDAS_NIVEL_CONFIANZA:
            if indice_confianza <= limite:
                return nivel
        return _NIVEL_CONFIANZA_MAXIMO

    @staticmethod
    def _factores(
        c_datos: float,
        c_disponibilidad: float,
        c_diferencia: float,
        delta_historial: float,
        usa_disponibilidad: bool,
        usa_historial: bool,
    ) -> tuple[list[str], list[str]]:
        positivos: list[str] = []
        negativos: list[str] = []

        if c_datos >= 0.8:
            positivos.append("Alta completitud de Variables Oficiales (directas e indirectas)")
        elif c_datos < 0.5:
            negativos.append("Baja completitud de Variables Oficiales")

        if usa_disponibilidad:
            if c_disponibilidad >= 0.8:
                positivos.append("Plantillas mayormente disponibles y sin fatiga relevante")
            elif c_disponibilidad < 0.5:
                negativos.append("Baja disponibilidad de plantilla o fatiga elevada (Variable006/007)")

        if c_diferencia >= 0.6:
            positivos.append("Diferencia clara de nivel entre ambos equipos (Fuerza Ofensiva/Defensiva)")
        elif c_diferencia < 0.3:
            negativos.append("Equipos de nivel muy parejo -- margen estrecho")

        if usa_historial and delta_historial > 0.0:
            positivos.append("Historial Directo con tendencia marcada (ajuste menor, Variable010)")

        return positivos, negativos

    # -- Errores --------------------------------------------------------------

    @staticmethod
    def _registrar_error(context: PredictionContext, evento: str, detalle: str) -> None:
        """Único punto de registro de anomalías de este motor (`docs/30`
        §4.8) -- mismo patrón que `Engine01`/`Engine02`/`Engine03`/`Engine04`.
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="Engine05",
                capa_fase="Capa 3",
                timestamp=datetime.now(timezone.utc),
                detalle=detalle,
            )
        )
