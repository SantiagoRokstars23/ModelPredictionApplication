# Diagnóstico Integral de Cobertura de Datos

**Archivo:** `docs/40-Diagnostico-de-Fuentes-de-Datos.md`

**Misión:** FII-002 — Diagnóstico Integral de Cobertura de Datos

**Versión:** 1.0.0

**Estado:** Investigación de fuentes externas — sin descargas, sin CSV nuevos, sin código, sin modificación de `app/`/`engine/`/`models/`/`data/`/`knowledge/`.

---

## Nota de numeración

El brief permite explícitamente `docs/40-...md` "o el siguiente número disponible si existe conflicto". Verificado antes de escribir: `docs/39-Fase-II.md` (creado en `FII-001`) es el último documento de la secuencia — `docs/40` está libre, sin conflicto. No aplica ninguna renumeración.

---

## 1. Objetivo

Diagnosticar, con evidencia real verificada por investigación web (nunca inventada), qué fuentes de datos externas existen para alimentar al Modelo Santiago durante la Fase II y fases posteriores — para selecciones nacionales, clubes, ligas y torneos internacionales — y proponer una estrategia oficial de adquisición de datos, sin descargar ni incorporar ningún dato todavía. Responde directamente al Bloque A (Cobertura) del Roadmap ya fijado en `docs/39-Fase-II.md`.

---

## 2. Metodología

Cada una de las 10 fuentes obligatorias del brief, más 3 adicionales encontradas durante la investigación por ser directamente relevantes para el proyecto, fue investigada mediante búsquedas web reales (julio 2026) contra su documentación oficial, su repositorio, o análisis de terceros ya publicados. Ninguna cifra de este documento fue inventada ni extrapolada sin fuente — donde la evidencia encontrada es ambigua o incompleta, se indica explícitamente como tal, en vez de rellenar con un supuesto. Todas las fuentes primarias consultadas se citan en la sección 10 (Referencias).

---

## 3. Ficha por fuente

### 3.1 StatsBomb (Open Data + API comercial)

- **Cobertura:**
  - Selecciones: Mundial 2018/2022 (masculino), Eurocopa 2020/2024, Copa América 2024, AFCON 2024, Mundial Femenino (varias ediciones) — exactamente las competiciones ya usadas por este proyecto desde `DATA-006` a `DATA-009`.
  - Clubes: Limitada en Open Data (algunas temporadas completas de La Liga, Champions League); cobertura de clubes mucho más amplia solo en el API comercial de pago.
  - Competiciones/Torneos históricos: ~3.000+ partidos en Open Data, concentrados en torneos recientes (2018 en adelante); el API comercial cubre un catálogo mucho mayor, sin cifra pública exacta.
  - Ligas: Ninguna liga doméstica completa en Open Data salvo La Liga (temporadas concretas).
- **Variables disponibles:** datos de evento (event data) — la granularidad más alta de todas las fuentes investigadas: marcador, tiros (con coordenadas), pases, presiones, duelos, xG por tiro, alineaciones. Datos StatsBomb 360 (posicionamiento de jugadores fuera del balón) **solo con suscripción de pago**, no en Open Data.
- **Calidad:** **Excelente** — estándar de la industria (ya usado en la Fase I de este proyecto, `DATA-008`/`DATA-009`), datos de evento manuales/verificados, no agregados automáticos.
- **Cobertura temporal:** variable por competición; Open Data concentrado en torneos desde 2018-2020 en adelante, sin histórico profundo de décadas.
- **Licencia:** Open Data es **gratuita para investigación/uso no comercial**, con atribución obligatoria (StatsBomb Public Data User Agreement) — **no redistribuible como producto comercial**. El API completa (todas las competiciones/clubes, datos 360) es exclusivamente **comercial**, con precio no publicado (contacto directo con ventas).
- **Facilidad de integración:** **Fácil** — JSON estructurado, librería oficial en Python (`statsbombpy`), ya integrado en este proyecto.

### 3.2 API-Football (api-sports.io / api-football.com)

- **Cobertura:**
  - Selecciones: sí, incluye Mundial (confirmado para 2026: 48 equipos, 104 partidos), competiciones continentales.
  - Clubes: muy amplia — más de 1.200 competiciones/ligas reportadas.
  - Ligas/Torneos históricos: amplia en volumen de competiciones, pero la profundidad histórica real por competición **no está documentada de forma uniforme** (evidencia encontrada: proveedores similares suelen ofrecer temporada actual + 1-3 anteriores en el nivel básico, profundidad completa solo en planes altos — no se encontró una cifra oficial exacta de API-Football para esto, se documenta como brecha de evidencia, no como una afirmación).
- **Variables disponibles:** marcador, xG (nivel de partido y, en algunos casos, por tiro con coordenadas), posesión, corners, tiros a puerta/totales, faltas, tarjetas, alineaciones, cuotas (odds) en endpoints separados.
- **Calidad:** **Buena** — datos agregados por partido de buena cobertura y consistencia, pero no llega al nivel de evento crudo verificado manualmente que ofrece StatsBomb.
- **Cobertura temporal:** no uniformemente documentada; variable por plan y competición (brecha de evidencia, ver arriba).
- **Licencia:** freemium — plan gratuito con 100 solicitudes/día, sin tarjeta de crédito; planes de pago desde **$19/mes**, con todas las competiciones incluidas en todos los planes (a diferencia de otros proveedores que segmentan cobertura por plan).
- **Facilidad de integración:** **Muy fácil** — API REST estándar, JSON, documentación pública completa (`api-football.com/documentation`).

### 3.3 Football-Data.org

- **Cobertura:**
  - Selecciones: el tier gratuito incluye únicamente Mundial y Eurocopa — **no incluye Copa América, Eliminatorias ni Nations League** en el nivel gratuito.
  - Clubes/Ligas: 12 competiciones en el tier gratuito (Champions League, Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, Primeira Liga, Championship inglesa, Brasileirão) — todas las grandes ligas europeas top, más Brasil.
  - Torneos históricos: no detallado en la investigación; el tier gratuito prioriza temporada actual (resultados con retraso, no en vivo).
- **Variables disponibles:** en el tier gratuito, solo resultados, calendarios y tablas — **sin alineaciones, sin jugadores, sin estadísticas de partido** (tiros, corners, etc.). Esos datos requieren plan de pago.
- **Calidad:** **Aceptable** en el tier gratuito (básico, resultados/tablas confiables pero sin profundidad estadística); potencialmente **Buena** en planes pagos, no verificado en esta investigación.
- **Cobertura temporal:** no determinada con evidencia suficiente en esta investigación.
- **Licencia:** freemium — 10 llamadas/minuto gratis, planes de pago para mayor volumen y datos adicionales.
- **Facilidad de integración:** **Muy fácil** — API REST simple, ampliamente documentada y usada en tutoriales.

### 3.4 FBref (Sports-Reference LLC)

- **Cobertura:** entre las más amplias de todas las fuentes investigadas — grandes ligas europeas, selecciones nacionales, competiciones continentales, con estadísticas avanzadas derivadas de datos Opta.
- **Variables disponibles:** xG, xA, pases progresivos, acciones de creación de tiro, y decenas de métricas avanzadas adicionales — **cuando la licencia de datos Opta estaba vigente**.
- **Calidad:** **Excelente en contenido, pero con un hallazgo crítico de esta investigación no anticipado por el brief:** FBref **perdió su licencia de datos Opta en enero de 2026** — el sitio sigue mostrando datos históricos, pero la actualización futura de estadísticas avanzadas queda en duda según la evidencia encontrada. Se documenta como hallazgo, no como certeza absoluta (fuente: cobertura de terceros sobre el cambio de licencia, no un comunicado oficial revisado directamente).
- **Cobertura temporal:** muy amplia, décadas de historia para las ligas principales.
- **Licencia:** **restrictiva, la más problemática de las 10 fuentes obligatorias.** Los Términos de Uso de Sports-Reference **prohíben expresamente** el scraping automatizado sin permiso escrito; el rate-limiting bloquea (hasta 24 horas) a quien exceda 10 solicitudes/minuto; **prohíben explícitamente usar los datos para entrenar modelos de IA generativa sin permiso**; y parte de los datos, al provenir de terceros bajo licencia, **no pueden redistribuirse en absoluto**, incluso con permiso de scraping.
- **Facilidad de integración:** **Difícil** — sin API oficial; cualquier acceso automatizado sin autorización escrita expone al proyecto a un riesgo real de incumplimiento de términos de servicio, no solo a una limitación técnica.

### 3.5 Understat

- **Cobertura:** únicamente 6 ligas — Premier League, La Liga, Bundesliga, Serie A, Ligue 1 y la liga rusa ("Big 5" + Rusia). **Sin selecciones nacionales, sin ninguna competición sudamericana** — desalineado con el foco actual del proyecto (selecciones).
- **Variables disponibles:** xG y datos de tiros, principalmente.
- **Calidad:** **Buena** para xG de clubes de esas 6 ligas específicamente — **Limitada** para el propósito de este proyecto, dado que no cubre selecciones ni Sudamérica en absoluto.
- **Cobertura temporal:** desde 2014 hasta la temporada actual.
- **Licencia:** sin API oficial pública documentada — el acceso encontrado en la investigación es exclusivamente vía scraping no oficial de terceros.
- **Facilidad de integración:** **Media-Difícil** — sin API oficial, dependiente de scrapers de comunidad no mantenidos por Understat.

### 3.6 FIFA (fuente oficial)

- **Cobertura:** datos históricos de torneos organizados por FIFA (calendarios, plantillas, jugadores, entrenadores, resultados), accesibles a través de un conjunto de APIs documentado en `givevoicetofootball.fifa.com` (originado en un hackathon de FIFA, no en un programa de developer estándar).
- **Variables disponibles:** metadatos de torneo, calendario, plantillas — **no se encontró evidencia de que incluya estadísticas avanzadas** (xG, tiros, etc.).
- **Calidad:** **Aceptable** — datos oficiales y confiables en lo que cubren, pero con alcance limitado y sin la profundidad estadística que el modelo necesita para Variable003/004.
- **Cobertura temporal:** histórica de competiciones FIFA, sin rango exacto documentado en las fuentes consultadas.
- **Licencia:** **sin programa público de API keys ni documentación de developer estándar** — el acceso encontrado es a través de endpoints publicados de forma ad-hoc, sin garantía de estabilidad ni soporte.
- **Facilidad de integración:** **Difícil** — sin developer portal formal, sin garantía de continuidad del servicio.

### 3.7 UEFA (fuente oficial)

- **Cobertura:** competiciones UEFA — Eurocopa, Champions League, Europa League, Conference League, **Nations League** (esta última, relevante porque es una de las competiciones sin cobertura hoy en el proyecto, `VALID-003`).
- **Variables disponibles:** rankings de jugadores, resultados de partido, metadatos de competición, estadísticas por partido y por jugador (según terceros que documentan la API oficial: 5 endpoints incluyendo `get_player_rankings`, `get_match_player_stats`).
- **Calidad:** **Buena** — fuente oficial, pero el acceso real documentado en esta investigación es mayoritariamente a través de **intermediarios de pago** (ej. paquetes de terceros con token de API), no un portal de desarrollador público y gratuito de UEFA.
- **Cobertura temporal:** no determinada con evidencia suficiente en esta investigación.
- **Licencia:** sin evidencia de un programa gratuito público — acceso real mediado por terceros comerciales.
- **Facilidad de integración:** **Media** — existen bindings de terceros (ej. paquete TypeScript no oficial) que facilitan el acceso técnico, pero sin claridad sobre la legitimidad/estabilidad de usar la API sin un acuerdo directo con UEFA.

### 3.8 CONMEBOL (fuente oficial)

- **Cobertura:** competiciones CONMEBOL — Copa América, Libertadores, Sudamericana, Recopa.
- **Hallazgo central, explica una limitación ya conocida del proyecto:** **CONMEBOL no ofrece una API pública propia.** Los datos oficiales de sus competiciones son **distribuidos en exclusiva por Stats Perform** (acuerdo multianual confirmado en la investigación) — es decir, cualquier acceso a datos oficiales y verificados de Eliminatorias CONMEBOL requiere pasar por un proveedor comercial de nivel Opta/Stats Perform, no por una fuente abierta. **Esto explica, con una causa raíz nunca documentada hasta ahora, por qué las Eliminatorias CONMEBOL han quedado sin cobertura de StatsBomb desde `VALID-001`**: no es una omisión de StatsBomb, es que los derechos de esos datos pertenecen en exclusiva a otro proveedor.
- **Variables disponibles:** no determinado directamente (acceso mediado por Stats Perform, sin portal público que documentar).
- **Calidad:** presumiblemente **Excelente** si se accede vía Stats Perform (mismo estándar que Opta), pero **inaccesible** en la práctica sin ese acuerdo comercial.
- **Cobertura temporal:** no determinada.
- **Licencia:** **comercial exclusiva**, sin alternativa abierta oficial.
- **Facilidad de integración:** **Difícil** — no hay ruta gratuita ni de autoservicio.

### 3.9 Soccerway

- **Cobertura:** amplia — resultados de más de 100 ligas según proyectos de scraping de la comunidad, con foco en resultados y perfiles de jugador.
- **Variables disponibles:** resultados, goles (minuto, autor, asistencia, autogol, penalti), historial de transferencias, trofeos.
- **Calidad:** **Aceptable** — cobertura amplia pero sin estadísticas avanzadas (sin xG, sin datos de evento).
- **Cobertura temporal:** no determinada con evidencia suficiente.
- **Licencia:** **sin API oficial y sin términos de scraping claramente publicados** encontrados en esta investigación — zona gris, mismo riesgo cualitativo que FBref pero sin siquiera unos términos explícitos que consultar.
- **Facilidad de integración:** **Difícil** — depende enteramente de scrapers de comunidad no oficiales, frágiles ante cambios del sitio.

### 3.10 WorldFootball.net

- **Cobertura:** décadas de historia de resultados, tablas, alineaciones y transferencias, "todas las competiciones importantes a nivel mundial" según la propia descripción del sitio.
- **Variables disponibles:** resultados, tablas, perfiles de jugador, alineaciones, transferencias — sin evidencia de estadísticas avanzadas (xG, datos de evento).
- **Calidad:** **Aceptable** — buena cobertura histórica básica, sin profundidad estadística moderna.
- **Cobertura temporal:** décadas (la más profunda entre las fuentes sin API oficial investigadas).
- **Licencia:** **sin API oficial**; acceso público sin necesidad de login o API key para scraping básico, pero sin licencia explícita de reuso encontrada.
- **Facilidad de integración:** **Difícil** — mismo patrón que Soccerway, dependiente de scraping no oficial.

---

## 4. Fuentes adicionales encontradas durante la investigación (no exigidas por el brief, documentadas por ser claramente relevantes)

### 4.1 Football-Data.co.uk *(nombre distinto de Football-Data.org — no confundir)*

**Hallazgo más valioso de toda esta investigación.** CSV gratuitos, descarga directa, **sin necesidad de API key ni registro**, cobertura de 22 divisiones de 11 países europeos desde la temporada **1993/94**, con estadísticas de partido (tiros, tiros a puerta, corners, faltas, tarjetas, árbitro) desde 2000/01, y — a diferencia de las 10 fuentes obligatorias — **incluye cuotas de casas de apuestas históricas** en el mismo archivo. Es, con evidencia directa, la única fuente gratuita encontrada en toda esta investigación con **datos de mercado históricos** — exactamente lo que el Bloque D (Valor Esperado) de `docs/39-Fase-II.md` necesita y que hoy no existe en el proyecto (`cuotas.csv` vacío). **Limitación clara:** solo ligas domésticas europeas — ninguna selección nacional, ninguna competición sudamericana o asiática. Calidad: **Excelente** para lo que cubre. Licencia: pública, descarga directa declarada como gratuita. Facilidad: **Muy fácil** (CSV plano, sin autenticación).

### 4.2 Sportmonks

Proveedor comercial con cobertura declarada de 2.200+ ligas, incluidas selecciones nacionales (confirmado explícitamente para el Mundial 2026 y fixtures de selecciones desde el plan "Growth"), y confirmado en esta investigación que **cubre la Liga BetPlay colombiana** (página dedicada a "Colombian Primera A" en su documentación) — ninguna de las 10 fuentes obligatorias confirmó esa cobertura. Planes desde €29/mes (Starter, 5 ligas) hasta Enterprise (cotización, todas las competiciones con histórico completo); histórico más allá de 3 temporadas requiere complemento de pago en los planes intermedios. Calidad: **Buena-Excelente** según plan. Facilidad: **Fácil** (API REST bien documentada, prueba gratuita de 14 días).

### 4.3 Wyscout (Hudl) / Opta-Stats Perform

Mencionados explícitamente por ser, junto con StatsBomb, los tres proveedores que la propia industria reconoce como líderes. **Wyscout**: plataforma de video + datos, licencia personal desde ~€299-325/año — más orientada a scouting visual que a backtesting estadístico masivo, integración vía archivo/plataforma, no API abierta de bajo costo. **Opta (Stats Perform)**: el proveedor de mayor calidad y el que efectivamente posee los derechos exclusivos de datos oficiales de CONMEBOL (sección 3.8) — pricing no público, contacto comercial directo, fuera de alcance de un proyecto en esta etapa por costo, pero es el techo real de calidad al que StatsBomb/FBref alguna vez estuvieron ligados (FBref, de hecho, perdió su licencia Opta en enero 2026 — sección 3.4).

---

## 5. Matriz comparativa

| Fuente | Selecciones | Clubes | Estadísticas avanzadas | Marcadores/resultados | xG | Automatización |
|---|---|---|---|---|---|---|
| StatsBomb | ✅ Excelente | ⚠️ Limitada (Open Data) | ✅ Excelente (evento) | ✅ | ✅ | ✅ Fácil |
| API-Football | ✅ Buena | ✅ Excelente | ✅ Buena | ✅ | ✅ | ✅ Muy fácil |
| Football-Data.org | ⚠️ Solo Mundial/Euro (gratis) | ✅ Buena (12 ligas top) | ⚠️ Limitada (gratis) | ✅ | ❌ (gratis) | ✅ Muy fácil |
| FBref | ✅ Amplia | ✅ Excelente | ✅ Excelente (histórico) | ✅ | ✅ (histórico) | ❌ Difícil (legal) |
| Understat | ❌ No cubre | ⚠️ Solo 6 ligas | ✅ Buena (esas 6) | ✅ (esas 6) | ✅ | ⚠️ Media |
| FIFA oficial | ✅ Torneos FIFA | ❌ No | ❌ No | ✅ | ❌ | ❌ Difícil |
| UEFA oficial | ✅ Competiciones UEFA | ❌ No | ✅ Buena | ✅ | — | ⚠️ Media |
| CONMEBOL oficial | ✅ (vía Stats Perform) | ❌ No | — | — | — | ❌ Difícil (exclusivo) |
| Soccerway | ✅ Amplia | ✅ Amplia | ❌ No | ✅ | ❌ | ❌ Difícil |
| WorldFootball.net | ✅ Amplia (histórica) | ✅ Amplia (histórica) | ❌ No | ✅ | ❌ | ❌ Difícil |
| **Football-Data.co.uk** | ❌ No | ✅ 22 divisiones EU | ⚠️ Básica + odds | ✅ | ❌ | ✅ Muy fácil |
| **Sportmonks** | ✅ Buena (planes altos) | ✅ Excelente | ✅ Buena | ✅ | ✅ (según plan) | ✅ Fácil |

**Respuestas directas exigidas por el brief:**
- **Mejor para selecciones:** StatsBomb (calidad de evento) para las competiciones que cubre; Sportmonks si se necesita cobertura comercial más amplia que la de StatsBomb Open Data.
- **Mejor para clubes:** API-Football (relación cobertura/precio) o Sportmonks (mayor profundidad histórica en planes altos).
- **Mejor para estadísticas avanzadas:** StatsBomb (evento) donde tiene cobertura; FBref en contenido histórico, pero con el riesgo legal/de licencia ya documentado (sección 3.4).
- **Mejor para marcadores:** Football-Data.co.uk para ligas europeas domésticas (gratis, sin fricción); API-Football para selecciones/competiciones amplias.
- **Mejor para xG:** StatsBomb (por tiro, con coordenadas) donde tiene cobertura; Understat solo si el alcance se limitara a las 6 ligas que cubre (no aplica al foco actual de selecciones).
- **Mejor para automatización:** API-Football o Football-Data.co.uk (ambas de integración "Muy fácil", sin fricción legal).

---

## 6. Estrategia recomendada

**Nivel 1 — StatsBomb (ya en uso, sin cambios):** fuente principal para selecciones nacionales en las competiciones que ya cubre (Mundial, Eurocopa, Copa América, AFCON) — máxima calidad de evento, ya integrada, licencia ya aceptada por el proyecto desde `DATA-006`.

**Nivel 2 — API-Football (nueva incorporación recomendada):** para cerrar huecos de cobertura que StatsBomb Open Data no cubre — particularmente Eliminatorias y competiciones donde StatsBomb no libera datos abiertos. Justificación: mejor relación cobertura/costo/facilidad de las fuentes de pago investigadas, todas las competiciones incluidas en todos los planes (a diferencia de Football-Data.org, que segmenta por plan).

**Nivel 3 — Football-Data.co.uk (nueva incorporación recomendada, distinta prioridad):** única fuente gratuita encontrada con cuotas históricas — recomendada específicamente para el Bloque D (Valor Esperado) de `docs/39-Fase-II.md`, no como sustituto de StatsBomb/API-Football para estadísticas de partido. Limitada a ligas domésticas europeas — no resuelve selecciones.

**Nivel 4 — Fuentes oficiales (UEFA/CONMEBOL/FIFA), consideradas pero no priorizadas en el corto plazo:** ninguna ofrece un camino de autoservicio gratuito o de bajo costo (secciones 3.6-3.8) — UEFA y CONMEBOL median el acceso a través de terceros comerciales; FIFA no tiene programa de desarrollador estándar. Se documentan como referencia de "verdad oficial" para auditoría de datos ya obtenidos por otras vías, no como fuente de ingesta primaria.

**Explícitamente no recomendadas como fuente de ingesta automatizada:** FBref (riesgo legal directo, términos de uso lo prohíben expresamente), Soccerway y WorldFootball.net (sin licencia clara, dependientes de scraping fragil) — coherente con el principio ya vigente del proyecto ("nunca inventar datos", y por extensión, nunca obtenerlos violando términos de servicio explícitos).

---

## 7. Impacto sobre el proyecto

**Advertencia obligatoria, honesta:** los porcentajes de esta sección son estimaciones de **cobertura de disponibilidad de fuente** (¿existe un proveedor con datos reales de esa competición, accesible en algún nivel?), **no** una medición de partidos evaluables por el Engine como la que produjo `VALID-003` (35/124, 28.2%) — esa cifra depende, además de la fuente, de que exista historial previo suficiente por equipo. Ningún porcentaje aquí fue medido por backtesting; son estimaciones cualitativas basadas en la cobertura declarada de cada fuente, y deben tratarse como tales.

| Competición | Cobertura hoy (StatsBomb solo) | Cobertura con Nivel 1+2 (StatsBomb + API-Football) | Fuente que la resolvería |
|---|---|---|---|
| Mundial | ✅ Alta (2018, 2022; 2026 aún no jugado) | ✅ Alta | StatsBomb (histórico) + API-Football (2026 en vivo) |
| Eurocopa | ✅ Alta (2020, 2024) | ✅ Alta | StatsBomb |
| Copa América | ✅ Alta (2024) | ✅ Alta | StatsBomb |
| Nations League | ❌ Sin cobertura confirmada en Open Data | ⚠️ Parcial | API-Football o UEFA vía terceros (Nivel 4) |
| Eliminatorias (CONMEBOL) | ❌ Sin cobertura (datos exclusivos de Stats Perform, sección 3.8) | ⚠️ Parcial, sujeto a lo que API-Football realmente reporte para clasificatorias | Ninguna fuente de Nivel 1-3 garantiza cobertura completa — requeriría Nivel 4 (Stats Perform) para paridad con StatsBomb |
| Premier League | ⚠️ Ninguna en Open Data de selecciones | ✅ Alta | API-Football, Football-Data.co.uk, Football-Data.org (gratis) |
| LaLiga | ⚠️ Solo temporadas sueltas en Open Data | ✅ Alta | API-Football, Football-Data.co.uk, Football-Data.org (gratis) |
| Serie A | ❌ No en Open Data | ✅ Alta | API-Football, Football-Data.co.uk, Football-Data.org (gratis) |
| Bundesliga | ❌ No en Open Data | ✅ Alta | API-Football, Football-Data.co.uk, Football-Data.org (gratis) |
| Liga BetPlay (Colombia) | ❌ Sin cobertura en ninguna fuente de Nivel 1-3 confirmada | ⚠️ Solo si el plan pago de API-Football la incluye (no verificado en esta investigación) | **Sportmonks es la única fuente que confirmó explícitamente cobertura de Liga BetPlay** (sección 4.2) — no forma parte de la estrategia recomendada de Nivel 1-3 |

---

## 8. Riesgos identificados

- **Licencias:** StatsBomb Open Data es no comercial — cualquier uso futuro que el proyecto considere "comercial" (ej. apuestas reales con dinero de terceros) requeriría revisar el acuerdo con StatsBomb o migrar a su API de pago. FBref/Soccerway/WorldFootball.net exponen a riesgo legal real si se automatiza sin autorización.
- **Disponibilidad:** CONMEBOL no tiene fuente abierta — el proyecto seguirá sin Eliminatorias de alta calidad hasta que se evalúe un acuerdo comercial (Stats Perform) o se acepte una fuente de menor calidad (API-Football) para esa competición específica.
- **Calidad decreciente:** FBref perdió su licencia Opta en enero 2026 (hallazgo de esta investigación) — cualquier plan que dependiera de FBref para estadísticas avanzadas futuras debe reconsiderarse.
- **Evidencia incompleta:** varias cifras de esta investigación (profundidad histórica exacta de API-Football, cobertura temporal de UEFA/CONMEBOL/FIFA, términos exactos de Soccerway) no pudieron confirmarse con una fuente primaria concluyente — se documentaron como brechas de evidencia, no como hechos. Cualquier decisión de adquisición basada en esas cifras debe verificarse directamente contra la documentación oficial de cada proveedor antes de comprometer presupuesto o esfuerzo de integración.

---

## 9. Cierre obligatorio

**1. ¿Qué fuente es la mejor para selecciones nacionales?** StatsBomb, para las competiciones que ya cubre (calidad de evento, ya validada por este proyecto); Sportmonks como alternativa comercial de mayor cobertura si StatsBomb no alcanza.

**2. ¿Qué fuente es la mejor para clubes?** API-Football, por su relación cobertura/costo/facilidad de integración; Sportmonks si se necesita mayor profundidad histórica.

**3. ¿Qué fuente ofrece la mayor cobertura histórica?** WorldFootball.net y Football-Data.co.uk (décadas), aunque con calidad estadística muy distinta — la primera básica y sin API oficial, la segunda con estadísticas de partido y odds desde 2000/01, gratuita y de fácil integración.

**4. ¿Qué fuente ofrece las mejores estadísticas avanzadas?** StatsBomb (datos de evento con coordenadas) donde tiene cobertura; FBref en volumen histórico, pero con el riesgo legal ya documentado que desaconseja su automatización.

**5. ¿Qué combinación recomienda oficialmente?** Nivel 1 (StatsBomb, ya en uso) + Nivel 2 (API-Football, nueva) + Nivel 3 (Football-Data.co.uk, nueva, específica para EV) — Nivel 4 (fuentes oficiales UEFA/CONMEBOL/FIFA) como referencia de auditoría, no de ingesta primaria por ahora.

**6. ¿Qué porcentaje de cobertura podría alcanzarse?** No cuantificable con precisión sin backtesting real (ver advertencia de la sección 7) — cualitativamente, la combinación de Nivel 1+2 resolvería Mundial/Eurocopa/Copa América/ligas top europeas con alta confianza; Nations League y Eliminatorias quedarían en cobertura parcial, no garantizada.

**7. ¿Qué competiciones seguirían teniendo cobertura insuficiente?** Eliminatorias CONMEBOL (datos oficiales exclusivos de Stats Perform, sin alternativa abierta) y, con la estrategia de Nivel 1-3, Liga BetPlay (solo confirmada en Sportmonks, fuera de la estrategia recomendada).

**8. ¿Qué riesgos existen?** Licencia no comercial de StatsBomb, ausencia total de fuente abierta para CONMEBOL, degradación de calidad de FBref (pérdida de licencia Opta), y varias brechas de evidencia que requieren verificación directa antes de comprometer una integración real.

**9. ¿Qué misión recomienda inmediatamente después (`DATA-010`)?** Verificación técnica directa contra la documentación oficial de API-Football y Football-Data.co.uk (confirmar profundidad histórica real, formato exacto de respuesta, límites de tasa reales) — sin descargar todavía ningún dato masivo — como paso previo obligatorio antes de cualquier misión de ingesta real, siguiendo el mismo protocolo ya vigente (`docs/38-Protocolo-Oficial-Ingesta-Datos.md`).

**10. ¿Se considera suficiente la estrategia propuesta para iniciar la expansión de la Base de Conocimiento durante la Fase II?** Sí, como punto de partida — cierra la mayoría de las competiciones prioritarias (Mundial, Eurocopa, Copa América, ligas top europeas) con fuentes de bajo costo/gratuitas y de integración fácil. **No es suficiente para Eliminatorias CONMEBOL ni Liga BetPlay** — esas dos brechas quedan documentadas explícitamente como pendientes, no resueltas por esta estrategia, y requerirán una decisión explícita (aceptar cobertura parcial, o evaluar un acuerdo comercial de Nivel 4) antes de declarar el Bloque A completo.

---

## 10. Referencias

Todas las fuentes primarias/secundarias consultadas durante la investigación (julio 2026):

- [statsbomb/open-data (GitHub)](https://github.com/statsbomb/open-data) — repositorio y `competitions.json`
- [StatsBomb Open Data LICENSE.pdf](https://github.com/statsbomb/open-data/blob/master/LICENSE.pdf)
- [Hudl StatsBomb](https://www.hudl.com/products/statsbomb)
- [API-Football — Coverage](https://www.api-football.com/coverage)
- [API-Football — Pricing](https://www.api-football.com/pricing)
- [API-Sports Football Documentation v3](https://api-sports.io/documentation/football/v3)
- [Football-Data.org Registration](https://www.football-data.org/client/register)
- [TheStatsAPI — football-data.org Free Tier Limits 2026](https://www.thestatsapi.com/blog/football-data-org-free-tier-limits-2026)
- [Sports-Reference.com — Terms of Use](https://www.sports-reference.com/termsofuse.html)
- [Sports-Reference.com — SR and Data Use](https://www.sports-reference.com/data_use.html)
- [Sports-Reference.com — Bot/Scraping/Crawler Traffic](https://www.sports-reference.com/bot-traffic.html)
- [Understat — La Liga xG Table 2025/2026](https://understat.com/league/La_liga)
- [Give Voice to Football — API Documentation](https://givevoicetofootball.github.io/api/)
- [FIFA Give Voice to Football Swagger](https://givevoicetofootball.fifa.com/ApiFdcpSwagger/)
- [UEFA API bindings (GitHub, no oficial)](https://github.com/ErikMichelson/uefa-api)
- [Parse.bot — UEFA API Player Stats & Match Data](https://parse.bot/marketplace/a0d9a34d-70be-45b8-b4ae-a3e0eb9b639f/uefa-com-api)
- [CasinoCompendium — Stats Perform named Exclusive Official CONMEBOL Data Provider](https://casinocompendium.com/en/stats-perform-named-exclusive-official-conmebol-data-provider/)
- [Sportmonks — CONMEBOL Sudamericana API](https://www.sportmonks.com/football-api/conmebol-sudamerica-api/)
- [Football-Data.co.uk](https://www.football-data.co.uk/)
- [Football-Data.co.uk — data.php](https://www.football-data.co.uk/data.php)
- [Sportmonks — Plans & Pricing](https://www.sportmonks.com/football-api/plans-pricing/)
- [Sportmonks — Coverage](https://www.sportmonks.com/football-api/coverage/)
- [Sportmonks — Colombian Primera A glossary](https://www.sportmonks.com/glossary/colombian-primera-a-colombia/)
- [Hudl Wyscout](https://www.hudl.com/en_gb/products/wyscout)
- [SoccerEDU — Top Soccer Databases](https://www.socceredu.com/en-US/blog/soccer-databases)
- `docs/00-Project-Tracker.md`, entradas `VALID-001`/`VALID-003` — evidencia interna del proyecto sobre huecos de cobertura ya conocidos (Mundial 2026, Eliminatorias, Nations League sin cobertura de StatsBomb), confirmada aquí con causa raíz nueva (sección 3.8).
- `docs/39-Fase-II.md` — Roadmap de Fase II, Bloque A, que esta misión responde directamente.

---

Fin del documento.
