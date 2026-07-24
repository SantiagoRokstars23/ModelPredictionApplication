# Estrategia Oficial para la Población de la Base de Conocimiento

**Archivo:** `docs/37-Estrategia-Poblacion-Base-Conocimiento.md`

**Misión:** MS-011 — Estrategia Oficial para la Población de la Base de Conocimiento (el brief de esta misión la identificaba como "MS-007"; ver "Hallazgo de numeración" más abajo)

**Versión:** 1.0.0

**Estado:** Investigación documental — sin código, sin motores modificados, sin CSV poblados

---

## Nota de origen y hallazgo de numeración (`docs/22`, sección 7 — Gestión de hallazgos)

El brief de esta misión la identifica como **"MS-007"**. Verificado contra `docs/00-Project-Tracker.md` antes de escribir (Lista de verificación previa, `docs/22` sección 3): **`MS-007` ya está asignado** a "Prediction Pipeline" (línea 222 del Tracker, el mismo trabajo documentado en `docs/14-Prediction-Pipeline.md`) — una misión completamente distinta, ya completada. El último identificador real de la serie `MS-` es `MS-010` ("Matriz Oficial de Consumo de Variables del Engine").

**Resolución, sin ocultar la inconsistencia (`docs/22` §9: "nunca oculta una inconsistencia detectada"):** esta misión se registra como **`MS-011`** — el siguiente identificador disponible de la serie, no reutilizado. No es la primera vez que un brief reutiliza un identificador ya asignado (`CLAUDE.md`, "Nota práctica": "`MR-002` dos veces, `MR-005`, `GOV-001`"), pero registrar dos entradas distintas bajo el mismo rótulo `MS-007` en `docs/00-Project-Tracker.md` introduciría una ambigüedad real y evitable (dos temas sin ninguna relación, uno sobre el pipeline de predicción y otro sobre estrategia de datos) — a diferencia de los duplicados previos, que el proyecto ha tolerado sin corregir, aquí existe un identificador libre inmediato (`MS-011`) que resuelve el problema sin ningún costo. **Esto no cambia la prioridad del roadmap** (`docs/22` §7, punto 3) — es una corrección de rótulo, no una reclasificación de trabajo.

El resto de este documento se refiere a sí mismo como `MS-011`. El nombre de archivo (`docs/37-Estrategia-Poblacion-Base-Conocimiento.md`) es el que exige el brief y no colisiona con ningún documento existente (el último es `docs/36`).

---

# 1. Objetivo

Definir la hoja de ruta oficial para poblar `data/processed/selecciones-nacionales/` con datos reales: en qué orden, con qué fuentes, con qué volumen mínimo, bajo qué criterios de validación, y con qué estrategia de versionado — sin escribir código, sin modificar motores, variables ni fórmulas, y sin poblar ningún CSV en esta misma misión.

---

# 2. Metodología

Se releyó, verificando contra el estado real del repositorio (no de memoria, `docs/22` §3, "Cambios recientes"):

- `data/processed/selecciones-nacionales/*.csv` — conteo real de filas por archivo (sección 3).
- `data/processed/selecciones-nacionales/README.md` — las 11 entidades, sus columnas, sus claves foráneas y restricciones ya declaradas (Misión 001/MS-002/MS-006).
- `data/processed/README.md` — reglas generales del directorio `processed/`.
- `docs/05-Base-de-Conocimiento.md` — filosofía, flujo de datos, validación, versionado y Principio de Justificación de Datos ya vigentes (no redefinidos aquí).
- `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) — veredicto de disponibilidad por variable, ya resuelto para Variable006/007/008/009.
- `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) — clasificación A-E de cada dato necesario de las 12 Variables Oficiales, insumo directo de la sección 6 (MVP).
- `docs/32-Modelo-Relacional-Oficial.md` §6 / `docs/33-Modelo-Fisico-PostgreSQL.md` (sección "Alembic") — el grafo de dependencias FK ya fijado oficialmente.
- `app/persistence/mu_gol_provider.py` (`BUILD-016`) — `MINIMO_PARTIDOS_HISTORICOS = 10`, la única cifra numérica ya congelada en código que condiciona el volumen mínimo de `partidos.csv`.
- `app/engine/engine01.py`/`engine02.py` (`BUILD-009`/`BUILD-010`) — confirmación de que Variable003/004 (Nivel A) son las únicas que detienen el pipeline si faltan; el resto de variables activas son opcionales (`docs/17`).

---

# 3. Estado real verificado de `data/processed/selecciones-nacionales/`

| Archivo | Filas de datos (sin encabezado) | Estado |
|---|---|---|
| `selecciones.csv` | 40 | Real (Top 40 FIFA, MS-002) |
| `competiciones.csv` | 11 | Real (catálogo `Amistosos Internacionales` + 10 competiciones, MS-006) |
| `torneos.csv` | 1 | Solo el contenedor `TOR-2026-AMISTOSOS` — ninguna edición específica con fechas/sedes reales para las 10 competiciones de `MS-006` |
| `jugadores.csv` | 0 | Solo encabezado |
| `convocatorias.csv` | 0 | Solo encabezado |
| `partidos.csv` | 0 | Solo encabezado |
| `estadisticas_partido.csv` | 0 | Solo encabezado |
| `lesiones.csv` | 0 | Solo encabezado |
| `cuotas.csv` | 0 | Solo encabezado |
| `arbitros.csv` | 0 | Solo encabezado |
| `estadios.csv` | 0 | Solo encabezado |

`data/raw/` no contiene ningún archivo de datos (solo `README.md`, ya confirmado por `docs/27`) — ningún dato "falta en `processed/` pero existe en `raw/`"; si no está en `processed/`, no existe en ningún lado del repositorio hoy.

---

# 4. Grafo oficial de dependencias entre entidades

**Fuente de autoridad, no redefinida aquí:** `docs/32-Modelo-Relacional-Oficial.md` §6, citado literalmente por `docs/33-Modelo-Fisico-PostgreSQL.md` (sección "Alembic"):

> `competiciones → torneos → (selecciones, estadios, arbitros, en paralelo, sin dependencia entre sí) → jugadores → partidos → (convocatorias, estadisticas_partido, lesiones, cuotas, predicciones, resultados) → auditorias`

Verificado, campo por campo, contra las claves foráneas ya declaradas en `data/processed/selecciones-nacionales/README.md` (sección "Entidades") — **coincide exactamente**, sin ninguna contradicción:

```
competiciones.csv  (sin FK)
        │
        ▼
torneos.csv  (FK → competiciones)
        │
        ├────────────────┬──────────────────┐
        ▼                ▼                  ▼
selecciones.csv     estadios.csv       arbitros.csv
(sin FK)            (sin FK)           (sin FK)
        │
        ▼
jugadores.csv  (FK → selecciones)
        │
        ├───────────────────────────────┐
        ▼                               ▼
partidos.csv                      convocatorias.csv
(FK → torneos, selecciones×2,     (FK → torneos, selecciones,
 estadios, arbitros)                jugadores)
        │
        ├───────────────┬───────────────┐
        ▼               ▼               ▼
estadisticas_partido   lesiones.csv    cuotas.csv
.csv (FK → partidos,   (FK → jugadores; (FK → partidos)
 selecciones)           partidos opcional)
```

**Hallazgo, no una contradicción — matiz sobre el grafo ya oficial:** `selecciones.csv`, `estadios.csv` y `arbitros.csv` no tienen, en realidad, ninguna clave foránea hacia `competiciones`/`torneos` — el grafo de `docs/32`/`docs/33` los agrupa "después de torneos" por conveniencia de lectura del diagrama, no porque exista una dependencia real. En la práctica ya verificada del propio proyecto, `selecciones.csv` se pobló (`MS-002`) **antes** de que existiera ninguna fila de `torneos.csv` con fecha real — confirma que estas tres entidades son, genuinamente, de **Nivel 0** (paralelas a `competiciones`, no posteriores a `torneos`). Esta misión no corrige `docs/32`/`docs/33` (fuera de alcance: "no modificar documentos existentes"); solo documenta que el orden de población recomendado (sección 5) puede paralelizar estas tres entidades desde el primer día, sin esperar a `torneos.csv`.

---

# 5. Orden oficial recomendado para poblar los CSV

Basado en el grafo de la sección 4, con el matiz ya señalado (Nivel 0 ampliado):

| Nivel | Entidades | Depende de | Puede empezar |
|---|---|---|---|
| **0** | `competiciones.csv`, `selecciones.csv`, `estadios.csv`, `arbitros.csv` | Nada | Inmediatamente, en paralelo (dos de las cuatro ya están pobladas: `competiciones`/`selecciones`) |
| **1** | `torneos.csv` (ediciones específicas, no solo el contenedor de amistosos) | `competiciones.csv` | En cuanto `competiciones.csv` exista (ya existe) |
| **1** | `jugadores.csv` | `selecciones.csv` | En cuanto `selecciones.csv` exista (ya existe) |
| **2** | `partidos.csv` | `torneos.csv`, `selecciones.csv`, `estadios.csv`, `arbitros.csv` | Requiere que **las cuatro** entidades de Nivel 0/1 relevantes existan primero |
| **2** | `convocatorias.csv` | `torneos.csv`, `selecciones.csv`, `jugadores.csv` | Requiere `torneos.csv` + `jugadores.csv` |
| **3** | `estadisticas_partido.csv` | `partidos.csv`, `selecciones.csv` | Requiere `partidos.csv` ya poblado (mismos partidos exactos) |
| **3** | `lesiones.csv` | `jugadores.csv` (`partidos.csv` opcional, solo para `id_partido_origen`) | Requiere `jugadores.csv`; no bloqueada por `partidos.csv` |
| **3** | `cuotas.csv` | `partidos.csv` | Requiere `partidos.csv` ya poblado |

**Respuesta directa a "¿qué archivos pueden poblarse inmediatamente?":** `estadios.csv` y `arbitros.csv` — cero dependencias, cero filas hoy, sin ningún bloqueo. `torneos.csv` (ediciones reales) también puede empezar ya (`competiciones.csv` ya existe). `jugadores.csv` también puede empezar ya (`selecciones.csv` ya existe).

**Respuesta directa a "¿qué archivos requieren que otros existan previamente?":** `partidos.csv` (requiere las cuatro entidades de Nivel 0/1 relevantes), `convocatorias.csv` (requiere `torneos`+`jugadores`), `estadisticas_partido.csv`/`cuotas.csv` (requieren `partidos.csv`, con los **mismos** `id_partido` exactos), `lesiones.csv` (requiere `jugadores.csv`).

---

# 6. Conjunto Mínimo Viable (MVP) para una primera predicción completa

**Punto de partida verificado en código, no supuesto:** `Engine01`/`Engine02` (`BUILD-009`/`BUILD-010`) detienen el pipeline completo (`VariableObligatoriaNoDisponible`) si Variable003 (Potencial Ofensivo) o Variable004 (Solidez Defensiva) — ambas **Nivel A** — no están disponibles para cualquiera de los dos equipos. Ninguna otra Variable Oficial activa detiene el pipeline (`docs/17`: Variable001/002/006/007/008/010 son opcionales; Variable009 está bloqueada por esquema, no por dato). Esto significa que el MVP real, medido por "qué hace falta para que el Engine complete sus 4 capas sin detenerse", es **más pequeño** de lo que las 11 entidades del módulo podrían sugerir.

**MVP estricto (produce, como mínimo, el estado "Completa sin Valor Esperado", `docs/29` §6):**

| Entidad | Volumen mínimo | Por qué |
|---|---|---|
| `selecciones.csv` | 2 filas (los dos equipos del partido) | Ya cumplido (40 filas reales) |
| `competiciones.csv` + `torneos.csv` | 1 competición + 1 torneo/edición con fechas reales | Ya cumplido para `competiciones`; falta una edición real de `torneos` (hoy solo existe el contenedor de amistosos) |
| `estadios.csv` | 1 fila (la sede del partido a predecir) — o más, si los partidos históricos usados para las ventanas de Variable003/004 se jugaron en sedes distintas | FK obligatoria de `partidos.csv` |
| `arbitros.csv` | 1 fila por partido histórico + el del partido a predecir (o el mismo árbitro repetido) | FK obligatoria de `partidos.csv` |
| `partidos.csv` | **Mínimo 10 partidos finalizados por competición**, por equipo, más el partido a predecir | `MINIMO_PARTIDOS_HISTORICOS = 10` (`app/persistence/mu_gol_provider.py`, `BUILD-016`) es la única cifra ya congelada en código — necesaria para que `HistoricalMuGolProvider` resuelva `μ_gol` y `Engine03` no falle con `MuGolNoDisponible`. El mismo volumen (`N=10`) ya es, además, la ventana que usan Variable003/004 (`MODEL-009`/`MODEL-010`) |
| `estadisticas_partido.csv` | Una fila por equipo, por cada uno de esos mismos partidos (mínimo 20 filas: 10 partidos × 2 equipos) | Fuente directa de `xg`/`disparos_totales`/`disparos_al_arco` — sin esto, Variable003/004 nunca están disponibles y el pipeline se detiene siempre en Capa 1 |

**No forman parte del MVP estricto** (opcionales, no detienen el pipeline si faltan): `jugadores.csv`, `convocatorias.csv`, `lesiones.csv` (Variable006/007/008, todas Nivel B/C, tratadas como ajustes contextuales, `docs/17`), `cuotas.csv` (Engine06 es condicional — su ausencia produce "Completa sin Valor Esperado", no un fallo).

**Respuesta directa a "¿qué volumen mínimo de datos necesita cada CSV?":** ver tabla anterior — el número concreto y ya verificado en código es `N=10` partidos históricos por competición (no un supuesto de esta misión).

---

# 7. Fuentes oficiales aceptables por entidad

`docs/05-Base-de-Conocimiento.md` ya autoriza, en términos generales: "APIs deportivas, sitios oficiales de competiciones, estadísticas públicas, bases de datos deportivas, archivos CSV, entrada manual validada" — "toda fuente deberá ser identificable y verificable." Esta sección especializa esa regla general por entidad, basándose en las fuentes ya citadas y aceptadas en misiones previas (`MS-002`, `MS-006`).

| Entidad | Fuente recomendada | Precedente ya usado |
|---|---|---|
| `selecciones.csv` | Ranking FIFA oficial (fifa.com) + sitio oficial de cada federación | `MS-002` ("Top 40 FIFA") |
| `competiciones.csv` / `torneos.csv` | Sitio oficial de la confederación organizadora (FIFA, UEFA, CONMEBOL, CAF, AFC, CONCACAF, OFC) | `MS-006` (Wikipedia como fuente secundaria de verificación, UEFA.com/CAF Online/AFC/CONCACAF/CONMEBOL como fuentes primarias) |
| `estadios.csv` | Sitio oficial del estadio o de la federación local; bases de datos de estadios ampliamente verificadas (ej. worldstadiums.com) para capacidad/altitud | Ninguno todavía — primera vez que se puebla |
| `arbitros.csv` | Listas oficiales de árbitros FIFA/confederación ("FIFA International Referees List") | Ninguno todavía |
| `jugadores.csv` | Sitio oficial de la federación (convocatoria/plantilla publicada oficialmente) | Ninguno todavía |
| `convocatorias.csv` | Comunicado oficial de convocatoria de la federación, para el torneo específico | Ninguno todavía |
| `partidos.csv` | Sitio oficial de la competición/confederación (resultados oficiales); RSSSF como fuente secundaria de verificación histórica, ampliamente reconocida en estadística de fútbol | Ninguno todavía |
| `estadisticas_partido.csv` | Reportes oficiales de partido de la competición (cuando incluyen `xg`/disparos); proveedores especializados (Opta, StatsBomb, FBref) — **riesgo identificado en sección 9**: `xg` en particular no siempre está disponible en fuentes oficiales gratuitas | Ninguno todavía |
| `lesiones.csv` | Comunicado médico oficial de la federación/club; nunca una fuente sin verificación explícita | **Restricción ya fijada explícitamente en `MODEL-015`: "No usar Transfermarkt"** — se hereda aquí como regla, no se reabre |
| `cuotas.csv` | Casa de apuestas licenciada, con `fecha_captura` explícita | Ninguno todavía; fuera del MVP (sección 6) |

**Hallazgo explícito:** `MODEL-015` (Variable006/Disponibilidad) ya prohibió expresamente usar Transfermarkt como fuente para lesiones — esta misión no reabre esa decisión, solo la hereda y la generaliza como regla de la Base de Conocimiento: cualquier agregador no oficial (scraping de un sitio de terceros sin verificación) queda desaconsejado para toda entidad, no solo para `lesiones.csv`, por el mismo principio ya vigente en `docs/05` ("toda fuente deberá ser identificable y verificable").

---

# 8. Criterios de validación antes de incorporar datos a `processed/`

Síntesis, sin redefinir, de tres fuentes ya vigentes: la validación genérica de `docs/05` (sección "Validación"), las restricciones ya declaradas por entidad en el README del módulo, y la integridad referencial ya fijada por el esquema:

1. **Integridad referencial** — todo campo `FK →` debe resolver contra una fila ya existente en la entidad referenciada (sección 4). Ninguna fila se incorpora con una FK huérfana.
2. **Formato y tipo** — fechas en `YYYY-MM-DD` (`docs/05`), porcentajes `0-100`, probabilidades `0.00-1.00`; cada campo `ENUM` debe usar un valor ya formalizado (ver hallazgo de la sección 9 sobre ENUM sin formalizar).
3. **Duplicados** — claves únicas ya declaradas por entidad (ej. `(id_torneo, id_seleccion, id_jugador)` en `convocatorias.csv`; `(id_partido, id_seleccion)` en `estadisticas_partido.csv`) deben verificarse antes de insertar.
4. **Restricciones propias de cada entidad** — ya declaradas en el README del módulo (ej. `disparos_al_arco ≤ disparos_totales`; `fecha_estimada_retorno ≥ fecha_inicio`; `id_seleccion_local ≠ id_seleccion_visitante`) — deben verificarse fila por fila, no solo a nivel de esquema.
5. **Fuente verificable** — todo dato debe poder trazarse a una fuente identificable (sección 7) — nunca "entrada manual sin origen documentado", incluso si `docs/05` permite "entrada manual validada" como categoría.
6. **Nunca completar con datos inventados** — si un campo no está disponible desde la fuente, se deja vacío/nulo (cuando el esquema lo permite) o la fila se descarta — nunca se estima un valor plausible para "completar" el registro (`CLAUDE.md`, `docs/05`).
7. **No mezclar competiciones incompatibles** (`docs/05`, "Reglas") — ej. no usar datos de fútbol de clubes o categorías juveniles para poblar entidades de selecciones absolutas masculinas (alcance ya fijado por `MS-006`).

---

# 9. Estrategia de versionado de la Base de Conocimiento

`docs/05` ya fija los principios que esta sección no redefine: "los datos nunca deberán sobrescribirse", "toda modificación importante deberá quedar registrada", y que cada conjunto de datos debe indicar fecha de actualización, fuente, nivel de confianza, cobertura y observaciones ("Calidad de Datos"). El propio módulo ya aplica, en la práctica, un mecanismo concreto que satisface esos principios sin necesitar una herramienta nueva:

- **Versión semántica por módulo** (`data/processed/selecciones-nacionales/README.md`, campo "Versión": ya en `1.1.0`) — se incrementa cada vez que se agrega una entidad nueva con datos reales (`1.0.0` → `1.1.0` al poblar `selecciones`/`competiciones`, `MS-002`/`MS-006`). Se recomienda continuar esta convención: incremento de versión **menor** (`1.1.0` → `1.2.0`) por cada entidad nueva poblada con datos reales; incremento de versión **de parche** (`1.1.0` → `1.1.1`) por correcciones o ampliaciones dentro de una entidad ya poblada.
- **Registro obligatorio en `CHANGELOG.md`** por cada misión de carga de datos — ya es la práctica real desde `MS-001` (patrón ya seguido sin excepción por todas las misiones `MS-`/`DATA-` de este proyecto).
- **`docs/00-Project-Tracker.md`** como registro de qué misión pobló qué entidad y cuándo — ya es la práctica real, no una propuesta nueva.
- **Nunca sobrescribir una fila ya persistida** — `docs/05` ya lo exige; para CSV en particular, esto se traduce en: una corrección a una fila existente se registra como una nueva entrada de auditoría/observación en el `README.md` del módulo (sección "Estado de los archivos"), nunca como una edición silenciosa de la fila sin dejar rastro en `CHANGELOG.md`.

**Recomendación no aplicada aquí (Versión 2.0, `docs/05` ya lo anticipa):** un manifiesto de metadatos por lote de carga (fecha de captura, fuente, misión que lo incorporó) — hoy esa información vive dispersa entre `README.md` y `CHANGELOG.md`; formalizarla en un archivo propio (ej. `data/processed/selecciones-nacionales/MANIFEST.md` o una columna de auditoría transversal) sería una mejora de trazabilidad, no una necesidad inmediata para el MVP. Se documenta como sugerencia, no como parte del plan oficial de esta misión.

---

# 10. Riesgos identificados

| Riesgo | Severidad | Detalle |
|---|---|---|
| **`xg` (Expected Goals) puede no tener fuente pública gratuita confiable** | **Alto** | Variable003 (Nivel A, obligatoria) depende de `estadisticas_partido.csv.xg` — si la fuente elegida no publica `xg` para partidos de selecciones nacionales (a diferencia de las grandes ligas de clubes, con mejor cobertura de proveedores), el MVP completo de la sección 6 podría bloquearse en este campo específico, no en el volumen de partidos |
| **ENUM sin formalizar heredados de misiones anteriores** | **Medio** | `convocatorias.estado_convocatoria`, `lesiones.estado`, `lesiones.gravedad`, `jugadores.posicion_principal`/`posicion_convocatoria` — ninguno tiene sus valores permitidos enumerados en ningún documento (`MODEL-013`, `MODEL-015`, `docs/27`). Poblar estas columnas sin resolver primero esa formalización arriesga introducir variantes de texto inconsistentes (ej. "Portero" vs. "Arquero") que fragmentarían silenciosamente cálculos futuros |
| **Volumen real de partidos de selecciones nacionales es bajo por naturaleza** | **Medio** | A diferencia de clubes (que juegan decenas de partidos por temporada), una selección nacional juega, típicamente, 10-15 partidos oficiales al año — alcanzar `N=10` partidos "recientes" por competición para dos equipos específicos puede requerir mezclar varias competiciones/años, tensionando el principio de `docs/05` "no mezclar competiciones incompatibles" si no se diseña con cuidado |
| **Riesgo de mezclar fuentes de distinta fiabilidad entre entidades relacionadas** | **Medio** | Si `partidos.csv` proviene de una fuente y `estadisticas_partido.csv` de otra distinta para el mismo partido, podrían no coincidir en los mismos `id_partido`/eventos exactos — se recomienda, siempre que sea posible, una única fuente primaria por partido para ambos archivos |
| **Ninguna fuente de `clima`/estado real del campo por partido** (`docs/27`, Variable012) | Bajo (Variable012 no es Nivel A, no bloquea el MVP) | Ya documentado por `docs/27` como hallazgo, no nuevo aquí — se hereda, no se resuelve en esta misión |
| **Dependencia de fuentes externas no oficiales para lesiones** | Bajo (ya mitigado) | Ya resuelto por la restricción heredada de `MODEL-015` (sección 7) — se documenta como riesgo controlado, no abierto |

---

# 11. Secuencia recomendada de futuras misiones de carga de datos

Ordenada por dependencia (sección 4/5) y por menor riesgo primero — cada misión asume que la anterior está `Completada`:

| Misión propuesta | Entidad(es) | Por qué en este orden |
|---|---|---|
| **MS-012** | `estadios.csv` + `arbitros.csv` | Nivel 0 puro, cero dependencias, cero riesgo — desbloquea la FK obligatoria de `partidos.csv` sin necesitar nada más primero |
| **MS-013** | `torneos.csv` (ediciones reales, fechas y sedes, para las 10 competiciones ya catalogadas en `MS-006`) | Cierra explícitamente la brecha que `MS-006` dejó diferida; depende solo de `competiciones.csv` (ya poblado) |
| **MS-014** | `partidos.csv` + `estadisticas_partido.csv` (mismo lote, misma fuente cuando sea posible) | **La misión crítica del MVP** (sección 6) — desbloquea Variable001/002/003/004/009/010 y, con ellas, las Capas 1-3 completas del Engine. Se recomienda un primer lote acotado (2-4 selecciones, una competición, ≥10 partidos por selección) antes de escalar al resto de las 40 selecciones ya catalogadas |
| **MS-015** | `jugadores.csv` | Root de Nivel 1, depende solo de `selecciones.csv` (ya poblado); prerequisito de `convocatorias`/`lesiones` |
| **MS-016** | `convocatorias.csv` + `lesiones.csv` | Depende de `jugadores.csv` (`MS-015`) y, para `convocatorias`, de `torneos.csv` (`MS-013`) — desbloquea Variable006 (alcance reducido, Lesiones, `MODEL-015`) y Variable008 (alcance reducido, Profundidad, `MODEL-013`) |
| **MS-017** (menor prioridad, opcional para V1) | `cuotas.csv` | Depende de `partidos.csv`; desbloquea únicamente `Engine06` (Valor Esperado), ya condicional y no bloqueante — puede diferirse sin afectar el resto del MVP |

**Riesgo de secuencia explícitamente evitado:** ninguna misión de esta lista requiere resolver primero la formalización de ENUM pendientes (sección 10) — cada una puede poblar las columnas de texto libre o ya formalizadas sin bloquearse, dejando la formalización de ENUM como una misión de gobernanza de datos independiente y paralela (ya recomendada por `GR-010`/`docs/36`), no una dependencia dura de esta secuencia.

---

# Cierre obligatorio (preguntas del brief de esta misión)

**1. ¿Cuál es el orden oficial recomendado para poblar los CSV?**
Nivel 0 (`competiciones`, `selecciones`, `estadios`, `arbitros`, en paralelo) → Nivel 1 (`torneos` depende de `competiciones`; `jugadores` depende de `selecciones`) → Nivel 2 (`partidos` depende de torneos+selecciones+estadios+arbitros; `convocatorias` depende de torneos+selecciones+jugadores) → Nivel 3 (`estadisticas_partido`/`cuotas` dependen de `partidos`; `lesiones` depende de `jugadores`) — sección 5.

**2. ¿Qué dependencias existen entre ellos?**
El grafo FK exacto de `docs/32`/`docs/33`, verificado sin contradicción contra el README del módulo — sección 4. Hallazgo: `selecciones`/`estadios`/`arbitros` son, en realidad, independientes de `competiciones`/`torneos` (Nivel 0 ampliado), no estrictamente posteriores como sugiere el diagrama original.

**3. ¿Qué conjunto mínimo de datos permite ejecutar la primera predicción completa?**
2 selecciones + 1 torneo con fecha real + al menos 1 estadio/árbitro + **10 partidos finalizados por competición por equipo** (cifra ya fijada en código, `MINIMO_PARTIDOS_HISTORICOS`) + estadísticas de esos mismos partidos (`xg`/disparos) — sección 6. `jugadores`/`convocatorias`/`lesiones`/`cuotas` no son necesarios para que el pipeline complete sus 4 capas (son opcionales, `docs/17`).

**4. ¿Qué fuentes oficiales se recomiendan para cada entidad?**
Ver tabla de la sección 7 — federaciones/confederaciones oficiales como fuente primaria en todos los casos, con precedente ya usado en `MS-002`/`MS-006`; RSSSF como verificación histórica secundaria para `partidos`; Transfermarkt explícitamente desaconsejado (heredado de `MODEL-015`).

**5. ¿Qué reglas de validación deben cumplirse antes de incorporar datos?**
Integridad referencial, formato/tipo, ausencia de duplicados, restricciones propias de cada entidad, fuente verificable, nunca completar con datos inventados, no mezclar competiciones incompatibles — sección 8, síntesis de `docs/05` + el README del módulo, sin redefinir ninguna.

**6. ¿Qué estrategia de versionado debe seguir la Base de Conocimiento?**
Continuar la convención ya vigente: versión semántica por módulo (`README.md`), registro obligatorio en `CHANGELOG.md` por cada carga, seguimiento en `docs/00-Project-Tracker.md`, nunca sobrescribir una fila ya persistida — sección 9. Un manifiesto de metadatos por lote queda sugerido para una Versión 2.0, no aplicado aquí.

**7. ¿Qué misiones futuras se recomiendan y en qué orden?**
`MS-012` (estadios+árbitros) → `MS-013` (torneos, ediciones reales) → `MS-014` (partidos+estadísticas, la crítica para el MVP) → `MS-015` (jugadores) → `MS-016` (convocatorias+lesiones) → `MS-017` (cuotas, opcional) — sección 11.

**8. ¿Qué riesgos principales fueron identificados?**
`xg` sin fuente pública confiable para selecciones nacionales (alto); ENUM heredados sin formalizar (medio); bajo volumen natural de partidos de selecciones para alcanzar `N=10` sin mezclar competiciones incompatibles (medio); riesgo de fuentes inconsistentes entre `partidos`/`estadisticas_partido` del mismo partido (medio) — sección 10.

**9. ¿Qué documentos fueron creados o modificados?**
Creado: `docs/37-Estrategia-Poblacion-Base-Conocimiento.md` (este documento). Modificados: `CHANGELOG.md`, `docs/00-Project-Tracker.md` (registro de la misión). Ningún otro documento, motor, variable ni fórmula fue modificado.

**10. ¿Se actualizaron CHANGELOG.md y docs/00-Project-Tracker.md?**
Sí, ambos — ver entradas de esta misma misión (`MS-011`).

---

# Lista de verificación de cierre (`docs/22`, sección 5 — set estándar de 6 preguntas)

**1. ¿Qué problema resolvió?**
La ausencia de un plan explícito, ordenado y basado en evidencia (dependencias reales, cifras ya congeladas en código) para completar la Base de Conocimiento — hasta ahora, cada misión de carga de datos (`MS-001`, `MS-002`, `MS-006`) se decidió ad hoc, sin una hoja de ruta declarada que cubriera las 11 entidades del módulo.

**2. ¿Qué problemas nuevos descubrió?**
Dos: (a) una colisión de numeración real entre el brief de esta misión ("MS-007") y la misión ya existente `MS-007 — Prediction Pipeline` (resuelta reasignando `MS-011`, ver "Nota de origen"); (b) que `selecciones.csv`/`estadios.csv`/`arbitros.csv` no dependen realmente de `torneos.csv`/`competiciones.csv` pese a que el diagrama oficial de `docs/32`/`docs/33` las agrupa después — un matiz que no cambia ninguna FK, pero sí optimiza el orden de población real.

**3. ¿Qué documentos podrían necesitar actualización futura?**
`docs/32-Modelo-Relacional-Oficial.md`/`docs/33-Modelo-Fisico-PostgreSQL.md` podrían, en una futura misión editorial, aclarar que `selecciones`/`estadios`/`arbitros` son Nivel 0 puro (no posterior a `torneos`) — no se modifica aquí (fuera de alcance explícito de esta misión: "no modificar documentos existentes"). `data/processed/selecciones-nacionales/README.md` necesitará una nueva fila en "Estado de los archivos" después de cada misión de la secuencia de la sección 11.

**4. ¿Qué impacto tiene sobre el proyecto?**
Desbloquea metodológicamente la secuencia completa de misiones de captura de datos que, hasta ahora, solo estaba recomendada de forma genérica ("una misión de captura de datos reales", repetida como cierre de `MODEL-009` a `MODEL-015`, `INT-001`, `BUILD-023` a `BUILD-026`) sin un orden ni un volumen mínimo concretos. A partir de esta misión, "captura de datos reales" deja de ser una recomendación genérica y pasa a ser una secuencia de 6 misiones concretas con dependencias explícitas.

**5. ¿Cómo cambia el riesgo arquitectónico?**
Reduce el riesgo de que una futura misión de carga de datos population el orden equivocado (ej. intentar `partidos.csv` antes de que existan `estadios`/`árbitros` reales, generando FK huérfanas) o subestime el volumen necesario (`N=10`, ya verificado en código, no un supuesto). No introduce ningún riesgo arquitectónico nuevo — es un documento de planificación, no un cambio de arquitectura.

**6. ¿Qué impacto cualitativo tiene sobre el Índice de Madurez Arquitectónica (IMA)?**
Sin IMA formal todavía (mismo estado que `GOV-001`/`GOV-002`). Cualitativamente, esta misión agrega madurez en el eje de **datos** (hasta ahora el eje menos formalizado de los tres — arquitectura, gobernanza, y ahora datos), complementando la madurez ya alcanzada en arquitectura (`AR-001`/`AR-002`) y gobernanza (`GR-001` a `GR-010`).

---

# Gestión de hallazgos (`docs/22`, sección 7)

**Hallazgo 1 — colisión de numeración "MS-007":** documentado con el mismo rigor que el objetivo principal (ver "Nota de origen"). Justificación técnica: dos entradas distintas bajo el mismo rótulo en `docs/00-Project-Tracker.md` generarían ambigüedad real para cualquier lector futuro que busque "MS-007". **No cambia la prioridad del roadmap** — es una corrección de rótulo (`MS-011`), no una reclasificación de trabajo ni una nueva prioridad.

**Hallazgo 2 — `selecciones`/`estadios`/`arbitros` son Nivel 0, no posteriores a `torneos`:** documentado en la sección 4. Justificación técnica: verificado campo por campo contra las FK declaradas en el README del módulo — ninguna de las tres entidades tiene una columna `FK →` hacia `competiciones` ni `torneos`. **No cambia la prioridad del roadmap** — solo permite paralelizar su población (sección 11 ya refleja esto: `MS-012`, estadios+árbitros, no espera a `MS-013`, torneos).

---

# Autocrítica (`docs/22`, sección 8)

**¿Qué supuestos hice sin poder verificarlos completamente?** Que `MINIMO_PARTIDOS_HISTORICOS = 10` (`app/persistence/mu_gol_provider.py`) es representativo del volumen real necesario para una predicción "de calidad" — es, en realidad, un placeholder estructural ya documentado como tal en ese mismo módulo (no una calibración con evidencia real), y esta misión lo hereda como cifra de planificación sin volver a cuestionarlo, porque cuestionarlo pertenecería a una futura calibración (`models/parameter-calibration.md`), no a esta misión documental.

**¿Qué parte de este entregable podría estar equivocada?** La recomendación de fuentes por entidad (sección 7) es razonable pero no está verificada empíricamente contra la cobertura real de `xg` para partidos de selecciones nacionales en ninguna fuente pública concreta — el riesgo "Alto" de la sección 10 reconoce esto explícitamente; una futura misión de captura real podría descubrir que ninguna fuente gratuita cubre `xg` para selecciones nacionales fuera de los grandes torneos (Mundial, Eurocopa), obligando a revisar el MVP de la sección 6.

**¿Qué información me habría hecho falta para tener más certeza?** Un sondeo real de al menos una fuente candidata (ej. verificar si el sitio oficial de una confederación específica publica `xg` por partido) — fuera de alcance de esta misión ("no poblar CSV", "solo análisis documental"), pero sería el primer paso natural de `MS-014`.

**¿Qué validaría antes de que esto se tome como definitivo?** Que la primera ejecución real de `MS-012`-`MS-014` efectivamente respete el orden aquí propuesto sin encontrar una dependencia no anticipada (ej. que `partidos.csv` necesite, en la práctica, algún campo adicional de `estadios`/`árbitros` no capturado en el esquema actual).

**¿Existe una interpretación razonable distinta a la que elegí?** Sí — sobre la secuencia de la sección 11, podría argumentarse que `jugadores.csv`/`convocatorias.csv` (que desbloquean Variable006/008) deberían priorizarse **antes** que `partidos.csv`/`estadisticas_partido.csv`, si el objetivo fuera maximizar cuántas Variables Oficiales tienen dato real lo antes posible. Esta misión prioriza, en cambio, desbloquear el **pipeline completo** (las 4 capas del Engine) lo antes posible, porque sin Variable003/004 el Engine nunca pasa de Capa 1 — un criterio de priorización explícito, no el único válido.

---

# Fuera de alcance de esta misión

- No se escribió ningún código.
- No se modificó ningún motor, `PredictionContext`, `Runtime`, `VariablePreparation` ni `EnginePipeline`.
- No se modificó ninguna variable, fórmula matemática ni peso.
- No se pobló ningún archivo CSV de `data/processed/`.
- No se crearon scripts de carga.
- No se modificó ningún documento existente (`docs/05`, `docs/32`, `docs/33`, `docs/36`, los README de `data/processed/`) — solo se los referenció.
- No se aprueba esta estrategia como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5), igual que toda misión de arquitectura previa.

---

Fin del documento.
