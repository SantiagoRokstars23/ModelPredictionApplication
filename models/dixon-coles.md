# Dixon-Coles — Diseño Matemático y Arquitectónico de la Integración

**Archivo:** `models/dixon-coles.md`

**Misión:** MODEL-020 — Diseño matemático y arquitectónico de la integración Dixon-Coles (continúa `MODEL-019`, `models/poisson.md` §16, sin repetir su investigación)

**Versión:** 1.0.0-diseño

**Estado:** Diseño completo, no implementado. Estructura y ecuaciones definitivas; parámetro `ρ` declarado simbólicamente (`ρ=0`, sin calibrar). Ningún archivo de `app/` fue creado ni modificado por esta misión — documento exclusivamente de diseño, condición previa para una futura `IMP-003`.

---

# 1. Objetivo

Diseñar, con precisión suficiente para implementarse sin decisiones adicionales, la integración del ajuste Dixon-Coles dentro del pipeline ya vigente del Modelo Santiago: dónde se inserta, qué recibe, qué produce, qué modifica y qué no, la ecuación definitiva, el mecanismo de renormalización, el diseño del parámetro `ρ`, la prueba formal de compatibilidad hacia atrás (`ρ=0`), la prueba de compatibilidad con `Engine04`-`06`, el impacto esperado sobre las métricas ya medidas, y el plan de una futura misión de implementación (`IMP-003`). Esta misión **no vuelve a investigar ni a justificar Dixon-Coles** — esa evidencia ya está aprobada (`MODEL-019`, `models/poisson.md` §16) y su recomendación (opción C: investigar la separación de `λ` antes de migrar) ya fue ejecutada por `ANL-002`.

---

# 2. Descripción

Dixon-Coles dejó de ser, tras `ANL-002`, un candidato sin evidencia propia del proyecto: `ANL-002` midió (N=35, mismo backtest de `VALID-003`) que aproximadamente 70-80% del sesgo de empates observado (17.9pp) es atribuible a la independencia del Poisson —exactamente lo que Dixon-Coles corrige— y solo 20-30% a la separación de `λ_local`/`λ_visitante` (causa que Dixon-Coles no ataca). Esta misión traduce esa evidencia en un diseño completo, listo para una futura implementación, sin escribir una sola línea de código.

---

# 3. Problema que resuelve

Cerrar la brecha entre el diseño matemático ya investigado (`MODEL-019`) y una implementación futura (`IMP-003`): hoy existe evidencia y una recomendación, pero ningún documento especifica con precisión de ingeniería dónde vive el ajuste en el pipeline real, qué contrato de entrada/salida respeta, cómo se renormaliza la matriz, ni cómo se demuestra que no rompe nada ya vigente. Sin ese diseño, cualquier intento de implementación tendría que tomar esas decisiones de forma improvisada durante la escritura del código — exactamente lo que `CLAUDE.md` prohíbe ("la implementación pertenece al `engine`... la investigación pertenece a `models/`").

---

# 4. Ventajas (del diseño elegido, no de Dixon-Coles en sí — ya evaluado en `MODEL-019`)

- Aislamiento total: la corrección vive enteramente dentro de `Engine03`, sin tocar `Engine01`, `Engine02`, `Engine04`, `Engine05` ni `Engine06` (sección 8).
- Respeta el principio *append-only* de `PredictionContext` (`docs/30`, `BUILD-004`) sin necesitar ningún campo nuevo en el contrato — `Engine03Salida` se escribe una única vez, ya con la corrección incorporada.
- Generalización estricta matemáticamente demostrable (`ρ=0` ⟹ identidad exacta, sección 11) — riesgo de regresión mínimo y verificable por diferencia byte a byte.
- Reutiliza exactamente el contrato de tipos ya existente (`MarcadorProbabilidad`, `Engine03Salida`) — cero superficie nueva de `PredictionContext`.

---

# 5. Limitaciones (del diseño, heredadas y nuevas — no se repiten las ya documentadas en `MODEL-019`/`models/poisson.md` §16.4-16.5 sobre el alcance acotado de `τ`)

- El diseño exige que la corrección se aplique **dentro** de `Engine03.ejecutar()`, antes de construir `Engine03Salida` — si una futura misión decidiera, por otra razón arquitectónica, mover la corrección a un componente externo, tendría que resolver de nuevo el problema de *append-only* que esta misión ya resolvió (sección 8.4).
- `ρ` es un único escalar global (sección 7) — no captura variación por competición, por tipo de torneo ni por época, misma limitación estructural ya aceptada para `κ_local`/`κ_visitante`/`k` del Shrinkage.
- El diseño no resuelve el 70-80% restante del sesgo atribuido a la independencia únicamente en la medida en que la propia corrección `τ` está acotada (`MODEL-019` §16.4) — esta misión diseña la integración completa, no promete cerrar la brecha por sí sola.

---

# 6. Aplicación dentro del Modelo Santiago

## 6.1 Dónde entra Dixon-Coles en el pipeline (requisito 1 del brief)

**Diagrama conceptual** (nivel de flujo de datos, tal como lo pide el brief):

```
Variables (VariablePreparation)
        │
        ▼
Engine01 (Fuerza Ofensiva)
        │
        ▼
Engine02 (Fuerza Defensiva)
        │
        ▼
Engine03 (Poisson)
        │
        ▼
Dixon-Coles (corrección τ/ρ + renormalización)
        │
        ▼
Engine04 (Índice de Caos)
        │
        ▼
Engine05 (Confianza)
        │
        ▼
Engine06 (Valor Esperado)
```

**Diagrama arquitectónico** (nivel de implementación — dónde vive realmente el código, decisión de diseño de esta misión, justificada en 6.4):

```
Engine03.ejecutar()
   │
   ├─ calcular λ_local, λ_visitante                      (sección 6 de models/poisson.md — SIN CAMBIOS)
   ├─ construir distribuciones marginales P(X=x), P(Y=y)  (models/poisson.md §7 — SIN CAMBIOS)
   ├─ construir matriz conjunta cruda P(i,j)=P(X=i)·P(Y=j) (models/poisson.md §8 — SIN CAMBIOS)
   │
   ├──▶ [NUEVO] _aplicar_correccion_dixon_coles(matriz, λ_local, λ_visitante, ρ)
   │         aplica τ(x,y) sobre las 4 celdas (0,0)/(1,0)/(0,1)/(1,1)   (sección 6.3)
   │
   ├──▶ [NUEVO] _renormalizar_matriz(matriz)
   │         divide toda la matriz por Z                                (sección 6.5)
   │
   ├─ extraer Probabilidad Local/Empate/Visitante           (SOBRE la matriz ya corregida)
   ├─ extraer Top 4 marcadores                              (SOBRE la matriz ya corregida)
   │
   ▼
Engine03Salida   ── MISMO contrato exacto, MISMOS campos (BUILD-012, sin cambio de forma)
   │
   ▼
Engine04 / Engine05 / Engine06  ── CERO cambios de código (sección 8)
```

La diferencia entre ambos diagramas no es una contradicción: el diagrama conceptual describe el flujo lógico de información (tal como lo exige el brief); el arquitectónico describe la ubicación real del código, elegida deliberadamente para que la corrección se publique como parte de la única escritura de `context.engine.engine03` (nunca como una reescritura posterior), evitando así cualquier fricción con el principio *append-only* (sección 6.4).

## 6.2 Qué recibe exactamente (requisito 2 del brief)

| Entrada | Origen | Tipo | ¿Cambia respecto a hoy? |
|---|---|---|---|
| `λ_local` | `Engine03._calcular_lambda` (ya existente, sección 6 de `models/poisson.md`) | `float` | No — mismo valor, mismo cálculo |
| `λ_visitante` | ídem | `float` | No |
| Matriz Poisson cruda | `Engine03._construir_matriz_conjunta` (ya existente, `models/poisson.md` §8) | `list[MarcadorProbabilidad]` (`(MAX_GOLES+2)²` = 64 celdas, incluida la celda de cola `"7+"` por equipo) | No — es la misma matriz que hoy se usa directamente para extraer probabilidades; con Dixon-Coles se usa como entrada intermedia, no como salida final |
| `ρ` | Nueva constante simbólica de `Engine03` (sección 7) | `float` | N/A — parámetro nuevo |

## 6.3 Qué produce exactamente (salidas, requisito 2 del brief)

| Salida | Tipo | Reutiliza tipo existente? |
|---|---|---|
| Matriz conjunta corregida y renormalizada | `list[MarcadorProbabilidad]` | Sí — mismo tipo, mismas 64 celdas (mismos marcadores como claves de texto), solo probabilidades distintas |
| `probabilidad_local` / `probabilidad_empate` / `probabilidad_visitante` | `float` | Sí — mismos campos de `Engine03Salida`, recalculados sobre la matriz ya corregida |
| `top_marcadores` | `list[MarcadorProbabilidad]` (4 elementos) | Sí — mismo campo, mismo cálculo (`_top_marcadores`, sin cambios), aplicado sobre la matriz corregida |

**No se crea ningún tipo nuevo.** Toda la salida de Dixon-Coles cabe exactamente en la forma ya definida por `Engine03Salida` — es una condición de diseño, no una coincidencia (sección 6.4).

## 6.4 Qué modifica y qué no modifica (requisito 3 del brief)

| Pregunta | Respuesta | Por qué |
|---|---|---|
| ¿Modifica `λ`? | **No** | Dixon-Coles nunca toca `_calcular_lambda` — recibe `λ_local`/`λ_visitante` ya calculados, solo los usa como parámetros de `τ` (sección 6.3) |
| ¿Modifica las probabilidades (Local/Empate/Visitante)? | **Sí, cuando `ρ≠0`** | Redistribución de masa en 4 celdas + renormalización cambian la suma por diagonal (sección 6.5) |
| ¿Modifica la matriz? | **Sí, parcialmente** | Directamente en 4 de 64 celdas (`τ≠1`); el resto de la matriz solo cambia por el factor único de renormalización `1/Z` — su probabilidad *relativa* entre sí nunca cambia |
| ¿Modifica `Engine04` (código)? | **No** | Cero cambios de archivo — Engine04 sigue leyendo `engine03.probabilidad_local/empate/visitante` exactamente igual (sección 8.1) |
| ¿Modifica Confianza (`Engine05`, código o valor)? | **No, ninguno de los dos** | `Engine05` no lee ningún valor numérico de `Engine03Salida` — solo confirma que no es `None` (`models/confidence.md` §8, ya citado en `engine05.py`) — inmune por diseño previo a esta misión, no por un mecanismo nuevo (sección 8.2) |
| ¿Modifica EV (`Engine06`, código o valor)? | **Código: no. Valor: sí, cuando `ρ≠0`** | `Engine06` lee `probabilidad_local/empate/visitante` y `probabilidad_marcador` — mismos campos, valores más precisos (sección 8.3) |

## 6.5 Renormalización (requisito 5 del brief)

**Por qué la matriz deja de sumar 1.** La matriz Poisson cruda suma exactamente 1 porque es el producto de dos distribuciones marginales, cada una ya normalizada:

```
Σᵢⱼ P(i,j) = Σᵢⱼ P(X=i)·P(Y=j) = [Σᵢ P(X=i)] · [Σⱼ P(Y=j)] = 1 · 1 = 1
```

Al multiplicar únicamente 4 celdas por `τ(x,y)≠1` (dejando las 60 restantes, incluida la cola `"7+"`, en `τ=1`), la masa total ya no se conserva automáticamente:

```
Suma_corregida = Σ₍fuera de las 4 celdas₎ P(x,y)  +  Σ₍4 celdas₎ τ(x,y)·P(x,y)

              = [1 − Σ₍4 celdas₎ P(x,y)]  +  Σ₍4 celdas₎ τ(x,y)·P(x,y)

              = 1  +  Σ₍4 celdas₎ [τ(x,y) − 1] · P(x,y)
```

Si `ρ≠0`, al menos un `τ(x,y)≠1`, así que el término `Σ[τ(x,y)−1]·P(x,y)` es, en general, distinto de 0 → `Suma_corregida ≠ 1`. Esto no es un error del ajuste: es una consecuencia matemática necesaria de redistribuir masa de forma desigual — ya señalado, sin la demostración algebraica completa, en `models/poisson.md` §16.3.

**Cómo vuelve a sumar 1.** Renormalización estándar por división:

```
Z = Suma_corregida    (calculada sobre TODA la matriz, incluida "7+", tras aplicar τ)

P_final(x,y) = P_corregida(x,y) / Z    para toda celda (x,y)

⟹ Σ P_final(x,y) = Σ P_corregida(x,y) / Z = Suma_corregida / Z = Z / Z = 1
```

Válido siempre que `Z≠0` — condición garantizada dentro del rango estructural de `ρ` diseñado en la sección 7 (`τ(x,y)≥0` para las 4 celdas asegura que ninguna resta lleve la suma a valores no positivos).

**En qué momento ocurre.** Inmediatamente después de aplicar `τ` a las 4 celdas y **antes** de extraer `probabilidad_local`/`empate`/`visitante` y el Top 4 (sección 6.1, diagrama arquitectónico) — ningún consumidor, dentro o fuera de `Engine03`, ve jamás la matriz intermedia sin renormalizar. Esto restaura el invariante que `models/poisson.md` §8 ya exige ("la suma de todas las celdas de la matriz completa... es exactamente 1").

La celda de cola `"7+"` participa en la renormalización igual que cualquier otra celda (se divide por `Z`), aunque `τ("7+", ·) = 1` siempre — su valor absoluto cambia proporcionalmente, nunca su participación relativa frente al resto de celdas no corregidas directamente.

## 6.6 Diagrama resumen de compatibilidad (visual, complementa la sección 8)

```
                    ┌─────────────┐
  Engine01 ────────▶│             │
                    │             │
  Engine02 ────────▶│  Engine03   │──▶ Engine03Salida (SIN cambio de forma)
                    │  (Poisson   │        │
                    │  + Dixon-   │        ├──▶ Engine04  (código intacto)
                    │  Coles)     │        ├──▶ Engine05  (código intacto, inmune por diseño)
                    │             │        └──▶ Engine06  (código intacto)
                    └─────────────┘
```

---

# 7. Diseño del parámetro `ρ` (requisito 6 del brief)

| Atributo | Valor de diseño |
|---|---|
| **Tipo** | Escalar real (`float`), no vectorial, no por partido — un único valor global, mismo patrón que `KAPPA_LOCAL`/`KAPPA_VISITANTE`/`K_SHRINKAGE_VARIABLE003_004` |
| **Rango estructural (matemáticamente válido)** | El necesario para que `τ(x,y)≥0` en las 4 celdas: `τ(1,1)=1−ρ≥0 ⟹ ρ≤1`; `τ(0,0)=1−λμρ≥0 ⟹ ρ≤1/(λμ)` si `λμ>0`. Diseño conservador: clip estructural `ρ ∈ [−1, 1]`, mismo patrón de saturación dura ya usado para `λ_min`/`λ_max` (`models/poisson.md` §18) |
| **Rango empírico esperado (cita de literatura, no una decisión de esta misión)** | `ρ ∈ [−0.2, −0.1]` aproximadamente, valor de referencia original `ρ=−0.13` (Dixon y Coles, 1997, ya citado en `MODEL-019`/`models/poisson.md` §16.4) — se documenta como contexto, **no se fija como el rango permitido por el código** |
| **Valor inicial** | `ρ = 0.0` — mismo patrón exacto que `KAPPA_LOCAL = KAPPA_VISITANTE = 0.0`: la opción menos informativa posible, nunca "algo de corrección" sin evidencia propia del proyecto |
| **Significado físico** | Magnitud y dirección de la desviación de independencia entre los goles de ambos equipos, exclusivamente en marcadores bajos. `ρ<0` (único signo observado empíricamente en la literatura revisada, `MODEL-019` §16.4): ambos equipos se cuidan mutuamente en el marcador ajustado, produciendo más marcadores bajos/empates de los que predice la independencia total. `ρ>0` implicaría el efecto contrario — sin evidencia empírica de que ocurra en fútbol |
| **Cómo se calibraría (fuera de alcance de esta misión, solo referenciado)** | Máxima verosimilitud conjunta con los parámetros de ataque/defensa, sobre historial real (`MODEL-019` §16.4) — condicionado a evidencia propia suficiente en `data/results/`, misma condición ya aplicada a `KAPPA_LOCAL`/`KAPPA_VISITANTE`/`k` |

---

# 8. Compatibilidad hacia atrás y con `Engine04`-`06` (requisitos 7 y 8 del brief)

## 8.1 `ρ=0` reproduce exactamente el Modelo Santiago actual — demostración formal

```
ρ = 0
  ⟹ τ(0,0) = 1 − λ·μ·0 = 1
  ⟹ τ(0,1) = 1 + λ·0   = 1
  ⟹ τ(1,0) = 1 + μ·0   = 1
  ⟹ τ(1,1) = 1 − 0     = 1
  ⟹ τ(x,y) = 1  para las 60 celdas restantes (ya era 1 por definición, sección 6.3)

  ⟹ τ(x,y) = 1  para TODA celda (x,y) de la matriz completa

  ⟹ P_corregida(x,y) = 1 · P(X=x)·P(Y=y) = P(X=x)·P(Y=y)     (matriz idéntica a la cruda)

  ⟹ Z = Σ P_corregida(x,y) = Σ P(X=x)·P(Y=y) = 1              (sección 6.5 — la matriz cruda ya suma 1)

  ⟹ P_final(x,y) = P_corregida(x,y) / Z = P(x,y) / 1 = P(x,y) (idéntica a la matriz Poisson original)
```

Con `ρ=0`, la renormalización divide por `Z=1` — operación neutra. El paso completo `_aplicar_correccion_dixon_coles` + `_renormalizar_matriz` es, con `ρ=0`, la función identidad, demostrada algebraicamente término por término, no solo afirmada cualitativamente (extiende, con la prueba completa, lo ya afirmado en `models/poisson.md` §16.4: "generalización estricta, no un reemplazo").

## 8.2 Compatibilidad con Confianza (`Engine05`)

Inmune por diseño **preexistente**, no por un mecanismo nuevo de esta misión: `engine05.py` (líneas 55-67, ya citadas) documenta explícitamente que `Engine05` "no consume el valor numérico de `λ` ni de las probabilidades — solo necesita saber que Poisson pudo ejecutarse" (`models/confidence.md` §8). Verifica únicamente `context.engine.engine03 is not None`. Ningún valor que Dixon-Coles modifique (`λ`, probabilidades, matriz) es leído jamás por `Engine05` — compatibilidad total, con o sin `ρ≠0`, sin necesitar ningún cambio de código ni de diseño.

## 8.3 Compatibilidad con Valor Esperado (`Engine06`)

`Engine06._resolver_probabilidad_modelo` (`app/engine/engine06.py`, líneas 265-288, ya citadas) lee `engine03.probabilidad_local`/`empate`/`visitante` (mercado "Ganador del Partido") y recorre `engine03.probabilidad_marcador` buscando el marcador exacto (mercado "Marcador Exacto") — ambos, campos de `Engine03Salida`, tipo y nombre sin cambios (sección 6.3). Cuando `ρ=0`, los valores son idénticos a hoy (sección 8.1) — `Engine06` no distingue si Dixon-Coles está "activo" o no, porque no hay ninguna bandera nueva que leer, solo números potencialmente distintos dentro del mismo contrato. Cuando `ρ≠0`, `Engine06` sigue funcionando exactamente igual, con `P_modelo` más preciso — el propósito mismo de la corrección.

## 8.4 Compatibilidad con Bankroll y por qué el diseño respeta *append-only*

Bankroll (`docs/07-Bankroll.md`, futuro agente `bankroll-manager.md`) consume las recomendaciones de `Engine06`, dos niveles de indirección respecto a `Engine03` — ningún acoplamiento directo con la matriz Poisson ni con Dixon-Coles, compatible por la misma razón que `Engine06` (sección 8.3): la interfaz de `Engine06Salida` no cambia de forma.

**Por qué esto es posible sin ningún campo nuevo en `PredictionContext`:** el diseño (sección 6.1, diagrama arquitectónico) inserta Dixon-Coles **dentro** de `Engine03.ejecutar()`, antes de la única escritura de `context.engine.engine03`. `PredictionContext` es *append-only* (`docs/30`, `BUILD-004`: "ninguna sección ya escrita se reabre, recalcula ni elimina") — un diseño alternativo que escribiera primero la matriz cruda y luego la sobrescribiera con la corregida violaría ese principio. El diseño elegido nunca reabre nada: `context.engine.engine03` se publica **una única vez**, ya con la corrección incorporada. Es, precisamente, la razón por la que `Engine04`/`Engine05`/`Engine06` no requieren ningún cambio de código — no hay un campo nuevo que tengan que aprender a preferir.

## 8.5 Qué Engines permanecerán intactos (cierre obligatorio, adelantado aquí por ser parte de la prueba de compatibilidad)

`Engine01`, `Engine02`, `Engine04`, `Engine05` y `Engine06` — **los cinco, sin ningún cambio de código**. Solo `Engine03` se modifica (nuevos métodos privados, sección 10).

---

# 9. Impacto esperado (requisito 9 del brief)

Basado exclusivamente en evidencia ya aprobada (`MODEL-019` §16.5, `ANL-002`) — no se generan cifras nuevas, se proyecta la dirección esperada:

| Métrica | Impacto esperado | Justificación |
|---|---|---|
| **Recall de empates** | Mejora real, probablemente **insuficiente para cerrar la brecha completa** | `ANL-002`: ~70-80% del sesgo (17.9pp) es atribuible a independencia (lo que Dixon-Coles corrige); `MODEL-019` §16.4: `τ` está acotado (~13% en la celda 1-1 con `ρ≈-0.13`) — mejora en la dirección correcta, magnitud incierta sin calibración real |
| **Top-4 de marcadores** | Mejora esperada, más directa que en recall de empates | `VALID-003` ya documentó sobre-predicción de `1-0`/`0-1` y sub-predicción de `0-0`/`1-1` en el Top-4 — exactamente las 4 celdas que `τ` corrige, antes de la extracción del Top-4 (sección 6.1) |
| **Brier Score** | Mejora modesta esperada | Evidencia externa citada en `MODEL-019` §16.5 (RPS, familia de métrica análoga): mejora mínima pero consistente (0.1915→0.1914) cuando se aplica sin ponderación temporal adicional |
| **Log Loss** | Mejora modesta esperada, mismo razonamiento que Brier | Misma evidencia externa, misma familia de métrica de calibración probabilística |
| **Accuracy del ganador (L/E/V)** | Probablemente **sin cambio medible** | La redistribución de `τ` está concentrada en 4 celdas de baja probabilidad relativa; en partidos donde una clase ya domina claramente (`P>50%`), esa redistribución rara vez es suficiente para cambiar cuál de las 3 clases es la más probable |
| **MAE/RMSE de goles esperados** | **Sin cambio, por diseño** | Dependen exclusivamente de `λ_local`/`λ_visitante` (medias de las Poisson marginales) — Dixon-Coles nunca modifica `λ` (sección 6.4) |

---

# 10. Plan para la futura implementación (`IMP-003`) — requisito 10 del brief

**No se escribe código en esta misión.** Se especifica únicamente la superficie de cambio, para que `IMP-003` no tenga que tomar decisiones de diseño durante la escritura.

## 10.1 Módulos afectados

Únicamente `app/engine/engine03.py` — ningún otro archivo de `app/` (consistente con `MODEL-019` §16.8 y con el aislamiento demostrado en la sección 8).

## 10.2 Funciones nuevas (privadas de `Engine03`, mismo patrón que `_ajuste_localia`/`_calcular_lambda`/`_distribucion_goles`/`_construir_matriz_conjunta`/`_top_marcadores` ya existentes)

| Función | Firma (solo tipos, sin cuerpo) | Responsabilidad |
|---|---|---|
| `_tau_dixon_coles` | `(x: int, y: int, lambda_local: float, lambda_visitante: float, rho: float) -> float` | Ecuación de la sección 6.3 — devuelve `1.0` para cualquier `(x,y)` fuera de las 4 celdas |
| `_aplicar_correccion_dixon_coles` | `(celdas: list[MarcadorProbabilidad], lambda_local: float, lambda_visitante: float, rho: float) -> list[MarcadorProbabilidad]` | Aplica `_tau_dixon_coles` a las celdas cuyo `marcador` sea `"0-0"`, `"1-0"`, `"0-1"` o `"1-1"` (misma convención de texto ya usada por `_construir_matriz_conjunta`) |
| `_renormalizar_matriz` | `(celdas: list[MarcadorProbabilidad]) -> list[MarcadorProbabilidad]` | Calcula `Z` (sección 6.5) y divide cada celda — función pura, reutilizable, sin conocimiento de Dixon-Coles específicamente (podría reutilizarse para cualquier futura corrección que redistribuya masa) |

## 10.3 Funciones reutilizadas sin ningún cambio de código

- `_calcular_lambda`, `_distribucion_goles`, `_ajuste_localia` — no requieren ninguna modificación (sección 6.4: Dixon-Coles no toca `λ`).
- `_top_marcadores` — mismo código exacto; cambia únicamente el argumento que recibe desde `ejecutar()` (la matriz ya corregida/renormalizada en vez de la cruda).
- La lógica de clasificación Local/Empate/Visitante (hoy dentro de `_construir_matriz_conjunta`) — se reutiliza aplicándose sobre la matriz ya corregida; si conviene extraerla a un método propio reutilizable en dos momentos (cruda y corregida) es una decisión de estilo de `IMP-003`, no de este diseño.

## 10.4 Orden de implementación sugerido

1. Declarar `RHO_DIXON_COLES = 0.0` como constante simbólica, misma ubicación/estilo que `KAPPA_LOCAL`/`KAPPA_VISITANTE`/`LAMBDA_MIN`/`LAMBDA_MAX`.
2. Implementar `_tau_dixon_coles` (función pura, testeable de forma aislada).
3. Implementar `_aplicar_correccion_dixon_coles` (usa `_tau_dixon_coles`).
4. Implementar `_renormalizar_matriz` (función pura).
5. Insertar ambas llamadas, en ese orden, dentro de `ejecutar()`, entre `_construir_matriz_conjunta` y la extracción de `top_marcadores`/`probabilidad_local`/`empate`/`visitante` (sección 6.1).
6. **Validación de regresión obligatoria antes de cualquier otra cosa:** con `RHO_DIXON_COLES = 0.0`, reejecutar el mismo harness de `VALID-003`/`ANL-002` y confirmar resultados byte a byte idénticos a los ya publicados (mismo patrón de verificación "`diff` sin diferencias" ya usado en `FIX-001`/`FIX-002`).
7. Solo entonces, y solo con aprobación explícita del Arquitecto Estadístico Humano (Constitución, Art. 2/5), calibrar `ρ` con evidencia real — nunca en la misma misión que introduce la estructura (mismo patrón ya seguido por `IMP-002`, que fijó `k=5` sin calibrar, dejando la calibración para una misión futura).
8. Repetir el backtest de `VALID-003` con `ρ` calibrado y comparar métricas (misión `VALID-00X` futura), mismo patrón que `VALID-002` validó `IMP-002`.

---

# 11. Referencias

- `models/poisson.md` §16 (`MODEL-019`) — investigación completa de Dixon-Coles, evidencia bibliográfica y empírica, recomendación C. No se repite aquí.
- `models/poisson.md` §5-9 (`MODEL-003`) — Poisson independiente vigente, punto de partida de esta integración.
- `models/estabilizacion-muestras-pequenas.md` (`MODEL-017`/`MODEL-018`) — precedente de diseño matemático de un mecanismo nuevo (Shrinkage) como documento dedicado separado de la investigación de origen, patrón estructural reutilizado por este documento.
- `ANL-001` — diagnóstico original de separación excesiva de `λ`.
- `ANL-002` — descomposición cuantitativa del sesgo (≈20-30% atribuible a `λ`, ≈70-80% a independencia), evidencia que justifica directamente esta misión.
- `docs/30-Contrato-Oficial-del-Prediction-Context.md` (`BUILD-004`) — principio *append-only*, condición de diseño central de la sección 8.4.
- Dixon, M.J. y Coles, S.G. (1997) — ya citado en extenso en `models/poisson.md` §16.2/§14, no se repite.

---

# 12. Versión 2.0

Este documento **es** la Versión 2.0 de la integración Dixon-Coles (a diferencia de `models/poisson.md`, cuya sección 15 seguía marcando Dixon-Coles como "pendiente" tras solo la investigación de `MODEL-019`). Queda pendiente, explícitamente fuera de alcance de esta misión:

- Implementación real en `app/engine/engine03.py` (`IMP-003`, plan ya detallado en la sección 10).
- Calibración de `ρ` con evidencia real (condicionada a `data/results/` suficiente, y a aprobación explícita del Arquitecto Estadístico Humano).
- Validación empírica post-implementación (`VALID-00X`, mismo patrón que `VALID-002` para el Shrinkage).

---

# Cierre obligatorio

**1. ¿Dónde entra Dixon-Coles exactamente?**
Dentro de `Engine03.ejecutar()`, entre la construcción de la matriz Poisson cruda (`_construir_matriz_conjunta`, ya existente) y la extracción de `probabilidad_local`/`empate`/`visitante`/`top_marcadores` — nunca como un componente externo nuevo del `EngineRunner` (sección 6.1).

**2. ¿Qué recibe?**
`λ_local`, `λ_visitante` (ya calculados, sin cambios), la matriz Poisson cruda completa (64 celdas, incluida la cola `"7+"`), y `ρ` (sección 6.2).

**3. ¿Qué devuelve?**
Una matriz corregida y renormalizada de la misma forma exacta, más `probabilidad_local`/`empate`/`visitante` y `top_marcadores` recalculados — todo dentro del mismo tipo `Engine03Salida` ya existente, sin ningún campo nuevo (sección 6.3).

**4. ¿Qué modifica?**
La matriz de marcadores (4 celdas directamente, el resto por renormalización) y, en consecuencia, `probabilidad_local`/`empate`/`visitante`/`top_marcadores` — solo cuando `ρ≠0` (sección 6.4).

**5. ¿Qué no modifica?**
`λ_local`/`λ_visitante`, `Engine01`, `Engine02`, `Engine04`, `Engine05`, `Engine06` (código de ninguno de los cinco), `PredictionContext`, ninguna Variable Oficial, ningún peso ni CSV (sección 6.4, 8.5).

**6. ¿Cómo se renormaliza?**
Calculando `Z` = suma de la matriz completa tras aplicar `τ`, y dividiendo cada celda por `Z` — ocurre inmediatamente después de la corrección y antes de cualquier extracción de probabilidades o Top 4 (sección 6.5).

**7. ¿Cómo queda definido `ρ`?**
Escalar real, único y global, rango estructural `[−1,1]` con clip de seguridad, rango empírico esperado (no fijado) `[−0.2,−0.1]` según literatura, valor inicial `0.0` (sección 7).

**8. ¿`ρ=0` reproduce exactamente el modelo actual?**
Sí — demostrado algebraicamente término por término: con `ρ=0` todos los `τ(x,y)=1`, la matriz corregida es idéntica a la cruda, `Z=1`, y la renormalización es la división por 1 (sección 8.1).

**9. ¿Qué Engines permanecerán intactos?**
`Engine01`, `Engine02`, `Engine04`, `Engine05` y `Engine06` — los cinco, sin ningún cambio de código. Solo `Engine03` se modifica (sección 8.5, 10.1).

**10. ¿Está listo el proyecto para pasar a `IMP-003`?**
El **diseño** sí está completo y listo (ecuación definitiva, renormalización demostrada, contrato de entrada/salida especificado, compatibilidad demostrada formalmente, plan de módulos/funciones/orden ya detallado). La **calibración** de `ρ`, no — sigue condicionada a evidencia real en `data/results/` y a aprobación explícita del Arquitecto Estadístico Humano (Constitución, Art. 2/5), exactamente como para `κ_local`/`κ_visitante`/`k`. `IMP-003` puede iniciarse para implementar la **estructura** con `ρ=0` (paso 6 de la sección 10.4, validación de regresión obligatoria) — no para calibrar `ρ` en la misma misión.

---

Fin del documento.
