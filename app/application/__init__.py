"""Paquete `application` -- Capa de Aplicación del Modelo Santiago.

Primer paquete que expone un caso de uso completo del dominio: conecta
`PredictionContext` con el `EnginePipeline` oficial (`app/runtime/
engine_pipeline.py`, `INT-001`) mediante un único punto de entrada, sin
controladores, sin API, sin persistencia.

No estaba anticipado por el árbol de paquetes original de `docs/35-
Arquitectura-Oficial-del-Proyecto-Python.md` -- ver "Por qué vive en un
paquete nuevo" en el docstring de `predict_match.py` para la justificación
completa de por qué no se ubicó en `app/services` (que existe,
deliberadamente, fuera del camino crítico del Runtime).

BUILD-025: implementa `PredictMatchUseCase` (`predict_match.py`) -- primer
caso de uso oficial, sin modificar `PredictionContext`, `PredictionRuntime`,
`EnginePipeline`, `EngineRunner`, `VariablePreparation`, `Engine01`-`06` ni
`RuntimePersistence`.
"""

from app.application.predict_match import PredictMatchUseCase

__all__ = ["PredictMatchUseCase"]
