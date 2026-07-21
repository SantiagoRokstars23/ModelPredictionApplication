"""Paquete runtime -- coordinador de la ejecucion.

Materializa, sin redefinirlos, el Runtime y sus siete componentes ya
disenados en docs/26-Runtime-del-Modelo.md y docs/29-Arquitectura-del-Runtime.md
(PredictionRequest, PredictionContext, VariablePreparation, EngineRunner,
PredictionAssembler, PredictionReport, Persistence).

Responsabilidad (docs/35, seccion 4): construir el PredictionContext y
coordinar VariablePreparation -> EngineRunner -> PredictionAssembler ->
Persistence, en ese orden fijo. Nunca ejecuta SQL ni conoce FastAPI.

BUILD-004: implementado `PredictionContext` (prediction_context.py) -- la
representación oficial de docs/30, con sus diez bloques.

BUILD-005: implementado `PredictionRuntime` (runtime.py) -- el coordinador
que construye el `PredictionContext` e invoca, por inyección de
dependencias, las interfaces (`Protocol`) de `VariablePreparation`,
`EngineRunner` y `Persistence`. Ninguna lógica interna de esos tres
componentes está implementada todavía -- solo sus puntos de invocación.
"""

from app.runtime.prediction_context import (
    AuditBlock,
    BankrollBlock,
    EngineBlock,
    ErrorEntry,
    EstadoEjecucion,
    LearningBlock,
    MarketBlock,
    MatchBlock,
    MetadataBlock,
    PredictionBlock,
    PredictionContext,
    VariablesBlock,
)
from app.runtime.runtime import (
    EngineRunnerProtocol,
    PersistenceProtocol,
    PredictionRequestLike,
    PredictionRuntime,
    VariablePreparationProtocol,
)

__all__ = [
    "AuditBlock",
    "BankrollBlock",
    "EngineBlock",
    "EngineRunnerProtocol",
    "ErrorEntry",
    "EstadoEjecucion",
    "LearningBlock",
    "MarketBlock",
    "MatchBlock",
    "MetadataBlock",
    "PersistenceProtocol",
    "PredictionBlock",
    "PredictionContext",
    "PredictionRequestLike",
    "PredictionRuntime",
    "VariablePreparationProtocol",
    "VariablesBlock",
]
