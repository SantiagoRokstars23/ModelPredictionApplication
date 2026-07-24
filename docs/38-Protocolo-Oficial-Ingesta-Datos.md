# Protocolo Oficial de Ingesta y Validación de Datos

**Archivo:** `docs/38-Protocolo-Oficial-Ingesta-Datos.md`

**Misión:** MS-012 — Protocolo Oficial de Ingesta y Validación de Datos

**Versión:** 1.0.0

**Estado:** Investigación documental — sin código, sin CSV poblados, sin Engine/Runtime/Preparation/`PredictionContext` modificados

---

## Nota de origen y alcance

Verificado antes de escribir (`docs/22` §3, "Lista de verificación previa"): `MS-012` es el siguiente identificador libre de la serie (`MS-011`, la misión anterior, es la última registrada en `docs/00-Project-Tracker.md`) — **sin colisión de numeración**, a diferencia de lo detectado en `MS-011`.

Esta misión no define un procedimiento nuevo desde cero: **recopila, ordena y hace explícitas** reglas que ya existen, dispersas entre `data/processed/README.md`, `data/processed/selecciones-nacionales/README.md`, `docs/05-Base-de-Conocimiento.md`, `docs/32-Modelo-Relacional-Oficial.md` y `docs/33-Modelo-Fisico-PostgreSQL.md` — ninguno de esos documentos se modifica aquí. El resultado es el protocolo único que toda futura misión de población (`MS-013` en adelante, incluida la secuencia ya recomendada por `docs/37`/`MS-011`) deberá seguir.

---

# 1. Objetivo

Definir el procedimiento oficial de ingesta y validación de datos externos hacia `data/processed/selecciones-nacionales/`: qué fuentes son aceptables por entidad, qué reglas exactas determinan si una fila entra o se rechaza, cómo se actualiza un dato ya incorporado, y qué debe auditarse — sin poblar ningún CSV ni modificar ningún componente de código.

---

# 2. Metodología

Se releyó, verificando contra el estado real de los documentos (no de memoria): `docs/05-Base-de-Conocimiento.md` (flujo de datos, validación, normalización, versionado, ya vigentes), `docs/32-Modelo-Relacional-Oficial.md` (identidad conceptual, entidades independientes/derivadas, §5/§7/§8), `docs/33-Modelo-Fisico-PostgreSQL.md` (restricciones de integridad físicas, §7), `data/processed/README.md` y `data/processed/selecciones-nacionales/README.md` (restricciones ya declaradas por entidad), `docs/27`/`docs/36`/`MODEL-013`/`MODEL-015` (hallazgos de gobernanza de datos ya detectados y no resueltos, heredados aquí sin reabrirlos) y `docs/37-Estrategia-Poblacion-Base-Conocimiento.md` (`MS-011`, precedente inmediato: orden de población, fuentes recomendadas por entidad).

---

# 3. Flujo oficial de ingesta

**Relación con el flujo ya vigente (`docs/05`, sección "Flujo de los Datos"):** este protocolo no reemplaza ese flujo — lo opera-cionaliza para el caso específico de incorporar una fila nueva o corregida a `data/processed/selecciones-nacionales/`. La correspondencia exacta:

| Paso de este protocolo | Paso equivalente en `docs/05` |
|---|---|
| Fuente oficial | Fuentes de Información |
| Captura | Recolección |
| Validación | Validación |
| Normalización | Normalización |
| **Revisión manual** | Nuevo en este protocolo — operacionaliza la regla ya vigente de `docs/05`: "nunca deberá corregirse automáticamente sin evidencia" |
| CSV en `processed/` | `data/processed` |

```
Fuente oficial (docs/05 "Fuentes de Información"; clasificada Primaria/
                Secundaria/Prohibida por entidad, sección 4 de este documento)
        │
        ▼
Captura (docs/05 "Recolección" — únicamente información necesaria para
         el modelo, nunca datos irrelevantes; siempre trazable a la fuente
         exacta consultada, con fecha de captura)
        │
        ▼
Validación (sección 5-6 de este documento: integridad, formato, fecha,
             duplicados, valores nulos, consistencia, FK — docs/05
             "Validación", sin redefinirla)
        │
        ▼
Normalización (docs/05 "Normalización": mismo formato de fecha
                YYYY-MM-DD, mismo identificador para un mismo equipo/
                jugador/estadio ya existente, nunca un segundo
                identificador para la misma entidad real)
        │
        ▼
Revisión manual (verificación humana final antes de incorporar — nunca
                  se salta este paso para datos que alimentan una
                  Variable Oficial de Nivel A; ver sección 6, "¿Puede
                  existir un dato sin fuente?")
        │
        ▼
CSV en processed/ (única fuente autorizada para el Engine, docs/05
                     "processed/")
```

**Por qué se agrega "Revisión manual" como paso explícito, sin contradecir `docs/05`:** `docs/05` ya exige, en su sección "Validación", que "si un dato no supera la validación deberá descartarse o marcarse para revisión" — pero no nombra ese paso como una etapa propia del flujo, dejándolo implícito dentro de "Validación". Este protocolo lo separa explícitamente porque la validación automatizable (formato, tipo, FK, rangos — sección 5) es de naturaleza distinta a la revisión humana de plausibilidad (¿es creíble que este jugador tenga esta fecha de nacimiento? ¿coincide el resultado con lo que reporta la fuente primaria?) — la misma distinción que `docs/33` §7 ya hace entre restricciones expresables como `CHECK` físico y las que "no son expresables como `CHECK` simple" y requieren validarse en la capa de aplicación.

---

# 4. Fuentes permitidas por entidad

Clasificación en tres niveles, extendiendo con precisión el criterio ya usado en `docs/37`/`MS-011` (sección 7 de ese documento) y en los precedentes reales de `MS-002`/`MS-006`:

- **Fuente Primaria:** el organismo oficial dueño del dato (FIFA, la confederación correspondiente, la federación nacional). Siempre preferida cuando existe.
- **Fuente Secundaria:** verificación cruzada de un dato ya obtenido de fuente primaria, o fuente ampliamente reconocida en estadística de fútbol cuando no existe una fuente primaria accesible para un dato histórico específico. Nunca reemplaza a una fuente primaria si esta existe y está disponible.
- **Fuente Prohibida:** cualquier fuente sin verificación posible, o explícitamente descartada por una misión anterior.

| Entidad | Fuente Primaria | Fuente Secundaria | Fuente Prohibida |
|---|---|---|---|
| `selecciones.csv` | FIFA (ranking oficial), federación nacional | — | Agregadores no verificables |
| `competiciones.csv` / `torneos.csv` | Confederación organizadora (FIFA, UEFA, CONMEBOL, CAF, AFC, CONCACAF, OFC) | Wikipedia (ya usada como verificación secundaria en `MS-006`) | Fuentes sin URL/referencia citable |
| `estadios.csv` | Sitio oficial del estadio o de la federación local | Bases de datos de estadios ampliamente verificadas (ej. worldstadiums.com) | Wikis editables sin fuente primaria citada dentro del propio artículo |
| `arbitros.csv` | Listas oficiales FIFA/confederación ("FIFA International Referees List") | — | Fuentes sin verificación de categoría/vigencia |
| `jugadores.csv` | Sitio oficial de la federación (plantilla/roster oficial) | — | **Transfermarkt** (restricción ya fijada explícitamente en `MODEL-015` para lesiones, generalizada en `MS-011` a toda entidad — se hereda aquí, no se reabre) |
| `convocatorias.csv` | Comunicado oficial de convocatoria de la federación | — | Rumores o listas no oficiales previas al anuncio |
| `partidos.csv` | Sitio oficial de la competición/confederación (resultados oficiales) | RSSSF (verificación histórica, ampliamente reconocida) | Marcadores de redes sociales sin confirmación oficial |
| `estadisticas_partido.csv` | Reporte oficial de partido de la competición (cuando incluye `xg`/disparos) | Proveedores especializados reconocidos (Opta, StatsBomb, FBref) — **riesgo ya identificado en `MS-011`: cobertura real de `xg` para selecciones nacionales no garantizada** | Estimaciones propias de `xg` sin metodología publicada y verificable |
| `lesiones.csv` | Comunicado médico oficial de la federación/club | — | **Transfermarkt** (misma restricción heredada de `MODEL-015`); rumores de prensa sin confirmación oficial |
| `cuotas.csv` | Casa de apuestas licenciada, con `fecha_captura` explícita | — | Casas de apuestas no licenciadas o sin trazabilidad de fecha |

---

# 5. Reglas de aceptación

Responde exactamente las preguntas exigidas por el brief:

**¿Puede existir un dato sin fuente?** No. `docs/05` ya lo exige ("Toda fuente deberá ser identificable y verificable") y `lesiones.csv.fuente` ya lo hace obligatorio a nivel de esquema (`data/processed/selecciones-nacionales/README.md`: "`fuente` obligatoria"). Este protocolo generaliza esa misma exigencia a las 11 entidades del módulo, aunque hoy solo `lesiones.csv` tenga una columna dedicada para registrarla explícitamente — para el resto de entidades, la fuente debe quedar trazada en el `CHANGELOG.md`/`README.md` de la misión que incorpora los datos (mismo mecanismo ya usado en `MS-002`/`MS-006`), a falta de una columna de fuente por fila en el esquema actual (hallazgo, sección 8).

**¿Puede existir una fecha estimada?** Sí, únicamente cuando el propio esquema ya distingue explícitamente el campo como una estimación — precedente ya existente: `lesiones.fecha_estimada_retorno` es, por diseño, distinto de `lesiones.fecha_retorno_real` (`data/processed/selecciones-nacionales/README.md`); ambos pueden coexistir en la misma fila, con significado distinto. Este protocolo generaliza esa misma convención: una fecha estimada nunca se almacena en un campo que el esquema documenta como "fecha real/oficial" — solo en un campo que explícitamente admite estimación. Ningún campo fuera de `lesiones.fecha_estimada_retorno` admite hoy una fecha estimada (ej. `partidos.fecha`, `torneos.fecha_inicio`/`fecha_fin` no tienen un campo "estimado" paralelo) — para esas entidades, una fecha sin confirmar no se incorpora todavía (ver pregunta siguiente).

**¿Qué ocurre si dos fuentes discrepan?** Se prioriza la Fuente Primaria (sección 4) sobre la Secundaria. Si ambas fuentes consultadas son Primarias y discrepan entre sí (ej. la confederación y la federación nacional reportan un dato distinto), la fila **no se incorpora** hasta resolver la discrepancia — se documenta la discrepancia (ambas fuentes, ambos valores) en el `CHANGELOG.md`/observaciones de la misión, nunca se promedia, interpola ni se elige arbitrariamente uno de los dos valores sin justificación explícita (`CLAUDE.md`: "nunca inventes información"; `docs/05`: "nunca deberá corregirse automáticamente sin evidencia").

**¿Qué ocurre si falta un campo obligatorio?** La fila se rechaza — no se incorpora con el campo vacío ni con un valor inventado (`docs/05`: "nunca inventar datos faltantes"). Mismo criterio ya aplicado consistentemente en todo el Engine (`VariablePreparation`, `BUILD-017` a `024`: ausencia de dato → `disponible=False`, nunca un valor inventado) — extendido aquí a la etapa de ingesta, antes de que el dato llegue siquiera a `processed/`.

**¿Qué ocurre si el dato aún no ha sido confirmado oficialmente?** No se incorpora a `processed/` todavía. `docs/05` ya lo exige de forma general ("Toda información deberá incorporarse primero a la Base de Conocimiento antes de ser utilizada" presupone que la información ya es válida) — un dato no confirmado se mantiene en la etapa de "Captura"/"Revisión manual" (sección 3) hasta que exista confirmación de una Fuente Primaria o, en su defecto, de una Fuente Secundaria suficientemente verificada. No existe hoy, en el esquema físico (`docs/33`), un estado ENUM formalizado del tipo "pendiente de confirmación" para ninguna entidad — se documenta como hallazgo (sección 8), no se resuelve inventando un valor ENUM nuevo en esta misión.

---

# 6. Reglas de rechazo

Una fila **debe** descartarse, nunca incorporarse a `processed/`, cuando:

| Caso | Regla | Fuente ya vigente |
|---|---|---|
| **IDs duplicados** | Clave primaria o clave única de negocio (ej. `(id_torneo, id_seleccion, id_jugador)` en `convocatorias`; `(id_partido, id_seleccion)` en `estadisticas_partido`) ya existe en el archivo | `docs/33` §7 ("`UNIQUE`"), `data/processed/selecciones-nacionales/README.md` (restricciones por entidad) |
| **FK inexistente** | Cualquier columna `FK →` (sección 4 del grafo, `docs/37`/`MS-011`) no resuelve contra una fila ya existente de la entidad referenciada | `docs/33` §7 ("Integridad referencial") |
| **Resultado imposible** | `goles_local`/`goles_visitante` negativos; `disparos_al_arco > disparos_totales`; `id_seleccion_local = id_seleccion_visitante` | `docs/33` §7 (`CHECK` rango/negocio), `README.md` del módulo |
| **Partido suspendido / estado no confirmado** | Ninguna fila de `partidos.csv` con `goles_local`/`goles_visitante` completados si `estado_partido` no es el único valor de "finalizado" ya confirmado textualmente en el esquema (`README.md`: "goles solo se completan si `estado_partido = finalizado`") — **ver hallazgo, sección 8: ningún otro valor de `estado_partido` está formalizado**, por lo que esta misión no puede enumerar qué otros estados (ej. "suspendido", "aplazado") son válidos; solo puede confirmar que sin `estado_partido = finalizado` no se completan los goles | `README.md` del módulo, `docs/33` §4 |
| **Estadísticas incompatibles** | Una fila de `estadisticas_partido.csv` cuyo `id_partido` no tiene una fila correspondiente y finalizada en `partidos.csv`; o `posesion_pct` fuera de `[0,100]` | `README.md` del módulo, `docs/33` §7 |
| **Campo derivado almacenado directamente** | Cualquier intento de escribir un valor en un campo que el esquema ya declara derivado y **excluido** — ej. `torneos.campeon_id_seleccion` (se deriva de `partidos` con `fase = final`, nunca se almacena), `estadisticas_partido.xga` (se deriva por self-join del `xg` del rival), `cuotas.probabilidad_implicita` (se calcula en `engine/06`) | `README.md` del módulo ("Campo excluido"), `docs/32` §8 |
| **Fuente prohibida o sin verificación** | La fila proviene de una fuente clasificada como Prohibida (sección 4), o no puede trazarse a ninguna fuente identificable | `docs/05` ("toda fuente deberá ser identificable y verificable") |
| **Mezcla de competiciones incompatibles** | Datos de fútbol de clubes, categorías juveniles o fútbol femenino incorporados a un módulo cuyo alcance ya está fijado a selecciones absolutas masculinas (`MS-006`) | `docs/05` ("nunca mezclar competiciones incompatibles"), `README.md` del módulo |

---

# 7. Convención de actualización

**Regla general, heredada sin cambios de `docs/05`:** "los datos nunca deberán sobrescribirse... toda modificación importante deberá quedar registrada."

Traducida a una convención operativa concreta para archivos CSV:

- **Fila nueva (dato que no existía antes):** se **agrega** — nunca requiere ninguna otra acción sobre filas ya existentes.
- **Corrección de un valor ya incorporado (ej. un dato capturado con error):** se **corrige la fila**, pero la corrección debe quedar documentada explícitamente en el `CHANGELOG.md` (qué cambió, de qué valor a qué valor, por qué, con qué fuente) y en la sección "Estado de los archivos" del `README.md` del módulo — nunca una edición silenciosa sin rastro. Esto es distinto de "sobrescribir": lo que `docs/05` prohíbe es perder la trazabilidad de que existió un valor anterior, no la corrección en sí misma cuando hay evidencia de un error.
- **Actualización de un dato que cambia legítimamente con el tiempo** (ej. `ranking_fifa_actual`, que se actualiza periódicamente por diseño — el propio esquema ya incluye `ranking_fifa_fecha` para esto): se **reemplaza el valor** y se actualiza la fecha de vigencia asociada — el esquema ya anticipa este caso con un campo de fecha dedicado, no es una corrección de error.
- **No se versionan filas individuales** dentro de un mismo CSV (no existe, en el esquema actual, un campo de versión por fila) — el versionado ocurre a nivel de **módulo completo** (`README.md`, campo "Versión", ya en `1.1.0`), incrementado cada vez que se agrega o corrige contenido de forma significativa (misma convención ya usada en `MS-002`/`MS-006`, formalizada en `docs/37`/`MS-011` sección 9).
- **Nunca se elimina una fila** que ya haya sido consumida por una predicción persistida (`docs/05`: "nunca eliminar historial") — si una fila resulta errónea después de haber sido usada, se corrige (con trazabilidad, arriba) en lugar de eliminarse, para no invalidar retroactivamente auditorías ya registradas.

---

# 8. Auditoría

Qué debe quedar registrado cada vez que se modifica un CSV de `data/processed/selecciones-nacionales/` — síntesis de la sección "Calidad de Datos" de `docs/05` (ya vigente, no redefinida) aplicada a este caso concreto:

1. **Fecha de actualización** — cuándo se incorporó o corrigió el dato (ya exigido por `docs/05`).
2. **Fuente** — la fuente exacta consultada (sección 4), no solo su categoría (Primaria/Secundaria).
3. **Nivel de confianza** — si la fuente es Primaria (alta) o Secundaria (media, sujeta a verificación cruzada) — ya exigido por `docs/05`.
4. **Cobertura** — qué alcance tiene el lote incorporado (ej. "10 competiciones", "40 selecciones Top FIFA") — mismo patrón ya usado en el `README.md` del módulo, sección "Estado de los archivos".
5. **Observaciones** — cualquier decisión de diseño no obvia tomada durante la incorporación (mismo patrón ya usado en las "Decisiones arquitectónicas aplicadas" del `README.md` del módulo, ej. la convención de "Amistosos Internacionales").
6. **Misión que lo incorporó** — registro en `docs/00-Project-Tracker.md`, ya práctica establecida sin excepción desde `MS-001`.

**Dónde queda registrado, en la práctica ya vigente (no un mecanismo nuevo):** `CHANGELOG.md` (qué cambió y por qué, por misión), `data/processed/selecciones-nacionales/README.md` (sección "Estado de los archivos", el estado agregado actual de cada entidad) y `docs/00-Project-Tracker.md` (qué misión, cuándo, con qué dependencias). Los tres ya existen y ya se usan con este propósito — este protocolo no crea un cuarto mecanismo, solo formaliza que los tres, juntos, constituyen la auditoría completa exigida.

---

# 9. Validaciones generales recopiladas (sin modificar sus fuentes)

Consolidación, no redefinición, de las reglas ya dispersas en los cuatro documentos que el brief pide recopilar:

| Regla | Fuente exacta |
|---|---|
| Verificar Integridad, Formato, Fecha, Duplicados, Valores nulos, Consistencia antes de almacenar | `docs/05`, sección "Validación" |
| Fechas en `YYYY-MM-DD`; porcentajes `0-100`; probabilidades `0.00-1.00`; un único identificador por entidad real (nunca múltiples nombres para el mismo equipo) | `docs/05`, sección "Normalización" |
| Nunca inventar datos faltantes, modificar estadísticas oficiales, eliminar historial, usar datos sin validar, mezclar competiciones incompatibles | `docs/05`, sección "Reglas" |
| Todo campo debe justificarse por ser insumo de una Variable Oficial, un paso del algoritmo, un motor, o integridad/trazabilidad/auditabilidad | `docs/05`, "Principio de Justificación de Datos" |
| `NOT NULL` en todo campo obligatorio; `UNIQUE` en claves de negocio y combinaciones ya documentadas; `CHECK` de rango y de negocio; integridad referencial sin borrado en cascada de historial | `docs/33`, sección 7 |
| Ciertas reglas (suma de probabilidades ≈ 1; coherencia entre filas relacionadas) no son expresables como `CHECK` físico simple — deben validarse en la capa de aplicación, no forzarse a nivel de motor de base de datos | `docs/33`, sección 7 |
| Un jugador solo puede tener una `id_seleccion` activa a la vez (índice único parcial recomendado) | `docs/33`, sección 7; `README.md` del módulo |
| Restricciones específicas por entidad (`id_seleccion` único 3 letras; `disparos_al_arco ≤ disparos_totales`; `cuota_decimal > 1.00`; `id_seleccion_local ≠ id_seleccion_visitante`; etc.) | `data/processed/selecciones-nacionales/README.md`, tabla de cada entidad |
| Campos derivados nunca se almacenan directamente (`campeon_id_seleccion`, `xga`, `probabilidad_implicita`) | `README.md` del módulo ("Campo excluido"); `docs/32`, sección 8 |
| Toda entidad tiene una identidad conceptual y una clave natural propia, independiente de su clave técnica | `docs/32`, sección 5 |
| `Equipo`, `Competición`, `Estadio`, `Árbitro` son entidades independientes (pueden poblarse sin que exista ninguna otra entidad primero) | `docs/32`, sección 7 |
| Toda información deberá estar validada; no se permiten duplicados; formatos consistentes; nunca almacenar información incompleta | `data/processed/README.md` |

---

# 10. Hallazgos (documentados, no resueltos en esta misión)

1. **`estado_partido` (ENUM, `partidos.csv`) nunca tuvo sus valores permitidos formalizados más allá de `"finalizado"`** — ningún documento (`docs/05`, `docs/32`, `docs/33`, el `README.md` del módulo) enumera qué otros valores existen (ej. "programado", "suspendido", "aplazado"). Esto impide, en esta misión, definir con precisión la regla de rechazo "partido suspendido" pedida por el brief más allá de "no se completan `goles_local`/`goles_visitante` si el estado no es `finalizado`" — mismo tipo de vacío de gobernanza ya detectado por `MODEL-013` (`posicion_principal`), `docs/27`/`GR-010` (`estado_convocatoria`) y `MODEL-015` (`lesiones.estado`/`gravedad`). Se hereda, no se reabre ni se inventa un valor.
2. **Ninguna entidad tiene, en el esquema físico actual, un campo de "fuente" por fila** salvo `lesiones.csv.fuente` — para el resto de entidades, la trazabilidad de fuente vive únicamente en `CHANGELOG.md`/`README.md` a nivel de lote/misión, no a nivel de fila individual. Esta misión no propone agregar una columna nueva (fuera de alcance: "no modificar CSV/esquema"), pero lo documenta como una limitación real de trazabilidad granular.
3. **No existe un estado ENUM formalizado para "dato capturado, pendiente de confirmación oficial"** en ninguna entidad — la sección 5 ("¿Qué ocurre si el dato aún no ha sido confirmado?") responde conceptualmente ("no se incorpora todavía"), pero el esquema no tiene un mecanismo físico para representar ese estado intermedio dentro de `processed/` mismo (hoy, la única forma de "no incorporar" es, literalmente, no escribir la fila).
4. **La cobertura real de `xg`/estadísticas avanzadas para partidos de selecciones nacionales fuera de grandes torneos no está verificada** — ya identificado como riesgo en `docs/37`/`MS-011` (sección 10 de ese documento), se hereda aquí como una limitante directa de qué fuentes son realmente viables en la práctica para `estadisticas_partido.csv`, más allá de su clasificación teórica como Primaria/Secundaria (sección 4).

---

# Cierre obligatorio (preguntas del brief de esta misión)

**1. ¿Qué documento fue creado?**
`docs/38-Protocolo-Oficial-Ingesta-Datos.md` (este documento).

**2. ¿Qué flujo oficial de ingestión quedó definido?**
Fuente oficial → Captura → Validación → Normalización → Revisión manual → CSV en `processed/` — operacionalización explícita del flujo ya vigente de `docs/05`, con "Revisión manual" como paso nuevo y explícito que separa la validación automatizable de la verificación humana de plausibilidad — sección 3.

**3. ¿Qué categorías de fuentes se aprobaron?**
Fuente Primaria (organismo oficial dueño del dato), Fuente Secundaria (verificación cruzada o fuente ampliamente reconocida, nunca sustituye a la Primaria si existe) y Fuente Prohibida (sin verificación posible, o ya descartada explícitamente — ej. Transfermarkt, heredado de `MODEL-015`) — clasificadas por cada una de las 11 entidades, sección 4.

**4. ¿Qué reglas obligatorias debe cumplir una fila antes de entrar en `processed/`?**
Fuente identificable y verificable siempre; fecha estimada solo en un campo que el esquema ya distingue como tal (`lesiones.fecha_estimada_retorno`); ante discrepancia entre fuentes, prioridad a la Primaria y nunca promediar/inventar; campo obligatorio ausente → fila rechazada; dato no confirmado oficialmente → no se incorpora todavía — sección 5.

**5. ¿Qué situaciones obligan a rechazar una fila?**
IDs duplicados, FK inexistente, resultado imposible (goles negativos, `disparos_al_arco > disparos_totales`, mismo equipo local y visitante), estado de partido no confirmado como `finalizado` con goles ya completados, estadísticas sin partido finalizado correspondiente, campos derivados almacenados directamente, fuente prohibida, y mezcla de competiciones incompatibles — sección 6.

**6. ¿Cómo quedó definido el proceso de actualización de datos?**
Fila nueva → se agrega; corrección de un valor ya incorporado → se corrige con trazabilidad completa en `CHANGELOG.md`/`README.md`, nunca en silencio; dato que cambia legítimamente (ej. ranking FIFA) → se reemplaza junto con su fecha de vigencia; sin versionado por fila (solo por módulo completo, `README.md`); nunca se elimina una fila ya consumida por una predicción persistida — sección 7.

**7. ¿Qué mecanismo de auditoría quedó documentado?**
Fecha de actualización, fuente exacta, nivel de confianza, cobertura, observaciones y misión que lo incorporó — registrados en los tres mecanismos ya existentes y ya usados (`CHANGELOG.md`, `README.md` del módulo, `docs/00-Project-Tracker.md`), sin crear un cuarto mecanismo nuevo — sección 8.

**8. ¿Qué documentos del proyecto fueron utilizados como autoridad?**
`data/processed/README.md`, `data/processed/selecciones-nacionales/README.md`, `docs/05-Base-de-Conocimiento.md`, `docs/32-Modelo-Relacional-Oficial.md`, `docs/33-Modelo-Fisico-PostgreSQL.md` — exactamente los cuatro que el brief pide recopilar, ninguno modificado. También se citó `docs/37`/`MS-011` (precedente inmediato de fuentes por entidad) y los hallazgos ya heredados de `MODEL-013`/`MODEL-015`/`docs/27`/`GR-010`.

**9. ¿Qué hallazgos quedaron documentados sin resolver?**
`estado_partido` sin ENUM formalizado más allá de `"finalizado"`; ausencia de un campo de fuente por fila salvo en `lesiones.csv`; ausencia de un estado ENUM para "dato pendiente de confirmación"; cobertura real de `xg` para selecciones nacionales sin verificar — sección 10, ninguno resuelto aquí.

**10. ¿Se actualizaron CHANGELOG.md y docs/00-Project-Tracker.md?**
Sí, ambos — ver entradas de esta misma misión (`MS-012`).

---

# Lista de verificación de cierre (`docs/22`, sección 5 — set estándar de 6 preguntas)

**1. ¿Qué problema resolvió?**
La ausencia de un procedimiento único y explícito de ingesta — hasta ahora, las reglas de validación/aceptación/rechazo existían dispersas en cuatro documentos distintos, sin una secuencia operativa ni una clasificación de fuentes por entidad que una futura misión de población pudiera seguir directamente.

**2. ¿Qué problemas nuevos descubrió?**
Ninguno estructuralmente nuevo — los cuatro hallazgos de la sección 10 son extensiones o confirmaciones de vacíos de gobernanza ya detectados por misiones anteriores (`MODEL-013`, `MODEL-015`, `docs/27`/`GR-010`, `docs/37`/`MS-011`), no hallazgos genuinamente nuevos de esta misión.

**3. ¿Qué documentos podrían necesitar actualización futura?**
`data/processed/selecciones-nacionales/README.md` podría, en una futura misión de gobernanza de datos, agregar una columna de fuente por fila para las entidades que hoy no la tienen (hallazgo 2, sección 10) — no se modifica aquí (fuera de alcance). `docs/33` podría formalizar el ENUM de `estado_partido` en una futura misión dedicada — misma familia de recomendación ya hecha para `posicion_principal`/`estado_convocatoria`/`lesiones.estado`.

**4. ¿Qué impacto tiene sobre el proyecto?**
Cierra la última pieza puramente metodológica que faltaba antes de ejecutar la secuencia de captura de datos ya recomendada por `docs/37`/`MS-011` (`MS-012` a `MS-017` en ese documento, ahora `MS-013` en adelante dado que este protocolo ocupó el número `MS-012`) — toda futura misión de población puede referenciar este protocolo en lugar de re-derivar sus propias reglas de aceptación/rechazo.

**5. ¿Cómo cambia el riesgo arquitectónico?**
Reduce el riesgo de que distintas misiones de población apliquen criterios de validación inconsistentes entre sí (ej. que una misión acepte una fecha estimada donde otra la rechace) — no introduce ningún riesgo nuevo, es un documento de procedimiento.

**6. ¿Qué impacto cualitativo tiene sobre el Índice de Madurez Arquitectónica (IMA)?**
Sin IMA formal todavía (mismo estado que `GOV-001`/`GOV-002`/`MS-011`). Cualitativamente, complementa la madurez del eje de datos iniciada por `MS-011`, agregando la dimensión de **procedimiento repetible** (cómo se incorpora un dato) a la ya cubierta por esa misión (en qué orden y con qué volumen).

---

# Gestión de hallazgos (`docs/22`, sección 7)

Los cuatro hallazgos de la sección 10 se documentan con el mismo rigor que el objetivo principal. Ninguno cambia la prioridad del roadmap ya establecida por `docs/37`/`MS-011`: los hallazgos 1 y 3 (ENUM sin formalizar, ausencia de estado "pendiente de confirmación") son vacíos de gobernanza que no bloquean la secuencia de captura ya recomendada (ninguna de las misiones `MS-013` en adelante depende de resolverlos primero, mismo criterio ya aplicado en `docs/37` sección 11: "ninguna misión de esta lista requiere resolver primero la formalización de ENUM pendientes"); el hallazgo 2 (sin campo de fuente por fila) es una limitación de trazabilidad granular, mitigable con la práctica ya vigente de `CHANGELOG.md`/`README.md` a nivel de lote, sin bloquear ninguna captura; el hallazgo 4 (cobertura de `xg`) ya estaba declarado como riesgo "Alto" en `docs/37` y se hereda sin cambio de severidad.

---

# Autocrítica (`docs/22`, sección 8)

**¿Qué supuestos hice sin poder verificarlos completamente?** Que las tres categorías de fuente (Primaria/Secundaria/Prohibida) propuestas en la sección 4 son suficientes para cubrir la variedad real de fuentes que una futura misión de captura encontrará — es una clasificación razonable basada en los precedentes ya usados (`MS-002`/`MS-006`), pero no está probada contra un caso real de discrepancia entre fuentes, que solo aparecerá cuando se ejecute `MS-013` en adelante.

**¿Qué parte de este entregable podría estar equivocada?** La regla de la sección 5 sobre fechas estimadas (generalizar el patrón de `lesiones.fecha_estimada_retorno` a "solo se admite una fecha estimada si el esquema ya distingue el campo como tal") es una interpretación razonable del principio "nunca inventar datos", pero podría ser demasiado estricta para casos legítimos donde una fecha de torneo se anuncia con antelación pero sujeta a confirmación (ej. sede de un Mundial, anunciada años antes) — esta misión no resuelve esa tensión, solo aplica la regla más conservadora disponible.

**¿Qué información me habría hecho falta para tener más certeza?** Un caso real de discrepancia entre dos fuentes primarias (ej. FIFA vs. una confederación reportando un resultado distinto) para verificar si la regla de la sección 5 ("no incorporar hasta resolver") es operativamente viable o demasiado paralizante en la práctica.

**¿Qué validaría antes de que esto se tome como definitivo?** Que la primera ejecución real de una misión de captura (`MS-013` en adelante) efectivamente pueda seguir este protocolo sin encontrar una regla de aceptación/rechazo ambigua o faltante para un caso concreto no anticipado aquí.

**¿Existe una interpretación razonable distinta a la que elegí?** Sí — sobre la sección 7 (convención de actualización), podría argumentarse que el proyecto debería adoptar versionado por fila (ej. una columna `version`/`actualizado_en` en cada CSV) en lugar de versionado solo a nivel de módulo — esta misión prefirió no proponerlo como regla obligatoria (fuera de alcance: "no modificar CSV/esquema"), documentándolo únicamente como posible mejora futura, no como parte del protocolo oficial actual.

---

# Fuera de alcance de esta misión

- No se escribió ningún código.
- No se modificó el Engine, `Runtime`, `Preparation`, `PredictionContext` ni ningún CSV.
- No se crearon scripts de descarga ni de carga.
- No se descargó ningún dato real.
- No se inventó ninguna información, incluidos valores ENUM no formalizados (hallazgo 1, sección 10 — documentado, no resuelto).
- No se modificó ningún documento existente (`docs/05`, `docs/32`, `docs/33`, los README de `data/processed/`) — solo se los referenció y recopiló.
- No se aprueba este protocolo como definitivo — queda pendiente de revisión por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5).

---

Fin del documento.
