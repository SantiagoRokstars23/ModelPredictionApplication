# Contrato Oficial del Prediction Context

**Archivo:** `docs/30-Contrato-Oficial-del-Prediction-Context.md`

**Misión:** DEV-003 — Contrato Oficial del Prediction Context

**Versión:** 1.0.0

**Estado:** Especificación oficial — Contrato de datos de implementación (sin implementación)

---

# Nota de verificación previa (léase antes de continuar)

El brief de esta misión referencia `docs/26-Arquitectura-de-Ejecucion.md`, una ruta que no existe en el repositorio. El documento real de esa serie es `docs/26-Runtime-del-Modelo.md` (misión **DEV-001**), que formalizó por primera vez el "Objeto de Contexto". Existe además `docs/29-Arquitectura-del-Runtime.md` (misión **DEV-002**, ya completada), que le dio a ese mismo objeto el nombre de implementación `PredictionContext` y una primera tabla de qué componente escribe cada sección — documento no mencionado por el brief (probablemente por no existir todavía cuando se redactó), pero directamente relevante y de lectura obligatoria por ser el antecedente inmediato de esta misión. Este documento usa las rutas correctas de ambos y no repite ninguna de sus dos secciones ya existentes.

---

# Objetivo

`docs/26` especifica **qué es** el Objeto de Contexto (append-only, viaja entre fases). `docs/29` le da **nombre de componente** (`PredictionContext`) y una primera frontera de escritura por sección de alto nivel (Identificación, Metadatos, Variables Oficiales, Resultados parciales). Ninguno de los dos documentos define todavía su **estructura interna completa** — cuántos bloques tiene, qué campos contiene cada uno, cuándo aparece cada bloque, y cómo evoluciona desde que se crea hasta que se audita.

Ese es exactamente el vacío que cierra esta misión: el **Contrato Oficial** del `PredictionContext` — la referencia única, de aquí en adelante, para cualquier implementación futura, en cualquier lenguaje. No se implementa código, no se modifica ningún motor, algoritmo, variable o fórmula existente.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué NO repite este contrato |
|---|---|---|
| `docs/06-Flujo-Operacional.md` | Fases, orden de ejecución por capas, manejo de errores, integración con `data/` | Ninguna fase nueva — este contrato es la estructura del objeto que viaja *dentro* de la Fase 3 |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | Responsabilidad, entrada, salida y validaciones de la Capa de Preparación de Variables | Las mismas reglas de validación, sin cambio — este contrato solo define dónde aterriza su salida dentro del objeto |
| `docs/16-Contrato-Oficial-de-Variables.md` | Tipo, unidad, rango, nulabilidad e inmutabilidad de las 12 Variables Oficiales | No se redefine ninguna variable — el bloque `variables` de este contrato referencia esta tabla, no la repite |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Qué motor consume qué variable, directa o indirectamente | Reutilizada tal cual para justificar qué motores leen qué secciones del `PredictionContext` |
| `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md` | Objeto de entrada, objeto de respuesta completo (contrato de salida al usuario) | El objeto de entrada y el objeto de respuesta no se redefinen — se referencian como `PredictionRequest` y `PredictionReport` (nombres ya fijados en `docs/29`) |
| `docs/26-Runtime-del-Modelo.md` | El Objeto de Contexto, su regla append-only, el registro de ejecución (logs), el manejo de errores | Ninguna regla nueva de ejecución — este contrato solo detalla la estructura interna del mismo objeto |
| `docs/29-Arquitectura-del-Runtime.md` | Los siete componentes de la arquitectura de implementación (`PredictionRequest` → ... → `Persistence`), el nombre `PredictionContext`, la primera tabla de escritura por sección, los "Estados de ejecución" | No se rediseñan los componentes ni sus responsabilidades — este contrato es, exactamente, la especificación detallada del objeto que `docs/29` ya nombró |
| `engine/01` a `engine/06` | Objetivo, entradas y — el dato relevante aquí — la sección "Salida" exacta de cada motor | Ninguna fórmula ni paso de "Procesamiento"/"Flujo del Motor" se repite; solo se reutiliza, campo por campo, lo que cada "Salida" ya declara |
| `docs/09-Auditoria.md`, `docs/07-Backroll.md` | Métricas de auditoría (ROI, Yield, Top1/Top4, Drawdown) y umbrales de bankroll por nivel de confianza | Documentos todavía en estado de marcador mínimo (`AR-001`, INC-14/INC-16) — se referencian tal cual están hoy, sin ampliarlos ni corregirlos (fuera de alcance) |
| `learning/README.md` | Pipeline de aprendizaje (`error-analysis` → `pattern-discovery` → `confidence-calibration` → `weight-adjustment`), límites de responsabilidad | No se redefine el pipeline — el bloque `learning` de este contrato solo referencia dónde se ancla su resultado |

Ninguna inconsistencia detectada durante este análisis se corrige aquí — se documenta, si aparece, en "Observaciones" al final.

---

# 1. Propósito

## Qué representa

El `PredictionContext` es el único objeto que transporta toda la información de una predicción concreta a lo largo de su ciclo de vida completo: desde que se recibe la solicitud hasta que, semanas después, se audita y retroalimenta al sistema de aprendizaje. Es el "expediente" de una predicción — no una estructura de paso efímera entre dos funciones.

## Qué problema resuelve

Sin un contrato único y estable:

- Cada componente (Runtime, `VariablePreparation`, `EngineRunner`, `PredictionAssembler`, `Persistence`, Auditor, `learning/`) tendría que negociar su propia forma de intercambiar información con los demás, repitiendo en código lo que `docs/15`/`docs/17` ya prohíben duplicar en documentación.
- No existiría una única fuente de verdad sobre qué campos produce cada motor, obligando a leer los seis archivos de `engine/` cada vez que se necesite saber qué contiene una predicción completa.
- La trazabilidad completa de una predicción (Constitución, Artículo 8) dependería de reconstruir manualmente qué escribió cada componente, en lugar de leerlo directamente de un objeto con estructura fija y conocida.

---

# 2. Principios

| Principio | Qué significa para el `PredictionContext` | Fundamento |
|---|---|---|
| **Append Only** | Cada componente solo puede agregar la sección que le pertenece (sección 4); nunca modifica ni elimina una sección ya escrita por otro | Ya fijado en `docs/26` §3 y `docs/29` §3 — se hereda sin cambio |
| **Inmutabilidad** | Una vez que un componente cierra su sección, esa sección no vuelve a cambiar durante el resto de la ejecución — ni siquiera por el mismo componente que la escribió | Mismo principio que `docs/16` §8 aplicado a variables, extendido aquí a todas las secciones del objeto, no solo a las Variables Oficiales |
| **Trazabilidad** | Toda cifra del `PredictionReport` final debe poder rastrearse hasta la sección exacta del `PredictionContext` que la originó, y de ahí hasta la Variable Oficial o el motor que la produjo | Constitución, Artículo 8 |
| **Versionado** | El propio contrato (esta especificación, no una predicción individual) evoluciona bajo Versionado Semántico: agregar un bloque nuevo opcional es MINOR; cambiar la forma de un bloque existente es MAJOR; nunca se reutiliza el nombre de un bloque eliminado con un significado distinto | Mismo esquema ya adoptado por `docs/16` §9 para las Variables Oficiales, aplicado aquí al contenedor completo |
| **Desacoplamiento** | Ningún motor conoce el origen físico de un dato ni necesita invocar a otro motor directamente — todo pasa a través de secciones ya escritas del `PredictionContext` | `docs/15` §8, `docs/29` §9 (heredado de `docs/26`) |
| **Reproducibilidad** | El mismo `PredictionRequest`, con la misma Base de Conocimiento, debe producir un `PredictionContext` idéntico sección por sección | `docs/26` §9, Constitución Artículo 2.3 |

---

# 3. Ciclo de vida

```
Creación
    │
    ▼
Enriquecimiento
    │
    ▼
Consumo
    │
    ▼
Persistencia
    │
    ▼
Auditoría
```

| Etapa | Qué ocurre | Quién actúa | Duración |
|---|---|---|---|
| **Creación** | El Runtime recibe el `PredictionRequest` y construye el `PredictionContext` con los bloques `metadata` y `match` (sección 4) | Runtime | Instantánea, al inicio de la ejecución |
| **Enriquecimiento** | `VariablePreparation` agrega `variables`; `EngineRunner` agrega `engine` (una subsección por motor, en el orden por capas ya fijado) y `prediction`; opcionalmente `market` (Fase 4) y `bankroll` (Fase 5, si el usuario lo pide); cualquier anomalía se agrega a `errors` en el momento en que ocurre | `VariablePreparation`, `EngineRunner`, Odds Analyzer, Bankroll Manager | Toda la duración de la ejecución de una predicción (segundos) |
| **Consumo** | `PredictionAssembler` lee el `PredictionContext` completo (o su estado al detenerse) y construye el `PredictionReport` | `PredictionAssembler` | Instantánea, al cierre de la ejecución |
| **Persistencia** | `Persistence` escribe el `PredictionReport` en `data/predictions/` | `Persistence` | Instantánea, siempre antes del inicio del partido (`docs/14`) |
| **Auditoría** | Cuando el partido finaliza y existe resultado oficial, el Auditor compara el registro persistido contra `data/results/` y agrega el bloque `audit` **al registro persistido**, nunca al objeto en memoria de la ejecución original (ver nota siguiente) | Auditor | Días o semanas después de la Persistencia |

**Nota central de diseño (resuelve una ambigüedad real del brief):** el `PredictionContext` **en memoria**, tal como lo definen `docs/26`/`docs/29`, existe únicamente durante una ejecución — desde la Creación hasta la Persistencia. Ese objeto se descarta una vez que `Persistence` escribe el `PredictionReport` (mismo principio de temporalidad ya fijado para las Variables Oficiales en `docs/16` §7: "las variables son siempre temporales"). La etapa de **Auditoría** —y, como caso de uso derivado, el **Aprendizaje** (sección 8)— no reabren ni mutan ese objeto ya destruido: operan sobre el **registro persistido** en `data/predictions/`, extendiéndolo con nueva información cross-referenciada por `id_prediccion` (el bloque `audit` vive lógicamente junto a ese registro, escrito por el Auditor en el momento de la Fase 8 de `docs/06`; el bloque `learning` de la misma forma, en la Fase 9). El principio Append Only (sección 2) se cumple igual, solo que a dos escalas de tiempo distintas: segundos (dentro de una ejecución) y meses (a lo largo de la vida de una predicción ya cerrada). Ninguna de las dos escalas permite modificar lo ya escrito por la otra.

Por esta razón, la etapa "Auditoría" del ciclo de vida es la última que pide el brief (5 etapas, tal como se solicitó); el "Aprendizaje" no es una sexta etapa del ciclo de vida del objeto — es un **caso de uso** (sección 8) que consume el registro ya auditado.

---

# 4. Estructura

Diez bloques, ninguno implementado como clase — solo como contrato conceptual (nombre, contenido, quién escribe, cuándo aparece):

```
PredictionContext
 ├─ metadata     (obligatorio, Runtime)
 ├─ match        (obligatorio, Runtime)
 ├─ variables    (obligatorio, VariablePreparation)
 ├─ engine       (obligatorio — parcial si se detiene una capa; EngineRunner)
 │    ├─ engine01   (Fuerza Ofensiva)
 │    ├─ engine02   (Fuerza Defensiva)
 │    ├─ engine03   (Poisson)
 │    ├─ engine04   (Índice de Caos)
 │    ├─ engine05   (Confianza)
 │    └─ engine06   (Valor Esperado — condicional, Fase 4)
 ├─ prediction   (obligatorio — se completa en la medida en que engine se completa; EngineRunner/PredictionAssembler)
 ├─ market       (condicional — solo si hay cuotas y mercado solicitado; EngineRunner, excepción INC-05)
 ├─ bankroll     (condicional — solo si el usuario lo solicita; Bankroll Manager)
 ├─ errors       (siempre presente, puede estar vacío; cualquier componente)
 ├─ audit        (ausente en el objeto en memoria; se agrega al registro persistido, Fase 8; Auditor)
 └─ learning     (ausente en el objeto en memoria; se agrega al registro persistido, Fase 9; learning/)
```

## 4.1 `metadata`

| Campo | Contenido | Fuente |
|---|---|---|
| `version_modelo` | Versión del Modelo Santiago utilizada | `docs/11-Versiones.md` |
| `timestamp_creacion` | Momento en que el Runtime construyó el `PredictionContext` | `docs/26` §7 ("Inicio de ejecución") |
| `timestamp_cierre` | Momento en que `PredictionAssembler` cerró el objeto | Nuevo — necesario para calcular la duración total (`docs/26` §7, "Duración de cada fase") |
| `estado_ejecucion` | Uno de: Completa / Completa sin Valor Esperado / Detenida antes del Engine / Detenida durante el Engine | `docs/29` §6 (Estados de ejecución, ya definidos allí) |
| `id_prediccion` | `id_partido` + timestamp — asignado al persistir, no al crear | `docs/25` §6, `docs/14` Etapa 3 |

## 4.2 `match`

Equivalente exacto a la sección "Identificación" de `docs/26`/`docs/29`. Campos: `id_partido`, `seleccion_local`, `seleccion_visitante`, `competicion`, `torneo`, `fecha`, `hora_local` (opcional), `estadio` (si asignado), `arbitro` (si asignado) — mismos campos ya fijados en `docs/25` §1, sin alteración.

## 4.3 `variables`

Las 12 Variables Oficiales de `docs/16`, cada una con su valor (o marca explícita de "no disponible") y su nivel de confianza asociado si la muestra es reducida (`docs/15` §6). **Aclaración no explícita hasta ahora en ningún documento:** las variables de rendimiento (Variable001-004, 006-008) se construyen **una vez por equipo** (local y visitante); Variable009 (Localía) y Variable010 (Historial Directo) son propias del enfrentamiento, no de un equipo individual — un único valor por partido. Variable005 y Variable011 no aparecen en este bloque en V1 (diferidas, `MR-004`).

## 4.4 `engine`

Una subsección por motor, con exactamente los campos que cada `engine/0X.md` ya declara en su sección "Salida" — no se inventa ningún campo nuevo:

| Subsección | Campos (verbatim de la "Salida" de cada motor) |
|---|---|
| `engine01` | Fuerza Ofensiva, Nivel de confianza del cálculo, Variables utilizadas, Variables descartadas, Calidad de los datos |
| `engine02` | Fuerza Defensiva, Nivel de confianza del cálculo, Variables utilizadas, Variables descartadas, Calidad de los datos |
| `engine03` | Goles esperados (Local/Visitante), Distribución de goles, Probabilidad de cada marcador, Top de marcadores, Probabilidad de victoria/empate/derrota |
| `engine04` | Índice de Caos (0-100), Nivel de Caos, Factores que aumentan el caos, Factores que reducen el caos, Justificación |
| `engine05` | Índice de Confianza (0-100), Nivel de confianza, Factores positivos, Factores negativos, Justificación |
| `engine06` (condicional) | Valor Esperado, Probabilidad del Modelo, Probabilidad Implícita, Diferencia porcentual, Nivel de confianza, Índice de Caos asociado, Recomendación — uno por mercado evaluado (`engine/06`, "Mercados Compatibles") |

Este bloque es la **telemetría completa y verbosa** de cada motor — incluye campos de diagnóstico (variables descartadas, justificación) que no forman parte del contrato de salida al usuario. Es la fuente que consumen `PredictionAssembler` (para construir `prediction`) y, más adelante, `learning/` (para `error-analysis.md`/`pattern-discovery.md`).

## 4.5 `prediction`

El subconjunto curado que se convertirá en el `PredictionReport` (`docs/25` §6): `probabilidades` (Local/Empate/Visitante, de `engine03`), `top_marcadores` (de `engine03`), `variables_influyentes` (curada de `variables` + `engine`), `confianza` (de `engine05`), `indice_caos` (de `engine04`), `valor_esperado` (de `engine06`, o "no disponible — sin cuotas registradas"). Se completa progresivamente, en el mismo orden por capas que `engine` — nunca se rellena de una vez al final. **Por qué existe un bloque separado de `engine` y no basta con leer `engine` directamente:** `engine` mezcla campos de diagnóstico interno (variables descartadas, justificación completa) que no pertenecen al contrato externo; `prediction` es exactamente lo que el usuario final necesita ver, sin obligar a `PredictionAssembler` a filtrar campos de diagnóstico en el momento de construir el reporte.

## 4.6 `market`

Bloque condicional, presente únicamente si existen cuotas y un mercado fue solicitado (Fase 4, `docs/06`). Hoy contiene una única referencia: las cuotas leídas directamente de `cuotas.csv` por `EngineRunner` al invocar `engine06` — la excepción ya documentada (`INC-05`). Este bloque es, deliberadamente, el lugar reservado en el contrato para cuando exista el **Contrato de Datos de Mercado** (`docs/15`, "Relación con Datos de Mercado — actualización MR-004"; `docs/16`, "Reglas generales"): en ese momento futuro, `market` dejará de llenarse por acceso directo y pasará a ser escrito por `VariablePreparation`, igual que `variables`, sin que ningún otro bloque de este contrato tenga que cambiar. Esta misión no diseña ese contrato futuro (fuera de alcance) — solo le reserva un nombre y una posición estables en la estructura.

## 4.7 `bankroll`

Bloque condicional, presente únicamente si el usuario solicita gestión de bankroll (Fase 5, `docs/06`; fuera del núcleo del modelo). Contenido: la propuesta de distribución de capital según la estrategia del usuario (`.claude/agents/bankroll-manager.md`, "Salida"). Nunca se genera automáticamente.

## 4.8 `errors`

Registro append-only de anomalías detectadas antes de la Persistencia — la reificación, dentro del propio objeto, del "Registro de ejecución" ya especificado en `docs/26` §7 (no es una fuente de datos nueva y distinta: es la misma información, ahora también disponible como sección consultable del `PredictionContext`, no solo como log externo). Campos por entrada: evento, componente emisor, capa/fase, timestamp, detalle. Siempre presente, aunque esté vacío.

## 4.9 `audit`

Ausente en el objeto en memoria de la ejecución (ver nota de la sección 3). Una vez que el partido finaliza y existe resultado oficial, el Auditor agrega este bloque al registro persistido: referencia a `data/results/`, métricas calculadas (ROI, Yield, Top1, Top4, Drawdown — `docs/09-Auditoria.md`), fecha de auditoría.

## 4.10 `learning`

Ausente en el objeto en memoria. Se agrega al registro persistido después de `audit`, cuando `learning/` ejecuta su pipeline (`error-analysis.md` → `pattern-discovery.md` → `confidence-calibration.md` → `weight-adjustment.md`): diagnóstico, patrones detectados, resultado de calibración, y el estado de cualquier propuesta de `weight-adjustment.md` (pendiente / aprobada / rechazada — `docs/06` Fase 9).

---

# 5. Reglas

Consolidación, sin redefinir ninguna, de las reglas ya vigentes en `docs/15`/`docs/16`/`docs/26`/`docs/29`, aplicadas explícitamente a los diez bloques de la sección 4:

- **Cada motor únicamente puede escribir en su propia subsección de `engine`** — `engine01` nunca escribe en `engine03`, ni ningún motor escribe directamente en `prediction` (esa es responsabilidad exclusiva de `EngineRunner`/`PredictionAssembler`, que consolidan, no calculan).
- **Nunca se modifica información previa** — ninguna sección, una vez cerrada por su componente responsable, puede ser reabierta ni por el mismo componente ni por otro (sección 2, Inmutabilidad).
- **Nunca se borra información** — ni siquiera al detenerse una ejecución (`estado_ejecucion` = Detenida): las secciones ya escritas hasta ese punto permanecen, junto con la entrada correspondiente en `errors` que explica la detención.
- **Nunca se recalcula información de otro motor** — un motor que reciba una Variable Oficial o una salida de otro motor la usa tal como llega; si la considera insuficiente, declara su propia salida como no disponible o de confianza reducida, nunca "corrige" la sección de otro (`docs/17` §1, "No implica... modificar la variable").

---

# 6. Responsabilidades

| Pregunta | Respuesta |
|---|---|
| ¿Quién crea el Context? | El Runtime, al recibir el `PredictionRequest` (bloques `metadata`+`match`) |
| ¿Quién lo enriquece? | `VariablePreparation` (`variables`); `EngineRunner` (`engine`, `prediction`, `market` si aplica); Bankroll Manager (`bankroll`, si se solicita); cualquier componente puede agregar una entrada a `errors` en el momento en que detecta una anomalía |
| ¿Quién lo consume? | `PredictionAssembler`, para construir el `PredictionReport` (única lectura completa del objeto en memoria) |
| ¿Quién lo persiste? | `Persistence`, escribiendo el `PredictionReport` en `data/predictions/` — nunca el `PredictionContext` completo, que se descarta tras el Consumo |
| ¿Quién lo audita? | El Auditor (`.claude/agents/auditor.md`), agregando el bloque `audit` **al registro persistido**, cuando exista resultado oficial (`docs/06`, Fase 8) |

---

# 7. Compatibilidad

| Documento | Verificación |
|---|---|
| `docs/06-Flujo-Operacional.md` | Los diez bloques respetan exactamente las fases ya definidas (Fase 3 → `variables`/`engine`; Fase 4 → `market`; Fase 5 → `bankroll`; Fase 8 → `audit`; Fase 9 → `learning`); ninguna fase nueva introducida |
| `docs/14`/`docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md` | El bloque `prediction` es, campo por campo, el mismo contrato de salida ya definido en `docs/25` §6 — no se redefine |
| `engine/01` a `engine/06` | El bloque `engine` reutiliza, verbatim, la sección "Salida" ya declarada por cada motor — ninguna fórmula, variable ni algoritmo se toca |
| `learning/README.md` | El bloque `learning` referencia el mismo pipeline de cuatro documentos ya especificado, sin alterar sus límites de responsabilidad (nunca aplica cambios automáticos) |
| **Architecture Freeze** (`docs/23`, Parte 6) | Este contrato no cambia el estado de ningún criterio: sigue en **4 de 7** cumplidos (`docs/00-Project-Tracker.md`). En particular, el Criterio 5 ("ningún motor consume `data/processed/` directamente") **sigue sin cumplirse** — el bloque `market` hereda la excepción de `engine06`/cuotas (`INC-05`) tal cual, sin resolverla; este contrato solo le da un nombre y una posición estables en la estructura para cuando se resuelva |

---

# 8. Casos de uso

| Caso de uso | Bloques que se completan | Bloques ausentes |
|---|---|---|
| **Predicción simple** (sin cuotas, sin bankroll) | `metadata`, `match`, `variables`, `engine` (engine01-05), `prediction` (con `valor_esperado`: "no disponible") | `market`, `bankroll` |
| **Predicción con cuotas** | Los anteriores + `market`, `engine06`, `prediction.valor_esperado` con valor real | `bankroll` |
| **Predicción con bankroll** | Los de "Predicción con cuotas" (el Bankroll Manager requiere Valor Esperado, `docs/06` Fase 5) + `bankroll` | — |
| **Auditoría** (días/semanas después) | El registro persistido ya completo + `audit`, agregado por el Auditor sobre ese registro — el objeto en memoria original ya no existe (sección 3) | `learning` (todavía, hasta la Fase 9) |
| **Aprendizaje** (después de la Auditoría) | El registro persistido + `audit` + `learning`, agregado por `learning/` — nunca se ejecuta si `audit` no existe primero (`docs/06`, "nunca antes") | — |

---

# Validaciones obligatorias

- **¿Todos los motores pueden ejecutarse usando únicamente este Context?** Sí — cada motor de `engine/01` a `engine/06` recibe del `PredictionContext` exactamente lo que su sección "Entradas" ya declara (Variables Oficiales del bloque `variables`, o salidas de motores anteriores del bloque `engine`), con la única excepción ya heredada y documentada de `engine06`/cuotas (bloque `market`).
- **¿Ningún motor necesita acceder directamente a otro?** Confirmado — `engine03` no invoca a `engine01`/`engine02`, lee sus subsecciones ya escritas en `engine`; lo mismo aplica a `engine04`/`05` respecto de `engine03`, y a `engine06` respecto de `engine03`/`04`/`05`. Ningún motor conoce la existencia de otro motor como componente, solo como sección de datos ya disponible.
- **¿El contrato soporta futuras versiones sin romper compatibilidad?** Sí, bajo la misma regla de Versionado Semántico de la sección 2: agregar un bloque 11 (ej. un futuro `simulation` para `engine/08-Simulation.md`) es un cambio MINOR que no afecta a los diez bloques ya definidos; cambiar la forma de un bloque existente (ej. agregar campos nuevos a `engine03` cuando `models/poisson.md` alcance su Versión 2.0) es MINOR si es aditivo, MAJOR si elimina o redefine un campo ya consumido por `PredictionAssembler` o por `learning/`.

---

# Cierre obligatorio

**1. ¿Qué problema resuelve este contrato?**
Da, por primera vez, una estructura interna completa y estable al `PredictionContext` ya nombrado por `docs/29` — sin este contrato, cada implementación futura tendría que inferir esa estructura leyendo seis archivos de `engine/` y cuatro documentos de arquitectura por separado.

**2. ¿Qué responsabilidades aparecen?**
Las ya fijadas en la sección 6: Runtime crea; `VariablePreparation`/`EngineRunner`/Bankroll Manager enriquecen; `PredictionAssembler` consume; `Persistence` persiste; el Auditor y `learning/` extienden el registro persistido después de que la ejecución original terminó.

**3. ¿Qué componentes dependerán de él?**
Los siete de `docs/29` (`PredictionRequest`, `PredictionContext`, `VariablePreparation`, `EngineRunner`, `PredictionAssembler`, `PredictionReport`, `Persistence`) más, ahora explícitamente, el Auditor y `learning/` — que hasta este documento nunca se habían descrito como consumidores directos de la estructura del Context, sino del registro genérico de `data/predictions/`/`data/results/`.

**4. ¿Qué beneficios aporta para la implementación?**
Un implementador puede, sin leer ningún otro documento de `engine/`, saber exactamente qué campos tendrá disponibles en cada bloque y quién es responsable de escribirlos — el mismo beneficio que `docs/16` ya aportó para las variables, extendido aquí al objeto completo.

**5. ¿Qué riesgos elimina?**
El riesgo de que dos implementaciones futuras (o dos motores dentro de la misma implementación) definan de forma distinta qué contiene la salida de un motor, al no existir antes una única fuente de verdad sobre la forma exacta del `PredictionContext`.

**6. ¿Qué limitaciones mantiene?**
Las mismas tres ya heredadas de `docs/26`/`docs/29`: ninguna fórmula matemática real todavía (`models/`, sin Versión 2.0); el Contrato de Datos de Mercado sigue sin diseñarse (el bloque `market` solo reserva su lugar); ninguna decisión de stack tecnológico.

**7. ¿Qué parte sigue pendiente para V0.1?**
Las mismas ya identificadas por `docs/25`/`docs/26`/`docs/29`: al menos una fórmula matemática real en `models/` (empezando por `models/poisson.md`), el Contrato de Datos de Mercado completo, y la decisión de stack — ninguna de las tres es responsabilidad de esta serie `DEV-`.

**8. ¿Qué impacto tiene sobre el Architecture Freeze?**
Ninguno en el conteo de criterios (sigue en 4 de 7, `docs/23` Parte 6) — este contrato no resuelve `INC-05` (Criterio 5), solo le da una posición estable en la estructura (bloque `market`) para cuando se resuelva.

**9. ¿Qué misión recomendarías después?**
La misma ya recomendada por toda la serie `DEV-` y por `MODEL-006`: la primera fórmula matemática real con Versión 2.0 (`models/poisson.md`), que es lo único que permitiría que los campos ya definidos en el bloque `engine03` de este contrato contengan, por primera vez, un número calculado en lugar de un marcador conceptual.

**10. ¿Puede considerarse listo el diseño del Runtime tras este documento?**
Sí, en el nivel de diseño que le corresponde a la serie `DEV-`: con `docs/26` (qué hace), `docs/29` (en qué componentes se divide) y este documento (qué estructura exacta tiene el objeto que los conecta), el diseño arquitectónico del Runtime queda completo en sus tres niveles. Lo que falta para pasar de diseño a implementación no es más diseño de Runtime — es contenido matemático (`models/`) y una decisión de stack, ambas fuera del alcance de esta serie.

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Que la distinción entre el `PredictionContext` en memoria (vive solo durante una ejecución) y el "registro persistido" que luego recibe `audit`/`learning` es la lectura correcta de la intención del brief, y no una sobre-ingeniería. Es una interpretación razonada (evita contradecir `docs/16` §7 sobre temporalidad de las variables), pero el brief no distingue explícitamente entre ambos y una implementación futura podría preferir modelarlo de otra forma.
- **¿Qué parte de este entregable podría estar equivocada?** La separación entre los bloques `engine` y `prediction` (sección 4.4/4.5) es una decisión de diseño nueva, no exigida literalmente por ningún documento previo — se justificó por separar telemetría interna de contrato externo, pero es razonable que una futura implementación decida fusionarlos si el costo de mantener dos vistas resulta mayor que el beneficio.
- **¿Qué información me habría hecho falta para tener más certeza?** Un ejemplo real de auditoría ejecutada (hoy `data/audit/` y `data/results/` son solo marcadores de posición) habría permitido confirmar si el bloque `audit` propuesto en la sección 4.9 contiene efectivamente los campos que el Auditor necesitará, o si faltan campos no anticipables desde la documentación actual.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que la primera vez que se ejecute una auditoría real, el bloque `audit` (sección 4.9) efectivamente pueda construirse a partir de las métricas ya definidas en `docs/09-Auditoria.md` sin requerir un campo no previsto aquí.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí — el bloque `market` podría, alternativamente, no reservarse ahora y agregarse recién cuando exista el Contrato de Datos de Mercado, en lugar de anticiparse aquí como un bloque condicional vacío de contrato propio. Se eligió anticiparlo porque el brief lo pide explícitamente en la lista de bloques de ejemplo, y porque reservar el nombre ahora evita una colisión de nomenclatura futura — pero es una decisión, no un hecho ya determinado por la arquitectura existente.

---

# Fuera de alcance de esta misión

- No se implementa código, clases ni DTO.
- No se modifica el Engine, las Variables Oficiales, el algoritmo, ninguna fórmula matemática, el Pipeline ni el Runtime ya definido en `docs/26`/`docs/29`.
- No se elige lenguaje ni tecnología.
- No se diseña el Contrato de Datos de Mercado completo — el bloque `market` solo reserva su posición (`INC-05` sigue sin resolverse).
- No se amplían `docs/09-Auditoria.md` ni `docs/07-Backroll.md` — se referencian en el estado de marcador mínimo en que se encuentran hoy (`AR-001`).

---

Fin del documento.
