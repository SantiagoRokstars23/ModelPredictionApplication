# Profundidad de Plantilla — Componente único de Variable008 (V1)

**Archivo:** `models/profundidad-plantilla.md`

**Misión:** MODEL-013 — Especificación Matemática Oficial de Variable008 (Profundidad de Plantilla)

**Versión:** 1.0.0-investigación

**Estado:** Investigación — primer documento de `models/` dedicado a Variable008 (no evoluciona un stub, se crea desde cero, mismo patrón que `MODEL-005`/`MODEL-011`/`MODEL-012`)

---

## Nota de origen y alcance exacto de esta misión

Variable008 (Calidad de Plantilla) tiene, según `docs/03-Variables.md`, tres señales: "Valor de mercado", "Profundidad", "Experiencia". Esta misión **no** especifica Variable008 completa — especifica únicamente **"Profundidad de Plantilla"**, el único componente que `MR-004` (`docs/24-Analisis-Arquitectonico-INC-04-INC-05.md`, línea 75: *"asignar con alcance reducido (solo 'profundidad de plantilla', derivable de `convocatorias.csv`+`jugadores.csv`)..."*) ya autorizó formalmente para V1, excluyendo explícitamente "valor de mercado" (sin fuente en ningún CSV) y, por ese mismo texto, "experiencia" (no nombrada en el alcance reducido). **Esto resuelve, con evidencia directa del propio documento originario, la ambigüedad detectada por `GR-010`/`docs/36`** (que `docs/03` no aclaraba si "Experiencia" entraba al alcance de `MR-004`): `docs/24` sí lo aclara — el alcance reducido es "solo profundidad de plantilla", nada más. Esta misión no reabre esa decisión de alcance; la documenta con su fuente exacta y construye sobre ella.

La forma operacional de "Profundidad de plantilla" — "conteo de convocados por posición", vía `convocatorias.csv` + `jugadores.csv.posicion_principal` — ya está fijada por `docs/17-Matriz-de-Consumo-de-Variables.md` (fila "Profundidad de plantilla", que cita `docs/24`/`MR-004` como origen), un documento de "arquitectura funcional" de mayor autoridad que `models/` en la Jerarquía Documental (`CLAUDE.md`). Esta misión no redefine esa forma ni esa fuente — su único trabajo es fijar la **fórmula matemática exacta** que `docs/17` ya señala como pendiente ("Conteo, sin fórmula exacta fijada").

---

# 1. Objetivo

Definir la fórmula matemática completa que transforma el conteo de jugadores convocados por posición en el índice `Profundidad_Plantilla` (0-100) que `VariablePreparation` podrá implementar para Variable008, eliminando el estado "método pendiente" (`docs/03`) para este componente — sin implementar código, sin modificar el Runtime, `PredictionContext`, `Engine01`, `Engine02` ni `VariablePreparation`.

---

# 2. Definición operacional exacta

**Profundidad de Plantilla** mide la disponibilidad relativa de jugadores convocados por posición para un torneo específico, comparada contra la misma métrica de todas las demás selecciones convocadas al **mismo torneo** (`id_torneo`). Un equipo con más jugadores convocados que el promedio de sus rivales en ese torneo, en una posición dada, tiene mayor profundidad relativa en esa posición; el índice agregado combina todas las posiciones observadas en la convocatoria del equipo.

No mide historia, rendimiento reciente ni valor de mercado — responde exclusivamente "¿cuántas opciones tiene el cuerpo técnico por posición, comparado con el resto de convocatorias del mismo torneo?".

---

# 3. Problema que resuelve

`docs/17` ya fijó que Variable008 (alcance reducido) debe construirse contando convocados por posición (`convocatorias.csv` + `jugadores.csv.posicion_principal`), pero nunca definió la fórmula exacta — quedó marcada explícitamente "Conteo, sin fórmula exacta fijada". Sin esa fórmula, `VariablePreparation` no puede publicar Variable008 con dato real aunque el alcance y la fuente ya estén decididos (a diferencia de Variable001-004/002, que ya tenían su propia `MODEL-` antes de implementarse).

---

# 4. Fundamento y por qué se reutiliza el mecanismo de z-score/Φ de `MODEL-009`/`MODEL-010`, no un umbral inventado

**Problema de fondo, verificado antes de escribir esta fórmula:** ni `docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md`, ni `docs/32-Modelo-Relacional-Oficial.md`, ni `docs/33-Modelo-Fisico-PostgreSQL.md`, ni `data/processed/selecciones-nacionales/README.md` formalizan jamás la lista real de valores permitidos de `posicion_principal`/`posicion_convocatoria`. `docs/33` (línea 116/134) los tipa como `TEXT (CHECK ENUM)` en el modelo físico de PostgreSQL, pero **ningún documento del proyecto enumera esos valores** — a diferencia de, por ejemplo, `estado_convocatoria`, cuyo vacío de formalización ya fue detectado explícitamente por `docs/27`/`GR-010`. No existe hoy un "Portero/Defensa/Mediocampista/Delantero" (ni ninguna otra taxonomía) declarado en ningún documento del Modelo Santiago.

**Por qué esto no bloquea una definición matemática rigurosa (y por qué esta misión no se detiene aquí):** una fórmula que dependiera de conocer *a priori* los nombres exactos de las posiciones (ej. una lista fija `{"Portero", "Defensa", ...}`) sí quedaría bloqueada por ese vacío. Pero no es necesario conocer esos nombres para agrupar y contar: **la fórmula de esta misión agrupa dinámicamente por cualquier valor distinto que aparezca en `posicion_principal`** dentro de la convocatoria de cada torneo, sin asumir cuántas categorías existen ni cómo se llaman — el mismo principio que ya usa `GROUP BY` sobre una columna categórica sin necesitar su dominio declarado de antemano. Esto convierte el vacío de formalización en una **limitación documentada** (sección 16), no en un bloqueo matemático: **no se detiene la misión**, porque sí es posible una definición rigurosa sin inventar ningún valor de posición ni ningún umbral absoluto de "cuántos jugadores por posición son suficientes" (que sí habría requerido inventar un número sin respaldo, violando `CLAUDE.md`: "nunca inventes información").

**Por qué se reutiliza z-score/Φ (`P = 100·Φ(Z/s)`, `MODEL-009` §21, `MODEL-010` §15) y no un umbral fijo:** exactamente la misma razón que motivó ese mecanismo para Variable003/004 — convertir una cantidad sin escala acotada natural (un conteo de jugadores, `0, 1, 2, ...`) en un índice `[0,100]` sin inventar un punto de referencia absoluto ("un equipo con profundidad completa tiene X jugadores por posición"), que ningún documento del proyecto respalda. Comparar cada equipo contra la población de equipos del **mismo torneo** (no una cifra inventada) resuelve el problema con el mismo fundamento estadístico ya validado dos veces por el Arquitecto Estadístico Humano.

**Por qué la población es "el mismo torneo" (`id_torneo`) y no "la misma competición"** (a diferencia de Variable003/004, que comparan contra la competición en la misma ventana de fechas): una convocatoria es una fotografía única por torneo, no una serie de partidos con fecha propia — no existe una "ventana temporal de N partidos" que recortar (sección 8). El límite natural, no arbitrario, es el propio torneo: todas las selecciones convocadas al mismo `id_torneo` están sujetas al mismo reglamento de tamaño de plantilla (ej. un límite de convocados igual para todas las selecciones de un mismo Mundial) — comparar contra selecciones de un torneo distinto, con un reglamento de convocatoria potencialmente distinto, no sería una comparación válida.

---

# 5. Fuente de datos

| Dato | Archivo | Columna | Rol |
|---|---|---|---|
| Convocatoria del equipo al torneo específico | `convocatorias.csv` | `id_torneo`, `id_seleccion`, `id_jugador` | Identifica qué jugadores fueron convocados por el equipo evaluado a `context.match.torneo` |
| Posición de cada jugador | `jugadores.csv` | `posicion_principal` (vía `id_jugador`, ya fijado por `docs/17`, no `posicion_convocatoria`) | Clasifica cada convocado en un grupo de posición, cualquiera sea su valor textual |
| Población de comparación | `convocatorias.csv` | Todas las filas del mismo `id_torneo`, cualquier `id_seleccion` | Universo de selecciones convocadas al mismo torneo, para `μ_p`/`σ_p` |

**Por qué `posicion_principal` (`jugadores.csv`) y no `posicion_convocatoria` (`convocatorias.csv`):** decisión ya fijada por `docs/17`, no de esta misión — se documenta la razón por consistencia: `posicion_principal` es un atributo estable del jugador (su posición habitual de carrera), mientras que `posicion_convocatoria` podría variar de un torneo a otro según necesidades tácticas puntuales del cuerpo técnico (ej. un lateral convocado como comodín). Usar la posición estable evita que la misma persona clasifique en un grupo distinto en cada convocatoria, lo que introduciría ruido no relacionado con la profundidad real de la plantilla.

**No se usa** `estadisticas_partido.csv`, `lesiones.csv` ni ninguna fuente externa (ranking de scouting, valor de mercado): ninguno está autorizado por `docs/03`/`docs/16` para esta señal específica, y usar una fuente externa violaría explícitamente la restricción de esta misión.

**Tratamiento de `estado_convocatoria`:** se cuenta toda fila de `convocatorias.csv` para el `id_torneo`/`id_seleccion` evaluados, **sin filtrar por `estado_convocatoria`** — sus valores ENUM permitidos no están formalizados (`docs/27`, categoría B, aún sin resolver), por lo que filtrar por un valor de texto no verificado (ej. "dado de baja") arriesgaría excluir convocados válidos por un criterio inventado. Limitación documentada explícitamente en la sección 16; una futura formalización de ese ENUM (recomendada por `GR-010`/`docs/36` para Variable006) permitiría, en una v2.0 de esta especificación, excluir bajas confirmadas.

---

# 6. Fórmula oficial V1

```
Para el torneo específico Tor = id_torneo del partido a predecir, y el equipo evaluado T:

Sea P(T) el conjunto de posiciones distintas observadas en la convocatoria de T
    (valores de jugadores.csv.posicion_principal, vía join con convocatorias.csv,
    para filas con id_torneo = Tor, id_seleccion = T, descartando convocatorias
    sin jugador resoluble o sin posición parseable -- sección 11).

Para cada posición p ∈ P(T):

    conteo(T, p) = número de jugadores convocados por T a Tor en la posición p

    Población: conteo(T', p) para cada selección T' con al menos una fila válida
    en convocatorias.csv para el mismo Tor (incluye a T, mismo criterio ya usado
    por MODEL-009/010 para la población de Variable003/004)

    μ_p = media de conteo(T', p) sobre la población
    σ_p = desviación estándar muestral de conteo(T', p) sobre la población

    Si σ_p es indefinida (menos de 2 selecciones con datos válidos en Tor) o es 0,
    la posición p se excluye del cálculo de Z, sin renormalizar los pesos restantes
    (mismo tratamiento que Variable003/004, MODEL-009 §24/MODEL-010 §18)

    z_p = (conteo(T, p) − μ_p) / σ_p     -- para cada p no excluida

k = número de posiciones no excluidas (dinámico -- no una lista fija, sección 4)

Z = Σ (1/k) · z_p                         (peso igualitario entre posiciones, símbolo propio)
s = √(k · (1/k)²) = √(1/k)                (derivado matemáticamente de los pesos, no elegido a mano)

Profundidad_Plantilla = 100 · Φ(Z / s)
```

Si `k = 0` (todas las posiciones quedaron excluidas, o `P(T)` está vacío), `Profundidad_Plantilla` no se calcula — Variable008 (componente Profundidad) se marca `disponible=False` (sección 11).

**Ningún umbral absoluto de "cuántos jugadores por posición bastan"** — la fórmula es enteramente relativa a la población del propio torneo, mismo principio que Variable003/004 (sección 4).

---

# 7. Variables internas / Métricas necesarias

- `P(T)`: conjunto dinámico de posiciones observadas en la convocatoria del equipo evaluado — no una lista predeclarada (sección 4).
- `conteo(T, p)`: entero, número de convocados de `T` en la posición `p`.
- `μ_p`, `σ_p`: media y desviación estándar muestral de `conteo(T', p)` sobre la población del torneo.
- `z_p`: z-score por posición.
- `Z`, `k`, `s`: agregación, mismo patrón simbólico que `MODEL-009`/`MODEL-010`.

Ninguna métrica adicional (no se usa edad, altura, pie hábil, club actual — ninguno está autorizado por `docs/03` para "Profundidad").

---

# 8. Ventana temporal

**No aplica.** A diferencia de Variable001/003/004 (ventana de `N` partidos recientes), la convocatoria a un torneo es una fotografía única por `id_torneo` — no hay una serie de eventos que recortar en el tiempo. El propio torneo específico del partido a predecir (`context.match.torneo`, mismo principio de acotación ya usado por Variable002/`MODEL-012`) ya delimita el conjunto por completo: no hay ningún parámetro `N` que fijar ni calibrar para este componente.

---

# 9. Normalización

Rango de salida: **0 a 100**, acotado por construcción de `Φ` (idéntico mecanismo que Variable003/004, `models/offensive-strength.md` §21, `models/defensive-strength.md` §15) — no requiere `clip` adicional, `Φ` ya garantiza el rango.

---

# 10. El vacío documental de la taxonomía de posiciones (hallazgo explícito de esta misión)

Ya introducido en la sección 4 como fundamento de diseño; se documenta aquí de forma explícita como hallazgo, con su impacto y su vía de resolución futura, siguiendo el mismo estándar de honestidad que `MODEL-011` §10 aplicó a `Estabilidad_Forma`.

**Hallazgo:** ningún documento del Modelo Santiago (`docs/03`, `docs/16`, `docs/31`, `docs/32`, `docs/33`, `data/processed/selecciones-nacionales/README.md`) formaliza los valores ENUM permitidos de `posicion_principal`/`posicion_convocatoria`, pese a que ambas columnas ya están tipadas como `TEXT (CHECK ENUM)` en el modelo físico de PostgreSQL (`docs/33`).

**Por qué no bloquea esta especificación:** la fórmula de la sección 6 agrupa dinámicamente por cualquier valor distinto observado, sin requerir conocer ese dominio de antemano (sección 4) — la ausencia de formalización es una limitación de gobernanza de datos, no una laguna matemática.

**Riesgo real que sí introduce:** sin un ENUM formalizado, dos selecciones podrían registrar la misma posición real con etiquetas de texto distintas (ej. `"Portero"` vs. `"Arquero"` vs. `"GK"`) — la fórmula las trataría como dos posiciones distintas en lugar de una sola, fragmentando artificialmente el conteo y sesgando `Z` hacia abajo para ambas variantes (menos observaciones por grupo, `σ` más inestable). Este riesgo es indetectable desde `models/` — solo se resuelve formalizando el ENUM en el nivel de la Base de Conocimiento.

**Recomendación, no aplicada aquí:** una futura misión de gobernanza de datos (misma familia que la ya recomendada por `GR-010`/`docs/36` para `estado_convocatoria`) que formalice los valores permitidos de `posicion_principal`/`posicion_convocatoria` en `docs/33` y en `data/processed/selecciones-nacionales/README.md` — no bloquea `BUILD-022`, pero mejora la fiabilidad del agrupamiento sin cambiar la fórmula en sí.

---

# 11. Casos límite

| Caso | Comportamiento |
|---|---|
| Selección sin ninguna fila en `convocatorias.csv` para el torneo específico | `disponible=False` — nunca un valor inventado |
| Torneo con una única selección con datos válidos (sin población de comparación) | Toda posición queda con `σ_p` indefinida → todas excluidas → `k=0` → `disponible=False` |
| Fila de `convocatorias.csv` cuyo `id_jugador` no resuelve en `jugadores.csv` (FK rota) | Se descarta esa fila individual — no invalida el resto de la convocatoria del equipo |
| Jugador con `posicion_principal` vacío o no parseable | Se descarta esa fila individual, mismo tratamiento que una fila corrupta en `MODEL-009`/`MODEL-010` |
| Posición con `σ_p` indefinida (menos de 2 selecciones con esa posición en la población) o `σ_p = 0` | Se excluye esa posición del cálculo de `Z`, sin renormalizar — idéntico a Variable003/004 |
| Posición exclusiva del equipo evaluado, ninguna otra selección del torneo la registra | Mismo caso anterior — población de esa posición `<2`, se excluye |
| Todas las posiciones excluidas | `disponible=False` |
| Resultado fuera de `[0,100]` (no debería ocurrir por construcción de `Φ`, pero se valida igual, mismo criterio que Variable003/004) | Se descarta como fallo de cálculo, `disponible=False`, registrado como error |

---

# 12. Complejidad computacional

**Precalculable, `O(J_torneo)`** — una única pasada sobre las filas de `convocatorias.csv` restringidas al `id_torneo` específico (uniendo contra `jugadores.csv` por `id_jugador`), donde `J_torneo` es el total de jugadores convocados por todas las selecciones a ese torneo. Es, de las variables de rendimiento operacionalizadas hasta ahora, la de **menor** complejidad relativa a los datos que toca: no hay ventana de `N` partidos (sección 8), no hay *self-join* sobre el rival (a diferencia de Variable004), y la población se limita a un único torneo, no a una competición completa a lo largo del tiempo (a diferencia de Variable003/004).

---

# 13. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable008 (componente "Profundidad") podría pasar de "Método: Pendiente" a "definido, ver `models/profundidad-plantilla.md`" — actualización editorial futura, fuera de alcance de esta misión de `models/` |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | La fila "Profundidad de plantilla" (hoy "Parcial") podría pasar a "Diseñada" en una futura misión editorial — no se edita aquí |
| `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md` (`MR-004`) | Sin cambios — se cita como origen del alcance reducido ya decidido, no se reabre esa decisión |
| `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) | Sin cambios — confirma que "Profundidad" es categoría C (derivable) |
| `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) | Resuelve, con evidencia directa de `docs/24`, la ambigüedad de alcance que esa misión había detectado y dejado explícitamente sin resolver (ver "Nota de origen") |
| `models/offensive-strength.md` (`MODEL-001`/`MODEL-009`), `models/defensive-strength.md` (`MODEL-002`/`MODEL-010`) | Sin cambios a sus fórmulas — se reutiliza explícitamente su mecanismo de z-score/Φ, con la misma justificación estadística, aplicado aquí a un conteo de convocados en lugar de una métrica de tiro |
| `app/preparation/preparation.py` | Consumidor directo en una futura `BUILD-022`, mismo patrón ya validado por `BUILD-018`/`019`/`020`/`021` |

---

# 14. Impacto

Una vez que esta especificación sea revisada y aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5 — nunca autoaprobada por el Arquitecto Estadístico IA):

- **`VariablePreparation` podría implementar el cálculo real del componente "Profundidad" de Variable008** en una futura `BUILD-022`, siguiendo exactamente la fórmula de la sección 6 y los casos límite de la sección 11 — mismo patrón ya validado por `BUILD-018`/`019`/`020`/`021`.
- **De las cuatro variables analizadas por `GR-010`/`docs/36`, Variable008 pasaría a ser la primera con fórmula matemática completamente definida** — Variable006/007 siguen pendientes de su propia `MODEL-` (recomendación explícita de `GR-010`).
- **No desbloquea, por sí sola, ninguna ejecución real** — `convocatorias.csv`/`jugadores.csv` siguen con 0 filas reales hoy (verificado antes de escribir, mismo estado que el resto de la Base de Conocimiento de Selecciones Nacionales salvo `selecciones.csv`/`competiciones.csv`). El impacto inmediato es metodológico, no de datos — mismo matiz honesto que `MODEL-009`/`010`/`011`/`012`.

---

# 15. Ventajas

- Reutiliza un mecanismo estadístico ya validado dos veces (`MODEL-009`/`MODEL-010`) en lugar de inventar uno nuevo — consistencia metodológica entre las variables de rendimiento del proyecto.
- No requiere conocer de antemano la taxonomía de posiciones (sección 4) — robusta a un vacío de gobernanza de datos que ningún otro componente de este proyecto había expuesto hasta ahora.
- Menor complejidad computacional que Variable001/003/004 (sección 12) — sin ventana de `N`, sin *self-join*.
- Ningún peso ni umbral inventado — la única elección de diseño propia (ponderación igualitaria entre posiciones dinámicamente observadas) sigue exactamente el mismo criterio de derivación matemática que `MODEL-009`/`MODEL-010` (`s` derivado de los pesos, no elegido a mano).

---

# 16. Limitaciones

- **Vacío de formalización de la taxonomía de posiciones** (sección 10) — riesgo real de fragmentación de conteo por variantes de etiqueta de texto (ej. "Portero" vs. "Arquero"), no detectable ni corregible desde `models/`.
- **No filtra por `estado_convocatoria`** (sección 5) — cuenta también convocados posteriormente dados de baja, por no existir un ENUM formalizado que permita distinguir ese estado con seguridad; podría sobreestimar la profundidad real en escenarios de bajas confirmadas.
- Compara únicamente contra selecciones del mismo torneo — un torneo con pocas selecciones participantes (población pequeña) produce `σ_p` inestable, mismo tipo de limitación ya documentada para competiciones pequeñas en `MODEL-009`/`MODEL-010`.
- Asume, sin una cita textual que lo confirme explícitamente en `docs/03`/`docs/16`, que todas las selecciones de un mismo torneo están sujetas al mismo reglamento de tamaño de convocatoria — supuesto razonable (convención estándar de torneos de selecciones) pero no verificado documentalmente en este proyecto.
- Ponderación igualitaria entre posiciones (`1/k`) es un placeholder sin calibrar, igual que los pesos de Variable003/004 — ninguna evidencia estadística real la respalda todavía.

---

# 17. Aplicación dentro del Modelo Santiago

Es la especificación matemática oficial que `VariablePreparation` deberá implementar para el componente "Profundidad" de Variable008 (alcance reducido ya fijado por `MR-004`), alimentando `engine/01`/`engine/02` como variable contextual (`docs/17`). No alimenta ningún otro motor ni ninguna otra señal de Variable008 ("valor de mercado", "experiencia" quedan fuera del alcance de esta misión y del alcance reducido ya vigente).

---

# 18. Referencias

- `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md` (`MR-004`) — origen del alcance reducido de Variable008.
- `docs/17-Matriz-de-Consumo-de-Variables.md` — fija la fuente (`convocatorias.csv`+`jugadores.csv.posicion_principal`) y la forma ("conteo por posición") que esta misión formaliza matemáticamente.
- `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`), `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) — confirman disponibilidad de datos y recomiendan explícitamente esta investigación como siguiente paso.
- `models/offensive-strength.md` (`MODEL-001`/`MODEL-009`), `models/defensive-strength.md` (`MODEL-002`/`MODEL-010`) — origen del mecanismo z-score/Φ reutilizado aquí.
- `docs/33-Modelo-Fisico-PostgreSQL.md` — confirma el tipo `TEXT (CHECK ENUM)` de las columnas de posición y la ausencia de sus valores permitidos formalizados (sección 10).

---

# 19. Versión 2.0 (siguiente iteración de esta investigación)

Pendiente, condicionado a datos reales suficientes y a gobernanza de datos adicional:

- Formalización del ENUM de `posicion_principal`/`posicion_convocatoria` (sección 10) — permitiría verificar si la fragmentación de conteo por variantes de etiqueta es un problema real, no solo teórico.
- Formalización del ENUM de `estado_convocatoria` (recomendación ya compartida con `GR-010` para Variable006) — permitiría excluir bajas confirmadas del conteo de profundidad.
- Evaluación empírica de si una ponderación no igualitaria entre posiciones (ej. mayor peso a porteros, posición con menor margen de rotación táctica) mejora la capacidad predictiva frente a la ponderación igualitaria actual — hoy descartada por falta de evidencia, no por imposibilidad.
- Evaluación de si "Experiencia" (categoría C, aproximable por conteo de convocatorias históricas, `docs/27`) debería incorporarse como un segundo componente de Variable008 en una futura ampliación de alcance — hoy fuera de alcance por decisión ya fijada de `MR-004`.

---

# Validaciones

- **¿La fórmula usa solo datos autorizados por `docs/03`/`docs/17` para el componente "Profundidad" de Variable008?** Sí — únicamente `convocatorias.csv` y `jugadores.csv.posicion_principal`, exactamente las columnas ya fijadas por `docs/17`.
- **¿Se fija algún peso sin justificar?** La ponderación igualitaria entre posiciones (`1/k`) sigue el mismo criterio de derivación que `MODEL-009`/`MODEL-010` (`s` derivado matemáticamente, no elegido a mano) — documentada explícitamente como placeholder sin calibrar (sección 16), igual que sus precedentes.
- **¿Se inventó alguna fuente de datos o taxonomía de posiciones?** No — se verificó explícitamente que ningún documento formaliza esa taxonomía (sección 10, sección 4) y se diseñó la fórmula para no necesitarla de antemano, en lugar de inventarla.
- **¿Se introdujo alguna API externa?** No.
- **¿Es reproducible?** Sí — función determinista de los datos de convocatoria observados, sin aleatoriedad ni estimación subjetiva.
- **¿Se detuvo la misión por falta de rigor matemático?** No fue necesario — la sección 4 explica por qué el vacío de formalización de posiciones no impide una definición rigurosa.

---

# Cierre obligatorio

**1. ¿Qué definición operacional quedó aprobada?**
Profundidad de Plantilla = z-score del conteo de convocados por posición del equipo, comparado contra la población de todas las selecciones convocadas al mismo torneo específico, agregado con `Φ` en un índice 0-100 — sección 2.

**2. ¿Qué fuente de datos consume?**
`convocatorias.csv` (identificación de convocados por torneo/selección) y `jugadores.csv.posicion_principal` (clasificación por posición) — sección 5, exactamente la fuente ya fijada por `docs/17`. No usa `estadisticas_partido.csv`, `lesiones.csv` ni ninguna fuente externa.

**3. ¿Qué métricas utiliza?**
`conteo(T,p)` por posición dinámicamente observada, `μ_p`/`σ_p` de la población del torneo, `z_p` por posición, agregados en `Z`/`k`/`s` — sección 7. Ninguna métrica ajena a la convocatoria (no edad, no club, no valor de mercado).

**4. ¿Qué fórmula matemática quedó definida?**
`Profundidad_Plantilla = 100·Φ(Z/s)`, con `Z = Σ(1/k)·z_p` y `s = √(1/k)`, `k` = número de posiciones no excluidas — sección 6. Mismo mecanismo de `MODEL-009`/`MODEL-010`, aplicado a un conteo de convocatoria en vez de una métrica de tiro.

**5. ¿Qué rango produce?**
0 a 100, acotado por construcción de `Φ`, sin necesidad de `clip` — sección 9.

**6. ¿Qué casos límite contempla?**
Selección sin convocatoria válida → `disponible=False`; torneo sin población de comparación → `disponible=False`; fila con FK rota o posición no parseable → se descarta individualmente; posición con `σ` indefinida o 0 → se excluye sin renormalizar; todas las posiciones excluidas → `disponible=False` — sección 11.

**7. ¿Qué documentos quedaron afectados?**
Solo `models/profundidad-plantilla.md` (creado). `docs/03`, `docs/17` quedan documentados como afectados a futuro por una misión editorial, ninguno modificado — sección 13. Resuelve, sin editarlo, el hallazgo de ambigüedad de alcance que `docs/36`/`GR-010` había dejado abierto (ver "Nota de origen").

**8. ¿Qué desbloqueará BUILD-022?**
El camino metodológico completo para implementar el componente "Profundidad" de Variable008 en `VariablePreparation`, mismo patrón que `BUILD-018`/`019`/`020`/`021`. No desbloquea, por sí solo, una predicción real — `convocatorias.csv`/`jugadores.csv` siguen sin filas reales (verificado antes de escribir).

**9. ¿Queda completamente implementable en V1?**
Sí, para el alcance ya autorizado ("Profundidad" únicamente) — la fórmula queda completamente definida, sin ningún elemento pendiente de investigación adicional para ese alcance. "Valor de mercado" y "Experiencia" (las otras dos señales de Variable008) permanecen fuera de este alcance, ya decidido por `MR-004`, no por esta misión.

**10. ¿Qué misión recomendarías después?**
La misma aprobación pendiente que `MODEL-009`/`010`/`011`/`012` (Arquitecto Estadístico Humano), seguida de `BUILD-022` (implementación real del componente "Profundidad" de Variable008, mismo patrón que `BUILD-018`-`021`). En paralelo, sigue vigente la recomendación de `GR-010` de encargar `MODEL-` para Variable007 (siguiente prioridad tras esta misión) y una misión de gobernanza de datos que formalice los ENUM de `posicion_principal`/`posicion_convocatoria`/`estado_convocatoria`.

---

# Fuera de alcance de esta misión

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext`, `Engine01`, `Engine02` ni `VariablePreparation`.
- No se modifica `docs/03`, `docs/16`, `docs/17`, `docs/30` ni ningún otro documento existente.
- No se especifican "Valor de mercado" ni "Experiencia" (las otras dos señales de Variable008) — quedan fuera del alcance reducido ya fijado por `MR-004`.
- No se formaliza el ENUM de `posicion_principal`/`posicion_convocatoria`/`estado_convocatoria` — se documenta como hallazgo pendiente, no se resuelve aquí.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano.

---

Fin del documento.
