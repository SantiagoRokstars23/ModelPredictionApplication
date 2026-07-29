# Anatomía Completa del Error del Modelo Santiago

**Archivo:** `models/error-modelo.md`

**Misión:** ANL-004 — Anatomía completa del error del Modelo Santiago

**Versión:** 1.0.0-investigación

**Estado:** Investigación — descomposición cuantitativa del error residual, sin ninguna implementación. Documento nuevo (no existía antes de esta misión).

---

# 1. Objetivo

Determinar, con evidencia cuantitativa y no por descarte cualitativo, dónde nace realmente el error residual del Modelo Santiago tras el cierre de la Fase I de investigación (`VALID-003`/`VALID-004`, `MODEL-020`/`IMP-003`, `MODEL-021`, `MODEL-022`): qué fracción del error observado proviene del cálculo de `λ`, qué fracción es inherente a modelar el fútbol como un proceso de Poisson (incluso con `λ` perfectos), qué fracción proviene del ranking del Top-4, y cómo se distribuye ese error entre mercados, competiciones, tipos de partido y magnitudes de `λ`. La pregunta que responde este documento ya no es "¿qué Variable está mal calibrada?" (ya investigado exhaustivamente, `MODEL-021`/`022`) sino "¿qué parte de la arquitectura explica el error que queda?".

---

# 2. Descripción

Sobre los mismos 35 partidos evaluables de `VALID-003`/`VALID-004`/`ANL-002`/`ANL-003` (mismo snapshot temporal, mismo pipeline real invocado directamente), se descompone el error observado en 8 dimensiones: origen en `λ`, piso teórico de un Poisson correctamente especificado, estructura del error del Top-4, desagregación por mercado, por competición, por tipo de partido (equilibrado/favorito claro) y por magnitud de `λ`, y una estimación cuantitativa del error inevitable. El hallazgo central — anticipado por el título de la misión, no por ninguna investigación previa — es que la gran mayoría del error observado no es atribuible a ningún defecto corregible del modelo: es, matemáticamente, el resultado esperable de un proceso aleatorio de baja frecuencia de eventos (goles) aplicado a un solo partido.

---

# 3. Problema que resuelve

Sin esta descomposición, cualquier métrica agregada de error (Brier `0.544`, Log Loss `0.889`, Accuracy ganador `60%`) es ambigua: no distingue entre "el modelo está mal" y "el fútbol es así de impredecible incluso con un modelo correcto". Esta confusión ya afectó el criterio de aceptación de `VALID-004` (Dixon-Coles rechazado por no mover la mayoría de las métricas) sin que existiera, hasta ahora, una estimación explícita de cuánta mejora era matemáticamente posible en primer lugar. Este documento resuelve esa ambigüedad con una técnica estándar y auditable (el "piso de Poisson", sección 6.2).

---

# 4. Ventajas (de esta descomposición, no del modelo en sí)

- Separa, por primera vez con evidencia cuantitativa, "error corregible" de "error inevitable" — evita que futuras misiones persigan mejoras que el propio marco teórico no permite alcanzar.
- Reutiliza exclusivamente infraestructura y datos ya aprobados (mismo conjunto de 35 partidos, mismo pipeline real) — ninguna fuente nueva, ningún supuesto no verificable.
- Cada una de las 8 descomposiciones es independiente y auditable por separado — un lector puede verificar cualquiera de ellas sin aceptar las demás.

---

# 5. Limitaciones

- `N=35` (y subconjuntos más pequeños dentro de cada desagregación, ej. `n=8` para Copa América, `n=11` por tercio de `|Δλ|`/`P_max`) — todas las cifras de esta sección son órdenes de magnitud con evidencia real, no estimaciones estadísticamente definitivas.
- Solo 2 de las 5 competiciones activas del proyecto (Eurocopa, Copa América) tienen partidos evaluables — Mundial, Eliminatorias y Nations League quedan sin ninguna cobertura en este análisis, mismo límite ya documentado desde `VALID-001`/`VALID-003` (ausencia de cobertura de StatsBomb).
- El "piso de Poisson" (sección 6.2) asume que los `λ` actuales del modelo son la mejor estimación disponible de la tasa real — no que sean exactos. Es una cota **inferior** del error atribuible al modelo (el error real por mala calibración de `λ` podría ser mayor que el 9.4% aquí medido, nunca menor), no una medición directa de la calidad de `λ`.

---

# 6. Aplicación dentro del Modelo Santiago

## 6.1 Objetivo específico 1 — Error atribuible al cálculo de `λ`

Sobre 70 observaciones (35 partidos × 2 lados), error firmado `λ − goles_reales`:

| | Valor |
|---|---|
| Error medio firmado | `+0.036` (sesgo casi nulo, `λ` ligeramente sobreestimado en promedio) |
| MAE | `0.928` |
| `λ` "demasiado alto" (error `>+0.5`) | 29/70 (**41.4%**) |
| `λ` "demasiado bajo" (error `<−0.5`) | 19/70 (**27.1%**) |
| `λ` "cercano" (`\|error\|≤0.5`) | 22/70 (**31.4%**) |

**Hallazgo central:** el sesgo direccional promedio es casi nulo (`+0.036`, insignificante frente a un MAE de `0.928`) — el problema de `λ` no es una tendencia sistemática a sobre- o subestimar, es **dispersión**: casi 7 de cada 10 observaciones se desvían más de medio gol del resultado real, repartidas de forma relativamente pareja entre exceso y defecto (41.4% vs. 27.1%).

**`λ` demasiado separados vs. demasiado cercanos:** contraintuitivamente, los partidos con **menor** separación entre `λ_local`/`λ_visitante` (tercio inferior de `|Δλ|`) muestran el **peor** desempeño (Brier `0.679`, Accuracy ganador `45.5%`) — peor que el tercio con mayor separación (Brier `0.529`, Accuracy `61.5%`). El mejor desempeño ocurre en el tercio **medio** (Brier `0.427`, Accuracy `72.7%`). Correlación `|Δλ|` vs. Brier por partido: `r=−0.144` (débil, dirección contraria a la intuición ingenua de "más separación = peor"). **Interpretación:** un partido genuinamente equilibrado (poca separación real de nivel entre los equipos) es, por naturaleza futbolística, más difícil de predecir correctamente — no es que el modelo "falle más" ahí, es que ese tipo de partido es intrínsecamente más incierto (desarrollado con evidencia cuantitativa en la sección 6.8).

## 6.2 Objetivo específico 2 — Error atribuible al supuesto de Poisson ("piso teórico")

**Método (técnica estándar, no inventada aquí):** usando los `λ_local`/`λ_visitante` **actuales** del modelo como si fueran exactamente correctos, se calcula el Brier/Log Loss **esperado** si el resultado de cada partido se muestreara repetidamente de esa misma distribución de Poisson — es decir, cuánto error persistiría **incluso si el modelo tuviera razón**, únicamente por la aleatoriedad inherente de un solo partido. Matemáticamente: `E[Brier] = Σ_(x,y) P(x,y)·BrierLoss(predicción_actual, resultado=(x,y))`, sumado sobre las 64 celdas de la matriz ya publicada por `Engine03` (`probabilidad_marcador`) — no requiere ningún dato nuevo, ninguna suposición adicional.

| | Brier | Log Loss |
|---|---|---|
| **Observado** (vs. resultado real) | `0.5439` | `0.8886` |
| **Piso de Poisson** (si `λ` fueran exactos) | `0.4926` | `0.8423` |
| **Fracción del error ya explicada por el piso** | **90.6%** | **94.8%** |
| Exceso (atribuible a `λ` mal estimado + independencia mal especificada + otros) | `0.0513` (9.4%) | `0.0463` (5.2%) |

**Hallazgo central de esta misión, el más importante de los 8 objetivos:** entre el **90% y el 95%** del error ya medido en `VALID-003`/`VALID-004` **existiría de todos modos, incluso si el cálculo de `λ` fuera perfecto** — es, matemáticamente, el costo de modelar goles como eventos de Poisson de baja frecuencia sobre un único partido, no un defecto corregible del Modelo Santiago. Solo el **9.4%** restante (Brier) es, en principio, atacable mediante mejor calibración de `λ` o corrección de la independencia (Dixon-Coles). Esto **explica cuantitativamente**, por primera vez, por qué `VALID-004` midió una mejora "modesta" de Dixon-Coles (`Log Loss −3.2%`, `Brier −2.0%`): Dixon-Coles solo puede operar dentro de ese 5-9% de margen matemáticamente disponible — nunca podría, aunque estuviera perfectamente calibrado, cerrar el 90%+ restante.

## 6.3 Objetivo específico 3 — Error del Top-4: ¿mal ordenado o incompleto?

| Posición del marcador real en el Top-4 | Frecuencia |
|---|---|
| #1 (más probable) | 9/35 (**25.7%**) |
| #2 | 2/35 (5.7%) |
| #3 | 2/35 (5.7%) |
| #4 | 2/35 (5.7%) |
| **Fuera del Top-4** | **20/35 (57.1%)** |

**Respuesta directa: faltan marcadores, el Top-4 no está mal ordenado.** Si el problema fuera de orden (el modelo identifica los marcadores correctos pero los prioriza mal), se esperaría una masa significativa en las posiciones #2-#4. En cambio, la caída de #1 (25.7%) a #2-#4 (5.7% cada una) es abrupta, y **más de la mitad de los resultados reales (57.1%) no aparecen en ninguna de las 4 posiciones** — el problema es de **cobertura**: la distribución de marcadores reales es más ancha que las 4 celdas que el modelo prioriza (mismo síntoma ya documentado por `VALID-003`: sobre-concentración en `1-0`/`0-1`, sub-representación de marcadores como `2-1`/`1-2` — `ANL-001`/`VALID-004`).

## 6.4 Objetivo específico 4 — Error por mercado

| Mercado | Accuracy/Recall |
|---|---|
| Ganador (L/E/V) | **60.0%** |
| Empate (recall) | **0.0%** |
| BTTS | 42.9% |
| Over/Under 2.5 | 48.6% |
| Marcador Exacto (rank-1) | 25.7% |
| Top-4 | 42.9% |

**El mercado que más error explica, por un margen enorme, es Empate (0%)** — el sesgo estructural ya documentado exhaustivamente (`VALID-003`, `ANL-002`, `VALID-004`) y confirmado aquí sin ninguna mejora nueva. Marcador Exacto (25.7%) es, esperablemente, el mercado más exigente de todos (equivalente al `rank-1` del Top-4). BTTS y Top-4 quedan empatados como el segundo peor grupo (~43%).

## 6.5 Objetivo específico 5 — Error por competición

| Competición | N | Accuracy ganador | Brier |
|---|---|---|---|
| Eurocopa | 27 | 59.3% | 0.547 |
| Copa América | 8 | 62.5% | 0.533 |

**Solo 2 de las 5 competiciones activas del proyecto tienen partidos evaluables** (Mundial, Eliminatorias Mundial y Nations League: 0 partidos evaluables, mismo límite de cobertura de `VALID-001`/`VALID-003` — sin datos de StatsBomb). Entre las 2 disponibles, la diferencia es pequeña (3.2 puntos de Accuracy, 0.014 de Brier) y el tamaño de muestra de Copa América (`n=8`) es demasiado reducido para considerar la diferencia significativa. **No hay evidencia de que la competición, por sí sola, sea un factor relevante de error** — con la salvedad honesta de que 3 de 5 competiciones no pueden evaluarse todavía en absoluto.

## 6.6 Objetivo específico 6 — Error por tipo de partido

Terciles de `P_max` (probabilidad del resultado más probable según el propio modelo):

| Tipo | Rango `P_max` | N | Accuracy ganador | Brier |
|---|---|---|---|---|
| Equilibrado | 0.422-0.531 | 11 | **45.5%** | **0.679** |
| Intermedio | 0.541-0.664 | 11 | **72.7%** | **0.427** |
| Favorito claro | 0.686-0.915 | 13 | 61.5% | 0.529 |

**Patrón no monótono, con dos hallazgos distintos:** (1) los partidos **equilibrados** (menor `P_max`) son, esperablemente, los más difíciles de acertar — coherente con la sección 6.1 y con la propia naturaleza del fútbol; (2) pero los partidos de **favorito claro** (mayor `P_max`, mayor confianza del modelo) **no** son los más fáciles — su Accuracy (61.5%) y Brier (0.529) son **peores** que el tercio intermedio. Esto es un indicio, con evidencia directa aunque `N` pequeño, del mismo patrón de sobreconfianza ya señalado cualitativamente por `ANL-001` (`P(favorito)` media 78.6% vs. accuracy real 62.5% en aquella muestra) — cuando el modelo está más seguro, no siempre acierta proporcionalmente más.

## 6.7 Objetivo específico 7 — Error por magnitud de `λ`

Terciles de `λ` individual (2N=70 observaciones):

| Magnitud | Rango `λ` | N | MAE |
|---|---|---|---|
| `λ` bajo | 0.252-0.739 | 23 | **0.639** |
| `λ` medio | 0.744-1.471 | 23 | **1.113** |
| `λ` alto | 1.509-3.487 | 24 | 1.027 |

**`λ` bajos son los más precisos** (MAE `0.639`) — coherente con que la mayoría de los marcadores reales de fútbol son bajos (0, 1, 2 goles), así que una predicción de `λ` bajo cae "cerca" de casi cualquier resultado real plausible. **`λ` medios muestran el mayor error** (`1.113`), superando incluso a `λ` altos (`1.027`) — con `N=23`/`24` por grupo, esta diferencia entre medio y alto no es lo bastante grande para considerarse concluyente, pero la brecha entre `λ` bajo y el resto sí es sustancial y consistente con la naturaleza de la distribución de Poisson (la varianza de una Poisson es igual a su media — `λ` más altos tienen, matemáticamente, más margen de error absoluto posible).

## 6.8 Objetivo específico 8 — Error inevitable

La sección 6.2 ya proporciona la respuesta cuantitativa central: **entre 90% y 95% del error actualmente medido persistiría aunque el cálculo de `λ` fuera perfecto**, únicamente por la naturaleza aleatoria de un partido de fútbol modelado como proceso de Poisson. Esto es consistente, no una novedad aislada, con la evidencia externa ya citada en `MODEL-019` (§16.5): la mejora de Dixon-Coles sobre Poisson simple, medida por RPS en datos reales de la Eredivisie, fue de apenas `0.1915→0.1914` — una fracción minúscula — exactamente lo que se esperaría si el "piso" de error inherente domina la varianza total. **Respuesta honesta a la pregunta del brief:** sí, incluso un Modelo Santiago "perfecto" (con `λ` exactos y sin ningún sesgo de independencia) seguiría teniendo un Brier del orden de `0.49` y un Log Loss del orden de `0.84` sobre esta muestra — muy por debajo de cero, porque el resultado de un único partido de fútbol es, y seguirá siendo, mayoritariamente aleatorio incluso cuando el modelo subyacente sea correcto.

---

# 7. Referencias

- `VALID-003`/`VALID-004` — métricas base ya publicadas, reutilizadas como punto de comparación (no recalculadas de fuentes externas).
- `ANL-001`/`ANL-002`/`ANL-003` — hallazgos de sesgo de empates, separación de `λ` y descomposición de `λ` en componentes, no repetidos aquí.
- `MODEL-019` §16.5 — evidencia externa (RPS, Eredivisie 2023-24) que ya anticipaba una mejora marginal de Dixon-Coles, ahora explicada cuantitativamente por el piso de Poisson de esta misión.
- `MODEL-020`/`IMP-003` — implementación de Dixon-Coles cuyo margen de mejora matemáticamente disponible queda acotado por la sección 6.2 de este documento.
- `MODEL-021`/`MODEL-022` — descartan Variable001 (parcialmente) y Variable007 (con la evidencia actual) como fuente de error corregible mediante Shrinkage.

---

# 8. Versión 2.0 — Síntesis y próximos pasos

Este documento no propone ninguna implementación (fuera de alcance explícito de `ANL-004`). La síntesis para una futura misión de diseño:

- **Mayor retorno esperado, con evidencia cuantitativa:** atacar el 57.1% de "marcadores reales fuera del Top-4" (sección 6.3) — no mediante Dixon-Coles (ya acotado a un margen pequeño, sección 6.2), sino investigando si la propia dispersión de la matriz de marcadores (más allá de las 4 celdas bajas que Dixon-Coles corrige) necesita un mecanismo distinto.
- **Línea de investigación a descartar:** cualquier expectativa de que una recalibración de `λ` por sí sola (Shrinkage adicional, ajuste de pesos) pueda cerrar más que, aproximadamente, el 9-10% de "exceso" ya acotado en la sección 6.2 — perseguir una mejora mayor mediante ese camino contradice la evidencia cuantitativa de esta misión.
- Pendiente de una futura misión: investigar si el patrón de sobreconfianza en partidos de "favorito claro" (sección 6.6) es reproducible con mayor `N`, antes de proponer cualquier corrección de calibración.

---

Fin del documento.
