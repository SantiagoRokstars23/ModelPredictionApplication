# Estrategia Oficial para Variables Pendientes (006, 007, 008 y 009)

**Archivo:** `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md`

**Misión:** GR-010 — Estrategia Oficial para Variables Pendientes (006, 007, 008 y 009)

**Versión:** 1.0.0

**Estado:** Análisis de gobernanza — sin código, sin modificación de `PredictionContext`, sin modificación del Runtime

---

## Objetivo

Resolver oficialmente, para cada una de las cuatro Variables Oficiales que hoy permanecen `disponible=False` sin método de cálculo autorizado o sin esquema compatible (Variable006, 007, 008, 009 — ver `app/preparation/preparation.py`, "Hallazgo central", actualizado por `BUILD-020`), cuál es su camino oficial hacia V1: qué puede implementarse ya, qué requiere datos nuevos, qué requiere investigación matemática y qué requiere un cambio arquitectónico. Esta misión analiza y recomienda — no implementa, no modifica `PredictionContext`, no modifica el Runtime, no modifica ningún algoritmo ni peso (Constitución, Art. 2/5).

---

## Metodología

Se releyó el estado real de cuatro fuentes antes de escribir, en lugar de confiar en memoria de sesión (`docs/22`, Lista de verificación previa): `docs/03-Variables.md` (definición de cada variable), `docs/16-Contrato-Oficial-de-Variables.md` (contrato de tipo/escala/nivel), `docs/17-Matriz-de-Consumo-de-Variables.md` (consumidores por motor), `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`, clasificación A-E dato por dato, ya ejecutada y aprovechada aquí en lugar de repetirse), `docs/02-modelo.md` (Nivel de importancia), `app/preparation/preparation.py` (estado real de implementación tras `BUILD-020`) y `app/engine/engine03.py` (código real de `_ajuste_localia`, incluido su propio "Hallazgo #3" ya documentado desde `BUILD-012`). Se verificó también, directamente, que `convocatorias.csv`, `jugadores.csv`, `lesiones.csv` y `estadios.csv` existen con el esquema de columnas que `docs/27` describe, pero **las cuatro tienen hoy 0 filas de datos reales** (mismo estado ya documentado para `partidos.csv`/`estadisticas_partido.csv` en `BUILD-017` a `BUILD-021`) — la disponibilidad analizada aquí es de **esquema**, no de fila real; ninguna de las cuatro variables resolvería un valor real hoy aunque su código existiera.

---

## Variable006 — Disponibilidad de Plantilla

**Definición (`docs/03`):** mide el impacto de bajas importantes, con tres señales: Lesiones, Suspensiones, Rotaciones. Nivel B (`docs/02-modelo.md`). Es la variable con más consumidores directos de las 12 (`engine/01`, `02`, `04`, `05` — `docs/17`, sección 10).

**¿Puede calcularse con los datos actuales?**
Parcialmente. De sus tres señales (`docs/27`, sección Variable006):

| Señal | Categoría (`docs/27`) | Estado |
|---|---|---|
| Lesiones | A | 100% derivable de `lesiones.csv` (tipo, gravedad, fechas, estado) hoy mismo |
| Suspensiones | B | `convocatorias.csv.estado_convocatoria` existe como campo, pero sus valores ENUM permitidos nunca se formalizaron — no confirmado que "suspendido" sea uno de ellos |
| Rotaciones | D | No existe ninguna tabla de alineación titular por partido — `convocatorias.csv` es a nivel de *torneo* (quién fue convocado), no de *partido* (quién jugó ese partido); sin eso no puede derivarse qué jugadores rotaron |

**¿Qué falta exactamente?**
(1) Formalizar los valores ENUM válidos de `estado_convocatoria` — trabajo documental, cero captura nueva. (2) Una tabla nueva de alineación por partido (`id_partido` × `id_jugador` × titular/suplente, como mínimo) — sin ella, "Rotaciones" no es derivable de ningún campo existente.

**¿Qué fuente produciría el dato?**
(1) es una decisión de definición, no una fuente nueva — se resuelve con una nota en `docs/03`/`docs/16` o un documento de esquema (`data/README.md`), no con una misión de captura. (2) requeriría una tabla nueva en `data/processed/selecciones-nacionales/`, probablemente del mismo proveedor que ya alimenta `partidos.csv`/`convocatorias.csv` si expone un endpoint de alineaciones — no hay ninguna fuente identificada hoy en el proyecto.

**Estado:** Bloqueada (parcial) — **Implementable en V1 con alcance reducido** (solo "Lesiones", categoría A), mismo patrón que `MR-004` ya aplicó a Variable008. El alcance completo (las 3 señales) permanece bloqueado.

**Razón:** No es un problema de fórmula matemática — es un problema de captura de datos (Rotaciones, categoría D) y de una definición pendiente (Suspensiones, categoría B).

**Datos faltantes:** Tabla de alineación titular por partido (Rotaciones). Formalización del ENUM de `estado_convocatoria` (Suspensiones) — no es un dato faltante en sentido estricto, es una definición pendiente sobre un dato que ya existe.

**Riesgo:** **Alto** — es la variable más compartida (4 de 6 motores). Cualquier decisión de alcance tomada aquí se propaga simultáneamente a `engine/01`, `02`, `04` y `05`; si se implementa con alcance reducido sin documentarlo con la misma explicitud que `MR-004` usó para Variable008, cada motor podría asumir erróneamente que Variable006 ya está completa cuando solo cubre 1 de 3 señales. `docs/17` (sección 8) ya señala, además, que "Rotaciones" se re-deriva hoy de forma independiente en los cuatro documentos de motor — riesgo de interpretación divergente si se implementa fuera de la Capa de Preparación de Variables.

**Recomendación:** (a) Declarar explícitamente un alcance reducido para V1 = solo "Lesiones" (100% derivable hoy), documentado en `docs/03` con una nota "Estado en V1 (GR-010)" — mismo patrón textual que Variable008/009/010 ya tienen vía `MR-004`; esto habilitaría una futura `MODEL-` (fórmula de "Disponibilidad de Plantilla" a partir solo de lesiones activas) seguida de una `BUILD-` de implementación, sin esperar a Rotaciones. (b) Una misión documental breve y de bajo riesgo que formalice los valores ENUM de `estado_convocatoria` (Suspensiones) — desbloquea esa segunda señal sin ninguna captura nueva. (c) Diferir "Rotaciones" a V2, marcada explícitamente como bloqueada por ausencia de tabla (mismo tratamiento que `docs/27` ya le dio).

---

## Variable007 — Fatiga

**Definición (`docs/03`):** evalúa el desgaste físico acumulado, con tres señales: Días de descanso, Minutos jugados, Viajes. Nivel B (`docs/02-modelo.md`). Consumida por `engine/01`, `02`, `04` (`docs/17`).

**¿Puede derivarse únicamente desde `partidos.csv`?**
Parcialmente. "Días de descanso" sí, 100% desde `partidos.csv` (diferencia de fechas entre partidos consecutivos de la selección). "Viajes" necesita además `estadios.csv` (comparar ciudad/país del estadio entre partidos consecutivos, una aproximación geográfica, no una medición exacta) — sigue sin requerir ninguna tabla nueva, pero no es solo `partidos.csv`. "Minutos jugados" **no puede derivarse de ningún CSV actual**: requiere una estadística individual de jugador por partido que no existe ni siquiera en `estadisticas_partido.csv` (que es a nivel equipo-partido, no jugador-partido) — ya diferida desde `MS-001`.

**¿Hace falta información temporal adicional?**
No. La información temporal ya existe y es suficiente (`fecha` en `partidos.csv` resuelve "Días de descanso" por completo). Lo que falta no es temporalidad, es **granularidad**: una estadística a nivel de jugador individual ("Minutos jugados"), que ninguna tabla actual provee.

**¿Es posible una V1 reducida?**
Sí — mismo patrón que `MR-004` aplicó a Variable008: una V1 con solo "Días de descanso" + "Viajes" (2 de 3 señales, ambas categoría C, ya derivables hoy sin ninguna captura nueva), dejando "Minutos jugados" diferido explícitamente a V2. `docs/27` ya documenta que el impacto de esa ausencia está "Mitigado — 'Días de descanso' ya cubre parcialmente el mismo fenómeno".

**Estado:** Implementable en V1 con alcance reducido (Días de descanso + Viajes) — **pendiente de investigación matemática previa** (ningún `MODEL-` existe todavía para Variable007, a diferencia de Variable001-004).

**Razón:** El dato de las dos señales del alcance reducido ya es derivable hoy sin ninguna captura nueva; lo que falta es la fórmula que las combine en un único índice 0-100 (`docs/16`: Variable007 es "Índice (0-100)").

**Datos faltantes:** Solo "Minutos jugados" (estadística individual de jugador por partido) para el alcance completo — no bloquea el alcance reducido.

**Riesgo:** Medio — el riesgo de dato está mitigado (`docs/27`), pero implementar la fórmula sin una investigación matemática previa violaría "Investigación antes de implementación" (`CLAUDE.md`), repitiendo el error que `BUILD-017` ya evitó para Variable001-004 originalmente.

**Recomendación:** Encargar una investigación matemática (`MODEL-`, siguiente número disponible en esa serie) para Variable007 con alcance reducido (Días de descanso + Viajes), siguiendo el mismo patrón editorial ya validado por `MODEL-009` a `MODEL-012`, antes de escribir cualquier código. Nota de eficiencia para una futura misión de datos: la misma tabla nueva que resolvería "Rotaciones" (Variable006) probablemente también resolvería "Minutos jugados" (Variable007) si incluye minutos por jugador — conviene diseñarla pensando en ambas variables a la vez si se prioriza esa captura, en lugar de dos misiones de datos separadas.

---

## Variable008 — Calidad de Plantilla

**Definición (`docs/03`):** mide el potencial general del equipo, con tres señales: Valor de mercado, Profundidad, Experiencia. Nivel C (`docs/02-modelo.md`). **Ya activa en V1 con alcance reducido desde `MR-004`** — a diferencia de Variable006/007, esta variable ya tiene una decisión de alcance formal tomada.

**¿Qué significa operacionalmente?**
`MR-004` ya fijó que, en V1, Variable008 se reduce a un único componente: "profundidad de plantilla", operacionalizado como conteo de jugadores convocados por posición (`docs/17`, fila "Profundidad de plantilla": `convocatorias.csv` + `jugadores.csv.posicion_principal`, "Conteo, sin fórmula exacta fijada"). Es decir: `MR-004` fijó **qué tabla usar**, pero no fijó **la fórmula matemática exacta** que convierte ese conteo en un índice 0-100 — esa fila queda marcada explícitamente "**Parcial**" en `docs/17`, el mismo estado que tenían Variable003/004 antes de `MODEL-009`/`MODEL-010`.

**¿Puede obtenerse del esquema actual?**
Sí, para "profundidad de plantilla": 100% derivable de `convocatorias.csv` (`posicion_convocatoria`) + `jugadores.csv` (`posicion_principal`), ambas columnas ya existentes. Para "Valor de mercado", no — ningún campo de ningún CSV lo contiene (`docs/27`). Para "Experiencia", sí de forma aproximada (contando convocatorias históricas de cada jugador, `docs/27`: "aproximación imperfecta: cuenta convocatorias, no partidos realmente jugados"), pero **fuera del alcance que el texto de `docs/03` fijó explícitamente para V1** (ver Autocrítica, hallazgo).

**¿Qué tabla falta?**
Ninguna para "profundidad de plantilla" (ya resuelto con las dos tablas existentes). Para "Valor de mercado" faltaría una fuente completamente nueva y externa (tipo mercado de transferencias) — ninguna tabla de la Base de Conocimiento actual la contiene, y no hay ninguna fuente identificada en el proyecto.

**Estado:** Implementable en V1 (alcance ya autorizado por `MR-004`) — **pendiente únicamente de la investigación matemática de la fórmula**, no del dato.

**Razón:** El dato está disponible y el alcance ya fue decidido; falta la investigación matemática (`models/`) que transforme "conteo de convocados por posición" en un índice 0-100 — sin eso, implementarlo directamente en `preparation.py` repetiría el mismo error que `BUILD-017` evitó para Variable003/004 (pesos/fórmula sin calibrar ni documentar).

**Datos faltantes:** Ninguno para el alcance ya fijado (profundidad de plantilla). "Valor de mercado" permanece categoría D indefinidamente.

**Riesgo:** Bajo para el dato (ya disponible y con alcance ya decidido). **Medio para una ambigüedad de alcance detectada en esta misión** (ver Autocrítica): el texto de `docs/03` ("Estado en V1", Variable008) declara explícitamente diferido solo "valor de mercado" — nunca menciona "Experiencia" como dentro o fuera de alcance, a diferencia de cómo sí declara "valor de mercado" fuera de alcance en el mismo párrafo. Existe riesgo de que una futura implementación asuma, sin confirmación, que "Experiencia" también está autorizada por `MR-004`.

**Recomendación:** (a) Encargar la investigación matemática (`MODEL-`, siguiente número disponible) que defina la fórmula de "profundidad de plantilla" — es, de las cuatro variables de esta misión, la que tiene menos bloqueos pendientes. (b) Resolver explícitamente, en esa misma investigación o en una nota editorial de `docs/03`, si "Experiencia" entra o no al alcance de V1 — hallazgo detectado aquí, no resuelto por esta misión (requiere confirmación del Arquitecto Estadístico Humano/Product Owner sobre el alcance real pretendido por `MR-004`). (c) Diferir "Valor de mercado" a V2 sin roadmap de captura concreto — no hay fuente identificada.

---

## Variable009 — Localía

**Definición (`docs/03`/`docs/16`):** determina el efecto de jugar como local; Nivel D; tipo "Texto controlado (ENUM)" con valores `local`/`visitante`/`neutral`; consumidor directo `engine/03-Poisson.md` (`MR-004`). Todos sus datos son categoría A — 100% completos (`docs/27`): `id_seleccion_local`/`visitante` y país del estadio ya existen.

Esta sección responde **únicamente** lo que el brief de esta misión pide: cómo resolver, en el diseño, el conflicto entre `ValorVariable.valor: float | None` (`app/runtime/prediction_context.py`) y el ENUM de texto que `docs/16` exige para esta variable — sin romper `PredictionContext` y sin modificarlo en esta misión.

**Estado real del conflicto (verificado en código, no de memoria):** `Engine03` ya tiene la fórmula completa escrita (`_ajuste_localia`, `app/engine/engine03.py`, líneas 267-284) y ya declara sus placeholders (`KAPPA_LOCAL = KAPPA_VISITANTE = 0.0`, documentado desde `BUILD-012`). El método hace literalmente `condicion = localia.valor; if condicion == "local": ...` — una comparación de texto contra un campo tipado `float | None`. El propio docstring del método ya lo documenta como bloqueado explícitamente ("Hallazgo #3", `BUILD-012`) y ya anticipa la naturaleza de la solución: *"se conserva la estructura completa de la fórmula para que un futuro arreglo de **tipo** la reactive sin tocar este método"* — es decir, el propio código, desde su primera versión, ya señala que el arreglo correcto es de **tipo**, no de fórmula ni de dato.

**Cómo resolver el conflicto sin romper `PredictionContext` (recomendación de diseño, no una implementación):**

Ampliar el tipo de `ValorVariable.valor` de `float | None` a **`float | str | None`** — una unión de tipos aditiva, mínima, que:

1. **No toca ninguna línea de `Engine03._ajuste_localia`** — la comparación `condicion == "local"` ya escrita empieza a funcionar exactamente como el código ya anticipaba, sin reescribir el método.
2. **No afecta a las otras 11 Variables Oficiales** — todas seguirán publicando siempre `float`; solo el productor de Variable009 (`VariablePreparation`, en una futura `BUILD-`) asignaría un `str` en lugar de un `float`.
3. **No renombra, mueve ni reestructura ningún campo de `VariablesBlock`** — `localia` sigue siendo un `ValorVariable`, en la misma posición, con el mismo nombre.

**Alternativa descartada (y por qué):** crear un tipo separado (p. ej. `ValorVariableCategorico`) y cambiar el campo `localia` de `VariablesBlock` a ese nuevo tipo. Es, en abstracto, más "limpio" (separa variables numéricas de categóricas), pero (a) rompería la firma de acceso ya escrita en `Engine03._ajuste_localia` (`variables.localia.valor`), obligando a modificar ese método de todas formas — exactamente lo que la unión de tipos evita; y (b) no aporta beneficio real hoy, porque Variable009 es la única variable categórica de las 12 (`docs/16`) — introducir una segunda jerarquía de tipos para un solo caso violaría "simplicidad sobre complejidad" (`CLAUDE.md`).

**Estado:** Bloqueada — bloqueo de **esquema** (tipo), no de dato ni de fórmula.

**Razón:** Conflicto de tipos entre el Contrato Oficial de Variables (`docs/16`: "Texto controlado ENUM") y el esquema Pydantic de `PredictionContext` (`float | None`), documentado desde `BUILD-012` como "Hallazgo #3", nunca resuelto formalmente hasta esta misión.

**Datos faltantes:** Ninguno — el dato (condición local/visitante/neutral) es 100% derivable hoy de `partidos.csv`/`estadios.csv` (`docs/27`).

**Riesgo:** Bajo hoy — con `KAPPA_LOCAL = KAPPA_VISITANTE = 0.0`, el ajuste de Localía es neutral (`Adj_Localía = 1`) incluso si el tipo se corrigiera mañana, así que el bug es hoy inofensivo en la práctica. **El riesgo es creciente**: en cuanto una futura misión calibre `KAPPA_LOCAL`/`KAPPA_VISITANTE` con evidencia real distinta de 0, este conflicto de tipo dejaría de ser inofensivo — produciría, de forma silenciosa y sin ningún error visible, un ajuste de Localía permanentemente neutral cuando debería reflejar una ventaja real de local. Es, de las cuatro variables de esta misión, la única cuyo riesgo **empeora con el tiempo si no se resuelve**, en lugar de mantenerse constante.

**Recomendación:** Aplicar la ampliación de tipo descrita arriba (`float | str | None`) en una futura misión `BUILD-` dedicada, con aprobación explícita del Arquitecto Estadístico Humano (modifica `PredictionContext`, Constitución Art. 5) — fuera de alcance de esta misión `GR-010`, que no modifica código. Se recomienda ejecutar esa `BUILD-` **antes** de cualquier misión que calibre `KAPPA_LOCAL`/`KAPPA_VISITANTE` con evidencia real, para no calibrar un peso que después resulte inaplicable por el bug de tipo.

---

## Matriz consolidada

| Variable | Implementable V1 | Datos suficientes | Requiere nueva investigación | Requiere cambio arquitectónico |
|---|---|---|---|---|
| Variable006 (Disponibilidad de Plantilla) | Parcial — solo "Lesiones" | Parcial — Lesiones sí; Suspensiones necesita definición (no captura); Rotaciones no | Sí — fórmula del alcance reducido, ningún `MODEL-` existe todavía | No, para el alcance reducido. Sí, tabla nueva para el alcance completo (Rotaciones) — cambio de Base de Conocimiento, no de `PredictionContext` |
| Variable007 (Fatiga) | Parcial — "Días de descanso" + "Viajes" | Parcial — 2 de 3 señales sí; "Minutos jugados" no | Sí — ningún `MODEL-` existe todavía, ni para el alcance reducido | No, para el alcance reducido. Sí, tabla nueva para "Minutos jugados" (alcance completo) |
| Variable008 (Calidad de Plantilla) | Sí — alcance ya fijado por `MR-004` (profundidad de plantilla) | Sí, para el alcance fijado | Sí — la fórmula de "profundidad" sigue marcada "Parcial" en `docs/17`, sin `MODEL-` dedicado | No |
| Variable009 (Localía) | No | Sí — 100%, ya completo (`docs/27`) | No — la fórmula ya existe en `Engine03._ajuste_localia` | Sí — ampliar `ValorVariable.valor` a `float \| str \| None` |

---

# Cierre obligatorio (preguntas del brief de esta misión)

**1. ¿Qué Variables pueden implementarse hoy?**
Ninguna puede saltar directamente a código hoy sin un paso previo — implementar cualquiera sin ese paso repetiría el error que `BUILD-017` ya evitó ("Investigación antes de implementación", `CLAUDE.md`). La más próxima es **Variable008**: dato 100% disponible, alcance ya autorizado formalmente por `MR-004`, solo pendiente de una investigación matemática breve. Le sigue **Variable007** en alcance reducido (mismo tipo de bloqueo, sin decisión de alcance previa formalizada). **Variable006** en alcance reducido (solo Lesiones) es la tercera. **Variable009** tiene el dato y la fórmula completamente listos, pero bloqueada por un conflicto de tipo que exige aprobación humana explícita para modificar `PredictionContext` — no por falta de investigación.

**2. ¿Cuáles no?**
Ninguna de las cuatro en su **alcance completo** (todas sus señales/componentes) puede implementarse hoy: Variable006 completo (falta tabla de Rotaciones), Variable007 completo (falta Minutos jugados), Variable008 completo (falta fuente de Valor de mercado), Variable009 (bloqueada por tipo, independientemente del alcance).

**3. ¿Qué información falta exactamente?**
Variable006: tabla de alineación titular por partido (Rotaciones) + formalización del ENUM de `estado_convocatoria` (Suspensiones). Variable007: estadística individual de minutos jugados por partido (Minutos jugados). Variable008: fuente de valor de mercado, externa y no planeada. Variable009: ninguna información falta — es 100% dato disponible, bloqueada por tipo de esquema, no por dato.

**4. ¿Cuál requiere cambio arquitectónico?**
Variable009 — ampliar `ValorVariable.valor` de `float | None` a `float | str | None`. Es la única de las cuatro cuyo bloqueo no es de dato ni de fórmula, sino de contrato/esquema de `PredictionContext`.

**5. ¿Cuál requiere únicamente datos?**
Variable006 (Rotaciones) y Variable007 (Minutos jugados) para sus alcances completos — ambas señales podrían resolverse con la misma tabla nueva de alineación por partido, si se diseña pensando en ambas a la vez. Variable008 (Valor de mercado) también requiere solo datos, pero de una fuente de naturaleza distinta (mercado de transferencias, no estadística de partido).

**6. ¿Cuál requiere investigación matemática?**
Variable007 (ningún `MODEL-` existe todavía, ni para el alcance reducido) y Variable008 (la fórmula de "profundidad de plantilla" sigue marcada "Parcial" en `docs/17`). Variable006 también la requeriría, incluso en su alcance reducido de solo Lesiones. Variable009 **no** requiere investigación matemática nueva — la fórmula ya está escrita en `Engine03._ajuste_localia`, con sus placeholders `KAPPA_*` ya declarados desde `BUILD-012`.

**7. ¿Qué Variable debería implementarse inmediatamente después?**
Variable008 (alcance reducido) — es la que tiene menos bloqueos pendientes: dato 100% disponible, alcance ya autorizado formalmente, y solo necesita una investigación matemática breve (mismo patrón editorial ya usado cuatro veces: `MODEL-009`/`010`/`011`/`012`) antes de una futura `BUILD-` de implementación.

**8. ¿Cuál debería diferirse a V2?**
Los componentes de categoría D de cada variable: "Rotaciones" (Variable006), "Minutos jugados" (Variable007), "Valor de mercado" (Variable008) — los tres requieren una tabla o fuente nueva, ninguna planeada todavía. De las cuatro variables completas, **Variable006 en su forma completa** es la que debería diferirse más explícitamente a V2: 2 de sus 3 señales (Suspensiones, Rotaciones) tienen algún tipo de bloqueo, más que cualquier otra de las cuatro.

**9. ¿Qué documentos quedarían afectados?**
`docs/03-Variables.md` (secciones "Estado en V1" de Variable006/007, mismo patrón editorial ya usado para Variable008/009/010 — no modificado en esta misión, identificado como pendiente). `docs/16-Contrato-Oficial-de-Variables.md` (columna "Escala" de Variable009 si se aprueba la codificación de texto; columnas de alcance/bloqueo de Variable006/007/008 si se formaliza cada alcance reducido). `docs/17-Matriz-de-Consumo-de-Variables.md` (fila "Profundidad de plantilla", hoy "Parcial", pasaría a "Diseñada" tras un futuro `MODEL-`). `app/runtime/prediction_context.py` (tipo de `ValorVariable.valor` — solo si una futura misión `BUILD-` lo aprueba explícitamente). `models/` (tres documentos de investigación nuevos, candidatos, ninguno creado en esta misión: Variable006 alcance reducido, Variable007 alcance reducido, "profundidad de plantilla" de Variable008).

**10. ¿Se actualizaron `CHANGELOG.md` y `docs/00-Project-Tracker.md`?**
Sí, ambos — ver entradas de esta misma misión (`GR-010`).

---

# Lista de verificación de cierre (`docs/22`, sección 5 — set estándar de 6 preguntas)

**1. ¿Qué problema resolvió?**
Formalizó, por primera vez, un veredicto explícito por variable (Implementable/Bloqueada, razón, datos faltantes, riesgo, recomendación) para las cuatro últimas Variables Oficiales activas sin método real — hasta ahora, su estado quedaba disperso entre `docs/27` (clasificación de datos), `docs/17` (consumo) y comentarios de código (`preparation.py`, `engine03.py`), sin una decisión de estrategia consolidada en un único documento.

**2. ¿Qué problemas nuevos descubrió?**
Dos: (a) ambigüedad de alcance en Variable008 — el texto de `docs/03` ("Estado en V1", `MR-004`) declara diferido explícitamente "valor de mercado" pero nunca se pronuncia sobre si "Experiencia" está dentro o fuera del alcance reducido, a diferencia de cómo sí trata "valor de mercado"; (b) el riesgo de Variable009 (bloqueo de tipo) es **creciente**, no constante — hoy inofensivo porque `KAPPA_LOCAL`/`KAPPA_VISITANTE = 0.0`, pero se activaría en cuanto se calibren esos parámetros, produciendo un fallo silencioso (ajuste de Localía permanentemente neutral) si no se resuelve antes.

**3. ¿Qué documentos podrían necesitar actualización futura?**
`docs/03-Variables.md` (notas "Estado en V1" para Variable006/007, y aclaración de alcance para Variable008/Experiencia), `docs/16-Contrato-Oficial-de-Variables.md`, `docs/17-Matriz-de-Consumo-de-Variables.md` (fila "Profundidad de plantilla") — ninguno modificado en esta misión, todos identificados como pendientes (`docs/22`, sección 6, "identificar, nunca aplicar").

**4. ¿Qué impacto tiene sobre el proyecto?**
Desbloquea metodológicamente la siguiente ronda de investigación matemática (`MODEL-`) con un orden de prioridad explícito (Variable008 primero, Variable007 segundo, Variable006 en alcance reducido tercero) y dictamina que Variable009 no necesita ninguna `MODEL-` — solo una `BUILD-` de cambio de tipo con aprobación humana. Evita que una futura sesión repita el análisis de datos ya hecho por `docs/27`.

**5. ¿Cómo cambia el riesgo arquitectónico?**
Reduce el riesgo de que Variable009 se calibre (`KAPPA_LOCAL`/`KAPPA_VISITANTE`) antes de resolver su bloqueo de tipo — riesgo que, sin esta misión, no tenía ninguna recomendación de secuencia explícita. Reduce también el riesgo de ambigüedad en Variable006 (la variable más compartida, 4 motores) al proponer que su alcance reducido se documente con la misma explicitud que `MR-004` ya usó para Variable008.

**6. ¿Qué impacto cualitativo tiene sobre el Índice de Madurez Arquitectónica (IMA)?**
No existe todavía un IMA formal (mismo estado que `GOV-001`/`GOV-002`). Cualitativamente, esta misión agrega madurez de **planificación de datos**: por primera vez, el proyecto tiene un veredicto explícito de qué variables activas necesitan captura de datos nueva (Rotaciones, Minutos jugados, Valor de mercado) frente a cuáles solo necesitan investigación matemática o un cambio de tipo — una distinción que antes existía de forma dispersa pero nunca consolidada.

---

# Gestión de hallazgos (`docs/22`, sección 7)

**Hallazgo:** ambigüedad de alcance de Variable008 respecto a "Experiencia" (ver Variable008, Riesgo).

1. **Documentado con el mismo rigor que el objetivo principal** — ver sección Variable008 arriba, con cita textual exacta de `docs/03`.
2. **Justificación técnica:** `docs/03` ("Estado en V1", Variable008) nombra explícitamente solo "valor de mercado" como diferido, sin mencionar "Experiencia" en ningún sentido — un lector no puede confirmar, solo con ese texto, si "Experiencia" está autorizada o simplemente fue omitida por descuido editorial.
3. **¿Cambia la prioridad del roadmap vigente?** **No.** Es una aclaración de alcance menor, no una contradicción bloqueante — no impide implementar "profundidad de plantilla" (el único componente con investigación matemática recomendada de forma inmediata en esta misión). Se recomienda resolverla como parte de la misma futura `MODEL-` de Variable008, o con una nota editorial breve de `docs/03`, sin abrir una misión de reconciliación dedicada.

---

# Autocrítica (`docs/22`, sección 8)

**¿Qué supuestos hice sin poder verificarlos completamente?**
Que la "misma tabla nueva" resolvería tanto "Rotaciones" (Variable006) como "Minutos jugados" (Variable007) — es una inferencia razonable (ambas son estadísticas a nivel jugador-partido) pero no está confirmada por ningún documento del proyecto ni por conocimiento del proveedor de datos real que eventualmente alimentaría esa tabla.

**¿Qué parte de este entregable podría estar equivocada?**
La recomendación de tipo para Variable009 (`float | str | None`) es una propuesta de diseño razonada, pero no la única técnicamente válida — asume que preservar `Engine03._ajuste_localia` sin tocarlo es más valioso que una separación de tipos más estricta; un Arquitecto Estadístico Humano con otra prioridad (p. ej. tipado más estricto con `mypy`) podría preferir la alternativa descartada.

**¿Qué información me habría hecho falta para tener más certeza?**
Confirmación directa del Arquitecto Estadístico Humano/Product Owner sobre si "Experiencia" está o no dentro del alcance de `MR-004` para Variable008 (hallazgo, no resuelto aquí). También, detalle real del proveedor de datos que alimenta `data/processed/` hoy, para saber si una tabla de alineación por partido es técnicamente obtenible de esa misma fuente o requeriría un proveedor distinto.

**¿Qué validaría antes de que esto se implemente o se tome como definitivo?**
Que la ampliación de tipo propuesta para Variable009 no rompa ninguna validación Pydantic existente en `_ContextModel` (no verificado directamente en esta misión, solo inferido de la definición de `ValorVariable` ya leída). Que el orden de prioridad recomendado (Variable008 → 007 → 006 reducido) siga siendo válido si una futura misión captura antes la tabla de alineación por partido (cambiaría el cálculo de costo/beneficio).

**¿Existe una interpretación razonable distinta a la que elegí?**
Sí, para Variable006: en lugar de un alcance reducido de solo "Lesiones", podría defenderse no implementar nada de Variable006 hasta tener las tres señales completas, argumentando que una "Disponibilidad de Plantilla" que ignora Suspensiones/Rotaciones podría ser engañosa para los cuatro motores que la consumen. Se prefirió la alternativa de alcance reducido por ser el patrón ya validado y aceptado explícitamente por el usuario en `MR-004` para Variable008 — pero es una elección de precedente, no la única lógicamente posible.

---

# Fuera de alcance de esta misión

- No se implementa código Python.
- No se modifica el Runtime, `PredictionContext`, ningún motor (`engine/01-06`) ni `VariablePreparation`.
- No se modifica ningún peso, algoritmo ni Variable Oficial existente.
- No se crea ningún documento `models/` (las investigaciones matemáticas recomendadas quedan para futuras misiones `MODEL-`).
- No se resuelve la ambigüedad de alcance de "Experiencia" en Variable008 — se documenta como hallazgo, no se decide aquí.
- No se aplica la ampliación de tipo recomendada para Variable009 — queda como propuesta de diseño para una futura `BUILD-` con aprobación explícita del Arquitecto Estadístico Humano.

---

Fin del documento.
