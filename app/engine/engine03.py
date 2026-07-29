"""Engine03 -- Distribución de Poisson (`engine/03-Poisson.md`).

Referencias obligatorias revisadas antes de escribir este módulo:
`models/poisson.md`, `docs/17-Matriz-de-Consumo-de-Variables.md`,
`docs/30-Contrato-Oficial-del-Prediction-Context.md` (v2.0.0),
`docs/06-Flujo-Operacional.md`.

BUILD-012: primer motor probabilístico completo -- transforma Fuerza
Ofensiva/Defensiva (`Engine01`/`Engine02`, ya bipartitas desde `BUILD-010`/
`BUILD-011`) en una matriz conjunta de marcadores y en las probabilidades
Local/Empate/Visitante. Implementa `Engine03Protocol`
(`app/engine/engine_runner.py`, BUILD-007). Su única dependencia dentro de
`app/` es el propio `PredictionContext`.

## Contradicción #1 -- Localía (Variable009), reportada y resuelta por
## decisión explícita del usuario

El brief de BUILD-012 restringía las entradas de Engine03 a únicamente
`Engine01Salida`/`Engine02Salida`, prohibiendo leer Variables Oficiales
directamente. Eso contradecía tres fuentes autorizadas coincidentes:
`docs/06-Flujo-Operacional.md` ("engine/03... consume... más la Variable
Oficial Localía directamente"), `docs/17` (Variable009 asignada como
entrada directa de `engine/03`) y `models/poisson.md` §6 (`Adj_Localía`,
construido a partir de Variable009). El usuario autorizó explícitamente
que Engine03 lea `context.variables.localia` directamente, además de
`Engine01Salida`/`Engine02Salida`.

## Contradicción #2 -- μ_gol, sin fuente real hoy (reportada y resuelta)

`models/poisson.md` §6 exige `μ_gol` (promedio histórico de goles por
equipo por partido, "calculado dinámicamente... no un valor fijo") --
ninguna Variable Oficial, ninguna salida de `Engine01`/`Engine02` ni
ningún repositorio ya construido lo provee. Fijarlo como constante
contradiría el propio `models/poisson.md`. Resuelto por decisión explícita
del usuario: `Engine03` acepta un colaborador inyectable opcional
(`MuGolProvider`, `Protocol`, mismo patrón que `PreparationRepositoryProtocol`
en `app/preparation/preparation.py`, BUILD-006). Si no se inyecta, o si el
proveedor no tiene dato para la competición del partido, Engine03 registra
`ErrorEntry` y se detiene -- nunca inventa un valor. Ninguna implementación
real de `MuGolProvider` existe todavía (fuera de alcance de esta misión).

## Hallazgo #3 -- tipo de Variable009 (documentado, NO bloqueante, sin
## resolver -- fuera del alcance de esta misión)

`docs/16-Contrato-Oficial-de-Variables.md` define Variable009 como "Texto
controlado (ENUM)" con valores `local`/`visitante`/`neutral`. Pero
`ValorVariable.valor` (`app/runtime/prediction_context.py`, BUILD-004)
está tipado `float | None` -- no existe ninguna codificación numérica
documentada de ese ENUM. Como Variable009 es opcional (Nivel D, `docs/16`),
Engine03 trata cualquier valor no interpretable con seguridad como "no
disponible" y aplica un ajuste neutral (`Adj_Localía = 1`) -- el mismo
comportamiento ya establecido para variables opcionales ausentes en
`Engine01`/`Engine02` ("sin ajuste, nunca un valor inventado"). Esto no
bloquea la misión: hoy `VariablePreparation` (BUILD-006) entrega Variable009
siempre como no disponible, por lo que este código es, en la práctica, el
único camino alcanzable. Se documenta como hallazgo, no se resuelve --
requeriría una reconciliación de `docs/16`/`ValorVariable` (candidato de
una futura misión `GR-`), fuera del alcance de `app/engine/engine03.py`.

## Parámetros -- placeholders documentados (TODO)

`KAPPA_LOCAL`/`KAPPA_VISITANTE` (ajuste de Localía) y `LAMBDA_MIN`/
`LAMBDA_MAX` (restricciones de `MODEL-007` §18) no tienen, a diferencia de
`DELTA_MAX`/`PEN_MAX` en `engine01`/`engine02`, ningún valor de ejemplo
citable en `models/poisson.md` -- ese documento los deja explícitamente
simbólicos, sin proponer siquiera un "ej.". Placeholders elegidos aquí,
ninguno con pretensión de realismo estadístico:

- `KAPPA_LOCAL = KAPPA_VISITANTE = 0.0`: la ausencia de evidencia sobre la
  magnitud de la ventaja de localía se representa con la opción menos
  informativa posible -- ningún ajuste (`Adj_Localía = 1`), no una
  suposición arbitraria de "algo de ventaja".
- `LAMBDA_MIN = 0.01`: un épsilon puramente técnico para evitar el caso
  degenerado `λ = 0` (`P(X=0) = 1`) exigido por `MODEL-007` §18 -- no
  representa ninguna afirmación sobre fútbol real.
- `LAMBDA_MAX = 10.0`: techo estructural generoso para evitar un `λ`
  patológico ante una combinación extrema de factores favorables -- **es
  el placeholder con la justificación más débil de todo el Engine**, sin
  ninguna cita textual de respaldo (a diferencia de `DELTA_MAX`/`PEN_MAX`).
  **TODO explícito:** requiere calibración real
  (`models/parameter-calibration.md` §7) en cuanto exista evidencia en
  `data/results/`.

## Límite de la matriz (`MAX_GOLES = 6`)

Citado literalmente de `models/poisson.md` §8: "La matriz se construye
para `i, j ∈ {0, 1, ..., 6}`, con una celda adicional agregada '7+' por
cada equipo que acumula la probabilidad restante de la cola". No se
introduce ningún límite nuevo.

## MODEL-020/IMP-003 -- integración del ajuste Dixon-Coles

Implementa exactamente el diseño ya aprobado en `MODEL-020`
(`models/dixon-coles.md`) -- ninguna ecuación, rango ni decisión
arquitectónica se reinterpreta aquí, solo se traduce a código. La
corrección vive **dentro** de `ejecutar()`, entre `_construir_matriz_
conjunta` (matriz Poisson cruda, sin cambios) y la extracción de
`top_marcadores`/probabilidades agregadas -- nunca como un componente
nuevo del `EngineRunner` (`models/dixon-coles.md` §6.1/§8.4, principio
*append-only* de `PredictionContext`, `docs/30`).

`_construir_matriz_conjunta` ya no clasifica Local/Empate/Visitante --
esa lógica se extrajo a `_clasificar_resultado` (idéntica, solo movida)
para poder aplicarse tanto sobre la matriz cruda como sobre la corregida,
sin duplicar código. La matriz cruda (`matriz_original` en `ejecutar()`)
nunca se modifica ni se sobrescribe -- `_aplicar_correccion_dixon_coles`
siempre construye una lista nueva.

**Hallazgo de esta misión, no anticipado por `MODEL-020` (que especificaba
la renormalización como paso incondicional):** con `RHO_DIXON_COLES=0.0`,
`τ(x,y)=1.0` exactamente para las 4 celdas (resta/suma con `0.0` es exacta
en IEEE754), por lo que `matriz_corregida` ya es, célula por célula, bit a
bit idéntica a `matriz_original` -- pero `Z = Σ matriz_corregida`, calculado
por una suma en punto flotante de 64 términos, **no siempre es exactamente
`1.0`** (verificado empíricamente: ~80% de un muestreo aleatorio de `λ`
produce `Z` con un error relativo de 1-2 ULP). Dividir por ese `Z` en el
caso `ρ=0` introduciría una diferencia de punto flotante que el modelo
vigente nunca tuvo -- violaría la exigencia de reproducción **exacta**
(no aproximada) exigida por `IMP-003`. Solución aplicada, no una excepción
a la ecuación sino la misma identidad ya demostrada en `models/dixon-
coles.md` §8.1 (`Z=1` exacto cuando `ρ=0`, en aritmética exacta): cuando
`RHO_DIXON_COLES == 0.0`, `ejecutar()` omite la división por `Z` y usa
`matriz_corregida` directamente -- matemáticamente equivalente a dividir
por el `Z=1` exacto que la demostración ya establece, sin el redondeo
evitable de calcularlo numéricamente. Verificado con un backtest
determinista: `probabilidad_marcador`/`top_marcadores`/`probabilidad_
local`/`empate`/`visitante` quedan bit a bit idénticos a la ejecución sin
esta misión.

## Qué NO hace este módulo

No implementa Chaos, Confidence, Expected Value, recomendaciones, mercado,
Kelly ni ajustes manuales. No modifica `Engine01`, `Engine02`,
`PredictionContext`, el Runtime, `Persistence`, `VariablePreparation` ni
`EngineRunner`. No asigna un valor calibrado a ningún peso ni a `ρ`
(`RHO_DIXON_COLES` permanece `0.0`, sin calibrar, conforme a `MODEL-020`).
No crea ningún Engine nuevo -- la corrección vive dentro de `Engine03`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from scipy.stats import poisson as _poisson_dist

from app.runtime.prediction_context import (
    DistribucionGoles,
    Engine03Salida,
    ErrorEntry,
    MarcadorProbabilidad,
    PredictionContext,
    VariablesBlock,
)

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- ver "Parámetros" en el docstring del módulo.
# ---------------------------------------------------------------------------

KAPPA_LOCAL = 0.0
KAPPA_VISITANTE = 0.0
LAMBDA_MIN = 0.01
LAMBDA_MAX = 10.0

RHO_DIXON_COLES = 0.0
"""`ρ`, MODEL-020 (`models/dixon-coles.md` §7) -- escalar único, sin
calibrar, mismo patrón que `KAPPA_LOCAL`/`KAPPA_VISITANTE`: la opción menos
informativa posible, nunca "algo de corrección" sin evidencia propia del
proyecto. Rango estructural diseñado `[-1, 1]`; rango empírico esperado
por la literatura (no fijado aquí) `[-0.2, -0.1]` (Dixon y Coles, 1997,
citado en `models/poisson.md` §16.4). Con `ρ=0`, `Engine03` es
matemáticamente idéntico al Poisson independiente ya vigente (demostrado
en `models/dixon-coles.md` §8.1). **TODO explícito:** calibración real
condicionada a evidencia suficiente en `data/results/` y a aprobación
explícita del Arquitecto Estadístico Humano (Constitución, Art. 2/5) --
fuera de alcance de `IMP-003`.
"""

MAX_GOLES = 6  # models/poisson.md §8
CELDA_COLA = "7+"
TOP_N_MARCADORES = 4  # models/poisson.md §9: "Seleccionar las primeras cuatro"
_CELDAS_DIXON_COLES = frozenset({"0-0", "1-0", "0-1", "1-1"})
"""Las 4 celdas de marcador bajo que `τ(x,y;λ,μ,ρ)` corrige -- `models/
dixon-coles.md` §6.1/§6.3, reproducidas literalmente de `models/poisson.md`
§16.2 (Dixon y Coles, 1997). Ninguna otra celda de la matriz se toca.
"""


class MuGolProvider(Protocol):
    """Colaborador inyectable -- única fuente admitida de `μ_gol`
    (`models/poisson.md` §6). Ninguna implementación real existe todavía;
    ver "Contradicción #2" en el encabezado del módulo.
    """

    def obtener_mu_gol(self, competicion: str) -> float | None:
        """Debe devolver el promedio histórico de goles por equipo por
        partido para `competicion`, o `None` si no hay evidencia
        suficiente -- nunca debe inventar un valor.
        """
        ...


class EntradaFaltante(RuntimeError):
    """`context.engine.engine01`/`engine02` (o `context.variables`) no
    están disponibles todavía -- Engine03 requiere la salida completa de
    la Capa 1 (`docs/06`, "Capa 2: engine/03... requiere la salida de la
    Capa 1"). Nunca se inventa un resultado parcial.
    """


class MuGolNoDisponible(RuntimeError):
    """No existe un proveedor de `μ_gol` inyectado, o el proveedor no
    tiene dato para la competición del partido -- ver "Contradicción #2"
    en el encabezado del módulo. Nunca se sustituye por un valor fijo.
    """


def _clip(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(maximo, valor))


class Engine03:
    """Implementación de `Engine03Protocol` (`app/engine/engine_runner.py`,
    BUILD-007). Calcula `λ_local`/`λ_visitante` (`models/poisson.md` §6-8,
    §17-18), construye la matriz conjunta de marcadores con SciPy, y
    publica Probabilidades Local/Empate/Visitante y Top 4 en
    `context.engine.engine03`.
    """

    def __init__(self, mu_gol_provider: MuGolProvider | None = None) -> None:
        self._mu_gol_provider = mu_gol_provider

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        if context.engine.engine01 is None or context.engine.engine02 is None:
            self._registrar_error(
                context,
                evento="Entrada de Capa 1 faltante",
                detalle=(
                    "context.engine.engine01/engine02 no están disponibles -- "
                    "Engine03 requiere Fuerza Ofensiva y Defensiva de ambos "
                    "equipos ya publicadas (docs/06, Capa 2 requiere Capa 1)."
                ),
            )
            raise EntradaFaltante(
                "Engine03 requiere context.engine.engine01 y context.engine.engine02."
            )

        if context.variables is None:
            self._registrar_error(
                context,
                evento="Bloque variables ausente",
                detalle=(
                    "PredictionContext.variables es None -- VariablePreparation "
                    "no se ejecutó todavía. Engine03 no puede evaluar Localía "
                    "(Variable009) sin él."
                ),
            )
            raise EntradaFaltante(
                "Engine03 requiere context.variables ya construido por VariablePreparation."
            )

        if self._mu_gol_provider is None:
            self._registrar_error(
                context,
                evento="μ_gol no disponible",
                detalle=(
                    "Ningún MuGolProvider fue inyectado -- μ_gol no tiene fuente "
                    "real todavía (no es Variable Oficial, no es salida de "
                    "Engine01/Engine02). Ver models/poisson.md §6. No se inventa "
                    "un valor fijo."
                ),
            )
            raise MuGolNoDisponible("Engine03 requiere un MuGolProvider inyectado.")

        mu_gol = self._mu_gol_provider.obtener_mu_gol(context.match.competicion)
        if mu_gol is None:
            self._registrar_error(
                context,
                evento="μ_gol no disponible",
                detalle=(
                    f"El MuGolProvider inyectado no tiene dato para la "
                    f"competición '{context.match.competicion}'. No se inventa "
                    "un valor fijo (models/poisson.md §6)."
                ),
            )
            raise MuGolNoDisponible(
                f"Sin μ_gol para la competición '{context.match.competicion}'."
            )

        fo_local = context.engine.engine01.local.fuerza_ofensiva
        fo_visitante = context.engine.engine01.visitante.fuerza_ofensiva
        fd_local = context.engine.engine02.local.fuerza_defensiva
        fd_visitante = context.engine.engine02.visitante.fuerza_defensiva

        lambda_local = self._calcular_lambda(
            fo_propio=fo_local, fd_rival=fd_visitante, mu_gol=mu_gol,
            ajuste_localia=self._ajuste_localia("local", context.variables),
        )
        lambda_visitante = self._calcular_lambda(
            fo_propio=fo_visitante, fd_rival=fd_local, mu_gol=mu_gol,
            ajuste_localia=self._ajuste_localia("visitante", context.variables),
        )

        dist_local = self._distribucion_goles(lambda_local)
        dist_visitante = self._distribucion_goles(lambda_visitante)

        matriz_original = self._construir_matriz_conjunta(dist_local, dist_visitante)

        # Corrección Dixon-Coles (MODEL-020/IMP-003) -- `matriz_original`
        # permanece intacta; se construye una matriz nueva a partir de ella
        # (models/dixon-coles.md §6.1, requisito 3 de IMP-003).
        matriz_corregida = self._aplicar_correccion_dixon_coles(
            matriz_original, lambda_local, lambda_visitante, RHO_DIXON_COLES
        )
        if RHO_DIXON_COLES == 0.0:
            # models/dixon-coles.md §8.1 demuestra Z=1 exacto cuando ρ=0 --
            # se omite la división para no introducir ruido de punto
            # flotante que el modelo vigente nunca tuvo (ver "MODEL-020/
            # IMP-003" en el docstring del módulo). Misma identidad ya
            # demostrada, no una ecuación distinta.
            probabilidad_marcador = matriz_corregida
        else:
            probabilidad_marcador = self._renormalizar_matriz(matriz_corregida)

        top_marcadores = self._top_marcadores(probabilidad_marcador)
        prob_local, prob_empate, prob_visitante = self._clasificar_resultado(probabilidad_marcador)

        context.engine.engine03 = Engine03Salida(
            goles_esperados_local=lambda_local,
            goles_esperados_visitante=lambda_visitante,
            distribucion_goles=DistribucionGoles(local=dist_local, visitante=dist_visitante),
            probabilidad_marcador=probabilidad_marcador,
            top_marcadores=top_marcadores,
            probabilidad_local=prob_local,
            probabilidad_empate=prob_empate,
            probabilidad_visitante=prob_visitante,
        )

        return context

    # -- Cálculo de λ (models/poisson.md §6, §17-18) ------------------------

    def _ajuste_localia(self, lado: str, variables: VariablesBlock) -> float:
        """`Adj_Localía` (`models/poisson.md` §6/§17). Ver "Hallazgo #3" en
        el encabezado del módulo -- `condicion` nunca podrá compararse
        exitosamente contra los literales de texto mientras
        `ValorVariable.valor` siga tipado `float`; se conserva la
        estructura completa de la fórmula para que un futuro arreglo de
        tipo la reactive sin tocar este método.
        """
        localia = variables.localia
        if not localia.disponible or localia.valor is None:
            return 1.0

        condicion = localia.valor
        if condicion == "local":
            return 1.0 + (KAPPA_LOCAL if lado == "local" else -KAPPA_VISITANTE)
        if condicion == "neutral":
            return 1.0
        return 1.0

    def _calcular_lambda(
        self, fo_propio: float, fd_rival: float, mu_gol: float, ajuste_localia: float
    ) -> float:
        """`models/poisson.md` §6/§17/§21: Fuerza Base cruzada × Ajuste de
        Localía × restricciones (`λ_min`/`λ_max`, `MODEL-007` §18).
        Historial Directo y Calidad de Plantilla no participan aquí
        (`models/poisson.md` §19-20) -- Calidad de Plantilla ya está
        incorporada dentro de `fo_propio`/`fd_rival` vía `Pen`
        (`engine01`/`engine02`).
        """
        lambda_base = mu_gol * (fo_propio / 50) * ((100 - fd_rival) / 50)
        lambda_preliminar = lambda_base * ajuste_localia
        return _clip(lambda_preliminar, LAMBDA_MIN, LAMBDA_MAX)

    # -- Distribución y matriz (models/poisson.md §7-9) ----------------------

    def _distribucion_goles(self, lambda_: float) -> dict[str, float]:
        """`P(X=x)` para `x ∈ {0,...,MAX_GOLES}` vía SciPy
        (`scipy.stats.poisson`, sin implementación manual), más la celda
        de cola `"7+"` (`models/poisson.md` §8) usando la función de
        supervivencia (`sf(MAX_GOLES) = P(X > MAX_GOLES)`).
        """
        distribucion = {
            str(x): float(_poisson_dist.pmf(x, mu=lambda_)) for x in range(MAX_GOLES + 1)
        }
        distribucion[CELDA_COLA] = float(_poisson_dist.sf(MAX_GOLES, mu=lambda_))
        return distribucion

    def _construir_matriz_conjunta(
        self, dist_local: dict[str, float], dist_visitante: dict[str, float]
    ) -> list[MarcadorProbabilidad]:
        """`models/poisson.md` §8: `P(i,j) = P(X_local=i) · P(X_visitante=j)`.
        Matriz Poisson pura -- **sin** corrección Dixon-Coles y sin
        clasificar Local/Empate/Visitante (`MODEL-020`/`IMP-003`: ambos
        pasos se aplican por separado en `ejecutar()`, sobre esta matriz o
        sobre la ya corregida, ver `_aplicar_correccion_dixon_coles`/
        `_clasificar_resultado`; esta matriz nunca se modifica ni se
        sobrescribe, `models/dixon-coles.md` §6.1).
        """
        celdas: list[MarcadorProbabilidad] = []
        for etiqueta_i, p_i in dist_local.items():
            for etiqueta_j, p_j in dist_visitante.items():
                celdas.append(
                    MarcadorProbabilidad(marcador=f"{etiqueta_i}-{etiqueta_j}", probabilidad=p_i * p_j)
                )
        return celdas

    def _clasificar_resultado(
        self, celdas: list[MarcadorProbabilidad]
    ) -> tuple[float, float, float]:
        """Suma por diagonal sobre cualquier matriz ya construida (cruda o
        corregida por Dixon-Coles) -- misma clasificación Local/Empate/
        Visitante ya vigente desde `BUILD-012` (`models/poisson.md` §8),
        extraída de `_construir_matriz_conjunta` para poder aplicarse sobre
        la matriz ya corregida sin duplicar lógica (`MODEL-020`/`IMP-003`,
        requisito 5: "Extraer... SOBRE la matriz ya corregida"). Trata
        `"7+"` como `MAX_GOLES+1` únicamente para efectos de comparación
        (nunca para la probabilidad, que permanece exacta) -- misma
        convención ya vigente, sin cambios.
        """
        prob_local = 0.0
        prob_empate = 0.0
        prob_visitante = 0.0

        for celda in celdas:
            etiqueta_i, etiqueta_j = celda.marcador.split("-")
            valor_i = MAX_GOLES + 1 if etiqueta_i == CELDA_COLA else int(etiqueta_i)
            valor_j = MAX_GOLES + 1 if etiqueta_j == CELDA_COLA else int(etiqueta_j)
            if valor_i > valor_j:
                prob_local += celda.probabilidad
            elif valor_i == valor_j:
                prob_empate += celda.probabilidad
            else:
                prob_visitante += celda.probabilidad

        return prob_local, prob_empate, prob_visitante

    # -- Corrección Dixon-Coles (MODEL-020/IMP-003, models/dixon-coles.md) --

    def _tau_dixon_coles(
        self, x: int, y: int, lambda_local: float, lambda_visitante: float, rho: float
    ) -> float:
        """`τ(x,y;λ,μ,ρ)` -- ecuación definitiva, reproducida literalmente
        de `models/dixon-coles.md` §6.3 (a su vez, de `models/poisson.md`
        §16.2, Dixon y Coles, 1997). Ninguna variante -- `1.0` para
        cualquier `(x,y)` fuera de las 4 celdas de `_CELDAS_DIXON_COLES`.
        """
        if x == 0 and y == 0:
            return 1.0 - (lambda_local * lambda_visitante * rho)
        if x == 0 and y == 1:
            return 1.0 + (lambda_local * rho)
        if x == 1 and y == 0:
            return 1.0 + (lambda_visitante * rho)
        if x == 1 and y == 1:
            return 1.0 - rho
        return 1.0

    def _aplicar_correccion_dixon_coles(
        self,
        celdas: list[MarcadorProbabilidad],
        lambda_local: float,
        lambda_visitante: float,
        rho: float,
    ) -> list[MarcadorProbabilidad]:
        """Aplica `τ` únicamente sobre `_CELDAS_DIXON_COLES` (`"0-0"`,
        `"1-0"`, `"0-1"`, `"1-1"`) -- ninguna otra celda (`models/dixon-
        coles.md` §6.1, requisito 2 de `IMP-003`). Construye una lista
        **nueva**; `celdas` (la matriz recibida, cruda) nunca se modifica.
        """
        corregidas: list[MarcadorProbabilidad] = []
        for celda in celdas:
            if celda.marcador in _CELDAS_DIXON_COLES:
                etiqueta_i, etiqueta_j = celda.marcador.split("-")
                tau = self._tau_dixon_coles(
                    int(etiqueta_i), int(etiqueta_j), lambda_local, lambda_visitante, rho
                )
            else:
                tau = 1.0
            corregidas.append(
                MarcadorProbabilidad(marcador=celda.marcador, probabilidad=tau * celda.probabilidad)
            )
        return corregidas

    def _renormalizar_matriz(self, celdas: list[MarcadorProbabilidad]) -> list[MarcadorProbabilidad]:
        """`Z = Σ celdas`; `P_final = P_corregida / Z` -- exactamente como
        quedó documentado en `models/dixon-coles.md` §6.5, restaura el
        invariante "la matriz completa suma exactamente 1" (`models/
        poisson.md` §8) tras la redistribución de masa de `_aplicar_
        correccion_dixon_coles`. Construye una lista nueva; `celdas` nunca
        se modifica.
        """
        z = sum(celda.probabilidad for celda in celdas)
        return [
            MarcadorProbabilidad(marcador=celda.marcador, probabilidad=celda.probabilidad / z)
            for celda in celdas
        ]

    def _top_marcadores(
        self, probabilidad_marcador: list[MarcadorProbabilidad]
    ) -> list[MarcadorProbabilidad]:
        """`models/poisson.md` §9: ordenar la matriz y conservar las
        primeras `TOP_N_MARCADORES` (cuatro). Excluye las celdas de cola
        (`"7+"`) -- no representan un marcador específico, solo una masa
        de probabilidad agregada; incluirlas en un "Top de marcadores"
        sería presentar un resultado que no es, en sí mismo, un marcador
        real.
        """
        marcadores_especificos = [
            celda for celda in probabilidad_marcador if CELDA_COLA not in celda.marcador
        ]
        ordenados = sorted(marcadores_especificos, key=lambda celda: celda.probabilidad, reverse=True)
        return ordenados[:TOP_N_MARCADORES]

    # -- Errores --------------------------------------------------------------

    @staticmethod
    def _registrar_error(context: PredictionContext, evento: str, detalle: str) -> None:
        """Único punto de registro de anomalías de este motor (`docs/30`
        §4.8) -- mismo patrón que `Engine01`/`Engine02`.
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="Engine03",
                capa_fase="Capa 2",
                timestamp=datetime.now(timezone.utc),
                detalle=detalle,
            )
        )
