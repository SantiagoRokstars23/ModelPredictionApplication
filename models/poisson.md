# Modelo Poisson — Distribución de Marcadores

**Archivo:** `models/poisson.md`

**Misión:** MODEL-003 — Modelo Matemático de Poisson

**Versión:** 2.0.0-investigación

**Estado:** Investigación — estructura matemática completa; parámetros (`μ_gol`, `κ`, `κ'`) **pendientes de calibración estadística**, conforme a `CLAUDE.md`

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
- Dixon, M.J. y Coles, S.G. (1997). "Modelling Association Football Scores and Inefficiencies in the Football Betting Market." *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 46(2), 265-280.
- `models/offensive-strength.md` y `models/defensive-strength.md` (`MODEL-001`, `MODEL-002`) — fuente de `FO`/`FD`, entradas directas de esta fórmula.

---

# 15. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a datos reales suficientes en `data/results/`:

- Calibración de `μ_gol` (dinámico por competición), `κ`, `κ'`.
- Evaluación de si incorporar la corrección de Dixon-Coles (`τ`/`ρ`) mejora la capacidad predictiva en marcadores bajos, una vez exista suficiente historial para estimar `ρ` de forma confiable.
- Validación empírica de la elección de truncar la matriz en 6 goles (sección 8) contra la distribución real observada.
- Definición formal, en `docs/28`, de "Goles Esperados" como Variable Derivada de Categoría D con fórmula ya definida (actualización pendiente, fuera de esta misión).

---

# Validaciones

- **¿`λ` depende exclusivamente de Offensive y Defensive Strength?** Sí, más Localía (Variable009) — la única variable adicional, ya declarada como entrada directa de `engine/03` desde `MR-004`. Ninguna otra variable participa.
- **¿No contradice `engine/03`?** Confirmado en la sección 11 — mismas entradas, mismo motor, sin redefinir su texto.
- **¿Produce una matriz completa de marcadores?** Sí — la sección 8 define la matriz para todo `i,j` con probabilidad total 1 (incluida la cola agregada).

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

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/03`, el Runtime, el Pipeline, las Variables Oficiales ni `docs/28`.
- No se fija ningún valor numérico de parámetro (`μ_gol`, `κ`, `κ'`).
- No se adopta la corrección de Dixon-Coles — queda como candidato documentado de Versión 2.0.

---

Fin del documento.
