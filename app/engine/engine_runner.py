"""`EngineRunner` -- coordina la ejecución de los 6 motores por capas.

Ver docs/06-Flujo-Operacional.md ("Diagrama de dependencias del Engine"),
docs/17-Matriz-de-Consumo-de-Variables.md (qué motor consume la salida de
cuál), docs/29-Arquitectura-del-Runtime.md (el componente `EngineRunner`,
sección 2/4), docs/26-Runtime-del-Modelo.md §8 (manejo de errores: "las
capas siguientes tampoco se ejecutan").

BUILD-007: implementa `EngineRunner`, que satisface `EngineRunnerProtocol`
(`app/runtime/runtime.py`, BUILD-005) mediante tipado estructural -- sin
heredar de él, sin modificarlo. Coordina únicamente el orden de ejecución;
no calcula, no consulta la base de datos, no contiene lógica de negocio.
Ninguno de los seis motores inyectados se implementa aquí -- solo sus
interfaces (`Engine01Protocol` a `Engine06Protocol`), exactamente igual que
BUILD-005 hizo con `VariablePreparationProtocol`/`PersistenceProtocol` y
BUILD-006 con `PreparationRepositoryProtocol`.

## Paralelismo: documentado, no implementado

Capa 1 (`Engine01`+`Engine02`) y Capa 3 (`Engine04`+`Engine05`) son, por
diseño arquitectónico (`docs/06`), pares de motores independientes entre sí
-- ninguno depende de la salida del otro. Esta misión los ejecuta de forma
estrictamente secuencial (una llamada después de la otra, en el mismo
hilo) -- **no implementa concurrencia real** (`asyncio`, hilos, procesos),
conforme a la restricción explícita de BUILD-007. El lugar exacto donde una
futura misión podría introducir paralelismo real está señalado con un
comentario en `_ejecutar_capa`, condicionado a que exista evidencia real de
que la latencia lo justifique (`CLAUDE.md`: evitar complejidad sin
evidencia de que mejora el modelo).

## Excepción heredada, no resuelta aquí: `Engine06`

`docs/06`, Fase 4, documenta que `engine/06-Expected-Value.md` es
**condicional** -- solo se ejecuta si existen cuotas y un mercado fue
solicitado; su ausencia nunca es un fallo, es una omisión esperada. Esta
misión no implementa esa distinción (requeriría leer `context.market` y
decidir si corresponde invocar `Engine06Protocol`, una decisión más cercana
a lógica de negocio que a "coordinar el orden de ejecución"): `Engine06` se
trata aquí de forma genérica, igual que los otros cinco motores. Se
documenta como simplificación de esta misión, no como una corrección de
`docs/06`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from app.runtime.prediction_context import ErrorEntry, PredictionContext


class MotorProtocol(Protocol):
    """Forma estructural común a los seis motores -- usada únicamente para
    tipar la lista heterogénea de `_ejecutar_capa`; los seis `Protocol`
    específicos (`Engine01Protocol` a `Engine06Protocol`) son los que se
    exponen en el constructor de `EngineRunner`, conforme a lo pedido por
    esta misión.
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        ...


class Engine01Protocol(Protocol):
    """Interfaz de invocación de engine/01-Offensive-Strength.md."""

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Debe agregar `context.engine.engine01` (docs/30 §4.4)."""
        ...


class Engine02Protocol(Protocol):
    """Interfaz de invocación de engine/02-Defensive-Strength.md."""

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Debe agregar `context.engine.engine02` (docs/30 §4.4)."""
        ...


class Engine03Protocol(Protocol):
    """Interfaz de invocación de engine/03-Poisson.md."""

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Debe agregar `context.engine.engine03` (docs/30 §4.4)."""
        ...


class Engine04Protocol(Protocol):
    """Interfaz de invocación de engine/04-Chaos-Index.md."""

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Debe agregar `context.engine.engine04` (docs/30 §4.4)."""
        ...


class Engine05Protocol(Protocol):
    """Interfaz de invocación de engine/05-Confidence.md."""

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Debe agregar `context.engine.engine05` (docs/30 §4.4)."""
        ...


class Engine06Protocol(Protocol):
    """Interfaz de invocación de engine/06-Expected-Value.md (condicional,
    Fase 4 -- ver nota de la excepción heredada en el encabezado del módulo).
    """

    def ejecutar(self, context: PredictionContext) -> PredictionContext:
        """Debe agregar `context.engine.engine06` (docs/30 §4.4)."""
        ...


class EngineRunner:
    """Coordina la ejecución de los 6 motores, por capas, exactamente en el
    orden ya fijado por `docs/06`/`docs/17`/`docs/29`. Satisface
    `EngineRunnerProtocol` (`app/runtime/runtime.py`, BUILD-005) mediante
    tipado estructural.

    Recibe los seis motores por inyección de dependencias, tipados como
    interfaces (`Protocol`) -- ninguna implementación concreta de ningún
    motor se importa ni se instancia aquí.
    """

    def __init__(
        self,
        engine01: Engine01Protocol,
        engine02: Engine02Protocol,
        engine03: Engine03Protocol,
        engine04: Engine04Protocol,
        engine05: Engine05Protocol,
        engine06: Engine06Protocol,
    ) -> None:
        self._engine01 = engine01
        self._engine02 = engine02
        self._engine03 = engine03
        self._engine04 = engine04
        self._engine05 = engine05
        self._engine06 = engine06

    def ejecutar(self, context: PredictionContext) -> None:
        """Ejecuta las 4 capas en orden fijo (docs/06, "Diagrama de
        dependencias del Engine"). Si una capa falla (cualquiera de sus
        motores), las capas siguientes no se ejecutan (`docs/26` §8: "las
        capas siguientes tampoco se ejecutan").
        """
        capa_1_ok = self._ejecutar_capa(
            context, [(self._engine01, "engine01"), (self._engine02, "engine02")], "Capa 1"
        )
        if not capa_1_ok:
            return

        capa_2_ok = self._ejecutar_capa(context, [(self._engine03, "engine03")], "Capa 2")
        if not capa_2_ok:
            return

        capa_3_ok = self._ejecutar_capa(
            context, [(self._engine04, "engine04"), (self._engine05, "engine05")], "Capa 3"
        )
        if not capa_3_ok:
            return

        self._ejecutar_capa(context, [(self._engine06, "engine06")], "Capa 4")

    def _ejecutar_capa(
        self,
        context: PredictionContext,
        motores: list[tuple[MotorProtocol, str]],
        nombre_capa: str,
    ) -> bool:
        """Ejecuta todos los motores de una capa.

        Un motor que falla no bloquea a otro motor de la **misma** capa
        (son independientes entre sí, `docs/06` -- ver nota de paralelismo
        en el encabezado del módulo: aquí se ejecutan secuencialmente, no en
        paralelo real). Si **cualquiera** de los motores de esta capa falla,
        la capa se considera fallida y bloquea la capa siguiente.

        (Nota: este es, precisamente, el punto donde una futura misión
        podría reemplazar el bucle secuencial por ejecución concurrente real
        de los motores de una misma capa, sin cambiar la interfaz pública de
        `EngineRunner.ejecutar`.)
        """
        exito_capa = True
        for motor, nombre in motores:
            try:
                motor.ejecutar(context)
            except Exception as exc:  # captura amplia intencional: todo fallo se
                # registra, nunca se propaga sin dejar rastro (docs/26 §7)
                self._registrar_error(context, nombre, nombre_capa, exc)
                exito_capa = False
        return exito_capa

    def _registrar_error(
        self, context: PredictionContext, componente: str, capa_fase: str, exc: Exception
    ) -> None:
        """Único punto de entrada para registrar una anomalía en el bloque
        `errors` (docs/30 §4.8) -- mismo patrón ya usado en
        `PredictionRuntime._registrar_error` (`app/runtime/runtime.py`,
        BUILD-005), no importado desde allí para no acoplar `app/engine` a
        `app/runtime` más allá del propio `PredictionContext` (docs/35,
        sección 6: "Engine nunca conoce... ningún otro paquete de `app/`"
        salvo el propio contrato de datos).
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
