"""`predict_controller` -- primer endpoint HTTP del Modelo Santiago
(Misión BUILD-026): expone `POST /predict`, el único punto de entrada web
que invoca `PredictMatchUseCase` (`app/application`, BUILD-025).

Referencias releídas antes de escribir este módulo: `docs/25-Trazado-de-
Ejecucion-del-Prediction-Pipeline.md` §1 (forma de los datos mínimos de un
partido), `docs/30-Contrato-Oficial-del-Prediction-Context.md` §4.2 (campos
obligatorios de `MatchBlock`, ya verificados en `BUILD-025`), `docs/35-
Arquitectura-Oficial-del-Proyecto-Python.md` (responsabilidad de `app/api`:
"recibir la solicitud HTTP... invocar `app/runtime`... nunca calcular una
probabilidad"), `app/application/predict_match.py` (BUILD-025,
`PredictMatchUseCase`, única lógica reutilizada aquí), `app/main.py`
(BUILD-001, la app FastAPI vacía sobre la que este router aún no se monta
-- ver "Hallazgo" más abajo).

## Qué hace este módulo, en orden exacto (el mismo que exige el brief)

```
POST /predict  (JSON: id_partido, seleccion_local, seleccion_visitante,
                competicion, torneo, fecha, estadio opcional)
        │
        ▼
Leer el cuerpo JSON como dict -- ningún esquema Pydantic propio (ver
"Por qué `dict`, no un modelo de request" más abajo)
        │
        ▼
Convertir `fecha` (string ISO) a `datetime.date` -- único ajuste de tipo
necesario para satisfacer la firma ya existente de `PredictMatchUseCase.
execute` (BUILD-025, no modificada aquí)
        │
        ▼
PredictMatchUseCase(version_modelo=...).execute(...)
        │
        ▼
PredictionContext (mutado por EnginePipeline -> EngineRunner -> Engine01..06,
                    incluidos sus propios `errors` si algo falló, INT-001)
        │
        ▼
context.model_dump(mode="json")  -- serialización nativa de Pydantic,
                                     ninguna estructura nueva inventada
        │
        ▼
Respuesta JSON
```

Nada más ocurre en este módulo -- ni cálculo, ni recalculo de Variables
Oficiales, ni lógica de negocio, ni un servicio o repositorio nuevo (todos
explícitamente prohibidos por el brief). Toda la ejecución real pertenece,
sin excepción, a `PredictMatchUseCase` y a lo que este ya orquesta
(`EnginePipeline`, `EngineRunner`, `VariablePreparation`, `Engine01`-`06`,
todos sin modificar).

## Por qué `dict`, no un modelo de request propio

El brief prohíbe explícitamente "diseñar un DTO" para la respuesta, y el
flujo exigido es literalmente "leer JSON... nada más" -- crear una clase
`BaseModel` nueva para validar el cuerpo de la solicitud sería, en espíritu,
la misma clase de estructura que el brief pide evitar (aunque técnicamente
solo mencione la respuesta). Se usa el mecanismo más simple que FastAPI ya
ofrece sin ninguna definición adicional: un parámetro anotado como `dict`,
que FastAPI reconoce automáticamente como el cuerpo JSON de la solicitud,
sin declarar ningún esquema propio. Los campos requeridos se leen por
indexación directa (`payload["campo"]`) -- si faltan, la solicitud falla
con el error nativo de Python/FastAPI (`KeyError` -> 500), nunca con una
excepción propia inventada por este módulo (restricción explícita del
brief: "No lanzar excepciones propias"). `estadio` es el único campo
opcional (`payload.get("estadio")`, `None` si se omite) -- consistente con
la firma ya existente de `PredictMatchUseCase.execute` (BUILD-025).

## Manejo de errores -- exactamente lo que pide el brief, nada agregado

`context.errors` (una lista de `ErrorEntry`, `docs/30` §4.8) ya queda
poblado por `EnginePipeline`/`EngineRunner`/`VariablePreparation` cuando
algo falla (`INT-001`, `BUILD-007`, `BUILD-017` a `024`) -- este controlador
no necesita ninguna lógica adicional para que esos errores "aparezcan en la
respuesta": al serializar el `PredictionContext` completo con
`model_dump(mode="json")`, `errors` viaja como cualquier otro campo, sin
ningún tratamiento especial. No se envuelve la llamada a `execute` en un
`try/except` propio -- duplicaría una responsabilidad que ya existe
(prohibido explícitamente: "No lanzar excepciones propias").

## Hallazgo explícito: este router no queda montado en `app/main.py`

El brief restringe los archivos permitidos a `app/api/__init__.py` y
`app/api/predict_controller.py` (más `CHANGELOG.md`/`docs/00-Project-
Tracker.md` "si es imprescindible") -- `app/main.py` no aparece en esa
lista. Sin `app.include_router(router)` en `app/main.py`, `POST /predict`
no es alcanzable por un servidor real todavía, aunque el router en sí
(`router`, definido abajo) es completamente funcional e importable. Se deja
como hallazgo documentado, no como un descuido: montar este router en
`app/main.py` (una línea, `app.include_router(router)`) queda para una
futura misión explícitamente autorizada a modificar ese archivo.

## `version_modelo` -- mismo hallazgo de configuración ya heredado de BUILD-025

`PredictMatchUseCase.__init__` (BUILD-025) exige `version_modelo: str` sin
valor por defecto, deliberadamente, para nunca inventar una versión no
provista. Este controlador necesita, igualmente, proveer un valor real para
poder invocarlo -- no existe hoy ninguna fuente de configuración para esto
(`app/config/settings.py` no la declara, y crear una queda fuera del
alcance de archivos permitidos de esta misión). Se usa la última versión
citada textualmente en `docs/11-Versiones.md` ("v1.3") como constante de
módulo, documentada explícitamente como placeholder -- no inventada, citada
de la única fuente de versiones ya existente en el proyecto.
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter

from app.application.predict_match import PredictMatchUseCase

router = APIRouter()

VERSION_MODELO = "v1.3"
"""Última versión citada textualmente en `docs/11-Versiones.md` -- placeholder
documentado (ver "`version_modelo`" en el docstring del módulo), no una
calibración ni un valor inventado. Requiere una fuente de configuración real
en una futura misión con acceso a `app/config/`.
"""


@router.post("/predict")
def predict(payload: dict) -> dict:
    """Único endpoint de esta misión -- `POST /predict`. Ver el docstring
    del módulo para el flujo completo y las decisiones de diseño. Nunca
    calcula, nunca recalcula Variables Oficiales, nunca contiene lógica de
    negocio -- reutiliza exclusivamente `PredictMatchUseCase` (BUILD-025).
    """
    fecha = date.fromisoformat(payload["fecha"])

    use_case = PredictMatchUseCase(version_modelo=VERSION_MODELO)
    context = use_case.execute(
        id_partido=payload["id_partido"],
        seleccion_local=payload["seleccion_local"],
        seleccion_visitante=payload["seleccion_visitante"],
        competicion=payload["competicion"],
        torneo=payload["torneo"],
        fecha=fecha,
        estadio=payload.get("estadio"),
    )

    return context.model_dump(mode="json")
