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

BUILD-012: implementado `Engine03` (engine03.py) -- primer motor
probabilístico completo (`models/poisson.md`), satisface
`Engine03Protocol`. Consume `Engine01Salida`/`Engine02Salida` (bipartitas
desde `BUILD-010`/`BUILD-011`) más Variable009 (Localía) directamente,
autorizado explícitamente por el usuario tras detectar que el brief
original lo prohibía, contradiciendo `docs/06`/`docs/17`/`models/poisson.md`.
Acepta un `MuGolProvider` inyectable (mismo patrón que
`PreparationRepositoryProtocol` de `app/preparation`); sin implementación
real todavía -- Engine03 se detiene si no se inyecta uno.

BUILD-013: implementado `Engine04` (engine04.py) -- primer motor de la
Capa 3 (`models/chaos-index.md`), satisface `Engine04Protocol`. Consume
`context.engine.engine03` (entropía de Shannon de la distribución L/E/V)
más Variable006/007 directamente desde `context.variables`, autorizado
explícitamente por el usuario tras detectar que el brief original
restringía las entradas a únicamente `context.engine.engine03`,
contradiciendo `docs/06`/`docs/17`/`models/chaos-index.md` §7.2 (mismo
patrón de contradicción ya resuelto en `BUILD-012`). Variable001
(inestabilidad de forma) y Variable012 (Factores Externos, ausente del
esquema de `VariablesBlock`) quedan como términos estructurales sin dato
real -- ver docstring de `engine04.py`. `EntradaFaltante` se re-exporta con
alias por motor (mismo patrón ya aplicado a `VariableObligatoriaNoDisponible`
en `Engine01`/`Engine02`) porque `Engine03` y `Engine04` declaran, cada uno,
su propia clase con ese nombre.

BUILD-014: implementado `Engine05` (engine05.py) -- segundo motor de la
Capa 3 (`models/confidence.md`), satisface `Engine05Protocol`. Consume
`context.engine.engine01`/`engine02` (indirecto), confirma ejecución de
`context.engine.engine03` sin leer su valor (`models/confidence.md` §8),
y lee Variable006/007/010 directamente desde `context.variables`
(autorizado por `docs/17`). Dos contradicciones detectadas entre `docs/17`
y `models/confidence.md`, reportadas y resueltas por decisión explícita del
usuario (no unilateralmente): (1) `C_forma` exige varianza de Variable001,
que `docs/17` clasifica como indirecta para `engine/05` y que no existe en
`VariablesBlock` -- queda fija en `1.0` (neutral), sin leer Variable001; (2)
`C_datos` exige el estado de "cada Variable Oficial", pero `docs/17` solo
autoriza 3 variables directas -- se amplía combinando esas 3 con la
completitud ya publicada por `Engine01Salida`/`Engine02Salida`
(`variables_utilizadas`/`variables_descartadas`), sin releer variables
indirectas. `EntradaFaltante` de `Engine05` se re-exporta con alias, mismo
patrón que `Engine03`/`Engine04`.

BUILD-015: implementado `Engine06` (engine06.py) -- último motor del
Engine, cierra la Capa 4 (`models/expected-value.md`), satisface
`Engine06Protocol`. Consume `context.engine.engine03`/`engine04`/`engine05`
(indirecto) y `context.market.cuotas` (condicional -- si no hay cuotas,
`context.engine.engine06` permanece `None`, sin error). Ninguna
contradicción bloqueante entre documentos (a diferencia de `BUILD-013`/
`BUILD-014`) -- solo brechas de dato/calibración documentadas como
placeholders (ver docstring de `engine06.py`): siete de los nueve mercados
de `engine/06` no tienen `P_modelo` calculable por ningún motor del Engine
(se descartan, nunca se inventa una probabilidad); los umbrales de
clasificación de EV no tienen ninguna cita numérica en `models/expected-
value.md` (placeholder más débil de todo el Engine). `EntradaFaltante` de
`Engine06` se re-exporta con alias, mismo patrón que `Engine03`-`05`.
"""

from app.engine.engine01 import Engine01
from app.engine.engine01 import VariableObligatoriaNoDisponible as Engine01VariableObligatoriaNoDisponible
from app.engine.engine02 import Engine02
from app.engine.engine02 import VariableObligatoriaNoDisponible as Engine02VariableObligatoriaNoDisponible
from app.engine.engine03 import Engine03, MuGolNoDisponible, MuGolProvider
from app.engine.engine03 import EntradaFaltante as Engine03EntradaFaltante
from app.engine.engine04 import Engine04
from app.engine.engine04 import EntradaFaltante as Engine04EntradaFaltante
from app.engine.engine05 import Engine05
from app.engine.engine05 import EntradaFaltante as Engine05EntradaFaltante
from app.engine.engine06 import Engine06
from app.engine.engine06 import EntradaFaltante as Engine06EntradaFaltante
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
    "Engine03",
    "Engine03EntradaFaltante",
    "Engine03Protocol",
    "Engine04",
    "Engine04EntradaFaltante",
    "Engine04Protocol",
    "Engine05",
    "Engine05EntradaFaltante",
    "Engine05Protocol",
    "Engine06",
    "Engine06EntradaFaltante",
    "Engine06Protocol",
    "EngineRunner",
    "MotorProtocol",
    "MuGolNoDisponible",
    "MuGolProvider",
]
