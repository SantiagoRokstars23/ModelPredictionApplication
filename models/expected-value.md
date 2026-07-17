# Expected Value

**Archivo:** `models/expected-value.md`

**Misión:** MODEL-006 — Modelo Matemático del Expected Value

**Versión:** 1.0.0-investigación

**Estado:** Investigación completa — evoluciona el stub original (a diferencia de `MODEL-005`, que se creó desde cero, este documento sí tenía un stub previo de 8 secciones mínimas, igual que `MODEL-001` a `004`)

---

## Nota de origen

Con este documento, los 6 motores del Engine (`engine/01` a `engine/06`) tienen, por primera vez de forma simultánea, un documento de `models/` que fundamenta su estructura matemática. Es el último eslabón de la cadena iniciada en `MODEL-001` — su Cierre (pregunta 8) evalúa explícitamente si eso equivale a un "núcleo matemático completo".

---

# 1. Objetivo

Desarrollar el fundamento matemático y conceptual del Valor Esperado (Expected Value) — la base científica de `engine/06-Expected-Value.md` — sin implementar código, sin modificar el Engine, las Variables Oficiales ni el Algoritmo, y sin fijar ningún valor numérico de coeficiente o umbral.

---

# 2. Descripción — ¿Qué mide el Expected Value?

**Qué mide:** si una cuota concreta, ofrecida por una casa de apuestas para un mercado concreto, representa una ventaja matemática para quien apuesta, dado lo que el Modelo Santiago estima como probabilidad real de ese resultado. No mide qué va a pasar en el partido (eso es `engine/03`), ni cuánto puede confiarse en esa estimación (`engine/05`), ni qué tan volátil es el partido en sí (`engine/04`) — mide la **discrepancia entre el modelo y el precio de mercado**.

**Qué NO mide:** el Expected Value no es una probabilidad de ganar la apuesta, ni una predicción de resultado, ni una recomendación de cuánto dinero arriesgar. Es una medida de **ventaja matemática esperada por unidad apostada**, calculada bajo el supuesto de que la probabilidad del modelo es correcta.

---

# 3. Problema que Resuelve

`engine/03`, `engine/04` y `engine/05` ya responden "¿qué probabilidad tiene cada resultado, qué tan confiable es ese cálculo y qué tan volátil es el partido?" — pero ninguno de los tres compara esa información con lo que el mercado de apuestas está dispuesto a pagar. Sin esa comparación, una probabilidad alta calculada correctamente puede llevar a apostar en un mercado que ya la refleja (o la supera) en su precio, sin ninguna ventaja real. El Valor Esperado resuelve exactamente esa comparación.

---

# 4. Distinción: Probabilidad → Expected Value → Gestión de Bankroll

Esta misión pide formalizar una cadena de tres preguntas distintas, cada una resuelta por un componente distinto del proyecto — confundirlas es el error conceptual más común en apuestas deportivas cuantitativas:

| Pregunta | Quién la responde | Naturaleza |
|---|---|---|
| ¿Qué probabilidad tiene cada resultado? | `engine/03-Poisson.md` (`MODEL-003`) | Estimación estadística |
| Dada esa probabilidad y la cuota ofrecida, ¿existe ventaja matemática? | `engine/06-Expected-Value.md` (este documento) | Comparación modelo vs. mercado |
| Dado que existe ventaja, ¿cuánto capital arriesgar? | `engine/07-Bankroll-Engine.md` *(futuro, no implementado todavía)* | Gestión de riesgo |

El Expected Value **no decide cuánto apostar** — eso pertenece, por diseño, a un motor distinto y futuro. Esta distinción ya está implícita en la lista de "Restricciones" de `engine/06` (nunca declara nada sobre tamaño de apuesta) y en que "Kelly Criterion adaptativo" aparece en su sección "Mejoras Futuras", no en su "Flujo del Motor" actual — el Criterio de Kelly (Kelly, 1956, ver sección 15) es, precisamente, una fórmula de *tamaño de apuesta* condicionada al Expected Value, no una fórmula de Expected Value en sí. Este documento fundamenta el segundo eslabón de la cadena; el tercero queda fuera de alcance hasta que `engine/07` exista y tenga su propio `models/`.

---

# 5. Fundamento matemático y literatura

**Valor esperado de una variable aleatoria discreta.** El concepto es el de esperanza matemática estándar de probabilidad (no específico de apuestas deportivas): dado un resultado binario (ganar/perder una apuesta) con una probabilidad y un pago asociado a cada desenlace, el valor esperado es la suma de cada desenlace ponderado por su probabilidad. Aplicado a una apuesta de una unidad a una cuota decimal, produce la fórmula de la sección 7.

**Ley de los Grandes Números — por qué EV positivo no garantiza ganar una apuesta concreta.** Una sola apuesta es un evento binario de alta varianza relativa al tamaño típico de una ventaja estadística en deportes (unos pocos puntos porcentuales de diferencia entre probabilidad del modelo y probabilidad implícita). El valor esperado positivo es una propiedad del **promedio a largo plazo sobre muchas repeticiones** de apuestas con la misma ventaja relativa, no una garantía sobre el resultado individual — es la Ley de los Grandes Números aplicada a una secuencia de apuestas independientes. Esta distinción es la razón por la que `docs/07-Backroll.md` (gestión de bankroll) exige disciplina y volumen, no solo identificar valor: EV positivo es condición necesaria, no suficiente, para obtener retorno real.

**Eficiencia de mercados de apuestas y margen de la casa (overround).** La literatura sobre economía de mercados de apuestas (p. ej. Levitt, 2004 — ver sección 15) documenta que las casas de apuestas fijan precios incorporando un margen (overround/vig): la suma de las probabilidades implícitas de todos los resultados de un mismo mercado excede el 100%. Esto implica que la probabilidad implícita "cruda" de una única cuota sobreestima sistemáticamente el precio real de mercado — una comparación más precisa requiere normalizar el margen entre todas las opciones del mismo mercado (sección 8.2). La misma literatura documenta que los mercados de apuestas deportivas de alto volumen son razonablemente eficientes — relevante para la sección 9 (prudencia ante EV extremo).

**Closing Line Value (CLV).** Concepto ampliamente adoptado en la literatura de apuestas deportivas cuantitativas (popularizado, entre otros, por Miller & Davidow, 2019 — ver sección 15): la cuota de cierre (la vigente justo antes del inicio del partido) incorpora toda la información disponible hasta el último momento y se considera, en la práctica, el mejor estimador disponible del "verdadero" precio de mercado. Comparar la cuota usada por el modelo contra la cuota de cierre real permite distinguir si una discrepancia detectada era valor genuino o solo una cuota temprana que el mercado corrigió después — ver sección 11.

---

# 6. Componentes

*(Terminología ya usada por `engine/06`, sin redefinir sus nombres — solo se formaliza su cálculo.)*

| Componente | Símbolo | Origen |
|---|---|---|
| Probabilidad del Modelo | `P_modelo` | `engine/03-Poisson.md` (`MODEL-003`), para el mercado y resultado específicos solicitados |
| Cuota (decimal) | `c` | `cuotas.csv` (`data/processed/selecciones-nacionales/`), campo `cuota_decimal` — dato de mercado, no Variable Oficial (nota MR-004, `engine/06` sección "Entradas") |
| Probabilidad Implícita | `P_implícita` | Derivada de `c` — nunca almacenada, siempre calculada (sección 8) |
| Diferencia (Edge) | `Δ_edge` | `P_modelo − P_implícita` — el campo "Diferencia porcentual" ya declarado en la sección "Salida" de `engine/06` |

`cuotas.csv` (verificado en esta misión) ya incluye los campos `id_partido`, `mercado` y `seleccion_o_resultado` junto a `cuota_decimal` — el esquema permite, sin ampliarlo, agrupar todas las cuotas del mismo partido y mercado para la normalización de margen de la sección 8.2. Hoy el archivo no contiene filas de datos reales (solo encabezado), consistente con `docs/27-Auditoria-de-Variables-Pendientes.md`.

---

# 7. Construcción matemática — Fórmula del Expected Value

*(Estructura únicamente — ningún coeficiente ni umbral recibe valor numérico, conforme a `CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística".)*

## 7.1 Derivación

Para una apuesta de 1 unidad a una cuota decimal `c`:

- Si el resultado ocurre (probabilidad `P_modelo`, según el modelo): se recibe `c` unidades (stake devuelto + ganancia), ganancia neta = `c − 1`.
- Si el resultado no ocurre (probabilidad `1 − P_modelo`): se pierde la unidad apostada, ganancia neta = `−1`.

```
EV = P_modelo · (c − 1) + (1 − P_modelo) · (−1)
   = P_modelo·c − P_modelo − 1 + P_modelo
   = P_modelo·c − 1
```

## 7.2 Fórmula final

```
EV = (P_modelo · c) − 1
```

`EV` se expresa como retorno esperado por unidad apostada (ej. `EV = 0.08` ⇒ 8% de retorno esperado por unidad, bajo el supuesto de que `P_modelo` es correcta). `P_modelo` proviene directamente de `engine/03` (sección 6), sin transformación adicional — no se recalcula en este documento, se reutiliza, igual que `MODEL-005` reutilizó la distribución de Poisson para la entropía.

## 7.3 Probabilidad implícita

```
P_implícita = 1 / c
```

Esta es exactamente la operación que `engine/06` ya describe en su "Flujo del Motor", Paso 3 ("Calcular la probabilidad implícita de cada cuota") — este documento formaliza su fórmula, no la modifica.

## 7.4 Normalización por margen (refinamiento, no obligatorio para V1)

Para un mercado con `n` resultados mutuamente excluyentes y cuotas `c₁...cₙ`:

```
P_implícita_bruta_i = 1 / cᵢ

Margen = (Σ P_implícita_bruta_i) − 1        (overround, típicamente > 0)

P_implícita_normalizada_i = P_implícita_bruta_i / Σ P_implícita_bruta_i
```

`P_implícita_normalizada` es una comparación más precisa contra `P_modelo` que `P_implícita_bruta`, porque elimina el margen de la casa (sección 5). Requiere conocer **todas** las cuotas del mismo `id_partido` + `mercado`, no solo una — factible con el esquema actual de `cuotas.csv` (sección 6), pero no exigido por el "Flujo del Motor" actual de `engine/06` (que calcula "la probabilidad implícita de cada cuota" en singular). Se documenta como candidato explícito para la Versión 2.0 (sección 16), no como parte obligatoria de esta fórmula base.

---

# 8. Interpretación

`engine/06-Expected-Value.md` **ya fija**, en su propia sección "Clasificación", las cinco categorías (EV Muy Alto, EV Alto, EV Moderado, EV Bajo, EV Negativo) — este documento no las redefine ni les asigna umbrales numéricos nuevos, solo confirma su compatibilidad con la fórmula de la sección 7 y añade la interpretación cualitativa que faltaba:

| Categoría (`engine/06`) | Signo/magnitud de `EV` | Lectura |
|---|---|---|
| EV Negativo | `EV < 0` | La cuota no compensa el riesgo según el modelo — sin ventaja matemática |
| EV Bajo | `EV` positivo, cercano a 0 | Ventaja marginal |
| EV Moderado | `EV` positivo, intermedio | Ventaja razonable |
| EV Alto | `EV` positivo, considerable | Ventaja notable |
| EV Muy Alto | `EV` positivo, grande | Ver nota de prudencia, sección 9 |

**Nota de prudencia (fundamentada en la sección 5):** en mercados de apuestas deportivas de alto volumen, razonablemente eficientes, un `EV` extremadamente alto es, con más frecuencia, señal de un **error en el modelo o en el dato de la cuota** (cuota desactualizada, error de captura, mercado de baja liquidez) que de una oportunidad genuina — el mercado rara vez se equivoca por márgenes grandes. Esta lectura es consistente con que `engine/06` ya prohíbe, en su sección "Restricciones", "basarse únicamente en cuotas altas" y exige no ignorar el Índice de Caos ni el Nivel de Confianza (sección 10).

---

# 9. Relación con las cuotas

Las cuotas son un insumo **comparativo externo**, de solo lectura. El Expected Value:

- **Nunca modifica** `P_modelo` (siempre proviene, sin alteración, de `engine/03`).
- **Nunca modifica** el Nivel de Confianza (`engine/05`) ni el Índice de Caos (`engine/04`).
- **Nunca convierte** la cuota en una Variable Oficial — consistente con la nota arquitectónica ya fijada por `MR-004` en `engine/06` (sección "Entradas"): las cuotas son Datos de Mercado, categoría paralela a las 12 Variables Oficiales, con contrato propio todavía sin diseñar (`INC-05`, sección 12).

Esta separación es la misma que `MODEL-005` aplicó entre Chaos y Poisson (sección 9 de ese documento): un motor lee la salida de otro, pero nunca la reescribe.

---

# 10. Rol de Confidence y Chaos — el EV numérico frente a la Recomendación

`engine/06` declara, en su sección "Entradas", que recibe información de `engine/04` y `engine/05`, y en "Restricciones" prohíbe explícitamente "ignorar el Índice de Caos" e "ignorar el Nivel de Confianza" — pero también declara, en su sección "Salida", que "Valor Esperado (EV)" y "Recomendación" son campos **distintos**. Esta misión resuelve esa aparente tensión sin contradecir ninguno de los dos textos:

- **`EV` (sección 7)** es una función pura de `P_modelo` y `c` — no incorpora Confianza ni Caos. Mantenerlo puro preserva la separación de responsabilidades ya establecida en todo el proyecto (cada motor consume las salidas de otros, nunca las mezcla dentro de su propio cálculo base — el mismo principio que llevó a `MODEL-005` a usar símbolos nuevos en vez de reutilizar los de Confidence).
- **`Recomendación` (campo ya declarado en "Salida")** es la capa que sí integra `EV` con Confianza y Caos: un `EV` positivo calculado sobre un partido de Confianza baja o Caos alto debe **reportarse con el mismo número**, pero la Recomendación debe reflejar mayor cautela — nunca "ignorar" esos dos factores, tal como exige "Restricciones". Esta misión no fija la fórmula exacta de esa integración (sería fijar un peso sin evidencia estadística); documenta únicamente que el punto de integración correcto es la Recomendación, no el EV.

Esto responde, con evidencia textual del propio `engine/06`, a una pregunta que el stub original dejaba abierta.

---

# 11. Limitaciones

| Limitación | Explicación |
|---|---|
| Movimientos de mercado | La cuota se mueve dinámicamente según el flujo de apuestas de otros usuarios; el `EV` calculado refleja la cuota en el momento de la captura, no garantiza que siga vigente al momento de apostar |
| Cuotas desactualizadas | Relacionado con lo anterior: `cuotas.csv` incluye `fecha_captura` (esquema verificado en esta misión) precisamente porque una cuota puede quedar obsoleta antes de usarse — el modelo no valida por sí mismo si una cuota sigue vigente |
| Liquidez | Una cuota "de valor" puede no estar disponible para cualquier monto — las casas de apuestas limitan el stake aceptado en cuotas favorables al apostador; el `EV` es una medida por unidad, no garantiza que el monto deseado pueda apostarse a esa cuota |
| Margen de la casa (overround) | Ya fundamentado en la sección 5 — comparar `P_modelo` contra `P_implícita_bruta` (sección 8) sin normalizar (sección 8.2) subestima sistemáticamente el margen real de la casa |
| Closing Line Value no verificable en V1 | El concepto (sección 5) requeriría capturar y conservar la cuota de cierre real de cada partido para compararla contra la cuota usada por el modelo — `cuotas.csv` no tiene hoy ningún mecanismo de "cuota de cierre" distinto de la última fila capturada; queda como método de validación futura, no disponible todavía (sección 16) |
| Dependencia de `P_modelo` bien calibrada | Ya señalado en el stub original: si `engine/03` está mal calibrado, el `EV` calculado es matemáticamente correcto pero conceptualmente inútil — el Expected Value no puede detectar un error en la probabilidad de entrada, solo compararla con el mercado |
| No garantiza ganancias individuales | Ya señalado en el stub original, ahora fundamentado explícitamente en la Ley de los Grandes Números (sección 5) |

---

# 12. Compatibilidad

- **Con `MODEL-003` (Poisson):** `P_modelo` se reutiliza literalmente, sin recalcularla — misma relación de solo lectura que `MODEL-005` con la distribución de resultados.
- **Con `MODEL-004` (Confidence) y `MODEL-005` (Chaos):** consumidos como insumo de la Recomendación, nunca del `EV` numérico (sección 10) — resuelve, para este motor, la pregunta que `MODEL-004` y `MODEL-005` dejaron abierta sobre cómo se integran sus salidas en motores consumidores.
- **Con `engine/06` (texto actual, sin editarlo):** todos los términos de este documento (`EV`, `P_modelo`, `Probabilidad Implícita`, `Diferencia`, `Recomendación`) usan exactamente los nombres ya declarados en sus secciones "Definición", "Flujo del Motor" y "Salida" — ninguna sección de `engine/06` fue modificada ni contradicha.
- **Con el Contrato de Datos de Mercado (`INC-05`):** sigue sin diseñarse por completo. Este documento puede fundamentar la **estructura** de `c` y `P_implícita` porque el esquema físico de `cuotas.csv` ya existe (sección 6) — pero el contrato formal (validación, ciclo de vida, múltiples casas de apuestas) sigue pendiente, igual que lo dejó `MR-004`. Este motor es el único de los 6 cuya fórmula base depende de un dato todavía sin contrato completo (ver Cierre, pregunta 8).
- **Con `docs/25`/`docs/26` (Pipeline y Runtime):** el campo "Valor Esperado" que ambos documentos ya incluyen en su contrato de respuesta corresponde exactamente a la fórmula de la sección 7.2 — se corrige aquí una referencia del brief original de esta misión que citaba "`docs/26-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`" (nombre y número no coinciden: `docs/25` es el Trazado de Ejecución del Prediction Pipeline, `docs/26` es el Runtime del Modelo — verificado por listado directo del directorio antes de escribir este documento).

---

# 13. Ventajas

- Fórmula derivable en tres líneas desde primeros principios de valor esperado — sin necesidad de ningún supuesto adicional más allá de que `P_modelo` sea la probabilidad correcta.
- Mantiene el `EV` numérico puro (sección 10), evitando que Confianza y Caos se mezclen de forma no auditable dentro del cálculo base — la integración ocurre en un campo distinto y ya declarado (`Recomendación`).
- Reduce decisiones emocionales (ya señalado en el stub original) al formalizar exactamente qué compara y qué no compara.

---

# 14. Aplicación dentro del Modelo Santiago

Servirá como la fórmula base de `engine/06-Expected-Value.md`, consumida en su "Flujo del Motor" (Pasos 3 a 6). No influye en la generación de probabilidades de ningún otro motor (ya afirmado en el stub original, ahora fundamentado en la sección 9). Es, además, la pieza que finalmente permite auditar retroactivamente las predicciones (`docs/09-Auditoria.md`) comparando el `EV` calculado contra el resultado real y, cuando exista, contra la cuota de cierre (sección 11).

---

# 15. Referencias

- Kelly, J.L. (1956). "A New Interpretation of Information Rate." *Bell System Technical Journal*, 35(4), 917-926 — origen del Criterio de Kelly, referenciado en la sección 4 como perteneciente conceptualmente a la gestión de bankroll (fuera de alcance de este documento), no al cálculo de Expected Value.
- Levitt, S.D. (2004). "Why are Gambling Markets Organised So Differently from Financial Markets?" *The Economic Journal*, 114(495), 223-246 — fundamento de la discusión de eficiencia de mercados y margen de la casa (secciones 5 y 9).
- Miller, E. & Davidow, M. (2019). *The Logic of Sports Betting* — popularización del concepto de Closing Line Value (CLV) como estimador de referencia del precio "verdadero" de mercado (secciones 5 y 11).
- Ley de los Grandes Números — resultado clásico de teoría de la probabilidad, sin una fuente académica única citada, adoptado en la sección 5 para fundamentar por qué EV positivo no garantiza ganar una apuesta individual.
- `models/poisson.md` (`MODEL-003`) — fuente de `P_modelo`, reutilizada sin recalcular.
- `models/confidence.md` (`MODEL-004`) y `models/chaos-index.md` (`MODEL-005`) — insumos de la Recomendación (sección 10), no del `EV` numérico.

---

# 16. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a la existencia del Contrato de Datos de Mercado y a datos reales en `data/results/`:

- Diseño completo del Contrato de Datos de Mercado (`INC-05`, sección 12) — condición previa para que `engine/06` deje de leer `cuotas.csv` directamente.
- Adopción formal (o descarte justificado) de la normalización por margen de la sección 8.2 como parte obligatoria del Flujo del Motor.
- Mecanismo de captura de cuota de cierre en `cuotas.csv` (campo o fila adicional), condición previa para validar Closing Line Value (sección 11) empíricamente.
- Fórmula explícita de integración de Confianza/Caos en el campo `Recomendación` (sección 10), calibrada con evidencia estadística real, no con coeficientes arbitrarios.
- Diseño de `engine/07-Bankroll-Engine.md` y su propio `models/`, incluyendo si el Criterio de Kelly (sección 4) se adopta y con qué variante (Kelly completo, fraccional).

---

# Validaciones

- **¿El EV modifica alguna probabilidad?** No — `P_modelo` se lee de `engine/03` sin alteración (sección 7.2, 9).
- **¿El EV consume, sin modificar, Confidence y Chaos?** Sí — solo como insumo de `Recomendación`, nunca del `EV` numérico (sección 10).
- **¿Se mantiene el Engine desacoplado?** Sí, en el mismo grado que ya declaraba `engine/06` — la excepción de `cuotas.csv` (`INC-05`) no se amplía ni se resuelve aquí, se documenta (sección 12).
- **¿Es compatible con un futuro Contrato Oficial de Datos de Mercado?** Sí — la fórmula (sección 7) depende únicamente de `P_modelo` y `c`; de dónde provenga `c` (directamente de `cuotas.csv` hoy, de un contrato formal en el futuro) no altera la fórmula.

---

# Cierre obligatorio

**1. ¿Qué es el Expected Value y qué problema resuelve?**
Es la ventaja matemática esperada, por unidad apostada, de una apuesta concreta — compara la probabilidad del modelo con el precio que el mercado ofrece, algo que ningún otro motor del Engine calcula (secciones 2 y 3).

**2. ¿Cómo se distingue de Probabilidad y de Gestión de Bankroll?**
Probabilidad responde "¿qué puede pasar?" (`engine/03`); Expected Value responde "¿el precio del mercado compensa esa probabilidad?" (este documento); Gestión de Bankroll responde "¿cuánto arriesgar dado que hay ventaja?" (`engine/07`, futuro) — tres preguntas, tres componentes, nunca mezclados (sección 4).

**3. ¿Cuál es la fórmula estructural?**
`EV = (P_modelo · c) − 1`, con `P_implícita = 1/c` y `Δ_edge = P_modelo − P_implícita` (sección 7) — sin ningún coeficiente numérico fijado.

**4. ¿Cómo se interpreta sin inventar umbrales nuevos?**
Reutilizando las cinco categorías ya fijadas en la sección "Clasificación" de `engine/06` (sección 8), con una nota de prudencia explícita ante EV extremadamente alto, fundamentada en la eficiencia de mercados (sección 9).

**5. ¿Qué documentos deberán referenciar este modelo?**
`engine/06-Expected-Value.md` (implementación futura de su Versión 2.0), y cualquier documento futuro del Contrato de Datos de Mercado (`INC-05`).

**6. ¿Qué consumidor usará este resultado?**
`engine/06` directamente; `engine/07-Bankroll-Engine.md` (futuro) de forma indirecta, como precondición de su propio cálculo (sección 4).

**7. ¿Qué limitaciones detecté que no estaban en el stub original?**
Movimientos de mercado, liquidez, margen de la casa (overround) y Closing Line Value — ninguna de las cuatro estaba mencionada en el stub original, que solo señalaba calibración y no-garantía de ganancias individuales (sección 11).

**8. ¿Puede considerarse completo el núcleo matemático del Modelo Santiago después de MODEL-006?**
Parcialmente sí, parcialmente no, y ambas partes deben decirse con la misma precisión:

- **Sí, en un sentido estructural:** por primera vez, los 6 motores del Engine (`engine/01` a `06`) tienen un documento de `models/` que fundamenta su fórmula — la investigación previa que `CLAUDE.md` exige ("Investigación antes de implementación") existe ahora para el 100% del Engine, no solo para una parte.
- **No, en el sentido de "completo" como calibrado y verificado:** ningún coeficiente de ninguno de los 6 motores tiene valor numérico todavía (`CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística" — no hay evidencia estadística real porque `data/results/` sigue siendo un marcador de posición, `docs/27`). Y específicamente para este motor: el Contrato de Datos de Mercado (`INC-05`) sigue sin diseño completo, por lo que la mitad "de mercado" de `engine/06` (a diferencia de su mitad "de rendimiento deportivo", ya cubierta por `MODEL-001` a `005`) descansa todavía sobre una excepción arquitectónica documentada, no sobre una pieza terminada.

En síntesis: el núcleo matemático está **estructuralmente completo** por primera vez; **no está calibrado ni completamente desacoplado de sus fuentes de datos**. Ambas afirmaciones son ciertas a la vez y no se contradicen.

---

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/06`, el Engine en general, las Variables Oficiales, el Algoritmo, ni ningún otro documento de `docs/`.
- No se fija ningún valor numérico de coeficiente ni umbral de clasificación.
- No se diseña el Contrato de Datos de Mercado completo (`INC-05`) — se documenta su estado, no se resuelve.
- No se diseña `engine/07-Bankroll-Engine.md` ni el Criterio de Kelly aplicado — quedan referenciados como fuera de alcance conceptual (sección 4).

---

Fin del documento.
