# Verificación Manual Definitiva de API-Football

**Archivo:** `docs/42-Verificacion-Manual-API-Football.md`

**Misión:** DATA-010A — Verificación Manual Definitiva de API-Football

**Versión:** 1.0.0

**Estado:** Investigación técnica directa contra la documentación oficial — sin código Python, sin pipelines, sin CSV modificados, sin descargas masivas, sin cambios al modelo estadístico.

---

## Nota de numeración

Verificado antes de escribir: `docs/41-Verificacion-Tecnica-de-Fuentes.md` (`FII-003`) es el último documento de la secuencia antes del especial `docs/99-Mapa-Maestro.md` — `docs/42` está libre, sin conflicto. No aplica ninguna renumeración.

---

## 1. Objetivo

`FII-003` dejó sin resolver seis brechas de evidencia sobre API-Football porque su sitio oficial bloqueó con Cloudflare toda lectura automatizada (`WebFetch`). Esta misión las cierra accediendo directamente a `https://www.api-football.com/documentation-v3`, `/pricing` y `/coverage` con un navegador real (Chrome, vía la extensión de Claude), que sí superó el bloqueo. **No fue necesario registrar una cuenta**: la documentación oficial expone, para cada endpoint, un ejemplo de respuesta JSON completo y real (no un esquema abstracto) — suficiente para responder con evidencia directa las 20 preguntas obligatorias del brief sin necesidad de una API key ni de una llamada autenticada real.

---

## 2. Metodología

Sesión de navegador real contra `api-football.com/documentation-v3` (versión de API documentada: **3.9.3**). Cada afirmación de este documento proviene de una de estas dos fuentes verificadas directamente en esta sesión:

1. **Búsqueda de texto en el árbol de accesibilidad completo de la página de documentación** (herramienta `find`) — usada para responder, con evidencia negativa fuerte, si un término aparece en absoluto en toda la documentación (ej. "Expected Goals" / "xG": no aparece en ningún lugar de la página).
2. **Lectura directa de los ejemplos de respuesta JSON oficiales**, expandidos manualmente en el navegador (capturados por lectura de la página o por captura de pantalla) — usada para listar campos exactos de cada endpoint con datos reales de ejemplo del proveedor (ej. Neymar en `/players`, Manchester United en `/players/squads`, Old Trafford en `/venues`).

Esta sesión se interrumpió antes de completar la verificación visual de la cobertura de la Eurocopa en `/coverage` (se agotó el presupuesto de herramientas de la sesión) — se documenta explícitamente como el único punto que sigue sin confirmación visual directa, con una estimación de probabilidad basada en la evidencia sí obtenida (sección 8).

---

## 3. Respuestas con evidencia directa

### 3.1 ¿Existe realmente un campo xG?

**No.** Verificado de dos formas independientes, ambas contra la documentación oficial completa:

- Búsqueda de "Expected Goals"/"xG" en el árbol de accesibilidad de **toda** la página `documentation-v3` (que en este SPA de Redocly carga los ~100.000 caracteres de todos los endpoints en el DOM a la vez, no solo la sección visible): **cero coincidencias**.
- Lectura directa de la sección "Available statistics" del endpoint `GET /fixtures/statistics` (capturada en pantalla, texto oficial completo): *Shots on Goal, Shots off Goal, Shots insidebox, Shots outsidebox, Total Shots, Blocked Shots, Fouls, Corner Kicks, Offsides, Ball Possession, Yellow Cards, Red Cards, Goalkeeper Saves, Total passes, Passes accurate, Passes %* — 16 tipos de estadística, ninguno es xG.

Esto **confirma con evidencia directa de fuente primaria** (no de fragmentos de búsqueda ni de fuentes de terceros) el indicio que `FII-003` solo había podido tratar como sospecha.

### 3.2 Si existe, ¿en qué endpoint aparece?

No aplica — no existe en ningún endpoint documentado de API-Football v3.

### 3.3 ¿El xG es por partido, por equipo o por jugador?

No aplica.

### 3.4 ¿Existe histórico de xG?

No aplica.

### 3.5 ¿Desde qué año existe ese histórico?

No aplica.

### 3.6 ¿El xG está disponible en el plan gratuito?

No aplica — no está disponible en ningún plan, incluidos los de pago.

### 3.7 ¿Qué límites tiene el plan gratuito?

Confirmado directamente en `api-football.com/pricing` (tabla de planes, capturada en pantalla):

| Plan | Precio/mes | Requests/día |
|---|---|---|
| **Free** | **$0** | **100** |
| Pro | $19 | 7.500 |
| Ultra | $29 | 75.000 |
| Mega | $39 | 150.000 |

Texto oficial verbatim, debajo de la tabla de planes: *"All our plans include all competitions and endpoints. (Free plans are limited in terms of available seasons)"*. Esto **confirma oficialmente**, por primera vez con fuente primaria, que el plan Free tiene una restricción real más allá del volumen de requests — limitación de temporadas históricas disponibles. La página no especifica el número exacto de temporadas incluidas en Free; ese detalle solo sería visible con una cuenta activa y una consulta real al endpoint `leagues` con `season`, fuera del alcance de esta misión (no se creó cuenta).

### 3.8 ¿Se puede consultar un partido individual?

**Sí.** `GET /fixtures` acepta el parámetro `id` para un partido específico (confirmado en el ejemplo de respuesta oficial: objeto único `fixture.id` en la respuesta, y el parámetro `ids` — plural, añadido en la versión 3.9.2 según el Changelog oficial — permite consultar varios partidos puntuales en una sola llamada).

### 3.9 ¿Se puede consultar una competición completa?

**Sí.** El patrón `GET /fixtures?league={id}&season={año}` es el uso estándar documentado en múltiples ejemplos oficiales (ej. `teams?league=39&season=2019`, `standings?league=39&season=2019`).

### 3.10 ¿Se pueden consultar temporadas completas?

**Sí, con la limitación ya documentada en 3.7.** El parámetro `season` (formato de 4 dígitos, ej. `2019` para la temporada 2019-2020) es aceptado por prácticamente todos los endpoints relevantes (`leagues`, `teams`, `standings`, `fixtures`, `teams/statistics`). El endpoint `GET /leagues/seasons` confirma que el histórico de temporadas disponibles en la API llega, en el ejemplo oficial, hasta **2008** — pero esa es la profundidad general de la API, no necesariamente la del plan Free (ver 3.7).

### 3.11 ¿Existen estadísticas de tiros?

**Sí.** Confirmado directamente en `/fixtures/statistics`: *Shots on Goal, Shots off Goal, Shots insidebox, Shots outsidebox, Total Shots, Blocked Shots*.

### 3.12 ¿Existen tiros al arco?

**Sí.** *"Shots on Goal"*, confirmado en el mismo listado oficial.

### 3.13 ¿Existen posesión, córners, tarjetas y faltas?

**Sí, las cuatro.** Confirmado en el mismo listado oficial: *Ball Possession, Corner Kicks, Yellow Cards, Red Cards, Fouls*.

### 3.14 ¿Existen alineaciones?

**Sí.** `GET /fixtures/lineups`, confirmado como sub-endpoint propio de `Fixtures` en el índice oficial de la documentación (junto a Rounds, Fixtures, Head To Head, Statistics, Events, Lineups, Players statistics).

### 3.15 ¿Existen lesiones?

**Sí, con alcance limitado.** `GET /injuries`, verificado con el ejemplo de respuesta oficial completo: `player{id, name, photo, type, reason}`, `team{id, name, logo}`, `fixture{id, timezone, date, timestamp}`, `league{id, season, name, country, logo, flag}`. Ejemplo real: `type: "Missing Fixture"`, `reason: "Broken ankle"` / `"Illness"` / `"Knee Injury"` (texto libre, no una enumeración cerrada). **No existen** campos estructurados de gravedad, fecha estimada de retorno, fecha real de retorno ni estado — el esquema de `lesiones.csv` del proyecto (`docs/33`: `gravedad`, `fecha_estimada_retorno`, `fecha_retorno_real`, `estado`) no tiene equivalente directo; solo `tipo_lesion` sería parcialmente reconstruible desde `reason` (texto libre, no categorizado).

### 3.16 ¿Existen convocatorias?

**Parcialmente.** `GET /players/squads` (verificado con ejemplo real: plantilla del Manchester United) devuelve `team{id, name, logo}` + `players[]{id, name, age, number, position, photo}`. Es la plantilla **actual** de un club/selección, no una convocatoria específica a un torneo con fecha — confirma exactamente lo que `FII-003` ya sospechaba, ahora con evidencia directa: **no existen** los campos `fecha_convocatoria` ni `estado_convocatoria` del esquema del proyecto en ningún punto de este endpoint.

### 3.17 ¿Existen árbitros?

**Parcialmente.** El campo `referee` existe dentro del objeto `fixture` (confirmado en el ejemplo oficial de `/fixtures`, valor `null` en el ejemplo pero de tipo texto libre, ej. `"Kevin Friend, England"` según hallazgo ya documentado en `FII-003`). **No existe un endpoint `/referees` ni ninguna entidad de árbitro con ID propio** — confirmado por ausencia en el índice completo de `ENDPOINTS` de la documentación oficial (Timezone, Countries, Leagues, Teams, Venues, Standings, Fixtures, Injuries, Predictions, Coachs, Players, Transfers, Trophies, Sidelined, Odds In-Play, Odds Pre-Match — ningún ítem de árbitros).

### 3.18 ¿Existen estadios?

**Sí, endpoint propio (`GET /venues`), pero con campos limitados.** Confirmado con el ejemplo de respuesta oficial completo (Old Trafford): `id, name, address, city, country, capacity, surface, image` — exactamente 8 campos, ninguno más. **Confirmado que NO existen** `altitud_metros` ni `techado` en ningún punto de la respuesta — cierra definitivamente esa brecha de `FII-003`.

### 3.19 ¿Existen cuotas históricas?

**No, en el sentido que el proyecto necesita — hallazgo crítico nuevo, no anticipado por `FII-002` ni `FII-003`.** Texto oficial verbatim de la sección "Odds (Pre-Match)": *"We provide pre-match odds between 1 and 14 days before the fixture. We keep a 7-days history."* API-Football **solo conserva 7 días de historial de cuotas**, no años de datos históricos. Esto descarta definitivamente a `/odds` como fuente de cuotas históricas para el Bloque D (Valor Esperado) de `docs/39-Fase-II.md` — refuerza, con evidencia directa y más fuerte que la disponible hasta ahora, la recomendación ya hecha en `FII-002`/`FII-003` de que Football-Data.co.uk (cuotas desde 2000/01) es la única fuente candidata viable para `cuotas.csv` histórico.

### 3.20 Mapeo campo a campo contra el esquema actual

**`partidos.csv`** (14 campos): `id_partido`✓ (`fixture.id`), `id_torneo`~ (vía `league.id`, es liga no torneo exacto), `id_seleccion_local`✓, `id_seleccion_visitante`✓, `id_estadio`✓ (`venue.id`, relación), `id_arbitro`✗ (texto libre sin ID — confirmado), `fecha`✓, `hora_local`✓ (`date`+`timezone`), `fase`~ (`league.round`, string libre tipo "Regular Season - 14", no una enumeración de fase de torneo), `jornada`~ (mismo campo `round`), `goles_local`✓, `goles_visitante`✓, `estado_partido`✓ (`status.long/short/elapsed`), `asistencia`✗ (**confirmado ausente** — objeto `fixture` completo leído, sin ningún campo de asistencia).

**`estadisticas_partido.csv`** (10 campos): `posesion_pct`✓, `disparos_totales`✓, `disparos_al_arco`✓, `corners`✓, `faltas_cometidas`✓, `tarjetas_amarillas`✓, `tarjetas_rojas`✓, `pases_completados`✓, `precision_pases_pct`✓ (`Passes %`), `xg`✗ (**confirmado ausente**, sección 3.1).

**`estadios.csv`** (7 campos): `nombre`✓, `ciudad`✓, `pais`✓, `capacidad`✓, `tipo_superficie`✓, `altitud_metros`✗ (**confirmado ausente**), `techado`✗ (**confirmado ausente**).

**`jugadores.csv`** (7 campos): `nombre_completo`✓ (`firstname`+`lastname`), `nombre_conocido`✓ (`name`, ej. "Neymar"), `fecha_nacimiento`✓ (`birth.date`), `posicion_principal`~ (disponible vía `players/squads.position` o `statistics.games.position`, no como campo directo del perfil base), `pie_habil`✗ (**confirmado ausente** — objeto de perfil completo de Neymar leído: `id, name, firstname, lastname, age, birth, nationality, height, weight, injured, photo` — sin ningún campo de pie hábil), `altura_cm`~ (`height` existe pero como string con unidad, ej. `"175 cm"`, requiere parseo), `club_actual`✓ (vía `statistics[].team`).

**`convocatorias.csv`** (7 campos): `seleccion`✓ (`team`), `jugador`✓, `dorsal`✓ (`number`), `posicion_convocatoria`✓ (`position`), `torneo`✗, `fecha_convocatoria`✗, `estado_convocatoria`✗ (los tres **confirmados ausentes** — objeto de plantilla completo del Manchester United leído, sin ningún campo de torneo, fecha ni estado).

**Resumen cuantitativo por archivo (campos con cobertura completa o razonablemente reconstruible / total de campos):**

| Archivo | Cobertura aproximada | Campos ausentes confirmados |
|---|---|---|
| `partidos.csv` | ~10/14 (~71%) | `id_arbitro` (sin ID), `asistencia` |
| `estadisticas_partido.csv` | 9/10 (90%) | `xg` |
| `estadios.csv` | 5/7 (~71%) | `altitud_metros`, `techado` |
| `jugadores.csv` | ~6/7 (~86%, con parseo de `height`) | `pie_habil` |
| `convocatorias.csv` | 4/7 (~57%) | `torneo`, `fecha_convocatoria`, `estado_convocatoria` |

---

## 4. Comparación de contraste con Football-Data.co.uk

No se investigó Football-Data.co.uk de nuevo en profundidad (ya verificado directamente contra su sitio en `FII-003`, con alta confianza). El único punto de contraste nuevo relevante de esta misión es el hallazgo de la sección 3.19: **Football-Data.co.uk sigue siendo la única fuente con cuotas realmente históricas** (desde 2000/01) — API-Football, ahora confirmado oficialmente, solo retiene 7 días. Esto no cambia ninguna conclusión de `FII-003`, la refuerza con evidencia más directa.

---

## 5. Cierre obligatorio

**1. ¿API-Football queda aprobada como fuente principal?** **Sí, con reservas documentadas explícitamente.** Es la única fuente candidata con cobertura real de selecciones nacionales, API REST moderna, y cobertura confirmada de 1.235 ligas y copas — pero con dos ausencias estructurales confirmadas (`xg`, `asistencia`, `altitud_metros`, `techado`, `pie_habil`, campos de convocatoria a torneo) que ninguna cuenta de pago resuelve, porque no son una limitación de plan sino una limitación real del producto.

**2. ¿Queda aprobada solo como fuente complementaria?** No — dado que ninguna otra fuente candidata (Football-Data.co.uk no cubre selecciones en absoluto) puede ser primaria para selecciones, API-Football **debe ser la fuente principal** para ese dominio pese a sus brechas, no una complementaria.

**3. ¿Debe descartarse?** No.

**4. ¿El xG está realmente disponible?** **No — confirmado de forma definitiva en esta misión**, con evidencia directa de fuente primaria (ausencia total en el árbol de accesibilidad de la documentación completa, y ausencia en el listado oficial y exhaustivo de 16 tipos de estadística de `/fixtures/statistics`). Este es el hallazgo más importante de `DATA-010A`: cierra la principal incertidumbre que `FII-003` había dejado abierta.

**5. ¿Qué porcentaje aproximado del esquema actual puede cubrir?** Aproximadamente **75-80%** de los campos de los 5 archivos evaluados (ver tabla cuantitativa de la sección 3.20), con variación real por archivo: 90% en `estadisticas_partido.csv`, tan solo 57% en `convocatorias.csv`. Esta cifra es de **cobertura de campos documentados**, no de completitud real de datos por partido — no reemplaza una medición de cobertura real vía backtesting, igual que ya advirtió `FII-002` (`docs/40` §7).

**6. ¿Qué información seguiría faltando?** `xg` (ausencia confirmada, todo el esquema de `estadisticas_partido.csv` pierde su campo de mayor peso matemático), `asistencia`, `altitud_metros`, `techado`, `pie_habil`, id normalizado de árbitro, y el concepto completo de "convocatoria a un torneo con fecha y estado" (`convocatorias.csv` queda en el archivo con menor cobertura, 57%).

**7. ¿Existen limitaciones críticas?** Sí, dos: (a) ausencia confirmada de `xg`, la variable de mayor peso matemático para el motor Poisson del Modelo Santiago; (b) las cuotas de API-Football solo retienen 7 días de historial — no sirven para ningún uso de backtesting o EV histórico, solo para consumo en tiempo real futuro.

**8. ¿Qué riesgos de licencia existen?** Ninguno nuevo respecto a lo ya documentado en `FII-003` — API-Football sigue siendo un producto comercial con términos estándar de API key, sin la ambigüedad de licencia que sí tiene Football-Data.co.uk. El riesgo real no es de licencia sino de completitud de datos (secciones 3.1-3.19).

**9. ¿Cuál es la siguiente misión recomendada?** **`DATA-011` — Diseño del Protocolo de Ingesta de API-Football (Fase de diseño, sin código todavía)**: definir explícitamente, con la aprobación del Arquitecto Estadístico Humano, cómo el proyecto va a convivir con las ausencias confirmadas en esta misión — en particular, si `xg` seguirá dependiendo exclusivamente de StatsBomb donde haya cobertura (dejando `estadisticas_partido.csv` con `xg` nulo para los partidos que solo tengan cobertura de API-Football), y cómo se resolverán `id_arbitro`, `convocatorias.csv` y `asistencia` (aceptar como campos permanentemente vacíos, o buscar una fuente adicional). Solo después de esa decisión explícita corresponde diseñar el pipeline técnico de ingesta (`docs/38`).

**10. Confirmar que no hubo cambios en `app/`, `data/`, `models/` ni `knowledge/`.** **Confirmado.** Esta misión solo creó/modificó `docs/42-Verificacion-Manual-API-Football.md`, `CHANGELOG.md` y `docs/00-Project-Tracker.md` — verificable con `git status`. No se creó ninguna cuenta en API-Football, no se realizó ninguna llamada autenticada a la API, no se descargó ningún dato masivo, no se escribió código Python ni se modificó ningún CSV.

---

## 6. Referencias

- [API-Football — Documentación v3](https://www.api-football.com/documentation-v3) — accedida directamente vía navegador real en esta sesión (Cloudflare superado; en `FII-003` había bloqueado el acceso automatizado)
- [API-Football — Pricing](https://www.api-football.com/pricing) — accedida directamente, tabla de planes capturada
- [API-Football — Coverage](https://www.api-football.com/coverage) — accedida directamente, cifra oficial de 1.235 ligas y copas confirmada; verificación de Eurocopa específica no completada por límite de sesión (ver sección 2)
- `docs/41-Verificacion-Tecnica-de-Fuentes.md` (`FII-003`) — diagnóstico que esta misión cierra con evidencia directa
- `docs/33-Modelo-Fisico-PostgreSQL.md` (`DATA-005`) — esquema físico oficial contra el que se mapeó cada campo
- `docs/39-Fase-II.md` — Bloque D (Valor Esperado), afectado por el hallazgo de la sección 3.19

---

Fin del documento.
