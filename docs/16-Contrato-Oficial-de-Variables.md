# Contrato Oficial de Variables del Modelo Santiago

**Archivo:** `docs/16-Contrato-Oficial-de-Variables.md`

**Versión:** 1.0.0

**Estado:** Especificación oficial — Contrato de datos (sin implementación)

---

# Objetivo

Este documento es el **contrato oficial** que deben cumplir las variables normalizadas que la Capa de Preparación de Variables (`docs/15-Capa-de-Preparacion-de-Variables.md`) entrega a los motores estadísticos (`engine/`).

`docs/03-Variables.md` ya define **qué es** cada variable (objetivo, descripción, datos necesarios). Lo que no existía hasta ahora era una definición formal de **su forma**: tipo de dato, unidad, rango, nulabilidad, quién la construye, quién la consume y cómo evoluciona. Ese es exactamente el vacío que cierra este documento — es la referencia única para cualquier componente, presente o futuro, que produzca o consuma variables.

---

# Relación con la arquitectura existente (sin duplicar)

| Documento | Qué ya define | Qué NO repite este contrato |
|---|---|---|
| `docs/03-Variables.md` | Objetivo, Descripción y Datos necesarios de cada una de las 12 variables | Esas tres secciones no se repiten aquí — este contrato las referencia por su identificador y añade únicamente los atributos de forma (tipo, unidad, rango) que `docs/03-Variables.md` deja en blanco ("Escala: Pendiente" en todas las variables actuales) |
| `docs/02-modelo.md` | La jerarquía de importancia por Nivel A-D | No se redefinen los niveles; se usan como criterio para decidir qué variables son "obligatorias" en este contrato (sección "Tabla oficial de variables") |
| `docs/05-Base-de-Conocimiento.md` | Convención de normalización de **almacenamiento** (fechas `YYYY-MM-DD`, porcentajes 0-100, probabilidades 0.00-1.00) | Este contrato reutiliza esa misma convención de escalas para las variables cuando aplica, en lugar de inventar una nueva |
| `docs/14-Prediction-Pipeline.md` | Qué archivo de `data/processed/` alimenta a qué variable (Etapa 2, tabla de orden de archivos) | No se repite esa tabla; se referencia como la "fuente de datos" de cada variable |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | Que solo esa capa puede construir variables, que los motores solo las leen, y el ciclo interno de procesamiento (Lectura → Validación → Normalización → Construcción → Validación Final → Entrega) | No se redefine ese ciclo interno; este contrato define el ciclo de vida **de la variable como objeto** (sección 7), que es una vista complementaria, no contradictoria |

Ninguna inconsistencia detectada durante este análisis se resuelve aquí — se registra únicamente en "Observaciones del Arquitecto".

---

# 1. ¿Qué es una Variable Oficial?

Una Variable Oficial es el único tipo de dato que un motor estadístico del Modelo Santiago puede recibir como entrada. Representa un aspecto medible y ya preparado del partido, de un equipo, o de la relación entre ambos equipos — nunca un dato de negocio crudo.

**Qué puede contener:** un valor único (o un valor por equipo, cuando aplica) ya validado, normalizado y con su tipo, unidad y rango fijados por este contrato.

**Qué NO puede contener:**

- Datos crudos de la Base de Conocimiento sin transformar (ej. una fila completa de `partidos.csv`).
- Referencias a la fuente física del dato (una ruta de archivo, una consulta SQL, un nombre de proveedor).
- Fórmulas, pesos o lógica de cálculo — eso pertenece a `models/` y `engine/`.
- Valores inventados para rellenar un dato faltante — si no puede construirse, se marca explícitamente como no disponible (`docs/15`, sección 6).

---

# 2. ¿Qué información mínima debe definir cada variable?

| Atributo | Dónde vive |
|---|---|
| Identificador | Este contrato (sección "Tabla oficial de variables") |
| Nombre | `docs/03-Variables.md` (ya definido, no se repite) |
| Descripción | `docs/03-Variables.md`, sección "Descripción" (ya definida, no se repite) |
| Propósito | `docs/03-Variables.md`, sección "Objetivo" (ya definido, no se repite) |
| Fuente de datos | `docs/14-Prediction-Pipeline.md`, Etapa 2 (ya definida, no se repite) |
| Responsable de construirla | Este contrato (sección "Reglas generales": siempre la Capa de Preparación de Variables) |
| Responsable de consumirla | Este contrato (columna "Consumidores principales" de la tabla oficial) |
| Tipo, Unidad, Rango, Validación | Este contrato — **el aporte real de esta misión**, ausente en cualquier otro documento hasta ahora |

---

# 3. Tipo de dato (taxonomía arquitectónica)

El contrato reconoce siete tipos conceptuales, independientes de cualquier lenguaje de programación:

| Tipo | Definición | Ejemplo ya existente en la Base de Conocimiento (ilustrativo, no una variable oficial) |
|---|---|---|
| Numérico entero | Cantidad discreta, sin decimales | `ranking_fifa_actual` en `selecciones.csv` |
| Numérico decimal | Cantidad continua | `xg` en `estadisticas_partido.csv` |
| Porcentaje | Decimal acotado 0-100 por convención (`docs/05-Base-de-Conocimiento.md`) | `posesion_pct`, `precision_pases_pct` |
| Booleano | Verdadero/Falso | `activa` en `selecciones.csv`/`competiciones.csv` |
| Fecha | `YYYY-MM-DD` (`docs/05-Base-de-Conocimiento.md`) | `ranking_fifa_fecha`, `fecha_convocatoria` |
| Texto controlado (ENUM) | Un valor de un conjunto cerrado y predefinido | `confederacion` en `selecciones.csv`; `tipo` en `competiciones.csv` |

Ninguna de las 12 variables oficiales actuales requiere el tipo `fecha` de forma nativa — las fechas son metadatos que alimentan la construcción de una variable (ej. la fecha de un partido histórico alimenta Forma Reciente), pero no son en sí mismas una variable oficial. Se documenta igualmente en la taxonomía por completitud arquitectónica, para cuando una futura variable lo requiera (`CLAUDE.md`: preferir diseñar la extensión antes de necesitarla no está permitido — "ningún dato podrá incorporarse únicamente por si acaso" — por eso aquí solo se documenta el tipo, sin crear una variable de tipo fecha sin necesidad real).

---

# 4. Unidad de medida

Ninguna variable de este contrato queda sin unidad explícita (ver columna "Unidad" en la tabla oficial). Las unidades utilizadas son:

- **Índice (0-100):** para variables compuestas de múltiples señales sin una unidad física natural (ej. Forma Reciente, Potencial Ofensivo). Reutiliza la misma convención 0-100 ya usada por `docs/02-modelo.md` para Confianza e Índice de Caos — no se inventa una escala nueva.
- **Índice relativo (-100 a 100):** para variables que representan una interacción que puede favorecer o perjudicar (Compatibilidad Táctica) — a diferencia de un índice absoluto, necesita representar dirección, no solo magnitud.
- **Porcentaje (0-100):** para variables que representan una proporción real medible (Disponibilidad de Plantilla = % de la plantilla convocada disponible).
- **Partidos (entero, con signo):** para variables de conteo directo (Historial Directo = diferencia neta de victorias).
- **Condición (ENUM):** para variables categóricas (Localía).

---

# 5. Rango permitido

Ver columna "Rango" de la "Tabla oficial de variables". Como política general, aplicable salvo que la tabla indique lo contrario para una variable puntual:

- **Valor mínimo/máximo:** todo índice usa 0-100 salvo que su naturaleza exija signo (Compatibilidad Táctica: -100 a 100; Historial Directo: sin límite fijo, con signo).
- **Negativos:** solo permitidos donde la variable representa una dirección o ventaja/desventaja (Compatibilidad Táctica, Historial Directo). El resto nunca acepta negativos.
- **Decimales:** permitidos en todas las variables de tipo decimal; no aplican a Historial Directo (entero) ni a Localía (ENUM).
- **Valores nulos:** permitidos únicamente en variables no obligatorias (ver columna "Obligatoria"); nunca en las variables de Nivel A (`docs/02-modelo.md`) salvo la excepción explícita de un equipo debutante en el torneo (Variable002).
- **Valor por defecto:** **ninguna variable de este contrato tiene valor por defecto.** Asignar un valor por defecto (ej. 50 en una escala 0-100) equivaldría a inventar un dato, prohibido por `CLAUDE.md` ("Nunca inventar datos"). Cuando una variable no puede construirse, se entrega marcada explícitamente como no disponible, nunca con un valor neutro implícito.

---

# 6. Reglas de validación

Esta sección formaliza, a nivel de variable individual, la política ya definida en `docs/15-Capa-de-Preparacion-de-Variables.md` (sección 6):

| Situación | Regla |
|---|---|
| Variable obligatoria (Nivel A) no puede construirse | **Detener el pipeline.** No se genera una predicción sin una variable de Nivel A. |
| Variable no obligatoria (Nivel B/C/D) no puede construirse | **Continuar**, entregarla marcada como no disponible, y propagar esa ausencia a `engine/05-Confidence.md` (menor confianza). |
| Valor fuera del rango declarado en la tabla oficial | **Rechazar el valor y detener la construcción de esa variable puntual** — nunca truncar ni forzar el valor dentro del rango silenciosamente. |
| Valor de tipo incorrecto (ej. texto donde se espera decimal) | **Rechazar y emitir advertencia** — es un error de la capa de lectura, no de la variable; se detiene la construcción de esa variable. |
| Variable puede estimarse a partir de una muestra reducida (ej. 1 solo partido reciente) | **Puede entregarse**, pero marcada con confianza reducida — nunca se descarta solo por tener poca muestra si al menos existe un dato verificable. |
| Variable requeriría inventar el dato faltante | **Nunca.** Se marca como no disponible en su lugar, sin excepción. |

---

# 7. Ciclo de vida

```
Creación
    │
    ▼
Validación
    │
    ▼
Normalización
    │
    ▼
Entrega al Engine
    │
    ▼
Destrucción
```

Esta es la vista del ciclo de vida **de una variable como objeto**, complementaria (no contradictoria) al ciclo de vida **del proceso interno de la capa** ya definido en `docs/15-Capa-de-Preparacion-de-Variables.md` (Lectura de Datos → Validación → Normalización → Construcción de Variables → Validación Final → Entrega al Engine): "Creación" agrupa la lectura y construcción; "Destrucción" formaliza lo que `docs/15` ya establecía de forma implícita ("variables temporales... se descartan una vez que el Engine las consume").

Las variables **son siempre temporales**: existen únicamente durante el ciclo de una predicción concreta y nunca forman parte permanente de la Base de Conocimiento (`data/processed/`). Una nueva solicitud de predicción para el mismo partido reconstruye las variables desde cero — no se reutilizan instancias de una solicitud anterior, para evitar variables obsoletas si la Base de Conocimiento cambió entre solicitudes (ej. una lesión nueva registrada).

---

# 8. Inmutabilidad

Una vez entregada al Engine, una variable **no puede modificarse por nadie**, bajo ninguna circunstancia:

- Los motores (`engine/01` a `engine/06`) únicamente **leen** variables — nunca las escriben ni las corrigen (`docs/15`, sección "Reglas generales").
- Ni el Predictor, ni el Odds Analyzer, ni el Bankroll Manager pueden alterar el valor de una variable ya entregada; si un motor detecta un problema con una variable, su única acción posible es declarar su salida como no confiable o no disponible — nunca corregir la variable en sí (misma restricción ya vigente en cada `engine/0X.md`: "nunca estimará/inventará datos inexistentes").
- Únicamente la Capa de Preparación de Variables puede **volver a construir** una variable — nunca modificar la ya entregada. Reconstruir significa generar una instancia nueva, no editar la existente.
- Las variables dejan de existir (Destrucción, sección 7) inmediatamente después de que el Engine las consume para una predicción concreta.

---

# 9. Versionado

Este contrato evoluciona bajo las mismas reglas de Versionado Semántico ya adoptadas por el proyecto (`CHANGELOG.md`: "este proyecto se adhiere a Versionado Semántico"):

| Cambio | Tipo de versión | Regla |
|---|---|---|
| Agregar una variable nueva (Variable013 en adelante) | MINOR | Debe documentarse primero en `docs/03-Variables.md` (Objetivo, Descripción, Datos necesarios) y solo después incorporarse a la tabla de este contrato — nunca al revés. El identificador es el siguiente número consecutivo; nunca se reutiliza uno ya asignado, ni siquiera si una variable anterior fue deprecada. |
| Ampliar un rango sin afectar a los consumidores existentes | MINOR/PATCH | Los motores que ya consumían la variable siguen funcionando sin cambios. |
| Reducir un rango, cambiar el tipo, o cambiar la unidad | MAJOR | Requiere revisar cada motor consumidor listado en la tabla oficial antes de adoptar la nueva versión — es un cambio incompatible por definición. |
| Cambiar el significado de una variable existente | Equivale a una variable nueva | Nunca se reutiliza un identificador existente con un significado distinto (mismo principio de integridad referencial que `id_seleccion`/`id_competicion` en `data/processed/selecciones-nacionales/README.md`: los identificadores son inmutables una vez asignados). |
| Eliminar una variable | MAJOR | Nunca se elimina en silencio: se marca como "Deprecada" (con motivo documentado) y se conserva en el historial de este contrato — mismo principio que `data/archive/` ("Nunca eliminar información"), aplicado aquí al historial de decisiones del contrato, no a datos históricos de partidos. |

Todo cambio de este tipo debe registrarse en `CHANGELOG.md` y en `docs/11-Versiones.md`, con la evidencia estadística que lo respalde cuando el cambio afecte el rango o el significado (`CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística", aplicado aquí a la forma de la variable, no a su peso dentro de un motor).

---

# 10. Compatibilidad

Este contrato es deliberadamente **agnóstico de tecnología**: define tipo, unidad y rango en términos conceptuales, nunca en términos de un lenguaje o motor de base de datos concreto. Esto permite que:

- **Nuevos motores** (ej. un futuro motor de simulación Monte Carlo, mencionado en `engine/03-Poisson.md`, "Mejoras Futuras") puedan consumir exactamente las mismas 12 variables sin negociar un formato nuevo.
- **Nuevos modelos matemáticos** (Dixon-Coles, Bivariate Poisson, Bayesian Poisson, Machine Learning — todos ya previstos en `engine/03-Poisson.md` y `docs/12-Roadmap.md` v3) puedan sustituir la lógica interna de un motor sin que cambie el contrato de entrada.
- **Nuevas fuentes de datos** (PostgreSQL, APIs, múltiples proveedores — ya previstos en `docs/15`, sección 9) puedan alimentar la Capa de Preparación de Variables sin que el contrato de salida hacia los motores se altere.
- **Nuevas tecnologías de implementación** (Java, Python, o cualquier otra) puedan implementar tanto la Capa como los motores: un tipo "Decimal, rango 0-100, sin nulos" se traduce de forma directa a un `float`/`double` con una validación de rango en cualquier lenguaje, sin ambigüedad.

La condición necesaria para que esto se cumpla es que **ninguna implementación futura se salte este contrato** — es decir, que toda nueva tecnología se conecte a través de la Capa de Preparación de Variables (que sí puede cambiar libremente) y nunca directamente a los motores (que dependen únicamente de este contrato, nunca de la fuente).

---

# Reglas generales

- **Ningún motor modifica variables.** Los motores (`engine/01` a `engine/06`) únicamente las leen.
- **La Base de Conocimiento nunca consume variables.** `data/processed/` es el origen de los datos de negocio, nunca el destino de una variable ya construida.
- **Únicamente la Capa de Preparación de Variables puede construir variables** (`docs/15-Capa-de-Preparacion-de-Variables.md`).
- **Las variables nunca se almacenan permanentemente** como parte del conocimiento histórico — no existe (ni debe existir) un `data/processed/variables.csv`; son estrictamente temporales (sección 7).

---

# Tabla oficial de variables

| ID | Nombre | Tipo | Unidad | Rango | Obligatoria | Puede ser nula | Responsable de construcción | Consumidores principales |
|---|---|---|---|---|---|---|---|---|
| Variable001 | Forma Reciente | Decimal | Índice (0-100) | 0 a 100, sin negativos | Sí | No | Capa de Preparación de Variables | `engine/01`, `engine/02` |
| Variable002 | Rendimiento en el Torneo | Decimal | Índice (0-100) | 0 a 100, sin negativos | Sí | Solo si el equipo debuta en el torneo actual | Capa de Preparación de Variables | `engine/01`, `engine/02` |
| Variable003 | Potencial Ofensivo | Decimal | Índice (0-100), derivado de xG/disparos | 0 a 100, sin negativos | Sí | No | Capa de Preparación de Variables | `engine/01` |
| Variable004 | Solidez Defensiva | Decimal | Índice (0-100), derivado de xGA | 0 a 100, sin negativos | Sí | No | Capa de Preparación de Variables | `engine/02` |
| Variable005 | Compatibilidad Táctica | Decimal | Índice relativo (-100 a 100) | -100 a 100, acepta negativos | Sí (Nivel A, `docs/02-modelo.md`) | Sí, en la práctica actual (ver Observaciones) | Capa de Preparación de Variables | Sin consumidor explícito declarado en `engine/` (ver Observaciones del Arquitecto) |
| Variable006 | Disponibilidad de Plantilla | Decimal | Porcentaje (0-100) | 0 a 100, sin negativos | No | Sí | Capa de Preparación de Variables | `engine/01`, `engine/02`, `engine/04`, `engine/05` |
| Variable007 | Fatiga | Decimal | Índice (0-100) | 0 a 100, sin negativos | No | Sí | Capa de Preparación de Variables | `engine/01`, `engine/02`, `engine/04` |
| Variable008 | Calidad de Plantilla | Decimal | Índice (0-100) | 0 a 100, sin negativos | No (Nivel C) | Sí | Capa de Preparación de Variables | Sin consumidor explícito declarado en `engine/` (ver Observaciones del Arquitecto) |
| Variable009 | Localía | Texto controlado (ENUM) | Condición: `local` / `visitante` / `neutral` | Valores permitidos: los tres anteriores | No (Nivel D) | Sí, si la sede aún no está definida | Capa de Preparación de Variables | Sin consumidor explícito declarado en `engine/` (ver Observaciones del Arquitecto) |
| Variable010 | Historial Directo | Entero | Partidos (diferencia neta de victorias) | Sin límite fijo, acepta negativos | No (Nivel D) | Sí | Capa de Preparación de Variables | Sin consumidor explícito declarado en `engine/` (ver Observaciones del Arquitecto) |
| Variable011 | Estado Psicológico | Decimal | Índice (0-100) | 0 a 100, sin negativos | No (sin nivel asignado en `docs/02-modelo.md`, ver Observaciones) | Sí | Capa de Preparación de Variables | Sin consumidor explícito declarado en `engine/` (ver Observaciones del Arquitecto) |
| Variable012 | Factores Externos | Decimal | Índice (0-100) | 0 a 100, sin negativos | No (Nivel D) | Sí | Capa de Preparación de Variables | `engine/04` |

Los identificadores `VariableNNN` corresponden exactamente a los encabezados "# Variable NNN" de `docs/03-Variables.md` — no se crea una numeración paralela.

---

# Diagramas

## Diagrama general de la arquitectura

```
Base de Conocimiento
        │
        ▼
Capa de Preparación de Variables
        │
        ▼
Variables Oficiales
        │
        ▼
Motores
        │
        ▼
Predicción
```

## Diagrama de ciclo de vida de una variable

```
Creación
    │
    ▼
Validación
    │
    ▼
Normalización
    │
    ▼
Entrega al Engine
    │
    ▼
Destrucción
```

---

# Observaciones del Arquitecto

Durante el análisis de esta misión se cruzó, variable por variable, la jerarquía de importancia de `docs/02-modelo.md` (Niveles A-D) y la sección "Entradas" de cada uno de los 6 motores (`engine/01` a `engine/06`) contra las 12 variables de `docs/03-Variables.md`. Los hallazgos son los siguientes:

1. **Cinco de las doce variables oficiales no tienen un consumidor explícito declarado en ningún motor actual**: Compatibilidad Táctica (Variable005), Calidad de Plantilla (Variable008), Localía (Variable009), Historial Directo (Variable010) y Estado Psicológico (Variable011). Ninguna sección "Entradas" de `engine/01` a `engine/06` las cita por su nombre exacto. Esto es especialmente relevante para **Variable005**, porque `docs/02-modelo.md` la clasifica en **Nivel A (Muy Alto)** — el mismo nivel que Forma Reciente y xG — y sin embargo ningún motor documenta cómo la consume. Se recomienda una misión futura que, al actualizar `engine/01-06` (ver recomendación de MS-008), declare explícitamente qué motor consume cada una de estas cinco variables, o bien documente por qué deliberadamente no participan todavía en ningún cálculo.
2. **Variable011 (Estado Psicológico) no aparece clasificada en ningún Nivel A-D de `docs/02-modelo.md`.** Es la única de las 12 variables sin una jerarquía de importancia asignada — no está claro si su peso relativo pretendido es alto, medio o bajo. Se recomienda que una futura revisión de `docs/02-modelo.md` la incorpore explícitamente a alguno de los cuatro niveles (o a un nivel nuevo), en lugar de dejarla implícita.
3. **Variable003 (Potencial Ofensivo) y Variable004 (Solidez Defensiva) usan una etiqueta distinta a la de `docs/02-modelo.md`** (que las nombra literalmente "xG" y "xGA" en su lista de Nivel A). El significado coincide y la trazabilidad es clara a través de `engine/01`/`engine/02`, pero la inconsistencia terminológica podría confundir a un lector nuevo que busque "xG" como variable y no la encuentre con ese nombre exacto en `docs/03-Variables.md`. Se sugiere, para una futura misión editorial, añadir una nota cruzada en `docs/02-modelo.md` o `docs/03-Variables.md` que haga explícita la equivalencia.
4. **Este contrato es la primera vez que se fijan tipo, unidad y rango para las 12 variables** — `docs/03-Variables.md` dejaba el campo "Escala" como "Pendiente" en las doce. Los valores aquí definidos (mayoritariamente índices 0-100, con las excepciones justificadas de Compatibilidad Táctica e Historial Directo) son una propuesta arquitectónica razonada a partir de la naturaleza de cada variable, **no una validación estadística** — cuando `models/` desarrolle el "Método de cálculo" real de cada variable (pendiente también en `docs/03-Variables.md`), podría requerirse un ajuste de rango con evidencia, lo cual está previsto en la sección "Versionado" de este contrato.
5. **Ninguna variable está, hoy, acoplada de forma rígida a una fuente de datos** — las 12 se definen en términos de la Capa de Preparación de Variables, nunca de una columna CSV específica. El riesgo de acoplamiento identificado no está en las variables en sí, sino en los propios motores (`engine/01`, `engine/02`), cuyas secciones "Entradas" listan conceptos de negocio crudos en lugar de variables ya preparadas — mismo hallazgo ya registrado en `docs/15-Capa-de-Preparacion-de-Variables.md` y no se repite en detalle aquí.
6. **Suficiencia para futuras implementaciones en Java, Python u otra tecnología:** el contrato es suficiente en su nivel actual (tipo, unidad, rango, nulabilidad) para iniciar una implementación en cualquier lenguaje. Lo que **no** es suficiente todavía — y está correctamente fuera del alcance de esta misión — es el método exacto de cálculo de cada variable (pertenece a `models/`) y el mecanismo físico de serialización entre la Capa y los motores (ej. un objeto en memoria, un mensaje, un DTO), que solo podrá definirse cuando exista una decisión de stack tecnológico, hoy inexistente en el proyecto.

Ninguna de estas observaciones contradice el diseño existente ni se implementa en esta misión — quedan documentadas como insumo para el roadmap del proyecto (`docs/12-Roadmap.md`) y para la misión editorial de `engine/` ya recomendada en `docs/00-Project-Tracker.md` (MS-008).

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se modifican motores, el algoritmo (`docs/04-Algoritmo.md`), las variables existentes (`docs/03-Variables.md`) ni ningún otro documento existente.
- No se cambia la Base de Conocimiento (`data/`, `docs/05-Base-de-Conocimiento.md`).
- No se define el método de cálculo (fórmula) de ninguna variable — pertenece a `models/`.
- No se resuelven las inconsistencias detectadas (sección "Observaciones del Arquitecto") — quedan registradas para una misión futura.

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| 1. ¿Qué es una Variable Oficial? | Sección 1 |
| 2. ¿Qué información mínima debe definir cada variable? | Sección 2 |
| 3. Tipo de dato | Sección 3 |
| 4. Unidad de medida | Sección 4 |
| 5. Rango permitido | Sección 5 |
| 6. Reglas de validación | Sección 6 |
| 7. Ciclo de vida | Sección 7 |
| 8. Inmutabilidad | Sección 8 |
| 9. Versionado | Sección 9 |
| 10. Compatibilidad | Sección 10 |

---

Fin del documento.
