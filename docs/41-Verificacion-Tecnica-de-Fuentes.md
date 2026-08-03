# Verificación Técnica de las Fuentes de Datos Candidatas

**Archivo:** `docs/41-Verificacion-Tecnica-de-Fuentes.md`

**Misión:** FII-003 — Verificación Técnica de las Fuentes de Datos Candidatas

**Versión:** 1.0.0

**Estado:** Investigación técnica de dos fuentes externas — sin descargas, sin consumo real de API, sin CSV nuevos, sin código, sin modificación de `app/`/`engine/`/`data/`/`models/`/`knowledge/`.

---

## Nota de numeración

El brief permite explícitamente `docs/41-Verificacion-Tecnica-de-Fuentes.md` "o el siguiente número disponible si existe conflicto". Verificado antes de escribir: `docs/40-Diagnostico-de-Fuentes-de-Datos.md` (`FII-002`) es el último documento de la secuencia antes del especial `docs/99-Mapa-Maestro.md` — `docs/41` está libre, sin conflicto. No aplica ninguna renumeración.

---

## 1. Objetivo

`FII-002` concluyó, con evidencia de documentación pública y comparación funcional, que la estrategia candidata para expandir la Base de Conocimiento del Modelo Santiago es: StatsBomb (mantener, sin cambios) + **API-Football** (nueva) + **Football-Data.co.uk** (nueva, específica para `cuotas.csv`). Esta misión no vuelve a evaluar esa estrategia ni compara nuevas fuentes — verifica técnicamente, contra documentación oficial y datos crudos reales cuando fue posible, si esas dos fuentes concretas realmente ofrecen lo que `FII-002` asumió que ofrecían. Es un paso obligatorio antes de `DATA-010` (ingesta real), consistente con el principio de Justificación de Datos de `CLAUDE.md` y con `docs/38-Protocolo-Oficial-Ingesta-Datos.md`.

Ningún dato se incorpora todavía a `data/`.

---

## 2. Metodología

La investigación se dividió en dos verificaciones independientes, cada una documentada con sus fuentes citadas inline.

**Football-Data.co.uk** pudo verificarse **directamente contra el sitio y sus archivos crudos** (fetch HTTP real a `data.php`, `notes.txt`, y varios CSV de ejemplo de distintos países/temporadas). El nivel de confianza de esta parte del informe es **alto** — casi todas las afirmaciones citan texto verbatim de la fuente primaria.

**API-Football** presentó una limitación real, no anticipada por `FII-002`: **su sitio oficial (`api-football.com`) está protegido por Cloudflare y devolvió `HTTP 403` en todos los intentos de lectura automatizada directa** (`WebFetch` directo, proxy de lectura, y el navegador Chrome controlado no estaba disponible en esta sesión). En consecuencia, esa parte del informe se construyó combinando `WebSearch` (fragmentos que citan literalmente contenido oficial, incluyendo el propio blog de primera parte `api-football.com/news/post/*`) con **verificación cruzada independiente**: se repitieron dos búsquedas específicas (precios/límites, y existencia de `xG` en `/fixtures/statistics`) para confirmar consistencia entre fuentes antes de aceptar cualquier cifra. Donde la evidencia sigue siendo insuficiente tras esa verificación cruzada, se documenta explícitamente como **brecha de evidencia** en la sección 8, no como un hecho — exactamente el mismo principio de honestidad que ya aplicó `FII-002`. Ninguna cifra de este documento fue inventada ni extrapolada sin fuente.

---

## 3. API-Football — Verificación Técnica

### 3.1 Cobertura real

- **Selecciones nacionales:** confirmado con fuente oficial de primera parte — la guía "FIFA World Cup 2026: Guide to Using Data with API-SPORTS" (`api-football.com/news/post/...`) confirma cobertura de la fase final del Mundial 2026 (48 equipos, 16 estadios, sedes Canadá/México/EE.UU.), accesible ya en vivo vía `league=1&season=2026`.
- **Copas continentales (Copa América, AFCON, Asian Cup):** reportadas como cubiertas por fragmentos que remiten a `api-football.com/coverage`, pero sin poder leer esa página directamente. **Parcialmente confirmado.**
- **Eurocopa (UEFA Euro):** ninguna fuente consultada la confirmó explícitamente, pese a ser consistente con la cobertura declarada de +1.200 competiciones. **No confirmado con fuente primaria directa.**
- **Ligas/copas de clubes:** cifra repetida de forma consistente entre fuentes (~1.200 competiciones; una fuente secundaria da "1.236 ligas" en el plan gratuito), pero sin lectura directa de `/coverage` que la confirme verbatim. **Tratar como orden de magnitud, no como cifra oficial exacta.**
- **Profundidad histórica por competición según plan (free vs. pago):** el objeto `coverage` por temporada existe como parte documentada de la respuesta de `GET /leagues`, pero **no se pudo confirmar cuántas temporadas históricas concretas incluye el plan gratuito** frente a los de pago. Este es el punto de cobertura más crítico sin resolver — el proyecto necesita profundidad histórica real para calibrar Poisson/Elo, no solo la temporada en curso.

### 3.2 Endpoints disponibles (v3)

| Necesidad del brief | Endpoint confirmado | Estado |
|---|---|---|
| Partidos | `GET /fixtures` | Confirmado |
| Estadísticas del partido | `GET /fixtures/statistics?fixture={id}` | Confirmado |
| Alineaciones | `GET /fixtures/lineups` | Confirmado |
| Árbitros | — | **No es endpoint propio.** El árbitro llega como *string* de texto libre dentro del objeto `fixture` (ej. `"Kevin Friend, England"`), sin ID normalizado ni entidad estructurada propia. |
| Estadios | `GET /venues` | Confirmado, endpoint propio |
| Clima | — | **No confirmado que exista.** No aparece en ningún listado de campos ni como endpoint en ninguna fuente consultada. Todo indicio apunta a que API-Football **no ofrece dato de clima**. |
| Lesiones | `GET /injuries` | Confirmado (actualización cada 4 horas; campos `type` Injury/Suspension, `reason`) |
| Jugadores | `GET /players` + `GET /players/statistics` | Confirmado |
| Entrenadores | `GET /coachs` | Confirmado (incluye histórico de clubes con fechas) |
| Cuotas | `GET /odds` | Confirmado, endpoint separado |
| Eventos minuto a minuto | `GET /fixtures/events` | Confirmado (goles, tarjetas, sustituciones, con minuto) |
| — (adicional, no pedido por el brief) | `GET /players/squads` | Confirmado — plantilla actual de un club/selección, no "convocatoria a un torneo" con fecha/estado |
| — (adicional) | `GET /predictions` | Confirmado — algoritmo propio del proveedor, irrelevante para este proyecto (Modelo Santiago no consume predicciones de terceros) |

**Autenticación:** API REST estándar, JSON. Dos vías: directa (`v3.football.api-sports.io`, header `x-apisports-key`) o vía RapidAPI (`api-football-v1.p.rapidapi.com/v3`, headers `X-RapidAPI-Key`/`X-RapidAPI-Host`). Confirmado por consistencia entre múltiples fuentes de terceros con ejemplos de código.

### 3.3 Campos útiles — mapeo exacto contra el esquema físico ya definido en `docs/33-Modelo-Fisico-PostgreSQL.md`

**Nota de alcance:** el brief pide `equipos.csv`, pero el esquema real del proyecto no tiene esa entidad — el equivalente actual es `selecciones.csv` (selecciones nacionales; "equipos" de club pertenecerá a la Fase III, `docs/39` §7). Se documenta aquí como `selecciones.csv` para no inventar un archivo inexistente.

**`partidos.csv`** (`id_partido, id_torneo, id_seleccion_local, id_seleccion_visitante, id_estadio, id_arbitro, fecha, hora_local, fase, jornada, goles_local, goles_visitante, estado_partido, asistencia`):
- Cubiertos vía `/fixtures`: fecha, hora, selecciones local/visitante, fase/ronda, goles local/visitante, estado del partido.
- Cubierto vía `/venues` (relación por ID): estadio.
- **No cubierto como entidad con ID:** árbitro (string libre, sin normalizar — requeriría tabla de mapeo manual/heurística construida por el proyecto, no provista por la fuente).
- **No confirmado:** el campo `asistencia` (attendance) — ninguna fuente consultada confirmó su existencia en `/fixtures`.

**`estadisticas_partido.csv`** (`xg, posesion_pct, disparos_totales, disparos_al_arco, corners, faltas_cometidas, tarjetas_amarillas, tarjetas_rojas, pases_completados, precision_pases_pct`):
- Cubiertos vía `/fixtures/statistics` (post oficial "Match Facts" lista explícitamente: Ball Possession, Corner Kicks, Fouls, Yellow/Red Cards, Total passes, Passes accurate, Shots on/off Goal, Goalkeeper Saves): posesión, corners, faltas, tarjetas amarillas/rojas, pases (total y precisión aproximada), disparos totales/al arco.
- **`xg` — el campo más crítico del mapeo, sin confirmar.** El listado de tipos de estadística del post oficial "Match Facts" **no incluye "Expected Goals" ni "xG"** en ninguna búsqueda realizada, ni en la verificación cruzada específica hecha para este punto. No se pudo leer la documentación interactiva directamente (bloqueo Cloudflare) para descartarlo con certeza total, pero la ausencia es consistente en todas las fuentes consultadas. **Tratar como brecha de evidencia crítica, con indicio fuerte de ausencia real** — ver sección 8.

**`estadios.csv`** (`nombre, ciudad, pais, capacidad, tipo_superficie, altitud_metros, techado`):
- Cubiertos vía `/venues`: nombre, ciudad, país, capacidad, superficie.
- **No encontrados en ninguna fuente:** `altitud_metros`, `techado` (techo/domo).

**`selecciones.csv`** (equivalente real de "equipos.csv" en este proyecto — `nombre_pais, nombre_federacion, confederacion, ranking_fifa_actual, ranking_fifa_fecha, seleccionador_actual, activa`):
- `nombre_pais` cubierto vía `/teams` (filtro `type=national`).
- `seleccionador_actual` derivable vía `/coachs` (campo `team` del entrenador activo), no directo pero reconstruible.
- **No confirmados:** `nombre_federacion`, `confederacion`, `ranking_fifa_actual`/`ranking_fifa_fecha` — ninguna fuente consultada menciona un endpoint o campo de ranking FIFA en API-Football v3.

**`jugadores.csv`** (`nombre_completo, nombre_conocido, fecha_nacimiento, posicion_principal, pie_habil, altura_cm, club_actual`):
- Cubiertos vía `/players`: nombre, fecha de nacimiento, nacionalidad, altura, posición, club actual.
- **No confirmado:** `pie_habil` (preferred foot) — el único indicio encontrado correspondía a documentación de Sportmonks (competidor), no de API-Football; se descarta por posible confusión de fuentes en la búsqueda.

**`convocatorias.csv`** (`torneo, seleccion, jugador, dorsal, posicion_convocatoria, fecha_convocatoria, estado_convocatoria`):
- Existen dos endpoints relacionados pero **ninguno modela el concepto exacto que pide el esquema**: `/players/squads` da la plantilla *actual* de un club/selección (sin fecha ni torneo asociado), y `/fixtures/lineups` da la alineación *real* de un partido puntual (con dorsal y posición, pero solo de los que jugaron, no de toda la convocatoria). `fecha_convocatoria` y `estado_convocatoria` (convocado/lesionado/descartado) no existen como campos nativos — habría que derivarlos combinando `/players/squads` + `/injuries` + `/fixtures/lineups`, con trabajo de transformación no trivial a cargo del proyecto.

**Conclusión de esta subsección:** ningún archivo del esquema queda cubierto **COMPLETO** por API-Football; los cinco son, en el mejor caso, **PARCIAL** — ver tabla consolidada en la sección 6.

### 3.4 Límites

Confirmado con verificación cruzada independiente (dos búsquedas distintas devolvieron cifras idénticas, citando `api-football.com/pricing` y `api-football.com/news/post/how-ratelimit-works`):

| Plan | Precio/mes | Requests/día | Requests/minuto |
|---|---|---|---|
| Free | $0 | 100 | 10 |
| Pro | $19 | 7.500 | 300 (5/seg) |
| Ultra | $29 | 75.000 | 450 (7/seg) |
| Mega | $39 | 150.000 | 900 (15/seg) |

- El cupo diario del plan Free se reinicia a las 00:00 UTC; no se acumula.
- Reportado de forma consistente entre fuentes: **todos los planes, incluido Free, incluyen todas las competiciones y endpoints** — a diferencia de proveedores que segmentan cobertura por plan (ej. Football-Data.org, `FII-002` §3.3). Esto es una ventaja real si se confirma en la práctica.
- **No confirmado:** si el plan Free tiene alguna restricción adicional no relacionada con volumen (ej. delay en datos en vivo, límite de temporadas históricas accesibles). Los fragmentos disponibles son insuficientes para afirmar u descartar esto.

### 3.5 Automatización

- **Tipo de API:** REST estándar, JSON. Confirmado, patrón consistente en todas las fuentes.
- **SDK/librería oficial:** existe una organización oficial en GitHub (`github.com/api-sports`) con librerías en **Python** y **.NET/C#**, y una en Ruby. No se confirmó SDK oficial en Node.js/PHP (solo wrappers de terceros no oficiales).
- **Estabilidad:** existió una migración v2→v3 con cambios estructurales (reestructuración de campos de equipo local/visitante, nueva sintaxis de filtros). No se encontró evidencia de una fecha de deprecación de v2 específica de API-Football — una cifra encontrada en la investigación ("deprecado a fines de 2025") correspondía en realidad a **Sportmonks**, un competidor distinto, y se descarta explícitamente aquí para no repetir esa confusión de fuentes.
- **Quejas de fiabilidad documentadas:** no se encontró evidencia específica y verificable (foros, GitHub issues) sobre inconsistencia de datos de este proveedor en particular dentro del alcance de esta investigación. **No hay evidencia suficiente ni para afirmar ni para descartar** problemas de fiabilidad — se documenta como ausencia de evidencia, no como garantía de estabilidad.

---

## 4. Football-Data.co.uk — Verificación Técnica

Toda esta sección se verificó por fetch directo contra el sitio (`data.php`, `notes.txt`, y CSV crudos de Inglaterra, España, Alemania y Argentina).

### 4.1 Temporadas disponibles

- **Ligas principales (11 países):** Inglaterra, Escocia, Alemania, Italia, España, Francia, Países Bajos, Bélgica, Portugal, Turquía, Grecia — confirmado con fetch directo en tres de ellas (`englandm.php`, `spainm.php`, `germanym.php`): cobertura desde **1993/94** hasta la temporada en curso (**2025/26**), URL de ejemplo `mmz4281/9394/E0.csv` → `mmz4281/2526/E0.csv`.
- **Resultados básicos:** 25 temporadas (desde 1993/94). **Estadísticas de partido y cuotas:** 26 temporadas, pero solo **desde 2000/01** — confirmado textualmente en `data.php`. Es decir, para el rango 1993/94-1999/00 solo hay resultado, no estadísticas ni cuotas.
- **Actualización:** confirmado en `data.php` y `notes.txt` — al menos dos veces por semana (domingo y miércoles noche); cuotas se recolectan viernes por la tarde (partidos de fin de semana) y martes por la tarde (partidos entre semana).
- **Ligas "extra" (16 países adicionales — Argentina, Austria, Brasil, China, Dinamarca, Finlandia, Irlanda, Japón, México, Noruega, Polonia, Rumania, Rusia, Suecia, Suiza, EE.UU.):** un único CSV acumulativo por país (`new/{COD}.csv`), no por temporada. Verificado directamente en `new/ARG.csv`: son datos de clubes (Boca Juniors, River Plate, San Lorenzo), **nunca selecciones nacionales**. El rango de fechas exacto de este archivo específico no pudo confirmarse con precisión (limitación de la herramienta de lectura, no del sitio).

### 4.2 Formato

- **Archivo:** CSV plano (más copia en Excel), descarga directa por URL, **sin API key ni registro** — confirmado textualmente en `data.php` ("all FREE!!!") y empíricamente (fetch exitoso sin autenticación).
- **Patrón de URL — ligas principales (predecible, automatizable):** `football-data.co.uk/mmz4281/{temporada}/{division}.csv` (ej. `mmz4281/2526/E0.csv` = Premier League 25/26; códigos vistos: E0=Premier League, E1=Championship, E2=League 1, E3=League 2, EC=Conference, SP1/SP2=España).
- **Patrón de URL — ligas extra:** `football-data.co.uk/new/{COD}.csv` (archivo único acumulativo, no por temporada).
- **Riesgo operativo confirmado empíricamente durante esta misma investigación:** fetches consecutivos devolvieron **HTTP 429 (Too Many Requests)** tras solo 2-3 solicitudes en poco tiempo — rate-limiting real del servidor. Cualquier automatización futura debe espaciar solicitudes y usar backoff, algo compatible con la cadencia de actualización del propio sitio (2 veces/semana, sin necesidad de polling agresivo).

### 4.3 Variables (fuente: `notes.txt`, fetch verbatim)

- **Identificación de partido:** `Div`, `Date`, `Time`, `HomeTeam`, `AwayTeam`. Sin columna de temporada explícita (se infiere de la carpeta/URL), sin jornada/ronda, sin fase (liga round-robin).
- **Resultado:** `FTHG`/`FTAG` (goles FT), `FTR` (resultado), `HTHG`/`HTAG`/`HTR` (medio tiempo).
- **Estadísticas de partido:** `Attendance`, `Referee`, `HS`/`AS` (tiros), `HST`/`AST` (tiros a puerta), `HC`/`AC` (corners), `HF`/`AF` (faltas), `HY`/`AY` (amarillas), `HR`/`AR` (rojas) — todas **solo desde ~2000/01, ausentes en temporadas anteriores y en la mayoría de las ligas "extra"**.
- **Cuotas — 1X2:** ~18 casas de apuestas identificables por código de columna (Bet365 `B365H/D/A`, Pinnacle `PSH/D/A`, William Hill `WHH/D/A`, Betfair `BFH/D/A`, Interwetten, Ladbrokes, Bet&Win, etc.), más agregados de mercado `MaxH/D/A`/`AvgH/D/A` (máximo/promedio).
- **Cuotas — Over/Under 2.5 goles y Hándicap Asiático:** cubiertos con columnas equivalentes por casa (`B365>2.5`, `PAHH/A`, etc.); el hándicap asiático de mercado (`AHh`) existe **desde 2019/20** (confirmado textualmente en `notes.txt`).
- **Cuotas de cierre:** confirmado textualmente en `notes.txt` — sufijo `C` tras el código de casa (ej. `B365CH`).
- **Formato de cuota:** decimal — confirmado con confianza razonable (consistente en columnas crudas y en múltiples fuentes de terceros), aunque `notes.txt` no lo declara de forma verbatim.
- **Confirmado explícitamente, no asumido:** **no existe ninguna columna de xG, posesión %, pases completados/precisión, estadio, ni ningún dato de jugador o plantilla** en `notes.txt` — la fuente no ofrece estadísticas avanzadas ni datos de jugadores bajo ningún concepto.
- **Confirmado explícitamente:** **ninguna de las 27 competiciones cubiertas (11 principales + 16 extra) es de selecciones nacionales** — todas son ligas domésticas de clubes.

### 4.4 Facilidad de integración

- **Automatización:** dificultad baja para las ligas principales — patrón de URL 100% predecible, sin autenticación, formato estable en las tres décadas verificadas (1993/94-2025/26, mismo esquema de carpetas en Inglaterra/España/Alemania).
- **Riesgo real detectado:** rate-limiting del servidor (HTTP 429, confirmado empíricamente — ver 4.2) y **evolución del conjunto de columnas a lo largo del tiempo** (ej. `AHh` solo desde 2019/20, sufijo de cierre `C` añadido después) — un parser debe tolerar columnas ausentes/adicionales por temporada, no asumir un esquema fijo.
- **Estabilidad histórica:** 25+ años con el mismo dominio y convención de carpetas es una señal fuerte para un proveedor gratuito, pero **sin ningún SLA ni compromiso contractual de continuidad** — es un operador único sin garantías formales.

### 4.5 Licencia

- **Sin términos de uso explícitos sobre uso comercial, redistribución o atribución** — verificado en la home page y en `disclaimer.php`. Solo existe un aviso de copyright genérico ("© Football-Data. All Rights Reserved") y descargos de responsabilidad relacionados con apuestas/juego responsable, sin ninguna cláusula de licencia de datos.
- Modelo de negocio declarado: afiliación de apuestas (ingresos por publicidad de casas de apuestas) — relevante para entender el sesgo del sitio, no para licenciamiento.
- **Conclusión:** sin declaración de dominio público ni permiso expreso de redistribución. El proyecto debería tratar el uso bajo un criterio de precaución razonable (uso no comercial/analítico, atribución como buena práctica) hasta que el Arquitecto Estadístico Humano fije el criterio de riesgo aceptable — decisión de gobernanza, no un hallazgo técnico adicional.

---

## 5. Comparación directa

**¿Qué ofrece una que la otra no?**
- **API-Football, exclusivo:** selecciones nacionales (incluido Mundial 2026 confirmado), API REST en vivo/automatizable con estructura de IDs normalizados, endpoints de jugadores/entrenadores/lesiones/alineaciones — todo lo que Football-Data.co.uk no tiene en absoluto.
- **Football-Data.co.uk, exclusivo:** cuotas históricas de ~18 casas de apuestas desde 2000/01 (mercado 1X2, Over/Under, hándicap asiático, cuotas de apertura y de cierre) — API-Football también tiene endpoint de cuotas (`/odds`), pero sin profundidad histórica confirmada ni la variedad de casas que Football-Data.co.uk documenta explícitamente.

**¿Qué falta en ambas?**
- **xG confiable:** API-Football no lo confirma como campo (indicio fuerte de ausencia); Football-Data.co.uk no lo tiene bajo ningún concepto. Ninguna de las dos alcanza el nivel de dato de evento de StatsBomb.
- **Estadio como entidad normalizada con altitud/techado:** ausente en ambas (API-Football tiene estadio pero sin esos dos campos; Football-Data.co.uk no tiene estadio en absoluto).
- **Convocatoria a torneo con fecha/estado:** ninguna de las dos modela ese concepto de forma nativa.
- **Datos de jugadores/plantillas:** ausentes por completo en Football-Data.co.uk (no es su alcance); parcialmente cubiertos en API-Football pero con al menos un campo no confirmado (`pie_habil`).

**¿Cuál sería la fuente primaria?** **API-Football** — es la única de las dos que cubre selecciones nacionales, el foco actual del proyecto (`data/processed/selecciones-nacionales/`); Football-Data.co.uk no puede ser primaria porque no tiene ningún dato de selecciones.

**¿Cuál sería la secundaria?** **Football-Data.co.uk**, exclusivamente para `cuotas.csv` (Bloque D, Valor Esperado) — su cobertura de mercado gratuita, histórica y bien documentada no tiene comparación en API-Football sin verificar el plan/costo real de su endpoint `/odds`.

---

## 6. Compatibilidad con el Modelo Santiago

| Archivo | API-Football | Football-Data.co.uk | Fuente(s) que lo completaría |
|---|---|---|---|
| `partidos.csv` | **PARCIAL** — falta `id_arbitro` normalizado (string libre) y `asistencia` no confirmada | **NO aplica a selecciones** (solo ligas de clubes); si el alcance se ampliara a clubes en Fase III, sería PARCIAL (sin IDs normalizados de equipo, sin estadio, sin fase/jornada) | Ninguna de las dos por sí sola; requiere normalización manual de árbitro en API-Football |
| `estadisticas_partido.csv` | **PARCIAL** — falta `xg` (brecha crítica, ver sección 8), `posesion_pct`/`corners`/`faltas`/`tarjetas`/`pases` sí cubiertos | **NO aplica a selecciones**; para clubes sería PARCIAL (tiros/corners/faltas/tarjetas desde 2000/01, sin xG ni posesión ni pases) | Ninguna cubre xG — seguiría dependiendo de StatsBomb donde tenga cobertura |
| `estadios.csv` | **PARCIAL** — falta `altitud_metros` y `techado` | **NO** — sin ninguna columna de estadio | Ninguna de las dos completa este archivo por sí sola |
| `jugadores.csv` | **PARCIAL** — falta `pie_habil` (no confirmado) | **NO** — sin datos de jugadores | API-Football, con ese único campo pendiente de verificar |
| `convocatorias.csv` | **PARCIAL, con transformación no trivial** — requiere combinar `/players/squads` + `/injuries` + `/fixtures/lineups`; sin campos nativos de `fecha_convocatoria`/`estado_convocatoria` | **NO** — sin datos de plantillas | Ninguna de las dos lo resuelve de forma directa |
| `cuotas.csv` (fuera del alcance de los 5 archivos del brief, pero relevante para el Bloque D) | Endpoint `/odds` existe, profundidad/costo real no verificados | **La más completa de las dos** — ~18 casas, 1X2/O-U/hándicap asiático, apertura y cierre, desde 2000/01 | Football-Data.co.uk es la recomendación clara para este archivo |

**Ningún archivo del esquema queda COMPLETO con ninguna de las dos fuentes.** Todos quedan, en el mejor caso, PARCIAL — algunos con brechas menores (verificación pendiente de un campo puntual) y uno con una brecha estructural real (`xg`, el campo de mayor peso matemático del esquema de estadísticas).

---

## 7. Riesgos

- **Dependencia de un solo operador sin SLA:** ambas fuentes son operadas por terceros sin garantía contractual de continuidad — API-Football es un producto comercial con historial de migración de versión (v2→v3); Football-Data.co.uk es un proyecto de un operador único, sin respaldo corporativo, cuyo modelo de negocio es afiliación de apuestas (riesgo de cierre si ese modelo deja de ser rentable para el operador).
- **Cambios de API:** API-Football ya tuvo al menos una migración estructural (v2→v3); no hay evidencia de una fecha de deprecación anunciada para v3, pero el precedente existe.
- **Licencia:** Football-Data.co.uk no publica términos de licencia de datos — riesgo de gobernanza, no técnico, que requiere una decisión explícita del Arquitecto Estadístico Humano antes de cualquier uso más allá de investigación/backtesting interno.
- **Rate limiting real, confirmado empíricamente en ambas fuentes durante esta misma investigación:** Football-Data.co.uk devolvió HTTP 429 tras pocas solicitudes; API-Football declara límites duros por plan (100 req/día en Free). Cualquier pipeline de ingesta debe diseñarse con estos límites como restricción dura desde el inicio, no como un detalle de implementación tardío.
- **Estabilidad de esquema:** Football-Data.co.uk confirmó al menos dos cambios de columnas a lo largo de su historia (`AHh` desde 2019/20, sufijo `C` de cierre) — cualquier parser debe tolerar esquema variable por temporada.
- **Mantenimiento/dependencia externa:** ninguna de las dos fuentes está bajo control del proyecto; ambas requieren monitoreo continuo de cambios de estructura si se automatiza la ingesta.

---

## 8. Brechas de evidencia — pendientes de verificación manual antes de cerrar `DATA-010`

Estas seis brechas no pudieron resolverse con las herramientas de lectura automatizada de solo lectura disponibles en esta misión (bloqueo Cloudflare del sitio de API-Football). Requieren que un humano (o una sesión con navegador autenticado) abra la documentación interactiva de API-Football directamente:

1. **Existencia real del campo `xg` en `/fixtures/statistics`** — el hallazgo de mayor peso de todo este informe, y el que más condiciona la decisión de adopción. Indicio fuerte de ausencia, sin confirmación ni descarte definitivo.
2. **Profundidad histórica exacta de temporadas por plan** (Free vs. Pro/Ultra/Mega) — crítico porque el proyecto necesita histórico real para calibrar Poisson/Elo, no solo la temporada en curso.
3. **Cobertura confirmada de Eurocopa (UEFA Euro)** en el listado oficial de `/coverage`.
4. **Confirmación textual exacta de precios/límites** leyendo `/pricing` directamente (los números de la sección 3.4 tienen buen respaldo indirecto y verificación cruzada, pero no lectura directa de la fuente primaria).
5. **Existencia del campo `asistencia`** (attendance) en `/fixtures`.
6. **Restricciones adicionales del plan Free** más allá del límite de 100 req/día (delay en datos en vivo, límite de temporadas históricas accesibles).

**Recomendación operativa:** dado que API-Football ofrece un plan gratuito sin tarjeta de crédito (100 req/día, confirmado en la sección 3.4), la forma más directa de cerrar estas seis brechas es registrar una cuenta gratuita y consultar la documentación interactiva y un par de llamadas de prueba — una acción que **excede el alcance de esta misión** (`Restricciones`: no consumir APIs, no crear código) y debe ejecutarse como el primer paso de `DATA-010`, no como parte de `FII-003`.

---

## 9. Cierre obligatorio

**1. ¿API-Football cumple realmente lo prometido?** **Parcialmente.** Confirma con solidez razonable la cobertura de selecciones (incluido Mundial 2026, con fuente oficial de primera parte), una API REST moderna y fácil de automatizar, y precios/límites consistentes entre fuentes cruzadas. Pero tiene una brecha crítica sin resolver — la existencia de `xg`, el campo más importante del esquema de estadísticas de partido — y varias brechas menores (árbitro sin ID, asistencia, altitud/techado de estadio, pie hábil) que `FII-002` no había detectado porque no llegó al nivel de campo individual.

**2. ¿Football-Data.co.uk cumple realmente lo prometido?** **Sí, dentro de su alcance ya conocido.** `FII-002` lo describió como "la única fuente gratuita con cuotas históricas" — esta verificación lo confirma con evidencia directa (notes.txt, ~18 casas, tres mercados, desde 2000/01) y no encontró ninguna sorpresa negativa: sigue sin selecciones, sigue sin xG/posesión/pases, sigue sin datos de jugadores/estadios — exactamente como `FII-002` ya documentaba. Es la fuente que mejor cumplió su promesa original, precisamente porque su promesa siempre fue acotada.

**3. ¿Cuál cubriría mejor el Modelo Santiago?** Ninguna por sí sola. API-Football es indispensable para el foco actual (selecciones) pero con una brecha crítica en `xg`; Football-Data.co.uk no aporta nada a selecciones y solo sirve para `cuotas.csv`. Se necesitan ambas, cada una para un propósito distinto y no superpuesto — consistente con la estrategia de niveles ya recomendada en `FII-002`.

**4. ¿Cuál debería ser la fuente primaria?** **API-Football** — es la única candidata nueva con cobertura de selecciones nacionales.

**5. ¿Cuál debería ser la fuente secundaria?** **Football-Data.co.uk** — exclusivamente para `cuotas.csv` (Bloque D), nunca como sustituto de estadísticas de partido de selecciones.

**6. ¿Qué información seguiría faltando?** xG confiable (ninguna de las dos lo ofrece con certeza); estadio como entidad completa (altitud, techado); convocatoria a torneo con fecha/estado; pie hábil de jugador; Eliminatorias CONMEBOL (ya documentado como hueco estructural en `FII-002`, sin cambios aquí).

**7. ¿Existen limitaciones críticas?** Sí, dos: (a) el campo `xg` de API-Football no pudo confirmarse y hay indicio fuerte de que no existe — condiciona directamente la calidad de `estadisticas_partido.csv`; (b) el sitio de API-Football bloqueó toda lectura automatizada durante esta investigación (Cloudflare), lo que impidió cerrar seis puntos de evidencia (sección 8) sin intervención humana o de una cuenta autenticada.

**8. ¿Se recomienda oficialmente adoptar estas fuentes para `DATA-010`?** **Recomendación condicionada, no un "sí" incondicional.** Football-Data.co.uk puede adoptarse ya para `cuotas.csv` sin verificación adicional — la evidencia directa de esta misión es suficiente. API-Football **no debe comprometerse a una integración de ingesta completa todavía** sin que un ser humano (o una sesión con navegador autenticado) cierre primero las seis brechas de la sección 8, en particular la existencia de `xg` — adoptar la fuente sin resolver eso arriesga construir un pipeline de ingesta alrededor de un campo que podría no existir.

**9. ¿Qué misión debe ejecutarse inmediatamente después?** `DATA-010`, pero redefinida en dos pasos secuenciales en lugar de uno: **Paso 1** — registrar una cuenta gratuita de API-Football y cerrar manualmente las seis brechas de la sección 8 (sin ingesta masiva todavía, solo confirmación de documentación/muestra); **Paso 2**, solo si el Paso 1 confirma `xg` y profundidad histórica suficientes — diseño del protocolo de ingesta real siguiendo `docs/38-Protocolo-Oficial-Ingesta-Datos.md`.

**10. ¿La evidencia obtenida es suficiente para iniciar la expansión real de la Base de Conocimiento durante la Fase II?** **Suficiente para Football-Data.co.uk, no todavía para API-Football.** Iniciar una integración de ingesta de API-Football sin resolver la brecha de `xg` contradice el Principio de Justificación de Datos de `CLAUDE.md` ("si la información disponible no es suficiente, indíquelo claramente antes de continuar") — este documento lo indica explícitamente en vez de asumir que la fuente cumple.

---

## 10. Referencias

- [API-Football — Documentación v3](https://www.api-football.com/documentation-v3) *(bloqueado por Cloudflare durante esta investigación — no se pudo leer directamente, ver sección 2)*
- [API-Football — Pricing](https://www.api-football.com/pricing) *(ídem — verificado por cruce de `WebSearch`, no lectura directa)*
- [API-Football — Coverage](https://www.api-football.com/coverage) *(ídem)*
- [API-Football — FIFA World Cup 2026 Guide](https://www.api-football.com/news/post/fifa-world-cup-2026-guide-to-using-data-with-api-sports) — única página oficial cuyo contenido se confirmó vía fragmentos textuales citados por múltiples búsquedas independientes
- [API-Football — Match Facts (fixture statistics)](https://www.api-football.com/news/post/match-facts)
- [API-Football — How Ratelimit Works](https://www.api-football.com/news/post/how-ratelimit-works)
- [API-Football — Players Squads endpoint](https://www.api-football.com/news/post/football-players-squads)
- [API-Football — New Endpoint Injuries](https://www.api-football.com/news/post/new-endpoint-injuries)
- [API-Sports — GitHub organization](https://github.com/api-sports)
- [Football-Data.co.uk — data.php](https://www.football-data.co.uk/data.php) — fetch directo
- [Football-Data.co.uk — notes.txt](https://www.football-data.co.uk/notes.txt) — fetch directo, verbatim
- [Football-Data.co.uk — englandm.php](https://www.football-data.co.uk/englandm.php) — fetch directo
- [Football-Data.co.uk — spainm.php](https://www.football-data.co.uk/spainm.php) — fetch directo
- [Football-Data.co.uk — germanym.php](https://www.football-data.co.uk/germanym.php) — fetch directo
- [Football-Data.co.uk — all_new_data.php](https://www.football-data.co.uk/all_new_data.php) — fetch directo
- [Football-Data.co.uk — disclaimer.php](https://www.football-data.co.uk/disclaimer.php) — fetch directo
- CSV crudos verificados directamente: `mmz4281/2526/E0.csv`, `mmz4281/9394/E0.csv`, `mmz4281/1920/E1.csv`, `new/ARG.csv`
- `docs/40-Diagnostico-de-Fuentes-de-Datos.md` (`FII-002`) — diagnóstico funcional que esta misión verifica técnicamente
- `docs/33-Modelo-Fisico-PostgreSQL.md` (`DATA-005`) — esquema físico oficial contra el que se mapeó cada campo
- `docs/38-Protocolo-Oficial-Ingesta-Datos.md` — protocolo que gobernará `DATA-010`

---

Fin del documento.
