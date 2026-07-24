"""`PredictMatchUseCase` -- primer caso de uso oficial de la capa de
aplicación (Misión BUILD-025): conecta, mediante un único punto de entrada,
`PredictionContext` -> `EnginePipeline` -> `VariablePreparation` ->
`EngineRunner` -> `Engine01`...`Engine06`.

Referencias releídas antes de escribir este módulo: `docs/25-Trazado-de-
Ejecucion-del-Prediction-Pipeline.md` §1 (`PredictionRequest`, forma de los
datos mínimos de un partido), `docs/29-Arquitectura-del-Runtime.md` §3
(quién escribe cada sección del `PredictionContext`), `docs/30-Contrato-
Oficial-del-Prediction-Context.md` §4.1-4.2 (`MetadataBlock`/`MatchBlock`,
campos obligatorios vs. opcionales), `docs/35-Arquitectura-Oficial-del-
Proyecto-Python.md` (matriz de dependencias entre paquetes de `app/`),
`app/runtime/prediction_context.py` (BUILD-004, `PredictionContext`,
`MetadataBlock`, `MatchBlock`), `app/runtime/engine_pipeline.py` (INT-001,
`EnginePipeline`, `construir_pipeline_oficial`), `app/runtime/runtime.py`
(BUILD-005, `PredictionRuntime._crear_contexto`, mismo patrón de
construcción de `metadata`/`match` que este módulo reutiliza sin
modificarlo).

## Hallazgo explícito: el brief lista 5 "datos mínimos", el esquema exige 7

El brief de esta misión pide llenar únicamente "selección local, selección
visitante, competición, estadio, fecha" -- pero `MatchBlock` (`app/runtime/
prediction_context.py`, sección 4.2 de `docs/30`, **no modificable por esta
misión**) declara `id_partido` y `torneo` como campos **obligatorios**, sin
valor por defecto -- distintos de `competicion` (la competición general,
ej. "Copa América") y ya usados activamente por múltiples Variables
Oficiales (`context.match.torneo` resuelve el `id_torneo` específico para
Variable002/006/007/008, `MODEL-012`/`013`/`014`/`015`). Omitirlos haría que
`MatchBlock(...)` fallara con un error de validación de Pydantic en **toda**
invocación de `execute(...)` -- no una omisión menor, sino un caso de uso
que nunca podría ejecutarse. **Resolución, sin inventar ningún dato:**
`id_partido` y `torneo` se agregan como parámetros explícitos y obligatorios
de `execute(...)`, exactamente igual que los cinco ya nombrados por el
brief -- ambos siguen siendo "datos mínimos conocidos" del partido (`docs/25`
§1 ya los incluye en `PredictionRequest`), simplemente no listados en el
resumen abreviado del brief. Ningún valor se genera ni se asume: si el
llamador no los provee, la llamada falla explícitamente (`TypeError` de
Python, argumento faltante), nunca con un valor inventado. `hora_local`/
`arbitro` (los dos únicos campos restantes de `MatchBlock`, ambos ya
opcionales con valor por defecto `None` en el esquema) se dejan sin tocar,
respetando literalmente el "nada más" del brief -- ninguno de los dos se
agrega como parámetro de `execute(...)`.

## Qué hace este caso de uso, en orden exacto

```
PredictMatchUseCase.execute(id_partido, seleccion_local, seleccion_visitante,
                             competicion, torneo, fecha, estadio=None)
        │
        ▼
Construye PredictionContext (metadata + match únicamente -- "vacío" en el
mismo sentido que PredictionRuntime._crear_contexto, BUILD-005, sin
imitarlo por importación: mismo patrón, implementación propia e
independiente, sin modificar runtime.py)
        │
        ▼
construir_pipeline_oficial()  ──► EnginePipeline (INT-001), sin argumentos,
                                    exactamente como exige el brief
        │
        ▼
pipeline.ejecutar(context)  ──► VariablePreparation (una vez) -> EngineRunner
                                 -> Engine01...Engine06, por capas
        │
        ▼
return context  ──► el mismo PredictionContext, mutado in-place por sus
                     colaboradores -- ningún DTO, ningún ResponseModel,
                     ningún JSON, ninguna transformación
```

## Qué NO hace este módulo (restricciones explícitas del brief, todas verificadas)

No modifica `PredictionContext`, `PredictionRuntime`, `EnginePipeline`,
`EngineRunner`, `VariablePreparation`, `Engine01`-`06` ni `RuntimePersistence`
-- ninguno de esos archivos se toca. No persiste, no serializa, no formatea,
no convierte, no imprime, no agrega logging adicional. No captura errores
del Engine -- `EnginePipeline.ejecutar`/`EngineRunner`/`VariablePreparation`
ya registran sus propios fallos como `ErrorEntry` en `context.errors`
(`INT-001`, `BUILD-005`, `BUILD-007`, `BUILD-017` a `024`); envolver esa
llamada en un `try/except` propio duplicaría una responsabilidad que ya
existe, prohibido explícitamente por el brief ("Todo eso ya existe"). No
carga cuotas (`context.market` permanece `None`, el valor por defecto del
esquema -- Engine06 ya trata su ausencia como el caso condicional "Completa
sin Valor Esperado", sin cambios). No carga resultados. No crea
controladores, FastAPI, CLI, scripts ni pruebas. No implementa DTOs ni
ResponseModels -- el método devuelve el `PredictionContext` mismo, el
objeto interno de ejecución, tal como el brief exige explícitamente ("No
DTO. No ResponseModel. No JSON.").

## Por qué vive en un paquete nuevo (`app/application`), no en uno existente

`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md` no anticipaba este
paquete en su árbol original -- listaba `app/api`, `app/runtime`,
`app/engine`, `app/preparation`, `app/persistence`, `app/models`,
`app/schemas`, `app/services`, `app/config`. `app/services` no es el lugar
correcto: ese paquete existe, por diseño, **fuera** del camino crítico del
Runtime ("se ejecutan antes o después, nunca dentro", `docs/35` sección 5) --
mientras que `PredictMatchUseCase` es, precisamente, quien inicia ese camino
crítico. Esta misión (`BUILD-025`) autoriza explícitamente crear
`app/application/` como el paquete de Capa de Aplicación que años de
arquitectura hexagonal/limpia reconocerían como el punto de entrada al
dominio -- un caso de uso, no un servicio periférico. No se modifica
`docs/35` en esta misión (fuera de alcance: "no crear documentación");
queda como hallazgo documentado para una futura actualización editorial de
ese documento.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from app.runtime.engine_pipeline import construir_pipeline_oficial
from app.runtime.prediction_context import MatchBlock, MetadataBlock, PredictionContext


class PredictMatchUseCase:
    """Primer caso de uso oficial de `app/application` -- conecta
    `PredictionContext` con el `EnginePipeline` oficial (`INT-001`) mediante
    un único método público (`execute`). No calcula nada por sí mismo: toda
    la lógica matemática pertenece, sin excepción, a `VariablePreparation` y
    a los 6 motores, invocados a través de `EnginePipeline` sin
    modificarlo.
    """

    def __init__(self, version_modelo: str) -> None:
        """`version_modelo` se recibe aquí, no en `execute`, por ser un
        dato de configuración del modelo en ejecución (`docs/11-Versiones.md`),
        no un dato propio de un partido específico -- mismo criterio ya
        usado por `PredictionRuntime.__init__` (`app/runtime/runtime.py`,
        BUILD-005, sin modificarlo). Ningún valor por defecto: esta clase
        nunca inventa una versión no provista explícitamente.
        """
        self._version_modelo = version_modelo

    def execute(
        self,
        id_partido: str,
        seleccion_local: str,
        seleccion_visitante: str,
        competicion: str,
        torneo: str,
        fecha: date,
        estadio: str | None = None,
    ) -> PredictionContext:
        """Construye un `PredictionContext` con únicamente `metadata` +
        `match` (docs/30 §4.1-4.2) -- `variables`, `engine`, `prediction`,
        `market`, `bankroll`, `errors`, `audit` y `learning` permanecen en
        su valor por defecto del esquema (`None`/lista vacía/`EngineBlock()`
        vacío, `app/runtime/prediction_context.py`), exactamente el sentido
        de "`PredictionContext` vacío" que pide el brief. `estadio` es el
        único campo opcional que este método acepta, con el mismo valor por
        defecto (`None`) ya definido en `MatchBlock` -- ninguna otra señal
        opcional (`hora_local`/`arbitro`) se expone aquí (ver "Hallazgo
        explícito" en el docstring del módulo).

        Construye el `EnginePipeline` oficial con `construir_pipeline_
        oficial()` (`app/runtime/engine_pipeline.py`, `INT-001`), sin
        ningún argumento -- exactamente como exige el brief ("usando
        únicamente construir_pipeline_oficial()"). Lo ejecuta una única vez
        sobre el `context` recién construido y devuelve el mismo objeto,
        mutado in-place por sus colaboradores -- nunca una copia, nunca un
        DTO, nunca una serialización.
        """
        context = PredictionContext(
            metadata=MetadataBlock(
                version_modelo=self._version_modelo,
                timestamp_creacion=datetime.now(timezone.utc),
            ),
            match=MatchBlock(
                id_partido=id_partido,
                seleccion_local=seleccion_local,
                seleccion_visitante=seleccion_visitante,
                competicion=competicion,
                torneo=torneo,
                fecha=fecha,
                estadio=estadio,
            ),
        )

        pipeline = construir_pipeline_oficial()
        return pipeline.ejecutar(context)
