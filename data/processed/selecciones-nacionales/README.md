# Módulo: Selecciones Nacionales

**Directorio:** `data/processed/selecciones-nacionales/`

**Versión:** 1.12.0

**Estado:** Activo (esquema aprobado; `selecciones.csv`, `competiciones.csv`, `estadios.csv`, `arbitros.csv`, `torneos.csv`, `partidos.csv` y `estadisticas_partido.csv` poblados con datos reales, resto de entidades pendientes)

---

# Objetivo

Este módulo constituye la primera implementación de la Base de Conocimiento (`docs/05-Base-de-Conocimiento.md`) para el dominio de selecciones nacionales de fútbol.

Define 11 entidades, cada una en su propio archivo CSV, siguiendo el esquema aprobado en la Misión 001.

---

# Decisiones arquitectónicas aplicadas

1. **Principio de Justificación de Datos**: cada campo de cada entidad está justificado explícitamente en este documento (ver tablas por entidad), conforme a `docs/05-Base-de-Conocimiento.md`.
2. **Ubicación**: se mantiene `data/processed/selecciones-nacionales/`.
3. **`campeon_id_seleccion` eliminado** de `torneos`: es un dato derivado (se obtiene consultando el partido con `fase = final` en `partidos.csv`), nunca se almacena para evitar duplicación.
4. **Sin estadísticas individuales de jugador** en esta misión (goles, asistencias, minutos jugados por jugador y partido). Queda explícitamente diferido a una misión futura.
5. **`id_torneo` nunca nulo**: se define la competición `Amistosos Internacionales` y un torneo contenedor por año calendario para partidos amistosos (ver sección dedicada más abajo).

---

# Convención: Amistosos Internacionales

Los partidos amistosos no pertenecen a un torneo con fase de grupos ni eliminatorias, pero **todo partido debe tener un `id_torneo` válido** para preservar la integridad referencial del modelo (regla aplicada en esta misión: evitar `id_torneo` nulo).

Se resuelve de la siguiente forma:

- Se crea **una única competición permanente** en `competiciones.csv`: `Amistosos Internacionales` (tipo `amistoso`, organizada por FIFA). No es periódica (`periodicidad_anios` queda vacío) porque no sigue un ciclo fijo.
- Se crea **un torneo contenedor por año calendario** en `torneos.csv` (ej. `TOR-2026-AMISTOSOS`, `fecha_inicio: 2026-01-01`, `fecha_fin: 2026-12-31`). Todo amistoso jugado ese año se asocia a ese `id_torneo`.
- La sede no es única (los amistosos se juegan en estadios distintos), por lo que `paises_organizadores` para estos torneos contenedor queda como `N/A (sede variable, ver partidos.id_estadio)`.
- `numero_selecciones_participantes` queda vacío para estos torneos, ya que no existe un conjunto fijo de participantes.

**Regla operativa:** al registrar el primer amistoso de un nuevo año calendario, se debe crear primero la fila correspondiente en `torneos.csv` (`TOR-<año>-AMISTOSOS`) antes de insertar el partido. Esta misión ya crea la fila para el año en curso (2026) como ejemplo del patrón.

**Nota de granularidad:** se eligió agrupar por año calendario (no por ventana FIFA de fecha internacional) por simplicidad, siguiendo la regla del proyecto de no incrementar la complejidad sin evidencia de que mejora el modelo (`CLAUDE.md`). Si en el futuro se demuestra que la granularidad por ventana FIFA aporta valor predictivo, se documentará como mejora en `models/` antes de modificar este esquema.

---

# Estado de los archivos

`selecciones.csv` contiene 62 registros reales: 40 del Top 40 FIFA (Misión 002), 14 incorporadas en la Misión **MS-019** (Chile, Perú, Venezuela, Bolivia, Paraguay, Costa Rica, Serbia, Albania, Georgia, Eslovaquia, Eslovenia, Grecia, Finlandia, República de Irlanda — únicamente las selecciones cuya ausencia fue demostrada empíricamente en `MS-018` como bloqueo real de 19 partidos ya investigados, no una ampliación general del catálogo), más 8 incorporadas en la Misión **DATA-001** (Jordania, Cabo Verde, Arabia Saudita, Irak, Ghana, República Democrática del Congo, Haití, Escocia — rivales reales de las 5 selecciones prioritarias en la Copa Mundial FIFA 2026, sin las cuales sus partidos de fase de grupos/Ronda de 32 no podían incorporarse a `partidos.csv`). Fuentes y limitaciones detalladas en `CHANGELOG.md` (entradas `MS-019` y `DATA-001`). `competiciones.csv` contiene 11 registros reales: la fila de catálogo `Amistosos Internacionales` (Misión 001) más 10 competiciones internacionales pobladas en la Misión 006. `torneos.csv` contiene 15 registros reales: la fila de referencia `TOR-2026-AMISTOSOS` (Misión 001), 12 ediciones reales incorporadas en la Misión MS-015 — la edición más reciente ya oficialmente celebrada de cada una de las 8 competiciones cubiertas por el brief de esa misión (Copa Mundial FIFA 2026; Eurocopa 2024; Copa América 2024; UEFA Nations League 2024-25; CONCACAF Gold Cup 2025; Copa Asiática 2023; Copa Africana de Naciones 2025), y 5 filas para "Eliminatorias Mundial FIFA" (una por confederación — CONMEBOL, UEFA, CONCACAF, AFC, CAF) —, más 2 ediciones adicionales incorporadas en `MS-021` (`TOR-2020-EUROCOPA`, `TOR-2021-COPAAMERICA`): una **segunda edición** de Eurocopa y de Copa América, condición necesaria para que una selección pudiera alcanzar `N≥10` partidos dentro de una misma **competición** (`id_competicion`, agregando varias ediciones), ya que ninguna edición individual del formato actual permite por sí sola llegar a 10 partidos para un mismo equipo (máximo matemático: 7, equipo que llega a la final). Quedan pendientes las ediciones de OFC Nations Cup y Finalissima (`COMP-000010`/`COMP-000011`, fuera del alcance del brief de `MS-015`) y la clasificatoria OFC hacia el Mundial 2026. Fuentes y limitaciones detalladas en `CHANGELOG.md` (entradas `MS-015` y `MS-021`). `estadios.csv` contiene 75 registros reales: 32 de la Misión MS-013 (un estadio principal por cada una de 32 de las 40 selecciones ya catalogadas) más 33 de la Misión MS-017 (sedes de **torneo** — neutrales/anfitrionas — para la Copa Mundial FIFA 2026, la Eurocopa 2024, la Copa América 2024, la UEFA Nations League 2024-25 y las Eliminatorias CONMEBOL, ver detalle en la entidad `estadios.csv` más abajo), 8 de la Misión `MS-021` (sedes de la Eurocopa 2020 y la Copa América 2021), más 2 de la Misión **DATA-001** (Estadio Nacional Julio Martínez Prádanos, Santiago, y Neo Química Arena, São Paulo — ambas sedes ya identificadas como bloqueo pendiente desde `MS-019`, ahora catalogadas), todas pobladas siguiendo estrictamente el protocolo de ingesta (`docs/38-Protocolo-Oficial-Ingesta-Datos.md`). **Efecto lateral no buscado, pero verificado:** catalogar estas 2 sedes también resuelve la FK de estadio de 2 de los 6 partidos candidatos de `MS-016` que seguían bloqueados desde `MS-019` (Chile-Argentina en Santiago, Brasil-Paraguay en São Paulo) — no se investigan ni se incorporan esos 2 partidos específicos en esta misión (fuera del alcance exacto de `DATA-001`), pero queda documentado como oportunidad de bajo costo para una futura misión. Quedan pendientes 8 selecciones sin estadio de sede habitual (`NOR`, `UKR`, `PAN`, `RUS`, `WAL`, `HUN`, `CZE` — `ECU` quedó cubierto indirectamente por `MS-017` vía su sede de Eliminatorias), las sedes de Helsinki/Atenas/El Alto (3 de los 6 candidatos de `MS-016` que siguen bloqueados) y cualquier estadio adicional usado por amistosos o por torneos fuera del alcance de `MS-017`/`MS-021`/`DATA-001` (CONCACAF Gold Cup 2025, Copa Asiática 2023, Copa Africana de Naciones 2025). Fuentes y limitaciones detalladas en `CHANGELOG.md` (entradas `MS-013`, `MS-017`, `MS-021` y `DATA-001`) y `docs/00-Project-Tracker.md`. `arbitros.csv` contiene 51 registros reales (Misión MS-014): el panel completo de árbitros principales (no asistentes, no VAR) designados oficialmente por FIFA para la Copa Mundial FIFA 2026, cubriendo las seis confederaciones (AFC, CAF, CONCACAF, CONMEBOL, OFC, UEFA) — fuente primaria, `inside.fifa.com` ("Match officials appointed for FIFA World Cup 2026"), con el desglose nominal por confederación verificado contra la tabla ya organizada de Wikipedia. Fuentes y limitaciones detalladas en `CHANGELOG.md` (entrada `MS-014`). `partidos.csv` contiene 111 registros reales tras cuatro misiones sucesivas: **MS-018** (32 partidos — reevaluación inicial de los 51 candidatos de `MS-016` contra las FK ampliadas por `MS-017`), **MS-020** (13 partidos adicionales — integración de los partidos que quedaron completamente desbloqueados tras `MS-019`), **MS-021** (29 partidos adicionales, `PAR-000046` a `PAR-000074` — Eurocopa 2020 y Copa América 2021) y **DATA-001** (37 partidos adicionales, `PAR-000075` a `PAR-000111` — 33 de la Copa Mundial FIFA 2026, primera edición del Mundial poblada en el módulo, y 4 de Eliminatorias CONMEBOL adicionales, exclusivamente partidos de las 5 selecciones prioritarias: Argentina, Brasil, España, Francia e Inglaterra). De los 51 partidos candidatos originales de `MS-016` (alcance ya cerrado, no ampliado por `MS-021`/`DATA-001`), **45 ya están incorporados (88.2%)** y **6 siguen bloqueados** (ahora 3 por sede sin catalogar — Helsinki, Atenas, El Alto — y 1 por la altitud no verificable de Róterdam; los otros 2, Santiago y São Paulo, ya tienen sede catalogada desde `DATA-001` pero esos 2 partidos específicos no fueron investigados en esta misión, ver `estadios.csv`). `estadisticas_partido.csv` contiene 107 registros reales tras **DATA-008** (`ESTP-000076` a `ESTP-000107`, 32 filas nuevas — los 16 partidos de la Eurocopa 2020, `MS-021` — más 104 celdas antes vacías completadas en 56 filas ya existentes de la Eurocopa 2024 y la Copa América 2024), a partir de los 75 registros reales heredados de `MS-018`+`MS-020` (`MS-021`/`DATA-001` no habían ampliado esta entidad — ver historial más abajo). **Fuente exclusiva de `DATA-008`: StatsBomb Open Data** (repositorio público, datos evento a evento, gratuito, seleccionado como fuente principal en `DATA-007`) — nunca se calculó, estimó ni completó manualmente ningún valor; cada celda escrita es una agregación directa de eventos que StatsBomb ya etiquetó explícitamente (goles/xG por disparo, tarjetas, faltas, córners, pases con o sin resultado). **`posesion_pct` se dejó deliberadamente sin completar en las 32 filas nuevas**: StatsBomb no expone un campo único de "posesión %" en su flujo de eventos — cualquier cómputo a partir de eventos (por tiempo en posesión o por recuento de eventos) exigiría adoptar una convención metodológica propia, lo que el brief de esta misión prohíbe expresamente ("nunca calcular, nunca estimar"). De las 222 filas equipo-partido posibles (111 partidos × 2), 107 están escritas; **53 de los 111 partidos ya tienen ambos equipos con fila** (Eurocopa 2024: 18/18; Copa América 2024: 10/10; Nations League 2024-25: 8/8; Eurocopa 2020: 16/16; Eliminatorias CONMEBOL: 1/13) y **28 partidos (Eurocopa 2024 + Copa América 2024 íntegras) tienen ahora los 10 campos completos en ambos equipos**, sin ningún campo vacío. Copa América 2021 (13 partidos) y Mundial 2026 (33 partidos) siguen en 0 — ninguna de las dos ediciones está todavía liberada en StatsBomb Open Data. Ver `CHANGELOG.md` (entradas `MS-018`/`MS-020`/`MS-021`/`DATA-001`/`DATA-008`) para el detalle completo por partido. Tras **DATA-009**, `partidos.csv` contiene 124 registros reales (`PAR-000112` a `PAR-000124`, 13 filas nuevas) y `estadisticas_partido.csv` contiene 133 registros reales (26 filas nuevas), incorporando por primera vez partidos de rivales de las 5 selecciones prioritarias **que no involucran a ninguna de ellas** (ej. Polonia-Eslovaquia, Hungría-Portugal, Italia-Suiza, Perú-Chile), con el único objetivo de que esos rivales dejen de tener 0 estadísticas previas a la fecha de su partido contra una prioritaria — mismo mecanismo de StatsBomb Open Data ya usado por `DATA-008`, reutilizando los `matches.json` ya descargados en esa misión (ningún partido nuevo investigado fuera de esas 3 ediciones ya cubiertas: Eurocopa 2020, Eurocopa 2024, Copa América 2024). De los 85 partidos prioritaria-vs-rival que antes no tenían ninguna estadística previa del rival (medido a nivel de `id_competicion`, agregando ediciones), **20 ya la tienen ahora**; el porcentaje de `partidos.csv` con estadísticas completas para ambos equipos sube de 47.7% (53/111) a 53.2% (66/124). Se agregó 1 estadio nuevo (`EST-000076`, Hampden Park, Glasgow) — los otros 5 estadios necesarios (Gazprom Arena/Krestovsky Stadium, Stadio Olimpico, Parken, Signal Iduna Park, Levi's Stadium) **ya existían** en `estadios.csv` desde `MS-013`/`MS-017`/`MS-021`, bajo un nombre ligeramente distinto al usado inicialmente en la búsqueda de esta misión (ej. "Gazprom Arena (Krestovsky Stadium)" vs. "Saint-Petersburg Stadium"); el error de duplicación se detectó y corrigió dentro de la misma misión, antes de cerrarla (ver `CHANGELOG.md`, entrada `DATA-009`, "Hallazgo y autocorrección"). Ninguna selección nueva fue necesaria — los 20 rivales objetivo ya estaban catalogados desde `MS-019`/`DATA-001`. Ver `CHANGELOG.md` (entrada `DATA-009`) para el detalle completo. El resto de los CSV de este módulo (`jugadores`, `convocatorias`, `lesiones`, `cuotas`) siguen conteniendo únicamente la fila de encabezado — cumpliendo la regla "nunca inventar datos" mientras no exista una fuente verificada.

**Nota `DATA-012`:** `selecciones.csv`, `estadios.csv` y `jugadores.csv` ya cuentan con un importador automatizado real (`app/ingestion/selecciones_importer.py`, `estadios_importer.py`, `jugadores_importer.py`, contra `GET /teams`/`/venues`/`/players`+`/players/squads` de API-Football) — **no se ejecutó todavía contra estos archivos**: `DATA-012` no tuvo una credencial real de API-Football disponible en su sesión, y ejecutar el importador con datos de prueba contra estos CSV habría arriesgado corromper los registros reales ya catalogados arriba. El importador es idempotente (clave de negocio determinística por fila, nunca duplica) y respeta la política de campos `CONDICIONAL`/`NO DISPONIBLE` ya aprobada en `docs/44-Reconciliacion-del-Esquema.md` (`nombre_federacion`, `confederacion`, `ranking_fifa_actual`/`ranking_fifa_fecha` de `selecciones.csv`; `altitud_metros`/`techado` de `estadios.csv`; `pie_habil` de `jugadores.csv` quedan siempre vacíos, nunca inventados). Primera ejecución real pendiente de que un humano provea `API_FOOTBALL_KEY` (`.env.example`). Ver `docs/43-Pipeline-de-Ingesta.md`, `docs/44-Reconciliacion-del-Esquema.md` y `CHANGELOG.md` (entrada `DATA-012`).

---

# Entidades

## 1. `selecciones.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_seleccion` | STRING(3) | PK | Integridad referencial: identificador único usado por todas las entidades relacionadas |
| `nombre_pais` | STRING | | Identificación legible del equipo en reportes de predicción (`docs/08-predicciones.md`) |
| `nombre_federacion` | STRING | | Trazabilidad de la fuente oficial (`docs/05-Base-de-Conocimiento.md`: "toda fuente deberá ser identificable y verificable") |
| `confederacion` | ENUM | | Contextualiza viajes intercontinentales (Factores Externos, `docs/03-Variables.md`) y agrupación de clasificatorias |
| `ranking_fifa_actual` | INTEGER | | Proxy de fuerza general, usado como prior en `engine/03-Poisson.md` y `engine/05-Confidence.md` |
| `ranking_fifa_fecha` | DATE | | Vigencia del dato (`docs/05-Base-de-Conocimiento.md`: "Calidad de Datos → fecha de actualización") |
| `seleccionador_actual` | STRING | | Insumo cualitativo de Compatibilidad Táctica (Variable 005, `docs/03-Variables.md`) |
| `activa` | BOOLEAN | | Integridad del modelo: excluye federaciones inactivas de la predicción |

**Relaciones:** referenciada por `jugadores`, `convocatorias`, `partidos`, `estadisticas_partido`.
**Restricciones:** `id_seleccion` único, 3 letras mayúsculas; `ranking_fifa_actual` > 0; `ranking_fifa_fecha` no futura.
**Datos poblados en la Misión MS-019:** 14 selecciones reales adicionales (`CHI`, `PER`, `VEN`, `BOL`, `PAR`, `CRC`, `SRB`, `ALB`, `GEO`, `SVK`, `SVN`, `GRE`, `FIN`, `IRL`) — alcance controlado, no una ampliación general del Top 40 FIFA: únicamente las selecciones cuya falta bloqueaba, con evidencia empírica de `MS-018`, la incorporación de partidos reales ya investigados en `MS-016`. `ranking_fifa_fecha = 2026-07-20` (edición FIFA distinta a la de las 40 selecciones originales, `2026-06-11` — ambas vigentes en sus respectivas fechas de captura, sin corregirse entre sí). **Limitación documentada:** `seleccionador_actual` de Serbia, Georgia, Eslovenia y Grecia proviene de una única fuente secundaria (infobox de Wikipedia del equipo nacional), sin segunda fuente independiente de verificación cruzada — confianza moderada, no descartado por seguir el mismo criterio ya usado en `MS-013` (Wikipedia como respaldo cuando la fuente oficial de la federación resultó inaccesible), pero sí más débil que el resto de campos de esta misión (ranking FIFA/confederación, verificados por partida doble: fecha oficial confirmada en `inside.fifa.com`, valor numérico cruzado con Wikipedia).

**Datos poblados en la Misión DATA-001:** 8 selecciones reales adicionales (`JOR`, `CPV`, `KSA`, `IRQ`, `GHA`, `COD`, `HAI`, `SCO`) — rivales reales de las 5 selecciones prioritarias en la fase de grupos/Ronda de 32 de la Copa Mundial FIFA 2026 (`TOR-2026-MUNDIAL`), sin las cuales esos partidos no podían incorporarse a `partidos.csv` por integridad referencial. `ranking_fifa_fecha = 2026-04-01` (fecha de publicación oficial citada consistentemente por las fuentes consultadas para las 8 selecciones, distinta de las fechas ya usadas por lotes anteriores — todas vigentes en su momento de captura, ninguna corregida retroactivamente). **Fuente:** Wikipedia/prensa deportiva especializada verificada por búsqueda activa durante esta misión (Federación Jordana de Fútbol, Federação Caboverdiana de Futebol, Saudi Arabian Football Federation, Iraq Football Association, Ghana Football Association, Fédération Congolaise de Football-Association, Fédération Haïtienne de Football, Scottish Football Association) — nunca Transfermarkt.

---

## 2. `jugadores.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_jugador` | STRING | PK | Integridad referencial (`convocatorias`, `lesiones`) |
| `nombre_completo` | STRING | | Trazabilidad |
| `nombre_conocido` | STRING | | Legibilidad en reportes |
| `fecha_nacimiento` | DATE | | Proxy de Fatiga/Calidad de Plantilla (edad, Variable 007/008) |
| `posicion_principal` | ENUM | | Insumo de Compatibilidad Táctica (Variable 005) |
| `pie_habil` | ENUM | | Insumo secundario de Compatibilidad Táctica |
| `altura_cm` | INTEGER | | Insumo de perfil físico en Compatibilidad Táctica (ej. juego aéreo) |
| `id_seleccion` | STRING | FK → `selecciones` | Integridad referencial; insumo de Disponibilidad de Plantilla |
| `club_actual` | STRING | | Contexto de carga competitiva, insumo de Fatiga (Variable 007) |
| `activo_seleccion` | BOOLEAN | | Integridad: evita convocatorias inválidas |

**Restricciones:** `id_jugador` único e inmutable; `fecha_nacimiento` no futura; un jugador solo puede tener una `id_seleccion` activa a la vez.

---

## 3. `convocatorias.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_convocatoria` | STRING | PK | Integridad referencial/trazabilidad |
| `id_torneo` | STRING | FK → `torneos` | Reconstruye Disponibilidad de Plantilla (Variable 006) por torneo |
| `id_seleccion` | STRING | FK → `selecciones` | Idem |
| `id_jugador` | STRING | FK → `jugadores` | Idem |
| `dorsal` | INTEGER | | Trazabilidad/identificación oficial |
| `posicion_convocatoria` | ENUM | | Refina Compatibilidad Táctica para el torneo específico |
| `fecha_convocatoria` | DATE | | Vigencia del dato; insumo de Estado Psicológico (tensión por convocatoria tardía) |
| `estado_convocatoria` | ENUM | | Insumo directo de Disponibilidad de Plantilla (bajas antes/durante el torneo) |

**Restricciones:** único (`id_torneo`, `id_seleccion`, `id_jugador`); único (`id_torneo`, `id_seleccion`, `dorsal`).

---

## 4. `partidos.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_partido` | STRING | PK | Integridad referencial: entidad central del sistema |
| `id_torneo` | STRING | FK → `torneos` (nunca nulo) | Insumo de Rendimiento en el Torneo (Variable 002) y de Índice de Caos |
| `id_seleccion_local` | STRING | FK → `selecciones` | Insumo de Localía (Variable 009) |
| `id_seleccion_visitante` | STRING | FK → `selecciones` | Idem |
| `id_estadio` | STRING | FK → `estadios` | Insumo de Factores Externos (altitud, clima) |
| `id_arbitro` | STRING | FK → `arbitros` | Insumo de Factores Externos (Variable 012) |
| `fecha` | DATE | | Insumo de Forma Reciente (Variable 001) y Fatiga (descanso entre partidos) |
| `hora_local` | STRING | | Insumo secundario de Factores Externos (calor/humedad según franja horaria) |
| `fase` | ENUM | | Insumo de Índice de Caos (`engine/04-Chaos-Index.md`) y Estado Psicológico |
| `jornada` | INTEGER | | Contextualiza Rendimiento en el Torneo |
| `goles_local` | INTEGER | | Resultado oficial, base de `docs/09-Auditoria.md` |
| `goles_visitante` | INTEGER | | Idem |
| `estado_partido` | ENUM | | Filtra partidos válidos para el cálculo de variables |
| `asistencia` | INTEGER | | Insumo secundario de Estado Psicológico/presión ambiental |

**Campo excluido:** `resultado_final`/`ganador` — se deriva de `goles_local` vs. `goles_visitante`.
**Restricciones:** `id_seleccion_local` ≠ `id_seleccion_visitante`; goles solo se completan si `estado_partido = finalizado`; `jornada` obligatorio solo si `fase = fase_grupos`; `id_torneo` es **obligatorio siempre** (ver convención de Amistosos Internacionales).
**Formato de `id_partido` (fijado en `MS-018`, sin precedente previo):** `PAR-NNNNNN` (6 dígitos), mismo patrón que `EST-NNNNNN`/`ARB-NNNNNN`/`COMP-NNNNNN`.
**Valores de `fase` (literales, sin ENUM formalizado, hallazgo heredado de `docs/38`) usados en `MS-018`:** `fase_grupos`, `octavos_final`, `cuartos_final`, `semifinal`, `tercer_puesto`, `final` (torneos con eliminación directa) y `eliminatoria` (Eliminatorias Mundial FIFA — fase de liga todos-contra-todos, sin equivalente de "grupo" ni "eliminación directa"; usa `jornada` con el número de fecha aunque la restricción del esquema no lo exija fuera de `fase_grupos`, por ser informativo y no estar prohibido).
**Hallazgo de `MS-018`, no resuelto, confirmado sin cambios en `MS-020`, ampliado en `MS-021`:** ninguna columna registra el resultado de una tanda de penales. 5 de los 45 partidos poblados hasta `MS-020` se definieron en penales tras empate en el marcador de 90+prórroga (`PAR-000016`, `PAR-000017`, `PAR-000020`, `PAR-000024`, `PAR-000022`) — `goles_local`/`goles_visitante` reflejan fielmente el marcador de campo (nunca los penales, que no son goles de juego), pero esto significa que el campo derivado "campeón" (`torneos.campeon_id_seleccion`, obtenido de la fila con `fase = final`) **no es calculable con precisión** para un torneo cuya final se decida en penales usando solo `partidos.csv` — afecta ya a `PAR-000022` (final de la Nations League 2024-25, Portugal 2-2 España, Portugal ganador real por penales 5-3). `MS-021` añade 6 casos más de esta misma limitación ya conocida (`PAR-000055` Francia 3-3 Suiza, penales Suiza; `PAR-000057` Suiza 1-1 España, penales Suiza; `PAR-000059` Italia 1-1 España, penales Italia; `PAR-000061` Italia 1-1 Inglaterra, penales Italia — final de la Eurocopa 2020; `PAR-000073` Colombia 1-1 Argentina, penales Argentina; `PAR-000074` no se decide por penales, Argentina gana la final de la Copa América 2021 en tiempo regular 1-0). Se documenta la limitación en vez de agregar una columna nueva (fuera del alcance de `MS-018`/`MS-021`, que no autorizan modificar el esquema).

**Datos poblados en `MS-021`:** 29 partidos reales adicionales (`PAR-000046` a `PAR-000074`), exclusivamente de las 5 selecciones prioritarias del proyecto (Argentina, Brasil, España, Francia, Inglaterra) en dos ediciones nuevas: Eurocopa 2020 (`TOR-2020-EUROCOPA`, jugada en 2021, 16 partidos: 6 de España, 4 de Francia, 6 de Inglaterra) y Copa América 2021 (`TOR-2021-COPAAMERICA`, 13 partidos: 7 de Argentina, 7 de Brasil, con la final Argentina-Brasil contando para ambas). **Decisión de alcance:** se omite deliberadamente Inglaterra-Escocia (Eurocopa 2020, fase de grupos) — Escocia no está catalogada en `selecciones.csv` y el partido no era necesario para que Inglaterra alcanzara `N≥10` (ya lo hacía con los otros 6 partidos ingleses de esta misión); incorporar una selección nueva solo para esa fila habría sido una ampliación de `selecciones.csv` no justificada por el brief de `MS-021` (que restringe la ampliación de entidades a lo estrictamente necesario). **Fuente:** Wikipedia (fuente secundaria ya aceptada por `docs/38` sección 4 cuando no hay fuente primaria de confederación accesible en este entorno de trabajo, sin acceso a internet desde el Engine) — verificada activamente con la herramienta de búsqueda web durante esta misión, no recordada de memoria: se contrastaron los resultados de fase de grupos, octavos, cuartos, semifinal y final de ambos torneos contra al menos dos consultas independientes por dato crítico. **Corrección de una inconsistencia detectada durante la propia investigación:** una primera consulta sobre el cuadro de eliminatorias de la Copa América 2021 devolvió una final "Argentina-Colombia" que resultó ser un error del resumen automático de la fuente (contradecía la propia definición de semifinalistas ya confirmada) — se verificó con una segunda consulta dirigida específicamente al cuadro de eliminatorias completo, confirmando Argentina 1-0 Brasil como la final real (Maracaná, 10 de julio de 2021); se documenta este proceso de verificación cruzada como aplicación directa de "ante duda, no escribir el dato" antes de corregirlo con una fuente adicional. **`id_arbitro` se deja vacío en los 29 partidos**: ninguno de los 51 árbitros de `arbitros.csv` (panel FIFA del Mundial 2026) ofició partidos de 2021 — agregar árbitros de esa época está fuera del alcance de esta misión (`arbitros.csv` no forma parte del brief de `MS-021`). **`asistencia` se deja vacía cuando no hay una cifra verificada** (fase eliminatoria de la Eurocopa 2020 más allá de octavos, y la final de la Copa América 2021 — fuente solo confirma "acceso restringido, 10% de aforo para invitados con prueba COVID negativa" sin cifra exacta citable) y **se registra explícitamente en `0` para el resto de la Copa América 2021** (fase de grupos y cuartos/semifinal): los estadios permanecieron cerrados al público por protocolo COVID-19 vigente en Brasil durante ese torneo — un dato real verificado, no una ausencia de dato.

**Datos poblados en `DATA-001`:** 37 partidos reales adicionales (`PAR-000075` a `PAR-000111`), exclusivamente de las 5 selecciones prioritarias. **33 de la Copa Mundial FIFA 2026** (`TOR-2026-MUNDIAL`, primera edición del Mundial con partidos reales en el módulo — hasta ahora solo existía la fila de catálogo del torneo, sin partidos): 15 de fase de grupos, 5 de Ronda de 32 (`dieciseisavos_final`, valor literal nuevo para la columna `fase` — primer torneo del módulo con esta ronda adicional respecto al formato de 24/16 equipos ya usado por Eurocopa/Copa América, sin ENUM formalizado, mismo hallazgo heredado de `docs/38`), 5 de octavos de final, 4 de cuartos, 2 de semifinal, 1 de tercer puesto y 1 final (España 1-0 Argentina). **4 partidos adicionales de Eliminatorias CONMEBOL** (`TOR-2026-ELIM-CONMEBOL`, ya catalogado desde `MS-015`/`MS-018`): jornadas 6 (Brasil 0-1 Argentina, Maracaná, noviembre 2023 — cuenta para ambas selecciones prioritarias), 9 (Chile 1-2 Brasil), 10 (Brasil 4-0 Perú) y 16 (Brasil 1-0 Paraguay, el partido de clasificación matemática de Brasil al Mundial 2026). **Resultado medible:** las 5 selecciones prioritarias alcanzan ahora Argentina 27, Brasil 25, España 24, Francia 22, Inglaterra 23 partidos oficiales totales — dentro o muy cerca del rango orientativo de 25-30 fijado por el brief ("no existe un número exacto obligatorio"). **Fuente:** Wikipedia, ESPN, FIFA.com y prensa deportiva especializada, verificadas activamente por búsqueda web durante esta misión con al menos dos consultas independientes por dato crítico — nunca Transfermarkt, nunca amistosos, nunca eliminatorias usadas para completar el mínimo de forma artificial. **`id_arbitro` se completa solo en 3 de los 37 partidos** (Slavko Vinčić, Alejandro Hernández Hernández, César Arturo Ramos — los únicos confirmados con fuente citable durante esta misión; los tres ya estaban en `arbitros.csv`, panel FIFA del Mundial 2026, verificado antes de escribir) — se deja vacío en el resto en vez de asumir un árbitro no confirmado. **Limitación central de esta misión, con autorización explícita del Arquitecto Estadístico Humano:** no fue posible extraer estadísticas detalladas (xG, disparos, posesión) de ninguna de las fuentes consultadas para estos 37 partidos — el dato existe oficialmente (Opta/FIFA), pero está renderizado mediante JavaScript no accesible a las herramientas de esta misión; se decidió incorporar `partidos.csv` completo (campos sí verificables) y no ampliar `estadisticas_partido.csv`, en vez de omitir los 37 partidos por completo — ver entidad `estadisticas_partido.csv` para el detalle. **Efecto lateral verificado, no explotado en esta misión:** catalogar Estadio Nacional de Santiago y Neo Química Arena (São Paulo) — necesarios para las jornadas 9 y 16 de Eliminatorias CONMEBOL — también resuelve la FK de estadio de 2 de los 6 partidos candidatos de `MS-016` que seguían bloqueados (Chile-Argentina, Brasil-Paraguay); esos 2 partidos específicos no se investigaron ni incorporaron aquí (fuera del alcance exacto de `DATA-001`).

**Datos poblados en `DATA-009`:** 13 partidos reales adicionales (`PAR-000112` a `PAR-000124`) — a diferencia de toda misión anterior, **ninguno de estos 13 partidos involucra a una selección prioritaria**: son partidos reales de rivales frecuentes de Argentina/Brasil/España/Francia/Inglaterra contra terceros equipos, dentro de las mismas ediciones ya cubiertas por StatsBomb Open Data (Eurocopa 2020, Eurocopa 2024, Copa América 2024). **Objetivo exacto:** que esos rivales dejen de tener 0 partidos con estadística real anteriores a la fecha en que enfrentaron a una prioritaria — condición que hoy determina si Variable003/Variable004 devuelven `disponible=False` para ese rival (`VALID-001`/`VALID-002`). **Los 13 partidos:** Polonia 1-2 Eslovaquia, Hungría 0-3 Portugal, Italia 3-0 Suiza, Escocia 0-2 República Checa, Dinamarca 1-2 Bélgica, Países Bajos 3-2 Ucrania (Eurocopa 2020); Italia 2-1 Albania, Turquía 3-1 Georgia, Eslovenia 1-1 Dinamarca (Eurocopa 2024); Perú 0-0 Chile, Colombia 2-1 Paraguay, Ecuador 1-2 Venezuela, Uruguay 3-1 Panamá (Copa América 2024). **Selección de partidos, no arbitraria:** de los partidos reales disponibles en los `matches.json` ya cacheados por `DATA-008`, se priorizaron los que involucran **dos rivales objetivo a la vez** (ej. Polonia-Eslovaquia resuelve ambos con una sola incorporación) y los que usan estadios ya catalogados, para minimizar tanto el número de partidos nuevos como de estadios nuevos. **`id_arbitro` y `hora_local` se dejan vacíos en los 13 partidos**: StatsBomb no expone árbitro verificable contra `arbitros.csv` (panel Mundial 2026, no aplica a estas ediciones) y el campo `kick_off` de la fuente mezcla convenciones de huso horario no siempre distinguibles como hora local sin riesgo de error (ver `CHANGELOG.md`, entrada `DATA-009`) — se prefirió dejarlo vacío a escribir una hora potencialmente incorrecta. **`asistencia` vacía**: StatsBomb no publica asistencia en sus datos de partido. **Resultado medible:** de los 85 partidos prioritaria-vs-rival que antes no tenían ninguna estadística previa del rival (a nivel de `id_competicion`, agregando ediciones — mismo criterio que usa el Engine real), **20 ya la tienen ahora**; quedan 65 sin resolver, concentrados en competiciones sin cobertura de StatsBomb (Mundial 2026, Eliminatorias CONMEBOL, Nations League) o en partidos que eran, genuinamente, el debut del rival en la edición ya cubierta (sin partido real anterior que citar). **Hallazgo y autocorrección, documentado con transparencia:** al construir la lista de estadios nuevos necesarios, una búsqueda inicial por nombre no encontró 5 de los 6 estadios ya catalogados (estaban bajo un nombre ligeramente distinto: "Gazprom Arena (Krestovsky Stadium)" en vez de "Saint-Petersburg Stadium", entre otros) — se escribieron inicialmente como estadios nuevos, duplicando 5 filas ya existentes desde `MS-017`/`MS-021`. El error se detectó **dentro de la misma misión**, antes de cerrarla, mediante una verificación cruzada adicional del archivo completo (búsqueda por nombre/ciudad, no solo por los términos usados en la búsqueda inicial) — se corrigió eliminando las 5 filas duplicadas y reapuntando el `id_estadio` de los partidos afectados a los IDs ya existentes, sin dejar duplicados, huérfanos ni referencias rotas (verificado programáticamente antes de escribir la versión final). Se documenta explícitamente como ejemplo de por qué la regla de "reutilización" (`docs/38`) exige verificar contra el contenido real del archivo, no solo contra los términos de búsqueda usados para identificar el dato original.

---

## 5. `estadisticas_partido.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_estadistica_partido` | STRING | PK | Integridad referencial |
| `id_partido` | STRING | FK → `partidos` | Relación obligatoria |
| `id_seleccion` | STRING | FK → `selecciones` | Idem |
| `xg` | DECIMAL | | Insumo directo de Potencial Ofensivo (Variable 003) y `engine/01-Offensive-Strength.md` |
| `posesion_pct` | DECIMAL | | Insumo de Compatibilidad Táctica (Variable 005) |
| `disparos_totales` | INTEGER | | Insumo directo de Potencial Ofensivo (Variable 003) |
| `disparos_al_arco` | INTEGER | | Idem |
| `corners` | INTEGER | | Proxy secundario de dominio ofensivo |
| `faltas_cometidas` | INTEGER | | Insumo de Índice de Caos (indisciplina como imprevisibilidad) |
| `tarjetas_amarillas` | INTEGER | | Idem, y base para futura Disponibilidad de Plantilla por acumulación |
| `tarjetas_rojas` | INTEGER | | Idem |
| `pases_completados` | INTEGER | | Insumo de Compatibilidad Táctica (estilo de posesión/juego directo) |
| `precision_pases_pct` | DECIMAL | | Idem |

**Campo excluido:** `xga` — es idéntico al `xg` del rival en el mismo `id_partido`; se obtiene con un self-join, nunca se duplica.
**Restricciones:** único (`id_partido`, `id_seleccion`); `posesion_pct` 0-100; `disparos_al_arco` ≤ `disparos_totales`.
**Formato de `id_estadistica_partido` (fijado en `MS-018`, sin precedente previo):** `ESTP-NNNNNN` (6 dígitos), mismo patrón que `PAR-NNNNNN`/`EST-NNNNNN`.
**Datos poblados en `MS-018`:** 53 de 64 filas posibles (32 partidos × 2 equipos). **Datos poblados en `MS-020`:** 22 filas adicionales de los 13 partidos integrados en esa misión (26 posibles, 4 sin escribir por no tener ninguna estadística verificable — ambos equipos de `PAR-000044` y `PAR-000045`, Argentina-Venezuela y Brasil-Chile de Eliminatorias CONMEBOL). Total acumulado: 75 de 90 filas posibles. **`MS-021` no agrega filas a esta entidad** (decisión explícita de alcance, ver entidad `partidos.csv` arriba y `CHANGELOG.md`): los 29 partidos nuevos de esa misión (58 filas equipo-partido posibles) quedan sin estadísticas — investigar `xg`/disparos/posesión verificables para partidos de 2021 quedó fuera del alcance del brief, que solo exige `N≥10` partidos por competición. **`DATA-001` tampoco agrega filas**, pero por un motivo distinto: a diferencia de `MS-021` (decisión de alcance), `DATA-001` sí intentó activamente obtener `xg`/disparos/posesión para los 37 partidos nuevos (Copa Mundial FIFA 2026 y Eliminatorias CONMEBOL) contra las fuentes permitidas por `docs/38` (FIFA.com match centre, ESPN, Fox Sports, Sofascore, Wikipedia), sin éxito — la información existe oficialmente, pero está renderizada mediante JavaScript no accesible a las herramientas de extracción disponibles en esta sesión. Se dejó constancia explícita de esta limitación técnica (no de disponibilidad de la fuente) y se decidió, con autorización del Arquitecto Estadístico Humano, no ampliar esta entidad en vez de incorporar datos parciales o de baja confianza. Los campos `xg`, `pases_completados` y `precision_pases_pct` quedan vacíos en la mayoría de los partidos de Eurocopa 2024/Nations League 2024-25 (no disponibles en ninguna fuente autorizada accedida — UEFA.com bloqueó el acceso automatizado) y en todos los de Eliminatorias CONMEBOL (AFA/CBF no publican estas métricas en sus crónicas oficiales) — nunca se estimaron ni interpolaron; en 2 casos (`PAR-000038` Chile-Argentina y `PAR-000039` Argentina-Perú de Copa América) el `xg` reportado por la investigación original tenía baja confianza declarada explícitamente por la propia fuente ("no confirmado en página primaria") y se dejó vacío en vez de usarlo, aplicando "ante duda, no escribir el dato". Las 15 filas equipo-partido sin ninguna estadística verificable (ni tarjetas) se dejaron sin escribir en vez de crear una fila vacía sin valor informativo — ver `CHANGELOG.md` para el detalle completo.

**Datos poblados en `DATA-008`:** 32 filas nuevas (`ESTP-000076` a `ESTP-000107`) — los 16 partidos de la Eurocopa 2020 (`MS-021`, hasta ahora sin ninguna estadística) —, más 104 celdas completadas en 56 filas ya existentes de la Eurocopa 2024 (`PAR-000001` a `PAR-000013`, `PAR-000033` a `PAR-000037`) y la Copa América 2024 (`PAR-000014` a `PAR-000019`, `PAR-000038` a `PAR-000041`): `pases_completados`/`precision_pases_pct` en las 18 filas-partido de Eurocopa 2024 (nunca se habían completado desde `MS-018`) y `xg` en 16 celdas puntuales de ambas competiciones donde la investigación original lo había dejado en blanco. **Fuente:** StatsBomb Open Data (repositorio público en GitHub, `github.com/statsbomb/open-data`, datos evento a evento, licencia de atribución no comercial) — verificado directamente contra `competitions.json` que cubre exactamente estas ediciones (más Copa América 2024, que ya estaba con esas celdas completas desde `MS-018`, y Mundial 2018/2022, CAN 2023, sin partidos propios en el módulo todavía). **Método:** para cada uno de los 44 partidos candidatos (los 18 de Eurocopa 2024 + 16 de Eurocopa 2020 + 10 de Copa América 2024 ya existentes en `partidos.csv`), se localizó el `match_id` real de StatsBomb cruzando fecha (con tolerancia de ±1 día, ya que StatsBomb registra la fecha en UTC y varios partidos de Copa América 2024 se jugaron de noche en horario ET, cruzando la medianoche UTC) y ambos equipos (en cualquier orden, ya que la designación local/visitante entre fuentes puede diferir sin afectar el resultado real — confirmado explícitamente en `PAR-000008`, Alemania-España, donde StatsBomb registra a España como local) — **los 44 partidos candidatos fueron encontrados y verificados con marcador idéntico al ya registrado en `partidos.csv`, sin una sola discrepancia**, antes de aceptar el cruce como válido. Después, se agregaron los eventos de cada partido (archivo `events/{match_id}.json`) por equipo: `xg` = suma de `shot.statsbomb_xg` (excluyendo penales de desempate, periodo 5); `disparos_totales` = conteo de eventos `Shot` (excluyendo periodo 5); `disparos_al_arco` = disparos con `outcome` en `{Goal, Saved, Saved to Post}` (se excluye explícitamente `Saved Off Target`, que por su propio nombre en la fuente indica que iba fuera); `corners` = eventos `Pass` con `pass.type.name = Corner`; `faltas_cometidas` = conteo de eventos `Foul Committed`; `tarjetas_amarillas`/`tarjetas_rojas` = tarjetas etiquetadas explícitamente en `foul_committed.card`/`bad_behaviour.card` (`Second Yellow` se contabiliza como amarilla adicional, nunca como roja, para no interpretar una atribución que StatsBomb no etiqueta como tal); `pases_completados`/`precision_pases_pct` = eventos `Pass` sin campo `outcome` (StatsBomb marca explícitamente todo pase incompleto; su ausencia significa pase completado) sobre el total de eventos `Pass`. **Ninguna de estas agregaciones es una estimación**: cada una es un conteo o suma directa de una etiqueta que StatsBomb ya asignó evento por evento, nunca una inferencia propia. **`posesion_pct` se excluye deliberadamente de las 32 filas nuevas**, único de los 10 campos no completado: StatsBomb no publica un campo de "posesión %" agregado por partido en su flujo de eventos — construirlo exigiría adoptar una de varias convenciones metodológicas posibles (por tiempo de balón en juego o por recuento de eventos), lo que cruza hacia "calcular/estimar", expresamente prohibido por el brief de esta misión; se documenta como limitación, no se resuelve. **Discrepancia menor observada, no corregida (no se sobrescribe ningún valor ya poblado):** al calcular `xg` para partidos que ya tenían el campo lleno desde `MS-018` (no tocados en esta misión), los valores de StatsBomb difieren ligeramente de los ya registrados (ej. `PAR-000001` España: StatsBomb 1.57 vs el 1.91 ya registrado) — esperable al ser modelos de `xG` de proveedores distintos (la fuente original de `MS-016`/`MS-018` no fue StatsBomb); mismo patrón para `faltas_cometidas` (diferencias de 1-3 faltas en algunos partidos). **Se documenta como hallazgo de gobernanza de datos** (mezcla de proveedores de `xG` dentro de la misma población de comparación de Variable003/004): esta misión solo completa celdas vacías, nunca sustituye un valor ya incorporado — la decisión de homogeneizar el proveedor de `xG` de toda una competición, si se considera necesaria, corresponde al Arquitecto Estadístico Humano.

**Datos poblados en `DATA-009`:** 26 filas nuevas (`ESTP-000108` a `ESTP-000133`) — ambos equipos de cada uno de los 13 partidos nuevos de `partidos.csv` (ver entidad `partidos.csv` arriba), con la misma metodología exacta de `DATA-008` (agregación evento a evento desde `events/{match_id}.json` de StatsBomb Open Data, reutilizando los `matches.json` ya descargados en esa misión — cero descargas de `matches.json` nuevas, solo 13 `events/{match_id}.json` nuevos). `posesion_pct` queda vacía en las 26 filas, mismo motivo ya documentado en `DATA-008` (StatsBomb no publica ese campo). Validado programáticamente antes de escribir: `disparos_al_arco ≤ disparos_totales` en las 26 filas, sin IDs duplicados, sin pares (`id_partido`, `id_seleccion`) duplicados, FK completa hacia los 13 `id_partido` nuevos.

---

## 6. `lesiones.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_lesion` | STRING | PK | Integridad referencial |
| `id_jugador` | STRING | FK → `jugadores` | Insumo de Disponibilidad de Plantilla (Variable 006) |
| `tipo_lesion` | STRING | | Calibra el impacto real en Disponibilidad |
| `gravedad` | ENUM | | Idem |
| `fecha_inicio` | DATE | | Permite calcular disponibilidad exacta por partido/convocatoria |
| `fecha_estimada_retorno` | DATE | | Idem |
| `fecha_retorno_real` | DATE | | Idem |
| `id_partido_origen` | STRING | FK → `partidos` (opcional) | Trazabilidad del origen de la lesión |
| `estado` | ENUM | | Filtra lesiones activas vs. resueltas |
| `fuente` | STRING | | Regla "nunca inventar datos": la fuente debe ser verificable |

**Campo excluido:** `id_seleccion` — se deriva de `jugadores.id_jugador`.
**Restricciones:** `fecha_estimada_retorno` ≥ `fecha_inicio`; `fecha_retorno_real` solo si `estado = recuperado`; `fuente` obligatoria.

---

## 7. `cuotas.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_cuota` | STRING | PK | Integridad referencial |
| `id_partido` | STRING | FK → `partidos` | Relación obligatoria |
| `casa_apuestas` | STRING | | Trazabilidad de la fuente |
| `mercado` | ENUM | | Define qué probabilidad de mercado se compara en `engine/06-Expected-Value.md` |
| `seleccion_o_resultado` | STRING | | Idem |
| `cuota_decimal` | DECIMAL | | Insumo directo de `engine/06-Expected-Value.md` |
| `fecha_captura` | DATE+hora | | Las cuotas varían en el tiempo; se necesita la vigente al momento de la predicción |
| `estado_cuota` | ENUM | | Filtra cuotas abiertas de las cerradas/suspendidas |

**Campo excluido:** `probabilidad_implicita` — se calcula en `engine/06-Expected-Value.md`, no es un dato bruto.
**Restricciones:** `cuota_decimal` > 1.00; unicidad real = (`id_partido`, `casa_apuestas`, `mercado`, `seleccion_o_resultado`, `fecha_captura`).

---

## 8. `arbitros.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_arbitro` | STRING | PK | Integridad referencial |
| `nombre_completo` | STRING | | Trazabilidad |
| `nacionalidad` | STRING | | Contexto de Factores Externos (sesgo potencial, solo con evidencia) |
| `confederacion_arbitral` | ENUM | | Calibra la fiabilidad del dato (exigencia distinta por panel) |
| `categoria` | ENUM | | Idem |
| `activo` | BOOLEAN | | Filtra árbitros vigentes |

**Restricciones:** `nombre_completo` obligatorio; `categoria = fifa_internacional` requerido en torneos FIFA/confederación.
**Formato de `id_arbitro` (fijado en `MS-014`, sin precedente previo en este documento):** `ARB-NNNNNN` (6 dígitos), mismo patrón ya usado por `competiciones.csv` (`COMP-NNNNNN`) y `estadios.csv` (`EST-NNNNNN`, `MS-013`).
**Valores de `confederacion_arbitral` (ENUM) usados en `MS-014`:** `AFC`, `CAF`, `CONCACAF`, `CONMEBOL`, `OFC`, `UEFA` — mismos seis códigos de confederación ya usados en `selecciones.csv`/`competiciones.csv` (`confederacion_organizadora` excluye `FIFA` de esta columna específica, a diferencia de `competiciones.csv`: un árbitro pertenece siempre a una única confederación real, nunca a "FIFA" como panel propio — la designación FIFA es la categoría, no la confederación).
**Valores de `categoria` (ENUM) confirmados:** solo `fifa_internacional` está citado textualmente en este documento (ver "Restricciones" arriba) — `MS-014` no formaliza ningún otro valor (hallazgo heredado de `docs/38`, no resuelto).
**Datos poblados en la Misión MS-014:** 51 árbitros reales — ver `CHANGELOG.md` para fuentes y limitaciones completas.

---

## 9. `estadios.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_estadio` | STRING | PK | Integridad referencial |
| `nombre` | STRING | | Trazabilidad/contexto |
| `ciudad` | STRING | | Idem |
| `pais` | STRING | | Idem |
| `capacidad` | INTEGER | | Proxy de Estado Psicológico/presión ambiental |
| `tipo_superficie` | ENUM | | Insumo de Factores Externos (Variable 012: estado del campo) |
| `altitud_metros` | INTEGER | | Insumo directo de Factores Externos (Variable 012: altitud) |
| `techado` | BOOLEAN | | Insumo de Factores Externos (anula la variable clima si es techado) |

**Restricciones:** `capacidad` > 0; `altitud_metros` puede ser negativo.
**Formato de `id_estadio` (fijado en `MS-013`, sin precedente previo en este documento):** `EST-NNNNNN` (6 dígitos), mismo patrón ya usado por `competiciones.csv` (`COMP-NNNNNN`).
**Hallazgo heredado de `MS-012`/`docs/38`, no resuelto en `MS-013`, ampliado en `MS-017`:** el ENUM de `tipo_superficie` nunca fue formalizado en ningún documento — los 32 registros poblados en `MS-013` usan el valor literal `natural`. `MS-017` introduce, sin formalizar tampoco un ENUM (columna sin cambios), dos valores literales adicionales ya necesarios en la práctica: `artificial` (césped artificial permanente, típico de estadios multipropósito NFL/CFL) e `hibrido` (césped natural reforzado con fibra sintética). Sigue sin existir una taxonomía cerrada — cualquier futura misión que agregue estadios deberá seguir usando el valor descriptivo más simple y verificable, sin inventar uno nuevo si alguno de estos tres ya aplica.
**Datos poblados en la Misión MS-013:** 32 estadios reales (uno por selección, para 32 de las 40 ya catalogadas en `selecciones.csv`) — ver `CHANGELOG.md` para fuentes y limitaciones completas.
**Datos poblados en la Misión MS-017:** 33 estadios reales adicionales (`EST-000033` a `EST-000065`) — sedes de **torneo** (neutrales/anfitrionas), a diferencia de los 32 de `MS-013` que son la sede habitual de cada selección. Cubre: los 9 estadios alemanes de la Eurocopa 2024 no catalogados (excluye Allianz Arena, Múnich, ya existente); 16 estadios de la Copa América 2024 (13) y del Mundial FIFA 2026 (13, con solapamiento de 10 con los de Copa América — mismo estadio físico usado por ambos torneos, una sola fila) más 3 exclusivos de Copa América y 3 exclusivos del Mundial, en Estados Unidos, más BC Place (Canadá) y Estadio BBVA/Estadio Akron (México) del Mundial 2026; Estadio Mestalla (Valencia) y Stadion Poljud (Split) de la Nations League 2024-25; y Estadio Monumental Isidro Romero Carbo (Guayaquil — cierra el hueco de Ecuador ya documentado), Arena Fonte Nova (Salvador) y Arena BRB Mané Garrincha (Brasília) de las Eliminatorias CONMEBOL. **Introduce por primera vez los valores `artificial` e `hibrido` en `tipo_superficie`** (columna sin ENUM formalizado desde `MS-012`/`docs/38`, ver hallazgo bajo la entidad `estadios.csv`) — los 32 estadios de `MS-013` eran todos césped natural; varios estadios multipropósito de EE.UU. usan césped artificial permanente con césped natural instalado temporalmente para fútbol (confirmado explícitamente solo para algunos casos, ver `CHANGELOG.md`). Stadion Feijenoord ("De Kuip", Róterdam) quedó **explícitamente omitido**: ninguna fuente consultada ofrece una altitud coherente y citable para Róterdam (ciudad con zonas bajo el nivel del mar, sin un punto de referencia único) — regla de esta misión "ante duda, no incorporar el estadio". Ver `CHANGELOG.md` para fuentes, discrepancias entre proveedores y limitaciones completas por estadio.

**Datos poblados en la Misión MS-021:** 8 estadios reales adicionales (`EST-000066` a `EST-000073`) — sedes de torneo de la Eurocopa 2020 y la Copa América 2021 no catalogadas por misiones anteriores (excluye Wembley, Allianz Arena y Parken, ya existentes desde `MS-013`/`MS-017` y reutilizados aquí). Eurocopa 2020: Estadio de La Cartuja (Sevilla), Gazprom Arena/Krestovsky Stadium (San Petersburgo, techado — roof retráctil), Puskás Aréna (Budapest, techado `false`: el techo cubre la grada, no el terreno de juego, verificado explícitamente en la fuente para no marcarlo `true` por defecto), Arena Națională (Bucarest, techado — roof retráctil), Stadio Olimpico (Roma). Copa América 2021: Estádio Olímpico Nilton Santos (Río de Janeiro), Arena Pantanal (Cuiabá), Estádio Olímpico Pedro Ludovico (Goiânia). **Fuente:** búsqueda web activa durante esta misión (capacidad y altitud de cada ciudad/estadio, verificadas contra al menos una fuente independiente citada en `CHANGELOG.md`), no fuente primaria de confederación (no accesible desde este entorno) — clasificada como Fuente Secundaria por `docs/38`. **Limitación documentada:** la capacidad de varios estadios varía entre fuentes consultadas (ej. Arena Pantanal 41.390-44.000 según la fuente); se usó en cada caso el valor más consistentemente citado, nunca un promedio ni una estimación propia.

**Datos poblados en la Misión DATA-001:** 2 estadios reales adicionales (`EST-000074`, `EST-000075`) — Estadio Nacional Julio Martínez Prádanos (Santiago de Chile) y Neo Química Arena (São Paulo), sedes reales de partidos de Eliminatorias CONMEBOL 2026 de Brasil (jornadas 9 y 16) incorporados en esta misma misión. Ambas sedes ya habían sido identificadas como bloqueo pendiente desde `MS-019` (partidos Chile-Argentina y Brasil-Paraguay, ver hallazgo bajo la entidad `partidos.csv`) — quedan ahora catalogadas, aunque esos 2 partidos específicos no se incorporan en esta misión (fuera de su alcance exacto). Todas las sedes usadas por los 33 partidos de la Copa Mundial FIFA 2026 incorporados en esta misión ya estaban catalogadas desde `MS-017` — cero estadios nuevos necesarios para el Mundial 2026, verificado explícitamente antes de investigar cada partido para evitar trabajo duplicado (`docs/38`, "reutilización").

**Datos poblados en la Misión DATA-009:** 1 estadio real adicional (`EST-000076`, Hampden Park, Glasgow) — sede real de Escocia 0-2 República Checa (Eurocopa 2020, grupo D). De los 6 estadios que esta misión necesitaba para sus 13 partidos nuevos, 5 **ya existían** en este archivo bajo un nombre distinto al usado en la búsqueda inicial (Gazprom Arena/Krestovsky Stadium `EST-000067` ya catalogado por `MS-021` como "Gazprom Arena (Krestovsky Stadium)"; Stadio Olimpico `EST-000070` ya catalogado por `MS-021`; Parken `EST-000017`, Signal Iduna Park `EST-000037` y Levi's Stadium `EST-000048` ya catalogados por `MS-017`) — se detectó la duplicación por verificación cruzada antes de cerrar la misión (no al momento de escribir, ver `CHANGELOG.md` entrada `DATA-009`, "Hallazgo y autocorrección") y se corrigió eliminando las 5 filas duplicadas y reapuntando los `id_estadio` de los partidos afectados a los IDs ya existentes, sin dejar ningún duplicado ni referencia rota.

---

## 10. `competiciones.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_competicion` | STRING | PK | Integridad referencial: identificador único usado por `torneos.id_competicion` |
| `nombre` | STRING | | Trazabilidad/legibilidad en reportes de predicción |
| `confederacion_organizadora` | ENUM | | Contextualiza el nivel de exigencia esperado (Variable 011, Estado Psicológico/presión competitiva) y el organismo responsable de la fuente oficial de datos |
| `tipo` | ENUM | | Insumo directo de Índice de Caos y de la ponderación por tipo de partido (`docs/02-modelo.md`, Niveles A-D) |
| `periodicidad_anios` | INTEGER | | Contextualiza relevancia competitiva (vacío si la competición no sigue un ciclo fijo, ej. `tipo = amistoso` o `interconfederacion`) |
| `activa` | BOOLEAN | | Filtra competiciones vigentes |

**Restricciones:** `id_competicion` único, formato `COMP-NNNNNN` (6 dígitos); `nombre` único; `periodicidad_anios` > 0 cuando no está vacío.

**Relaciones:** referenciada por `torneos.id_competicion` (FK obligatoria — todo torneo pertenece a exactamente una competición).

**Valores de `confederacion_organizadora` (ENUM):** `FIFA`, `UEFA`, `CONMEBOL`, `CONCACAF`, `AFC`, `CAF`, `OFC` — mismos códigos de confederación usados en `selecciones.csv`. Excepción documentada: `CONMEBOL-UEFA` para competiciones organizadas conjuntamente por dos confederaciones (caso único actual: Finalissima). No se crea un valor genérico "conjunta" para evitar perder trazabilidad de qué organismos específicos participan.

**Valores de `tipo` (ENUM), definidos en esta misión (MS-006):**

| Valor | Significado | Ejemplo |
|---|---|---|
| `amistoso` | Partido bilateral sin fase de grupos ni eliminatoria | Amistosos Internacionales |
| `mundial` | Fase final de la Copa Mundial FIFA | Copa Mundial FIFA |
| `eliminatoria_mundial` | Proceso clasificatorio hacia la Copa Mundial FIFA, organizado por confederación bajo normativa FIFA | Eliminatorias Mundial FIFA |
| `continental` | Torneo de selecciones de una única confederación, formato grupos + eliminación directa | Eurocopa, Copa América, CONCACAF Gold Cup, Copa Asiática, Copa Africana de Naciones, OFC Nations Cup |
| `liga_naciones` | Formato de liga con ascenso/descenso entre divisiones, seguido de una fase final | UEFA Nations League |
| `interconfederacion` | Partido o serie entre campeones de dos confederaciones distintas, sin ciclo fijo | Finalissima |

**Datos de catálogo incluidos en la Misión 001:** fila `Amistosos Internacionales` (ver convención dedicada).

**Datos poblados en la Misión 006 (MS-006):** 10 competiciones internacionales relevantes para selecciones nacionales (`COMP-000002` a `COMP-000011`), verificadas mediante fuentes públicas ampliamente reconocidas (Wikipedia, UEFA.com, CAF Online, AFC, CONCACAF, CONMEBOL — ver `CHANGELOG.md` para el detalle de fuentes por competición). No se incluyen competiciones de clubes, categorías juveniles ni fútbol femenino — fuera del alcance actual del Modelo Santiago (predicción de partidos de selecciones absolutas masculinas). No se crean aún filas en `torneos.csv` para estas competiciones (ediciones específicas con fechas y sedes) — queda explícitamente diferido a una misión futura, conforme al alcance de MS-006.

**Nota sobre periodicidad variable:** algunas competiciones cambian de ciclo con el tiempo. La Copa Africana de Naciones (CAF) fue bienal hasta su edición 2027 inclusive; CAF anunció en diciembre de 2025 el paso a un ciclo cuatrienal a partir de 2028 para alinearse con la Eurocopa. Se almacena `periodicidad_anios = 4` por representar el ciclo vigente hacia el futuro, dejando esta nota como registro de la transición (evita invocar una migración de esquema para un campo que ya captura el estado más reciente y verificable).

---

## 11. `torneos.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_torneo` | STRING | PK | Integridad referencial (obligatorio en `partidos`, nunca nulo) |
| `id_competicion` | STRING | FK → `competiciones` | Relación obligatoria |
| `edicion` | STRING | | Trazabilidad/legibilidad temporal |
| `paises_organizadores` | STRING | | Insumo de Factores Externos (sede única vs. multisede afecta Localía, Variable 009) |
| `fecha_inicio` | DATE | | Delimita la ventana temporal de Rendimiento en el Torneo (Variable 002) |
| `fecha_fin` | DATE | | Idem |
| `formato` | STRING | | Contextualiza Índice de Caos (grupos + eliminación directa vs. liga) |
| `numero_selecciones_participantes` | INTEGER | | Contextualiza el nivel competitivo (vacío si `tipo` de la competición es `amistoso`) |

**Campo eliminado (decisión de esta misión):** `campeon_id_seleccion` — dato derivado de `partidos` (fila con `fase = final`), nunca almacenado.
**Restricciones:** `fecha_fin` ≥ `fecha_inicio`.
**Datos de catálogo incluidos en esta misión:** fila `TOR-2026-AMISTOSOS` (ver convención dedicada).
**Convención de `id_torneo` para "Eliminatorias Mundial FIFA" (fijada en `MS-015`):** `TOR-<año del Mundial>-ELIM-<CONFEDERACIÓN>` (ej. `TOR-2026-ELIM-CONMEBOL`) — una fila por confederación, no una sola fila para toda la competición `COMP-000003`, porque cada proceso clasificatorio real (CONMEBOL, UEFA, CONCACAF, AFC, CAF) tiene su propio calendario, formato y número de participantes, sin una sede ni un formato único que los agrupe. `paises_organizadores` usa la misma convención ya fijada para amistosos (`"N/A (sede variable, ver partidos.id_estadio)"`) para todo torneo sin una sede fija (clasificatorias; Nations League en su fase de liga).
**Datos poblados en la Misión MS-015:** 12 ediciones reales (13 filas de datos en total junto con `TOR-2026-AMISTOSOS`) — ver `CHANGELOG.md` para fuentes completas por torneo.
**Datos poblados en la Misión MS-021:** 2 ediciones reales adicionales (`TOR-2020-EUROCOPA`, `TOR-2021-COPAAMERICA`) — una **segunda edición** de dos competiciones ya catalogadas por `MS-015` (`COMP-000004`, `COMP-000006`), no una competición nueva. Primer caso en el módulo de dos filas de `torneos.csv` compartiendo el mismo `id_competicion` — confirma en la práctica que Variable003/004 (`N≥10` "dentro de una misma competición") deben interpretarse a nivel de `id_competicion` (agregando todas sus ediciones), no de `id_torneo` individual, ya que ninguna edición aislada permite matemáticamente llegar a 10 partidos para un mismo equipo (máximo posible: 7, equipo finalista). `TOR-2021-COPAAMERICA` documenta en `paises_organizadores` únicamente la sede final (`Brasil`) — la edición se organizó originalmente entre Argentina y Colombia, con Brasil asumiendo la sede completa semanas antes del inicio por la pandemia de COVID-19; se registra el dato final y verificable, y el cambio de sede se documenta como observación en `CHANGELOG.md`, no como un campo adicional del esquema.

---

# Próximos pasos (fuera de esta misión)

- Misión futura: estadísticas individuales de jugador por partido (goles, asistencias, minutos jugados, tarjetas), explícitamente diferida por decisión de esta misión.
- Incorporación de datos reales validados desde `data/raw/` siguiendo el flujo de `docs/05-Base-de-Conocimiento.md`.
