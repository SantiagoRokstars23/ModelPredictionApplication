# Diseño Oficial del Pipeline de Ingesta

**Archivo:** `docs/43-Pipeline-de-Ingesta.md`

**Misión:** DATA-011 — Diseño Oficial del Pipeline de Ingesta

**Versión:** 1.0.0

**Estado:** Diseño técnico — sin código, sin CSV nuevos ni modificados, sin llamadas a ninguna API, sin modificación de `app/`/`data/`/`models/`/`knowledge/`.

---

## Nota de numeración

Verificado antes de escribir: `docs/42-Verificacion-Manual-API-Football.md` (`DATA-010A`) es el último documento de la secuencia antes del especial `docs/99-Mapa-Maestro.md` — `docs/43` está libre, sin conflicto.

---

## 1. Objetivo

Producir una especificación técnica completa del pipeline de adquisición, transformación y almacenamiento de datos, suficiente para que una misión de implementación futura no tenga que volver a tomar ninguna decisión arquitectónica — solo escribir código contra este diseño. Esta misión no consume ninguna API ni escribe ningún CSV; diseña, con la evidencia ya verificada por `FII-002`, `FII-003` y `DATA-010A`, exactamente qué se va a construir.

---

## 2. Metodología y principio de no reinvestigación

Este documento **no vuelve a investigar** las fuentes — reutiliza, campo por campo, la evidencia ya verificada directamente contra documentación oficial en `docs/41-Verificacion-Tecnica-de-Fuentes.md` (`FII-003`) y `docs/42-Verificacion-Manual-API-Football.md` (`DATA-010A`), y el protocolo ya vigente de `docs/38-Protocolo-Oficial-Ingesta-Datos.md` (`MS-012`), sin contradecir ninguno de los tres. El esquema físico objetivo es el ya oficial de `docs/33-Modelo-Fisico-PostgreSQL.md` (`DATA-005`) y `docs/32-Modelo-Relacional-Oficial.md` (`DATA-004`).

**Regla de honestidad aplicada en todo el documento:** un campo que `FII-003`/`DATA-010A` confirmaron ausente se documenta aquí como ausente, sin reabrir la pregunta. Un campo que ninguna de esas dos misiones verificó explícitamente (ej. los campos exactos de respuesta de `/teams` o de `/leagues` más allá de lo ya citado) se marca **"pendiente de confirmación en la primera implementación"** — nunca se asume su existencia ni su formato por conocimiento general de la API, solo por lo ya verificado con evidencia directa.

---

## 3. Grafo de dependencias y orden de ejecución (justificado, no asumido)

`docs/32-Modelo-Relacional-Oficial.md` §7 ya estableció que **Equipo (Selecciones), Competición, Estadio y Árbitro son entidades independientes** — pueden poblarse sin que exista ninguna otra entidad primero. El brief propone un orden estrictamente secuencial (Competiciones → Equipos → Estadios → Partidos → Estadísticas → Jugadores → Convocatorias → Cuotas); este diseño lo reemplaza por un orden **agrupado por capas de dependencia real**, porque una secuencia estrictamente lineal obligaría a esperar innecesariamente entre entidades que no dependen entre sí (ej. no hay ninguna razón para poblar Estadios antes de Selecciones si ninguna depende de la otra).

```
Capa 0 (independientes entre sí, sin FK de entrada — pueden ejecutarse en paralelo)
  ├── Competiciones + Torneos     (FK de salida: ninguna)
  ├── Selecciones                 (FK de salida: ninguna)
  ├── Estadios                    (FK de salida: ninguna)
  └── Árbitros                    (FK de salida: ninguna; ver hallazgo 7.1 — sin fuente poblable)

Capa 1 (depende únicamente de Selecciones, Capa 0)
  └── Jugadores                   (FK: seleccion_id)

Capa 2 (depende de Torneos + Selecciones, Capa 0; Estadios/Árbitros opcionales)
  └── Partidos                    (FK: torneo_id, seleccion_local_id, seleccion_visitante_id;
                                    FK opcionales: estadio_id, arbitro_id)

Capa 3 (depende de Partidos, Capa 2, + Selecciones, Capa 0)
  └── Estadísticas de Partido     (FK: partido_id, seleccion_id)

Capa 4 (depende de Torneos + Selecciones, Capa 0, + Jugadores, Capa 1)
  └── Convocatorias               (FK: torneo_id, seleccion_id, jugador_id)

Capa 5 (depende de Partidos, Capa 2 — ver hallazgo 7.1: sin fuente poblable para el dominio actual)
  └── Cuotas                      (FK: partido_id)
```

**Por qué Jugadores se adelanta respecto al orden de ejemplo del brief:** su único FK de entrada es `seleccion_id` (Capa 0) — no depende de Partidos ni de Estadísticas, por lo que retrasarlo hasta después de esas dos entidades solo introduce una espera artificial sin ninguna razón de integridad referencial.

**Por qué Árbitros y Cuotas permanecen en el grafo pese a no tener fuente poblable hoy:** ambas entidades siguen siendo parte del esquema oficial (`docs/33`) y del orden de dependencia real; su falta de fuente es una limitación de las dos fuentes candidatas, no del diseño del pipeline — se documentan en su posición correcta del grafo y se marcan explícitamente como bloqueadas (sección 7.1).

---

## 4. Arquitectura del pipeline

Reutiliza sin contradecirlo el flujo ya oficial de `docs/38` §3 (`Fuente oficial → Captura → Validación → Normalización → Revisión manual → CSV en processed/`), con la "Transformación" que pide este brief ubicada exactamente en el paso "Normalización" ya definido allí — no es una etapa nueva, es el nombre que usa este documento para el mismo paso.

```
   API-Football                          Football-Data.co.uk
 (Selecciones, Competiciones,           (Cuotas — ver hallazgo 7.1:
  Torneos, Estadios, Partidos,           sin cobertura de selecciones
  Estadísticas, Jugadores,               nacionales, fuente bloqueada
  Convocatorias)                         para el dominio actual)
        │                                         │
        ▼                                         ▼
  Extracción                              Extracción
  (1 llamada por endpoint/lote,           (descarga CSV por URL
  respetando el rate limit del             predecible, respetando
  plan — docs/42 §3.7)                     el rate-limit del sitio,
        │                                   FII-003 §4.2)
        └───────────────────┬─────────────────────┘
                             ▼
                       Validación
             (docs/38 §5-6: duplicados, FK,
              formato, rangos, resultado
              imposible → rechazo de la fila
              antes de transformarla)
                             │
                             ▼
                Normalización / Transformación
             (fechas → YYYY-MM-DD; resolución de
              ID externo → UUID interno del
              proyecto; parseo de campos string;
              mapeo a ENUM del esquema — sección 6)
                             │
                             ▼
                      Revisión manual
             (docs/38 §3 — verificación humana de
              plausibilidad, obligatoria antes de
              incorporar; nunca se omite)
                             │
                             ▼
                     CSV oficiales en
           data/processed/selecciones-nacionales/
```

---

## 5. Componente de soporte necesario, no incluido en el esquema actual

El pipeline requiere una **tabla de correspondencia de identificadores externos** (`id` de API-Football / claves de Football-Data.co.uk ↔ clave de negocio del proyecto, ej. `id_seleccion`, `id_torneo`) para poder resolver los FK de cada fila sin volver a consultar la fuente en cada ejecución. Esto **no es un CSV nuevo del dominio del modelo** (no representa una entidad de negocio, es un artefacto técnico interno del pipeline) y esta misión no lo crea — se documenta como un componente que la misión de implementación deberá diseñar dentro de `app/` (fuera del alcance de esta misión, que no puede tocar `app/`), no dentro de `data/processed/`.

---

## 6. Mapeo campo a campo por archivo

Orden: el de ejecución de la sección 3. Columnas: **Campo → Fuente → Endpoint → Transformación → Obligatorio → Observaciones**. "Obligatorio" reproduce exactamente `docs/33`. Todo campo marcado `✗ Sin fuente` reaparece consolidado en la sección 7.

### 6.1 `competiciones.csv` + `torneos.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `competiciones.id_competicion` | Generado internamente | — | Asignación de clave de negocio propia (`COMP-NNNNNN`) | Sí | No proviene de ninguna fuente externa — es una clave del proyecto |
| `competiciones.nombre` | API-Football | `GET /leagues` | Identidad (copia directa de `league.name`) | Sí | — |
| `competiciones.confederacion_organizadora` | API-Football (parcial) | `GET /leagues` | Mapeo país→confederación, o inferencia desde la agrupación por confederación de `/coverage` (`DATA-010A` §3, "1235 Leagues & Cups" agrupadas por confederación en la página oficial) | Sí | `/leagues` no confirma un campo directo de confederación (solo `country`) — **pendiente de confirmación en la primera implementación**: verificar si `/leagues` expone confederación o si debe derivarse de la agrupación de `/coverage` |
| `competiciones.tipo` | API-Football | `GET /leagues` | Mapeo ENUM (`type: "league"` / `"cup"` → ENUM del proyecto) | Sí | ENUM del proyecto (`docs/33`) aún no formalizado con sus valores exactos — mapeo pendiente de esa formalización, no inventado aquí |
| `competiciones.periodicidad_anios` | ✗ Sin fuente | — | — | No | Ninguna fuente investigada expone periodicidad como campo — se deja NULL (campo no obligatorio) |
| `torneos.id_torneo` | Generado internamente | — | Clave de negocio propia | Sí | — |
| `torneos.edicion` | API-Football | `GET /leagues` (campo `season`) | Identidad | Sí | — |
| `torneos.paises_organizadores` | API-Football (aproximado) | `GET /leagues` (campo `country`) | Identidad, con advertencia: `country` es del nivel liga, no necesariamente de la sede del torneo específico | No | Aproximación, no un campo dedicado de "país organizador" |
| `torneos.fecha_inicio` / `fecha_fin` | ✗ Sin fuente confirmada | — | — | Sí | Ninguna de las dos misiones de verificación confirmó un campo explícito de fecha de inicio/fin de temporada en `/leagues` — **pendiente de confirmación en la primera implementación**; si no existe, deberá derivarse como `MIN(fecha)`/`MAX(fecha)` de los partidos ya cargados del torneo (cálculo posterior a Partidos, no en esta capa) |
| `torneos.formato` | ✗ Sin fuente | — | — | No | No confirmado en ninguna fuente investigada |
| `torneos.numero_selecciones_participantes` | ✗ Sin fuente directa | — | Derivable por conteo de `COUNT(DISTINCT seleccion)` sobre `partidos.csv` ya cargado | No | No es un campo directo — requiere que Partidos ya esté poblado |

### 6.2 `selecciones.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `id_seleccion` | Generado internamente | — | Clave de negocio propia (3 letras, `docs/33`) | Sí | — |
| `nombre_pais` | API-Football | `GET /teams` (`type=national`) | Identidad | Sí | Confirmado en `FII-003` §3.3 |
| `nombre_federacion` | ✗ Sin fuente | — | — | Sí | Confirmado ausente en `FII-003` §3.3 |
| `confederacion` | ✗ Sin fuente | — | — | Sí | Confirmado ausente en `FII-003` §3.3 |
| `ranking_fifa_actual` / `ranking_fifa_fecha` | ✗ Sin fuente | — | — | Sí | Confirmado ausente — ninguna fuente investigada expone ranking FIFA |
| `seleccionador_actual` | API-Football (derivado) | `GET /coachs` | Resolución: filtrar por `team` = selección, tomar el registro sin fecha de fin | No | Derivable pero no directo — requiere una segunda llamada y lógica de resolución |
| `activa` | API-Football (aproximado) | `GET /leagues?team={id}&current=true` | Derivado (¿participa en alguna competición vigente?) | Sí | Aproximación, no un campo booleano directo del perfil de selección |

### 6.3 `estadios.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `id_estadio` | Generado internamente | — | Clave de negocio propia | Sí | — |
| `nombre` | API-Football | `GET /venues` | Identidad | Sí | Confirmado `DATA-010A` §3.18 (ejemplo real: "Old Trafford") |
| `ciudad` | API-Football | `GET /venues` | Identidad | Sí | Confirmado |
| `pais` | API-Football | `GET /venues` | Identidad | Sí | Confirmado |
| `capacidad` | API-Football | `GET /venues` | Identidad | Sí | Confirmado |
| `tipo_superficie` | API-Football | `GET /venues` (campo `surface`) | Mapeo ENUM (`"grass"` → valor ENUM del proyecto) | Sí | Confirmado que el campo existe; mapeo ENUM pendiente de que el proyecto formalice sus valores permitidos |
| `altitud_metros` | ✗ Sin fuente | — | — | Sí | **Confirmado ausente** — `DATA-010A` §3.18, objeto `/venues` completo leído (8 campos exactos, ninguno de altitud) |
| `techado` | ✗ Sin fuente | — | — | Sí | **Confirmado ausente** — mismo objeto, sin campo de techo/domo |

### 6.4 `arbitros.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| Todos los campos (`nombre_completo`, `nacionalidad`, `confederacion_arbitral`, `categoria`, `activo`) | ✗ Sin fuente | — | — | Sí (todos) | **Confirmado ausente un endpoint de árbitros** — `DATA-010A` §3.17: no existe `/referees` en el índice completo de `ENDPOINTS` de la documentación oficial. `referee` solo existe como texto libre dentro de `fixture`, sin ID ni entidad propia. Ver hallazgo 7.1: `arbitros.csv` queda bloqueado con las dos fuentes aprobadas. |

### 6.5 `jugadores.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `id_jugador` | Generado internamente | — | Clave de negocio propia (se puede usar `player.id` de API-Football como semilla, resuelto vía tabla de correspondencia — sección 5) | Sí | — |
| `nombre_completo` | API-Football | `GET /players` | Composición: `firstname` + `" "` + `lastname` | Sí | Confirmado `DATA-010A` §3.20 (ejemplo real: Neymar) |
| `nombre_conocido` | API-Football | `GET /players` (campo `name`) | Identidad | No | Confirmado |
| `fecha_nacimiento` | API-Football | `GET /players` (campo `birth.date`) | Conversión de formato a `YYYY-MM-DD` | Sí | Confirmado |
| `posicion_principal` | API-Football (indirecto) | `GET /players/squads` (campo `position`) | Mapeo ENUM | Sí | El perfil base de `/players` (`docs/42` §3.20) no incluye posición directamente — se resuelve vía `/players/squads`, endpoint distinto |
| `pie_habil` | ✗ Sin fuente | — | — | No | **Confirmado ausente** — `DATA-010A` §3.20, objeto de perfil completo de Neymar leído (`id, name, firstname, lastname, age, birth, nationality, height, weight, injured, photo`), sin ningún campo de pie hábil |
| `altura_cm` | API-Football | `GET /players` (campo `height`) | **Parseo obligatorio**: el valor llega como string con unidad (ej. `"175 cm"`) — extraer el entero antes de almacenar | No | Confirmado el campo, con formato que requiere transformación explícita |
| `id_seleccion` | API-Football (derivado) | `GET /players` (vía `statistics[].team`) | Resolución FK: `team.id` externo → `id_seleccion` interno (tabla de correspondencia, sección 5) | Sí | Requiere que `selecciones.csv` (Capa 0) ya esté poblado |
| `club_actual` | API-Football | `GET /players` (vía `statistics[].team.name`) | Identidad | No | Confirmado |
| `activo_seleccion` | ✗ Sin fuente directa | — | Derivado: ¿aparece en `/players/squads` de alguna selección con `season` vigente? | Sí | Aproximación, no un campo booleano directo |

### 6.6 `partidos.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `id_partido` | Generado internamente (semilla `fixture.id`) | — | Resolución vía tabla de correspondencia | Sí | — |
| `id_torneo` | API-Football (derivado) | `GET /fixtures` (vía `league.id`) | Resolución FK: `league.id` externo → `id_torneo` interno | Sí | Requiere Capa 0 (Competiciones/Torneos) ya poblada |
| `id_seleccion_local` / `id_seleccion_visitante` | API-Football | `GET /fixtures` (vía `teams.home.id`/`teams.away.id`) | Resolución FK | Sí | Requiere Capa 0 (Selecciones) ya poblada; validación obligatoria: ambos IDs distintos (`docs/38` §6) |
| `id_estadio` | API-Football | `GET /fixtures` (vía `fixture.venue.id`) | Resolución FK | No | Requiere Capa 0 (Estadios); confirmado `DATA-010A` §3.20 que el objeto `venue` embebido en `fixture` solo trae `id, name, city` (no todos los campos de `/venues`) — se usa solo para resolver el FK, no para poblar `estadios.csv` |
| `id_arbitro` | ✗ Sin fuente | — | — | No | **Confirmado ausente como entidad con ID** — `referee` es texto libre dentro de `fixture` (`DATA-010A` §3.17); sin `arbitros.csv` poblado (sección 6.4) no hay FK que resolver — queda NULL siempre con las fuentes actuales |
| `fecha` | API-Football | `GET /fixtures` (campo `fixture.date`) | Conversión de formato ISO 8601 con timezone → `YYYY-MM-DD` | Sí | Confirmado |
| `hora_local` | API-Football | `GET /fixtures` (campos `fixture.date` + `fixture.timezone`) | Extracción de la hora, ajustada al timezone solicitado en el parámetro de la llamada | No | Confirmado |
| `fase` | API-Football (aproximado) | `GET /fixtures` (vía `league.round`) | **Derivado, no trivial**: `round` es un string libre (ej. `"Regular Season - 14"`, `"Quarter-finals"`) — requiere reglas de parsing/heurística (palabras clave: "Final", "Semi-finals", "Quarter-finals", "Group Stage" → fase; de lo contrario, fase = "fase de grupos"/liga regular) | Sí | Mapeo ENUM pendiente de que el proyecto formalice sus valores permitidos (`docs/38` hallazgo 1, heredado sin resolver) |
| `jornada` | API-Football (aproximado) | `GET /fixtures` (vía `league.round`) | **Derivado, no trivial**: extraer el número final del string `round` cuando existe (ej. `"...- 14"` → `14`); no aplica en fases de eliminación directa | Solo si `fase = fase_grupos` | Mismo campo fuente que `fase`, misma limitación |
| `goles_local` / `goles_visitante` | API-Football | `GET /fixtures` (vía `goals.home`/`goals.away`) | Identidad | Solo si `estado_partido = finalizado` | Confirmado; validación obligatoria: no negativos (`docs/38` §6) |
| `estado_partido` | API-Football | `GET /fixtures` (vía `status.long`/`status.short`) | Mapeo ENUM (valores de API-Football → ENUM del proyecto) | Sí | Confirmado el campo; **hallazgo heredado de `docs/38` §10.1, no resuelto aquí**: el ENUM del proyecto nunca formalizó valores más allá de `"finalizado"` — el mapeo completo queda pendiente de esa formalización |
| `asistencia` | ✗ Sin fuente | — | — | No | **Confirmado ausente** — `DATA-010A` §3.20, objeto `fixture` completo leído (`id, referee, timezone, date, timestamp, periods, venue, status`), sin ningún campo de asistencia |

### 6.7 `estadisticas_partido.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `id_estadistica_partido` | Generado internamente | — | Clave de negocio propia | Sí | — |
| `partido_id` / `seleccion_id` | API-Football (derivado) | `GET /fixtures/statistics?fixture={id}` | Resolución FK (doble: por partido y por equipo dentro del partido) | Sí | Requiere Capa 2 (Partidos) y Capa 0 (Selecciones) ya pobladas |
| `xg` | ✗ Sin fuente | — | — | Sí | **Confirmado ausente con la mayor solidez de evidencia de todo este documento** (`DATA-010A` §3.1): cero coincidencias en el árbol de accesibilidad completo de la documentación oficial, y el listado exhaustivo de 16 tipos de estadística de `/fixtures/statistics` no lo incluye. Football-Data.co.uk tampoco lo tiene y, además, no cubre selecciones (no es alternativa). **Queda NULL de forma permanente con las fuentes actualmente aprobadas.** |
| `posesion_pct` | API-Football | `GET /fixtures/statistics` (`Ball Possession`) | Parseo: valor llega como string con `%` (ej. `"55%"`) — extraer el número | Sí | Confirmado; validación: rango `[0,100]` (`docs/38` §6) |
| `disparos_totales` | API-Football | `GET /fixtures/statistics` (`Total Shots`) | Identidad | Sí | Confirmado |
| `disparos_al_arco` | API-Football | `GET /fixtures/statistics` (`Shots on Goal`) | Identidad | Sí | Confirmado; validación: `disparos_al_arco ≤ disparos_totales` (`docs/38` §9) |
| `corners` | API-Football | `GET /fixtures/statistics` (`Corner Kicks`) | Identidad | Sí | Confirmado |
| `faltas_cometidas` | API-Football | `GET /fixtures/statistics` (`Fouls`) | Identidad | Sí | Confirmado |
| `tarjetas_amarillas` / `tarjetas_rojas` | API-Football | `GET /fixtures/statistics` (`Yellow Cards`/`Red Cards`) | Identidad | Sí | Confirmado |
| `pases_completados` | API-Football | `GET /fixtures/statistics` (`Passes accurate`) | Identidad | Sí | Confirmado |
| `precision_pases_pct` | API-Football | `GET /fixtures/statistics` (`Passes %`) | Parseo: string con `%` → número | Sí | Confirmado |

### 6.8 `convocatorias.csv`

| Campo | Fuente | Endpoint | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| `id_convocatoria` | Generado internamente | — | Clave de negocio propia | Sí | — |
| `torneo_id` | ✗ Sin fuente directa | — | — | Sí | **Confirmado ausente** — `/players/squads` (`DATA-010A` §3.16) devuelve la plantilla *actual* de un club/selección, sin vínculo a un torneo específico. Solo sería inferible cruzando manualmente con `partidos.csv` (¿el jugador aparece en alineaciones de partidos de ese torneo?) — inferencia indirecta y no confiable, no una resolución de FK directa |
| `seleccion_id` | API-Football | `GET /players/squads?team={id}` | Resolución FK | Sí | Confirmado (ejemplo real: Manchester United) |
| `jugador_id` | API-Football | `GET /players/squads` | Resolución FK | Sí | Confirmado |
| `dorsal` | API-Football | `GET /players/squads` (campo `number`) | Identidad | Sí | Confirmado |
| `posicion_convocatoria` | API-Football | `GET /players/squads` (campo `position`) | Mapeo ENUM | Sí | Confirmado el campo; ENUM pendiente de formalización |
| `fecha_convocatoria` | ✗ Sin fuente | — | — | Sí | **Confirmado ausente** — objeto completo de plantilla leído (`id, name, age, number, position, photo`), sin ningún campo de fecha |
| `estado_convocatoria` | ✗ Sin fuente | — | — | Sí | **Confirmado ausente**, mismo objeto |

**Nota crítica sobre esta entidad:** de los 7 campos, 3 (`torneo_id`, `fecha_convocatoria`, `estado_convocatoria`) — todos obligatorios según `docs/33` — no tienen fuente con las dos fuentes aprobadas. Una fila de `convocatorias.csv` con campos obligatorios ausentes **debe rechazarse** según la regla ya vigente de `docs/38` §5 ("¿Qué ocurre si falta un campo obligatorio? La fila se rechaza"). **Esto significa que `convocatorias.csv` no puede poblarse en absoluto con las fuentes hoy aprobadas**, no solo que quede parcialmente incompleto — ver hallazgo 7.1.

### 6.9 `cuotas.csv`

| Campo | Fuente | Endpoint / archivo | Transformación | Obligatorio | Observaciones |
|---|---|---|---|---|---|
| Todos los campos | ✗ Sin fuente aplicable al dominio actual | — | — | — | **Hallazgo más severo de este documento, ver sección 7.1.** Football-Data.co.uk (fuente recomendada para cuotas desde `FII-002`/`FII-003`) **no cubre selecciones nacionales bajo ningún concepto** (`FII-003` §4.3: sus 27 competiciones son todas ligas domésticas de clubes) — no es una fuente aplicable al dominio actual del proyecto en absoluto, con independencia de qué tan bien cubra sus propios campos. API-Football sí cubre selecciones vía `GET /odds`, pero **solo retiene 7 días de historial** (`DATA-010A` §3.19, texto oficial verbatim), inútil para cualquier uso de backtesting o EV histórico — solo serviría para consumo de cuotas en tiempo real de partidos futuros próximos, un caso de uso distinto al que `cuotas.csv`/cuotas históricas fue diseñado para resolver (`docs/39` Bloque D). |

---

## 7. Columnas que no pueden llenarse — consolidado (responde directamente los puntos 3 y 6 del brief)

**Ninguna columna de esta lista se completa por inventar un valor.** Todas quedan `NULL` (si no son obligatorias) o bloquean la fila completa (si son obligatorias, por la regla ya vigente de `docs/38` §5).

| Archivo | Columna | Obligatorio | Motivo (evidencia) |
|---|---|---|---|
| `partidos.csv` | `id_arbitro` | No | Sin endpoint de árbitros en ninguna fuente aprobada (`DATA-010A` §3.17) |
| `partidos.csv` | `asistencia` | No | Confirmado ausente en el objeto `fixture` completo (`DATA-010A` §3.20) |
| `estadisticas_partido.csv` | `xg` | **Sí** | Confirmado ausente con la evidencia más sólida de este documento (`DATA-010A` §3.1) — **bloquea la fila si el esquema no permite `xg` nulo**; ver hallazgo 7.2 |
| `estadios.csv` | `altitud_metros` | **Sí** | Confirmado ausente (`DATA-010A` §3.18) |
| `estadios.csv` | `techado` | **Sí** | Confirmado ausente (`DATA-010A` §3.18) |
| `jugadores.csv` | `pie_habil` | No | Confirmado ausente (`DATA-010A` §3.20) |
| `competiciones.csv` | `periodicidad_anios` | No | Sin fuente en ninguna investigación realizada |
| `torneos.csv` | `fecha_inicio` / `fecha_fin` | **Sí** | No confirmado un campo directo — requiere derivación posterior desde `partidos.csv` (sección 6.1) |
| `torneos.csv` | `formato` | No | Sin fuente |
| `selecciones.csv` | `nombre_federacion` | **Sí** | Confirmado ausente (`FII-003` §3.3) |
| `selecciones.csv` | `confederacion` | **Sí** | Confirmado ausente (`FII-003` §3.3) |
| `selecciones.csv` | `ranking_fifa_actual` / `ranking_fifa_fecha` | **Sí** | Confirmado ausente (`FII-003` §3.3) |
| `arbitros.csv` | Las 5 columnas de dato (todas) | **Sí** (todas) | Entidad completa sin fuente poblable — sección 7.1 |
| `convocatorias.csv` | `torneo_id`, `fecha_convocatoria`, `estado_convocatoria` | **Sí** (las 3) | Confirmado ausente (`DATA-010A` §3.16) — bloquea la entidad completa, sección 7.1 |
| `cuotas.csv` | Todas las columnas | **Sí** (todas) | Entidad completa sin fuente aplicable al dominio actual — sección 7.1 |

### 7.1 Hallazgo crítico: tres entidades completas quedan bloqueadas, no solo parcialmente incompletas

A diferencia de lo que `FII-003`/`DATA-010A` ya habían caracterizado como "cobertura parcial" campo por campo, este diseño revela que **tres de las diez entidades del grafo no pueden poblarse en absoluto** con las dos fuentes hoy aprobadas, porque les falta al menos un campo **obligatorio** sin fuente:

1. **`arbitros.csv`** — ningún campo tiene fuente (sección 6.4).
2. **`convocatorias.csv`** — 3 de 7 campos son obligatorios y no tienen fuente (sección 6.8).
3. **`cuotas.csv`** — ninguna de las dos fuentes aprobadas cubre el dominio actual (selecciones nacionales) en absoluto (sección 6.9).

Esto no es un hallazgo nuevo sobre las fuentes (ya estaba implícito en `FII-003`/`DATA-010A`) — es un hallazgo nuevo sobre **qué produce realmente el pipeline diseñado**: de las 6 entidades exigidas por el brief más las 4 de soporte, solo **7 de 10** pueden poblarse de forma completa o parcial útil; 3 quedan completamente bloqueadas.

### 7.2 Segundo hallazgo: `xg` es un campo obligatorio sin fuente

`docs/33` declara `xg` como `Obligatorio: Sí` en `estadisticas_partido.csv`. Con la regla ya vigente de `docs/38` §5 ("si falta un campo obligatorio, la fila se rechaza"), **una interpretación literal y estricta rechazaría todas las filas de `estadisticas_partido.csv` provenientes de API-Football**, porque ninguna tendría `xg`. Esta misión **no tiene autoridad para relajar esa obligatoriedad** (sería modificar el esquema, fuera de alcance) ni para inventar un valor — se documenta como una contradicción real entre el esquema ya oficial y la fuente disponible, que requiere una decisión explícita del Arquitecto Estadístico Humano antes de la implementación (ver Cierre, pregunta 2).

---

## 8. Columnas por fuente (puntos 4 y 5 del brief)

| Fuente | Columnas que provee (de los 6 archivos exigidos) |
|---|---|
| **API-Football** | `partidos.csv`: `id_partido`(semilla), `id_torneo`, `id_seleccion_local`, `id_seleccion_visitante`, `id_estadio`, `fecha`, `hora_local`, `fase`(aprox.), `jornada`(aprox.), `goles_local`, `goles_visitante`, `estado_partido`. `estadisticas_partido.csv`: `posesion_pct`, `disparos_totales`, `disparos_al_arco`, `corners`, `faltas_cometidas`, `tarjetas_amarillas`, `tarjetas_rojas`, `pases_completados`, `precision_pases_pct`. `jugadores.csv`: `nombre_completo`, `nombre_conocido`, `fecha_nacimiento`, `posicion_principal`, `altura_cm`(con parseo), `id_seleccion`, `club_actual`. `estadios.csv`: `nombre`, `ciudad`, `pais`, `capacidad`, `tipo_superficie`. `convocatorias.csv`: `seleccion_id`, `jugador_id`, `dorsal`, `posicion_convocatoria`. |
| **Football-Data.co.uk** | **Ninguna** de las columnas de los 6 archivos exigidos — no cubre selecciones nacionales (ver sección 6.9 y 7.1). Sigue siendo la fuente recomendada exclusivamente si el proyecto amplía su alcance a ligas de clubes en una fase futura (`docs/39` §7, Fase III), fuera del dominio evaluado por esta misión. |
| **Generado internamente (no es una fuente externa)** | Todos los `id_*` de clave de negocio (asignados por el proyecto), y las claves técnicas UUID + `creado_en`/`actualizado_en` de todas las entidades (`docs/33`). |
| **Sin fuente (ninguna de las dos)** | Ver tabla consolidada, sección 7. |

---

## 9. Estrategia de actualización por archivo

| Archivo | Estrategia | Justificación |
|---|---|---|
| `competiciones.csv` / `torneos.csv` | **Por torneo** (manual, al confirmarse un nuevo torneo o edición) | No cambian con frecuencia; no existe beneficio en poblarlos con cadencia diaria/semanal |
| `selecciones.csv` | **Manual / por evento** (cambio de seleccionador, alta/baja) | Los campos dinámicos más relevantes (`ranking_fifa_*`) no tienen fuente en absoluto (sección 7) — no hay nada que actualizar automáticamente con cadencia regular |
| `estadios.csv` | **Manual** (baja frecuencia de cambio real) | Un estadio cambia de nombre/capacidad con muy poca frecuencia |
| `arbitros.csv` | **No aplica** | Entidad bloqueada, sección 7.1 |
| `jugadores.csv` | **Semanal** | Coincide con la cadencia real ya confirmada en la documentación oficial: `/players/squads` se actualiza "several times a week" (`DATA-010A`, capturado en pantalla en la sesión de verificación) |
| `partidos.csv` | **Incremental, por torneo activo** (diaria durante ventanas de competición) | `/fixtures` se actualiza "every minute" según la documentación oficial para partidos en vivo, pero para el propósito de este pipeline (registrar resultado final) basta una consulta diaria durante la ventana del torneo, no en tiempo real |
| `estadisticas_partido.csv` | **Incremental**, inmediatamente después de que cada partido cambie a `estado_partido = finalizado` | Depende de `partidos.csv` ya actualizado (Capa 3) |
| `convocatorias.csv` | **No aplica** | Entidad bloqueada, sección 7.1 |
| `cuotas.csv` | **No aplica** | Entidad bloqueada para el dominio actual, sección 7.1 |

---

## 10. Validaciones

Reutiliza, sin redefinirlas, las reglas ya vigentes de `docs/38` §5-6 y §9 — esta sección solo las instancia para el caso concreto de esta ingesta, sin crear reglas nuevas que las contradigan.

**Antes de aceptar cualquier registro (obligatorias, heredadas de `docs/38`):**
- IDs duplicados (clave primaria o clave única de negocio ya existente).
- FK inexistente (`torneo_id`, `seleccion_id`, `jugador_id`, `partido_id`, `estadio_id`, `arbitro_id` deben resolver contra una fila ya cargada).
- Fecha inválida (formato no `YYYY-MM-DD` tras la normalización; fecha futura imposible para un partido ya marcado `finalizado`).
- `id_seleccion_local = id_seleccion_visitante` (mismo equipo local y visitante).
- `goles_local`/`goles_visitante` negativos.
- `disparos_al_arco > disparos_totales`.
- `posesion_pct` fuera de `[0,100]`.
- `cuota_decimal ≤ 1.00` (no aplica hoy — entidad bloqueada, sección 7.1).
- Campo obligatorio ausente tras la transformación → **rechazo de la fila completa** (regla ya vigente, `docs/38` §5) — esta es la regla que, aplicada estrictamente, bloquea `arbitros.csv`, `convocatorias.csv` y `cuotas.csv` (sección 7.1) y genera la contradicción de `xg` (sección 7.2).
- Fuente prohibida o sin verificación (`docs/38` §4) — no aplica aquí porque solo se diseñan las dos fuentes ya aprobadas.
- Mezcla de competiciones incompatibles (clubes, categorías juveniles, fútbol femenino) — validación explícita necesaria porque API-Football no distingue estos casos de forma tan clara como StatsBomb Open Data ya lo hacía.

**Validaciones específicas de esta ingesta, no cubiertas literalmente por `docs/38` porque son propias de consumir una API externa (no contradicen el protocolo, lo extienden a un caso nuevo):**
- Respuesta HTTP distinta de `200`/`204` → no se procesa la respuesta, se reintenta según política de backoff (no diseñada en detalle aquí — corresponde a la implementación).
- Límite de rate excedido (`100 req/día` en plan Free, `DATA-010A` §3.7) → la ejecución se detiene para ese lote, no se continúa consumiendo con reintentos agresivos.
- Campo que llega con formato inesperado tras el parseo (ej. `height` sin el sufijo `" cm"` esperado) → la fila se marca para Revisión manual (`docs/38` §3), no se descarta automáticamente ni se fuerza un valor.

---

## 11. Riesgos

- **Contradicción de esquema no resuelta (`xg`, sección 7.2):** requiere decisión explícita del Arquitecto Estadístico Humano antes de implementar — sin esa decisión, la implementación no puede saber si debe rechazar todas las filas de `estadisticas_partido.csv` de API-Football o si el esquema debe admitir `xg` nulo.
- **Tres entidades completas bloqueadas (sección 7.1):** `arbitros.csv`, `convocatorias.csv` y `cuotas.csv` no producen ninguna fila con las fuentes hoy aprobadas — riesgo de que una futura misión de implementación asuma que "diseñar el pipeline" significa que las 10 entidades quedarán pobladas, cuando en realidad 3 permanecerán vacías indefinidamente sin una fuente adicional.
- **Campos derivados no triviales (`fase`/`jornada` desde `round`, sección 6.6):** el parsing heurístico de un string libre es una fuente real de errores silenciosos si no se prueba contra una muestra amplia de competiciones antes de confiar en él para producción.
- **Dependencia de dos proveedores externos sin SLA** — ya documentado en `FII-003` §7, se hereda sin cambio.
- **ENUMs del proyecto aún no formalizados** (`tipo_superficie`, `posicion_principal`, `estado_partido` más allá de "finalizado", `fase`) — cada mapeo de esta sección 6 que dice "ENUM pendiente de formalización" bloquea, en la práctica, la transformación de ese campo hasta que se resuelva ese hallazgo heredado de `docs/38` §10.1.
- **Rate limit del plan Free (100 req/día)** — con selecciones + torneos + partidos + estadísticas + jugadores + convocatorias, el volumen de llamadas necesario para una carga inicial completa probablemente exceda el plan gratuito; la implementación deberá estimar el volumen real antes de decidir si el plan Free alcanza o si se requiere el plan Pro ($19/mes, `DATA-010A` §3.7).

---

## 12. Cierre obligatorio

**1. ¿El pipeline quedó completamente definido?** Sí, en el sentido de que cada uno de los 6 archivos exigidos (más las 4 entidades de soporte) tiene una tabla campo a campo con fuente, endpoint, transformación y obligatoriedad — no quedan decisiones de mapeo por tomar durante la implementación. **No** en el sentido de que 3 entidades completas (sección 7.1) no tienen ninguna fuente que las pueble; el diseño de esas 3 está "completo" solo en el sentido de que confirma, con evidencia, que no pueden implementarse todavía.

**2. ¿Quedan decisiones arquitectónicas pendientes?** Sí, una — explícita y señalada como tal (sección 7.2): qué hacer con la obligatoriedad de `xg` en `estadisticas_partido.csv` dado que ninguna fuente aprobada lo provee. Requiere al Arquitecto Estadístico Humano, no a esta misión (Constitución, Art. 2/5).

**3. ¿Qué datos nunca podrán obtenerse (con las fuentes hoy aprobadas)?** `xg`, `asistencia`, `altitud_metros`, `techado`, `pie_habil` de forma permanente por campo; y de forma estructural, las 3 entidades completas de la sección 7.1 (`arbitros.csv`, `convocatorias.csv`, `cuotas.csv`) hasta que se apruebe una fuente adicional.

**4. ¿Qué transformaciones son obligatorias?** Conversión de fecha ISO 8601 con timezone → `YYYY-MM-DD`; parseo de campos string con unidad (`height`, `posesion_pct`, `precision_pases_pct`); resolución de FK vía tabla de correspondencia de IDs externos (sección 5) para prácticamente todos los campos relacionales; derivación heurística de `fase`/`jornada` desde el string `round` (la más riesgosa, sección 11).

**5. ¿Qué validaciones son críticas?** La regla ya vigente de `docs/38` §5 ("campo obligatorio ausente → fila rechazada"), aplicada estrictamente, es la más crítica de todas porque es la que expone la contradicción de la sección 7.2 y bloquea las 3 entidades de la sección 7.1 — no es una validación nueva de esta misión, es la consecuencia de aplicar sin excepciones una regla ya aprobada.

**6. ¿Qué archivo depende de cuál?** Grafo completo en la sección 3: Competiciones/Torneos, Selecciones, Estadios y Árbitros son independientes entre sí (Capa 0); Jugadores depende solo de Selecciones (Capa 1); Partidos depende de Torneos + Selecciones (Capa 2); Estadísticas de Partido depende de Partidos (Capa 3); Convocatorias depende de Torneos + Selecciones + Jugadores (Capa 4); Cuotas depende de Partidos (Capa 5).

**7. ¿Cuál será la primera pieza a implementar?** **Selecciones** — es la entidad de Capa 0 de la que dependen más entidades aguas abajo (Jugadores, Partidos, Estadísticas, Convocatorias), tiene la mayor cobertura de campos confirmados (5 de 7), y no requiere que ninguna otra entidad exista primero.

**8. ¿La siguiente misión ya puede ser implementación?** **No todavía, sin condición.** Puede ser implementación **solo después** de que el Arquitecto Estadístico Humano resuelva la decisión pendiente de la pregunta 2 (`xg`) — de lo contrario, la primera ejecución real de `estadisticas_partido.csv` tropieza de inmediato con una contradicción de esquema no resuelta. La implementación de las entidades de Capa 0 (Selecciones, Estadios) sí podría comenzar sin esperar esa decisión, porque no involucran `xg`.

**9. ¿Qué riesgos quedan?** Los seis de la sección 11 — ninguno bloquea el diseño en sí, pero tres (`xg`, entidades bloqueadas, ENUMs sin formalizar) sí bloquean partes específicas de la implementación hasta resolverse.

**10. Confirmar que no hubo cambios en `app/`, `data/`, `models/` ni `knowledge/`.** **Confirmado.** Esta misión solo creó `docs/43-Pipeline-de-Ingesta.md` y actualizó `CHANGELOG.md`/`docs/00-Project-Tracker.md` — verificable con `git status`. No se escribió código Python, no se creó ningún CSV, no se consumió ninguna API, no se implementó ningún importador.

---

## 13. Referencias

- `docs/41-Verificacion-Tecnica-de-Fuentes.md` (`FII-003`) — evidencia de campo reutilizada sin reinvestigar
- `docs/42-Verificacion-Manual-API-Football.md` (`DATA-010A`) — evidencia de campo directa de fuente primaria, reutilizada sin reinvestigar
- `docs/40-Diagnostico-de-Fuentes-de-Datos.md` (`FII-002`) — estrategia de fuentes por nivel que este diseño implementa
- `docs/38-Protocolo-Oficial-Ingesta-Datos.md` (`MS-012`) — flujo de ingesta, reglas de aceptación/rechazo y auditoría, reutilizados sin contradecirlos
- `docs/33-Modelo-Fisico-PostgreSQL.md` (`DATA-005`) — esquema físico objetivo de las 10 entidades diseñadas aquí
- `docs/32-Modelo-Relacional-Oficial.md` (`DATA-004`) §7 — independencia de Equipo/Competición/Estadio/Árbitro, base del grafo de dependencias (sección 3)
- `docs/39-Fase-II.md` — Bloque D (Valor Esperado), afectado directamente por el hallazgo de `cuotas.csv` (sección 6.9)

---

Fin del documento.
