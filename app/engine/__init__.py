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

BUILD-009: implementado `Engine01` (engine01.py) -- primer motor con
cálculo matemático real (`models/offensive-strength.md`), satisface
`Engine01Protocol`. Únicamente Fuerza Ofensiva (Fuerza Defensiva pertenece
a `engine/02`, todavía sin implementar -- ver "Contradicción #1" en
engine01.py). Bloqueo arquitectónico documentado, no resuelto en esa
misión: `Engine01Salida` (un único `float`) no podía publicar `FO_local`/
`FO_visitante` simultáneamente -- ver "Contradicción #2" en engine01.py.

BUILD-010 (tras GR-009): `Engine01` ya publica `context.engine.engine01`
con la estructura bipartita aprobada (`Engine01Salida`/`Engine01SalidaEquipo`,
`app/runtime/prediction_context.py`, `docs/30` v2.0.0 §4.4.1) -- el
bloqueo de publicación quedó resuelto; `PublicacionBloqueadaPorEsquema`
dejó de existir (ya no se lanza ninguna excepción propia de bloqueo).

BUILD-011: implementado `Engine02` (engine02.py) -- segundo motor con
cálculo matemático real (`models/defensive-strength.md`), satisface
`Engine02Protocol`, mismo patrón exacto que `Engine01`. Reutiliza sin
redefinir los pesos `M_forma`/`Pen` ya usados por `engine01`
(`models/defensive-strength.md` §6.1). Ya publica `context.engine.engine02`
con la estructura bipartita (`Engine02Salida`/`Engine02SalidaEquipo`) --
esta misión detectó que `Engine02Salida` (a diferencia de `Engine01Salida`)
seguía sin actualizar tras `BUILD-010` (fuera de su alcance en ese
momento), y el usuario autorizó explícitamente ampliar el alcance de
`BUILD-011` a `app/runtime/prediction_context.py` para aplicarle el mismo
cambio ya validado. `Engine01` y `Engine02` declaran, cada uno en su
propio módulo, una clase `VariableObligatoriaNoDisponible` distinta (no
son intercambiables: una se refiere a Variable003, la otra a Variable004)
-- este paquete las re-exporta con un alias por motor para evitar que una
oculte a la otra.
"""

from app.engine.engine01 import Engine01
from app.engine.engine01 import VariableObligatoriaNoDisponible as Engine01VariableObligatoriaNoDisponible
from app.engine.engine02 import Engine02
from app.engine.engine02 import VariableObligatoriaNoDisponible as Engine02VariableObligatoriaNoDisponible
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
    "Engine01",
    "Engine01Protocol",
    "Engine01VariableObligatoriaNoDisponible",
    "Engine02",
    "Engine02Protocol",
    "Engine02VariableObligatoriaNoDisponible",
    "Engine03Protocol",
    "Engine04Protocol",
    "Engine05Protocol",
    "Engine06Protocol",
    "EngineRunner",
    "MotorProtocol",
]
