# Modelo Poisson — Distribución de Marcadores

**Archivo:** `models/poisson.md`

**Misión:** MODEL-003 — Modelo Matemático de Poisson (fundacional) / MODEL-007 — Calibración Matemática del Modelo de Poisson (orden de aplicación, restricciones matemáticas, ejemplo simbólico completo)

**Versión:** 2.1.0-investigación

**Estado:** Investigación — estructura matemática completa; parámetros (`μ_gol`, `κ`, `κ'`, `λ_min`, `λ_max`) **pendientes de calibración estadística**, conforme a `CLAUDE.md`

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
