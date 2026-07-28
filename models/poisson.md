# Modelo Poisson — Distribución de Marcadores

**Archivo:** `models/poisson.md`

**Misión:** MODEL-003 — Modelo Matemático de Poisson (fundacional) / MODEL-007 — Calibración Matemática del Modelo de Poisson (orden de aplicación, restricciones matemáticas, ejemplo simbólico completo) / MODEL-019 — Investigación del ajuste Dixon-Coles para la corrección del sesgo de empates (sección 16)

**Versión:** 2.2.0-investigación

**Estado:** Investigación — estructura matemática completa; parámetros (`μ_gol`, `κ`, `κ'`, `λ_min`, `λ_max`) **pendientes de calibración estadística**, conforme a `CLAUDE.md`. `MODEL-019` investiga (sin implementar) si Dixon-Coles resuelve el sesgo de empates ya medido por `VALID-001`/`VALID-003`/`ANL-001`/`CAL-004` — recomendación: **C) investigar además la magnitud de separación de `λ` antes de migrar** (sección 16.10).

---

# 1. Objetivo

Desarrollar el fundamento matemático completo que `engine/03-Poisson.md` implementará: cómo `Fuerza Ofensiva` (`MODEL-001`) y `Fuerza Defensiva` (`MODEL-002`) se transforman en una distribución de probabilidad de marcadores, y cómo esa distribución produce las Probabilidades Local/Empate/Visitante y el Top 4 que `docs/06`, `docs/14`, `docs/25` y `docs/26` ya asumían, sin definir hasta ahora, cómo se calculaban.

---

# 2. Descripción

La Distribución de Poisson modela la cantidad de goles de un equipo en un partido como el número de eventos independientes ocurridos en un intervalo de tiempo fijo (90 minutos), dado una tasa promedio `λ`. Es el núcleo probabilístico del Modelo Santiago: todo lo que los motores anteriores (`engine/01`, `02`) calculan converge aquí en una única distribución conjunta de marcadores.

---

# 3. Problema que Resuelve

Convertir dos índices acotados (Fuerza Ofensiva, Fuerza Defensiva, 0-100) en una distribución de probabilidad completa sobre todos los marcadores posibles — no solo un resultado más probable, sino una matriz entera de probabilidades conjuntas.

---

# 4. Fundamento matemático

**Por qué Poisson modela goles:** un gol es un evento discreto y relativamente raro dentro de un partido, que puede entenderse como el resultado de muchas oportunidades independientes, cada una con una probabilidad pequeña de convertirse en gol — la Distribución de Poisson es, formalmente, el límite de una distribución Binomial(n, p) cuando *n* es grande y *p* es pequeño, con `λ = n·p` constante (resultado estándar de teoría de probabilidad, no específico de fútbol). Esta aproximación es razonable cuando la tasa de generación de oportunidades es aproximadamente constante durante el partido.

**Cuándo funciona:** en partidos "normales", sin eventos disruptivos, donde ambos equipos mantienen un enfoque táctico estable durante los 90 minutos, y donde el número total de goles del partido está lejos de los extremos (ni 0-0 sistemático ni goleadas).

**Cuándo deja de funcionar:** cuando la tasa de gol **no es constante** en el tiempo (una expulsión, un cambio de marcador que altera la estrategia, tiempo de descuento con un equipo desesperado atacando) — el modelo asume una tasa fija `λ` decidida *antes* del partido; no se actualiza dinámicamente. También se debilita cuando los goles de ambos equipos **no son realmente independientes** entre sí (ver sección 5, Dixon-Coles).

---

# 5. Literatura científica

**Maher (1982):** primer modelo que trata los goles de local y visitante como dos variables Poisson **independientes**, con `λ_local` y `λ_visitante` derivados multiplicativamente de parámetros de ataque y defensa por equipo, más un factor de ventaja de local. Esta es, exactamente, la arquitectura que el Modelo Santiago ya adoptó desde `MODEL-001`/`MODEL-002`: Fuerza Ofensiva y Fuerza Defensiva como parámetros multiplicativos independientes por equipo.

**Dixon-Coles (1997):** identificó que el modelo de Maher, por asumir independencia total, predice sistemáticamente **mal la frecuencia real de marcadores bajos** (0-0, 1-0, 0-1, 1-1) — en la práctica, estos resultados ocurren con una frecuencia distinta a la que predice el producto simple de dos Poisson independientes, porque existe una dependencia débil entre los goles de ambos equipos precisamente en marcadores bajos. Su solución: un factor de corrección `τ(x,y; λ,μ,ρ)`, aplicado únicamente a esas cuatro celdas de la matriz, controlado por un parámetro de dependencia `ρ` (típicamente pequeño y negativo), estimado por máxima verosimilitud junto con los parámetros de ataque/defensa.

**Qué adopta el Modelo Santiago:** la estructura multiplicativa de Maher (ataque × defensa × ventaja de local) — ya presente en el diseño desde `MODEL-001`.

**Qué simplifica, explícitamente, en esta V1:** **no se adopta la corrección de Dixon-Coles** (`τ`/`ρ`) — se asume independencia total entre `λ_local` y `λ_visitante` (sección 6). Es una simplificación deliberada, no un descuido: estimar `ρ` requiere ajuste por máxima verosimilitud sobre un historial amplio de resultados reales, que hoy no existe (`data/results/` está vacío). Se documenta como candidato de "Versión 2.0" (sección 15), condicionado a que exista ese historial.

---

# 6. Construcción de λ

*(Sin asignar ningún valor numérico a los parámetros — solo su rol estructural, igual que `MODEL-001`/`MODEL-002`.)*

Cada `λ` combina el ataque de un equipo contra la defensa del **rival** (nunca contra su propia defensa) — estructura cruzada estándar de Maher/Dixon-Coles:

```
λ_local     = μ_gol · (FO_local / 50)     · ((100 − FD_visitante) / 50) · Adj_Localía(local)

λ_visitante = μ_gol · (FO_visitante / 50) · ((100 − FD_local) / 50)     · Adj_Localía(visitante)
```

Donde:

- `FO_local`, `FO_visitante` = Fuerza Ofensiva de cada equipo (`MODEL-001`, salida de `engine/01`), 0-100.
- `FD_local`, `FD_visitante` = Fuerza Defensiva de cada equipo (`MODEL-002`, salida de `engine/02`), 0-100, donde 100 = defensa élite (por la convención de signo invertido ya fijada en `MODEL-002`).
- `(100 − FD_rival)/50`: transforma la fuerza defensiva del rival en un multiplicador — a defensa rival promedio (`FD = 50`), el multiplicador es 1 (neutro); a defensa rival élite (`FD → 100`), el multiplicador tiende a 0 (suprime fuertemente los goles esperados); a defensa rival muy débil (`FD → 0`), el multiplicador tiende a 2.
- `μ_gol`: promedio histórico de goles por equipo por partido en la competición relevante — **calculado dinámicamente** a partir de `partidos.csv` (no un valor fijo propuesto por este documento; varía por competición, consistente con `data/processed/selecciones-nacionales/competiciones.csv`, MS-006, donde distintos tipos de competición ya tienen distinta naturaleza competitiva).
- `Adj_Localía`: `1 + κ` si el equipo juega de local, `1 − κ'` si juega de visitante, `1` si la sede es neutral (`Variable009`, `MR-004`) — `κ`, `κ'` simbólicos, pendientes de calibración.

**Ambos `λ` dependen exclusivamente de las salidas de `engine/01`/`engine/02` y de Variable009** — ninguna otra variable participa en esta fórmula, consistente con lo que `docs/17-Matriz-de-Consumo-de-Variables.md` ya declara como entradas de `engine/03` (Fuerza Ofensiva/Defensiva de ambos motores, más Localía directa desde `MR-004`).

---

# 7. Distribución de Poisson

Para un equipo con tasa `λ`, la probabilidad de anotar exactamente `x` goles es:

```
P(X = x) = (λˣ · e^(−λ)) / x!         para x = 0, 1, 2, 3, ...
```

Donde `e` es la base del logaritmo natural y `x!` es el factorial de `x`. Esta fórmula se aplica dos veces por partido — una vez con `λ_local` para los goles del equipo local, y una vez con `λ_visitante` para el visitante.

---

# 8. Matriz de marcadores

Bajo el supuesto de independencia (sección 5 — sin corrección Dixon-Coles en esta V1):

```
P(marcador = i-j) = P(X_local = i) · P(X_visitante = j)
                   = [(λ_local^i · e^(−λ_local)) / i!] · [(λ_visitante^j · e^(−λ_visitante)) / j!]
```

La matriz se construye para `i, j ∈ {0, 1, ..., 6}`, con una celda adicional agregada "7+" por cada equipo que acumula la probabilidad restante de la cola — la suma de todas las celdas de la matriz completa (incluida esa cola) es exactamente 1. La truncación en 6 es una elección práctica, no una limitación matemática: para valores de `λ` típicos de fútbol (órdenes de 1 a 3), la probabilidad de 7 o más goles de un equipo es marginal — la distribución completa (sin truncar) sigue siendo la definición formal; la matriz truncada es solo una representación operativa.

De esta única matriz se derivan, sin cálculos aparte:

- **Probabilidad Local** = suma de todas las celdas donde `i > j`.
- **Probabilidad Empate** = suma de las celdas donde `i = j`.
- **Probabilidad Visitante** = suma de las celdas donde `i < j`.

**Este es, por primera vez, el mecanismo matemático exacto detrás de "Probabilidad Local/Empate/Visitante"** — un contrato que `docs/06-Flujo-Operacional.md`, `docs/14-Prediction-Pipeline.md`, `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md` y `docs/26-Runtime-del-Modelo.md` ya exigían como salida, sin que ningún documento anterior definiera cómo se obtenía.

---

# 9. Obtención del Top 4

Algoritmo conceptual, sin pseudocódigo ni implementación:

1. Construir la matriz completa de probabilidades conjuntas `P(i,j)` (sección 8).
2. Ordenar todas las celdas de la matriz de mayor a menor probabilidad.
3. Seleccionar las primeras cuatro — el "Top 4 de marcadores más probables" ya exigido en `docs/14`/`docs/25`/`docs/26`, cada uno con su probabilidad individual.

No requiere ningún cálculo adicional a la matriz ya construida — es, literalmente, una ordenación de sus celdas.

---

# 10. Limitaciones

| Limitación | Explicación |
|---|---|
| Independencia entre goles | Supuesto central del modelo (Maher); Dixon-Coles demuestra que es imperfecto en marcadores bajos — no corregido en esta V1 (sección 5) |
| Partidos con expulsiones | Una tarjeta roja cambia la tasa de gol efectiva a mitad de partido; el modelo usa un único `λ` fijo, decidido antes del inicio — no captura este cambio dinámico |
| Prórroga | El modelo produce probabilidades para los 90 minutos reglamentarios; un período adicional tendría una tasa de gol distinta (fatiga, cambio de enfoque), no modelada aquí |
| Penales (tanda) | Proceso completamente distinto — binomial de aciertos individuales, no Poisson de goles de juego; fuera del alcance de este modelo por naturaleza, no por omisión |
| Partidos extremadamente abiertos | Un gol temprano puede alterar genuinamente la dinámica táctica del rival (jugar más arriesgado), rompiendo la independencia asumida más de lo habitual |
| Partidos extremadamente cerrados | El escenario donde la crítica de Dixon-Coles pesa más — es, precisamente, donde la ausencia de la corrección `ρ` en esta V1 introduce el mayor sesgo conocido |

---

# 11. Compatibilidad

- **Con `MODEL-001`/`MODEL-002`:** la fórmula de `λ` (sección 6) usa exclusivamente `Fuerza Ofensiva` y `Fuerza Defensiva` tal como esos dos documentos las definen — ningún término nuevo se introduce sin origen declarado.
- **Con `engine/03-Poisson.md`:** su propio texto declara "El motor recibe información proveniente de otros motores... Fuerza Ofensiva, Fuerza Defensiva" de ambos equipos, más "Localía" (agregada en `MR-004`) — exactamente las entradas usadas aquí, sin ninguna adicional.
- **Con `docs/17-Matriz-de-Consumo-de-Variables.md`:** confirma que `engine/03` no consume variables directamente salvo Localía — coherente con que esta fórmula solo agrega Variable009 como entrada directa, el resto llega vía `engine/01`/`02`.
- **Con `docs/28-Catalogo-de-Variables-Derivadas.md`:** "Goles Esperados" (Categoría D de ese catálogo, "Resultados parciales de motor") es exactamente `λ_local`/`λ_visitante` de esta sección — se actualiza su estado de "Pendiente" a fórmula ya definida aquí (sin editar `docs/28` en esta misión, fuera de su alcance).

---

# 12. Ventajas

- Modelo ampliamente validado en la literatura de fútbol desde hace más de cuarenta años (Maher, 1982).
- Convierte dos índices acotados en una distribución de probabilidad completa, no solo un resultado puntual — coherente con el principio del proyecto de nunca entregar "un único marcador" (`docs/02-modelo.md`, sección 6).
- Estructura simple de calibrar: solo tres parámetros simbólicos nuevos (`μ_gol`, `κ`, `κ'`) además de los ya definidos en `MODEL-001`/`MODEL-002`.

---

# 13. Aplicación dentro del Modelo Santiago

Es el núcleo probabilístico del sistema: recibe las salidas de `engine/01`/`02` y produce, en una sola matriz, todo lo que `engine/04` (Chaos), `engine/05` (Confidence) y `engine/06` (Expected Value) consumirán después — Probabilidades, Top 4 de marcadores y Goles Esperados.

---

# 14. Referencias

- Maher, M.J. (1982). "Modelling Association Football Scores." *Statistica Neerlandica*, 36(3), 109-118.
- Dixon, M.J. y Coles, S.G. (1997). "Modelling Association Football Scores and Inefficiencies in the Football Betting Market." *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 46(2), 265-280. 525 citas (Semantic Scholar) — verificado en `MODEL-019`.
- Karlis, D. y Ntzoufras, I. (2003). "Analysis of sports data by using bivariate Poisson models." *Journal of the Royal Statistical Society: Series D (The Statistician)*, 52(3), 381-393 — origen del modelo Bivariate Poisson y de la aproximación por distribución de Skellam para la diferencia de goles, ambos comparados en `MODEL-019` §16.9.
- `pena.lt`/`penaltyblog` (2025). "Football Prediction Models: Which Ones Work the Best?" — comparación empírica por *Ranked Probability Score* (Poisson, Dixon-Coles, Bivariate Poisson, Zero-Inflated Poisson, Binomial Negativa, Weibull) sobre datos reales de la Eredivisie 2023-24, usada como evidencia cuantitativa central en `MODEL-019` §16.5/16.9.
- `models/offensive-strength.md` y `models/defensive-strength.md` (`MODEL-001`, `MODEL-002`) — fuente de `FO`/`FD`, entradas directas de esta fórmula.
- `models/estabilizacion-muestras-pequenas.md` (`MODEL-017`/`MODEL-018`) — Shrinkage de Variable003/004, cuya interacción con la eficacia de Dixon-Coles se analiza en `MODEL-019` §16.7.

---

# 15. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a datos reales suficientes en `data/results/`:

- Calibración de `μ_gol` (dinámico por competición), `κ`, `κ'`.
- ~~Evaluación de si incorporar la corrección de Dixon-Coles (`τ`/`ρ`) mejora la capacidad predictiva en marcadores bajos~~ — investigado en `MODEL-019` (sección 16): recomendación **C) investigar además la magnitud de separación de `λ`** antes de migrar, no una migración directa. La calibración de `ρ` (si una futura misión de implementación lo justifica) sigue condicionada a que exista suficiente historial real, mismo motivo ya señalado aquí.
- Validación empírica de la elección de truncar la matriz en 6 goles (sección 8) contra la distribución real observada.
- Definición formal, en `docs/28`, de "Goles Esperados" como Variable Derivada de Categoría D con fórmula ya definida (actualización pendiente, fuera de esta misión).

---

# 16. Investigación del ajuste Dixon-Coles para la corrección del sesgo de empates (`MODEL-019`)

**Origen:** `VALID-001`, `VALID-003`, `ANL-001` y `CAL-004` midieron, de forma independiente y con muestras crecientes (`N=8` → `N=16` → `N=35`), el mismo sesgo: el Modelo Santiago **nunca predice un empate como resultado más probable** (recall de empates = 0% en las tres muestras), con la brecha entre probabilidad de empate asignada y frecuencia real de empates creciendo hasta 17.5 puntos porcentuales en `VALID-003` (22.5% asignado vs. 40.0% real, la muestra más grande y más reciente). Esta misión investiga, sin implementar nada, si el ajuste Dixon-Coles es la solución matemáticamente más adecuada.

## 16.1 Problema original: por qué el Poisson independiente subestima empates

El diseño vigente (`Engine03`, sección 6-8 de este documento) modela `goles_local` y `goles_visitante` como dos variables Poisson **independientes** — la probabilidad conjunta de cualquier marcador `(x,y)` es, simplemente, el producto `P(X=x)·P(Y=y)`. Esta independencia es una simplificación matemática conveniente (permite construir la matriz completa a partir de dos distribuciones marginales, sección 8), pero **no es realista**: en un partido real, ambos equipos ajustan su comportamiento táctico en función del marcador y del comportamiento del rival — cuando el resultado está 0-0 o 1-1, ambos equipos tienden a jugar de forma más conservadora (ninguno quiere arriesgar perdiendo lo que ya tiene), lo que hace que estos marcadores se sostengan con una frecuencia real mayor a la que predice el producto simple de dos Poisson independientes. Dixon y Coles (1997) documentaron esto empíricamente contra datos reales de la liga inglesa: la Poisson independiente subestima sistemáticamente **exactamente 4 marcadores** — `0-0`, `1-0`, `0-1` y `1-1` — y ningún otro. La razón de que sean justo estos 4 y no otros: son los únicos marcadores donde **ambos** equipos anotan como máximo 1 gol — la región donde la dependencia táctica descrita arriba tiene el efecto proporcionalmente más grande sobre la probabilidad conjunta (en marcadores altos, con más goles ya anotados por ambos lados, cualquier dependencia residual queda diluida entre muchas más combinaciones posibles).

**Evidencia directa dentro del propio proyecto, no solo bibliográfica:** `VALID-003` (`docs/00-Project-Tracker.md`) ya mostró la misma firma exacta sobre datos reales del Modelo Santiago — de los marcadores reales de la muestra de 35 partidos, `1-1` ocurrió 8 veces pero el modelo solo lo predijo como más probable 5 veces; `0-0` ocurrió 4 veces, predicho solo 1 vez — mientras que el modelo **sobre-predice** sistemáticamente `1-0` (13 veces predicho vs. 3 reales) y `0-1` (8 predicho vs. 3 reales). Esto es consistente con el diagnóstico Dixon-Coles, pero con un matiz importante desarrollado en la sección 16.9: la sobre-predicción de `1-0`/`0-1` (no solo la sub-predicción de `0-0`/`1-1`) sugiere que el problema no es únicamente de correlación en marcadores bajos, sino también de **cuán separados están `λ_local` y `λ_visitante`** entre sí (ver `ANL-001`, ya citado en el brief de esta misión).

## 16.2 El modelo Dixon-Coles: origen, objetivo, fundamento, cuándo y por qué

**Origen:** Mark Dixon y Stuart Coles, "Modelling Association Football Scores and Inefficiencies in the Football Betting Market", *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 1997 — 525 citas registradas en Semantic Scholar, uno de los papers más influyentes de modelado estadístico de fútbol.

**Objetivo declarado por los autores:** mejorar el modelo de Maher (1982) — que ya usaba dos Poisson independientes con parámetros de ataque/defensa multiplicativos por equipo, exactamente la arquitectura que el Modelo Santiago adoptó desde `MODEL-001`/`MODEL-002` (sección 5 de este documento) — corrigiendo su tendencia sistemática a predecir mal la frecuencia real de marcadores bajos, y además detectar ineficiencias explotables en las casas de apuestas de la época.

**Fundamento matemático:** en vez de reemplazar la Poisson independiente por completo (lo que exigiría un modelo bivariado con muchos más parámetros, sección 16.9), Dixon-Coles **preserva la estructura Poisson-independiente para todo el resto de la matriz** y multiplica únicamente las 4 celdas ya identificadas por un factor de corrección `τ(x,y;λ,μ,ρ)`:

```
τ(0,0) = 1 − λ·μ·ρ
τ(0,1) = 1 + λ·ρ
τ(1,0) = 1 + μ·ρ
τ(1,1) = 1 − ρ
τ(x,y) = 1   para cualquier otro (x,y)
```

donde `λ`=`λ_local`, `μ`=`λ_visitante` (usando la notación original del paper) y `ρ` es el único parámetro nuevo (sección 16.4). La probabilidad conjunta corregida es `P(x,y) = τ(x,y) · Poisson(x;λ) · Poisson(y;μ)`.

**Cuándo apareció:** 1997, en respuesta directa a la limitación ya conocida del modelo de Maher (1982) de 15 años antes.

**Por qué fue creado:** los propios autores señalan que la Poisson independiente, pese a ser razonablemente precisa en general, fallaba de forma **predecible y explotable** específicamente en marcadores bajos — suficiente para generar apuestas de valor esperado positivo contra las casas de apuestas que usaban modelos más simples en esa época, motivación original y explícita del paper (su segundo título, "...Inefficiencies in the Football Betting Market", lo confirma).

## 16.3 Diferencias matemáticas frente al Poisson clásico

| | Poisson independiente (vigente en `Engine03`) | Dixon-Coles |
|---|---|---|
| Marginales de `goles_local`/`goles_visitante` | Poisson(`λ_local`), Poisson(`λ_visitante`) | **Idénticas, sin cambio** |
| Probabilidad conjunta, marcadores altos (`x≥2` o `y≥2`) | Producto simple | **Idéntica, sin cambio** (`τ=1`) |
| Probabilidad conjunta en `{0-0, 1-0, 0-1, 1-1}` | Producto simple | Producto simple **× `τ(x,y;ρ)`** |
| Parámetros nuevos | Ninguno | **`ρ`** (un único escalar, compartido por todo el histórico, no por partido) |
| Normalización | Ya suma 1 automáticamente (marginales normalizadas) | Requiere **renormalizar** la matriz completa tras aplicar `τ` (la corrección redistribuye masa de probabilidad, no la crea; sin renormalizar, la suma de la matriz ya no es exactamente 1 — desviación pequeña pero no nula, documentada explícitamente por los propios autores) |

**Qué cambia:** únicamente 4 celdas de la matriz completa (`(MAX_GOLES+2)²` = 64 celdas en la implementación actual del Modelo Santiago, sección 8). El resto de la matriz —incluyendo toda la "cola" que ya modela `CELDA_COLA` (sección 8)— permanece exactamente igual.
**Qué permanece igual:** el cálculo de `λ_local`/`λ_visitante` (sección 6, Fuerza Ofensiva/Defensiva × `μ_gol` × Ajuste de Localía) — Dixon-Coles no toca en absoluto cómo se estima `λ`, solo cómo se combina la probabilidad conjunta a partir de `λ` ya calculado.
**Nuevo parámetro:** `ρ` (sección 16.4).
**Por qué modifica únicamente marcadores bajos:** es una decisión de diseño explícita de los propios autores, no una limitación accidental — Dixon y Coles probaron empíricamente que la desviación entre el modelo independiente y los datos reales se concentraba, de forma estadísticamente significativa, solo en esas 4 celdas; extender la corrección a más celdas no mejoraba el ajuste y sí añadía complejidad injustificada (mismo principio, aplicado 20 años antes, que `CLAUDE.md` exige hoy: "si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse").

## 16.4 El parámetro `ρ`

**Significado/interpretación:** mide la **desviación de la independencia** entre los goles de ambos equipos, exclusivamente en marcadores bajos. `ρ=0` reduce el modelo exactamente al Poisson independiente ya vigente (los 4 factores `τ` se vuelven `1`) — Dixon-Coles es, matemáticamente, una **generalización estricta** del modelo actual, no un reemplazo incompatible.

**Rango habitual:** típicamente entre `-0.1` y `-0.2` en ligas europeas de élite; el valor original estimado por Dixon y Coles sobre datos de la liga inglesa de los años 90 fue `ρ=-0.13`, cifra que se sigue citando como valor de referencia por defecto en implementaciones posteriores.

**Signo:** un `ρ` **negativo** (el caso empíricamente observado siempre) implica que los marcadores bajos ocurren **con más frecuencia** que la predicha por independencia total — consistente con la intuición táctica de la sección 16.1 (cautela mutua en el marcador ajustado).

**Cómo se estima normalmente:** por máxima verosimilitud, junto con (no por separado de) los parámetros de ataque/defensa de cada equipo y el factor de ventaja de local — es decir, `ρ` no se calibra de forma aislada; se ajusta simultáneamente con todo el resto del modelo sobre un historial amplio de resultados reales (temporadas completas, no partidos individuales). Dixon y Coles propusieron además una variante de "máxima verosimilitud ponderada" (dar más peso a partidos recientes que a partidos antiguos del mismo histórico) para que `ρ` refleje el estado actual de una liga, no un promedio histórico completo.

**Efecto cuando `ρ` aumenta (se acerca a 0) o disminuye (más negativo):** cuanto más negativo, mayor la corrección — `τ(1,1)=1-ρ` crece por encima de 1 (más probabilidad para el empate 1-1), mientras `τ(0,1)`/`τ(1,0)` decrecen levemente por debajo de 1 (menos probabilidad para las victorias mínimas 1-0/0-1) y `τ(0,0)` se ajusta según el producto `λ·μ` (efecto pequeño cuando ambos `λ` son bajos, mayor cuando son moderados). En el límite `ρ→0`, el modelo colapsa exactamente al Poisson independiente ya vigente.

**Limitación cuantitativa importante para esta investigación (no reportada explícitamente en ninguna fuente consultada, derivada aquí mediante cálculo directo):** el efecto de `τ` está **acotado** — con `ρ=-0.13` (valor de referencia), `τ(1,1)=1.13` (aumento del 13% sobre la probabilidad de 1-1, sin importar cuán separados estén `λ_local`/`λ_visitante`) y `τ(0,0)` depende del producto `λ·μ`, típicamente entre `1.03` y `1.10` para valores de `λ` moderados. Esto significa que Dixon-Coles **nunca puede, por sí solo, revertir un sesgo de la magnitud ya medida por `VALID-003`** (17.5 puntos porcentuales) si la causa dominante es que `λ_local` y `λ_visitante` están, de entrada, muy separados entre sí — un ajuste porcentual acotado (13% sobre una celda, menos sobre otra) no puede compensar una separación de `λ` arbitrariamente grande. Esta observación es central para la recomendación de la sección 16.10.

## 16.5 Evidencia científica

**Volumen de literatura:** el paper original tiene 525 citas (Semantic Scholar) — un volumen alto para un paper de estadística aplicada al deporte, confirmando que no es una técnica marginal ni experimental. Existen extensiones publicadas en revistas revisadas por pares hasta la actualidad, incluyendo una extensión reciente a fútbol femenino publicada en *Journal of the Royal Statistical Society Series C* (2023/2024) — evidencia de que el modelo sigue siendo objeto de investigación activa, no una técnica abandonada.

**Qué mejoras reportan / qué métricas mejora:** una comparación empírica independiente y reciente (blog técnico `pena.lt`, autor del paquete Python `penaltyblog`, especializado en modelado de fútbol) sobre datos reales de la Eredivisie holandesa 2023-2024, usando *Ranked Probability Score* (RPS — métrica estándar para evaluar predicciones ordinales L/E/V, más apropiada que Accuracy simple porque penaliza según la distancia entre la predicción y el resultado real) reportó: Dixon-Coles **0.1914**, empatado en primer lugar con un modelo de conteo Weibull, frente a Poisson simple **0.1915**, Zero-Inflated Poisson **0.1915**, Binomial Negativa **0.1916** y Bivariate Poisson **0.1916** (el peor de los seis). **Hallazgo honesto, no favorable a una recomendación entusiasta:** la mejora medida (0.1915→0.1914) es **mínima en términos absolutos** — del orden de una parte en 2000 — mucho menor de lo que la brecha de 17.5 puntos porcentuales ya medida en `VALID-003` haría desear. El mismo estudio encontró que el **ajuste temporal** (ponderar partidos recientes más que antiguos, técnica original también de Dixon-Coles 1997) aporta una mejora adicional mayor (RPS≈0.189) que la propia corrección `τ`/`ρ` por sí sola — sugiriendo que, en la práctica moderna, el valor de "Dixon-Coles" como paquete se debe más a su componente de ponderación temporal que a la corrección de marcadores bajos en sí misma.

**Limitaciones documentadas en la literatura:** (1) el modelo sigue asumiendo una tasa de gol constante durante los 90 minutos (no captura una expulsión o un cambio táctico a mitad de partido — misma limitación ya heredada del Poisson simple, sección 4 de este documento); (2) la corrección `τ` es válida solo para las 4 celdas explícitamente identificadas — no generaliza a otros posibles sesgos de correlación en otras zonas de la matriz; (3) estimar `ρ` de forma confiable requiere un historial amplio (típicamente varias temporadas completas de una liga) — con muestras pequeñas, la estimación de máxima verosimilitud de `ρ` es inestable (mismo tipo de problema de muestra pequeña ya documentado extensamente en `CAL-004`/`MODEL-017`/`MODEL-018` para Variable003/004, aplicado aquí a un parámetro distinto).

## 16.6 Uso en modelos deportivos modernos

**Casas de apuestas:** servicios de modelado de cuotas documentados públicamente combinan explícitamente un modelo Dixon-Coles con las cuotas de las principales casas minoristas del Reino Unido (Sky Bet, Bet365, Ladbrokes, Coral, Paddy Power, William Hill) como mecanismo de contraste/blending — evidencia de que sigue siendo, hoy, una referencia práctica en la industria, no solo académica.

**Modelos académicos:** además del paper original, existen extensiones publicadas en revistas revisadas por pares (ej. la ya citada extensión a fútbol femenino) y comparaciones sistemáticas contra alternativas más recientes (Bivariate Poisson, Zero-Inflated Poisson, modelos de conteo Weibull) en trabajos de 2024-2025 — el modelo se sigue usando como punto de referencia (*baseline*) obligado en cualquier paper nuevo de predicción de marcadores de fútbol.

**Proyectos open source / GitHub / Kaggle / blogs técnicos:** múltiples implementaciones públicas confirmadas, incluyendo el paquete `penaltyblog` (Python, publicado en PyPI, con implementación optimizada en Cython específicamente para Dixon-Coles), al menos 3 repositorios de GitHub dedicados exclusivamente a implementar este modelo, y varios blogs técnicos reconocidos en la comunidad de análisis de fútbol (`dashee87.github.io`, `opisthokonta.net`) con tutoriales completos paso a paso — confirma adopción amplia y práctica, no solo teórica.

## 16.7 Compatibilidad con el Modelo Santiago

**Variable001/Variable002:** sin ningún impacto — estas Variables alimentan `M_forma` dentro de `Engine01`/`Engine02` (Fuerza Ofensiva/Defensiva), un paso completamente anterior y externo a donde Dixon-Coles operaría (`_construir_matriz_conjunta` en `Engine03`, después de que `λ_local`/`λ_visitante` ya están calculados). Compatible sin fricción.

**Variable003/Variable004:** sin ningún impacto directo — alimentan `Engine01`/`Engine02` de la misma forma. **Relación indirecta importante, ya señalada en la sección 16.4:** la magnitud de separación entre `λ_local` y `λ_visitante` que Dixon-Coles no puede compensar depende, en última instancia, de qué tan extremos sean los valores de Variable003/004 — por lo que el Shrinkage recién implementado (siguiente punto) sí interactúa indirectamente con la eficacia de una futura corrección Dixon-Coles.

**Shrinkage (`IMP-002`/`MODEL-018`):** **totalmente compatible y, de hecho, complementario** — el Shrinkage ya redujo el rango observado de Variable003/004 (`VALID-003`: rango 21.94-88.81 y 18.35-78.19, frente al 3.02-96.47/2.06-87.80 medido por `CAL-004` antes del Shrinkage), lo que **reduce la separación típica entre `λ_local` y `λ_visitante`** — precisamente la condición bajo la cual Dixon-Coles es más efectivo (sección 16.4: su corrección acotada compensa mejor separaciones moderadas que separaciones extremas). Ambos mecanismos atacan el mismo síntoma (sesgo de empates) desde ángulos distintos y no conflictivos: Shrinkage reduce la causa raíz (separación excesiva de `λ`, diagnóstico de `ANL-001`), Dixon-Coles corrige el síntoma residual en el nivel de la matriz de probabilidad conjunta.

**Engine05 (Confianza):** consume `probabilidad_local`/`probabilidad_empate`/`probabilidad_visitante` ya calculados por `Engine03` — Dixon-Coles seguiría produciendo exactamente esas 3 cifras (solo con valores distintos, más precisos), sin cambiar la interfaz que `Engine05` ya espera. Compatible sin cambios en `Engine05`.

**Engine06 (Expected Value):** consume las probabilidades de `Engine03` para contrastarlas contra cuotas de mercado (`cuotas.csv`) — mismo razonamiento que `Engine05`: la interfaz no cambia, solo la precisión de los valores que la alimentan. Compatible sin cambios en `Engine06`.

**Conclusión de compatibilidad:** Dixon-Coles es arquitectónicamente compatible con el 100% de los componentes ya vigentes del Modelo Santiago, sin romper ninguna interfaz existente — el único punto de inserción necesario es dentro de `Engine03._construir_matriz_conjunta` (o una función equivalente nueva), aislado del resto del pipeline.

## 16.8 Complejidad de implementación

**Dificultad:** baja-media. La fórmula de `τ` (sección 16.2) es aritmética simple (4 líneas de código), aplicable directamente sobre la matriz ya construida por el mecanismo actual (sección 8) — no exige rediseñar la construcción de la matriz, solo insertar un paso de corrección + renormalización antes de extraer `probabilidad_local`/`empate`/`visitante`/`top_marcadores`.

**Archivos afectados (estimado, no ejecutado en esta misión):** únicamente `app/engine/engine03.py` — ningún otro archivo de `app/` necesitaría cambios, dado que la interfaz de salida (`Engine03Salida`) no cambiaría de forma.

**Riesgo:** bajo en términos de romper funcionalidad ya existente (es una generalización estricta, `ρ=0` reproduce el comportamiento actual exactamente) — el riesgo real está concentrado enteramente en **la elección del valor de `ρ`** sin evidencia estadística suficiente propia del proyecto (mismo tipo de riesgo ya gestionado con cautela en `CAL-002`/`MODEL-018` para otros parámetros: `KAPPA_LOCAL`/`KAPPA_VISITANTE`, `k` del Shrinkage). Usar el valor de referencia de la literatura (`ρ≈-0.13`) sin verificarlo contra datos reales del Modelo Santiago violaría directamente "nunca alterar pesos sin evidencia estadística" (`CLAUDE.md`).

**Impacto esperado:** limitado y acotado (sección 16.4/16.5) — mejora real pero modesta en la probabilidad de empate para marcadores específicos (0-0, 1-1), sin garantía de cerrar por sí solo la brecha de 17.5 puntos porcentuales ya medida.

**Compatibilidad hacia atrás:** total — con `ρ=0` el comportamiento es idéntico al actual; cualquier valor de `ρ` distinto de 0 es, matemáticamente, una extensión aditiva, nunca una sustitución incompatible.

## 16.9 Comparación con alternativas

| Alternativa | Qué corrige | Parámetros nuevos | Evidencia empírica (RPS, `pena.lt` 2023-24 Eredivisie) | Compatibilidad con la arquitectura actual |
|---|---|---|---|---|
| **Poisson independiente** (vigente) | — (baseline) | 0 | 0.1915 | — |
| **Dixon-Coles** | 4 celdas de marcador bajo (`0-0`,`1-0`,`0-1`,`1-1`) | 1 (`ρ`) | **0.1914** (mejor, empatado con Weibull) | Alta — inserción aislada en `Engine03` |
| **Bivariate Poisson** (Karlis-Ntzoufras) | Correlación entre **todos** los marcadores, no solo los bajos, vía un tercer componente Poisson compartido | 1-2 (parámetro de covarianza, más el parámetro de forma) | 0.1916 (el **peor** de los 6 modelos comparados en ese estudio) | Media — exige rediseñar la construcción de la matriz conjunta (ya no es un producto de 2 marginales) |
| **Zero-Inflated Poisson (ZIP)** | Exceso específico de **ceros** (equipos que no anotan ningún gol), vía un proceso de mezcla | 1-2 por equipo (probabilidad de "inflación" de cero) | 0.1915 (empatado con Poisson simple — sin mejora medible en ese estudio) | Media — requiere una estructura de mezcla distinta a la matriz Poisson simple |
| **Skellam** (Karlis-Ntzoufras 2003, vía diferencia de goles) | Modela directamente la **diferencia** de goles (L/E/V), evitando la necesidad de una corrección de correlación explícita | 0 adicionales sobre el enfoque bivariado subyacente | No evaluado en el mismo estudio (métrica RPS no aplica igual al no producir marcador exacto) | **Baja** — no produce una distribución de marcadores exactos; el Modelo Santiago necesita `top_marcadores`/Over-Under/BTTS (`VALID-003`), que exigen conocer el marcador completo, no solo la diferencia |
| **Elo + goles esperados** | Fuerza relativa vía un sistema de rating recursivo, no un modelo de marcador exacto | Requiere K-factor, `μ`/`σ` de incertidumbre inicial (ver `MODEL-018` §10, Opción D, ya evaluada allí para Variable003/004, mismo tipo de mecanismo) | No comparable directamente (paradigma distinto, no produce marcadores) | **Muy baja** — exigiría rediseñar `Engine01`-`Engine03` por completo, reemplazando Fuerza Ofensiva/Defensiva por un sistema de rating recursivo |

**¿Por qué elegir uno sobre otro?** Bivariate Poisson y ZIP fueron, en la única comparación empírica reciente encontrada, **iguales o peores** que el Poisson simple ya vigente — no hay evidencia que justifique su mayor complejidad para el caso general. Skellam y Elo+xG quedan descartados por incompatibilidad estructural con requisitos ya vigentes del Modelo Santiago (marcador exacto completo, no solo signo del resultado). Dixon-Coles es, de las 5 alternativas comparadas, la única que (a) mejora medible aunque modestamente sobre el baseline en la única evidencia empírica encontrada, (b) requiere el menor número de parámetros nuevos (uno), y (c) es arquitectónicamente compatible sin rediseñar nada ya vigente.

## 16.10 Recomendación oficial

**C) Investigar además la magnitud de separación de `λ_local`/`λ_visitante` antes de migrar a Dixon-Coles.**

**Justificación completa:** Dixon-Coles es, de las alternativas comparadas, la técnica correcta en principio — bien evidenciada (525 citas, uso activo en la industria y la academia), de bajo riesgo arquitectónico (generalización estricta del modelo actual, compatible con el 100% de los componentes ya vigentes, incluido el Shrinkage recién implementado), y de implementación acotada a un único archivo. **No se recomienda, sin embargo, migrar directamente (opción B)** por una razón cuantitativa específica desarrollada en esta misión (sección 16.4/16.5), no por duda genérica: la corrección `τ` está matemáticamente **acotada** a un ajuste porcentual fijo sobre 4 celdas (típicamente 7%-15% con el valor de referencia `ρ≈-0.13`), mientras que la brecha ya medida por `VALID-003` es de **17.5 puntos porcentuales** en la probabilidad de empate — una magnitud que un ajuste acotado, por diseño, no puede garantizar cerrar por sí solo, especialmente si (como sugiere `ANL-001`, ya citado en el brief de esta misión) la causa dominante del sesgo es que `λ_local` y `λ_visitante` llegan **demasiado separados** a la etapa de Poisson, no solo que la etapa de Poisson asuma independencia. La propia evidencia empírica externa más reciente encontrada (comparación RPS en Eredivisie 2023-24) refuerza esta cautela: la mejora medida de Dixon-Coles sobre Poisson simple fue mínima (0.1915→0.1914) cuando se aplicó de forma aislada, sin ponderación temporal adicional. **Tampoco se recomienda descartar Dixon-Coles (relegarlo a opción A, mantener Poisson sin más)** — es una mejora real, de bajo riesgo, y corrige exactamente el patrón de sesgo (sub-predicción de `0-0`/`1-1`, sobre-predicción de `1-0`/`0-1`) que `VALID-003` ya documentó con evidencia directa del propio proyecto. La recomendación C reconoce ambos hechos a la vez: Dixon-Coles probablemente forme parte de la solución final, pero implementarlo aislado, sin antes entender cuánto del sesgo total es atribuible a la separación de `λ` (un problema distinto, ya señalado por `ANL-001`, y no resuelto por `τ`/`ρ`), arriesga declarar "resuelto" un problema que en realidad solo se atenuó parcialmente — contrario al principio de "toda conclusión respaldada por evidencia" (`CLAUDE.md`).

---

# 17. Orden exacto de aplicación (`MODEL-007`)

*(Aporte de `MODEL-007` — la sección 6 ya definía cada término; esta sección formaliza el orden exacto en que se aplican, tal como lo exige esa misión.)*

```
Fuerza Base (cruzada)
   FO_propio × ((100 − FD_rival)/50) × μ_gol
        │
        ▼
Ajuste Localía (multiplicativo, directo — Variable009)
   × Adj_Localía(condición)
        │
        ▼
Historial Directo — NO se aplica en este punto.
   La arquitectura vigente (docs/03-Variables.md, docs/17-Matriz-de-Consumo-de-Variables.md,
   MR-004) asigna Variable010 exclusivamente a engine/05-Confidence.md. Ver sección 19
   para la justificación completa de por qué esta misión no lo incorpora aquí.
        │
        ▼
Calidad de Plantilla — NO se aplica como término adicional en este punto.
   Ya actúa aguas arriba, dentro de Pen (MODEL-001 §6.3, reutilizado por MODEL-002),
   que ya modificó FO/FD antes de llegar a esta fórmula. Ver sección 20.
        │
        ▼
λ preliminar
        │
        ▼
Restricciones matemáticas (sección 18): clip(λ_preliminar, λ_min, λ_max)
        │
        ▼
λ final (λ_local o λ_visitante)
```

Los dos pasos marcados como "NO se aplica" se incluyen explícitamente en el diagrama, en lugar de omitirse en silencio, porque el brief de `MODEL-007` los pedía como pasos del orden de aplicación — se documenta por qué no son pasos reales de esta fórmula, en vez de fingir que lo son.

---

# 18. Restricciones matemáticas de λ (`MODEL-007`)

| Restricción | Definición | Por qué es necesaria |
|---|---|---|
| **No negatividad** | `λ ≥ 0`, siempre | Garantizado por construcción: todo factor de la sección 6 es no negativo (`FO ≥ 0`; `(100−FD)/50 ≥ 0` porque `FD ≤ 100`; `μ_gol > 0` por definición, es un promedio de goles; `Adj_Localía > 0` **siempre que `κ' < 1`** — condición que debe imponerse explícitamente sobre el parámetro de visitante, para que el ajuste nunca invierta el signo de `λ`). Un producto de factores no negativos nunca es negativo — no se requiere una restricción adicional, solo la condición `κ' < 1` sobre el parámetro. |
| **Piso (`λ_min`)** | `λ_min > 0`, simbólico, valor pendiente de calibración | Evita el caso degenerado `λ = 0`, que implicaría `P(X=0) = 1` — una certeza absoluta de que un equipo no anotará, que ningún equipo real tiene. Ningún equipo, por débil que sea su Fuerza Ofensiva o por elite que sea la defensa rival, tiene probabilidad cero de anotar. |
| **Techo (`λ_max`)** | `λ_max`, simbólico, valor pendiente de calibración | Evita goles esperados irrealmente altos ante una combinación extrema de entradas favorables (ej. Fuerza Ofensiva máxima, Fuerza Defensiva rival mínima, ajuste de localía máximo) — protege contra el efecto acumulado de multiplicar varios factores favorables sin control. |
| **Función de saturación** | `λ = clip(λ_preliminar, λ_min, λ_max)` | Mismo patrón de recorte duro ya usado consistentemente en `MODEL-001`/`MODEL-002` para acotar Fuerza Ofensiva/Defensiva a `[0, 100]` — coherencia de estilo, no una técnica nueva introducida aquí |

**Alternativa de saturación suave (candidato de Versión 2.0, no adoptado aquí):** un recorte duro (`clip`) introduce una discontinuidad en la derivada exactamente en `λ_min`/`λ_max` — una función de saturación suave (ej. una transformación asintótica tipo sigmoide) evitaría esa discontinuidad, pero se descarta por ahora por añadir complejidad sin evidencia de que el recorte duro sea insuficiente (`CLAUDE.md`: "Si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse") — queda documentada como posible mejora futura, condicionada a evidencia empírica de que el corte duro distorsiona las predicciones cerca de los límites.

---

# 19. Historial Directo — por qué no participa en el cálculo de `λ` (`MODEL-007`)

**Corrección de alcance aplicada antes de escribir, exactamente por la misma razón que otras misiones de esta serie corrigieron discrepancias entre el brief y la arquitectura ya vigente (`docs/26`, `docs/29`):** el brief de `MODEL-007` pide diseñar `λ` como función de, entre otros factores, "Historial Directo". Se detectó, antes de incorporarlo, que hacerlo contradiría **tres** fuentes ya vigentes:

1. **`docs/03-Variables.md`, Variable010:** "Consumidor asignado: `engine/05-Confidence.md`... Esta variable tendrá poca influencia. **Nunca deberá dominar el modelo.**"
2. **`docs/17-Matriz-de-Consumo-de-Variables.md`:** clasifica explícitamente a Variable010 como "no utilizada, ni directa ni indirectamente" por `engine/03-Poisson.md` — su único consumidor confirmado es `engine/05`.
3. **`MR-004`** (la misión que activó esta variable en V1): la asignó a Confidence "como factor contextual menor", nunca a Poisson.

Incorporar Historial Directo a `λ` sería, en la práctica, lo opuesto de "nunca deberá dominar el modelo": `λ` es el parámetro más consecuente de todo el Engine — determina la distribución completa de marcadores, de la cual dependen, después, Probabilidades, Top 4, Índice de Caos, Confianza y Valor Esperado (sección 13). Cualquier variable que module `λ` directamente tiene, por construcción, la máxima influencia posible sobre el resultado final — precisamente lo que `docs/03` prohíbe para esta variable.

**Decisión de esta misión:** `λ` se calcula, en la sección 6, exclusivamente a partir de Fuerza Ofensiva, Fuerza Defensiva rival, `μ_gol` y Localía — sin Historial Directo. Esto no es una omisión: es la aplicación directa de la Constitución (Art. 6, "Gestión de cambios" — ningún cambio de variable/motor se aplica sin evidencia y sin documentación previa en el nivel correspondiente) y del Manual Operativo (`docs/22`, "Restricciones permanentes": "nunca asume un hecho sin evidencia documental"). Una investigación de `models/` no tiene autoridad para redefinir, de forma implícita, la Matriz de Consumo ya vigente (`docs/17`) — ese cambio, si alguna vez se justificara con evidencia estadística real, requeriría una misión `MR-`/`GR-` de reconciliación dedicada, nunca una decisión unilateral dentro de una investigación matemática.

**Mecanismo hipotético (documentado únicamente por completitud intelectual — explícitamente NO adoptado):** si una futura misión de reconciliación decidiera, con evidencia, incorporar Historial Directo a `λ`, el mecanismo menos disruptivo sería un ajuste multiplicativo acotado y simétrico, análogo a `Adj_Localía` (ej. `1 + clip(w_H·h, −δ_H,max, +δ_H,max)` con `δ_H,max` deliberadamente pequeño, para respetar "nunca deberá dominar el modelo" incluso si se adoptara). Este mecanismo **no forma parte de la fórmula oficial de esta misión** — se documenta solo para que una futura reconciliación no tenga que diseñarlo desde cero si alguna vez se aprueba.

---

# 20. Calidad de Plantilla — mecanismo indirecto ya vigente (`MODEL-007`)

A diferencia de Historial Directo, Calidad de Plantilla (Variable008) **sí** participa en el cálculo de `λ` — pero **indirectamente**, no como un término nuevo de esta fórmula. Su mecanismo ya existe, desde `MODEL-001`/`MODEL-002`:

```
Variable008 (Calidad de Plantilla, alcance reducido — MR-004)
        │
        ▼
Pen (penalización de disponibilidad, MODEL-001 §6.3 — reutilizada sin cambios por MODEL-002)
        │
        ▼
Fuerza Ofensiva / Fuerza Defensiva = clip(P · M_forma · (1 − Pen), 0, 100)
        │
        ▼
λ_local / λ_visitante (sección 6 de este documento — consume FO/FD ya ajustadas)
```

**Por qué no se agrega un segundo término directo en `λ` para Calidad de Plantilla:** hacerlo duplicaría el mismo efecto dos veces — una vez ya incorporado dentro de `Pen` (que ajustó Fuerza Ofensiva/Defensiva antes de que este documento las reciba), y otra vez si se sumara un término adicional en la fórmula de `λ`. Esta es exactamente la clase de riesgo que `docs/15-Capa-de-Preparacion-de-Variables.md` y `docs/17-Matriz-de-Consumo-de-Variables.md` ya identificaron de forma genérica para variables compartidas entre motores (ej. la duplicación ya señalada de "Rotaciones", `docs/17` sección 8) — este documento evita repetir ese mismo error con Calidad de Plantilla.

**Mecanismo, en una frase:** Calidad de Plantilla ya modula `λ` — a través de Fuerza Ofensiva y Fuerza Defensiva, no como una entrada adicional de esta sección.

---

# 21. Ejemplo simbólico completo (`MODEL-007`)

*(Completamente simbólico — ningún símbolo recibe un valor numérico, conforme a la restricción explícita del brief.)*

Sean:

```
FO_local = a          FD_local = b
FO_visitante = a'      FD_visitante = b'
μ_gol = m
κ = k_L   (ajuste de local)
κ' = k_V  (ajuste de visitante)
λ_min, λ_max  (piso y techo, sección 18)
```

**Paso 1 — Fuerza Base cruzada (sección 6):**

```
λ_local (base)     = m · (a/50)  · ((100 − b')/50)
λ_visitante (base) = m · (a'/50) · ((100 − b)/50)
```

**Paso 2 — Ajuste Localía (multiplicativo, sección 17):**

```
λ_local (con localía)     = λ_local (base)     · (1 + k_L)
λ_visitante (con localía) = λ_visitante (base) · (1 − k_V)
```

**Paso 3 — Historial Directo y Calidad de Plantilla:** no se aplican en este punto (secciones 19 y 20) — Calidad de Plantilla ya está incorporada dentro de `a`, `a'`, `b`, `b'` (porque `FO`/`FD` ya la incluyen vía `Pen`); Historial Directo no participa en absoluto.

**Paso 4 — Restricciones matemáticas (sección 18):**

```
λ_local     = clip( λ_local (con localía)     , λ_min, λ_max )
λ_visitante = clip( λ_visitante (con localía) , λ_min, λ_max )
```

**Resultado simbólico final:**

```
λ_local     = clip( m · (a/50)  · ((100 − b')/50) · (1 + k_L) , λ_min, λ_max )
λ_visitante = clip( m · (a'/50) · ((100 − b)/50)  · (1 − k_V) , λ_min, λ_max )
```

Ningún paso de este ejemplo asigna un valor numérico a `a`, `b`, `a'`, `b'`, `m`, `k_L`, `k_V`, `λ_min` ni `λ_max` — el ejemplo ilustra exclusivamente el mecanismo de composición, no un resultado calibrado.

---

# 22. Limitaciones adicionales (`MODEL-007`)

*(Extiende, sin repetir, la sección 10 ya existente.)*

- **`λ_min`/`λ_max` son símbolos sin validar empíricamente.** Un piso o techo mal calibrado podría no activarse nunca (inútil) o activarse con demasiada frecuencia (introduciendo un sesgo artificial hacia el centro de la distribución) — solo la calibración contra `data/results/` real puede determinar valores razonables.
- **La exclusión de Historial Directo (sección 19) no es una limitación estadística de este modelo, sino una restricción arquitectónica deliberada.** Tiene una consecuencia real: el Modelo Santiago no captura, en su núcleo probabilístico, ningún efecto de "paridad histórica" o "maldición" entre dos selecciones que se enfrentan recurrentemente — ese efecto, si existiera y fuera estadísticamente significativo, solo se reflejaría tenuemente vía Confidence, nunca vía la distribución de goles esperados.
- **El mecanismo indirecto de Calidad de Plantilla (sección 20) hereda, amplificada, la limitación ya señalada en `MODEL-002` (sección 9):** no está demostrado que la misma penalización (`Pen`) sea igualmente apropiada para el ataque y la defensa — si esa reutilización resulta incorrecta, su efecto se propagaría, sin corrección adicional, hasta `λ`, dos niveles aguas abajo de su origen.

---

# Validaciones

- **¿`λ` depende exclusivamente de Offensive y Defensive Strength?** Sí, más Localía (Variable009) — la única variable adicional, ya declarada como entrada directa de `engine/03` desde `MR-004`. Ninguna otra variable participa.
- **¿No contradice `engine/03`?** Confirmado en la sección 11 — mismas entradas, mismo motor, sin redefinir su texto.
- **¿Produce una matriz completa de marcadores?** Sí — la sección 8 define la matriz para todo `i,j` con probabilidad total 1 (incluida la cola agregada).

## Validaciones adicionales (`MODEL-007`)

- **¿Consistencia con `MODEL-001`?** Sí — Fuerza Ofensiva se consume tal como esa investigación la define (sección 6); ningún término de esta misión modifica su fórmula, y Calidad de Plantilla se reconoce explícitamente como ya incorporada dentro de ella (sección 20), sin duplicarla.
- **¿Consistencia con `MODEL-002`?** Sí, misma razón — Fuerza Defensiva se consume sin modificación, y la reutilización de `Pen` entre ambos motores (ya decidida en `MODEL-002`) se hereda, no se redefine.
- **¿Consistencia con `MODEL-003` (este mismo documento, versión fundacional)?** Sí — la sección 6 (Construcción de `λ`) no se modifica; esta misión solo la extiende con orden de aplicación (sección 17), restricciones (sección 18) y un ejemplo simbólico (sección 21).
- **¿Consistencia con `docs/03-Variables.md`?** Sí — en particular, la exclusión de Historial Directo (sección 19) es una aplicación literal, no una contradicción, de "Consumidor asignado: `engine/05-Confidence.md`" y "Nunca deberá dominar el modelo" (Variable010).
- **¿Consistencia con `engine/03-Poisson.md`?** Sí — su sección "Entradas" solo declara Fuerza Ofensiva, Fuerza Defensiva y Localía; esta misión no agrega ninguna entrada que ese documento no declare.

---

# Cierre obligatorio

**1. ¿Cómo se obtiene λ_local?**
`μ_gol · (FO_local/50) · ((100−FD_visitante)/50) · Adj_Localía(local)` — sección 6.

**2. ¿Cómo se obtiene λ_visitante?**
Estructura simétrica cruzada: `μ_gol · (FO_visitante/50) · ((100−FD_local)/50) · Adj_Localía(visitante)`.

**3. ¿Qué hipótesis asume Poisson?**
Que los goles de cada equipo ocurren como eventos independientes con tasa constante `λ` durante el partido, y que los goles de ambos equipos son independientes entre sí (esta última, ya señalada como la más frágil, sección 5).

**4. ¿Qué limitaciones tiene?**
Las seis de la sección 10 — independencia entre goles, expulsiones, prórroga, penales, partidos muy abiertos, partidos muy cerrados.

**5. ¿Qué produce exactamente este modelo?**
Una matriz completa de probabilidades conjuntas de marcador, de la cual se derivan Probabilidad Local/Empate/Visitante y el Top 4 — sin cálculos independientes para cada uno.

**6. ¿Qué documentos deberán referenciarlo?**
`engine/03-Poisson.md` (implementación futura), `docs/28` (al actualizar el estado de "Goles Esperados"), y `models/` futuros para `engine/04`/`05`/`06`, que consumen la salida de este modelo.

**7. ¿Qué misión recomendarías después?**
`models/chaos-index.md` o `models/confidence.md` — cualquiera de los dos puede desarrollarse ahora que Poisson define su entrada principal (la matriz de marcadores y los `λ`); ambos consumen esa misma salida sin depender uno del otro.

---

# Cierre obligatorio — `MODEL-007`

**1. ¿Cómo nace `λ` dentro del Modelo Santiago?**
Nunca como un dato capturado directamente de la Base de Conocimiento — nace enteramente como una salida derivada de otras salidas del Engine: el producto de Fuerza Ofensiva propia, Fuerza Defensiva rival (cruzada), un promedio histórico de gol por competición (`μ_gol`) y un ajuste multiplicativo de Localía, seguido de las restricciones matemáticas de la sección 18 (sección 6 y 17).

**2. ¿Qué factores lo modifican?**
Directamente: Fuerza Ofensiva propia, Fuerza Defensiva rival, `μ_gol`, Localía (Variable009). Indirectamente, a través de Fuerza Ofensiva/Defensiva: Forma Reciente, Rendimiento en el Torneo, Disponibilidad de Plantilla, Fatiga y Calidad de Plantilla (sección 20).

**3. ¿Qué factores NO deberían modificarlo?**
Historial Directo (Variable010) — excluido explícitamente y con justificación completa en la sección 19, por asignación arquitectónica vigente (`docs/03`, `docs/17`, `MR-004`) y por la advertencia expresa "nunca deberá dominar el modelo". Tampoco deberían modificarlo: Compatibilidad Táctica y Estado Psicológico (diferidas, sin fuente de datos, `MR-004`), ni las cuotas de mercado (`engine/03` ya declara explícitamente "nunca ajustar resultados para coincidir con cuotas").

**4. ¿Qué parte queda pendiente para calibración?**
Los cinco parámetros simbólicos sin valor numérico: `μ_gol` (dinámico por competición), `κ`, `κ'` (Localía), y los nuevos `λ_min`, `λ_max` (sección 18) — ninguno se fija en esta misión.

**5. ¿Qué evidencia estadística será necesaria?**
Historial real de partidos con goles observados (`data/results/`, hoy vacío) suficiente para estimar `μ_gol` por tipo de competición y para calibrar `κ`/`κ'` con suficientes observaciones de condición local/visitante/neutral; adicionalmente, suficientes marcadores extremos observados para calibrar `λ_min`/`λ_max` con evidencia, no por conveniencia.

**6. ¿Qué documento debería continuar después?**
Con los 6 motores ya en estado de investigación estructural completa (`MODEL-001` a `MODEL-006`), el documento que debería "continuar" no es un séptimo motor — es la captura de datos reales ya priorizada por `docs/27-Auditoria-de-Variables-Pendientes.md`, condición necesaria para que cualquier calibración (de `λ` o de cualquier otro parámetro) deje de ser simbólica.

**7. ¿Puede implementarse `engine/03` cuando esta misión termine?**
La **estructura**, sí — todos los términos de `λ` están definidos, en orden, con restricciones matemáticas explícitas. Los **coeficientes**, no — misma distinción ya aplicada de forma consistente en `MODEL-001` a `MODEL-006`: una implementación hoy sería sintácticamente correcta pero no calibrada.

**8. ¿Qué riesgos matemáticos siguen abiertos?**
Cuatro: (a) ausencia de la corrección de Dixon-Coles para marcadores bajos (ya conocido, sección 10); (b) elección de `λ_min`/`λ_max` todavía sin evidencia empírica (sección 22); (c) el supuesto de independencia entre `λ_local` y `λ_visitante` se mantiene sin corregir; (d) el mecanismo indirecto compartido de Calidad de Plantilla (vía `Pen`, heredado de `MODEL-002`) podría sub- o sobre-representar su efecto real sobre `λ`, al estar dos niveles aguas abajo de su origen (sección 22).

**9. ¿Qué misión recomendarías inmediatamente después?**
Una misión de captura de datos (ya identificada por `docs/27`) que habilite la calibración real de los parámetros simbólicos de los 6 motores, empezando por lo ya priorizado allí ("Grandes oportunidades", la tabla de alineación por partido). Alternativamente, si se prioriza el eje de gobernanza documental, una futura misión `MR-`/`GR-` podría evaluar formalmente, con evidencia, si Historial Directo debería reconsiderarse como entrada de `engine/03` — pero eso exige reabrir `docs/17`, fuera del alcance de esta investigación matemática.

**10. ¿Qué porcentaje del núcleo matemático queda completo tras esta misión?**
El mismo que ya declaraba `MODEL-006`: estructuralmente completo para los 6 motores, sin calibrar. Esta misión no agrega un motor nuevo a esa cuenta — refina específicamente la robustez matemática de Poisson (orden de aplicación, restricciones, ejemplo simbólico), sin cambiar el porcentaje agregado del núcleo del Engine.

---

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/03`, el Runtime, el Pipeline, las Variables Oficiales ni `docs/28`.
- No se fija ningún valor numérico de parámetro (`μ_gol`, `κ`, `κ'`, `λ_min`, `λ_max`).
- No se adopta la corrección de Dixon-Coles — queda como candidato documentado de Versión 2.0.
- No se incorpora Historial Directo a `λ` — se documenta explícitamente por qué (sección 19), en lugar de incorporarlo siguiendo el brief literal, por contradecir `docs/03`/`docs/17`/`MR-004` ya vigentes.
- No se modifica `docs/17-Matriz-de-Consumo-de-Variables.md` ni ningún otro documento de arquitectura — la exclusión de Historial Directo se documenta aquí, no se reconcilia allá (eso pertenece a una futura misión `MR-`/`GR-`, si alguna vez se justifica).

---

Fin del documento.
