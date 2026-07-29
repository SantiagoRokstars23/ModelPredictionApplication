# Estabilización Estadística de Variable003, Variable004, Variable001 y Variable007 en Muestras Pequeñas

**Archivo:** `models/estabilizacion-muestras-pequenas.md`

**Misión:** MODEL-017 — Diseño del mecanismo de estabilización estadística para Variable003 y Variable004; ampliado por **MODEL-018** — Diseño matemático del mecanismo de Shrinkage para Variable003 y Variable004 (sección "Versión 2.0"); ampliado por **MODEL-021** — Investigación del Shrinkage para Variable001 (Forma Reciente) (sección 13); ampliado por **MODEL-022** — Investigación de la Variable007 (Fatiga) (sección 14)

**Versión:** 1.3.0-investigación

**Estado:** Investigación — comparación de mecanismos, recomendación única (MODEL-017) y formulación matemática definitiva lista para implementar (MODEL-018), ambas para Variable003/004. **MODEL-021** confirmó que Variable001 sufre un problema estructural emparentado pero no idéntico. **MODEL-022** investiga Variable007 (Fatiga) con el mismo rigor y llega a una conclusión **distinta de ambos casos anteriores**: con la evidencia real disponible hoy, Variable007 **no muestra** el mismo problema — su componente de z-score usa una población grande (tamaño real de torneo, no una pareja de equipos), su propagación hacia `λ` es lineal y no se satura dentro del rango probado, y sus correlaciones con error/Top-4/Accuracy son débiles. **No se recomienda Shrinkage para Variable007 con la evidencia actual.** **No implementable todavía como código**: ninguna fórmula, peso, CSV, Variable Oficial ni Engine fue modificado por ninguna de las cuatro misiones (fuera de alcance explícito de los cuatro briefs). La adopción de cualquier ecuación aquí formalizada requiere una futura misión de implementación, aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2/5).

---

# 1. Objetivo

Determinar, mediante análisis estadístico comparativo, cuál es el mecanismo óptimo para estabilizar Variable003 (Potencial Ofensivo) y Variable004 (Solidez Defensiva) cuando el tamaño de muestra (`N` partidos con estadísticas reales) es reducido — sin modificar todavía ninguna fórmula, peso ni código del proyecto. Este documento responde a la evidencia empírica producida por `CAL-004-Auditoría-de-Estabilidad-del-Z-Score` (`docs/00-Project-Tracker.md`), no la repite.

---

# 2. Descripción

`CAL-004` demostró, con prueba matemática exacta (no solo correlación), que el mecanismo actual de Variable003/004 — un z-score `Z = Σvᵢ·zᵢ` transformado por `Φ` (`models/offensive-strength.md` §21, `models/defensive-strength.md` §15) — **degenera** cuando la población de comparación es mínima: con `N=1` (población de 2 equipos), la desviación estándar de la población es siempre exactamente `|A−B|/2`, forzando a cualquier z-score a colapsar a `±1` exacto, sin importar la magnitud real de la diferencia entre los dos equipos. Verificado con 5 equipos reales completamente distintos (Chile, Perú, Costa Rica, Suecia, Ucrania) que producen el mismo valor final (`P=11.03356809599234`) pese a tener estadísticas crudas muy distintas entre sí. Además, incluso con `N≈10` (España, Francia, Inglaterra, Argentina), algunos equipos (Inglaterra) muestran oscilaciones de hasta 19 puntos entre ventanas de tamaño similar — el problema no se limita a `N=1`.

Este documento investiga, sin implementar, qué mecanismo estadístico debería reemplazar o complementar el z-score puro para que Variable003/004 sean confiables independientemente del tamaño de muestra disponible por equipo/competición.

---

# 3. Problema que resuelve

El z-score puro asume, implícitamente, que la población de comparación es lo bastante grande para que la media y la desviación estándar estimadas sean representativas de la verdadera distribución de la métrica en esa competición. Cuando `N` es pequeño (la situación real y predominante hoy: 16 de 32 combinaciones equipo/competición tienen exactamente `N=1`, `CAL-004`), esa asunción es falsa, y el z-score deja de medir "cuán bueno es este equipo" para medir, en el caso extremo, únicamente "quién ganó el único partido disponible" — información binaria disfrazada de una escala continua 0-100. Este documento busca un mecanismo que:

- Trate una muestra de `N=1` con la humildad estadística correspondiente (acercar el resultado a un valor neutro/poblacional, no a un extremo).
- Reduzca gradualmente esa humildad a medida que `N` crece, sin una discontinuidad abrupta.
- Preserve, para equipos con historial amplio (`N` grande), un comportamiento equivalente o muy cercano al z-score actual, evitando distorsionar innecesariamente el caso donde el z-score ya funciona razonablemente bien.

---

# 4. Comparación de mecanismos

Se evaluaron 7 técnicas, cada una documentada con los 9 criterios exigidos por el brief.

## 4.1 Mínimo de N antes de calcular la Variable

**Fundamento matemático:** ninguno propio — es una regla de decisión (umbral), no un estimador. Si `N < N_mín`, la Variable se marca `disponible=False` en vez de calcularse.

**Ventajas:** trivial de implementar; cero distorsión del valor cuando sí se calcula (el z-score, si se publica, es el mismo de siempre); perfectamente interpretable y auditable (una regla binaria, sin parámetros ocultos).

**Desventajas:** no resuelve nada para `N` por encima del umbral — la evidencia de `CAL-004` muestra que incluso `N≈10` (Inglaterra) sigue siendo volátil, por lo que un umbral razonable (`N_mín=5`, por ejemplo) dejaría el problema de fondo intacto para la mayoría de los casos reales; desperdicia información parcial (un equipo con `N=3` legítimamente informativo queda descartado por completo); introduce un "precipicio" de disponibilidad (de `disponible=False` a `disponible=True` sin transición), lo que ya se ha documentado como un patrón a evitar en otras Variables del proyecto (`docs/06`, "manejo de errores").

**Facilidad de implementación:** máxima (una comparación numérica).

**Coste computacional:** nulo.

**Interpretabilidad:** máxima.

**Comportamiento N=1:** `disponible=False` — evita la degeneración por completo, pero al costo de no producir ningún valor.

**Comportamiento N≈5:** depende del umbral elegido; si `N_mín≤5`, el valor se calcula igual de "crudo" que hoy, sin ninguna mejora sobre la volatilidad ya demostrada.

**Comportamiento N≈10:** sin cambio respecto al comportamiento actual — el caso de Inglaterra en `CAL-004` seguiría igual de volátil.

**Comportamiento N grande:** sin cambio — nunca fue el problema.

## 4.2 Shrinkage hacia la media de la competición

**Fundamento matemático:** estimador combinado `P_final = w(N)·P_crudo + (1−w(N))·μ_competición`, con `w(N) = N/(N+k)` — una media ponderada entre el valor crudo (z-score actual) y la media de la competición, donde `k` es una constante que representa "cuántos partidos equivalentes de evidencia" se necesitan para confiar plenamente en el valor propio del equipo. Es la forma más simple de la familia de estimadores de contracción ("shrinkage estimators").

**Ventajas:** resuelve directamente ambos hallazgos de `CAL-004` — en `N=1`, `w(1)=1/(1+k)` es pequeño, por lo que el resultado queda dominado por la media de la competición (nunca un extremo arbitrario); en `N≈10`, si `k` es moderado (ej. `k=5`), `w(10)≈0.67`, suavizando sin eliminar la señal propia del equipo. Extremadamente simple de explicar ("cuando hay poca evidencia, nos apoyamos más en el promedio de la competición") — coherente con el principio de auditabilidad de la Constitución del proyecto. No requiere estimar ningún parámetro adicional a partir de los datos: `k` puede fijarse como una constante estructural documentada (igual que `DELTA_MAX`/`PEN_MAX` ya lo son hoy en `engine/01`/`02`), sin violar "nunca alterar pesos sin evidencia estadística" siempre que se documente como estructural, no calibrado.

**Desventajas:** introduce una constante nueva (`k`) cuyo valor concreto, aunque razonable, no está calibrado con evidencia real todavía (mismo estatus que `KAPPA_LOCAL`/`DELTA_MAX` hoy); no es la solución "óptima" en sentido estadístico estricto (ese lugar lo ocupan Empirical Bayes/James-Stein, sección 4.3/4.6), solo una aproximación razonable y barata.

**Facilidad de implementación:** alta — una función adicional de una línea sobre el resultado ya calculado por `_aplicar_formula_potencial_ofensivo`/`_aplicar_formula_solidez_defensiva`, sin tocar el resto de la fórmula.

**Coste computacional:** despreciable — un cálculo aritmético adicional por Variable, reutilizando la media de la competición que el propio repositorio ya calcula (`poblacion_competicion`).

**Interpretabilidad:** alta — una media ponderada es uno de los conceptos estadísticos más fácilmente auditables que existen.

**Comportamiento N=1:** fuerte contracción hacia la media de la competición — el valor final ya no depende casi exclusivamente del resultado de un único partido; los 5 equipos del ejemplo de `CAL-004` (Chile, Perú, Costa Rica, Suecia, Ucrania) dejarían de compartir el mismo valor exacto en la práctica (la media de competición a la que se contraen es distinta entre Eurocopa y Copa América), aunque seguirían todos cerca de esa media respectiva — comportamiento correcto, no un defecto.

**Comportamiento N≈5:** contracción moderada — atenúa parcialmente la volatilidad sin eliminar la señal propia del equipo.

**Comportamiento N≈10:** contracción leve — el resultado se acerca bastante al z-score crudo actual, pero con un margen de suavizado que debería reducir (no necesariamente eliminar) la oscilación de 19 puntos observada en Inglaterra.

**Comportamiento N grande:** `w(N)→1` — converge al z-score puro, exactamente el comportamiento deseado (no distorsiona el caso donde el mecanismo actual ya es razonable).

## 4.3 Empirical Bayes

**Fundamento matemático:** generalización rigurosa del shrinkage (4.2) en la que el peso de contracción no se fija arbitrariamente (`k`), sino que se **estima a partir de los propios datos**, comparando la varianza entre equipos (`τ²`, cuánto varía la verdadera calidad ofensiva entre selecciones) contra la varianza dentro de cada equipo (`σ²/N`, el ruido de muestreo). El peso óptimo resultante es matemáticamente `w = τ²/(τ² + σ²/N)` — la misma forma funcional que el shrinkage simple, pero con `k = σ²/τ²` derivado de los datos, no supuesto. Esta es exactamente la metodología ya usada en investigaciones publicadas sobre fuerza de selecciones nacionales de fútbol con muestras pequeñas (ver Referencias).

**Ventajas:** teóricamente superior al shrinkage simple — el peso de contracción refleja la variabilidad real observada en la competición, no una constante elegida a mano; se adapta automáticamente si la varianza real entre equipos cambia con el tiempo (ej. si una competición se vuelve más pareja).

**Desventajas:** requiere una cantidad razonable de observaciones para estimar `τ²`/`σ²` de forma estable — con solo 32 combinaciones equipo/competición en todo el módulo hoy (`CAL-004`), y con más de la mitad de ellas en `N=1`, la propia estimación de `τ²` podría ser inestable en esta etapa temprana del proyecto (un problema de muestra pequeña aplicado, irónicamente, a la estimación del mecanismo que corrige la muestra pequeña); más compleja de auditar y explicar que el shrinkage simple, al introducir una etapa de estimación de varianza que debe recalcularse periódicamente.

**Facilidad de implementación:** media — requiere, además del cálculo de contracción, una rutina que estime `τ²`/`σ²` a partir de la población completa de equipos de la competición.

**Coste computacional:** bajo, pero mayor que el shrinkage simple (un paso de estimación adicional, ejecutable una vez por competición, no por partido).

**Interpretabilidad:** media — el resultado final sigue siendo una media ponderada (fácil de explicar), pero el peso ya no es una constante citable directamente, sino el resultado de un cálculo estadístico adicional.

**Comportamiento N=1/N≈5/N≈10/N grande:** cualitativamente igual al shrinkage simple (sección 4.2), pero con el peso `w(N)` ajustado automáticamente según la varianza real de cada competición, en vez de un `k` fijo.

## 4.4 Bayesian Prior (completo, con distribución explícita)

**Fundamento matemático:** especificar una distribución previa completa para el "verdadero" Potencial Ofensivo de cada equipo (ej. `Normal(50, 15²)` u otra), y combinarla formalmente con la verosimilitud de los datos observados vía el teorema de Bayes, produciendo una distribución posterior completa (no solo un punto).

**Ventajas:** el más flexible y rico de todos — permite incorporar conocimiento previo explícito (ej. "las selecciones europeas top suelen rondar tal rango") y produce, además de un punto estimado, una medida de incertidumbre completa (un intervalo creíble), útil en principio para alimentar `Engine05` (Confianza).

**Desventajas:** exige elegir una distribución previa concreta con parámetros específicos — hacerlo sin evidencia estadística que los respalde entraría en tensión directa con "nunca alterar pesos sin evidencia estadística" (`CLAUDE.md`), y hacerlo con evidencia insuficiente (32 observaciones totales) sería prematuro; la complejidad de implementación, auditoría y explicación a un no-estadístico es sustancialmente mayor que cualquier alternativa de esta lista, sin que el proyecto haya demostrado necesitar esa complejidad todavía (`CLAUDE.md`: "si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse").

**Facilidad de implementación:** baja — requiere, como mínimo, resolver un modelo conjugado cerrado (si la elección de distribuciones lo permite) o un método numérico (ej. muestreo) en caso contrario.

**Coste computacional:** bajo si el modelo es conjugado (fórmula cerrada); potencialmente alto si se requiere muestreo.

**Interpretabilidad:** baja para audiencias no estadísticas, pese a ser rigurosa — el propio texto exige explicar qué es una distribución previa y por qué se eligió esa forma concreta.

**Comportamiento N=1/N≈5/N≈10/N grande:** cualitativamente análogo al shrinkage (el prior domina en `N` pequeño, los datos dominan en `N` grande), pero con una curva de transición que depende de la forma exacta de la distribución elegida, no de una fórmula tan simple como `N/(N+k)`.

## 4.5 Laplace Smoothing

**Fundamento matemático:** suavizado aditivo clásico para estimaciones de frecuencia/probabilidad a partir de conteos discretos (`(k+α)/(n+α·d)`), diseñado para evitar probabilidades de 0 o 1 en variables categóricas (ej. clasificadores Naive Bayes).

**Ventajas:** extremadamente simple y bien entendido en el caso para el que fue diseñado.

**Desventajas — descarte inmediato:** Variable003/004 no son conteos ni probabilidades categóricas — son transformaciones de métricas continuas (`xG`, disparos) vía z-score. Laplace Smoothing no tiene una forma natural de aplicarse a este tipo de dato sin forzar una reformulación artificial del problema como si fuera un conteo, lo que no refleja la estructura real de la fórmula ya vigente (`models/offensive-strength.md` §21). Es un desajuste técnico de origen, no una cuestión de grado.

**Facilidad de implementación / coste / interpretabilidad / comportamiento por N:** no aplica — se descarta antes de llegar a evaluarse en estos términos, precisamente porque no es la herramienta correcta para este tipo de dato.

## 4.6 James–Stein Estimator

**Fundamento matemático:** caso particular, formalmente derivado y con demostración de optimalidad (bajo pérdida cuadrática, para 3 o más grupos estimados simultáneamente), de la misma familia de estimadores de contracción: `θ̂_JS = ȳ + (1 − (k−3)·σ²/S)·(y_i − ȳ)`, donde `ȳ` es la media global, `S` la suma de desviaciones cuadradas entre los `k` grupos y `σ²` la varianza de muestreo (asumida conocida u homogénea entre grupos). Es, históricamente, **el ejemplo canónico de esta familia de técnicas aplicado a estadísticas deportivas**: Efron y Morris (1977) lo demostraron con los promedios de bateo de 18 jugadores de béisbol en 1970, mostrando un error cuadrático total menos de un tercio del estimador ingenuo, superando al promedio observado en 16 de los 18 casos (ver Referencias).

**Ventajas:** respaldo teórico más fuerte de toda la lista — garantía formal de dominancia frente al z-score puro cuando se estiman múltiples equipos a la vez (exactamente la situación de Variable003/004, con 32 combinaciones equipo/competición simultáneas); precedente directo y específico en estadística deportiva.

**Desventajas:** la forma clásica asume varianza de muestreo homogénea entre grupos (`σ²` igual para todos los equipos) — en este proyecto, cada equipo tiene un `N` distinto (1 a 13), por lo que la varianza de muestreo real **no** es homogénea, exigiendo una variante del estimador (James-Stein con varianzas desiguales) más compleja que la versión de manual; en la práctica, esa variante termina siendo matemáticamente muy cercana al shrinkage ponderado por `N` de la sección 4.2/4.3, sin una ventaja decisiva adicional para este caso concreto.

**Facilidad de implementación:** media — la versión con varianzas desiguales no es tan simple como la fórmula clásica de manual.

**Coste computacional:** bajo, cerrado (no iterativo).

**Interpretabilidad:** media — el resultado final vuelve a ser una contracción hacia una media global, pero la derivación formal (por qué ese factor de contracción específico es óptimo) es más avanzada de explicar que el shrinkage simple.

**Comportamiento N=1/N≈5/N≈10/N grande:** cualitativamente igual al shrinkage (sección 4.2), con el factor de contracción derivado formalmente en vez de elegido por conveniencia — la ventaja teórica es real, pero la variante que este proyecto necesitaría (varianzas desiguales) reduce la simplicidad que hace atractivo a James-Stein en su forma clásica.

## 4.7 Regularización mediante media móvil

**Fundamento matemático:** ponderar los partidos más recientes más que los antiguos (ej. media móvil exponencial), suavizando la serie temporal de un equipo.

**Ventajas:** útil para el problema de **recencia** (¿debe pesar más el partido de ayer que el de hace un año?).

**Desventajas — no ataca el problema de esta misión:** la media móvil suaviza *a lo largo del tiempo dentro del propio equipo*, pero no resuelve la degeneración de `CAL-004`, que ocurre quirúrgicamente cuando la **población de comparación** (no la serie temporal de un solo equipo) es minúscula. Con `N=1`, no existe "serie" que suavizar — el problema persiste igual. Es una técnica que responde a una pregunta distinta y complementaria (recencia), no a la que plantea esta misión (estabilidad con muestra pequeña).

**Facilidad de implementación / coste / interpretabilidad / comportamiento por N:** no se evalúa en profundidad por no atacar la causa raíz identificada en `CAL-004` — queda documentada como técnica válida para un problema diferente, no como candidata aquí.

---

# 5. Ventajas (de la técnica recomendada, adelanto — ver sección 6)

El shrinkage simple hacia la media de la competición (sección 4.2) ofrece el mejor equilibrio entre resolver ambos hallazgos de `CAL-004`, mantenerse dentro de la complejidad que el proyecto puede auditar y calibrar hoy, y no introducir una dependencia de un volumen de datos que el proyecto todavía no tiene (32 observaciones totales).

---

# 6. Limitaciones

Ninguna de las 7 técnicas comparadas es "gratuita": todas introducen, como mínimo, una constante o un supuesto adicional que no estaba en el z-score original. El shrinkage simple no es la opción teóricamente óptima (ese lugar lo ocupan Empirical Bayes o James-Stein con varianzas desiguales) — es la opción **más defendible dado el volumen de datos actual del proyecto**. Si en el futuro el módulo de Selecciones Nacionales acumula muchas más observaciones por competición, la limitación práctica de Empirical Bayes (estimar `τ²`/`σ²` de forma estable) dejaría de aplicar, y una futura misión debería reevaluar si migrar de shrinkage simple a Empirical Bayes — no un fracaso del análisis, sino la consecuencia esperable de un proyecto que declara explícitamente el "Principio de Desarrollo Incremental" (`CLAUDE.md`).

---

# 7. Aplicación dentro del Modelo Santiago

**Recomendación oficial única: Shrinkage hacia la media de la competición (sección 4.2).**

Justificación, respondiendo directamente a los criterios de aceptación del brief:

- **Mejor equilibrio estabilidad/interpretabilidad:** resuelve ambos hallazgos de `CAL-004` (degeneración en `N=1`, volatilidad en `N≈10`) con una fórmula que cualquier lector de este documento puede verificar a mano (`P_final = w·P_crudo + (1−w)·μ_competición`), sin requerir estimar parámetros adicionales a partir de datos todavía escasos.
- **Más sencilla de implementar:** de las técnicas que sí resuelven el problema (excluye Mínimo de N, que no lo resuelve del todo, y Laplace Smoothing, que no aplica), es la de menor esfuerzo — una función adicional sobre un valor ya calculado, reutilizando datos que el repositorio ya expone (`poblacion_competicion`).
- **Menor sesgo en muestras pequeñas:** en `N=1`, contrae fuertemente hacia la media de la competición — exactamente el comportamiento correcto dado que, per `CAL-004`, el z-score en `N=1` no contiene información fiable más allá de un patrón ordinal de 3 bits.
- **Conserva mejor el comportamiento en `N` grande:** `w(N)→1` cuando `N` crece, convergiendo al z-score puro — no penaliza a España o Francia, cuyos valores en `N≈10-13` ya se comportaron razonablemente en `CAL-004`.
- **Uso en modelos deportivos modernos:** esta misma familia de técnicas (contracción hacia una media global) es la empleada explícitamente en investigaciones publicadas sobre fuerza de selecciones nacionales de fútbol con datos escasos, y es el mismo principio, con validación empírica clásica en deporte, del estimador James-Stein (Efron y Morris, 1977) — el Modelo Santiago adoptaría la versión más simple de una familia con precedente sólido, no una técnica improvisada.

Se descartan explícitamente como recomendación principal: **Laplace Smoothing** (desajuste técnico de origen, no aplica a datos continuos); **Bayesian Prior completo** (complejidad no justificada por el volumen de datos actual, riesgo de elegir parámetros de prior sin evidencia); **Regularización por media móvil** (resuelve un problema distinto — recencia, no tamaño de muestra); **Mínimo de N como único mecanismo** (no resuelve la volatilidad ya demostrada en `N≈10`); **Empirical Bayes y James-Stein** quedan como la ruta de mejora natural **futura**, no la recomendación de esta misión, precisamente por depender de una estimación de varianza que el volumen de datos actual (32 observaciones) no sostiene todavía con solidez.

**Impacto esperado sobre Variable003/004, si se implementara en una misión futura:** el valor numérico de ambas Variables cambiaría para todo equipo con `N` por debajo del máximo real (13) — de forma más notoria para los 16 equipos con `N=1` (que dejarían de tomar valores extremos idénticos entre equipos completamente distintos) y de forma más leve para España/Francia/Argentina (`N` ya relativamente alto). Esto **no es una recalibración de pesos** en el sentido de `CAL-002`/`CAL-004` (no toca `PESO_METRICA_POTENCIAL_OFENSIVO`, `KAPPA_LOCAL`/`KAPPA_VISITANTE` ni ninguna fórmula ya vigente) — es una capa adicional aplicada **después** del z-score ya calculado, por lo que no contradice ninguna conclusión de `CAL-002` (los pesos internos de Variable003/004 seguirían siendo, correctamente, inertes como ya se demostró) ni de `CAL-004`.

---

# 8. Referencias

- Efron, B. y Morris, C. (1977). "Stein's Paradox in Statistics." *Scientific American*, 236(5), 119-127 — el ejemplo original de contracción de James-Stein aplicado a promedios de bateo de béisbol (18 jugadores, temporada 1970), demostrando un error cuadrático total menos de un tercio del estimador ingenuo.
- Investigación aplicada sobre fuerza de selecciones nacionales de fútbol con datos escasos mediante metodología de Empirical Bayes (contracción hacia una media global cuando el número de partidos disponibles es pequeño) — mismo dominio exacto de este proyecto (selecciones nacionales, muestras pequeñas por competición).
- `docs/00-Project-Tracker.md`, entrada `CAL-004` — evidencia empírica exacta que origina esta investigación (degeneración matemática en `N=1`, volatilidad en `N≈10`), no repetida aquí.
- `models/offensive-strength.md` §17-27 (`MODEL-009`), `models/defensive-strength.md` §13-21 (`MODEL-010`) — especificación vigente del z-score que esta investigación busca complementar, no reemplazar en su estructura interna.
- `CLAUDE.md` — "Nunca alterar pesos sin evidencia estadística", "Principio de Desarrollo Incremental", "Si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse" — criterios aplicados explícitamente en la sección 7 para descartar Bayesian Prior/Empirical Bayes/James-Stein como recomendación inmediata.

---

# Versión 2.0 — Formulación matemática definitiva (MODEL-018)

## 9. Decisión de diseño previa: ¿sobre qué variable se aplica la contracción?

Antes de comparar formulaciones, es necesario resolver una ambigüedad que ninguna de las opciones del brief especifica por sí sola: la fórmula vigente (`models/offensive-strength.md` §21, `models/defensive-strema.md` §15) no produce directamente un percentil `P`, sino un z-score combinado `Z* = Z/s` (con `Z = Σvᵢ·zᵢ`, `s=√(Σvᵢ²)`), que **luego** se transforma en `P = 100·Φ(Z*)`.

Contraer sobre `P` (el percentil final, acotado 0-100) en vez de sobre `Z*` (el z-score combinado, no acotado) introduciría una distorsión: `Φ` es una transformación **no lineal**, por lo que promediar dos percentiles ya transformados no es matemáticamente equivalente a promediar los z-scores subyacentes y transformar una sola vez el resultado — el orden de las operaciones importa, y solo una de las dos secuencias es correcta desde el punto de vista de la teoría de estimación (el z-score es la cantidad con una varianza de muestreo bien definida y aproximadamente aditiva; el percentil es una función acotada y comprimida en los extremos de esa cantidad).

**Decisión de diseño, aplicable a las 4 opciones comparadas:** la contracción se aplica sobre `Z*` (antes de `Φ`), nunca sobre `P` (después de `Φ`). `Φ` se aplica una única vez, al final, sobre el `Z*` ya contraído. Esta decisión no es una quinta opción a comparar — es una precondición matemática compartida por todas, y se documenta aquí explícitamente porque ninguna búsqueda bibliográfica sobre "shrinkage" en general la resuelve por sí sola; depende de la estructura interna específica ya vigente en este proyecto.

Consecuencia directa: el término "Media de la competición" (`μ_competición`) de todas las fórmulas siguientes se refiere a la **media histórica de `Z*`** de todos los equipos ya evaluados en esa `id_competicion` — equivalentemente, `Φ⁻¹(P̄_competición / 100)`, usando la media empírica de `P` ya medida por `CAL-004` (Variable003: media agregada `P̄=36.32`; Variable004: `P̄=33.17`; **ambas distintas de 50 y distintas entre Eurocopa y Copa América**, evidencia ya documentada, no un supuesto nuevo). No es cero: un z-score individual tiene media 0 dentro de su propio cálculo poblacional (2 equipos comparados), pero la media histórica de esos z-scores **agregados a través de muchos partidos y equipos** no tiene por qué ser 0, y la evidencia de `CAL-004` confirma que no lo es.

## 10. Comparación de las 4 formulaciones

### Opción A — Shrinkage lineal simple (ya recomendada en `MODEL-017`)

**Ecuación completa:**

```
w(N) = N / (N + k)
Z*_final = w(N)·Z*_equipo + (1 − w(N))·Z*_competición
P_final = 100·Φ(Z*_final)
```

**Significado de cada parámetro:** `N` = número real de partidos con estadística disponible para ese equipo en esa competición (ya expuesto por `obtener_metricas_ofensivas`/`obtener_metricas_defensivas`); `Z*_equipo` = z-score combinado ya calculado hoy con la fórmula vigente; `Z*_competición` = media histórica de `Z*` en esa competición (sección 9); `k` = constante fija, elegida por el analista, que representa "cuántos partidos de evidencia propia equivalen a la confianza depositada en la media de la competición" (desarrollado en la sección 11).

**Ventajas:** una sola constante libre (`k`), calculable con una división y una suma; totalmente auditable a mano; no requiere estimar nada a partir de los datos (a diferencia de C); es exactamente el caso límite de B cuando `σ²`/`τ²` se tratan como constantes fijas, no estimadas — es decir, A es un caso particular, no una alternativa desconectada de B.

**Inconvenientes:** asume que `k` (equivalente a `σ²/τ²`, ver Opción B) es el mismo para todos los equipos y todas las competiciones — no distingue si una competición en particular es más o menos homogénea que otra en su varianza real entre equipos.

**Facilidad de implementación:** máxima de las 4 — una función pura de `N`, `Z*_equipo` y `Z*_competición`, sin estado ni estimación.

**Comportamiento por `N`** (con `k=5`, valor de referencia — ver sección 11): `N=1`: `w=1/6≈0.167` (fuerte contracción, ~83% del valor final proviene de la media de la competición); `N=3`: `w=3/8=0.375`; `N=5`: `w=5/10=0.5` (punto exacto de "mitad evidencia propia, mitad media de competición" — de ahí el nombre técnico de `k` como "punto de estabilización", sección 11); `N=10`: `w=10/15≈0.667`; `N=20`: `w=20/25=0.8`; `N→∞`: `w→1`, `Z*_final→Z*_equipo` (converge exactamente al z-score puro ya vigente, sin distorsión residual).

### Opción B — Shrinkage por precisión (precision weighting)

**Ecuación completa:**

```
precisión_equipo = N / σ²
precisión_prior = 1 / τ²
Z*_final = (precisión_equipo · Z*_equipo + precisión_prior · Z*_competición) / (precisión_equipo + precisión_prior)
P_final = 100·Φ(Z*_final)
```

**Significado de cada parámetro:** `σ²` = varianza de muestreo dentro de un equipo (cuánto varía el z-score de partido a partido para el mismo equipo — ruido); `τ²` = varianza real entre equipos de la competición (cuánto difieren genuinamente los equipos entre sí — señal); `precisión` = inverso de una varianza, cantidad que se sabe formalmente que se **suma** al combinar dos estimaciones independientes (resultado estándar de combinación de estimadores gaussianos independientes). Álgebra directa: si se define `k = σ²/τ²`, esta ecuación se reduce exactamente a la Opción A con `w(N)=N/(N+k)` — B es la derivación formal de la que A es la instancia práctica.

**Ventajas:** hace explícito qué representa matemáticamente `k` (una razón de varianzas, no una constante arbitraria); permite, en principio, que `σ²` varíe por competición si hubiera evidencia de que una es más ruidosa que otra (heterocedasticidad entre competiciones, no solo entre equipos por distinto `N`).

**Inconvenientes:** exige fijar (o estimar) dos cantidades (`σ²` y `τ²`) en vez de una sola (`k`) — si ambas se fijan como constantes arbitrarias sin evidencia, no aporta ninguna ventaja práctica sobre A y solo añade una capa de indirección; si se estiman de los datos, deja de ser una fórmula fija y se convierte en la Opción C.

**Facilidad de implementación:** media — matemáticamente casi idéntica a A, pero requiere justificar dos constantes en vez de una, lo que introduce más superficie de discusión sin más precisión real si ambas se fijan a mano.

**Comportamiento por `N`:** idéntico, cifra por cifra, a la Opción A si se fija `k=σ²/τ²` con el mismo valor numérico — no hay ninguna diferencia de comportamiento entre A y B en la práctica de este proyecto salvo que se decida estimar `σ²`/`τ²` por separado, en cuyo caso B se convierte en C.

### Opción C — Shrinkage derivado de Empirical Bayes

**Ecuación completa:** misma forma funcional que B, pero con `σ̂²` y `τ̂²` **estimados a partir de los propios datos** de la competición (ej. `τ̂² = max(0, S²_entre_equipos − σ̂²/N̄)`, método de momentos estándar para modelos de efectos aleatorios), en vez de fijados por el analista.

**Ventajas:** ya identificadas en `MODEL-017` §4.3 — se adapta automáticamente a la varianza real observada en cada competición, sin necesidad de que un analista humano fije `k` a mano.

**Inconvenientes:** ya identificados en `MODEL-017` §4.3 y reconfirmados aquí — con 32 observaciones totales y más de la mitad de las combinaciones equipo/competición en `N=1`, estimar `τ̂²` de forma estable es, en sí mismo, un problema de muestra pequeña; un `τ̂²` mal estimado (ej. truncado a 0 por el término `max(0, ...)` cuando la varianza muestral entre equipos es baja por casualidad) puede producir una contracción total (`k→∞`, todos los equipos empujados a la media) o nula (`k→0`, sin contracción), sin que exista suficiente evidencia hoy para distinguir cuál de los dos extremos es el correcto.

**Facilidad de implementación:** baja en este momento del proyecto — no por complejidad algebraica (la fórmula de `τ̂²` es estándar), sino porque requiere una rutina adicional de estimación por competición, ejecutada sobre una base de datos todavía insuficiente para producir una estimación confiable.

**Comportamiento por `N`:** cualitativamente igual a A/B, pero el punto exacto de contracción (`k` efectivo) no es una constante conocida de antemano — varía según la competición y podría cambiar cada vez que se agreguen más partidos al dataset, complicando la reproducibilidad exacta de un valor de `P` calculado en dos momentos distintos del proyecto.

### Opción D — Actualización Bayesiana recursiva estilo Elo/Glicko

**Ecuación completa (forma general de un filtro de Kalman de un solo paso, la misma familia matemática que usan Glicko/TrueSkill):**

```
Ganancia_t = τ²_t / (τ²_t + σ²)
Z*_t = Z*_{t-1} + Ganancia_t · (z_partido_t − Z*_{t-1})
τ²_t = (1 − Ganancia_t) · τ²_{t-1}   (la incertidumbre se reduce con cada partido nuevo)
```

**Significado de cada parámetro:** en vez de recalcular `Z*` desde cero sobre una ventana fija de `N` partidos (como hace el diseño actual), esta familia mantiene una estimación `Z*_t` que se **actualiza partido a partido**, con una "ganancia" que depende de cuánta incertidumbre `τ²_t` queda acumulada (alta al inicio, cuando `N` es pequeño; decreciente con cada partido observado) frente al ruido de un único partido (`σ²`).

**Ventajas:** es el enfoque que efectivamente usan los sistemas de rating deportivo más conocidos (Elo, Glicko, TrueSkill) — máxima legitimidad de precedente en "modelos deportivos"; captura de forma natural la evolución temporal de la fuerza de un equipo (un partido de hace 3 años pesa menos que uno de la semana pasada), resolviendo *de paso* el problema de recencia que `MODEL-017` §4.7 identificó como fuera de alcance de la Opción A.

**Inconvenientes:** exige rediseñar la arquitectura de cálculo de Variable003/004 de "ventana fija recalculada" (diseño actual, `models/offensive-strength.md` §22) a "estado acumulado actualizado secuencialmente" — un cambio estructural mucho mayor que agregar una función de contracción sobre un resultado ya calculado; requiere procesar los partidos en **orden cronológico estricto** por equipo (el diseño actual no garantiza ni necesita ese orden para el cálculo de ventana fija); introduce un parámetro adicional (`τ²_0`, la incertidumbre inicial antes del primer partido) sin el cual la recursión no puede arrancar.

**Facilidad de implementación:** la más baja de las 4 — no es una función pura sobre el resultado ya calculado, sino un cambio de arquitectura del propio cálculo de la Variable.

**Comportamiento por `N`:** en régimen estacionario (muchos partidos, `τ²_t` ya pequeño), el comportamiento marginal por partido nuevo es equivalente al de A/B/C; pero el valor exacto en `N` pequeño depende del **orden** en que llegaron los partidos, no solo de cuántos hay — una diferencia cualitativa real frente a A/B/C, que son insensibles al orden.

## 11. El parámetro `k`

`k` representa, en la Opción A (la recomendada, sección 12), el **"punto de estabilización"**: el valor de `N` en el cual la evidencia propia del equipo y la media de la competición pesan exactamente lo mismo (`w(k)=0.5` por construcción, ya que `w(k)=k/(k+k)=0.5`). Equivalentemente (Opción B), `k=σ²/τ²`: la razón entre cuánto varía el resultado de un equipo de partido a partido (ruido) y cuánto varían genuinamente los equipos entre sí (señal) — un `k` alto significa que el ruido de muestreo domina y se necesita mucha evidencia propia antes de confiar en el valor individual; un `k` bajo significa que la señal entre equipos ya es fuerte y poca evidencia basta.

**No se elige un valor definitivo en esta misión** (fuera de alcance explícito del brief). Rango propuesto y qué implica cada extremo:

| `k` | Punto de estabilización | Implicación |
|---|---|---|
| `k≈3` | Con 3 partidos ya hay 50% de confianza propia | Contracción más suave — preserva más señal individual incluso en `N` bajo, pero deja el caso `N=1` todavía relativamente expuesto (`w(1)=1/4=25%` de peso propio, no despreciable dada la degeneración exacta demostrada en `CAL-004`) |
| `k≈5` | Con 5 partidos, mitad de la ventana completa actual (`N_máx=10`) | Punto medio razonable y fácil de justificar narrativamente ("se necesita la mitad de una ventana completa para confiar a medias en el valor propio"); en `N=1`, `w=1/6≈17%` — contracción fuerte, coherente con la severidad de la degeneración ya demostrada |
| `k≈8` | Casi toda la ventana completa necesaria para 50% de confianza | Contracción conservadora — incluso equipos con `N=10` (ventana llena) solo llegan a `w=10/18≈56%`, dejando siempre un peso considerable a la media de la competición; podría infravalorar equipos genuinamente distintos que ya acumularon una ventana completa de evidencia |
| `k≈10` | Se necesita una ventana llena completa para 50% de confianza | La más conservadora — equivale a decir que ni siquiera la ventana máxima diseñada (`N=10`) basta por sí sola para superar el 50% de peso propio (`w(10)=0.5` exacto); coherente solo si se cree que la varianza entre equipos (`τ²`) es genuinamente muy baja comparada con el ruido de muestreo — hipótesis no verificada todavía con los datos actuales |

**Recomendación de rango inicial: `k∈[5,8]`**, con `k=5` como valor de partida más defendible por dos razones documentadas, no por preferencia arbitraria: (1) es exactamente la mitad de `N_máx=10`, la ventana ya fijada por el diseño vigente (`VENTANA_PARTIDOS_POTENCIAL_OFENSIVO`/`VENTANA_PARTIDOS_SOLIDEZ_DEFENSIVA`), dándole una justificación estructural coherente con una constante ya existente en el proyecto, en vez de introducir un número sin relación con nada ya vigente; (2) produce una contracción fuerte en `N=1` (`w≈17%`) proporcional a la severidad ya demostrada por `CAL-004` (colapso exacto a `±1`, no una simple imprecisión menor). La calibración fina de `k` dentro de este rango, con evidencia real, queda explícitamente para una futura misión de calibración (no de diseño) — una vez exista suficiente volumen de datos para que esa calibración sea estadísticamente significativa.

## 12. Ecuación oficial propuesta

```
Z*_equipo         = Z / s                                   (ya vigente, sin cambios)
Z*_competición    = Φ⁻¹( P̄_competición / 100 )               (media histórica de Z*, por id_competicion)
w(N)              = N / (N + k)                              (k constante estructural documentada, k∈[5,8], k=5 recomendado como punto de partida)
Z*_final          = w(N) · Z*_equipo + (1 − w(N)) · Z*_competición
P_final           = 100 · Φ(Z*_final)
```

Es la Opción A, con la precondición de diseño de la sección 9 (contracción sobre `Z*`, no sobre `P`) incorporada explícitamente en la propia ecuación. Se elige por sobre B (matemáticamente equivalente, pero B introduce dos constantes en vez de una sin ninguna ventaja práctica salvo que se estimen de los datos), C (Empirical Bayes — teóricamente más fino, pero la estimación de `τ̂²`/`σ̂²` no es confiable con el volumen de datos actual, mismo hallazgo ya de `MODEL-017`) y D (Elo/Glicko recursivo — exige un cambio estructural del cálculo de la Variable, no solo una función de contracción sobre el resultado ya calculado, y depende del orden cronológico de los partidos, complejidad no justificada por la evidencia disponible hoy).

---

# Versión 2.0 — Estado y pendientes

Requiere, como mínimo, antes de poder implementarse como código:

- Decisión explícita del Arquitecto Estadístico Humano sobre si adoptar la ecuación aquí formalizada (Constitución, Art. 2/5 — no autoaprobable por el Arquitecto Estadístico IA).
- Elección final del valor de `k` dentro del rango `[5,8]` propuesto (o una futura calibración con más datos).
- Especificación operacional exacta (qué método expone `P̄_competición` por `id_competicion`, cómo se integra en `_aplicar_formula_potencial_ofensivo`/`_aplicar_formula_solidez_defensiva` sin modificar el z-score interno ya vigente) — tarea de una futura misión de implementación, no de esta.
- Revalidación mediante un nuevo backtest (mismo patrón que `VALID-001`/`CAL-002`) que confirme que el shrinkage mejora, y no solo cambia, las métricas ya medidas (Accuracy empate, Brier, Log Loss).

---

# Sección 13 — Investigación del Shrinkage para Variable001 (`MODEL-021`)

**Origen:** `ANL-003` midió que Variable001 (Forma Reciente) genera, en datos reales, una contribución a la separación `λ_local`−`λ_visitante` (`0.582` de media) comparable a la de Variable003 (`0.579`) y muy superior a Variable002 (`0.169`), **pese a compartir exactamente el mismo peso formal** (`W_FORMA_RECIENTE=W_RENDIMIENTO_TORNEO=0.5`) — un hallazgo que no se explica por el peso, y que motiva esta investigación: ¿Variable001 sufre el mismo problema estructural que `CAL-004` ya demostró para Variable003/004? Toda la evidencia de esta sección proviene de invocar directamente los repositorios y fórmulas ya existentes (`_FormaRecienteRepository`, `VariablePreparation._calcular_forma_reciente`/`_aplicar_formula_forma_reciente`) — solo lectura, ningún archivo modificado.

## 13.1 Anatomía de Variable001 (Parte 1) — sin reinterpretar, código citado literalmente

```
Fuente de datos:  partidos.csv (TODO el historial, cualquier torneo/competición —
                   "sin distinción de amistosos y competiciones", models/forma-
                   reciente.md §8; a diferencia de Variable003/004, no hay ningún
                   join contra torneos.csv/competiciones.csv)

Ventana:          N = VENTANA_PARTIDOS_FORMA_RECIENTE = 5 (últimos partidos
                   oficiales del equipo, orden cronológico descendente, luego
                   invertido a ascendente antes de usarse — preparation.py,
                   _FormaRecienteRepository.obtener_ultimos_partidos)

Transformación:   puntos_j = 3 (victoria) | 1 (empate) | 0 (derrota), sistema
                   estándar de fútbol -- por partido, sobre los goles reales

Normalización:    Forma_Reciente = 100 · (Σ puntos_j) / (3 · n)
                   n = partidos realmente encontrados (n ≤ N=5)

Punto de "percentil":  NO EXISTE. A diferencia de Variable003/004 (z-score
                   Z=Σvᵢ·zᵢ, transformado por Φ contra una población de equipos
                   de la misma competición), Variable001 es una PROPORCIÓN
                   DIRECTA de puntos sobre el máximo posible -- nunca se calcula
                   un z-score, nunca hay una población de comparación entre
                   equipos, nunca se invoca Φ. Ya acotada [0,100] por
                   construcción aritmética (models/forma-reciente.md §9).
```

**Diferencia estructural ya visible en la propia anatomía, antes de cualquier dato:** Variable003/004 comparan a un equipo **contra otros equipos de su misma competición** (de ahí que `CAL-004` hablara de "población de comparación" degenerada). Variable001 nunca compara a un equipo contra nadie más — es una estadística **intra-equipo pura** (su propio historial, sin referencia externa). Esto tiene una consecuencia directa para la Parte 6 (simulación): no existe, en el diseño actual, ningún "`Z*_competición`" ni "`μ_competición`" análogo hacia el cual contraer Variable001.

## 13.2 Distribución real (Parte 2) — 53 selecciones con Variable001 calculable (de 62 catalogadas)

| | Variable001 (hoy, sin estabilizar) | Variable003 (post-Shrinkage, `VALID-003`) | Variable003 (pre-Shrinkage, `CAL-004`, N=32) | Variable004 (post-Shrinkage) | Variable004 (pre-Shrinkage) |
|---|---|---|---|---|---|
| N observaciones | 53 | 35 | 32 | 35 | 32 |
| Media | 23.85 | 52.60 | 36.32 | 53.82 | 33.17 |
| Mediana | 16.67 | 48.10 | 31.69 | 58.78 | 23.98 |
| Desv. estándar | **28.57** | 17.73 | **27.18** | 16.14 | **28.50** |
| Mínimo | 0.00 | 21.94 | 3.02 | 18.35 | 2.06 |
| Máximo | 100.00 | 88.81 | 96.47 | 78.19 | 87.80 |
| P5 | 0.00 | — | — | — | — |
| P25 | 0.00 | — | — | — | — |
| P50 | 16.67 | — | — | — | — |
| P75 | 33.33 | — | — | — | — |
| P95 | 88.00 | — | — | — | — |

**Hallazgo directo:** la desviación estándar de Variable001 hoy (`28.57`) es prácticamente idéntica a la de Variable003/004 **antes** de que `IMP-002` aplicara el Shrinkage (`27.18`/`28.50`) — y sustancialmente mayor que ambas **después** del Shrinkage (`17.73`/`16.14`). Esto no demuestra por sí solo un problema (una desviación alta también podría reflejar diferencias reales entre selecciones) — la Parte 3 (dependencia con `N`) es la que distingue señal real de ruido de muestra pequeña.

## 13.3 Dependencia con N (Parte 3)

Sobre las mismas 53 selecciones, con `N` = partidos realmente encontrados (1 a 5):

- **Distribución de `N`:** 17/53 (32%) tienen exactamente `N=1`; 15/53 (28%) alcanzan la ventana completa `N=5`; el resto se reparte entre 2, 3 y 4.
- **Pearson(N, Variable001) = 0.387** — positivo, débil-moderado.
- **Pearson(N, |Variable001−50|) = −0.485** — negativo, moderado: a mayor `N`, el valor tiende a alejarse menos de 50. **Más fuerte que el hallazgo análogo de `CAL-004` para Variable003/004 (`r=−0.246`, "dirección correcta pero débil")** — evidencia de que el patrón de degeneración por muestra pequeña es, si acaso, más pronunciado en Variable001 que el que ya justificó implementar el Shrinkage de Variable003/004.

**Prueba matemática exacta, análoga a la de `CAL-004` (no solo correlación):** con `N=1`, `puntos_j ∈ {0,1,3}` produce exactamente **3 valores posibles** de Variable001: `0.0` (derrota), `33.33` (empate) o `100.0` (victoria) — verificado sobre los 17 equipos reales con `N=1` (México, Senegal, Japón, Turquía, Argelia, Egipto, Bolivia, Costa Rica, Serbia, Grecia, Irlanda, Jordania, Arabia Saudita, Irak, Ghana, RD Congo, Haití): **ninguno produce un cuarto valor distinto de esos tres**, sin importar el marcador real del partido (una victoria 5-0 y una victoria 1-0 producen exactamente el mismo `100.0`). Es, estructuralmente, **una degeneración más severa que la de `CAL-004`**: el z-score de Variable003/004 en `N=1` colapsa a `±1` exacto, pero `Φ(±1)` todavía produce dos valores continuos distinguibles (`≈15.9%`/`≈84.1%`); Variable001 en `N=1` no tiene ninguna transformación suavizante — el valor final publicado es, literalmente, uno de solo 3 números posibles.

## 13.4 Sensibilidad (Parte 4) — comparación directa a `+5`/`+10`/`+20` puntos, sobre los 35 partidos evaluables reales

| Δ Variable | +5pts | +10pts | +20pts | Patrón |
|---|---|---|---|---|
| Variable003 → Δλ | +0.122 | +0.244 | +0.464 | **Lineal** (≈×2, ×2) |
| Variable004 → Δλ (rival) | −0.093 | −0.187 | −0.374 | **Lineal** (≈×2, ×2) |
| Variable001 → Δλ | +0.010 | +0.019 | +0.021 | **Saturante** (×1.9, ×1.1) |

**Hallazgo estructural, con explicación matemática exacta, no solo empírica:** la sensibilidad de Variable001 **se satura** entre `+10` y `+20` puntos — casi no crece más. La causa es identificable en el propio código (`engine01.py`/`engine02.py`, sin modificarlo, solo leído): `m_forma = 1 + clip(0.5·r + 0.5·t, −DELTA_MAX, +DELTA_MAX)` con `DELTA_MAX=0.20`. Un incremento de `+20` puntos en Variable001 (ej. de 50 a 70) mueve `r=(Forma−50)/50` de `0` a `0.4`, y `0.5·r=0.20` — **exactamente el límite `DELTA_MAX`**: el propio clip ya vigente (compartido con Variable002, diseñado en `MODEL-001`/`BUILD-009`, sin relación con esta investigación) satura el efecto de cualquier perturbación grande sobre `λ`. Variable003/004 no tienen un clip comparable en su rango de operación real — su clip estructural (`FO`/`FD ∈ [0,100]`) nunca se activa en datos reales (`ANL-003`, confirmado también aquí: ninguno de los 70 valores de `FO`/`FD` toca 0 o 100).

**Consecuencia central para el diagnóstico:** la contribución realizada de Variable001 a la separación de `λ` (`ANL-003`, `0.582`) **no** proviene de que cada punto de Variable001 mueva `λ` desproporcionadamente — al contrario, su efecto por punto está entre 6 y 12 veces **más contenido** que el de Variable003 (compárese `0.010`/`5pts` vs. `0.122`/`5pts`) y además se satura. Proviene, en cambio, de que **el propio valor de Variable001 varía muchísimo entre partidos reales** (sección 13.2: `desv=28.57`, equivalente a Variable003/004 sin Shrinkage) — el problema no está en la propagación hacia `λ` (ya amortiguada por `DELTA_MAX`), está en la **calidad del dato de entrada** (el valor 0-100 de Variable001 en sí).

## 13.5 Variabilidad — equipos con mayor/menor oscilación (Parte 5)

**Ejemplos reales, más oscilantes** (mayor desviación estándar de puntos en su ventana): Rep. Checa (`N=2`, puntos `[3,0]`, desv=`2.12`); Bélgica/Noruega/Venezuela/Eslovaquia (`N=3`, patrón `[3,0,0]` o `[0,3,0]`, desv=`1.73`); Francia (`N=5`, `[3,3,3,0,0]`, Variable001=`60.0`); Argentina (`N=5`, `[3,3,3,3,0]`, Variable001=`80.0`).

**Ejemplos reales, más estables** (desv=`0`, resultado idéntico en toda la ventana): España (`N=5`, `[3,3,3,3,3]`, Variable001=`100.0` — 5 victorias consecutivas, señal real, no ruido); Paraguay (`N=5`, `[0,0,0,0,0]`, Variable001=`0.0` — 5 derrotas consecutivas); Alemania/Austria/Canadá/Ucrania/Panamá/Albania (rachas perfectas de menor tamaño).

**Matiz importante, no visible sin este desglose:** a diferencia de la degeneración de `N=1` (arbitraria, depende solo de un resultado aislado), los casos de `N=5` con `desv=0` **sí representan señal real** (una racha genuina de 5 resultados idénticos) — no son ruido disfrazado de información. Esto distingue Variable001 de Variable003/004 en un aspecto favorable: su ventana máxima (`N=5`) captura un fenómeno futbolístico reconocible (racha de forma), mientras que la degeneración de `CAL-004` en Variable003/004 no tenía ninguna interpretación futbolística — era puramente un artefacto de una población de 2 equipos.

## 13.6 Simulación conceptual del Shrinkage sobre Variable001 (Parte 6) — sin implementar

**Adaptación necesaria, no una copia literal:** la ecuación oficial de Variable003/004 (sección 12 de este documento) contrae el **z-score** `Z*` hacia `Z*_competición` (la media histórica de `Z*` en esa competición). Variable001 **no tiene z-score ni población de competición** (sección 13.1) — aplicar "exactamente el mismo shrinkage" en sentido literal es matemáticamente imposible sin inventar una población que hoy no existe en el diseño. La adaptación estructuralmente más simple y fiel al mismo principio (contracción hacia un valor neutro cuando la evidencia propia es escasa) es contraer directamente sobre el valor ya acotado `[0,100]`, hacia el punto neutro teórico `50` (no hay `Φ` que invertir, ya que Variable001 nunca pasó por `Φ`):

```
w(N) = N / (N + k)                              (misma forma funcional, MODEL-018 §12)
Forma_final = w(N) · Forma_cruda + (1 − w(N)) · 50
```

**Efecto simulado (matemático, con `k=5`, mismo valor de referencia que Variable003/004 — no una calibración, solo para ilustrar):**

| N | w(N) | Ejemplo: Forma_cruda=100 (racha perfecta) | Ejemplo: Forma_cruda=0 (racha nula) |
|---|---|---|---|
| 1 | 0.167 | 100 → **58.3** | 0 → **41.7** |
| 3 | 0.375 | 100 → **68.75** | 0 → **31.25** |
| 5 | 0.5 | 100 → **75.0** | 0 → **25.0** |
| N→∞ (hipotético) | →1 | → 100 (converge al valor crudo) | → 0 |

**Efecto esperado en equipos con `N` pequeño:** fuerte contracción hacia 50 — un único resultado (victoria o derrota) dejaría de producir un valor tan extremo como `100`/`0`, exactamente el mismo tipo de corrección que `IMP-002` ya aplicó a Variable003/004. **Efecto esperado en equipos con `N` grande (`N=5`, el máximo real hoy):** contracción moderada pero **nunca completa** — incluso en `N=5` (la ventana llena), `w(5)=0.5` con `k=5`, por lo que una racha perfecta real de España (`100.0`) quedaría en `75.0`, no en `100.0` — a diferencia de Variable003/004 (`N_máx=10`, `w(10)≈0.67` con el mismo `k`), Variable001 **nunca alcanza el mismo nivel de convergencia al valor crudo que Variable003/004**, porque su ventana máxima (`5`) es la mitad de la de Variable003/004 (`10`) — con `k=5` fijo, el "punto de estabilización" (`w=0.5`) coincide exactamente con la ventana máxima de Variable001, mientras que para Variable003/004 la ventana máxima ya supera ese punto. **Esto es un hallazgo de diseño relevante para una futura calibración**, no una recomendación de valor: si se reutilizara `k=5` sin ajuste, Variable001 quedaría contraída de forma más agresiva, en términos relativos, que Variable003/004 — razonable dado que su ventana es más corta (menos evidencia máxima posible), pero debe decidirse explícitamente, no heredarse por accidente. **Convergencia cuando N→∞:** matemáticamente, `w(N)→1` y `Forma_final→Forma_cruda`, igual que en Variable003/004 — aunque `N→∞` no es alcanzable en este dominio (`VENTANA_PARTIDOS_FORMA_RECIENTE=5` es un tope estructural, no una muestra creciente), por lo que en la práctica el sistema nunca abandona la zona de contracción parcial.

## 13.7 Riesgo (Parte 7)

- **Pérdida de sensibilidad a rachas reales:** el riesgo más concreto, con evidencia directa en la sección 13.5 — España (`N=5`, 5 victorias reales consecutivas) pasaría de `100.0` a `75.0` con `k=5`; Paraguay (`N=5`, 5 derrotas reales) de `0.0` a `25.0`. A diferencia de Variable003/004 (donde `CAL-004` demostró que el valor extremo en muestra pequeña **no** reflejaba necesariamente una diferencia real), aquí una racha de 5 resultados **sí** es, en general, información futbolística genuina — el riesgo de sobre-suavizar una señal real es mayor que el que existía para Variable003/004.
- **Retraso en detectar cambios reales:** un equipo que mejora abruptamente (ej. cambio de entrenador) tardaría más partidos en que Variable001 lo refleje plenamente, exactamente el mismo tipo de retraso ya aceptado como trade-off para Variable003/004 en `MODEL-017`/`018` — pero, dado que la ventana de Variable001 (`N=5`) ya es más corta que la de Variable003/004 (`N=10`), el retraso *relativo* introducido por el shrinkage sería proporcionalmente mayor.
- **Exceso de suavizado dado un `k` mal elegido:** mismo riesgo genérico ya documentado en la sección 6 de este documento para Variable003/004 — aplica igual aquí, con el matiz adicional (13.6) de que reutilizar `k=5` sin ajuste produciría, en términos relativos a la ventana máxima, una contracción más fuerte que la que Variable003/004 recibieron.
- **Riesgo no compartido con Variable003/004, específico de Variable001:** al no existir una "población de competición" hacia la cual contraer, la única alternativa estructuralmente simple es contraer hacia el punto neutro fijo `50` — una elección menos informada que "la media real de la competición" (que sí incorpora información real sobre el nivel de esa competición específica). Contraer hacia `50` asume que "el equipo promedio" tiene Forma Reciente igual a 50 en general, una asunción más fuerte y potencialmente menos precisa que la que Variable003/004 ya hacían.

## 13.8 Comparación explícita Variable003 vs. Variable001 (Parte 8)

| Aspecto | Variable003 (Potencial Ofensivo) | Variable001 (Forma Reciente) |
|---|---|---|
| Mecanismo de cálculo | z-score `Z=Σvᵢzᵢ` vs. población de la competición, transformado por `Φ` | Proporción directa de puntos, sin población, sin `Φ` |
| Población de comparación | Sí — otros equipos de la misma competición y ventana de fechas | **No existe** — estadística intra-equipo pura |
| Ventana máxima | `N=10` | `N=5` |
| Mecanismo de degeneración en `N` mínimo | Colapso del z-score a `±1` exacto (población de 2) | Colapso a exactamente 3 valores discretos (`0`/`33.3`/`100`) |
| Severidad de la degeneración | Severa (`CAL-004`) | **Más severa en términos de resolución** (3 valores vs. un continuo tras `Φ`) |
| Desv. estándar real (sin estabilizar) | 27.18 (`CAL-004`, N=32) | 28.57 (N=53) — **magnitud comparable** |
| Correlación `N` vs. extremidad | `r=−0.246` (débil) | `r=−0.485` (moderada, **más fuerte**) |
| Sensibilidad marginal sobre `λ` (+5pts) | `+0.122`, lineal | `+0.010`, **saturante** (clip `DELTA_MAX` ya vigente) |
| Contribución realizada a `|Δλ|` (`ANL-003`) | 0.579 | 0.582 (**comparable**, pese a sensibilidad marginal ~12× menor) |
| ¿El valor en `N` alto sigue siendo información real? | Cuestionable en `N` intermedio (Inglaterra, `CAL-004`, osciló 19pts en `N≈8-10`) | Sí — una racha de 5 resultados es información futbolística reconocible |
| Mecanismo de shrinkage directamente reutilizable | — (es el original) | **No literalmente** — requiere adaptación (contracción sobre el valor 0-100, no sobre un z-score) |

**¿Es el mismo problema estadístico?** **Parcialmente.** Comparten la causa raíz genérica (muestra pequeña, ausencia de cualquier mecanismo de estabilización) y una magnitud de varianza real comparable — pero **no** comparten el mecanismo exacto de degeneración (colapso de z-score vs. colapso a 3 valores discretos), **no** comparten el canal de propagación hacia `λ` (Variable003 propaga casi sin freno; Variable001 ya está parcialmente contenida por `DELTA_MAX`), y **no** comparten la interpretabilidad del valor en el extremo superior de su ventana (el `N=10` de Variable003 todavía mostraba volatilidad cuestionable; el `N=5` de Variable001 refleja, en los casos revisados, rachas reales). Tratar ambos problemas con la fórmula idéntica sería una simplificación conveniente pero no rigurosa.

---

# Sección 14 — Investigación de la Variable007 (Fatiga) (`MODEL-022`)

**Origen:** `ANL-003` y `MODEL-021` señalaron que Variable007 mostraba, como Variable001, sensibilidad marginal baja pero contribución realizada relativamente alta a la separación de `λ` — misma pregunta que ya se hizo para Variable001: ¿sufre el mismo problema estructural de muestra pequeña? Toda la evidencia de esta sección proviene de invocar directamente los repositorios y fórmulas ya existentes (`_FatigaRepository`, `VariablePreparation._calcular_fatiga`/`_aplicar_formula_fatiga_descanso`/`_aplicar_formula_fatiga_viaje`) sobre los 35 partidos evaluables de `VALID-003`/`ANL-002`/`ANL-003`/`MODEL-021` (mismo snapshot temporal) — solo lectura, ningún archivo modificado.

## 14.1 Anatomía de Variable007 — dos señales de naturaleza distinta, promediadas

```
Fatiga = (Fatiga_Descanso + Fatiga_Viaje) / 2   si ambas disponibles
       = la señal única disponible                si solo una lo está
       = disponible=False                          si ninguna lo está (debut absoluto)

--- Fatiga_Descanso (z-score, SÍ usa Φ) ---
Entrada:        Días_descanso(T) = fecha_partido − fecha(Partido_anterior(T))
                Partido_anterior: el más reciente con fecha < fecha_partido, sobre
                TODO partidos.csv, sin filtrar por torneo (§4) -- una sola
                observación, no una ventana de N partidos propios
Población:      TODAS las selecciones con fila en partidos.csv del MISMO
                id_torneo del partido a predecir, con Partido_anterior resoluble
                (metricas.selecciones_torneo ∩ partido_anterior_por_seleccion)
Normalización:  z = (Días_descanso(T) − μ_población) / σ_población
Transformación: Fatiga_Descanso = 100·(1 − Φ(z))   -- invertido, más descanso = menos fatiga
Exclusión:      si población < 2 selecciones o σ=0 → None (§13)

--- Fatiga_Viaje (categórica, SIN z-score, SIN Φ) ---
Entrada:        ciudad/país del estadio del Partido_anterior(T) vs. del partido actual
Categoría:      0 (misma ciudad) | 1 (mismo país) | 2 (país distinto)
Fórmula:        Fatiga_Viaje = 50 · Categoría   -- mapeo ordinal fijo, sin calibrar
```

**Diferencia estructural clave, visible antes de cualquier dato:** Variable007 es un HÍBRIDO de dos mecanismos que ninguna de las variables ya investigadas combina — un componente tipo z-score/`Φ` (como Variable003/004) pero cuya población es **el tamaño real de un torneo** (potencialmente grande), no una ventana de partidos propios; y un componente puramente categórico (3 valores fijos, sin ninguna dependencia de tamaño de muestra en absoluto, ni siquiera análoga a la de Variable001). No existe, además, ningún concepto de "N partidos propios" para `Fatiga_Descanso` — depende de un único dato (el partido inmediatamente anterior), no de un promedio sobre una ventana como Variable001 (`N≤5`) o Variable003/004 (`N≤10`).

## 14.2 Distribución real (Parte 4) — 70 observaciones (35 partidos × 2 lados), 100% con dato

| | media | mediana | desv.std | min | max | P5 | P25 | P50 | P75 | P95 |
|---|---|---|---|---|---|---|---|---|---|---|
| Variable007 (Fatiga) | 56.70 | 57.59 | **20.31** | 6.56 | 100.0 | 28.41 | 43.52 | 57.59 | 67.52 | 95.11 |
| Variable001 (referencia, `MODEL-021`) | 23.85 | 16.67 | 28.57 | 0.0 | 100.0 | — | — | — | — | — |
| Variable003 pre-Shrinkage (`CAL-004`) | 36.32 | 31.69 | 27.18 | 3.02 | 96.47 | — | — | — | — | — |

**Hallazgo directo:** la desviación estándar real de Variable007 (`20.31`) es **notablemente menor** que la de Variable001 (`28.57`) y que la de Variable003/004 antes del Shrinkage (`27-29`) — más cercana, aunque todavía superior, a Variable003/004 **después** del Shrinkage (`16-18`). Primera señal cuantitativa de que Variable007 no está en la misma situación que las dos variables ya investigadas.

## 14.3 Degeneración por tamaño de muestra (Parte 3) — resultado distinto a `CAL-004`/`MODEL-021`

**Sobre `Fatiga_Descanso`, la única señal con z-score:** la "N" relevante no es el historial propio del equipo (no existe ventana), es **el tamaño de la población del torneo**. Medida directamente sobre los 35 partidos: media=`14.83`, mediana=`15`, rango `0-19`; distribución por tamaño exacto: `{0: 1, 12: 11, 13: 3, 14: 2, 15: 1, 16: 2, 18: 12, 19: 3}`. **Solo 1 de 35 partidos tiene población insuficiente (`<2`)** — ese caso ya está correctamente excluido por la propia fórmula (`_aplicar_formula_fatiga_descanso` devuelve `None`, cae a `Fatiga_Viaje` en solitario). **Ningún partido de esta muestra tiene una población de tamaño 2 o 3** (a diferencia de la premisa de la pregunta del brief) — el mínimo real observado, quitando el único caso excluido, es `12` selecciones. **No se reproduce el patrón de `CAL-004`/`MODEL-021`**: no hay colapso a pocos valores discretos, porque la población nunca es pequeña en la práctica — los torneos reales de este dataset (Eurocopa, Copa América, más los partidos agregados por `DATA-009`) tienen entre 16 y 24 selecciones participantes, y la mayoría comparten un `Partido_anterior` resoluble.

**Limitación honesta de esta conclusión, no ocultada:** la evidencia es tranquilizadora **para los tipos de torneo presentes en la muestra actual** (torneos continentales grandes) — no garantiza el mismo comportamiento para una futura "torneo" de tipo bilateral o eliminatoria de 2 equipos (ej. una serie de repechaje), donde la población de `selecciones_torneo` sí podría reducirse a 2, reproduciendo el mismo tipo de degeneración ya demostrada para Variable003/004. No hay ningún caso así en los datos actuales para verificarlo empíricamente.

**Sobre `Fatiga_Viaje`:** sin ninguna dependencia de tamaño de muestra por diseño (categórico fijo, sección 14.1) — no aplica el concepto de degeneración por `N` en absoluto.

## 14.4 Sensibilidad real (Parte 2) — comparación con Variable001/Variable003/Variable004

| Δ Variable007 (local) | Δλ_local media | Δλ_visitante media | Patrón |
|---|---|---|---|
| +5pts | −0.0242 | +0.0184 | |
| +10pts | −0.0484 | +0.0369 | |
| +20pts | −0.0968 | +0.0736 | **Lineal** (×2.0, ×2.0 exacto) |

**A diferencia de Variable001 (`MODEL-021`, saturante entre `+10`/`+20`), Variable007 escala de forma perfectamente lineal** en el rango probado — sin evidencia de que el clip compartido `pen=clip(...,0,PEN_MAX=0.30)` se active: con `Variable006`/`Variable008` siempre en `0` (sin dato, `termino_disponibilidad=termino_calidad=0`), el término de fatiga por sí solo (`W_FATIGA·fatiga/100 = fatiga/300`) alcanzaría el techo `PEN_MAX=0.30` solo si `fatiga=90`; en la muestra real (media `56.7`, P95 `95.1`), la mayoría de los casos probados con `+20` quedan por debajo de ese umbral, por lo que el clip casi no se activa — comportamiento distinto al de Variable001, cuyo clip relevante (`DELTA_MAX=0.20` dentro de `m_forma`) se satura ya con `+20` puntos desde valores típicos.

## 14.5 Saturación (Parte 6)

- **En el valor crudo:** `0/70` observaciones tocan `0.0`; `2/70` (2.9%) tocan exactamente `100.0` — saturación mínima y ocasional en el techo, coherente con casos reales de fatiga máxima (cero días de descanso y viaje intercontinental simultáneos), no un artefacto de la fórmula.
- **En la propagación hacia `λ`:** ninguna evidencia de saturación dentro del rango `+5` a `+20` (sección 14.4) — la respuesta es lineal, a diferencia de Variable001.
- **Zonas donde aumentar Fatiga ya no cambia `λ`:** ninguna detectada en el rango probado; teóricamente existiría cerca de `fatiga→100` combinado con el clip `PEN_MAX`, pero no se observó en esta muestra.

## 14.6 Correlaciones (Parte 5)

| Par | r (Pearson) |
|---|---|
| Fatiga ↔ λ (propio) | 0.404 |
| Fatiga ↔ \|Δλ\| | 0.167 (débil) |
| Fatiga ↔ Accuracy | 0.017 (nula) |
| Fatiga ↔ Empate real | −0.017 (nula) |
| Fatiga ↔ Error (\|λ−goles reales\|) | 0.228 (débil) |
| Fatiga ↔ Top-4 (marcador real presente) | −0.165 (débil) |

**Interpretación:** Fatiga influye en `λ` de forma moderada y esperada (r=0.404, consistente con su rol de penalización), pero **no muestra ninguna asociación fuerte con la calidad de la predicción** (Accuracy, Top-4, Empates) — las correlaciones con esas 4 métricas de desempeño son todas débiles o nulas. No hay evidencia de que Variable007, en su estado actual, sea una fuente relevante de error sistemático.

## 14.7 Comparación explícita Variable001 vs. Variable007 (Parte 7)

| Aspecto | Variable001 (Forma Reciente) | Variable007 (Fatiga) |
|---|---|---|
| Mecanismo | Proporción directa, sin z-score, sin `Φ`, sin población | Híbrido: z-score/`Φ` (Descanso) + categórico fijo (Viaje) |
| "N" relevante | Ventana propia, `N≤5` partidos | Sin ventana propia (1 solo dato); población = tamaño del torneo |
| Degeneración por muestra pequeña | **Sí, severa** — colapso a 3 valores exactos en `N=1` (32% de los casos) | **No detectada** — población real siempre ≥12 en esta muestra (excepto 1 caso ya excluido correctamente por la fórmula) |
| Desv. estándar real | 28.57 | 20.31 (menor) |
| Sensibilidad marginal sobre `λ` (+5pts) | +0.010, **saturante** (`+10`→`+20` casi sin cambio) | −0.024 (local), **lineal** (`×2`, `×2` exacto) |
| Propagación hacia `λ` | Amortiguada por `DELTA_MAX=0.20` (satura fácilmente) | Amortiguada por `PEN_MAX=0.30`, pero no se satura en el rango real observado |
| Correlación con Error/Top-4/Accuracy | No medida directamente en `MODEL-021` (fuera de su alcance) | Débiles/nulas (0.02-0.23) |
| Riesgo de shrinkage | Alto — rachas de `N=5` suelen ser señal real | Bajo — sin evidencia de degeneración que corregir |

**Conclusión de la comparación:** Variable001 y Variable007 **no** son el mismo caso. Variable001 mostró evidencia matemática directa de degeneración (3 valores exactos en `N=1`) con un canal de propagación ya amortiguado pero un problema real en el valor crudo. Variable007 no muestra evidencia de degeneración con los datos actuales — su componente de z-score opera sobre poblaciones grandes en la práctica, y su propagación hacia `λ` es lineal y bien comportada.

## 14.8 ¿Merece Shrinkage? (Parte 8)

**No, con la evidencia actual — respuesta cuantitativa, no categórica:**

1. **Sin degeneración matemática demostrada:** a diferencia de `CAL-004` (Variable003/004, población=2 exacta, colapso a `±1` probado) y de `MODEL-021` (Variable001, `N=1` exacto, colapso a 3 valores probado), esta misión **no encontró ningún caso real** de población pequeña para `Fatiga_Descanso` en los 35 partidos evaluables — el mínimo observado (excluyendo el único caso ya correctamente excluido) es `12`.
2. **Sensibilidad lineal, no saturante ni explosiva:** el comportamiento sobre `λ` es predecible y proporcional en el rango probado (`+5` a `+20`).
3. **Correlaciones débiles con desempeño:** ninguna asociación relevante con Accuracy, Top-4 o Empates que sugiera que Variable007 esté distorsionando las predicciones.
4. **Salvedad explícita, no un "no" absoluto:** la conclusión depende de que los torneos futuros mantengan poblaciones grandes (`selecciones_torneo`) — un escenario de torneo bilateral o serie de 2 equipos podría reproducir la degeneración de `CAL-004`, sin evidencia todavía disponible para confirmarlo o descartarlo. Por eso la recomendación es **"No, con la evidencia actual"**, no **"Nunca"**.

---

Fin del documento.
