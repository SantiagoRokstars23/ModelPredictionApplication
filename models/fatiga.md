# Fatiga — Variable007 (alcance reducido V1)

**Archivo:** `models/fatiga.md`

**Misión:** MODEL-014 — Especificación Matemática Oficial de Variable007 (Fatiga)

**Versión:** 1.0.0-investigación

**Estado:** Investigación — primer documento de `models/` dedicado a Variable007 (no evoluciona un stub, se crea desde cero, mismo patrón que `MODEL-005`/`MODEL-011`/`MODEL-012`/`MODEL-013`)

---

## Nota de origen y alcance exacto de esta misión

Variable007 (Fatiga) tiene, según `docs/03-Variables.md`, tres señales: "Días de descanso", "Minutos jugados", "Viajes". `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) ya evaluó su disponibilidad de dato y concluyó: "Días de descanso" y "Viajes" son categoría C (derivables hoy sin ninguna captura nueva); "Minutos jugados" es categoría D (no existe — estadística individual de jugador por partido, explícitamente diferida desde `MS-001`, confirmado también por `docs/27-Auditoria-de-Variables-Pendientes.md`). `docs/36` autoriza explícitamente "una V1 con solo 'Días de descanso' + 'Viajes'" — **esta misión especifica exactamente ese alcance reducido, no Variable007 completa**. Se responde de forma explícita, como exige el brief: **Variable007 completa (con "Minutos jugados") no puede especificarse con el esquema de datos actual** — sección 11 desarrolla este hallazgo con evidencia directa.

Ningún documento de arquitectura funcional (`docs/17-Matriz-de-Consumo-de-Variables.md`) fija todavía una fuente y forma exactas para Variable007, a diferencia de Variable008 (`MODEL-013`, que ya partía de "conteo, sin fórmula fijada"). Esta misión, por lo tanto, fija tanto la fuente/forma como la fórmula matemática — mismo nivel de trabajo que `MODEL-011`/`MODEL-012` hicieron para Variable001/002.

---

# 1. Objetivo

Definir la fórmula matemática completa que transforma "Días de descanso" y "Viajes" en el índice `Fatiga` (0-100) que `VariablePreparation` podrá implementar para Variable007 en su alcance reducido V1, eliminando el estado "método pendiente" (`docs/03`, `docs/28`: "Pendiente") para esas dos señales — sin implementar código, sin modificar el Runtime, `PredictionContext`, `Engine01`, `Engine02`, `Engine04` ni `VariablePreparation`.

---

# 2. Definición operacional exacta

**Fatiga** mide el desgaste físico relativo de un equipo de cara a un partido específico, combinando dos señales relativas, ambas comparadas contra la población de selecciones que participan en el mismo torneo del partido a predecir:

- **Escasez de descanso:** cuántos días han transcurrido desde el partido oficial más reciente del equipo hasta la fecha del partido a predecir, en relación con el mismo indicador de las demás selecciones del torneo — menos días de descanso que sus pares implica mayor fatiga relativa.
- **Desplazamiento geográfico:** si el equipo debe viajar de sede respecto de su partido anterior para llegar a la sede del partido a predecir (misma ciudad, mismo país o distinto país) — mayor desplazamiento implica mayor fatiga.

**Convención de dirección (consistente con `models/chaos-index.md` §6, "`Δ_fatiga`: fatiga suma caos" y con Variable007 = "Nivel B", `docs/02-modelo.md`):** valores altos de `Fatiga` representan **mayor** desgaste físico (peor estado), no mejor. Es la dirección opuesta a Variable006 (Disponibilidad de Plantilla, donde alto = mejor) — se documenta explícitamente para no introducir ambigüedad en `Engine01`/`Engine02`/`Engine04` al consumir el valor.

No mide "Minutos jugados" (sección 11) ni ningún otro insumo no autorizado por `docs/03` (ej. no usa edad de plantilla, no usa carga de club) — es, exclusivamente, una medida relativa de descanso insuficiente y desplazamiento geográfico.

---

# 3. Problema que resuelve

`docs/03`/`docs/28` marcan Variable007 con "Método: Pendiente" pese a que dos de sus tres señales ya son derivables hoy sin ninguna captura nueva (`docs/27`, `docs/36`/`GR-010`). Sin una fórmula matemática oficial, `VariablePreparation` no puede publicar Variable007 con dato real aunque el alcance reducido y la fuente ya estén disponibles — la misma brecha que `MODEL-011`/`MODEL-012`/`MODEL-013` ya cerraron para Variable001/002/008. `GR-010` (`docs/36`) recomendó explícitamente esta investigación como la prioridad inmediatamente posterior a `MODEL-013`.

---

# 4. Fundamento — por qué dos mecanismos matemáticos distintos, no uno solo

**Por qué "Escasez de descanso" reutiliza el mecanismo z-score/Φ de `MODEL-009`/`MODEL-010`/`MODEL-013`:** "Días de descanso" es una cantidad continua sin escala acotada natural (un número de días, `0, 1, 2, ...`) y sin ningún umbral absoluto respaldado por evidencia en este proyecto (ej. "menos de 3 días es fatiga alta" sería un número inventado, prohibido por `CLAUDE.md`: "nunca inventes información"). Comparar cada equipo contra la población de selecciones del **mismo torneo** (mismo criterio que `MODEL-013` §4 usó para "Profundidad de Plantilla") resuelve esto sin inventar un punto de referencia absoluto.

**Por qué "Viajes" NO usa el mismo mecanismo z-score/Φ:** a diferencia de "Días de descanso", `docs/27` ya fija la forma de esta señal como "una aproximación geográfica, no una medición exacta" — la Base de Conocimiento actual (`estadios.csv`) solo tiene `ciudad`/`pais` como texto, sin coordenadas ni distancia (`altitud_metros` es elevación, no ubicación relativa; verificado antes de escribir). Esto produce, como máximo, una categoría **ordinal de 3 niveles** (mismo lugar / mismo país / distinto país), no una cantidad continua — aplicarle un z-score introduciría una falsa precisión estadística sobre una variable que en realidad es categórica. Se usa, en su lugar, un mapeo ordinal directo (sección 7), documentado explícitamente como placeholder sin calibrar (mismo estatus que los pesos `vᵢ` de `MODEL-009`/`010`/`013` — no elegido con evidencia, elegido por ausencia de alternativa mejor con el dato disponible).

**Por qué se combinan como promedio simple, no como una segunda capa de z-score/Φ:** una vez que ambas señales ya producen un valor en `[0,100]` de forma independiente, combinarlas como `Z = Σvᵢ·zᵢ` seguido de una segunda `Φ` no tiene fundamento estadístico (no son ambas variables `z` de la misma naturaleza). Se reutiliza, en su lugar, el patrón ya validado por `MODEL-012` (`Rendimiento_Torneo = (Puntos_pct+Gol_pct)/2`, promedio simple de dos sub-índices ya acotados 0-100, con degradación a un solo término si el otro es indefinido) — mismo principio aplicado aquí a dos señales heterogéneas de Fatiga.

**Por qué "Días de descanso" NO se restringe al mismo torneo del partido a predecir (a diferencia de la población de comparación):** el desgaste físico de un equipo depende de su calendario real de partidos, no de una convención administrativa de torneo — un amistoso disputado 2 días antes de un partido de torneo produce el mismo desgaste real que un partido de torneo disputado 2 días antes. Mismo principio ya aplicado por `MODEL-011`/`models/forma-reciente.md` §8 a Variable001 ("sin distinción de amistosos y competiciones"). Por eso, el "partido anterior" de cada equipo (sección 6) se busca sobre **todo** `partidos.csv`, sin filtrar por `id_torneo` — solo la **población de comparación** (qué otras selecciones se usan para `μ`/`σ`) se restringe al torneo del partido a predecir.

---

# 5. Fuente de datos

| Dato | Archivo | Columna | Rol |
|---|---|---|---|
| Partido anterior de cada equipo (fecha, sede) | `partidos.csv` | `fecha`, `id_estadio`, `id_seleccion_local`, `id_seleccion_visitante`, `estado_partido` | Identifica el partido oficial más reciente de cada selección antes de la fecha del partido a predecir, sin filtrar por torneo (sección 4) |
| Filtro de validez | `partidos.csv` | `estado_partido = finalizado` | Único valor ya confirmado por `data/processed/selecciones-nacionales/README.md` ("Filtra partidos válidos para el cálculo de variables"; "goles solo se completan si `estado_partido = finalizado`") — un partido programado y no jugado no es un "partido anterior" real |
| Población de comparación (selecciones del torneo) | `partidos.csv` | `id_torneo`, `id_seleccion_local`, `id_seleccion_visitante` | Selecciones con al menos una fila válida en el mismo `id_torneo` del partido a predecir (`context.match.torneo`) |
| Ubicación del partido anterior y del partido a predecir | `estadios.csv` | `ciudad`, `pais` (vía `id_estadio`) | Clasifica el desplazamiento geográfico en la sección 7 |
| Identificación del partido a predecir | `context.match` (`docs/30` §4.2) | `torneo`, `fecha`, `estadio` (opcional — "si asignado") | Ya disponible directamente en `PredictionContext`, sin necesidad de una consulta adicional a `partidos.csv` para estos tres campos |

**Por qué no se usa `jugadores.csv.club_actual`** (hallazgo explícito de esta misión, sección 11): el propio `README.md` de `data/processed/selecciones-nacionales/` justifica ese campo como "insumo de Fatiga (Variable007)" ("contexto de carga competitiva"), pero **no existe en ningún archivo de la Base de Conocimiento un calendario de partidos de clubes** — `club_actual` es únicamente una cadena de texto con el nombre del club, sin fechas de partido, minutos ni convocatorias de club. Sin esa fuente, no es posible derivar carga competitiva de club alguna; usarla igual violaría "nunca inventes información" (`CLAUDE.md`). Se documenta como hallazgo, no se resuelve aquí.

**Por qué no se usa `jugadores.csv.fecha_nacimiento`** (también citado por el mismo README como "proxy de Fatiga... edad, Variable 007/008"): la edad de los jugadores convocados es un proxy de fatiga *fisiológica individual a largo plazo* (recuperación más lenta en jugadores mayores), conceptualmente distinto de "Días de descanso"/"Viajes" (desgaste *del calendario de partidos* del equipo, no de la composición etaria de su plantilla) — ninguna de las dos señales en el alcance reducido de esta misión (`docs/36`/`GR-010`) lo requiere, y `docs/03` no lo lista como "Dato necesario" de Variable007. Queda fuera de esta especificación; podría evaluarse como señal adicional en una futura ampliación de alcance (sección 20), no en el alcance reducido ya autorizado.

**Por qué no se usa `selecciones.csv.confederacion`:** `docs/27` ya fijó la forma exacta de "Viajes" como "comparando ciudad/país del estadio entre partidos consecutivos" — un dato de sede de partido, no de confederación de origen del equipo. Introducir confederación como proxy de distancia intercontinental sería una fuente/forma distinta de la ya evidenciada por `docs/27`, fuera del alcance de lo que esta misión está autorizada a especificar (se documenta como candidata de V2, sección 20).

---

# 6. Fórmula oficial V1 — Escasez de Descanso

```
Sea F = context.match.fecha (fecha del partido a predecir)
Sea Tor = context.match.torneo
Sea T el equipo evaluado (local o visitante)

Partido_anterior(X) = la fila de partidos.csv con estado_partido = finalizado,
    fecha < F, (id_seleccion_local = X o id_seleccion_visitante = X),
    de fecha máxima (la más reciente) -- sobre TODO partidos.csv,
    sin filtrar por id_torneo (sección 4)

Días_descanso(X) = F − fecha(Partido_anterior(X))     -- en días, entero ≥ 0

Población(Tor) = { X : existe al menos una fila de partidos.csv con
    id_torneo = Tor y (id_seleccion_local = X o id_seleccion_visitante = X) }
    (incluye a T, mismo criterio de población que MODEL-013 §5 para Variable008)

μ = media de Días_descanso(X) sobre { X ∈ Población(Tor) : Partido_anterior(X) existe }
σ = desviación estándar muestral de Días_descanso(X), misma población

Si σ es indefinida (menos de 2 selecciones con Partido_anterior resoluble en Tor) o es 0,
    Fatiga_Descanso no se calcula (sección 10)

z = (Días_descanso(T) − μ) / σ

Fatiga_Descanso(T) = 100 · (1 − Φ(z))     (Φ = CDF normal estándar)
```

**Por qué `1 − Φ(z)` y no `Φ(z)` directamente:** `Días_descanso` alto significa *más* descanso, es decir *menos* fatiga — dirección opuesta a las métricas de `MODEL-009`/`MODEL-010`/`MODEL-013` (donde un `z` alto siempre significaba "mejor" en la variable positiva correspondiente). Se invierte con `1 − Φ(z)` en lugar de redefinir el signo de la métrica (`-Días_descanso`), preservando `Días_descanso` con su signo intuitivo (positivo = más días de descanso) — misma decisión de mantener la métrica en su signo natural e invertir solo la transformación final que `MODEL-010` §14 aplicó al construir `P_def = 100·(1−Φ(Z_def/s_def))` para Variable004.

**Por qué `s = 1` (sin el ajuste `√(Σvᵢ²)` de `MODEL-009`/`010`/`013`):** esta señal usa una única métrica (`Días_descanso`), no una suma ponderada de varias — no hay combinación de `z` que requiera derivar una escala de agregación. `z` ya es, por construcción, aproximadamente `N(0,1)` bajo el supuesto estándar de normalidad de la población, por lo que `Φ(z)` se aplica directamente.

---

# 7. Fórmula oficial V1 — Desplazamiento Geográfico (Viajes)

```
Estadio_anterior(T) = id_estadio de Partido_anterior(T)     (sección 6)
Estadio_destino(T)  = context.match.estadio                  (si asignado)

Categoría_Viaje(T) =
    0   si Estadio_anterior(T) = Estadio_destino(T), o
        estadios.csv.ciudad es igual para ambos estadios
    1   si distinta ciudad, pero estadios.csv.pais es igual para ambos estadios
    2   si estadios.csv.pais es distinto entre ambos estadios

Fatiga_Viaje(T) = 50 · Categoría_Viaje(T)     (0 → 0, 1 → 50, 2 → 100)
```

**Por qué `{0, 50, 100}` y no otro mapeo:** con solo tres categorías ordinales y sin datos de distancia real (sección 4), el espaciado uniforme es la única asignación que no requiere inventar una distancia relativa entre categorías (ej. asumir que un viaje internacional "pesa" el doble de uno doméstico sería un supuesto adicional sin evidencia). Se documenta explícitamente como **placeholder sin calibrar** (sección 16), mismo estatus que los pesos `vᵢ` de `MODEL-009`/`010`/`013`.

**Condición de no disponibilidad:** si `Estadio_anterior(T)` o `Estadio_destino(T)` no existen (partido anterior sin `id_estadio` resoluble, o `context.match.estadio` ausente — `docs/30` §4.2 confirma que el campo es opcional, "si asignado"), `Fatiga_Viaje(T)` no se calcula (sección 10).

---

# 8. Fórmula oficial V1 — Combinación

```
Fatiga(T) =
    (Fatiga_Descanso(T) + Fatiga_Viaje(T)) / 2     si ambas señales disponibles
    Fatiga_Descanso(T)                              si solo Escasez de Descanso disponible
    Fatiga_Viaje(T)                                  si solo Viajes disponible
    Variable007 se marca disponible = False          si ninguna señal disponible
```

Mismo patrón de degradación ya validado por `MODEL-012` (`Rendimiento_Torneo`, promedio de `Puntos_pct`/`Gol_pct` con degradación a un solo término) — nunca se renormaliza inventando un peso distinto para el término restante, ni se sustituye el término ausente por un valor arbitrario.

---

# 9. Variables internas / Métricas necesarias

- `Partido_anterior(X)`: partido oficial más reciente de la selección `X` antes de `F`, sobre todo `partidos.csv` (sección 4).
- `Días_descanso(X)`: diferencia en días entre `F` y la fecha de `Partido_anterior(X)`.
- `Población(Tor)`, `μ`, `σ`: población de comparación y sus estadísticos, restringidos al torneo del partido a predecir (sección 6).
- `z`: z-score de `Días_descanso(T)`.
- `Categoría_Viaje(T)`: nivel ordinal (0/1/2) de desplazamiento geográfico (sección 7).
- `Fatiga_Descanso(T)`, `Fatiga_Viaje(T)`, `Fatiga(T)`: sub-índices y valor final, todos en `[0,100]`.

Ninguna métrica adicional (no minutos jugados, no edad, no club, no confederación — sección 5).

---

# 10. Ventana temporal

**No aplica una ventana de `N` partidos (a diferencia de Variable001 `N=5` / Variable003-004 `N=10`).** Ambas señales de Fatiga son, por naturaleza, comparaciones puntuales contra el **partido inmediatamente anterior** de cada equipo (`N=1` conceptual), no un promedio móvil: el descanso físico se determina por el último partido jugado, no por un promedio de los últimos 5 o 10 partidos — promediar fechas de varios partidos pasados no representaría el estado de descanso actual del equipo de cara al partido a predecir. Esta es una divergencia deliberada, justificada por la naturaleza fisiológica de la señal, mismo tipo de divergencia ya documentada por `MODEL-011` §4 (Variable001 diverge del mecanismo de Variable003/004 por la naturaleza distinta del dato) y por `MODEL-013` §8 (Variable008 tampoco usa ventana de `N`, por ser una fotografía única).

La **población de comparación** (`μ`/`σ` de Días_descanso, sección 6) sí tiene un límite temporal implícito: se restringe a las selecciones del mismo torneo del partido a predecir, análogo a la restricción "mismo torneo" ya usada por `MODEL-013` para Variable008 — no una ventana de partidos, sino un límite de contemporaneidad (todas las selecciones comparadas están sujetas al mismo calendario competitivo).

---

# 11. Minutos jugados — por qué queda fuera de esta especificación (hallazgo explícito, respuesta directa a la restricción del brief)

**Hallazgo, verificado antes de escribir esta sección:** ninguna fuente de la Base de Conocimiento actual (`data/processed/selecciones-nacionales/`) registra minutos jugados por jugador y partido. `data/processed/selecciones-nacionales/README.md` lo confirma explícitamente en su punto 4 de "Decisiones arquitectónicas aplicadas": **"Sin estadísticas individuales de jugador en esta misión (goles, asistencias, minutos jugados por jugador y partido). Queda explícitamente diferido a una misión futura."** `docs/27-Auditoria-de-Variables-Pendientes.md` clasifica "Minutos jugados" como categoría **D** ("debe capturarse") y `docs/36`/`GR-010` confirma: "ningún `MODEL-` existe todavía, ni para el alcance reducido" — siendo, además, la única de las tres señales de Variable007 sin ninguna vía de derivación desde el esquema actual (a diferencia de "Días de descanso"/"Viajes", ambas categoría C).

**Conclusión explícita exigida por el brief:** **Variable007 completa, con sus tres señales ("Días de descanso", "Minutos jugados", "Viajes"), no puede especificarse ni calcularse con el esquema de datos actual.** Esta misión no inventa una fuente ni una fórmula para "Minutos jugados" — se detiene explícitamente en ese punto, cumpliendo la restricción del brief ("No asumir disponibilidad de minutos jugados si no existen"). Lo que sí queda completamente especificado, y es la única fracción de Variable007 con evidencia suficiente hoy, es el **alcance reducido de dos señales** (secciones 6-8) — mismo patrón de alcance parcial ya aplicado por `MR-004`/`MODEL-013` a Variable008 ("Profundidad" sí, "Valor de mercado" no).

**Vía de resolución futura, no aplicada aquí:** capturar minutos jugados requeriría una nueva tabla de estadística individual por jugador y partido (`docs/27`: "estadística individual de jugador por partido") — la misma tabla que `docs/36` sugiere podría, en una futura misión de captura de datos, resolver también "Rotaciones" de Variable006 simultáneamente (ambas son estadísticas a nivel jugador-partido). Una vez exista esa fuente, "Minutos jugados" podría incorporarse como una tercera señal de Fatiga en una versión 2.0 de esta especificación (sección 20) — sin necesidad de rediseñar las dos señales ya definidas aquí, que seguirían siendo válidas.

---

# 12. Normalización

Rango de salida: **0 a 100**. `Fatiga_Descanso` está acotado por construcción de `Φ` (idéntico mecanismo que `MODEL-009`/`010`/`013`); `Fatiga_Viaje` está acotado por construcción del mapeo ordinal (sección 7, `{0,50,100} ⊂ [0,100]`); su promedio simple (sección 8) permanece en `[0,100]` sin necesidad de `clip` adicional — consistente con `docs/16-Contrato-Oficial-de-Variables.md` (Variable007: "Índice (0-100)").

---

# 13. Casos límite

| Caso | Comportamiento |
|---|---|
| Equipo sin ningún partido oficial anterior (`Partido_anterior(T)` no existe — debut absoluto) | `Fatiga_Descanso` y `Fatiga_Viaje` no calculables → Variable007 se marca `disponible = False` — nunca un valor inventado (Variable007 ya es opcional, `docs/17`, "no detiene el pipeline") |
| Torneo con menos de 2 selecciones con `Partido_anterior` resoluble (`σ` indefinida) | `Fatiga_Descanso` no se calcula; se usa solo `Fatiga_Viaje` si está disponible (sección 8); si ninguna, `disponible = False` |
| `σ = 0` (todas las selecciones de la población con exactamente el mismo `Días_descanso`) | Mismo tratamiento que `σ` indefinida — se excluye `Fatiga_Descanso`, sin dividir por cero |
| `context.match.estadio` no asignado (`docs/30` §4.2, campo opcional) | `Fatiga_Viaje` no calculable; se usa solo `Fatiga_Descanso` si está disponible; si ninguna, `disponible = False` |
| `Partido_anterior(T)` sin `id_estadio` resoluble en `estadios.csv` (FK rota o estadio no asignado en ese partido histórico) | Mismo tratamiento que la fila anterior — `Fatiga_Viaje` no calculable para ese equipo |
| Fila de `partidos.csv` con `fecha` no parseable o `estado_partido` distinto de `finalizado` | Se descarta como candidata a `Partido_anterior` — no invalida la búsqueda del resto de partidos de esa selección |
| Torneo contenedor de amistosos (`TOR-<año>-AMISTOSOS`) como `Tor` | La población incluye cualquier selección con un amistoso ese año calendario, sin distinción de fecha exacta dentro del año — limitación documentada explícitamente (sección 16), no un caso de error |
| `Días_descanso(T)` extremadamente alto (equipo inactivo por mucho tiempo, no por buen descanso) | Se calcula igual — sin umbral inventado que lo distinga de "buen descanso" (limitación documentada, sección 16) |
| Resultado fuera de `[0,100]` (no debería ocurrir por construcción) | Se descarta como fallo de cálculo, `disponible = False`, registrado como error — mismo criterio que `MODEL-009`/`010`/`013` |

---

# 14. Complejidad computacional

**Precalculable, `O(P_Tor)`** — para la población de comparación, una pasada sobre las filas de `partidos.csv` restringidas al `id_torneo` del partido a predecir para identificar `Población(Tor)` (`O(P_Tor)`, `P_Tor` = partidos del torneo), más, para cada selección de esa población, una búsqueda del partido más reciente anterior a `F` sobre su propio historial completo (indexable por selección + fecha descendente, `O(log H)` con un índice adecuado, `H` = historial total de esa selección). Para `Fatiga_Viaje`, solo dos búsquedas puntuales en `estadios.csv` (`O(1)` cada una, tabla pequeña). Es una complejidad comparable a la de `MODEL-013` (menor que Variable003/004, que además requieren agregación de múltiples métricas por partido dentro de una ventana de `N`).

---

# 15. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable007 podría pasar de "Método: Pendiente" a "definido (alcance reducido), ver `models/fatiga.md`" — actualización editorial futura, fuera de alcance de esta misión de `models/` |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Sin cambios — ya asigna Variable007 a `engine/01`, `02`, `04`; esta especificación no amplía ni reduce ese consumo |
| `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) | Sin cambios — confirma que "Días de descanso"/"Viajes" son categoría C y "Minutos jugados" categoría D, consistente con esta especificación |
| `docs/28-Catalogo-de-Variables-Derivadas.md` | Fatiga (Var007) podría pasar de "Pendiente" a "Definida (alcance reducido)" — actualización editorial futura, no aplicada aquí |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Sin cambios — confirma que `context.match.torneo`/`fecha` están siempre disponibles y `context.match.estadio` es opcional (sección 13), compatible sin ajustes con esta especificación |
| `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) | Resuelve la investigación matemática que esa misión recomendó explícitamente como siguiente prioridad tras `MODEL-013` |
| `models/offensive-strength.md` (`MODEL-009`), `models/defensive-strength.md` (`MODEL-010`), `models/profundidad-plantilla.md` (`MODEL-013`) | Sin cambios — se reutiliza su mecanismo z-score/Φ (para Escasez de Descanso) y su convención de población "mismo torneo" (`MODEL-013`) |
| `models/rendimiento-torneo.md` (`MODEL-012`) | Sin cambios — se reutiliza su patrón de combinación (promedio simple de dos sub-índices con degradación a un solo término) |
| `models/chaos-index.md` | Sin cambios — confirma la dirección "`Δ_fatiga`: fatiga suma caos" ya usada aquí (sección 2) para fijar la convención de signo de `Fatiga` |
| `models/parameter-calibration.md` | No modificado en esta misión — quedaría pendiente de una futura ampliación que catalogue los nuevos símbolos sin calibrar de esta especificación (el mapeo ordinal `{0,50,100}` de la sección 7, y el peso implícito `1/2` de la combinación de la sección 8), distintos de `w_F` (que ya cataloga el peso de Fatiga *dentro* de `Pen`, en `Engine01`/`Engine02` — un símbolo de otro nivel, no de esta fórmula interna) |
| `app/preparation/preparation.py` | Consumidor directo en una futura `BUILD-023`, mismo patrón ya validado por `BUILD-018` a `BUILD-022` |

---

# 16. Limitaciones

- **Mapeo ordinal `{0,50,100}` de "Viajes" sin calibrar** (sección 7) — ningún dato de distancia real (coordenadas de estadio) respalda el espaciado uniforme; es la asignación de menor supuesto posible con el dato disponible, no una calibración estadística.
- **Peso implícito `1/2` entre las dos señales** (sección 8) — ponderación igualitaria por ausencia de evidencia que favorezca una señal sobre la otra, mismo criterio ya usado en todo el proyecto (`MODEL-009` §21) pero sin calibrar.
- **Población de "amistosos" potencialmente heterogénea:** el torneo contenedor anual (`TOR-<año>-AMISTOSOS`, `data/processed/selecciones-nacionales/README.md`) agrupa cualquier amistoso del año calendario — la población de comparación de `Días_descanso` podría mezclar selecciones con calendarios reales muy distintos dentro del mismo año, diluyendo el significado de `μ`/`σ` para ese caso específico. No se resuelve aquí; recalcular la población con una granularidad más fina (ej. ventana FIFA de fecha internacional) fue ya descartado, por ahora, como complejidad no justificada (`data/processed/selecciones-nacionales/README.md`, "Nota de granularidad").
- **`Días_descanso` no distingue inactividad de buen descanso:** un equipo que no juega hace mucho tiempo (ej. tras eliminación temprana en una edición previa) obtiene el mismo tratamiento que un equipo genuinamente bien descansado — ninguna evidencia respalda un umbral que los distinga, así que no se introduce uno (sección 13).
- **No usa `jornada`** (`partidos.csv.jornada`) como criterio de contemporaneidad de la población, pese a que sería, en principio, un límite más preciso que "todo el torneo": `jornada` no es un campo siempre disponible (`data/processed/selecciones-nacionales/README.md`: "`jornada` obligatorio solo si `fase = fase_grupos`") — usarlo como filtro excluiría o degradaría el cálculo en fases eliminatorias y en amistosos, sin ninguna ganancia consistente. Se documenta como candidata de refinamiento futuro (sección 20), no como limitación bloqueante hoy.
- **No incorpora "Minutos jugados"** (sección 11) — la limitación central de esta misión, ya extensamente documentada y no bloqueante para el alcance reducido.
- **Sin datos reales hoy:** `partidos.csv`/`estadios.csv` tienen actualmente 0 filas (verificado antes de escribir, misma condición que el resto de la Base de Conocimiento de Selecciones Nacionales salvo `selecciones.csv`/`competiciones.csv`/`torneos.csv`) — esta especificación resuelve el bloqueo metodológico, no el de datos.

---

# 17. Ventajas

- Resuelve, con evidencia documental exacta (`docs/27`, `docs/36`), las dos únicas señales de Variable007 con dato disponible hoy, sin necesidad de ninguna captura nueva.
- Reutiliza tres mecanismos ya validados en este proyecto (z-score/Φ de `MODEL-009`/`010`/`013`; población "mismo torneo" de `MODEL-013`; combinación por promedio simple con degradación de `MODEL-012`) en lugar de inventar un cuarto mecanismo — consistencia metodológica entre las especificaciones de `models/`.
- Distingue explícitamente, con justificación matemática (sección 4), por qué una señal continua (descanso) y una señal categórica (viaje) requieren tratamientos distintos, en lugar de forzar ambas al mismo mecanismo.
- No requiere ninguna fuente de datos nueva ni ninguna tabla adicional — ambas señales se derivan enteramente de `partidos.csv`/`estadios.csv`, ya existentes en el esquema aprobado.
- Deja "Minutos jugados" explícitamente fuera, con un hallazgo documentado y verificable, en lugar de aproximarlo con un dato no autorizado (ej. edad o club) que violaría "nunca inventes información".

---

# 18. Aplicación dentro del Modelo Santiago

Es la especificación matemática oficial que `VariablePreparation` deberá implementar para Variable007 en su alcance reducido V1 (Escasez de Descanso + Viajes), alimentando `engine/01`, `engine/02` y `engine/04` como variable contextual/opcional (`docs/17`). No alimenta "Minutos jugados" (sección 11), que permanece sin especificación matemática hasta que exista la fuente de datos correspondiente.

---

# 19. Referencias

- `docs/03-Variables.md` — define las tres señales originales de Variable007 y su objetivo ("evaluar el desgaste físico acumulado").
- `docs/16-Contrato-Oficial-de-Variables.md` — fija el tipo/rango de Variable007 (Decimal, Índice 0-100, sin negativos).
- `docs/17-Matriz-de-Consumo-de-Variables.md` — confirma los tres motores consumidores (`engine/01`, `02`, `04`).
- `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) — clasificación de categoría de disponibilidad de cada señal.
- `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) — autoriza el alcance reducido y recomienda esta investigación como siguiente prioridad.
- `data/processed/selecciones-nacionales/README.md` — confirma la ausencia de estadística individual de jugador (Minutos jugados) y el estado real de los archivos consultados.
- `models/offensive-strength.md` (`MODEL-009`), `models/defensive-strength.md` (`MODEL-010`) — origen del mecanismo z-score/Φ reutilizado para Escasez de Descanso.
- `models/profundidad-plantilla.md` (`MODEL-013`) — origen de la convención de población "mismo torneo específico" reutilizada aquí.
- `models/rendimiento-torneo.md` (`MODEL-012`) — origen del patrón de combinación por promedio simple con degradación.
- `models/chaos-index.md` — confirma la convención de dirección de `Fatiga` ("suma caos").

---

# 20. Versión 2.0 (siguiente iteración de esta investigación)

Pendiente, condicionado a datos reales suficientes y, en algunos casos, a nueva captura de datos:

- Incorporación de "Minutos jugados" como tercera señal, una vez exista una tabla de estadística individual por jugador y partido (sección 11) — posiblemente la misma tabla que resolvería "Rotaciones" de Variable006 (`docs/36`).
- Reemplazo del mapeo ordinal `{0,50,100}` de "Viajes" por una distancia real (great-circle) si `estadios.csv` incorpora coordenadas de latitud/longitud en una futura misión de captura.
- Evaluación empírica de si el peso `1/2` entre Escasez de Descanso y Viajes debería ajustarse, una vez exista evidencia en `data/results/` (`models/parameter-calibration.md` §7).
- Evaluación de si granular la población de comparación por `jornada` (cuando esté disponible) mejora la precisión frente a "mismo torneo completo" — hoy descartado por la disponibilidad inconsistente de ese campo (sección 16), no por imposibilidad conceptual.
- Evaluación de si `selecciones.csv.confederacion` aporta valor como proxy adicional de distancia intercontinental cuando `estadios.csv` no permite derivarla con precisión — hoy fuera de alcance por no estar autorizado por la fuente/forma ya fijada de "Viajes" (`docs/27`).

---

# Validaciones

- **¿La fórmula usa solo datos autorizados por `docs/03` para Variable007?** Sí — únicamente "Días de descanso" y "Viajes", las dos señales de categoría C confirmadas por `docs/27`/`docs/36`. "Minutos jugados" queda explícitamente fuera (sección 11).
- **¿Se fija algún peso sin justificar?** El mapeo ordinal `{0,50,100}` y el peso implícito `1/2` de la combinación son placeholders documentados explícitamente como no calibrados (secciones 7, 8, 16) — mismo estatus que los pesos de `MODEL-009`/`010`/`013`, nunca ocultos.
- **¿Se inventó alguna fuente de datos?** No — se verificó explícitamente que `jugadores.csv.club_actual`/`fecha_nacimiento` y `selecciones.csv.confederacion` no son suficientes o no están autorizados para estas dos señales (sección 5), y no se usan pese a estar disponibles en el esquema.
- **¿Se introdujo alguna API externa?** No.
- **¿Es reproducible?** Sí — función determinista del calendario de partidos y la ubicación de estadios observados, sin aleatoriedad ni estimación subjetiva.
- **¿Se detuvo la misión por falta de rigor matemático?** Parcialmente — se detiene explícitamente para "Minutos jugados" (sección 11, exigido por el brief), pero no para el alcance reducido de dos señales, que queda completamente especificado.

---

# Cierre obligatorio

**1. ¿Qué definición operacional quedó aprobada?**
Fatiga = promedio simple (con degradación a un solo término si falta uno) de dos sub-índices 0-100: Escasez de Descanso (z-score de los días transcurridos desde el partido anterior del equipo, invertido y comparado contra la población de selecciones del mismo torneo) y Desplazamiento Geográfico (categoría ordinal de viaje entre la sede del partido anterior y la del partido a predecir) — sección 2. Alto = mayor fatiga (peor estado), consistente con `models/chaos-index.md`.

**2. ¿Qué fuente consume?**
`partidos.csv` (fecha, sede, estado, torneo, selecciones de cada partido) y `estadios.csv` (ciudad, país) — sección 5. No usa `jugadores.csv.club_actual`/`fecha_nacimiento` ni `selecciones.csv.confederacion` (justificado explícitamente por qué no).

**3. ¿Qué métricas utiliza?**
`Días_descanso(X)` con su población `μ`/`σ` restringida al torneo, `z`, `Categoría_Viaje(T)` (0/1/2) — sección 9. Ninguna métrica de minutos jugados, edad ni club.

**4. ¿Qué fórmula matemática quedó definida?**
`Fatiga_Descanso = 100·(1−Φ(z))` (secciones 6), `Fatiga_Viaje = 50·Categoría_Viaje` (sección 7), `Fatiga = (Fatiga_Descanso + Fatiga_Viaje)/2` con degradación a un solo término (sección 8).

**5. ¿Qué rango produce?**
0 a 100, acotado por construcción de `Φ` y del mapeo ordinal — sección 12.

**6. ¿Qué casos límite contempla?**
Debut absoluto (sin partido anterior) → `disponible=False`; población sin varianza (`σ` indefinida o 0) → se excluye Escasez de Descanso; `context.match.estadio` no asignado o sede del partido anterior no resoluble → se excluye Viajes; ambas ausentes → `disponible=False`; torneo contenedor de amistosos → limitación documentada, no error; días de descanso extremadamente altos → se calcula igual, sin umbral inventado — sección 13.

**7. ¿Qué documentos quedaron afectados?**
Solo `models/fatiga.md` (creado). `docs/03`, `docs/17`, `docs/28` quedan documentados como afectados a futuro por una misión editorial, ninguno modificado en esta misión de `models/` — sección 15.

**8. ¿Qué desbloqueará BUILD-023?**
El camino metodológico completo para implementar Variable007 en su alcance reducido (Escasez de Descanso + Viajes) en `VariablePreparation`, mismo patrón que `BUILD-018` a `BUILD-022`. No desbloquea, por sí solo, una predicción real — `partidos.csv`/`estadios.csv` siguen con 0 filas reales hoy (verificado antes de escribir).

**9. ¿Queda implementable en V1?**
Sí, para el alcance reducido (Escasez de Descanso + Viajes) — la fórmula queda completamente definida, sin ningún elemento pendiente de investigación adicional para ese alcance. Variable007 **completa** (con "Minutos jugados") **no es implementable en V1**: no existe fuente de datos, y esta misión lo declara explícitamente en lugar de asumirlo o inventar una fuente (sección 11).

**10. ¿Se actualizaron `CHANGELOG.md` y `docs/00-Project-Tracker.md`?**
Sí, ambos — ver entradas de esta misma misión (`MODEL-014`).

---

# Fuera de alcance de esta misión

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext`, `Engine01`, `Engine02`, `Engine04` ni `VariablePreparation`.
- No se modifica `docs/03`, `docs/16`, `docs/17`, `docs/28`, `docs/30` ni ningún otro documento existente de `docs/`.
- No se especifica "Minutos jugados" — declarado explícitamente no implementable con el esquema de datos actual (sección 11), no un simple diferimiento de alcance como el de Variable008.
- No se formaliza un calendario de partidos de club ni una tabla de estadística individual de jugador — se documenta como hallazgo pendiente (sección 11), no se resuelve aquí.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5).

---

Fin del documento.
