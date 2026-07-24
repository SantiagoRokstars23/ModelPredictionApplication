"""`EnginePipeline` -- integra `VariablePreparation` + `EngineRunner` en un
único flujo oficial de ejecución (Misión INT-001).

Referencias releídas antes de escribir este módulo: `docs/00-Project-
Tracker.md`, `docs/06-Flujo-Operacional.md` (diagrama de dependencias del
Engine por capas, manejo de errores), `docs/17-Matriz-de-Consumo-de-
Variables.md` (qué motor consume la salida de cuál), `docs/26-Runtime-del-
Modelo.md` §7-8 (log de ejecución, "las capas siguientes tampoco se
ejecutan"), `docs/29-Arquitectura-del-Runtime.md` (los siete componentes
oficiales, sección 2, y el orden de ejecución exacto, sección 4),
`docs/30-Contrato-Oficial-del-Prediction-Context.md` (`PredictionContext`,
append-only), `docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`
(matriz de dependencias entre paquetes de `app/`), `app/runtime/runtime.py`
(BUILD-005, `PredictionRuntime`), `app/engine/engine_runner.py` (BUILD-007,
`EngineRunner`), `app/preparation/preparation.py` (BUILD-017 a BUILD-024,
`VariablePreparation`), `app/engine/engine01.py` a `engine06.py` (BUILD-009
a BUILD-015), `app/persistence/mu_gol_provider.py` (BUILD-016,
`HistoricalMuGolProvider`).

**Nota sobre la "Autoridad documental" citada por el brief de INT-001:** el
brief nombra `docs/30-Architecture.md`, `docs/17-Variables-Oficiales.md`,
`docs/06-Engine-Pipeline.md` y `docs/23-Architecture-Freeze.md` -- ninguno
de esos cuatro nombres de archivo existe literalmente en `docs/`. Se
verificó, número por número, cuál es el documento real detrás de cada cita:
`docs/30-Contrato-Oficial-del-Prediction-Context.md` (arquitectura del
Objeto de Contexto), `docs/17-Matriz-de-Consumo-de-Variables.md` (consumo de
Variables Oficiales por motor), `docs/06-Flujo-Operacional.md` (el propio
diagrama de dependencias del Engine, citado literalmente como "Engine
Pipeline" en el brief). El único caso genuinamente sin equivalente evidente
por número es `docs/23-Architecture-Freeze.md`: `docs/23` es en realidad
`Plan-Maestro-de-Reconciliacion-Operativa.md` (una misión `AR-002` de
gobernanza, no de arquitectura de freeze); el documento que sí se titula
literalmente "Architecture Freeze" es `docs/19-Architecture-Freeze-Review.md`.
**Esto no bloquea la misión:** es el mismo tipo de desliz de nombre ya
documentado sin bloquear, sin contradicción de contenido, en `app/engine/
engine06.py` (BUILD-015, "el brief cita `docs/06-Arquitectura-del-Engine.md`,
que no existe") y en `app/runtime/prediction_context.py` (BUILD-014). Se
leyeron ambos candidatos (`docs/19` y `docs/23`) antes de escribir código;
ninguno contradice la arquitectura ya verificada en `docs/06`/`docs/17`/
`docs/29`/`docs/30`, que es la que efectivamente rige esta integración.

# Hallazgo central de esta misión: el orquestador ya existe, en dos piezas
# ya completas -- lo que faltaba era la composición (wiring), no el diseño

Antes de escribir código se verificó, componente por componente, el estado
real de la arquitectura que `docs/29` (sección 2) exige:

| Componente (`docs/29` §2) | Estado antes de esta misión |
|---|---|
| `VariablePreparation` | Completo -- las 9 Variables Oficiales activas tienen ya un veredicto de implementabilidad (7 con dato real, `MODEL-009` a `MODEL-015`/`BUILD-018` a `BUILD-024`); Variable009 bloqueada por esquema, no por esta misión |
| `EngineRunner` | Completo desde `BUILD-007` -- coordina los 6 motores exactamente por las 4 capas de `docs/06`, con manejo de errores que detiene las capas siguientes (verificado leyendo el código, no solo el docstring) |
| `Engine01`-`Engine06` | Completos desde `BUILD-009` a `BUILD-015` -- verificado que sus dependencias en código (`context.engine.engineXX`/`context.variables` leídos) coinciden exactamente con el grafo de dependencias que el propio brief de esta misión describe (sección "Obligación 6" del brief) -- **ninguna contradicción encontrada** |
| `PredictionRuntime` | Completo desde `BUILD-005` -- ya coordina `VariablePreparation` -> `EngineRunner` -> Assembler -> `Persistence`, con manejo de errores y estados de ejecución (`docs/29` §6) |
| `HistoricalMuGolProvider` | Completo desde `BUILD-016` -- satisface `MuGolProvider` (`app/engine/engine03.py`) estructuralmente, sin necesitar ningún cambio |

**Lo único que no existía en ningún archivo del repositorio: un punto de
composición (composition root) que instancie las implementaciones
concretas de `VariablePreparation` y de los 6 motores, y las inyecte en
`EngineRunner`.** `app/main.py` (BUILD-001) es deliberadamente una
aplicación FastAPI vacía, sin ninguna dependencia de `app/runtime`/
`app/engine`/`app/persistence` (fuera de alcance de esa misión y de esta,
que no crea endpoints ni APIs). Sin ese punto de composición, sería
imposible ejecutar el flujo `VariablePreparation -> Engine01...Engine06` con
objetos reales -- solo con protocolos. Este módulo es exactamente eso: un
composition root, no un rediseño de ningún componente ya existente.

# Por qué un archivo nuevo, no una modificación de `runtime.py`/`engine_runner.py`

`app/runtime/runtime.py` (`PredictionRuntime`, `VariablePreparationProtocol`,
`EngineRunnerProtocol`, `PersistenceProtocol`) declara explícitamente, desde
`BUILD-005`: "ninguna implementación concreta de esos tres componentes se
importa ni se instancia aquí". Agregar imports concretos de `app.preparation`/
`app.engine` a `runtime.py` violaría esa restricción ya vigente sin ninguna
necesidad real -- el mismo resultado se logra con un módulo nuevo, dedicado
exclusivamente a la composición, sin tocar ningún archivo ya existente.
`app/engine/engine_runner.py` tampoco se modifica: ya está completo (tabla
arriba) y el brief de esta misión solo autoriza completarlo "si está
incompleto" -- no lo está.

# Alcance exacto de este módulo -- por qué no incluye Assembler ni Persistence

El propio diagrama técnico del brief de INT-001 termina en "PredictionContext
completo", inmediatamente después de `Engine06` -- no incluye Assembler ni
Persistence. El brief, además, prohíbe explícitamente esta misión de tocar
"Persistencia" ("Fuera de alcance"). `docs/29` (sección 2) sí incluye
Assembler y Persistence como parte del pipeline completo, pero esos dos
pasos **ya están implementados** dentro de `PredictionRuntime`
(`_ensamblar_reporte`/`_invocar_persistence`, `BUILD-005`) y tienen su propio
colaborador real (`RuntimePersistence`, `BUILD-008`) -- con una brecha ya
documentada y no resuelta en ese propio módulo (`persist_prediction` exige
`partido_id`, una clave técnica que el `PredictionReport` actual no
resuelve). Esta misión no reabre esa brecha (fuera de alcance explícito) ni
inventa una solución para ella. `EnginePipeline` (esta clase) integra
únicamente el tramo `VariablePreparation -> EngineRunner`, exactamente el
que pide el diagrama de esta misión -- quien necesite el pipeline completo
de `docs/29` (incluida persistencia) sigue usando `PredictionRuntime`
directamente, sin ningún cambio de este módulo.

## Qué NO hace este módulo

No modifica `PredictionContext`, `Engine01`-`06`, `EngineRunner`,
`PredictionRuntime`, `VariablePreparation` ni ningún motor. No calcula
ninguna fórmula, no calibra ningún parámetro. No implementa Variable009, no
implementa un Market Provider, no implementa persistencia ni captura de
datos. No crea ningún endpoint de API. No reabre bloques ya publicados de
`PredictionContext`, no recalcula Variables Oficiales, no borra
información -- respeta íntegramente el principio append-only ya vigente
(`docs/30`, `BUILD-004`).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from app.engine.engine01 import Engine01
from app.engine.engine02 import Engine02
from app.engine.engine03 import Engine03, MuGolProvider
from app.engine.engine04 import Engine04
from app.engine.engine05 import Engine05
from app.engine.engine06 import Engine06
from app.engine.engine_runner import EngineRunner
from app.persistence.mu_gol_provider import HistoricalMuGolProvider
from app.preparation.preparation import VariablePreparation
from app.runtime.prediction_context import ErrorEntry, PredictionContext


class VariablePreparationProtocol(Protocol):
    """Misma interfaz ya declarada por `app/runtime/runtime.py`
    (`VariablePreparationProtocol`, BUILD-005) -- se redeclara aquí, en
    lugar de importarla desde allí, para no acoplar este módulo a
    `runtime.py` más allá de lo estrictamente necesario (`PredictionContext`
    es la única dependencia real compartida). Misma forma estructural
    exacta -- `VariablePreparation` (BUILD-006/017-024) ya la satisface sin
    ningún cambio.
    """

    def preparar(self, context: PredictionContext) -> None:
        """Debe agregar el bloque `variables` (docs/30 §4.3) al `context`."""
        ...


class EngineRunnerProtocol(Protocol):
    """Misma forma estructural que `EngineRunner.ejecutar` (`app/engine/
    engine_runner.py`, BUILD-007) -- redeclarada aquí por el mismo motivo
    que `VariablePreparationProtocol`.
    """

    def ejecutar(self, context: PredictionContext) -> None:
        """Debe agregar las subsecciones de `engine` (docs/30 §4.4) al
        `context`, por capas.
        """
        ...


def construir_engine_runner(mu_gol_provider: MuGolProvider | None = None) -> EngineRunner:
    """Instancia los 6 motores concretos (`Engine01` a `Engine06`, `BUILD-009`
    a `BUILD-015`) y los inyecta en `EngineRunner` (`app/engine/engine_
    runner.py`, BUILD-007) -- ningún motor se modifica, solo se instancia.

    `Engine03` recibe `HistoricalMuGolProvider` (`app/persistence/mu_gol_
    provider.py`, BUILD-016) si no se provee otro proveedor -- obligación 7
    del brief de INT-001: "No implementar uno nuevo. Usar el mecanismo ya
    existente." Si en el futuro se invoca esta función sin ningún `μ_gol`
    real disponible (ej. `HistoricalMuGolProvider.obtener_mu_gol` devuelve
    `None` por falta de historial en `partidos.csv`), `Engine03` se comporta
    exactamente igual que hoy (`MuGolNoDisponible`, `app/engine/engine03.py`)
    -- esta función no altera ese comportamiento en absoluto, solo decide
    qué instancia de `MuGolProvider` inyectar.
    """
    return EngineRunner(
        engine01=Engine01(),
        engine02=Engine02(),
        engine03=Engine03(mu_gol_provider=mu_gol_provider or HistoricalMuGolProvider()),
        engine04=Engine04(),
        engine05=Engine05(),
        engine06=Engine06(),
    )


def construir_variable_preparation() -> VariablePreparation:
    """Instancia `VariablePreparation` (`app/preparation/preparation.py`,
    BUILD-017 a BUILD-024) con todos sus colaboradores por defecto -- ningún
    parámetro nuevo, ninguna variación de comportamiento respecto a
    invocarla directamente.
    """
    return VariablePreparation()


class EnginePipeline:
    """Orquestador oficial del tramo `VariablePreparation -> EngineRunner`
    (Misión INT-001) -- integra, sin modificarlos, los dos componentes ya
    completos de `docs/29-Arquitectura-del-Runtime.md` §2 que producen un
    `PredictionContext` completo hasta el final del Engine (`docs/29` §4):

    ```
    PredictionContext (ya construido: metadata + match, docs/30 §4.1-4.2)
            |
            v
    VariablePreparation  ──► agrega el bloque `variables` (una única vez)
            |
            v
    EngineRunner
            |
            +── Capa 1 (Engine01 + Engine02) ──► Fuerza Ofensiva / Defensiva
            |
            v
            Capa 2 (Engine03)                ──► Goles Esperados, Probabilidades
            |
            v
            Capa 3 (Engine04 + Engine05)      ──► Índice de Caos / Confianza
            |
            v
            Capa 4 (Engine06, condicional)    ──► Valor Esperado
            |
            v
    PredictionContext completo
    ```

    No construye el `PredictionContext` inicial (bloques `metadata`/`match`)
    -- eso sigue siendo responsabilidad de quien invoque este pipeline (ej.
    `PredictionRuntime._crear_contexto`, `BUILD-005`, sin cambios). No
    invoca Assembler ni Persistence (ver "Alcance exacto de este módulo" en
    el docstring del módulo) -- se detiene exactamente en el punto que pide
    el diagrama de esta misión.
    """

    def __init__(
        self,
        preparation: VariablePreparationProtocol | None = None,
        engine_runner: EngineRunnerProtocol | None = None,
    ) -> None:
        self._preparation = preparation or construir_variable_preparation()
        self._engine_runner = engine_runner or construir_engine_runner()

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Ejecuta `VariablePreparation` **una única vez** y, si tuvo éxito,
        `EngineRunner` -- nunca al revés, nunca en paralelo, nunca más de
        una vez (Obligación 1/4 del brief de INT-001: orden fijo,
        "prohibido recalcular Variables Oficiales desde los motores").

        Si `VariablePreparation` falla, `EngineRunner` **no se invoca en
        absoluto** -- ninguno de los 6 motores se ejecuta sin
        `context.variables` ya construido (Obligación 5: "detener
        únicamente las etapas posteriores que dependan del componente
        fallido"; los 6 motores dependen, todos, de `context.variables`,
        `docs/17`). El fallo queda registrado en `context.errors`
        (`ErrorEntry`, `docs/30` §4.8) -- nunca se lanza sin registrar
        (Obligación 5).

        Devuelve el mismo `context` recibido, mutado in-place por sus dos
        colaboradores -- ninguna sección ya escrita se reabre, recalcula ni
        elimina (principio append-only, `docs/30`, `BUILD-004`); este
        método en sí mismo nunca escribe directamente en `context`, solo
        invoca a quienes ya tienen esa autorización.
        """
        if not self._invocar_preparation(context):
            return context  # detenido antes del Engine -- ningún motor se ejecuta

        self._invocar_engine_runner(context)
        return context

    def _invocar_preparation(self, context: PredictionContext) -> bool:
        """Único punto de entrada para invocar `VariablePreparation`. Mismo
        patrón de manejo de errores ya validado por `PredictionRuntime.
        _invocar_preparation` (`app/runtime/runtime.py`, BUILD-005) -- no
        reutilizado directamente porque ese método es privado de una clase
        acoplada a `Persistence`, fuera del alcance de esta misión; se
        reimplementa aquí como una pieza equivalente e independiente, sin
        modificar `runtime.py`.
        """
        try:
            self._preparation.preparar(context)
        except Exception as exc:  # captura amplia intencional -- ningún fallo se propaga sin registro
            self._registrar_error(context, "VariablePreparation", "Fase 3 (Preparación)", exc)
            return False
        return True

    def _invocar_engine_runner(self, context: PredictionContext) -> None:
        """`EngineRunner.ejecutar` ya registra sus propios errores por capa
        y detiene las capas siguientes internamente (`app/engine/engine_
        runner.py`, BUILD-007, sin cambios) -- este método solo blinda
        contra un fallo no previsto en la propia invocación (ej. un motor
        que ni siquiera pueda ejecutarse por un error ajeno a los ya
        capturados en `_ejecutar_capa`), sin duplicar esa lógica interna.
        """
        try:
            self._engine_runner.ejecutar(context)
        except Exception as exc:  # captura amplia intencional -- ver docstring del método
            self._registrar_error(context, "EngineRunner", "Fase 3 (Engine)", exc)

    @staticmethod
    def _registrar_error(context: PredictionContext, componente: str, capa_fase: str, exc: Exception) -> None:
        """Único punto de registro de anomalías de este orquestador --
        mismo patrón exacto ya usado en `EngineRunner._registrar_error` y
        `PredictionRuntime._registrar_error` (ambos sin modificar).
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


def construir_pipeline_oficial(mu_gol_provider: MuGolProvider | None = None) -> EnginePipeline:
    """Punto de composición único y oficial (INT-001): construye
    `EnginePipeline` con `VariablePreparation` y `EngineRunner` ya wireados
    con los 6 motores concretos. Es la función que responde, en código, a
    "¿qué componente quedó como orquestador oficial del Engine?" -- su
    resultado (`EnginePipeline`) es ese orquestador; esta función es,
    simplemente, la forma más simple de obtenerlo con sus valores por
    defecto ya oficiales.
    """
    return EnginePipeline(
        preparation=construir_variable_preparation(),
        engine_runner=construir_engine_runner(mu_gol_provider),
    )
