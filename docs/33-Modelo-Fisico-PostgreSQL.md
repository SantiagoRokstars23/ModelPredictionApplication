# Modelo Físico Oficial PostgreSQL del Modelo Santiago

**Archivo:** `docs/33-Modelo-Fisico-PostgreSQL.md`

**Misión:** DATA-005 — Modelo Físico Oficial PostgreSQL del Modelo Santiago

**Versión:** 1.1.0

**Estado:** Especificación oficial — modelo físico conceptual para PostgreSQL (sin implementación)

---

# Nota de verificación previa

*(Nota histórica, preservada tal cual se escribió originalmente en `DATA-005` — ver "Nota de reconciliación (GR-008)" más abajo para su resolución.)*

Esta misión es la primera del proyecto que compromete una **tecnología concreta de almacenamiento** (PostgreSQL) y, en su sección 9, hace referencia explícita a Flyway, Liquibase, Spring Data JPA y Hibernate — es decir, asume implícitamente Java/Spring Boot como stack de implementación futura, algo que ninguna misión `DEV-`/`GOV-` anterior había formalizado todavía (`docs/26`/`docs/29` afirman explícitamente "no elige lenguaje ni tecnología... fuera de alcance de toda la serie `DEV-`"). Este documento ejecuta el encargo tal como está definido —el diseño físico en sí no depende de que Java sea o no el lenguaje final, PostgreSQL es independiente del lenguaje de aplicación— pero deja registrado en "Observaciones" que la elección de stack sigue sin una misión `GOV-`/`DEV-` dedicada que la declare oficialmente.

---

# Nota de reconciliación (GR-008)

La ambigüedad señalada arriba **ya quedó resuelta**: `docs/34-Decision-Oficial-del-Stack-Tecnologico.md` (`ARCH-000`) congeló oficialmente **Python + FastAPI + SQLAlchemy 2.x + Alembic** como stack del Modelo Santiago V1 — no Java/Spring Boot/Hibernate/JPA/Flyway/Liquibase. Esta misión (`GR-008`) sincroniza el texto de este documento con esa decisión. El **modelo físico en sí** (las 14 tablas, sus tipos conceptuales, claves e índices de las secciones 2 a 8) no requirió ningún cambio de fondo — ya era agnóstico de ORM y de lenguaje, como corresponde a un documento de diseño, no de implementación. Únicamente la sección 9 ("Compatibilidad") y las referencias puntuales a herramientas específicas de Java se actualizaron para reflejar el stack realmente vigente. Ninguna referencia se eliminó en silencio: donde una mención pertenecía a una etapa histórica real del proyecto, se conservó con una nota aclaratoria (Constitución, Art. 8, Trazabilidad).

---

# Objetivo

`docs/32-Modelo-Relacional-Oficial.md` (DATA-004) definió 15 entidades conceptuales, sus relaciones, cardinalidades y claves conceptuales, sin comprometerse con ningún motor relacional. Esta misión traduce ese modelo a un **Modelo Físico para PostgreSQL específicamente**: nombres físicos, tipos de dato conceptuales, estrategia de identificadores, índices recomendados y restricciones de integridad — sin escribir una sola sentencia SQL, sin generar migraciones, sin código.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué NO repite este documento |
|---|---|---|
| `docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md` | 13 dominios de información y su ciclo de vida | No se redefine ningún dominio |
| `docs/32-Modelo-Relacional-Oficial.md` | 15 entidades, relaciones, cardinalidades, claves conceptuales | Ninguna entidad, relación o cardinalidad se redefine — este documento las traduce a PostgreSQL, no las rediseña |
| `docs/16-Contrato-Oficial-de-Variables.md` | Tipo, unidad, rango de las 12 Variables Oficiales | Las variables no tienen tabla física (son temporales, `docs/16` §7); no se repiten aquí |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Estructura del `PredictionContext`, incluida la proyección `PredictionReport` que sí se persiste | Se reutiliza esa proyección, campo por campo, para diseñar la tabla física `predicciones` |
| `data/processed/selecciones-nacionales/README.md` | Esquema campo por campo, con tipo lógico (`STRING`, `INTEGER`, `DATE`, `BOOLEAN`, `DECIMAL`, `ENUM`) y restricciones de las 11 entidades físicas ya existentes | No se repite ninguna justificación de campo — se reutilizan los mismos campos, asignándoles su tipo conceptual PostgreSQL y su rol físico (PK/FK/UNIQUE) |

Ninguna inconsistencia detectada durante este análisis se corrige aquí — se documenta en "Observaciones".

---

# 1. Propósito

El Modelo Físico PostgreSQL es la traducción del Modelo Relacional Conceptual (`docs/32`) a las decisiones concretas que exige un motor relacional real: cómo se llama cada tabla, qué tipo de columna representa cada dato, cómo se implementa cada relación, qué se indexa y qué restricciones de integridad se aplican. Es, deliberadamente, **específico de PostgreSQL** en sus recomendaciones de tipo (`JSONB`, `TIMESTAMPTZ`, índices parciales), pero no genera ni una sola sentencia ejecutable — sigue siendo un documento de diseño, no un artefacto de migración.

---

# 2. Convenciones generales

| Convención | Regla adoptada | Justificación |
|---|---|---|
| **Nombres** | `snake_case` en tablas y columnas | Ya es la convención real de los 11 CSV existentes (`id_seleccion`, `ranking_fifa_actual`) — continuidad total, cero fricción de traducción |
| **Tablas: singular o plural** | **Plural** (`selecciones`, `jugadores`, `partidos`) | Los archivos físicos ya existentes usan plural (`selecciones.csv`, `jugadores.csv`, `partidos.csv`) — se preserva la convención ya establecida en vez de introducir una nueva |
| **Nombre físico de tabla vs. nombre de entidad conceptual** | La tabla usa el nombre de dominio ya establecido (`selecciones`), no el nombre genérico de la entidad conceptual (`Equipo`, `docs/32`) | `docs/32` usa "Equipo" por generalidad conceptual; el vocabulario físico del proyecto, ya consolidado desde `MS-001`, es "selección" — cambiarlo ahora rompería la trazabilidad de quince documentos previos sin ningún beneficio |
| **Clave primaria (columna)** | `id` (mismo nombre en las 15 tablas) | Uniformidad: facilita el mapeo ORM (sección 9) y evita que cada tabla tenga una convención distinta para su clave técnica |
| **Clave de negocio (columna)** | Se conserva el nombre ya usado (`id_seleccion`, `id_partido`, etc.), como columna `UNIQUE`, no como PK física | Preserva la legibilidad y trazabilidad ya usada en `docs/03`, `docs/14`, `docs/16`, `docs/17` y el resto del proyecto — desarrollado en la sección 8 |
| **Clave foránea (columna)** | `<entidad_referenciada_singular>_id` (ej. `torneo_id`, `seleccion_local_id`, `jugador_id`) | Distingue sin ambigüedad una referencia técnica (`torneo_id` → `torneos.id`) de un código de negocio (`id_torneo`) — evita que una columna con el mismo prefijo ("id_torneo") tenga dos significados distintos en dos tablas |
| **Timestamps** | Toda tabla **mutable** (permite corrección documentada con el tiempo) tiene `creado_en` y `actualizado_en` (`TIMESTAMPTZ`). Toda tabla **inmutable por regla de negocio** (`predicciones`, `resultados`, `auditorias`, `cuotas`) tiene únicamente `creado_en` | La ausencia de `actualizado_en` en las tablas inmutables hace visible, al nivel del propio esquema, un principio que hasta ahora solo existía como regla documental (`docs/14`: "nunca se modifica una predicción") — un intento de `UPDATE` sobre esas tablas no tendría ninguna columna de auditoría de cambio que lo respalde, sin necesidad de un trigger |
| **Auditoría de "quién" hizo un cambio** | No se define ninguna columna `creado_por`/`modificado_por` | No existe todavía ninguna entidad "Usuario/Operador" en `docs/32` — agregar esa columna hoy sería un dato sin consumidor, violando el Principio de Justificación de Datos (`docs/05`) |
| **Versionado de fila** | No se adopta un contador de versión optimista (ej. `version_id_col` de SQLAlchemy) como regla general — se deja como recomendación opcional para tablas de referencia mutables (sección 9), no como convención obligatoria | No existe hoy evidencia de concurrencia de escritura simultánea sobre una misma fila que lo justifique (`CLAUDE.md`: "ningún dato podrá incorporarse únicamente por si acaso") |
| **ENUM textual vs. tipo `ENUM` nativo de PostgreSQL** | Todo campo categórico (`confederacion`, `tipo`, `fase`, `gravedad`, `mercado`, etc.) se implementa como `TEXT` restringido por `CHECK`, nunca como tipo `ENUM` nativo | Un tipo `ENUM` nativo de PostgreSQL requiere `ALTER TYPE` para agregar un valor nuevo — una operación incómoda de migrar y bloqueante en algunas versiones. `TEXT` + `CHECK` permite ampliar valores con una migración aditiva simple, más compatible con el principio de "Desarrollo Incremental" (`docs/21`, Art. 2.7) |

---

# 3. Tipos de datos oficiales

Solo el tipo conceptual — ningún `CREATE TABLE`, ninguna precisión/escala exacta (se define en la migración física real, fuera de esta misión).

| Tipo conceptual | Uso | Justificación |
|---|---|---|
| **UUID** | Toda clave técnica (`id`) y toda clave foránea (`*_id`) | Desarrollado en la sección 8 |
| **TEXT** | Toda cadena de longitud variable: nombres, descripciones, códigos de negocio, campos categóricos restringidos por `CHECK` | PostgreSQL no penaliza `TEXT` frente a `VARCHAR(n)` en rendimiento — usar `TEXT` evita fijar un límite arbitrario de longitud que después obligue a una migración para ampliarlo |
| **BOOLEAN** | Indicadores de dos estados (`activa`, `techado`, `activo_seleccion`, `acierto_top1`) | Corresponde exactamente al tipo `BOOLEAN` ya declarado en `data/processed/selecciones-nacionales/README.md` |
| **DATE** | Fechas sin componente de hora (`fecha_nacimiento`, `fecha`, `fecha_inicio`, `fecha_fin`) | Ya es la convención de `docs/05` (`YYYY-MM-DD`); `DATE` es su equivalente exacto en PostgreSQL |
| **TIME** | Hora local sin fecha (`hora_local` de `partidos`) | Mejora conceptual respecto al `STRING` original de `data/processed/selecciones-nacionales/README.md`: es la hora del partido en el huso horario del estadio, no un instante global — no necesita zona horaria propia |
| **TIMESTAMPTZ** (timestamp con zona horaria) | Todo instante preciso que combina fecha y hora en un contexto potencially multi-huso (`fecha_captura` de cuotas, `creado_en`/`actualizado_en`, `fecha_auditoria`, `fecha_registro` de resultados) | El Modelo Santiago opera con selecciones y competiciones de husos horarios distintos (Variable012, Factores Externos); usar `TIMESTAMPTZ` en vez de `TIMESTAMP` evita ambigüedad de zona horaria, un error común y difícil de detectar después |
| **INTEGER** | Conteos y cantidades enteras acotadas (`ranking_fifa_actual`, `disparos_totales`, `jornada`, `capacidad`, `altitud_metros`, `dorsal`, `asistencia`) | Ninguna de estas cantidades se acerca al límite de `INTEGER` (±2.147.483.647); reservar `BIGINT` para estos campos sería complejidad sin beneficio (`CLAUDE.md`) |
| **NUMERIC** | Toda cantidad decimal (`xg`, `posesion_pct`, `precision_pases_pct`, `cuota_decimal`, `probabilidad_local/empate/visitante`, `confianza`, `indice_caos`, `valor_esperado`) | Se prioriza precisión decimal exacta y reproducibilidad (Constitución Art. 2.3) sobre el rendimiento marginal de `DOUBLE PRECISION` — no existe hoy evidencia de volumen de datos que haga relevante esa diferencia de rendimiento; usar un único tipo decimal para todo el proyecto evita además dos convenciones numéricas paralelas |
| **JSONB** | Únicamente dos campos: `predicciones.top_marcadores` (lista de pares marcador/probabilidad) y `predicciones.variables_influyentes` (lista de variables que más pesaron) | Ambos son estructuras de forma variable (el Top 4 de marcadores no tiene una cardinalidad fija de columnas relacionales razonable) que se leen siempre completas junto con el resto de la predicción y casi nunca se consultan de forma aislada por su contenido interno — exactamente el caso de uso que justifica `JSONB` en vez de forzar una tabla adicional. Ningún otro campo del modelo usa `JSONB`: todos los demás datos tienen una forma fija y se benefician de columnas relacionales normales |

---

# 4. Entidades físicas

Quince tablas — mismas 15 entidades de `docs/32`, con nombre físico ya justificado (sección 2). Los campos ya documentados en `data/processed/selecciones-nacionales/README.md` se reutilizan tal cual, sin repetir su justificación de negocio; esta sección solo asigna tipo conceptual y rol físico (PK/FK/obligatoriedad/unicidad).

## 4.1 `selecciones` (Equipo)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_seleccion` | TEXT | Clave de negocio | Sí | Sí |
| `nombre_pais` | TEXT | — | Sí | No |
| `nombre_federacion` | TEXT | — | Sí | No |
| `confederacion` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `ranking_fifa_actual` | INTEGER | — | Sí | No |
| `ranking_fifa_fecha` | DATE | — | Sí | No |
| `seleccionador_actual` | TEXT | — | No (cargo puede estar vacante) | No |
| `activa` | BOOLEAN | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.2 `jugadores` (Jugador)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_jugador` | TEXT | Clave de negocio | Sí | Sí |
| `nombre_completo` | TEXT | — | Sí | No |
| `nombre_conocido` | TEXT | — | No | No |
| `fecha_nacimiento` | DATE | — | Sí | No |
| `posicion_principal` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `pie_habil` | TEXT (`CHECK` ENUM) | — | No | No |
| `altura_cm` | INTEGER | — | No | No |
| `seleccion_id` | UUID | FK → `selecciones.id` | Sí | No |
| `club_actual` | TEXT | — | No | No |
| `activo_seleccion` | BOOLEAN | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.3 `convocatorias` (asociativa N:M: Equipo × Jugador × Torneo)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_convocatoria` | TEXT | Clave de negocio | Sí | Sí |
| `torneo_id` | UUID | FK → `torneos.id` | Sí | Compuesta (ver abajo) |
| `seleccion_id` | UUID | FK → `selecciones.id` | Sí | Compuesta |
| `jugador_id` | UUID | FK → `jugadores.id` | Sí | Compuesta |
| `dorsal` | INTEGER | — | Sí | Compuesta (con torneo/selección) |
| `posicion_convocatoria` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `fecha_convocatoria` | DATE | — | Sí | No |
| `estado_convocatoria` | TEXT (`CHECK` ENUM — pendiente de formalizar del todo, `docs/27`) | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

**Únicos compuestos:** (`torneo_id`, `seleccion_id`, `jugador_id`); (`torneo_id`, `seleccion_id`, `dorsal`).

## 4.4 `competiciones` (Competición)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_competicion` | TEXT | Clave de negocio (`COMP-NNNNNN`) | Sí | Sí |
| `nombre` | TEXT | — | Sí | Sí |
| `confederacion_organizadora` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `tipo` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `periodicidad_anios` | INTEGER | — | No | No |
| `activa` | BOOLEAN | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.5 `torneos` (Torneo)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_torneo` | TEXT | Clave de negocio | Sí | Sí |
| `competicion_id` | UUID | FK → `competiciones.id` | Sí | No |
| `edicion` | TEXT | — | Sí | No |
| `paises_organizadores` | TEXT | — | No | No |
| `fecha_inicio` | DATE | — | Sí | No |
| `fecha_fin` | DATE | — | Sí | No |
| `formato` | TEXT | — | No | No |
| `numero_selecciones_participantes` | INTEGER | — | No | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.6 `partidos` (Partido — entidad central)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_partido` | TEXT | Clave de negocio | Sí | Sí |
| `torneo_id` | UUID | FK → `torneos.id` | Sí (siempre, incluso amistosos) | No |
| `seleccion_local_id` | UUID | FK → `selecciones.id` | Sí | No |
| `seleccion_visitante_id` | UUID | FK → `selecciones.id` | Sí | No |
| `estadio_id` | UUID | FK → `estadios.id` | No (si aún no asignado) | No |
| `arbitro_id` | UUID | FK → `arbitros.id` | No | No |
| `fecha` | DATE | — | Sí | No |
| `hora_local` | TIME | — | No | No |
| `fase` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `jornada` | INTEGER | — | Solo si `fase = fase_grupos` | No |
| `goles_local` | INTEGER | — | Solo si `estado_partido = finalizado` | No |
| `goles_visitante` | INTEGER | — | Solo si `estado_partido = finalizado` | No |
| `estado_partido` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `asistencia` | INTEGER | — | No | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

**Restricción de negocio:** `seleccion_local_id` ≠ `seleccion_visitante_id` (sección 7).

## 4.7 `estadisticas_partido` (asociativa N:M: Partido × Equipo)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_estadistica_partido` | TEXT | Clave de negocio | Sí | Sí |
| `partido_id` | UUID | FK → `partidos.id` | Sí | Compuesta |
| `seleccion_id` | UUID | FK → `selecciones.id` | Sí | Compuesta |
| `xg` | NUMERIC | — | Sí | No |
| `posesion_pct` | NUMERIC | — | Sí | No |
| `disparos_totales` | INTEGER | — | Sí | No |
| `disparos_al_arco` | INTEGER | — | Sí | No |
| `corners` | INTEGER | — | Sí | No |
| `faltas_cometidas` | INTEGER | — | Sí | No |
| `tarjetas_amarillas` | INTEGER | — | Sí | No |
| `tarjetas_rojas` | INTEGER | — | Sí | No |
| `pases_completados` | INTEGER | — | Sí | No |
| `precision_pases_pct` | NUMERIC | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

**Único compuesto:** (`partido_id`, `seleccion_id`).

## 4.8 `estadios` (Estadio)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_estadio` | TEXT | Clave de negocio | Sí | Sí |
| `nombre` | TEXT | — | Sí | No |
| `ciudad` | TEXT | — | Sí | No |
| `pais` | TEXT | — | Sí | No |
| `capacidad` | INTEGER | — | Sí | No |
| `tipo_superficie` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `altitud_metros` | INTEGER | — | Sí | No |
| `techado` | BOOLEAN | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.9 `arbitros` (Árbitro)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_arbitro` | TEXT | Clave de negocio | Sí | Sí |
| `nombre_completo` | TEXT | — | Sí | No |
| `nacionalidad` | TEXT | — | Sí | No |
| `confederacion_arbitral` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `categoria` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `activo` | BOOLEAN | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.10 `lesiones` (Lesión)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_lesion` | TEXT | Clave de negocio | Sí | Sí |
| `jugador_id` | UUID | FK → `jugadores.id` | Sí | No |
| `tipo_lesion` | TEXT | — | Sí | No |
| `gravedad` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `fecha_inicio` | DATE | — | Sí | No |
| `fecha_estimada_retorno` | DATE | — | No | No |
| `fecha_retorno_real` | DATE | — | Solo si `estado = recuperado` | No |
| `partido_origen_id` | UUID | FK → `partidos.id` | No | No |
| `estado` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `fuente` | TEXT | — | Sí | No |
| `creado_en` / `actualizado_en` | TIMESTAMPTZ | — | Sí | No |

## 4.11 `cuotas` (Cuota)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_cuota` | TEXT | Clave de negocio | Sí | Sí |
| `partido_id` | UUID | FK → `partidos.id` | Sí | Compuesta |
| `casa_apuestas` | TEXT | — | Sí | Compuesta |
| `mercado` | TEXT (`CHECK` ENUM) | — | Sí | Compuesta |
| `seleccion_o_resultado` | TEXT | — | Sí | Compuesta |
| `cuota_decimal` | NUMERIC | — | Sí | No |
| `fecha_captura` | TIMESTAMPTZ | — | Sí | Compuesta |
| `estado_cuota` | TEXT (`CHECK` ENUM) | — | Sí | No |
| `creado_en` | TIMESTAMPTZ | — | Sí | No (tabla inmutable: cada captura es un evento nuevo, nunca se actualiza una fila ya escrita) |

**Único compuesto:** (`partido_id`, `casa_apuestas`, `mercado`, `seleccion_o_resultado`, `fecha_captura`).

## 4.12 `predicciones` (Predicción)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `id_prediccion` | TEXT | Clave de negocio (`id_partido` + timestamp, `docs/25`) | Sí | Sí |
| `partido_id` | UUID | FK → `partidos.id` | Sí | Sí (refleja la cardinalidad 1:1 de `docs/32`) |
| `version_modelo` | TEXT | — | Sí | No |
| `probabilidad_local` | NUMERIC | — | Sí | No |
| `probabilidad_empate` | NUMERIC | — | Sí | No |
| `probabilidad_visitante` | NUMERIC | — | Sí | No |
| `top_marcadores` | JSONB | — | Sí | No |
| `variables_influyentes` | JSONB | — | Sí | No |
| `confianza` | NUMERIC | — | Sí | No |
| `indice_caos` | NUMERIC | — | Sí | No |
| `valor_esperado` | NUMERIC | — | No ("no disponible — sin cuotas registradas") | No |
| `estado_ejecucion` | TEXT (`CHECK` ENUM, `docs/29` §6) | — | Sí | No |
| `creado_en` | TIMESTAMPTZ | — | Sí | No (tabla inmutable: sin `actualizado_en`) |

## 4.13 `resultados` (Resultado)

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `partido_id` | UUID | FK → `partidos.id` | Sí | Sí (cardinalidad 1:1) |
| `goles_local` | INTEGER | — | Sí | No |
| `goles_visitante` | INTEGER | — | Sí | No |
| `fuente` | TEXT | — | Sí | No |
| `fecha_registro` | TIMESTAMPTZ | — | Sí | No |
| `creado_en` | TIMESTAMPTZ | — | Sí | No (tabla inmutable) |

## 4.14 `auditorias` (Auditoría)

*(Aclaración de diseño, desarrollada en "Observaciones": esta tabla registra la comparación **por partido** de una Predicción contra su Resultado — Top1/Top4/error de calibración de esa predicción puntual. Las métricas agregadas de cartera (ROI, Yield, Drawdown, `docs/09`) son series de tiempo calculadas a partir de **muchas** filas de esta tabla, no columnas de una sola fila — no se modela aquí una tabla adicional de agregados, por no existir hoy evidencia de su forma exacta.)*

| Columna | Tipo | Rol | Obligatorio | Único |
|---|---|---|---|---|
| `id` | UUID | PK técnica | Sí | Sí |
| `prediccion_id` | UUID | FK → `predicciones.id` | Sí | Sí (cardinalidad 1:1) |
| `resultado_id` | UUID | FK → `resultados.id` | Sí | Sí (cardinalidad 1:1) |
| `acierto_top1` | BOOLEAN | — | Sí | No |
| `acierto_top4` | BOOLEAN | — | Sí | No |
| `error_calibracion` | NUMERIC | — | No (métrica de V2.0, `docs/09`: "Brier Score") | No |
| `valor_esperado_realizado` | NUMERIC | — | No | No |
| `fecha_auditoria` | TIMESTAMPTZ | — | Sí | No |
| `creado_en` | TIMESTAMPTZ | — | Sí | No (tabla inmutable) |

**Restricción de negocio no expresable como `CHECK` simple entre columnas (anotada, no resuelta aquí):** `prediccion_id` y `resultado_id` deben referirse al mismo `partido_id` — esto requiere validar, al insertar, que `predicciones.partido_id = resultados.partido_id` para el par elegido. Un `CHECK` de PostgreSQL no puede comparar valores de otra tabla directamente; esta regla debe aplicarse en la capa de aplicación o mediante un mecanismo declarativo más avanzado (columna generada, *trigger*) — decisión de implementación física, fuera de esta misión.

## 4.15 `propuestas_aprendizaje` (Propuesta de Aprendizaje — tentativa, sin persistencia confirmada)

Igual que en `docs/31`/`docs/32`, esta tabla **no tiene hoy justificación de creación** — `learning/` nunca escribe en `data/` (`learning/README.md`). Se documenta su forma conceptual únicamente como referencia especulativa, para que una futura decisión no parta de cero:

| Columna (especulativa) | Tipo | Rol |
|---|---|---|
| `id` | UUID | PK técnica |
| `descripcion` | TEXT | — |
| `evidencia` | JSONB | Lista de `auditoria_id` que la respaldan |
| `estado` | TEXT (`CHECK`: pendiente/aprobada/rechazada) | — |
| `fecha_propuesta` | TIMESTAMPTZ | — |

**Esta tabla no se considera parte oficial del modelo físico hasta que exista una decisión explícita** — se excluye de las validaciones obligatorias de la sección "Validaciones" por esta misma razón.

---

# 5. Relaciones físicas

| Relación conceptual (`docs/32`) | Implementación física |
|---|---|
| 1:N (ej. `competiciones` → `torneos`) | Columna `*_id` (FK) en la tabla del lado "N", referenciando `id` (PK) de la tabla del lado "1" |
| 1:1 (`partidos` ↔ `predicciones`, `partidos` ↔ `resultados`, `predicciones`+`resultados` ↔ `auditorias`) | La misma FK simple, con restricción adicional `UNIQUE` sobre la columna FK — es exactamente lo que convierte una relación 1:N en 1:1 en un modelo relacional |
| N:M (`selecciones`×`jugadores`×`torneos`, resuelta por `convocatorias`; `partidos`×`selecciones`, resuelta por `estadisticas_partido`) | La entidad asociativa ya es una tabla de pleno derecho (con su propio `id` técnico y sus propios atributos: `dorsal`, `xg`, etc.) — **no** una tabla puente mínima de solo dos columnas, porque ambas entidades ya tienen atributos propios más allá de la relación |

---

# 6. Índices recomendados

| Índice | Columnas | Por qué | Impacto esperado |
|---|---|---|---|
| Índice de FK (implícito, recomendado explícitamente) | Toda columna `*_id` de las 15 tablas | PostgreSQL **no** indexa automáticamente las columnas FK (a diferencia de la PK) | Acelera *joins* y evita escaneos secuenciales al validar integridad referencial en borrados/actualizaciones del lado "1" |
| Compuesto | `partidos (torneo_id, fecha)` | Consulta más frecuente del pipeline: "partidos de un torneo, en orden cronológico" (`docs/14`, insumo de Variable002) | Evita ordenar en memoria una tabla que crecerá con cada partido nuevo |
| Compuesto | `lesiones (jugador_id, estado)` | Consulta de tiempo real: "lesiones activas de un jugador" (Variable006, en cada predicción) | Acceso directo sin escanear el historial completo de lesiones ya resueltas |
| Compuesto, descendente | `cuotas (partido_id, fecha_captura DESC)` | `engine/06` necesita la cuota **vigente más reciente** de un partido, no todo el historial | Evita ordenar todas las cuotas históricas de un partido en cada predicción |
| Compuesto | `convocatorias (torneo_id, seleccion_id)` | Consulta frecuente: "plantilla convocada de un equipo en un torneo" (Variable006, Variable008) | Acceso directo a la plantilla sin filtrar toda la tabla de convocatorias |
| Único (implícito por `UNIQUE`) | Todas las claves de negocio (`id_seleccion`, `id_partido`, etc.) | PostgreSQL crea automáticamente un índice al declarar `UNIQUE` — no requiere una decisión adicional | Búsquedas por código de negocio (las que usan los reportes, `docs/08`) tan rápidas como por la PK técnica |
| Diferido (no recomendado todavía) | Índice `GIN` sobre `predicciones.top_marcadores`/`variables_influyentes` (`JSONB`) | Solo tendría sentido si se necesitara *consultar dentro* del contenido JSON (ej. "todas las predicciones donde tal variable influyó") | Se documenta como opción futura, no como recomendación actual — no existe hoy evidencia de esa consulta (`CLAUDE.md`: no anticipar sin evidencia) |

---

# 7. Restricciones de integridad

| Tipo | Ejemplos | Regla |
|---|---|---|
| `NOT NULL` | Todo campo marcado "Obligatorio: Sí" en la sección 4 | Ningún dato de Nivel A/obligatorio puede faltar sin detener el pipeline (`docs/15`/`docs/16`, ya vigente; aquí se hace cumplir también a nivel físico) |
| `UNIQUE` | Claves de negocio; combinaciones ya documentadas (`torneo_id`+`seleccion_id`+`jugador_id` en convocatorias; `partido_id`+`seleccion_id` en estadísticas) | Mismas restricciones ya fijadas en `data/processed/selecciones-nacionales/README.md`, ahora expresadas como restricción física, no solo como regla documental |
| `CHECK` (rango) | `ranking_fifa_actual > 0`; `0 ≤ posesion_pct ≤ 100`; `cuota_decimal > 1.00`; `disparos_al_arco ≤ disparos_totales` | Hace cumplir a nivel de motor los rangos ya documentados — un valor inválido nunca llega a insertarse, en vez de detectarse solo en `VariablePreparation` |
| `CHECK` (negocio) | `seleccion_local_id ≠ seleccion_visitante_id` (`partidos`) | Regla de negocio ya vigente (`data/processed/selecciones-nacionales/README.md`), promovida a restricción física |
| **No expresable como `CHECK` simple** | Suma de `probabilidad_local + probabilidad_empate + probabilidad_visitante ≈ 1`; que `auditorias.prediccion_id` y `resultado_id` compartan el mismo `partido_id` | Ambas involucran más de una fila/columna con posible margen de redondeo — se recomienda validarlas en la capa de aplicación (`VariablePreparation`/`PredictionAssembler`, `docs/29`), no forzarlas como `CHECK` físico que podría rechazar una fila válida por un redondeo de centésimas |
| **Integridad referencial** | Toda columna `*_id` referencia una fila existente de su tabla padre | Comportamiento ante eliminación: **nunca** borrado en cascada de historial — ninguna entidad de este modelo permite eliminar información de la que dependan `predicciones`, `resultados` o `auditorias` (`docs/05`: "nunca eliminar historial") |
| **Índice único parcial** (recomendación, PostgreSQL-específica) | `jugadores`, condición `activo_seleccion = true`, único por jugador | Implementa físicamente la regla ya documentada "un jugador solo puede tener una `id_seleccion` activa a la vez" sin necesitar una columna adicional — PostgreSQL permite un índice único que solo aplica a las filas que cumplen una condición |

---

# 8. Estrategia de identificadores

**Decisión: UUID como clave técnica física (`id`) en las 15 tablas, preservando el identificador de negocio ya existente (`id_seleccion`, `id_partido`, etc.) como columna `UNIQUE` independiente — nunca como la PK física.**

## Análisis de alternativas

| Opción | Rendimiento | Escalabilidad | Trazabilidad | Simplicidad | Futura sincronización |
|---|---|---|---|---|---|
| **BIGSERIAL** | El mejor de las tres en un único nodo (entero de 8 bytes, secuencial, óptimo para índices B-tree) | Limitada: una secuencia es propia de una única base de datos — fusionar datos de dos entornos (desarrollo/producción, o una futura arquitectura distribuida) produce colisiones de identificador | Revela involuntariamente el volumen/ritmo de crecimiento del sistema (un identificador secuencial expone cuántas filas existen) — sensible para un modelo con valor comercial declarado (`README.md`/`LICENSE`) | La más simple de las tres | Nula sin coordinación explícita de rangos entre entornos |
| **UUID (v4, aleatorio)** | Peor que `BIGSERIAL`: al ser aleatorio, cada inserción cae en una posición impredecible del índice B-tree, causando fragmentación y más E/S de la necesaria | Alta: generable en cualquier nodo sin coordinación central | Buena: no revela volumen ni orden de creación | Ligeramente más compleja que `BIGSERIAL` (16 bytes vs. 8) | Excelente: es, precisamente, el caso de uso para el que UUID fue diseñado |
| **UUID v7 (ordenado temporalmente, RFC 9562)** | Mitiga la debilidad de UUIDv4: al incluir un componente temporal ordenado, las inserciones son mayormente secuenciales en el índice, acercándose al comportamiento de `BIGSERIAL` sin perder sus beneficios distribuidos | Alta, igual que UUIDv4 | Buena, y además el propio identificador codifica su momento aproximado de creación (beneficio adicional de trazabilidad) | Comparable a UUIDv4 | Excelente, igual que UUIDv4 |
| **ULID** | Objetivo equivalente a UUIDv7 (ordenable, 128 bits) | Alta, en teoría | Buena | **Sin tipo nativo en PostgreSQL** — requeriría almacenarse como `TEXT`/`BYTEA` con conversión manual, o mapearse a `UUID` con una codificación adicional | Igual que UUIDv7, sin ninguna ventaja adicional que compense la falta de tipo nativo |

## Justificación de la elección

1. **Trazabilidad y continuidad documental:** el identificador de negocio ya usado en quince documentos previos (`id_seleccion`, `id_partido`, etc.) se conserva intacto como columna `UNIQUE` — ningún reporte, prompt o documento existente necesita cambiar su vocabulario.
2. **Futura sincronización, ya anticipada por el proyecto:** `docs/05-Base-de-Conocimiento.md` ("Evolución") y `docs/15-Capa-de-Preparacion-de-Variables.md` (§9) ya proyectan explícitamente una futura migración hacia "bases de datos distribuidas" y "múltiples proveedores de datos" — evidencia documental real, no una hipótesis nueva de esta misión (`CLAUDE.md`: ningún dato/decisión "por si acaso"). Un identificador generado localmente (UUID) es la única opción de las tres que no requiere coordinación central para fusionar datos de distintos orígenes o entornos.
3. **Rendimiento, mitigado, no ignorado:** se reconoce explícitamente la debilidad de rendimiento de un UUID aleatorio puro (fragmentación de índice). Se recomienda **UUIDv7** —o, si el motor/librería de la implementación futura todavía no lo soporta nativamente, UUIDv4 como alternativa aceptada temporalmente— precisamente para mitigar esa debilidad sin renunciar a los beneficios de generación distribuida.
4. **ULID descartado, no por su diseño, sino por su ausencia de tipo nativo en PostgreSQL:** exigiría una conversión o un tipo de columna no nativo (`TEXT`/`BYTEA`) sin aportar ninguna ventaja que UUIDv7 no ofrezca ya de forma nativa en el motor elegido para esta misión.
5. **Simplicidad, priorizada explícitamente en segundo lugar:** se reconoce que `BIGSERIAL` sería más simple y de mejor rendimiento puro en un solo nodo — pero esta misión prioriza la trazabilidad y la sincronización futura ya evidenciadas en `docs/05`/`docs/15`, en línea con el principio de "Desarrollo Incremental" (diseñar para lo que el proyecto ya proyecta, no evitar toda complejidad a cualquier costo).

---

# 9. Compatibilidad

*(Sección reconciliada por `GR-008` con el stack oficial de `docs/34-Decision-Oficial-del-Stack-Tecnologico.md`, `ARCH-000`: Python + FastAPI + SQLAlchemy 2.x + Alembic. La versión original de esta sección, redactada en términos de Java/Spring Boot/Hibernate/JPA/Flyway/Liquibase, se documenta como nota histórica al final de esta sección — no se elimina en silencio.)*

| Herramienta oficial (`ARCH-000`) | Cómo la habilita este modelo (sin diseñarla) |
|---|---|
| **Alembic** | El orden de migración debe seguir exactamente el grafo de dependencias acíclico ya fijado en `docs/32` §6: `competiciones` → `torneos` → (`selecciones`, `estadios`, `arbitros`, en paralelo, sin dependencia entre sí) → `jugadores` → `partidos` → (`convocatorias`, `estadisticas_partido`, `lesiones`, `cuotas`, `predicciones`, `resultados`) → `auditorias`. Cada tabla de la sección 4 es, en la práctica, una migración candidata individual |
| **SQLAlchemy 2.x** | La columna `id` uniforme (`UUID`) en las 15 tablas coincide con el patrón `Mapped[UUID]`/`mapped_column` de una clase base declarativa común que cualquier modelo SQLAlchemy podría heredar — evita repetir la declaración de clave primaria en cada clase. El nombre de tabla en plural (sección 2) se declara directamente en el atributo `__tablename__` de cada modelo — sin fricción, a diferencia de la anotación adicional que exigiría un ORM con convención singular por defecto |
| **SQLAlchemy — nombrado de columnas** | Los nombres de columna en `snake_case` (sección 2) son ya el formato nativo de SQLAlchemy — no se necesita ninguna traducción ni estrategia de nombrado adicional, a diferencia de un ORM que parta de una convención `camelCase` |
| **SQLAlchemy — generación de UUID** | SQLAlchemy 2.x soporta el tipo `UUID` nativo de PostgreSQL (`sqlalchemy.dialects.postgresql.UUID`) y la generación de valores por defecto en Python (ej. `default=uuid.uuid4` o una función equivalente para UUIDv7) sin requerir una librería externa adicional — compatible directamente con la decisión de la sección 8 |

**Nota histórica (preservada, no eliminada):** la versión original de esta sección (`DATA-005`) recomendaba Flyway/Liquibase, Spring Data JPA y Hibernate, bajo el supuesto no mandatado de un stack Java/Spring Boot. Esa asunción quedó formalmente descartada por `docs/34` (`ARCH-000`), que congeló Python como lenguaje oficial. Se conserva esta nota, en lugar de borrar la referencia en silencio, porque documenta una decisión real que existió durante una etapa del proyecto (Constitución, Art. 8).

---

# Restricciones (confirmación de cumplimiento)

Este documento no genera `CREATE TABLE`, `ALTER TABLE`, SQL, código Python, modelos SQLAlchemy, repositorios ni migraciones — toda referencia a un mecanismo físico (índices, `CHECK`, `UNIQUE`) se describe en términos conceptuales, nunca como sintaxis ejecutable. No se modifica ninguna Variable Oficial, el Runtime, el `PredictionContext`, ningún motor ni ningún modelo matemático de `models/`.

---

# Validaciones obligatorias

- **¿Todas las entidades tienen representación física?** Sí, las 14 entidades activas de `docs/32` (todas salvo Propuesta de Aprendizaje, sección 4.15, explícitamente marcada como no oficial todavía por carecer de justificación de persistencia).
- **¿Todas las relaciones pueden implementarse?** Sí — las 1:N mediante FK simple, las 1:1 mediante FK con `UNIQUE`, y las dos únicas N:M del modelo mediante sus propias entidades asociativas ya existentes (`convocatorias`, `estadisticas_partido`), sin necesitar ninguna tabla puente adicional.
- **¿No existen dependencias circulares?** Confirmado — se hereda directamente el grafo acíclico ya verificado en `docs/32` §6; ninguna FK de este documento introduce una referencia nueva que cierre un ciclo.
- **¿PostgreSQL puede implementar el modelo completo?** Sí — ningún tipo, restricción o índice recomendado excede las capacidades de PostgreSQL (`UUID`, `JSONB`, `TIMESTAMPTZ`, `CHECK`, índices parciales y compuestos son todas características nativas y estables del motor).
- **¿El diseño es compatible con FastAPI/SQLAlchemy (stack oficial, `docs/34`)?** Sí, sin ninguna fricción: el nombrado de tabla en plural se declara directamente en `__tablename__`, y `snake_case` es ya la convención nativa de SQLAlchemy — a diferencia de la fricción menor que sí existía frente a un ORM de convención Java (ver sección 9, nota histórica).

---

# Cierre obligatorio

**1. ¿Qué problema arquitectónico resuelve este documento?**
La ausencia de una traducción concreta del Modelo Relacional Conceptual (`docs/32`) a decisiones físicas reales de un motor relacional específico — sin esta traducción, cualquier implementación futura tendría que tomar por su cuenta decisiones de tipo, identificador e índice sin una referencia única y ya razonada.

**2. ¿Qué convenciones oficiales quedaron definidas?**
Las diez de la sección 2: `snake_case`, tablas en plural, `id` uniforme como PK técnica, claves de negocio preservadas como `UNIQUE`, convención de nombre de FK, timestamps diferenciados por mutabilidad, ausencia deliberada de auditoría de "quién" y de versionado optimista, y `TEXT`+`CHECK` en vez de `ENUM` nativo.

**3. ¿Qué estrategia de identificadores fue elegida y por qué?**
UUID (preferentemente UUIDv7) como clave técnica, manteniendo el identificador de negocio ya existente como columna única — justificado por trazabilidad, por la sincronización futura ya proyectada en `docs/05`/`docs/15`, y por una mitigación explícita de la debilidad de rendimiento de un UUID puramente aleatorio (sección 8).

**4. ¿Qué entidades presentan mayor complejidad?**
`partidos` (la entidad central, con dos relaciones distintas hacia `selecciones` en roles diferentes, más dos relaciones opcionales) y `auditorias` (la única entidad cuya integridad de negocio —que ambas FK compartan el mismo partido— no puede expresarse como una restricción física simple, sección 4.14).

**5. ¿Qué índices serán críticos?**
Los de la sección 6 sobre columnas de alta frecuencia de consulta en tiempo de predicción: `partidos (torneo_id, fecha)`, `lesiones (jugador_id, estado)` y `cuotas (partido_id, fecha_captura DESC)` — los tres corresponden a variables que se recalculan en cada predicción (Rendimiento en el Torneo, Disponibilidad de Plantilla, Valor Esperado).

**6. ¿Qué restricciones aportan mayor seguridad?**
El índice único parcial sobre `jugadores.activo_seleccion` (hace física una regla que hasta ahora solo era documental) y la ausencia deliberada de `actualizado_en` en las tablas inmutables (`predicciones`, `resultados`, `auditorias`, `cuotas`), que hace visible el principio de inmutabilidad en el propio esquema, no solo en la documentación.

**7. ¿Qué parte continúa pendiente?**
Tres cosas: (a) la precisión/escala exacta de cada columna `NUMERIC` (diferida a la migración física real); (b) la decisión sobre si `propuestas_aprendizaje` merece existir físicamente; (c) los mismos datos de categoría D ya identificados por `docs/27`, que dejarían columnas del esquema sin ningún valor real que cargar.

**8. ¿Qué misión recomendarías después?**
*(Respondida en su momento por `DATA-005`; resuelta desde entonces por `docs/34`, `ARCH-000`, y sincronizada en este texto por `GR-008` — se conserva la pregunta y se actualiza la respuesta, no se elimina.)* Formalizar la elección de stack — tarea ya cumplida por `ARCH-000` (Python + FastAPI + SQLAlchemy + Alembic + PostgreSQL). La recomendación vigente, heredada de esa misión, es priorizar la primera fórmula matemática real en `models/poisson.md`.

**9. ¿El modelo físico puede considerarse estabilizado?**
A nivel de **tablas, tipos conceptuales, relaciones e identificadores**, sí — las 14 tablas activas cubren la totalidad de las entidades ya validadas en `docs/32`, sin ciclos ni ambigüedad de tipo. A nivel de **contenido real**, no — el estado de los datos sigue siendo el mismo que `docs/31` ya describió.

**10. ¿El proyecto ya está listo para comenzar la arquitectura de aplicación en el stack oficial (Python/FastAPI/SQLAlchemy, `docs/34`)?**
*(Pregunta actualizada por `GR-008` — la versión original de `DATA-005` preguntaba por "arquitectura Java", stack ya descartado por `ARCH-000`.)* El modelo de datos, sí — este documento es suficiente para que una implementación en SQLAlchemy comience a definir sus modelos declarativos sin ambigüedad. El proyecto en su conjunto, no todavía: sigue pendiente, como en cada cierre anterior de la serie `DEV-`, al menos una fórmula matemática real en `models/` — sin ella, la arquitectura de aplicación tendría un esquema de datos completo pero ningún cálculo real que ejecutar sobre él.

---

# Observaciones

*(Hallazgos detectados durante el análisis, registrados sin corregirse — Manual Operativo, `docs/22`, sección 7.)*

1. **El stack Java + Spring Boot + PostgreSQL se estaba asumiendo de facto, sin una misión que lo declarara formalmente.** *(Hallazgo original de `DATA-005`.)* Esta misión (y su brief) daba por sentado Flyway/Liquibase/Spring Data JPA/Hibernate como el ecosistema de implementación futura — información nueva y relevante que ninguna misión `DEV-`/`GOV-` anterior había fijado (`docs/26`/`docs/29` afirman explícitamente que la elección de stack está fuera de su alcance). **Resuelto:** `docs/34-Decision-Oficial-del-Stack-Tecnologico.md` (`ARCH-000`) formalizó el stack oficial (Python + FastAPI + SQLAlchemy + Alembic + PostgreSQL), y `GR-008` sincronizó el texto de este documento (secciones 2, 9, "Restricciones", "Validaciones", "Cierre") con esa decisión — ver "Nota de reconciliación (GR-008)" al inicio del documento.
2. **Clarificación de diseño sobre `auditorias` vs. métricas de cartera (ROI/Yield/Drawdown).** Ningún documento anterior distinguía explícitamente entre la comparación *por partido* (Top1/Top4/error de calibración — lo que esta misión modela como la tabla `auditorias`) y las métricas *agregadas en el tiempo* de `docs/09-Auditoria.md` (ROI, Yield, Drawdown), que son series calculadas sobre muchas filas de `auditorias`, no atributos de una fila individual. Esta distinción, necesaria para diseñar la tabla física, no existía antes de esta misión — se deja documentada aquí, sin proponer todavía la tabla de agregados correspondiente (fuera de alcance: no hay evidencia suficiente de su forma exacta).

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Que UUIDv7 estará disponible o será razonablemente adoptable en el momento de la implementación real — es un estándar reciente (RFC 9562, 2024); si la implementación ocurre sobre una versión de PostgreSQL o una librería que todavía no lo soporte de forma nativa y cómoda, la recomendación real terminaría siendo UUIDv4 puro, con la debilidad de rendimiento ya reconocida en la sección 8.
- **¿Qué parte de este entregable podría estar equivocada?** La recomendación de `TEXT` + `CHECK` en vez de `ENUM` nativo de PostgreSQL es una buena práctica ampliamente aceptada, pero no universal — algunos equipos prefieren el `ENUM` nativo precisamente por la validación más estricta a nivel de tipo. Se documentó la razón de la elección (facilidad de migración aditiva) para que sea revisable, no como un hecho incuestionable.
- **¿Qué información me habría hecho falta para tener más certeza?** Un volumen estimado real de datos (cuántos partidos/predicciones/cuotas se esperan por temporada) habría permitido justificar con más precisión si la diferencia de rendimiento entre `NUMERIC` y `DOUBLE PRECISION`, o entre UUID y `BIGSERIAL`, es realmente despreciable a la escala que el proyecto alcanzará — hoy esa estimación no existe en ningún documento.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que, al escribir la primera migración real (Alembic, `docs/34`), el índice único parcial propuesto para `jugadores.activo_seleccion` efectivamente se comporte como se espera con datos reales poblados — hoy no hay ninguna fila real que lo confirme empíricamente.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí, ya señalada: `BIGSERIAL` con una tabla de mapeo explícita entre entornos (en vez de UUID) sería una alternativa razonable si una futura misión determinara que la sincronización distribuida no es, en realidad, una prioridad cercana del roadmap — se eligió UUID por la evidencia ya documental de `docs/05`/`docs/15`, no por preferencia sin respaldo.

---

# Fuera de alcance de esta misión

- No se genera `CREATE TABLE`, `ALTER TABLE`, SQL, código Python, modelos SQLAlchemy, repositorios ni migraciones.
- No se diseña ninguna migración concreta de Alembic (herramienta ya elegida oficialmente por `ARCH-000`, no rediseñada aquí).
- No se modifican las Variables Oficiales, el Runtime, el `PredictionContext`, los motores ni ningún modelo matemático de `models/`.
- No se decide la precisión/escala exacta de ningún campo `NUMERIC` — se difiere a la migración física real.
- La elección de stack ya fue formalizada por `docs/34` (`ARCH-000`) y sincronizada en este documento por `GR-008` — ver "Nota de reconciliación (GR-008)".

---

Fin del documento.
