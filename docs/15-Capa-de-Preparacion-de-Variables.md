# Capa de Preparación de Variables

**Archivo:** `docs/15-Capa-de-Preparacion-de-Variables.md`

**Versión:** 1.1.0

**Estado:** Especificación oficial — Arquitectura (sin implementación)

---

# Objetivo

Este documento es la especificación oficial de una nueva pieza arquitectónica del Modelo Santiago: la capa responsable de transformar los datos de la Base de Conocimiento (`data/processed/`) en las variables normalizadas que consumirán los motores estadísticos (`engine/`).

Hasta ahora el flujo conceptual del modelo era:

```
Base de Conocimiento
        │
        ▼
Motores Estadísticos
        │
        ▼
Predicción
```

Este flujo asume implícitamente que los motores saben leer, validar y normalizar datos de negocio. Este documento formaliza una capa intermedia explícita para que esa suposición deje de ser implícita — y para que, en el futuro, dejar de ser cierta (cambiar de CSV a PostgreSQL, por ejemplo) no obligue a modificar ningún motor.

---

# Análisis previo obligatorio: elección del nombre

Antes de nombrar la capa se evaluaron cuatro alternativas.

| Nombre | Evaluación |
|---|---|
| **Feature Builder** | Rechazado. "Feature" es terminología de *Machine Learning* (`docs/12-Roadmap.md`, v3). El Modelo Santiago está en v1 (Poisson determinístico) y en **ningún** documento del proyecto (`docs/`, `engine/`, `models/`, `learning/`) se usa la palabra "Feature" — el término oficial y universal ya en uso es **"Variable"** (`docs/03-Variables.md`, el propio nombre de cada motor). Introducir "Feature" ahora crearía dos vocabularios paralelos para el mismo concepto. Además, "Builder" solo describe construcción, y esta capa también valida y normaliza — no es solo un ensamblador. |
| **Feature Engineering Layer** | Rechazado por la misma razón de vocabulario ("Feature"). Adicionalmente, "Feature Engineering" en la literatura de ML implica derivar variables *nuevas* de forma creativa/experimental para un modelo entrenado — no es lo que hace esta capa: esta capa no inventa variables, únicamente prepara las 12 ya definidas y cerradas en `docs/03-Variables.md`. Usar este nombre sugeriría una responsabilidad (descubrimiento de variables) que pertenece, si acaso, a una futura fase de `learning/pattern-discovery.md`, no a esta capa. |
| **Variable Builder** | Descarta el problema de vocabulario ("Variable" es correcto), pero "Builder" sigue siendo demasiado estrecho: no comunica la responsabilidad de validación (`¿Qué validaciones realiza?`, pregunta 6 de esta misión) ni la de desacoplamiento de fuente (pregunta 8), que son tan centrales como la construcción misma. |
| **Capa de Preparación de Variables / Variable Preparation Layer** | **Seleccionado.** "Variable" mantiene el vocabulario ya establecido en todo el proyecto. "Preparación" cubre las tres responsabilidades reales (leer, validar, normalizar, construir) sin reducirlas a una sola. "Capa" (*Layer*) comunica correctamente su naturaleza arquitectónica: una capa de desacoplamiento entre el origen de datos y la lógica matemática — el mismo patrón que una capa de acceso a datos (*data access layer*) o un puerto en arquitectura hexagonal, aplicado aquí a variables en lugar de entidades. |

**Decisión:** se adopta **"Capa de Preparación de Variables"** como nombre oficial en español (consistente con el resto de la documentación funcional: "Flujo Operacional", "Base de Conocimiento", "Índice de Caos"), con **"Variable Preparation Layer"** como equivalente en inglés cuando se requiera (igual que `docs/14-Prediction-Pipeline.md` usa un título en inglés por convención de esa misión). No se adopta ningún nombre con la palabra "Feature": sería inconsistente con el vocabulario ya consolidado del proyecto y anticiparía, sin evidencia, una fase de Machine Learning que todavía no existe.

---

# 1. ¿Qué es esta capa?

## Responsabilidad

Transformar los datos de negocio de la Base de Conocimiento en las 12 variables definidas en `docs/03-Variables.md`, ya validadas, normalizadas y listas para ser consumidas por `engine/01` a `engine/06`.

## Por qué existe

Porque hoy esa responsabilidad no tiene un dueño explícito: `docs/04-Algoritmo.md` ya describe sus pasos (Paso 3 "Normalización", Paso 4 "Cálculo de Variables") pero no asigna ningún componente que los ejecute; y, como se detalla en la sección "Análisis crítico obligatorio", varios motores (`engine/01`, `engine/02`) actualmente documentan internamente pasos equivalentes ("obtener", "validar", "normalizar") de forma duplicada entre sí.

## Qué problema resuelve

- Evita que los motores estadísticos necesiten conocer el origen físico de los datos (CSV hoy, PostgreSQL o APIs mañana).
- Evita que la misma variable (ej. Forma Reciente, usada tanto por `engine/01` como por `engine/02`) se calcule de forma independiente y potencialmente inconsistente en cada motor.
- Da un único punto de responsabilidad para validar la calidad del dato antes de que llegue a un cálculo matemático.

## Qué responsabilidades NO le pertenecen

- **No calcula probabilidades, fuerzas, caos, confianza ni valor esperado** — eso pertenece exclusivamente a `engine/`.
- **No decide si hay datos suficientes para intentar una predicción** — esa es la responsabilidad del Statistician (Fase 2 de `docs/06-Flujo-Operacional.md`), que actúa *antes* que esta capa y decide si el flujo continúa o se detiene.
- **No investiga ni respalda metodología matemática** — eso pertenece a `models/`.
- **No almacena nada de forma permanente** — solo produce variables temporales para una predicción concreta.
- **No define qué es cada variable** — eso ya lo define `docs/03-Variables.md`; esta capa solo lo ejecuta.

---

# 2. ¿Dónde se ubica dentro de la arquitectura?

La capa se ubica **entre la Fase 2 (Validación) y la Fase 3 (Ejecución del Engine)** de `docs/06-Flujo-Operacional.md`, como el primer paso interno de esa Fase 3 — el Predictor la invoca antes de invocar `engine/01`.

Integración sin duplicar contenido:

| Documento | Qué ya define (no se repite aquí) | Qué aporta esta capa |
|---|---|---|
| `docs/04-Algoritmo.md` | Los 14 pasos del algoritmo, incluyendo el Paso 3 (Normalización) y el Paso 4 (Cálculo de Variables) | Esta capa **es** la implementación arquitectónica de esos dos pasos — antes no tenían componente asignado. No se redefinen los 14 pasos, solo se les da dueño a dos de ellos. |
| `docs/05-Base-de-Conocimiento.md` | El flujo Recolección → Validación → Normalización → Almacenamiento, y el formato uniforme de `data/processed/` (fechas `YYYY-MM-DD`, porcentajes 0-100, etc.) | Esa normalización es de **almacenamiento** (formato consistente al guardar). La normalización de esta capa es de **modelado** (escalar variables para que sean comparables entre equipos/torneos) y ocurre en tránsito, en tiempo de predicción, nunca al guardar. Son dos normalizaciones distintas y complementarias, no la misma responsabilidad duplicada. |
| `docs/06-Flujo-Operacional.md` | Las Fases 0-10 completas, el orden de agentes, el diagrama de dependencias del Engine | No se modifica ninguna fase. Esta capa es un detalle interno de la Fase 3, ejecutado por el Predictor, del mismo modo en que `docs/14-Prediction-Pipeline.md` ya detalla otro aspecto interno de esa misma Fase (el orden de archivos) sin reescribir el documento madre. |
| `docs/14-Prediction-Pipeline.md` | El orden exacto de lectura de los 11 archivos de `data/processed/selecciones-nacionales/` (Etapa 2, tabla de orden de archivos) | Esa tabla **es** la fuente de entrada de esta capa — se reutiliza tal cual, no se redefine. Esta capa toma lo que esa tabla ya entrega ordenado y lo convierte en variables. |

---

# 3. ¿Cuál es su entrada?

La entrada es siempre información de negocio, sin importar su origen físico. Concretamente, para una predicción:

- Selecciones (`selecciones.csv` o equivalente futuro).
- Competición y torneo (`competiciones.csv`, `torneos.csv`).
- Historial de partidos (`partidos.csv`).
- Estadísticas por partido (`estadisticas_partido.csv`).
- Plantilla convocada (`jugadores.csv`, `convocatorias.csv`).
- Lesiones activas (`lesiones.csv`).
- Estadio y árbitro asignados (`estadios.csv`, `arbitros.csv`).
- Cuotas de mercado, si existen (`cuotas.csv`).

**Regla de diseño central:** la capa nunca sabe si esta información vino de un CSV, una fila de PostgreSQL o la respuesta de una API. Recibe una representación de negocio ya resuelta (equivalente a un objeto/registro), nunca una consulta ni una conexión. Quien resuelve la fuente física es una responsabilidad de acceso a datos externa a esta capa (hoy, lectura de `data/processed/`; mañana, un adaptador distinto) — la capa solo consume el resultado ya resuelto.

---

# 4. ¿Cuál es su salida?

El contrato oficial que consumirá el Engine es el conjunto completo de las 12 variables de `docs/03-Variables.md`, para ambos equipos cuando aplique:

```
Variable001  — Forma Reciente
Variable002  — Rendimiento en el Torneo
Variable003  — Potencial Ofensivo
Variable004  — Solidez Defensiva
Variable005  — Compatibilidad Táctica
Variable006  — Disponibilidad de Plantilla
Variable007  — Fatiga
Variable008  — Calidad de Plantilla
Variable009  — Localía
Variable010  — Historial Directo
Variable011  — Estado Psicológico
Variable012  — Factores Externos
```

Cada variable se entrega:

- **Validada**: pasó la política de validaciones de la sección 6.
- **Normalizada**: en una escala común, comparable entre cualquier par de equipos o torneos (mismo principio ya exigido individualmente por `engine/01` y `engine/02` en su "Paso 3").
- **Completa o explícitamente marcada como no disponible**: nunca se entrega un valor inventado; si falta, se declara "no disponible" (mismo principio que la Fase 2 de `docs/06-Flujo-Operacional.md`).
- **Lista para cálculo**: en un formato que el motor puede consumir directamente, sin que el motor tenga que interpretar, limpiar o convertir nada adicional.

---

# 5. ¿Qué transformaciones realiza?

La capa convierte datos de negocio en variables estadísticas siguiendo, para cada variable, el mismo patrón conceptual:

```
Historial de partidos (partidos.csv)
        │
        ▼
Cálculo de forma reciente (últimos partidos oficiales, resultado, rival, fecha)
        │
        ▼
Variable001 (Forma Reciente) — ya validada, normalizada y lista
```

Otros ejemplos del mismo patrón (sin fórmulas — las fórmulas pertenecen exclusivamente a `models/` y `engine/`):

```
estadisticas_partido.csv (xG, disparos, conversión)
        │
        ▼
Variable003 (Potencial Ofensivo)

lesiones.csv + convocatorias.csv
        │
        ▼
Variable006 (Disponibilidad de Plantilla)

estadios.csv + torneos.csv
        │
        ▼
Variable009 (Localía) + Variable012 (Factores Externos)
```

Esta capa decide **qué dato de negocio alimenta a qué variable** y **en qué escala se entrega**. No decide **cómo esa variable se pondera o combina matemáticamente** — eso ocurre después, dentro de cada motor, con la lógica ya respaldada en `models/`.

---

# 6. ¿Qué validaciones realiza?

| Situación | Política |
|---|---|
| Dato obligatorio ausente (ej. no existe `selecciones.csv` para uno de los equipos) | **Detener el pipeline.** No se puede construir ninguna variable sin identidad de equipo. Se informa al Statistician/Orchestrator, no se continúa. |
| Dato opcional ausente (ej. árbitro aún no asignado) | **Continuar**, entregando la variable contextual correspondiente (Variable012) marcada explícitamente como "no disponible" — nunca omitida en silencio. |
| Inconsistencia de formato (ej. fecha fuera de `YYYY-MM-DD`, `id_seleccion` con formato inválido) | **Detener la construcción de esa variable puntual** y emitir una advertencia; no se corrige automáticamente (`docs/05-Base-de-Conocimiento.md`: "Nunca deberá corregirse automáticamente sin evidencia"). Si la variable es crítica (Nivel A de `docs/02-modelo.md`), se detiene todo el pipeline; si es de Nivel D, se continúa con advertencia. |
| Dato corrupto o duplicado (ej. dos filas para el mismo `id_partido`) | **Detener y emitir advertencia**, igual que cualquier duplicado detectado en la Base de Conocimiento (`docs/05-Base-de-Conocimiento.md`: "Validación" ya exige verificar duplicados; esta capa hereda esa misma regla al momento de construir la variable). |
| Muestra insuficiente (ej. menos de 3 partidos recientes para calcular Forma Reciente) | **Continuar, pero declarar confianza reducida** en esa variable puntual — no se detiene el pipeline completo por una sola variable de Nivel B/C/D, pero sí se propaga la advertencia hacia `engine/05-Confidence.md`, que ya contempla "pocos partidos analizados" como factor de incertidumbre. |
| Las 12 variables no pudieron construirse en absoluto (fallo total de entrada) | **Detener el pipeline antes de invocar cualquier motor.** No se entrega un contrato incompleto al Engine. |

**Principio rector:** esta capa nunca decide si "vale la pena" predecir con datos parciales — esa decisión de sufiencia global ya la tomó el Statistician en la Fase 2. Esta capa solo decide, variable por variable, si *esa* variable puntual puede construirse, y si no, la declara faltante en vez de inventarla o de detener el pipeline completo por una variable secundaria.

---

# 7. ¿Qué información nunca modifica?

Esta capa:

- **Nunca modifica la Base de Conocimiento** (`data/processed/`) — solo lee.
- **Nunca modifica resultados históricos** (`data/results/`).
- **Nunca modifica predicciones** (`data/predictions/`) — no participa en su registro; eso ocurre después, en la Fase 6 de `docs/06-Flujo-Operacional.md`, con la salida ya combinada de los motores.
- **Nunca altera archivos originales** de ningún directorio de `data/`.

Su única responsabilidad es **construir variables temporales**, que existen únicamente durante el ciclo de una predicción concreta y se descartan una vez que el Engine las consume. No son un dato persistente ni versionado — si se necesitara auditar exactamente qué variables se usaron en una predicción, esa evidencia vive en el registro de la predicción (`data/predictions/`, `docs/14-Prediction-Pipeline.md`, Etapa 3), no en esta capa.

---

# 8. ¿Cómo se comunica con los motores?

Mediante un único contrato: las 12 variables ya preparadas (sección 4). Los motores (`engine/01` a `engine/06`) reciben exclusivamente ese contrato — nunca reciben, ni necesitan conocer:

- Un archivo CSV.
- Una consulta SQL.
- Una respuesta de API.
- El nombre de ningún proveedor de datos.

Para un motor, la Base de Conocimiento **no existe** — solo existen variables. Esto es exactamente el desacoplamiento que exige el objetivo de esta misión: si mañana `data/processed/` migra a PostgreSQL (`docs/05-Base-de-Conocimiento.md`, sección "Evolución", ya contempla esta migración), únicamente cambia la forma en que esta capa *lee* sus datos de entrada — su salida (las 12 variables) permanece idéntica, y ningún archivo de `engine/` necesita modificarse.

---

# 9. ¿Cómo mejora la escalabilidad?

`docs/12-Roadmap.md` ya proyecta una evolución de infraestructura (v1 Excel → v2 Python → v3 Machine Learning → v4 Dashboard → v5 Automatización completa). Sin esta capa, cada uno de esos saltos de infraestructura obligaría a revisar los 6 motores uno por uno, porque hoy sus secciones "Entradas" describen datos de negocio crudos, no variables ya construidas.

Con esta capa:

- **PostgreSQL / APIs / Data Warehouse**: solo cambia la forma en que la capa *lee* sus entradas (sección 3). El contrato de salida (sección 4) no cambia, y por lo tanto ningún motor se modifica.
- **Múltiples proveedores de datos**: la capa puede combinar información de más de una fuente antes de construir una variable (ej. cuotas de dos casas de apuestas distintas) sin que el Engine perciba ninguna diferencia.
- **Machine Learning (v3 del roadmap)**: si en el futuro se decide que alguna variable se calcule mediante un modelo entrenado en lugar de una regla determinística, ese cambio ocurre dentro de esta capa (o en un componente que ella invoca) — el contrato de salida sigue siendo el mismo conjunto de 12 variables, por lo que `engine/03-Poisson.md` y el resto no necesitan enterarse del cambio.
- **Datos en tiempo real**: la capa puede pasar de ejecutarse una vez por solicitud a ejecutarse de forma continua/streaming sin que cambie su contrato de salida.

En resumen: esta capa convierte cada futuro cambio de infraestructura de datos en un cambio **local a la capa**, en lugar de un cambio **transversal a los 6 motores**.

---

# 10. ¿Qué principios de arquitectura cumple?

| Principio | Justificación |
|---|---|
| **Responsabilidad Única (SRP)** | La única razón para modificar esta capa es un cambio en cómo se obtiene o prepara una variable. Un cambio en la fórmula de Poisson no la afecta; un cambio de CSV a PostgreSQL no afecta a `engine/`. Cada componente tiene un único motivo de cambio. |
| **Bajo Acoplamiento** | Los motores dependen únicamente del contrato de 12 variables (sección 4), nunca de la forma física de `data/processed/`. La capa depende únicamente de `docs/03-Variables.md` (qué construir) y del orden ya definido en `docs/14-Prediction-Pipeline.md` (qué leer primero), no de la lógica matemática interna de ningún motor. |
| **Alta Cohesión** | Todo lo que hace esta capa —leer, validar, normalizar, construir— está orientado a un único propósito: producir variables correctas. No mezcla cálculo estadístico ni decisiones de negocio (sufiencia, apuestas). |
| **Separación de Responsabilidades** | Aplica, a nivel de esta capa, el mismo principio que ya gobierna todo el proyecto (`CLAUDE.md`: "Ningún directorio deberá asumir responsabilidades que pertenezcan a otro"): la Base de Conocimiento almacena, esta capa prepara, el Engine calcula. |
| **Escalabilidad** | Justificado en la sección 9: los cambios de infraestructura quedan contenidos dentro de la capa. |
| **Mantenibilidad** | Una variable compartida por varios motores (ej. Forma Reciente, usada hoy por `engine/01` y `engine/02`) se calcula una sola vez, en un solo lugar, en lugar de mantenerse de forma duplicada en cada motor que la use. |
| **Extensibilidad** | Agregar una futura Variable013 a `docs/03-Variables.md` solo requiere extender esta capa (su paso de "Construcción de Variables"); no requiere rediseñar la validación o normalización interna de los 6 motores existentes. |

---

# Diagramas obligatorios

## Diagrama general de la arquitectura

```
Base de Conocimiento
        │
        ▼
Capa de Preparación de Variables
        │
        ▼
Variables Normalizadas
        │
        ▼
Motores Estadísticos
        │
        ▼
Predicción
```

## Diagrama interno de la capa

```
Lectura de Datos
        │
        ▼
Validación
        │
        ▼
Normalización
        │
        ▼
Construcción de Variables
        │
        ▼
Validación Final
        │
        ▼
Entrega al Engine
```

Correspondencia con `docs/04-Algoritmo.md`: "Lectura de Datos" corresponde al Paso 1 (Recolección); "Validación" al Paso 2; "Normalización" al Paso 3; "Construcción de Variables" y "Validación Final" son, en conjunto, el Paso 4 (Cálculo de Variables) llevado a un nivel de detalle que el Algoritmo no especificaba; "Entrega al Engine" es el punto exacto donde comienza el Paso 5 (Cálculo de Fuerzas), ya ejecutado por `engine/01` y `engine/02`.

---

# Análisis crítico obligatorio

**¿Esta nueva capa realmente aporta valor?**

Sí, y de forma concreta y verificable hoy mismo, no solo hipotética: `engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` comparten al menos dos variables de entrada idénticas ("Forma Reciente", "Rendimiento en el Torneo" aparecen como "Variables Secundarias" en ambos documentos). Bajo el diseño actual, sin esta capa, cada motor tendría que obtener y normalizar esas variables de forma independiente (su propio "Paso 1-3"), con riesgo de que ambos motores terminen usando una Forma Reciente calculada de forma ligeramente distinta. Esta capa la calcula una única vez y la comparte.

**¿Existe una alternativa arquitectónica mejor?**

Se evaluaron tres alternativas y se descartaron:

- *Delegar la preparación al Statistician*: rechazado porque mezclaría una decisión de negocio (¿hay datos suficientes para predecir?) con una responsabilidad mecánica (construir cada variable), violando SRP para ese agente.
- *Dejar que cada motor prepare sus propias variables* (diseño actual documentado): rechazado porque es exactamente la duplicación descrita arriba, y porque acopla a cada motor con el formato físico de `data/processed/`.
- *Un "builder" independiente por motor*: rechazado porque no elimina la duplicación de variables compartidas entre motores (seguiría habiendo dos cálculos de Forma Reciente, solo que en dos módulos distintos en lugar de dos secciones de un mismo documento).

**¿Detectas responsabilidades mal ubicadas en otros documentos?**

Sí — ver "Observaciones del Arquitecto" a continuación. `engine/01` y `engine/02` documentan internamente (su "Paso 1", "Paso 2" y "Paso 3") exactamente la responsabilidad que esta capa asume ahora formalmente.

**¿Existe algún acoplamiento innecesario?**

Sí, de tipo documental (no de código, porque no existe código todavía): las secciones "Entradas" de `engine/01` y `engine/02` describen columnas y conceptos de negocio crudos (ej. "Disparos Totales", "Lesiones ofensivas") en lugar de variables ya preparadas. Esto acopla la lectura de esos documentos al vocabulario de la Base de Conocimiento en lugar de al vocabulario de `docs/03-Variables.md`. No es un problema funcional hoy (todo es documentación), pero fijaría una duplicación real si se implementara código directamente sobre el texto actual sin pasar antes por esta capa.

**¿Existe riesgo de duplicidad documental?**

Se mitigó activamente en el diseño de este documento (sección 2): ninguna tabla de `docs/04-Algoritmo.md`, `docs/05-Base-de-Conocimiento.md`, `docs/06-Flujo-Operacional.md` ni `docs/14-Prediction-Pipeline.md` se repite aquí; se referencian y se les asigna el componente que les faltaba.

**¿Esta incorporación mejora realmente la mantenibilidad?**

Sí, pero su beneficio completo solo se materializa cuando una misión futura (fuera del alcance de esta) actualice `engine/01` a `engine/06` para que dejen de documentar sus propios pasos 1-3 y en su lugar declaren que reciben variables ya preparadas por esta capa. Hasta que eso ocurra, esta capa es una especificación arquitectónica válida y correcta, pero coexiste documentalmente con una responsabilidad todavía duplicada en `engine/`. Esto se deja explícitamente registrado, no oculto.

---

# Observaciones del Arquitecto

Durante el análisis de esta misión se detectaron las siguientes oportunidades de mejora arquitectónica, fuera del alcance de MS-008 pero registradas para una misión futura:

1. **Duplicación de responsabilidad en `engine/01` y `engine/02`.** Ambos documentos describen internamente ("Procesamiento", Pasos 1 a 3: Obtener → Validar → Normalizar) exactamente la responsabilidad que esta nueva capa formaliza. Se recomienda una misión editorial futura que actualice esos dos motores (y, por consistencia, el resto de `engine/01-06`) para que su "Procesamiento" comience directamente en el paso de cálculo de puntuación individual, asumiendo como precondición que reciben variables ya preparadas por `docs/15-Capa-de-Preparacion-de-Variables.md`. Esta misión no realiza ese cambio (`No modificar motores` es una restricción explícita de MS-008).
2. **Variables compartidas sin fuente única.** "Forma Reciente" y "Rendimiento en el Torneo" son insumo declarado tanto de `engine/01` como de `engine/02`. Sin una capa compartida, existe riesgo de que ambos motores terminen calculándolas de forma ligeramente distinta al implementarse. Esta capa resuelve el riesgo por diseño, pero el riesgo seguirá latente en la documentación actual de los motores hasta que se aplique la recomendación 1.
3. **Inconsistencia ya conocida, aún sin corregir.** `docs/06-Flujo-Operacional.md` ya documentó (durante MS-004) que `engine/05-Confidence.md` se autodenomina en su encabezado `engine/04-Confidence.md`, y que tanto `engine/04-Chaos-Index.md` como `engine/05-Confidence.md` referencian `engine/07-Bankroll-Engine.md` y `engine/08-Simulation.md`, archivos que no existen en el repositorio. Esta misión no corrige esa inconsistencia (fuera de alcance), pero reitera la recomendación de una misión editorial dedicada exclusivamente a `engine/`.
4. **Relación entre esta capa y el campo "Método de cálculo" de `docs/03-Variables.md`.** Las 12 variables tienen ese campo marcado como "Pendiente". Se recomienda que, cuando se complete, describa la lógica **conceptual** de la transformación (qué representa, qué principio estadístico aplica), mientras que el detalle **operativo** (de qué archivos exactos se lee, en qué orden, con qué política de validación) permanezca en esta capa. Sin esa coordinación explícita, existe riesgo de que ambos documentos intenten responder la misma pregunta con distinto nivel de detalle y terminen divergiendo.
5. **Frontera con el Statistician.** El Statistician ya valida datos en la Fase 2 de `docs/06-Flujo-Operacional.md`, pero a nivel de *suficiencia* (¿hay evidencia suficiente para intentar una predicción?). Esta capa valida a nivel de *construcción* (¿este dato puntual permite construir esta variable puntual?). Ambas validaciones son necesarias y no se solapan si se mantiene esta distinción, pero conviene que una futura revisión de `.claude/agents/statistician.md` deje esta frontera explícita en el propio archivo del agente (hoy no la menciona), para que no se preste a interpretación.

Ninguna de estas observaciones contradice el diseño existente ni se implementa en esta misión — quedan documentadas como insumo para el roadmap del proyecto (`docs/12-Roadmap.md`).

---

# Relación con Datos de Mercado — actualización MR-004

Análisis posterior (`docs/24-Analisis-Arquitectonico-INC-04-INC-05.md`) identificó que `engine/06-Expected-Value.md` consume `cuotas.csv` directamente, sin pasar por esta capa (`INC-05`). Se formaliza aquí el principio de solución, sin implementarlo todavía: las cuotas **nunca** se modelarán como una Variable Oficial más de `docs/16-Contrato-Oficial-de-Variables.md` (son datos de mercado, no de rendimiento deportivo). En su lugar, esta misma capa deberá, en una implementación futura, prepararlas como una segunda categoría de salida — **Datos de Mercado** — paralela a las Variables Oficiales, con su propio contrato todavía sin diseñar. Hasta que ese contrato exista, `engine/06` continúa leyendo `cuotas.csv` directamente, como excepción documentada.

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se modifican motores (`engine/`), el algoritmo (`docs/04-Algoritmo.md`), las variables (`docs/03-Variables.md`) ni ningún otro documento existente.
- No se renombra ningún documento existente.
- No se modifica el pipeline ya definido en `docs/06-Flujo-Operacional.md` ni en `docs/14-Prediction-Pipeline.md`.
- No se define la fórmula de normalización de ninguna variable — eso pertenece a `models/` cuando se investigue cada variable en su versión 2.0.

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| 1. ¿Qué es esta capa? | Sección 1 |
| 2. ¿Dónde se ubica dentro de la arquitectura? | Sección 2 |
| 3. ¿Cuál es su entrada? | Sección 3 |
| 4. ¿Cuál es su salida? | Sección 4 |
| 5. ¿Qué transformaciones realiza? | Sección 5 |
| 6. ¿Qué validaciones realiza? | Sección 6 |
| 7. ¿Qué información nunca modifica? | Sección 7 |
| 8. ¿Cómo se comunica con los motores? | Sección 8 |
| 9. ¿Cómo mejora la escalabilidad? | Sección 9 |
| 10. ¿Qué principios de arquitectura cumple? | Sección 10 |

---

Fin del documento.
