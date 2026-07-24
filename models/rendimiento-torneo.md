# Rendimiento en el Torneo — Variable002

**Archivo:** `models/rendimiento-torneo.md`

**Misión:** MODEL-012 — Especificación Oficial de Variable002 para V1

**Versión:** 1.0.0-investigación

**Estado:** Investigación — primer documento de `models/` dedicado a Variable002 (no evoluciona un stub, se crea desde cero, mismo patrón que `MODEL-005`/`models/chaos-index.md` y `MODEL-011`/`models/forma-reciente.md`)

---

## Nota de nomenclatura y de alcance (léase antes de continuar)

El brief de `MODEL-012` llama a esta variable **"Rendimiento Táctico"**. Verificado contra `docs/03-Variables.md`, `docs/16-Contrato-Oficial-de-Variables.md` y `docs/17-Matriz-de-Consumo-de-Variables.md`: el nombre oficial de Variable002 es, de forma consistente en los tres documentos, **"Rendimiento en el Torneo"** — ningún documento del proyecto usa "Rendimiento Táctico". Esta corrección es más importante que las de `MODEL-009` (que solo corregía una etiqueta informal): "Rendimiento Táctico" se acerca peligrosamente al nombre de una variable **distinta y ya diferida**, **Variable005 — Compatibilidad Táctica** ("Formación, Estilo de presión, Posesión, Juego directo, Contraataque", `docs/03`, **diferida formalmente por `MR-004`**, sin fuente de datos y sin motor asignado). Se deja explícito, antes de continuar: **esta misión especifica Variable002 (Rendimiento en el Torneo), no Variable005.** No se reintroduce, se menciona ni se toca ningún dato táctico (formación, presión, posesión) en ningún punto de este documento — habría revertido, sin autorización, la decisión ya vigente de `MR-004`.

**Alcance del documento:** el brief pide "actualizar únicamente el documento oficial donde reside la definición matemática de Variable002" y "no crear documentos paralelos". Verificado antes de escribir (mismo método que `MODEL-011`): **ningún documento de `models/` define hoy la construcción de Variable002** — `docs/28-Catalogo-de-Variables-Derivadas.md` ya lo confirma ("Rendimiento en el Torneo (Var002) | `docs/03`, `docs/16` | ... | Pendiente"), y `models/offensive-strength.md`/`defensive-strength.md` solo la consumen como modificador ya construido (`t = (Variable002−50)/50`, dentro de `M_forma`), sin definir nunca cómo se construye. No existe, por tanto, ningún documento que "actualizar" — crear `models/rendimiento-torneo.md` es completar el documento oficial que falta, no crear un documento paralelo a uno ya existente (mismo razonamiento y mismo precedente que `MODEL-011` aplicó para Variable001).

---

# 1. Objetivo

Desarrollar el fundamento matemático de Variable002 (Rendimiento en el Torneo) — la base científica que permitirá a `VariablePreparation` calcularla con dato real — sin implementar código, sin modificar el Runtime, `PredictionContext`, `Engine01`, Variables Oficiales ni Persistence.

---

# 2. Definición operacional exacta

**Variable002 (Rendimiento en el Torneo)** representa el desempeño de una selección **exclusivamente dentro de la edición del torneo que se está prediciendo** (`id_torneo` específico, no la competición en general) — cuántos puntos ha sumado y qué balance de goles ha producido en los partidos que ya disputó de ese torneo. Responde la pregunta que `docs/03-Variables.md` ya fija: "¿está mejorando este equipo a medida que avanza el torneo actual?", de forma independiente de su forma en partidos de otras competiciones (Variable001).

**Distinción exacta con Variable001 (`models/forma-reciente.md`, `MODEL-011`):** Variable001 usa los últimos `N=5` partidos oficiales de **cualquier** competición; Variable002 usa **todos** los partidos ya jugados por el equipo, pero únicamente dentro del `id_torneo` específico del partido que se está prediciendo — sin ventana `N` fija (sección 8). Ambas son Nivel A y comparten el mismo consumidor (`M_forma`, `engine/01`/`engine/02`), pero miden períodos y alcances distintos, tal como ya lo distingue `docs/03` ("Un equipo puede llegar con mala forma reciente pero mejorar considerablemente durante el torneo").

---

# 3. Problema que Resuelve

`M_forma` (`models/offensive-strength.md` §6.2, `models/defensive-strength.md` §6.1) ya combina Variable001 y Variable002 como sus dos modificadores de forma — pero, hasta este documento, solo Variable001 tenía una fórmula propia (`MODEL-011`). Sin esta especificación, `M_forma` no puede calcularse completamente con dato real aunque Variable001/003/004 ya lo tengan.

---

# 4. Fundamento y decisiones de diseño

**Por qué se combinan puntos y goles, y no solo puntos (a diferencia de Variable001):** `docs/03-Variables.md` distingue explícitamente los "Datos necesarios" de ambas variables. Variable001: "Resultado" únicamente (`MODEL-011` §4, explícitamente sin goles). Variable002: "Victorias, Empates, Derrotas, **Goles**, Rendimiento ofensivo, Rendimiento defensivo" — "Goles" sí está autorizado aquí, a diferencia de Variable001. Esta especificación usa, por tanto, tanto el resultado (puntos) como el balance de goles — no por preferencia propia, sino porque `docs/03` autoriza explícitamente ese dato para esta variable y no para la otra.

**Qué son "Rendimiento ofensivo" y "Rendimiento defensivo" en este contexto (no Variable003/004):** `docs/03` no lista `xG`, disparos ni ninguna estadística de tiro entre los "Datos necesarios" de Variable002 — solo "Goles". Interpretar "Rendimiento ofensivo"/"Rendimiento defensivo" como referencias a Variable003/Variable004 introduciría una dependencia de datos (`estadisticas_partido.csv`) que `docs/03` nunca autoriza para Variable002, y crearía además una ventana de comparación distinta (Variable003/004 usan los últimos `N=10` partidos de cualquier torneo de la competición, `MODEL-009`/`MODEL-010`; Variable002 usa solo el torneo actual) — mezclarlas sería inconsistente. La lectura textualmente más simple y menos inventiva es que ambos términos describen los dos componentes de "Goles": goles anotados (rendimiento ofensivo) y goles recibidos (rendimiento defensivo) **dentro del torneo**, ya derivables directamente de `partidos.csv` sin ninguna fuente adicional.

**Por qué la fórmula no introduce ningún peso libre (a diferencia de Variable003/004, igual que Variable001):** combinar "puntos" (ya acotado 0-100 por construcción, igual que `MODEL-011` §6) con "goles" exige una segunda cantidad también acotada de forma natural, para evitar introducir un coeficiente de escala sin evidencia (`CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística"). Se usa la **proporción de goles a favor sobre el total de goles del partido/torneo** (`goles_a_favor / (goles_a_favor + goles_en_contra)`) — un cociente que, igual que la proporción de puntos, ya cae en `[0,1]` por construcción, sin necesitar ningún parámetro de escala. Promediar dos cantidades ya acotadas con peso igual (sección 6) seguirá el mismo criterio neutral ya usado en todo el proyecto cuando "ninguna evidencia favorece un término sobre otro" (`MODEL-009`/`010`/`011`) — sin ser, por eso, un peso pendiente de calibración: no hay ningún símbolo nuevo que catalogar en `models/parameter-calibration.md` (mismo caso que Variable001).

---

# 5. Fuente de datos

| Dato (`docs/03`) | Archivo | Columna / cálculo | Disponibilidad (`docs/27`) |
|---|---|---|---|
| Partidos del torneo | `data/processed/selecciones-nacionales/partidos.csv` | Filtrado por `id_torneo` **exacto** del partido que se está prediciendo (`context.match`, no toda la competición) | Columnas existen; **0 filas** (verificado antes de escribir, mismo estado que `MODEL-009`/`010`/`011`) |
| Victorias / Empates / Derrotas | `partidos.csv` | Comparación `goles_local` vs. `goles_visitante`, según el lado del equipo — misma lógica que Variable001 (`MODEL-011` §5), aplicada solo a partidos del torneo | Categoría C — derivable |
| Goles (a favor / en contra) | `partidos.csv` | Los propios `goles_local`/`goles_visitante` de cada partido del torneo, según el lado del equipo | Categoría A/C |
| Rendimiento ofensivo / defensivo | Derivado de "Goles" (sección 4) | Suma de goles a favor / en contra sobre los partidos ya jugados del torneo | Deriva de lo anterior |

**No se usa `estadisticas_partido.csv`** — ninguna de las cinco entradas de `docs/03` para Variable002 requiere `xG`/disparos (sección 4). No se usa ninguna fuente externa, mismo principio ya fijado en `MODEL-009` §20.

---

# 6. Fórmula oficial V1

Sea `T` el `id_torneo` exacto del partido que se está prediciendo, y sean los `n` partidos que el equipo ya disputó dentro de `T` (sección 8 — sin ventana `N` fija, a diferencia de Variable001/003/004):

```
Puntos_torneo   = Σⱼ puntos_j                      (puntos_j ∈ {0,1,3}, sistema estándar, igual que Variable001)
Goles_favor     = Σⱼ goles_a_favor_j
Goles_contra    = Σⱼ goles_en_contra_j

Puntos_pct = 100 · Puntos_torneo / (3 · n)                              (definido si n ≥ 1)

Gol_pct    = 100 · Goles_favor / (Goles_favor + Goles_contra)           (definido si Goles_favor + Goles_contra ≥ 1)

Rendimiento_Torneo = (Puntos_pct + Gol_pct) / 2       si ambos están definidos
Rendimiento_Torneo = Puntos_pct                        si solo Puntos_pct está definido (sin goles en ningún sentido, ej. único partido 0-0)
```

**Ningún peso ni coeficiente libre** — igual que Variable001 (`MODEL-011` §6): ambos sub-índices ya están acotados `[0,100]` por construcción aritmética; el promedio simple es la combinación neutral ya justificada en la sección 4, no una calibración pendiente.

---

# 7. Variables internas

Dos métricas crudas, ambas ya presentes en `partidos.csv`: el resultado de cada partido del torneo (para `Puntos_torneo`) y los goles de cada partido del torneo (para `Goles_favor`/`Goles_contra`). Ninguna estadística de tiro, ninguna dato táctico (sección "Nota de nomenclatura").

---

# 8. Ventana temporal

**Sin `N` fijo — a diferencia deliberada de Variable001 (`N=5`) y Variable003/004 (`N=10`).** La ventana de Variable002 es, por definición (`docs/03`: "Analiza únicamente los partidos disputados en la competición que se está prediciendo"), **todos** los partidos que el equipo ya jugó dentro del `id_torneo` específico del partido a predecir — ni más (no se extiende a otras ediciones de la misma competición, ni a otras competiciones), ni menos (no se trunca a los últimos `N`, porque el propio torneo ya acota naturalmente el conjunto). Esta ventana crece partido a partido a medida que avanza el torneo, empezando en `n=0` (debut absoluto en esa edición) — comportamiento ya anticipado por `docs/03`, "Frecuencia de actualización: Después de cada jornada".

**Sin ponderación interna** — mismo criterio que Variable001 (`MODEL-011` §8): todos los partidos ya jugados del torneo pesan igual, sin favorecer los más recientes dentro de la propia ventana.

**Tratamiento de competiciones:** el `id_torneo` de "Amistosos Internacionales" (`TOR-2026-AMISTOSOS`, `torneos.csv`) agrupa, por diseño ya fijado desde `MS-006`, todos los amistosos bilaterales de un año calendario en una única edición — Variable002 hereda esa agrupación tal cual, sin introducir una excepción nueva: para un partido amistoso, "el torneo actual" es ese mismo bloque anual ya existente en el esquema, no una construcción de esta misión.

---

# 9. Normalización

Rango de salida: **0 a 100**, acotado por construcción aritmética directa (ambos sub-índices ya caen en `[0,100]`/`[0,1]·100` antes de promediar) — consistente con `docs/16` (Variable002: "Índice (0-100)"). Sin `Φ`, sin `clip` adicional necesario — mismo caso que Variable001 (`MODEL-011` §9).

---

# 10. Casos límite

| Caso | Comportamiento |
|---|---|
| **Debut absoluto en el torneo (`n = 0`)** | **Excepción ya documentada, no nueva de esta misión** (`docs/17-Matriz-de-Consumo-de-Variables.md`, sección 6 y tabla final: "Variable002 puede llegar nula si el equipo debuta en el torneo actual, sin que eso detenga el pipeline (continúa con confianza reducida)"). Variable002 se marca `disponible = False`, pero **a diferencia de Variable001/003/004, esto NO detiene el pipeline** — el cálculo continúa con confianza reducida, exactamente como ya lo fija `docs/17` |
| **Pocos partidos jugados del torneo (`n` bajo pero `> 0`)** | Se usa el subconjunto disponible; `muestra_reducida = True` se propaga en `ValorVariable` — mismo mecanismo que Variable001/003/004. No hay un "mínimo" distinto de `n ≥ 1`, porque la ventana ya es, por definición, todo lo disputado hasta ahora |
| **Estadísticas faltantes** (fila de `partidos.csv` con goles corruptos o no numéricos en un partido puntual del torneo) | Esa fila se descarta individualmente — no invalida el resto de los partidos ya jugados del torneo, mismo tratamiento que `MODEL-009`/`010`/`011` |
| **Métrica inexistente — `Gol_pct` indefinido** (`Goles_favor + Goles_contra = 0`, ej. único partido 0-0 disputado) | `Rendimiento_Torneo` se calcula solo con `Puntos_pct` (sección 6) — no se inventa un valor para `Gol_pct`, ni se sustituye por 50 ni por cualquier otro número |
| **Ambos sub-índices indefinidos** (`n = 0`) | Coincide exactamente con la fila "Debut absoluto" — `disponible = False`, pipeline continúa (excepción de `docs/17`) |

---

# 11. Complejidad computacional

**Puede precalcularse — misma familia de complejidad que Variable001 (`MODEL-011` §12), más simple que Variable003/004.** No requiere ninguna agregación a nivel de competición ni de rivales: es una función directa de los propios partidos del equipo dentro de un único `id_torneo`, `O(n)` donde `n` es, en la práctica, pequeño (un torneo real rara vez supera unas pocas decenas de partidos por selección, y para la mayoría de las competiciones del catálogo, muchos menos). Sin `Φ`, sin `self-join` sobre el rival (a diferencia de Variable004).

---

# 12. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable002 podría pasar de "Método: Pendiente" a "definido, ver `models/rendimiento-torneo.md`" — actualización editorial futura de `docs/`, fuera de alcance de esta misión de `models/` |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Sin cambios — ya asigna Variable002 directa a `engine/01`/`engine/02`, indirecta a `03-06`, y ya documenta la excepción de debut (sección 10) que esta especificación aplica sin modificarla |
| `docs/28-Catalogo-de-Variables-Derivadas.md` | Podría, en una futura misión (no esta), pasar "Rendimiento en el Torneo (Var002)" de "Pendiente" a "Diseñada" |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Sin cambios — `rendimiento_torneo` en `VariablesBlock` ya está tipado `float \| None`, compatible sin bloqueo de esquema |
| `app/preparation/preparation.py` (`VariablePreparation`) | Consumidor directo en una futura `BUILD-021`, mismo patrón ya validado por `BUILD-018`/`BUILD-019` |
| `models/offensive-strength.md` / `models/defensive-strength.md` | Sin cambios a sus fórmulas — `M_forma` (que ya consume Variable002 como `t = (Variable002−50)/50`) podría recibir, junto con Variable001, sus dos modificadores de forma completamente reales por primera vez |
| `models/forma-reciente.md` | Sin cambios — se cita como precedente editorial y de convención (sistema de puntos 3-1-0), no como dependencia de datos |

---

# 13. Impacto

Una vez que esta especificación sea revisada y aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5 — nunca autoaprobada por el Arquitecto Estadístico IA):

- **`VariablePreparation` podría implementar el cálculo real de Variable002** en una futura `BUILD-021`, siguiendo exactamente la fórmula de la sección 6 y los casos límite de la sección 10 — mismo patrón ya validado por `BUILD-018`/`BUILD-019`.
- **`M_forma` (dentro de `Engine01`/`Engine02`) quedaría completo con sus dos modificadores de forma reales** (Variable001 desde `MODEL-011`, Variable002 desde esta misión) — condicionado, igual que siempre, a que existan filas reales en `partidos.csv` (hoy sin filas, verificado antes de escribir). Mismo matiz honesto que todas las misiones `MODEL-` anteriores: el impacto inmediato es metodológico, no de datos.
- **Ninguna de las cuatro variables principales de desempeño de equipo queda ya sin especificación matemática** (Forma Reciente, Rendimiento en el Torneo, Potencial Ofensivo, Solidez Defensiva — las cuatro cubiertas entre `MODEL-009`, `010`, `011` y esta misión) — aunque ninguna esté todavía calibrada ni respaldada por datos reales.
- **No desbloquea, por sí sola, ninguna ejecución real** — `partidos.csv` sigue sin filas reales, y esta especificación, como toda la serie `MODEL-`, es investigación pendiente de aprobación, no una implementación.

---

# 14. Ventajas

- Ningún peso libre, igual que Variable001 — ningún símbolo nuevo que agregar al catálogo de `models/parameter-calibration.md`.
- Reutiliza el mismo sistema de puntos 3-1-0 ya fijado por `MODEL-011`, sin redefinirlo — consistencia de convención entre las dos variables de resultado.
- La ventana "todo el torneo hasta ahora" no requiere ningún placeholder de tamaño de muestra (`N`) — a diferencia de Variable001/003/004, está completamente determinada por la propia definición del torneo, sin ninguna elección arbitraria que calibrar.

---

# 15. Limitaciones

- `Gol_pct` pondera igual una diferencia de gol de +1 y de +5 si la proporción resultante es similar con pocos goles totales (ej. 1-0 da `Gol_pct=100`, igual que una hipotética paliza sin goles en contra) — limitación conocida de cualquier ratio con muestra pequeña de goles, más notoria al inicio de un torneo con pocos partidos jugados.
- El promedio simple entre `Puntos_pct` y `Gol_pct` (sección 6) es una decisión de diseño razonada (sección 4), no validada empíricamente — no está demostrado que ambas señales deban pesar exactamente igual.
- Mismo supuesto ya señalado en `MODEL-001`/`002` sobre `M_forma`: que el mismo modificador de forma es apropiado tanto para el ataque como para la defensa, hereda sin cambios a esta variable.
- No pondera por fuerza del rival del torneo — mismo principio de exclusión deliberada ya aplicado a Variable001 (`MODEL-011` §4): ese ajuste pertenece a `engine/03-Poisson.md`.

---

# 16. Aplicación dentro del Modelo Santiago

Especificación matemática oficial que `VariablePreparation` deberá implementar para Variable002, alimentando `M_forma` en `engine/01`/`engine/02` junto con Variable001, y transitivamente `engine/03-06`.

---

# 17. Referencias

- Sistema de puntos 3-1-0: misma convención estándar ya citada en `models/forma-reciente.md` (`MODEL-011`) §18 — no se repite la cita completa.
- `models/forma-reciente.md` (`MODEL-011`) — origen del sistema de puntos y del criterio de ponderación neutral reutilizados aquí.
- `models/offensive-strength.md` (`MODEL-001`), `models/defensive-strength.md` (`MODEL-002`) — consumidores ya existentes de Variable002 vía `M_forma`, sin cambios en esta misión.

---

# 18. Versión 2.0 (siguiente iteración de esta investigación)

Pendiente, condicionado a datos reales suficientes en `data/results/`:

- Validación empírica de si el promedio simple `(Puntos_pct + Gol_pct)/2` (sección 6) es la combinación óptima, o si una ponderación distinta (calibrada, no arbitraria) mejora la capacidad predictiva.
- Evaluación de si el debut en torneo (`n=0`, sección 10) debería, con evidencia real, tener un tratamiento de confianza reducida más específico que el ya genérico de `docs/17`.
- Evaluación de si "Rendimiento ofensivo"/"Rendimiento defensivo" deberían, en una futura versión, incorporar datos de tiro (`estadisticas_partido.csv`) si `docs/03` llegara a ampliarse — hoy explícitamente fuera de alcance (sección 4).

---

# Validaciones

- **¿La fórmula usa solo datos autorizados por `docs/03` para Variable002?** Sí — "Victorias/Empates/Derrotas" (vía puntos) y "Goles" (vía `Gol_pct`); no se usa ningún dato táctico ni de tiro.
- **¿Se confundió Variable002 con Variable005 (Compatibilidad Táctica)?** No — sección "Nota de nomenclatura" corrige explícitamente el nombre del brief y confirma que ningún dato táctico se usa ni se reintroduce.
- **¿Se fija algún peso sin justificar?** No aplica — sin pesos libres (sección 6), mismo caso que Variable001.
- **¿Se creó un documento paralelo indebidamente?** No — verificado que ningún documento de `models/` definía ya Variable002 antes de esta misión (`docs/28`, sección "Nota de nomenclatura y de alcance").
- **¿Es reproducible?** Sí — función determinista de los resultados y goles ya observados en el torneo.

---

# Cierre obligatorio

**1. ¿Qué definición operacional quedó aprobada?**
Variable002 = combinación de porcentaje de puntos (sistema 3-1-0) y proporción de goles a favor, ambos calculados exclusivamente sobre los partidos ya disputados por la selección dentro del `id_torneo` específico del partido a predecir — sección 2.

**2. ¿Qué fuente de datos consume?**
`partidos.csv`, filtrado por `id_torneo` exacto (resultado y goles) — sección 5. No usa `estadisticas_partido.csv` ni ninguna fuente externa.

**3. ¿Qué métricas utiliza?**
Puntos por partido (`{0,1,3}`) y goles a favor/en contra, ambos agregados sobre los partidos ya jugados del torneo — sección 7.

**4. ¿Qué fórmula matemática quedó definida?**
`Rendimiento_Torneo = (Puntos_pct + Gol_pct)/2` (o solo `Puntos_pct` si `Gol_pct` es indefinido), con `Puntos_pct = 100·Puntos_torneo/(3n)` y `Gol_pct = 100·Goles_favor/(Goles_favor+Goles_contra)` — sección 6. Sin pesos libres.

**5. ¿Qué ventana temporal utiliza?**
Sin `N` fijo — todos los partidos ya disputados por el equipo dentro del `id_torneo` específico del partido a predecir, sin ponderación interna — sección 8.

**6. ¿Qué rango produce?**
0 a 100, acotado por construcción aritmética — sección 9.

**7. ¿Qué casos límite contempla?**
Debut absoluto (`n=0`) → `disponible=False`, **pipeline NO se detiene** (excepción ya documentada en `docs/17`, confianza reducida); pocos partidos → `muestra_reducida=True`; fila corrupta → se descarta sola; `Gol_pct` indefinido → se usa solo `Puntos_pct` — sección 10.

**8. ¿Qué documentos quedaron afectados?**
Solo `models/rendimiento-torneo.md` (creado). `docs/03`, `docs/17`, `docs/28`, `docs/30`, `app/preparation/preparation.py`, `models/offensive-strength.md`/`defensive-strength.md` quedan documentados como afectados a futuro, ninguno modificado — sección 12.

**9. ¿Qué desbloqueará BUILD-021?**
El camino metodológico completo para implementar Variable002 en `VariablePreparation`, mismo patrón que `BUILD-018`/`BUILD-019`/(`BUILD-020` de Variable001). Con esta misión, las cuatro variables principales de desempeño de equipo (Forma Reciente, Rendimiento en el Torneo, Potencial Ofensivo, Solidez Defensiva) quedan, por primera vez, todas especificadas matemáticamente. No desbloquea una predicción real por sí sola — sección 13.

**10. ¿Qué misión recomendarías después?**
La misma aprobación pendiente que `MODEL-009`/`010`/`011` (Arquitecto Estadístico Humano), seguida de `BUILD-021` (implementación de Variable002, mismo patrón). Con las cuatro variables de desempeño ya especificadas, la prioridad más urgente pasa a ser la captura de datos reales (`docs/27`) — sin ella, las cuatro especificaciones siguen siendo sintácticamente correctas pero inejecutables.

---

# Fuera de alcance de esta misión

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext`, `Engine01`, Variables Oficiales ni Persistence.
- No se reintroduce ni se toca Variable005 (Compatibilidad Táctica) — permanece diferida exactamente como la dejó `MR-004`.
- No se calibra ningún peso — la fórmula no tiene ninguno que calibrar.
- No se actualiza `docs/03-Variables.md` ni `docs/28-Catalogo-de-Variables-Derivadas.md` — pertenece a una misión de `docs/`, no de `models/`.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano.

---

Fin del documento.
