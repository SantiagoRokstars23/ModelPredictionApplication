"""Paquete engine -- los 6 motores del Engine, en codigo.

Distinto del directorio raiz `engine/` (especificacion en Markdown de cada
motor -- engine/01-Offensive-Strength.md a engine/06-Expected-Value.md --
que permanece sin cambios). Ver docs/35-Arquitectura-Oficial-del-Proyecto-Python.md,
"Aclaracion de nomenclatura".

Responsabilidad (docs/35, seccion 4 y 6): ejecutar la logica matematica de
los 6 motores, una vez tengan Version 2.0 calibrada en el directorio raiz
`models/` (ver models/parameter-calibration.md, MODEL-008). Es el unico
paquete de todo el proyecto sin ninguna dependencia interna de infraestructura:
nunca conoce FastAPI, SQLAlchemy, PostgreSQL ni ningun otro paquete de app/ --
su unica entrada es el PredictionContext (docs/30-Contrato-Oficial-del-Prediction-Context.md).

BUILD-007: implementado `EngineRunner` (engine_runner.py), que coordina la
ejecucion de los 6 motores por capas (docs/06/docs/17/docs/29) -- ningun
motor concreto (Offensive Strength, Poisson, etc.) esta implementado
todavia, solo sus interfaces (`Engine01Protocol` a `Engine06Protocol`).
Paralelismo de Capa 1 (Engine01+02) y Capa 3 (Engine04+05) documentado, no
implementado -- ejecucion secuencial en este bootstrap. La condicionalidad
de `Engine06` (Fase 4, solo si hay cuotas) tampoco esta implementada -- se
trata de forma generica junto a los otros cinco motores (ver nota en
engine_runner.py).
"""

from app.engine.engine_runner import (
    Engine01Protocol,
    Engine02Protocol,
    Engine03Protocol,
    Engine04Protocol,
    Engine05Protocol,
    Engine06Protocol,
    EngineRunner,
    MotorProtocol,
)

__all__ = [
    "Engine01Protocol",
    "Engine02Protocol",
    "Engine03Protocol",
    "Engine04Protocol",
    "Engine05Protocol",
    "Engine06Protocol",
    "EngineRunner",
    "MotorProtocol",
]
