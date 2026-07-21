# Modelo Relacional Oficial del Modelo Santiago

**Archivo:** `docs/32-Modelo-Relacional-Oficial.md`

**Misión:** DATA-004 — Modelo Relacional Oficial del Modelo Santiago

**Versión:** 1.0.0

**Estado:** Especificación oficial — modelo relacional conceptual (sin implementación física)

---

# Objetivo

`docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md` (DATA-003) ya definió **13 dominios de información** agrupados por responsabilidad y sus relaciones conceptuales de alto nivel (Equipo → participa en → Partido, etc.). Ese documento agrupa deliberadamente por responsabilidad, no por entidad individual: por ejemplo, el dominio "Competiciones y Torneos" contiene dos entidades distintas (Competición, Torneo), y "Infraestructura y Oficiales" contiene otras dos (Estadio, Árbitro).

Esta misión da el siguiente paso: descompone esos 13 dominios en **entidades conceptuales individuales**, define sus relaciones exactas, cardinalidades y claves conceptuales — sin diseñar ninguna tabla, tipo de dato, índice o clave física. Es la referencia oficial para cualquier futura implementación en PostgreSQL, MySQL, SQL Server o cualquier otro motor relacional, sin comprometerse hoy con ninguno de ellos.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué NO repite este documento |
|---|---|---|
| `docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md` | 13 dominios de información, sus relaciones de alto nivel, el ciclo de vida de los datos, la frontera entre Base de Conocimiento y ejecución | No se redefine ningún dominio ni el ciclo de vida — este documento desciende un nivel, de dominio a entidad |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Estructura del `PredictionContext`, objeto transitorio de una única ejecución | Ninguna entidad de este documento representa al `PredictionContext` — se confirma en la sección 9 que permanece fuera del modelo relacional |
| `docs/16-Contrato-Oficial-de-Variables.md` | Tipo, unidad, rango de las 12 Variables Oficiales | Las variables no son entidades relacionales — son temporales y nunca se almacenan (`docs/16` §7); se referencian solo para confirmar que ninguna entidad aquí las duplica |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | Que los motores nunca conocen el origen físico de un dato | Se reafirma como principio de frontera (sección 9), sin repetir su diseño |
| `data/processed/selecciones-nacionales/README.md` | Esquema campo por campo de las 11 entidades físicas, incluidos sus identificadores (`id_seleccion`, `id_partido`, etc.) | No se repite ningún campo — se reutilizan únicamente los identificadores ya asignados como evidencia de la "Clave técnica ya asignada" de cada entidad (sección 5) |
| `docs/27`/`docs/28` | Qué datos existen, cuáles faltan, catálogo de cantidades derivadas | Se referencian como evidencia de que ninguna entidad aquí definida introduce un dato nuevo no auditado |

Ninguna inconsistencia detectada durante este análisis se corrige aquí — se documenta, si aparece, en "Observaciones", al final.

---

# 1. Propósito

El Modelo Relacional Conceptual es la traducción de los 13 dominios de `docs/31` a un conjunto de **entidades individuales, sus relaciones, cardinalidades y claves conceptuales** — el nivel de detalle inmediatamente anterior a un modelo físico de base de datos, pero todavía completamente agnóstico de tecnología. Representa **cómo se relacionan entre sí las piezas de conocimiento del Modelo Santiago**, no cómo se almacenan físicamente.

Su propósito específico es servir de contrato único para que cualquier futura implementación relacional (PostgreSQL, MySQL, SQL Server, o incluso un motor no relacional que deba simular estas relaciones) parta de la misma estructura conceptual, sin tener que re-derivarla leyendo seis documentos de arquitectura por separado.

---

# 2. Entidades oficiales

Se listan 15 entidades — una extensión deliberada de las ~12 de ejemplo del brief, para preservar la regla de responsabilidad única ya aplicada en `docs/31` (Estadio y Árbitro son dos entidades, no una; Estadística de Partido es una entidad propia, no parte de Partido).

| # | Entidad | Descripción | Dominio de `docs/31` |
|---|---|---|---|
| 1 | **Equipo** | Una selección nacional: su identidad y fuerza declarada | Equipos |
| 2 | **Jugador** | Un futbolista individual y sus atributos | Jugadores |
| 3 | **Convocatoria** | El vínculo entre un Jugador, un Equipo y un Torneo concreto | Convocatorias |
| 4 | **Competición** | El marco organizativo permanente bajo el que se juegan torneos (ej. "Copa Mundial FIFA") | Competiciones y Torneos |
| 5 | **Torneo** | Una edición concreta de una Competición (ej. "Mundial 2026") | Competiciones y Torneos |
| 6 | **Partido** | El enfrentamiento entre dos Equipos, en un Torneo, una fecha y (opcionalmente) un Estadio y un Árbitro | Partidos |
| 7 | **Estadística de Partido** | El rendimiento numérico de un Equipo específico dentro de un Partido ya jugado | Estadísticas de Partido |
| 8 | **Estadio** | El recinto donde se juega un Partido | Infraestructura y Oficiales |
| 9 | **Árbitro** | La persona que dirige un Partido | Infraestructura y Oficiales |
| 10 | **Lesión** | Una baja médica de un Jugador, vigente en un rango de fechas | Lesiones |
| 11 | **Cuota** | El precio de mercado de un resultado de un Partido, ofrecido por una casa de apuestas | Cuotas |
| 12 | **Predicción** | El registro inmutable de qué predijo el modelo para un Partido, antes de que ocurriera | Predicciones |
| 13 | **Resultado** | El resultado oficial verificado de un Partido ya finalizado | Resultados |
| 14 | **Auditoría** | La comparación cuantitativa entre una Predicción y su Resultado correspondiente | Auditoría |
| 15 | **Propuesta de Aprendizaje** | Un diagnóstico o recomendación de cambio, respaldado por evidencia acumulada de Auditorías | Aprendizaje |

**Nota sobre la entidad 15:** igual que en `docs/31` (dominio 13), esta entidad es conceptual pero **no tiene hoy una tabla física correspondiente** — `learning/` nunca escribe en `data/` (`learning/README.md`). Se define aquí porque el brief la pide por nombre y porque omitirla ocultaría una pieza real del modelo, no porque exista ya evidencia de que necesite persistencia propia (`CLAUDE.md`: "Ningún dato podrá incorporarse únicamente por si acaso"). La misma pregunta abierta de `docs/31` sigue sin resolverse aquí.

---

# 3. Relaciones

Únicamente conceptuales — sin SQL, sin sintaxis de ningún motor relacional.

```
Equipo
  1 ----- N
Jugador                    (un Jugador pertenece, en cada momento, a un único Equipo activo)

Equipo, Jugador, Torneo
        N:M
  (resuelta por) Convocatoria

Competición
  1 ----- N
Torneo                     (una Competición tiene muchas ediciones a lo largo del tiempo)

Torneo
  1 ----- N
Partido                    (todo Partido pertenece exactamente a un Torneo, incluidos los amistosos — docs/31)

Equipo
  1 ----- N
Partido (como local)       (relación independiente de la siguiente)

Equipo
  1 ----- N
Partido (como visitante)   (un mismo Equipo participa en muchos Partidos, en dos roles distintos)

Partido, Equipo
        N:M
  (resuelta por) Estadística de Partido

Estadio
  1 ----- N
Partido                    (relación opcional: un Partido puede no tener Estadio asignado aún)

Árbitro
  1 ----- N
Partido                    (relación opcional, misma razón)

Jugador
  1 ----- N
Lesión                     (un Jugador puede tener muchas Lesiones a lo largo de su carrera)

Partido
  1 ----- N
Lesión                     (relación opcional: una Lesión puede originarse, o no, en un Partido concreto)

Partido
  1 ----- N
Cuota                      (un Partido puede tener muchas Cuotas: distintas casas, mercados, momentos de captura)

Partido
  1 ----- 1
Predicción                 (regla de negocio: nunca se genera una segunda Predicción silenciosa para el mismo Partido)

Partido
  1 ----- 1
Resultado                  (un Partido finalizado tiene exactamente un Resultado oficial)

Predicción + Resultado
        1:1 (compuesta)
Auditoría                  (una Auditoría exige que ambas existan simultáneamente — nunca antes)

N Auditorías
  ----- 1
Propuesta de Aprendizaje   (una propuesta se respalda en evidencia acumulada de muchas Auditorías, nunca de una sola)
```

---

# 4. Cardinalidades

| Tipo | Relaciones que la usan | Por qué existe |
|---|---|---|
| **1:1** | Partido↔Predicción; Partido↔Resultado; (Predicción+Resultado)↔Auditoría | Un Partido es un evento único: solo puede tener una Predicción vigente (regla de negocio, `docs/06`) y un único Resultado oficial. La Auditoría es, por definición, la comparación de exactamente un par Predicción-Resultado — nunca se audita un Partido dos veces con datos distintos |
| **1:N** | Equipo→Jugador; Competición→Torneo; Torneo→Partido; Equipo→Partido (local); Equipo→Partido (visitante); Estadio→Partido; Árbitro→Partido; Jugador→Lesión; Partido→Lesión; Partido→Cuota; Auditoría→Propuesta de Aprendizaje (N:1 vista desde el lado inverso) | El lado "1" es una entidad de referencia estable (un Equipo, una Competición, un Estadio) que participa repetidamente en muchos eventos o registros del lado "N", sin que el evento pueda existir sin su referencia |
| **N:M** | Equipo×Jugador×Torneo (resuelta por Convocatoria); Partido×Equipo (resuelta por Estadística de Partido) | Son las dos únicas relaciones del modelo donde ambos lados participan múltiples veces del otro: un Jugador puede ser convocado por su Equipo en muchos Torneos distintos, y un Torneo convoca a muchos Jugadores de muchos Equipos; un Partido produce estadísticas de sus dos Equipos, y cada Equipo acumula estadísticas de muchos Partidos. Ninguna N:M se modela directamente — ambas requieren una entidad asociativa propia (`docs/31` ya las trataba como entidades de pleno derecho, no como tablas puente accesorias) |

**Confirmación explícita:** el modelo completo tiene exactamente **dos** relaciones N:M (Convocatoria, Estadística de Partido) — ambas ya existen como entidades propias con su propia responsabilidad (sección 2), no como artefactos técnicos añadidos solo para resolver la relación.

---

# 5. Claves conceptuales

Solo identidad conceptual, clave natural y clave técnica ya asignada — ningún tipo de dato, ningún `UUID`, ningún `SERIAL`.

| Entidad | Identidad conceptual | Clave natural | Clave técnica ya asignada (`docs/31`) |
|---|---|---|---|
| Equipo | El país/federación que representa | Nombre del país + confederación | `id_seleccion` |
| Jugador | La persona física | Nombre completo + fecha de nacimiento (insuficiente por sí sola: existen homónimos) | `id_jugador` |
| Convocatoria | La participación de un Jugador en un Equipo, para un Torneo concreto | (Torneo, Equipo, Jugador) — la combinación es naturalmente única | `id_convocatoria` |
| Competición | El marco organizativo permanente | Nombre de la competición | `id_competicion` |
| Torneo | Una edición concreta de una Competición | (Competición, edición/año) | `id_torneo` |
| Partido | El enfrentamiento único entre dos Equipos, en un Torneo y fecha dados | (Torneo, Equipo local, Equipo visitante, fecha) | `id_partido` |
| Estadística de Partido | El rendimiento de un Equipo en un Partido | (Partido, Equipo) | `id_estadistica_partido` |
| Estadio | El recinto físico | Nombre + ciudad + país | `id_estadio` |
| Árbitro | La persona que dirige el partido | Nombre completo + nacionalidad (misma advertencia de homónimos que Jugador) | `id_arbitro` |
| Lesión | Un episodio médico de un Jugador | (Jugador, fecha de inicio) | `id_lesion` |
| Cuota | Un precio de mercado capturado en un instante | (Partido, casa de apuestas, mercado, resultado, fecha de captura) | `id_cuota` |
| Predicción | El acto de predecir un Partido concreto | Partido (uno solo, por regla de negocio) | `id_prediccion` (`docs/30`: `id_partido` + timestamp) |
| Resultado | El desenlace oficial de un Partido | Partido (uno solo) | Sin identificador propio documentado todavía — se referencia siempre por `id_partido` |
| Auditoría | La evaluación de una Predicción ya cerrada | (Predicción, Resultado) — siempre el mismo par | Sin identificador propio documentado todavía — se referencia por `id_prediccion` |
| Propuesta de Aprendizaje | Una recomendación de cambio respaldada por evidencia | Conjunto de Auditorías que la respaldan + fecha de la propuesta | No existe — entidad sin tabla física (sección 2) |

**Nota metodológica:** las "claves técnicas ya asignadas" de la tabla anterior **no son claves físicas inventadas para esta misión** — son los identificadores que `data/processed/selecciones-nacionales/README.md` ya documenta como columna real de cada CSV (`id_seleccion`, `id_partido`, etc.), reutilizados tal cual. Esta misión no asigna ningún identificador nuevo ni decide su tipo de dato (`STRING`, `SERIAL`, `UUID` es una decisión de implementación física, fuera de alcance).

---

# 6. Dependencias

```
Competición                                    (independiente)
    │
    ▼
Torneo                                         (depende de Competición)
    │
    ├──────────────┐
    ▼              ▼
Convocatoria    Partido                        (Partido depende de Torneo, Equipo×2, y opcionalmente Estadio/Árbitro)
    │              │
    │              ├──► Estadística de Partido  (depende de Partido + Equipo)
    │              ├──► Cuota                    (depende de Partido)
    │              ├──► Lesión (opcional)         (depende de Jugador; opcionalmente de Partido)
    │              ├──► Predicción                (depende de Partido)
    │              └──► Resultado                 (depende de Partido)
    │                        │         │
    │                        ▼         ▼
    │                    Auditoría (depende de Predicción + Resultado)
    │                        │
    │                        ▼
    │              Propuesta de Aprendizaje (depende de N Auditorías)
    ▼
Equipo, Jugador                                (Convocatoria depende de ambos, además de Torneo)

Equipo         (independiente)
Jugador        (depende de Equipo — ver sección 7)
Estadio        (independiente)
Árbitro        (independiente)
```

---

# 7. Entidades independientes

Entidades que pueden existir conceptualmente sin depender de la existencia previa de ninguna otra entidad de este modelo:

- **Equipo** — existe por sí solo (una selección nacional existe independientemente de si ya jugó algún partido).
- **Competición** — existe por sí sola (el marco organizativo puede definirse antes de que exista ninguna edición).
- **Estadio** — existe por sí solo (un recinto existe independientemente de si ya albergó un partido del modelo).
- **Árbitro** — existe por sí solo (una persona puede estar habilitada como árbitro internacional antes de dirigir un partido registrado).

**Caso intermedio, no binario (transparencia deliberada, sin forzar una clasificación limpia):** **Jugador** no es completamente independiente en el esquema actual — `data/processed/selecciones-nacionales/README.md` exige que todo Jugador tenga un `id_seleccion` (Equipo activo) — pero tampoco depende de un Partido, Torneo o Convocatoria para existir. Se lo trata aquí como "dependiente únicamente de Equipo", una categoría propia entre "independiente" y "derivada".

---

# 8. Entidades derivadas

Entidades que solo tienen sentido como consecuencia de la existencia previa de otras:

| Entidad derivada | Depende de | Por qué no puede existir antes |
|---|---|---|
| Torneo | Competición | Una edición no existe sin el marco organizativo que la define |
| Convocatoria | Equipo + Jugador + Torneo | Es, por definición, el vínculo entre los tres — no tiene identidad propia sin ellos |
| Partido | Torneo + 2 Equipos | El enfrentamiento no existe sin el marco del torneo ni sin los dos equipos que se enfrentan |
| Estadística de Partido | Partido + Equipo | Es el rendimiento *de* un partido ya definido — no puede calcularse antes de que el partido exista |
| Lesión | Jugador (y opcionalmente Partido) | Es un episodio médico *de* un jugador ya existente |
| Cuota | Partido | El mercado apuesta sobre un partido ya definido, nunca sobre un evento hipotético sin identidad |
| **Predicción** | Partido | Ejemplo del propio brief: no puede predecirse un partido que no exista |
| **Resultado** | Partido | Ejemplo del propio brief: el resultado es del partido, nunca independiente de él |
| **Auditoría** | Predicción + Resultado | Ejemplo del propio brief: la comparación exige que ambos ya existan |
| Propuesta de Aprendizaje | N Auditorías | No existe evidencia sin auditorías previas ya acumuladas |

---

# 9. Compatibilidad

| Documento | Verificación |
|---|---|
| `docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md` | Las 15 entidades de este documento son, exactamente, la descomposición de los 13 dominios en unidades individuales — ningún dominio queda sin representar, ninguna entidad nueva se introduce fuera de lo ya auditado |
| `docs/26`/`docs/29` (Runtime) | El Runtime sigue sin conocer ninguna entidad de este modelo directamente — solo consume Variables Oficiales ya preparadas (`docs/15`/`docs/16`); ninguna relación de este documento crea un acceso nuevo del Runtime a `data/` |
| `docs/30` (Prediction Context) | El `PredictionContext` **no es una entidad de este modelo relacional** — es transitorio (`docs/30` §3) y nunca se persiste como objeto completo; solo su proyección curada (`PredictionReport`) corresponde, de forma aproximada, a la entidad Predicción de este documento |
| `docs/16-Contrato-Oficial-de-Variables.md` | Ninguna de las 12 Variables Oficiales aparece como entidad de este modelo — son temporales por contrato (`docs/16` §7) y nunca se almacenan; el modelo relacional almacena los **datos físicos de origen** (Equipo, Partido, Estadística de Partido, etc.) de los que esas variables se derivan en tiempo de ejecución, nunca la variable ya calculada |
| **Architecture Freeze** (`docs/23`, Parte 6) | Sin cambios — sigue en **4 de 7** criterios (`docs/00-Project-Tracker.md`). Este documento no resuelve `INC-05`: la entidad Cuota sigue siendo, conceptualmente, la misma que hoy consume `engine/06` directamente sin pasar por `VariablePreparation` |

---

# Restricciones (confirmación de cumplimiento)

Este documento no genera SQL, `CREATE TABLE`, tipos de dato, índices, claves foráneas físicas, código, JPA ni Hibernate — toda referencia entre entidades se expresa como "depende de" o "se relaciona con", nunca como una restricción física. No se modifica ninguna Variable Oficial, motor, el Runtime, el `PredictionContext` ni ningún modelo matemático de `models/`.

---

# Validaciones obligatorias

- **¿Todas las entidades tienen una única responsabilidad?** Sí — verificado entidad por entidad en la sección 2; en particular, se evitó repetir el error que `docs/31` ya señaló como riesgo genérico (una entidad asumiendo la responsabilidad de otra): Estadística de Partido nunca registra el resultado (eso es Partido), Convocatoria nunca registra estadísticas individuales (diferido desde `MS-001`).
- **¿Existen ciclos innecesarios?** No — el grafo de dependencias de la sección 6 es acíclico: Competición → Torneo → Partido → {Estadística, Cuota, Lesión, Predicción, Resultado} → Auditoría → Propuesta de Aprendizaje, con Equipo/Jugador/Estadio/Árbitro como raíces independientes (o casi, en el caso de Jugador). Ninguna entidad depende, directa o indirectamente, de una entidad que a su vez dependa de ella.
- **¿Las cardinalidades son consistentes?** Sí, verificadas contra las restricciones ya documentadas en `docs/31`/`data/processed/selecciones-nacionales/README.md`: "un jugador solo puede tener una `id_seleccion` activa a la vez" (Equipo 1:N Jugador, no N:M); "todo partido debe tener un `id_torneo`" (Torneo 1:N Partido, obligatorio); "nunca se genera una segunda predicción silenciosamente" (Partido 1:1 Predicción).
- **¿El modelo soporta todas las fases del Prediction Pipeline?** Sí — el orden de lectura de `docs/14`, Etapa 2 (Equipo → Competición → Torneo → Estadio → Árbitro → Partido → Estadística de Partido → Jugador/Convocatoria → Lesión → Cuota) es exactamente un recorrido válido del grafo de dependencias de la sección 6, sin necesitar ninguna entidad antes de que sus dependencias ya estén resueltas.
- **¿El modelo puede implementarse en cualquier motor relacional?** Sí — ninguna sección asume sintaxis, tipo de dato o extensión propietaria de PostgreSQL, MySQL o SQL Server; las claves conceptuales (sección 5) se expresan en términos de identidad, no de mecanismo de generación (`SERIAL`, `UUID`, autoincremental), que es, precisamente, la decisión que se difiere al diseño físico.

---

# Cierre obligatorio

**1. ¿Qué problema arquitectónico resuelve este documento?**
La ausencia de un modelo relacional conceptual entre los dominios agrupados de `docs/31` y un futuro esquema físico — sin él, cualquier implementación tendría que inventar sus propias entidades, relaciones y cardinalidades a partir de documentos que describen dominios, no entidades individuales.

**2. ¿Cuántas entidades oficiales quedaron definidas?**
Quince: Equipo, Jugador, Convocatoria, Competición, Torneo, Partido, Estadística de Partido, Estadio, Árbitro, Lesión, Cuota, Predicción, Resultado, Auditoría y Propuesta de Aprendizaje (esta última sin tabla física todavía).

**3. ¿Qué relaciones son las más importantes?**
Torneo→Partido (todo partido, incluidos los amistosos, pertenece siempre a un torneo — ya una regla dura del esquema físico) y la cadena Predicción+Resultado→Auditoría→Propuesta de Aprendizaje, que es, literalmente, el mecanismo de mejora continua del Modelo Santiago (`docs/06`, Fases 8-9).

**4. ¿Qué entidades quedaron completamente desacopladas?**
Equipo, Competición, Estadio y Árbitro (sección 7) — ninguna depende de que exista previamente otra entidad de este modelo.

**5. ¿Qué entidades dependen directamente del Prediction Pipeline?**
Predicción y Resultado se generan como consecuencia directa de una ejecución del pipeline (`docs/14`/`docs/25`); Auditoría y Propuesta de Aprendizaje dependen de ellas de forma transitiva, pero no del pipeline de una predicción individual sino del ciclo posterior (`docs/06`, Fases 8-9).

**6. ¿Qué beneficios aporta para la implementación?**
Un implementador puede identificar, antes de escribir una sola línea de esquema físico, qué entidades son independientes (pueden poblarse primero), cuáles son derivadas (requieren que sus dependencias ya existan) y cuáles son las únicas dos relaciones N:M reales del sistema — reduciendo el riesgo de descubrir una dependencia circular o una relación mal cardinada ya con tablas creadas.

**7. ¿Qué parte continúa pendiente?**
Las mismas ya identificadas por `docs/31`: los datos de categoría D todavía sin capturar (`docs/27`), el Contrato de Datos de Mercado completo para la entidad Cuota (`INC-05`), y la decisión, todavía abierta, de si Propuesta de Aprendizaje necesita una tabla física propia.

**8. ¿Qué misión recomendarías después?**
Dos caminos posibles, no excluyentes: (a) una misión de diseño físico que traduzca este modelo relacional conceptual a un esquema real (tipos de dato, claves físicas, índices) para un motor concreto — la primera vez que el proyecto tomaría una decisión de stack en este eje; (b) continuar el eje ya identificado por `docs/31`/`docs/27`, capturando los datos de categoría D más críticos antes de fijar un esquema físico sobre columnas que todavía no existen.

**9. ¿El modelo relacional puede considerarse estabilizado?**
A nivel de **entidades, relaciones y cardinalidades conceptuales**, sí — las 15 entidades cubren la totalidad de lo que `docs/31` ya identificó, sin ciclos ni ambigüedad de cardinalidad detectada. A nivel de **contenido real**, no — el estado de los datos sigue siendo el mismo que describió `docs/31`: la mayoría de las entidades físicas existen solo como encabezado.

**10. ¿Qué falta para comenzar el diseño físico de PostgreSQL?**
Tres cosas, ninguna resuelta por esta misión por diseño: (a) una decisión explícita de motor relacional (PostgreSQL, MySQL u otro); (b) decidir el mecanismo de generación de identificadores (mantener los códigos legibles ya usados como `id_seleccion`, o migrar a un `SERIAL`/`UUID` técnico); (c) resolver, o al menos priorizar, los datos de categoría D (`docs/27`) que hoy dejarían columnas del esquema físico sin ningún dato real que cargar.

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Que la relación Partido↔Equipo (vía Estadística de Partido) es la mejor forma de modelar la única otra N:M del sistema, en lugar de tratar "Estadística de Partido (Local)" y "Estadística de Partido (Visitante)" como dos relaciones 1:N separadas (como se hizo con Equipo→Partido). Se prefirió la N:M porque Estadística de Partido ya es una entidad física propia con su propio identificador (`id_estadistica_partido`), a diferencia del rol local/visitante de Partido, que es un atributo de Partido, no una entidad aparte.
- **¿Qué parte de este entregable podría estar equivocada?** La clasificación de Jugador como "caso intermedio" (sección 7) es una decisión de transparencia, no una categoría estándar de modelado relacional — una implementación futura podría preferir forzarlo a "dependiente de Equipo" sin matiz, simplificando la sección 7 a solo dos categorías.
- **¿Qué información me habría hecho falta para tener más certeza?** Confirmación de si `data/results/` y `data/audit/` tendrán algún día un identificador propio documentado (hoy, sección 5, ambos se referencian solo por `id_partido`/`id_prediccion`) — sin eso, no puede confirmarse si necesitan una clave técnica propia o si su identidad siempre será heredada de Partido/Predicción.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que, al popular datos reales en las entidades hoy vacías (`torneos.csv` más allá del contenedor de amistosos, `jugadores.csv`, etc.), la cardinalidad N:M de Convocatoria efectivamente se comporte como se anticipó — hoy no hay ninguna fila real que lo confirme empíricamente.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí, ya señalada: Propuesta de Aprendizaje podría, alternativamente, no incluirse como entidad de un modelo *relacional* (por carecer de tabla física) y mencionarse solo como nota — se optó por incluirla con la misma advertencia ya usada en `docs/31`, por consistencia entre ambos documentos y porque el brief la pide explícitamente por nombre.

---

# Fuera de alcance de esta misión

- No se genera SQL, `CREATE TABLE`, tipos de dato, índices, claves foráneas físicas, código, JPA ni Hibernate.
- No se elige motor relacional (PostgreSQL, MySQL, SQL Server u otro).
- No se modifican las Variables Oficiales, los motores, el Runtime, el `PredictionContext` ni ningún modelo matemático de `models/`.
- No se resuelve si Propuesta de Aprendizaje necesita persistencia física propia — queda como pregunta abierta, heredada de `docs/31`.
- No se corrige la inconsistencia editorial de `docs/05-Base-de-Conocimiento.md` ya detectada (sin corregir) en `docs/31`.

---

Fin del documento.
