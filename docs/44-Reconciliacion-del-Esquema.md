# Reconciliación Oficial del Esquema de Datos

**Archivo:** `docs/44-Reconciliacion-del-Esquema.md`

**Misión solicitada como:** "GOV-001 — Reconciliación oficial del esquema de datos"

**Misión registrada como:** **GOV-003** (ver nota de numeración más abajo)

**Versión:** 1.0.0

**Estado:** Reconciliación documental — sin código, sin cambios al modelo estadístico, sin modificación de `app/`/`models/`/`data/`/`knowledge/`, sin eliminar ningún campo del esquema.

---

## Nota de numeración (verificación previa, `docs/22` §3)

El brief de esta misión la identifica como "`GOV-001`". Verificado antes de escribir contra `docs/00-Project-Tracker.md`: **`GOV-001` ya está reservado desde el inicio de la serie** — es la Constitución del Modelo Santiago (`docs/21-Constitucion-del-Modelo-Santiago.md`, misión completada), y `GOV-002` también está tomado (`docs/22-Manual-Operativo-del-Arquitecto-IA.md`). El propio `docs/22` §5 lo confirma textualmente: *"esto formaliza y extiende el patrón de 'Cierre obligatorio' ya usado en `GOV-001`"*.

Conforme al Artículo 7 de la Constitución ("toda contradicción debe documentarse, nunca ocultarse") y a `docs/22` §3, y siguiendo exactamente el mismo patrón ya usado en `docs/23` (misión solicitada como "MR-002", registrada como `AR-002` por colisión con un `MR-002` ya reservado), esta misión se registra como **`GOV-003`** — siguiente identificador libre de la serie `GOV-`, sin alterar `GOV-001`/`GOV-002` ya reservados. El contenido real de la misión (reconciliar el esquema oficial con la disponibilidad real de datos) pertenece genuinamente a la serie `GOV-` (gobernanza documental), por lo que se mantiene en la misma serie, solo con el número corregido — a diferencia de `AR-002`, que sí cambió de serie porque su contenido correspondía mejor a `AR-`.

El archivo `docs/44-Reconciliacion-del-Esquema.md` no tiene conflicto de numeración: `docs/43-Pipeline-de-Ingesta.md` (`DATA-011`) es el último documento de la secuencia antes del especial `docs/99-Mapa-Maestro.md`.

---

## 1. Objetivo

Reconciliar `docs/33-Modelo-Fisico-PostgreSQL.md` (esquema oficial) con la disponibilidad real de datos confirmada en `docs/42-Verificacion-Manual-API-Football.md` (`DATA-010A`) y `docs/43-Pipeline-de-Ingesta.md` (`DATA-011`), clasificando cada campo relevante en una de cinco categorías (`OBLIGATORIO`/`CONDICIONAL`/`OPCIONAL`/`DERIVADO`/`NO DISPONIBLE`) — de modo que una futura misión de implementación tenga un contrato documental sin contradicciones internas, en lugar de la tensión no resuelta que dejó `DATA-011` entre "campo declarado obligatorio en el esquema" y "campo sin ninguna fuente confirmada".

**Esta misión no modifica el modelo estadístico ni elimina ningún campo** — reclasifica, dentro del esquema ya existente, sin tocar `docs/33` directamente (fuera del alcance autorizado: "Ajustar la documentación del esquema" se interpreta aquí como este documento nuevo, que reconcilia sin sobrescribir `docs/33`, consistente con el patrón ya usado en toda la serie `GR-`/`AR-` de complementar sin duplicar ni sobrescribir el documento fuente).

---

## 2. Metodología de clasificación

Regla explícita, aplicada de forma consistente a los 7 archivos exigidos por el brief — evita que la clasificación sea ad hoc campo por campo:

1. **`DERIVADO`**: el campo nunca se descarga de una fuente externa — se calcula. Incluye tanto los casos ya declarados "Campo excluido... se deriva" en `docs/32`/`docs/33` (ej. `campeon_id_seleccion`, `probabilidad_implicita`), como los campos que este pipeline resuelve por cálculo/inferencia interna a partir de datos ya obtenidos de otra entidad (ej. `activo_seleccion`, `estado_cuota`).
2. **`OBLIGATORIO`**: el campo tiene una fuente confirmada (con evidencia directa de `DATA-010A`/`FII-003`) **y** `docs/33` lo declara `Obligatorio: Sí`.
3. **`CONDICIONAL`**: `docs/33` lo declara `Obligatorio: Sí` (o el campo alimenta una Variable Oficial activa de Nivel A/B, `docs/16`), **pero ninguna fuente hoy aprobada lo provee**. Es el caso explícito de `xg` dado por el brief — se generaliza a todo campo con el mismo patrón: sigue siendo parte del modelo, y **volverá a ser `OBLIGATORIO`** en cuanto exista una fuente válida.
4. **`OPCIONAL`**: `docs/33` lo declara `Obligatorio: No`, **y** tiene una fuente confirmada. No es imprescindible para ejecutar el Engine (no alimenta ninguna Variable Oficial activa, `docs/16`/`docs/17`) — su ausencia no bloquea nada.
5. **`NO DISPONIBLE`**: `docs/33` lo declara `Obligatorio: No`, **y** no tiene ninguna fuente razonable con las fuentes hoy aprobadas. A diferencia de `CONDICIONAL`, no hay evidencia de que vaya a resolverse — se documenta como brecha permanente pero no bloqueante (el campo nunca fue estructuralmente necesario).

**Distinción clave entre `CONDICIONAL` y `NO DISPONIBLE`:** ambas categorías describen "sin fuente hoy", pero difieren en si el campo es estructuralmente necesario (`Obligatorio: Sí` en `docs/33`, o consumido por una Variable Oficial). Un campo `Obligatorio: No` nunca puede clasificarse `CONDICIONAL` bajo esta regla — como mucho es `NO DISPONIBLE` (sigue sin bloquear nada aunque nunca se resuelva).

**Exclusión declarada, no una categoría nueva:** la clave técnica UUID (`id`) y los metadatos de persistencia (`creado_en`/`actualizado_en`) presentes en las 10 tablas de `docs/33` §4 se excluyen de esta clasificación — son infraestructura de persistencia generada por el sistema, no "datos" cuya disponibilidad externa esta misión reconcilia. Las claves de negocio (`id_partido`, `id_torneo`, etc.) también se excluyen por la misma razón: se asignan internamente al ingerir la fila, nunca provienen de una fuente externa.

---

## 3. Clasificación por archivo

### 3.1 `partidos.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `id_torneo` | Sí | **OBLIGATORIO** | Fuente confirmada (`league.id`, `DATA-010A` §3.20) |
| `id_seleccion_local` / `id_seleccion_visitante` | Sí | **OBLIGATORIO** | Fuente confirmada (`teams.home/away.id`) |
| `id_estadio` | No | **OPCIONAL** | Fuente confirmada (`venue.id` embebido), no bloquea la ejecución |
| `id_arbitro` | No | **NO DISPONIBLE** | Sin fuente en ninguna de las dos fuentes aprobadas — ni siquiera como texto normalizable (`DATA-010A` §3.17); no alimenta ninguna Variable Oficial |
| `fecha` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `hora_local` | No | **OPCIONAL** | Fuente confirmada, no bloqueante |
| `fase` | Sí | **OBLIGATORIO** | Fuente aproximada vía `league.round` (heurística de parsing, `docs/43` §6.6) — existe fuente, aunque con riesgo de calidad documentado en `docs/43` §11 |
| `jornada` | Solo si `fase=fase_grupos` | **OPCIONAL** | Misma fuente aproximada que `fase`; su obligatoriedad ya es condicional en el propio esquema original, no a la disponibilidad de fuente |
| `goles_local` / `goles_visitante` | Solo si `estado_partido=finalizado` | **OBLIGATORIO** | Fuente confirmada; alimenta directamente el cálculo de λ de Poisson (`engine/03`) |
| `estado_partido` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `asistencia` | No | **NO DISPONIBLE** | Confirmado ausente en el objeto `fixture` completo (`DATA-010A` §3.20); no consumido por ninguna Variable Oficial (`docs/16`) |

**Resumen:** 7 Obligatorios, 0 Condicionales, 3 Opcionales, 0 Derivados, 2 No disponibles.

### 3.2 `estadisticas_partido.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `xg` | Sí | **CONDICIONAL** | Confirmado sin fuente con la evidencia más sólida de todo el proceso de verificación (`DATA-010A` §3.1) — pero alimenta directamente **Variable003 (Potencial Ofensivo)**, Nivel A (Muy Alto), `engine/01` (`docs/16` líneas 199, 258-260). Es exactamente el caso que el brief pide de ejemplo: sigue siendo parte del modelo, no tiene fuente hoy, volverá a `OBLIGATORIO` si aparece una |
| `posesion_pct` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `disparos_totales` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `disparos_al_arco` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `corners` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `faltas_cometidas` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `tarjetas_amarillas` / `tarjetas_rojas` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `pases_completados` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `precision_pases_pct` | Sí | **OBLIGATORIO** | Fuente confirmada |

**Resumen:** 9 Obligatorios, 1 Condicional (`xg`), 0 Opcionales, 0 Derivados, 0 No disponibles.

**Nota sobre `xga`:** `docs/38` §6 y `docs/32` §8 ya declaran `xga` (xG en contra) como campo **excluido**, derivado por self-join del `xg` del rival — no es una columna de `estadisticas_partido.csv` (confirmado contra el encabezado real del CSV). Se documenta aquí solo para no dejarlo fuera por omisión: es `DERIVADO` por diseño, y su cálculo depende transitivamente de que `xg` deje de ser `CONDICIONAL` — mientras `xg` no tenga fuente, `xga` tampoco puede calcularse con datos reales.

### 3.3 `jugadores.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `nombre_completo` | Sí | **OBLIGATORIO** | Fuente confirmada (`firstname`+`lastname`) |
| `nombre_conocido` | No | **OPCIONAL** | Fuente confirmada, no bloqueante |
| `fecha_nacimiento` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `posicion_principal` | Sí | **OBLIGATORIO** | Fuente confirmada, vía `/players/squads` (endpoint distinto al perfil base — `docs/43` §6.5) |
| `pie_habil` | No | **NO DISPONIBLE** | Confirmado ausente (`DATA-010A` §3.20); no consumido por ninguna Variable Oficial |
| `altura_cm` | No | **OPCIONAL** | Fuente confirmada, con parseo obligatorio de unidad (`"175 cm"` → entero) |
| `seleccion_id` | Sí | **OBLIGATORIO** | Fuente confirmada (resolución FK vía `team`) |
| `club_actual` | No | **OPCIONAL** | Fuente confirmada |
| `activo_seleccion` | Sí | **DERIVADO** | Sin campo booleano directo — se calcula por inferencia (¿aparece en `/players/squads` de una selección con temporada vigente?, `docs/43` §6.5), a partir de datos ya obtenidos de otra llamada, no por descarga directa |

**Resumen:** 5 Obligatorios, 0 Condicionales, 3 Opcionales, 1 Derivado, 1 No disponible.

### 3.4 `convocatorias.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `torneo_id` | Sí | **CONDICIONAL** | Sin fuente directa — `/players/squads` no vincula a un torneo (`DATA-010A` §3.16); sigue siendo obligatorio en el esquema y parte necesaria del concepto de convocatoria |
| `seleccion_id` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `jugador_id` | Sí | **OBLIGATORIO** | Fuente confirmada |
| `dorsal` | Sí | **OBLIGATORIO** | Fuente confirmada (`number`) |
| `posicion_convocatoria` | Sí | **OBLIGATORIO** | Fuente confirmada (`position`) |
| `fecha_convocatoria` | Sí | **CONDICIONAL** | Confirmado ausente (`DATA-010A` §3.16); sigue siendo obligatoria en el esquema |
| `estado_convocatoria` | Sí | **CONDICIONAL** | Confirmado ausente; sigue siendo obligatoria en el esquema |

**Resumen:** 4 Obligatorios, 3 Condicionales, 0 Opcionales, 0 Derivados, 0 No disponibles.

### 3.5 `arbitros.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `nombre_completo`, `nacionalidad`, `confederacion_arbitral`, `categoria`, `activo` (los 5 campos de dato) | Sí (todos) | **CONDICIONAL** (los 5) | Sin fuente en API-Football/Football-Data.co.uk (`DATA-010A` §3.17: sin endpoint `/referees`). **No se clasifican `NO DISPONIBLE`** porque `docs/38` §4 ya identificó una Fuente Primaria conceptualmente válida y no evaluada todavía por esta línea de investigación: *"Listas oficiales FIFA/confederación ('FIFA International Referees List')"* — existe una vía razonable, solo no forma parte de las dos fuentes que `FII-003`/`DATA-010A` evaluaron técnicamente |

**Resumen:** 0 Obligatorios, 5 Condicionales, 0 Opcionales, 0 Derivados, 0 No disponibles.

### 3.6 `estadios.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `nombre`, `ciudad`, `pais`, `capacidad`, `tipo_superficie` | Sí (todos) | **OBLIGATORIO** (los 5) | Fuente confirmada (`DATA-010A` §3.18) |
| `altitud_metros` | Sí | **CONDICIONAL** | Confirmado ausente (`DATA-010A` §3.18); sigue siendo obligatorio en el esquema — un factor de juego real (altitud) con posible relevancia futura para el modelo, aunque hoy ninguna Variable Oficial lo consuma explícitamente (`docs/16` no lo cita) |
| `techado` | Sí | **CONDICIONAL** | Confirmado ausente; sigue siendo obligatorio en el esquema |

**Resumen:** 5 Obligatorios, 2 Condicionales, 0 Opcionales, 0 Derivados, 0 No disponibles.

### 3.7 `cuotas.csv`

| Campo | `docs/33` | Clasificación | Justificación |
|---|---|---|---|
| `partido_id` | Sí | **CONDICIONAL** | Ver nota de archivo completo, abajo |
| `casa_apuestas` | Sí | **CONDICIONAL** | Ídem |
| `mercado` | Sí | **CONDICIONAL** | Ídem |
| `seleccion_o_resultado` | Sí | **CONDICIONAL** | Ídem |
| `cuota_decimal` | Sí | **CONDICIONAL** | Ídem |
| `fecha_captura` | Sí | **CONDICIONAL** | Ídem |
| `estado_cuota` | Sí | **DERIVADO** | No es un campo que ninguna fuente provea directamente — se calcula por lógica del pipeline (ej. "vigente" mientras `fecha_captura` esté dentro de la ventana pre-partido, "cerrada" al iniciar el partido) |

**Resumen:** 0 Obligatorios, 6 Condicionales, 0 Opcionales, 1 Derivado, 0 No disponibles.

**Nota de archivo completo — matiz distinto al de `xg`:** a diferencia de `xg` (campo inexistente en la fuente), los campos de `cuotas.csv` **sí existen** en API-Football (`GET /odds`) — lo que falta no es el campo sino (a) la profundidad histórica real (`DATA-010A` §3.19: solo 7 días de historial, inútil para EV histórico) y (b) la cobertura de selecciones nacionales específicamente en ese endpoint, que **ninguna misión anterior verificó explícitamente** (`FII-003`/`DATA-010A` se enfocaron en `/fixtures`, `/fixtures/statistics`, `/venues`, `/players` — no en `/odds` para selecciones en particular). Football-Data.co.uk, la otra fuente aprobada, **no cubre selecciones nacionales bajo ningún concepto** (`FII-003` §4.3) — no es una fuente aplicable a este archivo en absoluto para el dominio actual del proyecto. Todos los campos quedan `CONDICIONAL` porque existe al menos una vía técnica (API-Football `/odds`) que podría resolverse con una fuente de mayor profundidad histórica, aunque hoy no sea utilizable para el propósito real del archivo.

---

## 4. Preguntas específicas del brief

### 4.1 xG: ¿debe desaparecer o debe permanecer como condicional?

**Debe permanecer como `CONDICIONAL`.** Tres razones, ninguna de ellas de conveniencia:

1. **No es competencia de esta misión eliminarlo.** El brief de esta misma misión prohíbe explícitamente "Eliminar campos del modelo" — solo el Arquitecto Estadístico Humano puede aprobar un cambio de esa naturaleza (Constitución, Art. 2/5), y eliminar `xg` del esquema es exactamente ese tipo de cambio (afecta la entrada de Variable003).
2. **Alimenta una Variable Oficial de Nivel A ya activa** (`docs/16`, `engine/01`, sección 3.2) — no es un campo decorativo sin consumidor, es una entrada matemática real del modelo.
3. **La ausencia de fuente hoy no implica ausencia de fuente para siempre** — exactamente el criterio que define `CONDICIONAL`: StatsBomb (fuente ya en uso, `FII-002`) sí provee `xg` donde tiene cobertura; la brecha es de las dos fuentes nuevas evaluadas (API-Football/Football-Data.co.uk), no del modelo ni del dominio.

### 4.2 Convocatorias: ¿debe mantenerse el diseño actual o debe documentarse como pendiente?

**Debe documentarse como pendiente, sin cambiar el diseño.** El diseño de `convocatorias.csv` (entidad asociativa N:M Equipo×Jugador×Torneo, `docs/32` §4.3) se mantiene exactamente igual — esta misión no tiene autorización para modificar el esquema. Lo que cambia es la clasificación de 3 de sus 7 campos (`torneo_id`, `fecha_convocatoria`, `estado_convocatoria`) de "obligatorio sin matiz" a `CONDICIONAL`: siguen siendo necesarios, no tienen fuente hoy, y la regla ya vigente de `docs/38` §5 ("campo obligatorio ausente → fila rechazada") sigue aplicando sin excepción — en la práctica, ninguna fila de `convocatorias.csv` puede aceptarse todavía, exactamente como ya encontró `DATA-011`, solo que ahora esa realidad tiene una categoría formal en lugar de quedar como un hallazgo aislado.

### 4.3 Árbitros: misma pregunta

**Debe documentarse como pendiente, sin cambiar el diseño.** `arbitros.csv` mantiene su diseño (`docs/32` §7: entidad independiente) sin modificación. Sus 5 campos de dato pasan a `CONDICIONAL` — con el matiz adicional de que `docs/38` ya identificó una Fuente Primaria razonable (listas oficiales FIFA/confederación) nunca evaluada técnicamente por `FII-003`/`DATA-010A`, lo que hace más concreto el camino hacia `OBLIGATORIO` que en otros campos `CONDICIONAL` de este documento.

### 4.4 Cuotas: ¿debe seguir existiendo el CSV? ¿Con qué fuente?

**Sí, debe seguir existiendo** — `Engine06` (Valor Esperado) ya existe en código desde `BUILD-015` y el Bloque D de la Fase II (`docs/39`) depende estructuralmente de este archivo; eliminarlo sería un cambio de arquitectura fuera del alcance de esta misión.

**Con qué fuente:** **ninguna de las dos fuentes hoy aprobadas resuelve el caso de uso real** (EV histórico para selecciones nacionales) — ver sección 3.7. Football-Data.co.uk queda descartado por completo para este archivo (no cubre selecciones). API-Football sigue siendo la única vía técnica con alguna aplicabilidad, pero limitada a cuotas de corto plazo (7 días), no a backtesting histórico. Se recomienda que una futura misión de investigación (no esta, que no tiene autorización para evaluar fuentes nuevas) evalúe explícitamente un proveedor especializado en cuotas históricas de selecciones nacionales — brecha que ni `FII-002` ni `FII-003` cerraron porque ninguna de las 13 fuentes investigadas combina selecciones + cuotas históricas.

---

## 5. Cierre obligatorio (preguntas del brief)

**1. ¿El esquema quedó completamente reconciliado?** Sí, en el sentido de que los 7 archivos exigidos tienen cada campo clasificado sin ambigüedad en una de las 5 categorías, con justificación trazable a `FII-003`/`DATA-010A`/`docs/16`. No en el sentido de que la reconciliación resuelva las brechas — las documenta y las categoriza, que es exactamente el alcance autorizado de esta misión (no le corresponde cerrarlas).

**2. ¿Qué campos pasan a ser condicionales?** `estadisticas_partido.xg` (el caso ejemplo del brief); `convocatorias.torneo_id`/`fecha_convocatoria`/`estado_convocatoria` (3); `arbitros.*` (los 5 campos de dato); `estadios.altitud_metros`/`techado` (2); `cuotas.*` (6 de 7, excluyendo `estado_cuota` que es `DERIVADO`). Total: **18 campos** pasan de "obligatorio sin matiz" a `CONDICIONAL`.

**3. ¿Qué campos siguen siendo obligatorios?** 30 campos en total (ver resúmenes por archivo, sección 3): 7 en `partidos.csv`, 9 en `estadisticas_partido.csv`, 5 en `jugadores.csv`, 4 en `convocatorias.csv`, 0 en `arbitros.csv`, 5 en `estadios.csv`, 0 en `cuotas.csv`.

**4. ¿Qué campos quedan pendientes de futuras fuentes?** Exactamente los 18 campos `CONDICIONAL` de la pregunta 2 — con la distinción hecha en la sección 3.5/3.7 de que `arbitros.csv` y `cuotas.csv` ya tienen, respectivamente, una fuente primaria candidata identificada (`docs/38`) y una vía técnica parcial (API-Football `/odds`), mientras que `xg` y los campos de `convocatorias.csv`/`estadios.csv` no tienen ninguna vía identificada más allá de "una fuente distinta a las dos ya evaluadas".

**5. ¿Qué contradicciones fueron eliminadas?** La principal: `docs/33` declaraba `xg`, los 3 campos débiles de `convocatorias.csv`, `altitud_metros`/`techado` y toda `arbitros.csv`/`cuotas.csv` como `Obligatorio: Sí` sin matiz, mientras que `DATA-011` ya había confirmado que ninguno tenía fuente — una contradicción literal entre "el esquema exige este dato siempre" y "ninguna fuente aprobada lo entrega nunca". La categoría `CONDICIONAL` resuelve esa contradicción sin tocar `docs/33` ni relajar la regla de rechazo de `docs/38` §5: el campo sigue siendo necesario, simplemente su indisponibilidad ahora tiene un nombre formal en lugar de leerse como un error de diseño.

**6. ¿Queda alguna contradicción conocida?** Sí, una, explícita y sin resolver por esta misión (fuera de su alcance): mientras `xg` (y los demás campos `CONDICIONAL` obligatorios en `docs/33`) no tengan fuente, la regla de rechazo de `docs/38` §5 sigue impidiendo, en la práctica, que se acepte cualquier fila de `estadisticas_partido.csv`/`convocatorias.csv` proveniente de API-Football — la reclasificación no cambia ese comportamiento operativo, solo lo documenta con precisión. Resolver esta tensión (¿el esquema debe admitir `CONDICIONAL` como un valor NULL válido a nivel de `CHECK` físico, o la regla de rechazo debe hacer una excepción explícita para campos `CONDICIONAL`?) es una decisión de gobernanza que **no le corresponde a esta misión**, ver pregunta 8.

**7. ¿Puede comenzar `DATA-012`?** Depende de qué se entienda por `DATA-012`. Si es la implementación completa del pipeline (incluyendo `estadisticas_partido.csv`/`convocatorias.csv` desde API-Football), **no todavía** — la contradicción de la pregunta 6 sigue bloqueando esas dos entidades operativamente. Si `DATA-012` se acota a las entidades sin campos `CONDICIONAL` obligatorios bloqueantes en la práctica (`partidos.csv`, `jugadores.csv`, `selecciones.csv`, la mayoría de `estadios.csv`), **sí puede comenzar** — mismo criterio de capas ya establecido en `docs/43` §3.

**8. ¿Existe alguna decisión pendiente del Arquitecto Estadístico Humano?** Sí, dos, ninguna resuelta ni pretendida resolver por esta misión: (a) si la regla de rechazo de `docs/38` §5 debe hacer una excepción explícita para campos `CONDICIONAL` (permitir la fila con ese campo en `NULL` en lugar de rechazarla completa) — sin esa decisión, `estadisticas_partido.csv`/`convocatorias.csv` permanecen sin poder poblarse desde API-Football pese a tener el resto de sus campos disponibles; (b) si vale la pena iniciar una investigación de fuente adicional específicamente para `cuotas.csv` de selecciones nacionales (sección 4.4), dado que ninguna de las 13 fuentes ya investigadas por `FII-002` resuelve ese caso de uso.

**9. ¿Qué riesgo queda antes de implementar?** El mismo de la pregunta 6/8: si una futura misión de implementación no espera la decisión del Arquitecto Estadístico Humano sobre la excepción de rechazo, construirá un pipeline que sistemáticamente descarta el 100% de las filas de `estadisticas_partido.csv`/`convocatorias.csv` provenientes de API-Football, sin que ese comportamiento sea un error de código — sería el comportamiento correcto según la regla ya vigente, pero probablemente no el que se pretendía al diseñar el pipeline en `DATA-011`.

**10. Confirmar que no hubo cambios en `app/`, `models/`, `data/` ni `knowledge/`.** **Confirmado.** Esta misión solo creó `docs/44-Reconciliacion-del-Esquema.md` y actualizó `CHANGELOG.md`/`docs/00-Project-Tracker.md` — verificable con `git status`. `docs/33` no fue modificado (se referenció, no se sobrescribió). No se eliminó ningún campo del esquema.

---

## 6. Lista de verificación de cierre (`docs/22` §5 — set estándar de 6 preguntas, obligatorio para toda misión `GOV-`)

**1. ¿Qué problema resolvió?** La contradicción literal entre `docs/33` (exige ciertos campos siempre) y la evidencia ya reunida por `DATA-010A`/`DATA-011` (ninguna fuente aprobada los provee) — sin esta reconciliación, cualquier implementación futura tropezaría con esa contradicción en tiempo de ejecución en lugar de encontrarla ya documentada y categorizada.

**2. ¿Qué problemas nuevos descubrió?** Uno: `cuotas.csv` tiene una brecha de evidencia propia que ninguna misión anterior cerró — la cobertura de `/odds` para selecciones nacionales específicamente nunca se verificó (`FII-003`/`DATA-010A` se enfocaron en otros endpoints), distinta de la ya confirmada limitación de 7 días de historial. No es un hallazgo que cambie ninguna recomendación ya hecha, pero cierra una imprecisión que quedaba implícita en `DATA-011`.

**3. ¿Qué documentos podrían necesitar actualización futura?** `docs/33-Modelo-Fisico-PostgreSQL.md` podría, en una futura misión de gobernanza dedicada (no esta, sin autorización para modificarlo), incorporar formalmente la columna "Clasificación" (`OBLIGATORIO`/`CONDICIONAL`/`OPCIONAL`/`DERIVADO`/`NO DISPONIBLE`) junto a su columna `Obligatorio` ya existente, en lugar de mantener la reconciliación en un documento separado.

**4. ¿Qué impacto tiene sobre el proyecto?** Desbloquea conceptualmente la discusión de `DATA-012` (pregunta 5.7) al separar con precisión qué partes del pipeline ya diseñado en `DATA-011` pueden implementarse hoy sin contradicción, y cuáles requieren una decisión de gobernanza previa.

**5. ¿Cómo cambia el riesgo arquitectónico?** Reduce el riesgo de que una implementación futura descubra la contradicción `xg`/`docs/38` §5 en producción, en lugar de encontrarla ya documentada con una recomendación explícita de qué decisión falta antes de proceder (sección 5, preguntas 8-9).

**6. ¿Qué impacto cualitativo tiene sobre el Índice de Madurez Arquitectónica (IMA)?** Sin IMA formal todavía (mismo estado heredado de `GOV-001`/`GOV-002`). Cualitativamente, esta misión agrega madurez en la dimensión de **coherencia entre el contrato documental y la evidencia empírica** — antes de esta misión, el esquema y la evidencia de disponibilidad vivían en documentos separados sin una reconciliación explícita entre ambos.

---

## 7. Gestión de hallazgos (`docs/22` §7)

El hallazgo de la sección 6, pregunta 2 (brecha de cobertura de `/odds` para selecciones nacionales, nunca verificada) se documenta con el mismo rigor que el objetivo principal. **No cambia la prioridad del roadmap vigente**: no bloquea `DATA-012` en las entidades que sí pueden implementarse (sección 5, pregunta 7), y la recomendación de investigarlo queda como una misión de investigación futura opcional, no urgente — el propio Bloque D de la Fase II (`docs/39`) ya depende de decisiones previas (Bloques A-C) antes de necesitar `cuotas.csv` resuelto.

---

## 8. Autocrítica (`docs/22` §8)

**¿Qué supuestos hice sin poder verificarlos completamente?** Que ningún campo `Obligatorio: No` de los 7 archivos evaluados es consumido por una Variable Oficial activa, más allá de los casos que sí pude confirmar explícitamente (`xg` vía `docs/16`). Para los demás campos (`asistencia`, `pie_habil`, `altitud_metros`, etc.) inferí ausencia de consumo por no encontrarlos citados en `docs/16`/`docs/17`/las "Observaciones del Arquitecto" de ese contrato — es una inferencia por ausencia de evidencia, no una confirmación positiva de que nunca se usarán.

**¿Qué parte de este entregable podría estar equivocada?** La clasificación de `activo_seleccion` y `estado_cuota` como `DERIVADO` en lugar de `CONDICIONAL` — es una interpretación razonable (se calculan a partir de datos ya obtenidos, no requieren una fuente nueva), pero alguien podría argumentar que son, en realidad, campos sin fuente directa que deberían tratarse igual que los demás `CONDICIONAL` hasta que su lógica de cálculo se implemente y valide.

**¿Qué información me habría hecho falta para tener más certeza?** Confirmación directa de si `/odds` de API-Football cubre selecciones nacionales en algún grado (brecha nueva identificada en la sección 6, pregunta 2) — sin ella, la nota de la sección 3.7 sobre `cuotas.csv` es la parte de este documento con menos evidencia directa, más cercana a una inferencia razonada que a un hecho verificado.

**¿Qué validaría antes de que esto se tome como definitivo?** Que la decisión pendiente del Arquitecto Estadístico Humano (sección 5, pregunta 8) efectivamente se tome antes de que una misión de implementación intente poblar `estadisticas_partido.csv`/`convocatorias.csv` — de lo contrario, esta reconciliación documental no tiene ningún efecto operativo real sobre el comportamiento ya vigente de `docs/38` §5.

**¿Existe una interpretación razonable distinta a la que elegí?** Sí — sobre `arbitros.csv`: podría argumentarse que, al no tener ningún campo `OBLIGATORIO` confirmado hoy (los 5 son `CONDICIONAL`), la entidad completa debería tratarse como fuera del alcance de cualquier implementación cercana, en lugar de mantenerse en el grafo de dependencias de `docs/43` en la misma posición que las demás entidades de Capa 0 — esta misión prefirió mantener su posición estructural en el grafo (el diseño no cambia, solo la clasificación de sus campos), consistente con la pregunta 4.3, pero es una decisión de énfasis, no la única razonable.

---

## 9. Fuera de alcance de esta misión

- No se modificó `docs/33-Modelo-Fisico-PostgreSQL.md` ni ningún otro documento existente.
- No se modificó el Engine, `Runtime`, `Preparation`, `PredictionContext`, ninguna Variable Oficial, fórmula ni peso.
- No se eliminó ningún campo del esquema.
- No se creó código, CSV ni se consumió ninguna API.
- No se resolvió la contradicción de la sección 5 (pregunta 6) — se documentó explícitamente como pendiente de decisión del Arquitecto Estadístico Humano.
- No se evaluó ninguna fuente de datos nueva (ej. para `cuotas.csv` de selecciones o `arbitros.csv`) — solo se documentó la necesidad de esa evaluación futura.

---

## 10. Referencias

- `docs/33-Modelo-Fisico-PostgreSQL.md` (`DATA-005`) — esquema oficial reconciliado, no modificado
- `docs/41-Verificacion-Tecnica-de-Fuentes.md` (`FII-003`), `docs/42-Verificacion-Manual-API-Football.md` (`DATA-010A`) — evidencia de disponibilidad reutilizada sin reinvestigar
- `docs/43-Pipeline-de-Ingesta.md` (`DATA-011`) — diseño del pipeline y hallazgo original de la contradicción que esta misión reclasifica
- `docs/38-Protocolo-Oficial-Ingesta-Datos.md` (`MS-012`) — regla de rechazo (§5) cuya tensión con `docs/33` motiva esta reconciliación
- `docs/16-Contrato-Oficial-de-Variables.md` — confirmación de que `xg` alimenta Variable003 (Nivel A, `engine/01`)
- `docs/21-Constitucion-del-Modelo-Santiago.md` (`GOV-001`), `docs/22-Manual-Operativo-del-Arquitecto-IA.md` (`GOV-002`) — misiones ya reservadas que motivaron la renumeración de esta misión a `GOV-003`

---

Fin del documento.
