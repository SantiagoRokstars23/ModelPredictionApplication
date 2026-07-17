# Confidence Index — Índice de Confianza

**Archivo:** `models/confidence.md`

**Misión:** MODEL-004 — Modelo Matemático de Confidence

**Versión:** 2.0.0-investigación

**Estado:** Investigación — estructura conceptual completa; coeficientes **pendientes de calibración estadística**, conforme a `CLAUDE.md`

---

## Corrección detectada antes de escribir

El stub anterior de este documento listaba "Índice de Caos" como variable candidata de Confidence. Verificado contra `docs/06-Flujo-Operacional.md` ("Diagrama de dependencias del Engine"): `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` se ejecutan **en paralelo** dentro de la Capa 3 — ninguno puede depender de la salida del otro, o no podrían ejecutarse simultáneamente. Confirmado también contra el texto actual de `engine/05` (sección "Entradas"): no menciona Chaos en absoluto. Esta fórmula **no usa el Índice de Caos** como entrada, para no contradecir la arquitectura ya establecida.

---

# 1. Objetivo

Desarrollar el fundamento matemático y conceptual del Índice de Confianza — la base científica de `engine/05-Confidence.md` — sin implementar código, sin modificar pesos ni el comportamiento del Engine.

---

# 2. Descripción — ¿Qué significa "confianza"?

**Probabilidad** (producida por `models/poisson.md`) es la mejor estimación del modelo sobre la *probabilidad de cada resultado*, dado el estado actual de ambos equipos. **Confianza** es un juicio de segundo nivel: *qué tan bien fundamentada está esa estimación misma* — no responde "¿quién va a ganar?", responde "¿qué tanto puedo confiar en el número que acabo de calcular?".

La distinción formal, tomada de la literatura de incertidumbre estadística (no inventada para este proyecto): **incertidumbre aleatoria** (inherente al fenómeno — incluso con información perfecta, un partido parejo puede terminar de cualquier forma) frente a **incertidumbre epistémica** (derivada de cuánto y qué tan buena es la información disponible para el modelo — datos faltantes, muestras pequeñas, plantilla inestable). La Probabilidad de Poisson ya incorpora la incertidumbre aleatoria (por eso entrega una distribución, no un único resultado). **La Confianza mide, específicamente, la incertidumbre epistémica** — cuánto del cálculo descansa sobre información sólida frente a información ausente o escasa.

---

# 3. Problema que Resuelve

Traducir múltiples señales de calidad y estabilidad de la información —completitud de datos, disponibilidad de plantilla, consistencia de forma reciente— en una única puntuación que acompañe a la predicción, sin alterarla.

---

# 4. Fundamento estadístico

**Qué mide:** el grado en que la Fuerza Ofensiva, la Fuerza Defensiva y los `λ` de Poisson descansan sobre datos completos, recientes y estables.

**Qué NO mide:**
- Quién va a ganar — eso es responsabilidad exclusiva de `engine/03-Poisson.md`.
- Qué tan impredecible es el partido en sí (equipos parejos, eliminación directa) — ese es el objeto de `engine/04-Chaos-Index.md`, un motor **paralelo y conceptualmente distinto**: Chaos pregunta "¿qué tan volátil es el resultado?"; Confidence pregunta "¿qué tan sólidos son mis datos?". Ambos pueden, de forma independiente, usar señales relacionadas con "equipos de nivel similar" — es una superposición conceptual que ya existía en el diseño original de ambos motores (`engine/04`, "Deportivos: equipos de nivel similar"; ver Compatibilidad, sección 11) y que esta misión no resuelve, por no estar autorizada a modificar `engine/04`.

**Marco teórico general:** la separación entre qué tan *nítida* (sharp) es una predicción y qué tan *calibrada* (calibrated, verificablemente correcta con el tiempo) está, es un tema establecido en la literatura de verificación de pronósticos probabilísticos (ej. Gneiting, Balabdaoui y Raftery, 2007, "Probabilistic Forecasts, Calibration and Sharpness", *Journal of the Royal Statistical Society: Series B*). Este documento define la **estructura** de la Confianza declarada; si esa Confianza declarada es honesta (bien calibrada) solo puede verificarse después, con resultados reales — responsabilidad ya asignada a `learning/confidence-calibration.md` (existente desde `MS-003`), no a este documento.

---

# 5. Variables que afectan la confianza

*(Todas ya existentes — ninguna nueva, conforme a la restricción de esta misión.)*

| Señal | Efecto | Origen | Ya usada por `engine/05` |
|---|---|---|---|
| Completitud de las Variables Oficiales | A mayor proporción de variables "disponibles" (no marcadas como faltantes), mayor confianza | Estado de cada Variable Oficial, ya expuesto en el Objeto de Contexto (`docs/26`, sección 3) | Corresponde a "Calidad de los datos disponibles" |
| Disponibilidad de Plantilla (Variable006) | A menor disponibilidad, menor confianza | Reutilizada de `MODEL-001`/`MODEL-002` (mismo rol que en `Pen`) | Sí — "Lesiones confirmadas, Suspensiones, Rotaciones esperadas" |
| Fatiga (Variable007) | A mayor fatiga, menor confianza | Reutilizada de `MODEL-001`/`MODEL-002` | Sí — "Estado físico de los equipos" |
| Estabilidad de Forma Reciente (Variable001) | A mayor variabilidad de resultados recientes, menor confianza | Momento de segundo orden (varianza) de una variable ya usada, no un dato nuevo | Coherente con el propósito ya declarado de `engine/05` |
| Diferencia de nivel entre equipos | A equipos más parejos, menor confianza en el resultado puntual | Fuerza Ofensiva/Defensiva, ya calculadas por `engine/01`/`02` | Sí — "Analizar la diferencia de nivel entre ambos equipos" (Paso 2 de `engine/05`) |
| Historial Directo (Variable010) | Ajuste fino, acotado — nunca decisivo | Ya asignada a `engine/05` por `MR-004` | Sí |

---

# 6. Construcción conceptual

*(Estructura únicamente — ningún peso recibe valor numérico.)*

```
Confianza = clip( 100 · C_datos · C_disponibilidad · C_forma · C_diferencia + Δ_historial , 0, 100 )
```

Donde cada factor `C_x ∈ [0,1]` solo puede **reducir** la confianza desde el techo de 100 — nunca aumentarla artificialmente:

- **`C_datos`**: proporción de Variables Oficiales relevantes que llegaron "disponibles" (no marcadas como faltantes) en el Objeto de Contexto. `C_datos = 1` si todo está disponible; disminuye proporcionalmente con cada ausencia declarada.
- **`C_disponibilidad`**: función decreciente de Variable006 y Variable007 — **misma pareja de variables que `Pen` en `MODEL-001`/`MODEL-002`**, reutilizada aquí también, para no triplicar el mismo cálculo en tres motores distintos.
- **`C_forma`**: función decreciente de la varianza reciente de Variable001 — forma muy errática reduce la confianza en que el nivel actual del equipo esté bien capturado.
- **`C_diferencia`**: función creciente de la diferencia absoluta entre Fuerza Ofensiva/Defensiva de ambos equipos — mayor diferencia, mayor confianza en el favoritismo calculado; equipos muy parejos, menor confianza puntual (sin decir *cuál* ganará, solo que el margen es estrecho).
- **`Δ_historial`**: ajuste aditivo pequeño y acotado a partir de Variable010 — aditivo, no multiplicativo, y con un rango simbólico reducido, para que "nunca deberá dominar el cálculo" (`engine/05`, ya declarado) se cumpla por construcción, no por disciplina.

---

# 7. Interpretación

`docs/02-modelo.md`, sección 7, **ya fija** la escala numérica de Confianza (90-100 / 80-89 / 70-79 / 60-69 / <60) — este documento no la redefine, solo confirma que es compatible con la estructura de la sección 6 y la relaciona con las cinco categorías cualitativas pedidas por esta misión, sin fijar ningún umbral nuevo:

| Categoría | Banda ya vigente (`docs/02-modelo.md`) |
|---|---|
| Muy alta | 90-100 |
| Alta | 80-89 |
| Media | 70-79 |
| Baja | 60-69 |
| Muy baja | <60 |

---

# 8. Relación con Poisson

`engine/03-Poisson.md` genera las probabilidades. `engine/05-Confidence.md` **nunca las reemplaza, nunca las ajusta y nunca las recalcula** — evalúa, en paralelo, qué tan bien fundamentadas están. Ambas salidas se entregan juntas al usuario (`docs/14`/`docs/25`/`docs/26`, contrato de respuesta): la probabilidad dice *qué* podría pasar; la confianza dice *cuánto confiar* en ese cálculo. La decisión de actuar o no sobre una probabilidad de baja confianza pertenece al usuario o al Bankroll Manager (fuera del núcleo, `CLAUDE.md`) — nunca a este modelo.

---

# 9. Limitaciones

| Limitación | Explicación |
|---|---|
| Incertidumbre imposible de medir | Decisiones tácticas de último minuto, estado anímico real de los jugadores — ningún dato de la Base de Conocimiento las captura, ni siquiera indirectamente |
| Eventos inesperados | Una lesión ocurrida *después* de construir el Objeto de Contexto no puede reflejarse — la Confianza solo captura la incertidumbre conocida en el momento del cálculo |
| Errores humanos en la captura de datos | Un dato mal registrado (no ausente, sino incorrecto) es indistinguible de un dato correcto para este modelo — `C_datos` solo detecta ausencia declarada, nunca error silencioso |
| Información incompleta pero no crítica | Bien capturada por `C_datos`; lo que no está cubierto es la información que ni siquiera se sabe que falta (ej. "Grandes oportunidades", `MODEL-001`/`DATA-001` — su ausencia ya está descontada del cálculo de Fuerza Ofensiva, pero el propio Índice de Confianza no tiene forma de saber que ese componente específico falta, solo que Variable003 se construyó con menos información de la ideal) |

---

# 10. Compatibilidad

- **Con `MODEL-001`/`MODEL-002`:** `C_disponibilidad` reutiliza exactamente Variable006/007, mismas variables que `Pen` — tercera reutilización consecutiva de este par (`engine/01`, `02`, ahora `05`), evitando triplicar el cálculo.
- **Con `MODEL-003`:** no consume el valor numérico de `λ` ni de las probabilidades — solo necesita saber que Poisson pudo ejecutarse; la fórmula de Confianza es independiente del resultado de Poisson, no de su ejecución.
- **Con `engine/05` (texto actual, sin editarlo):** las seis señales de la sección 5 corresponden exactamente a lo que su sección "Entradas" ya declara — sin el Índice de Caos que el stub anterior de este mismo documento sugería incorrectamente (ver "Corrección detectada antes de escribir").
- **Con `docs/17`:** ninguna variable usada aquí excede lo que esa matriz ya asigna a `engine/05`.
- **Con `docs/28`:** "Índice de Confianza" ya está catalogado (Categoría D, "Pendiente") — esta misión le da estructura, sin editar el catálogo (fuera de alcance).

---

# 11. Ventajas

- Nunca puede superar 100 ni caer bajo 0 por construcción — el `clip` y la naturaleza multiplicativa de los factores lo garantizan.
- Reutiliza variables ya definidas tres veces (Variable006/007, ahora en `engine/01`, `02` y `05`) en lugar de triplicar su cálculo — mismo principio de diseño ya aplicado en `MODEL-002`.
- Separa con precisión conceptual la incertidumbre epistémica (Confianza) de la aleatoria (ya capturada por la propia distribución de Poisson) y de la volatilidad del partido (Chaos, motor distinto).

---

# 12. Aplicación dentro del Modelo Santiago

Acompaña a cada predicción de `engine/03` con un juicio de fiabilidad — insumo directo para `engine/06-Expected-Value.md` (ya declarado en su propio texto: "Ignorar el Nivel de Confianza" está en su lista de restricciones) y para `learning/confidence-calibration.md`, que verificará después, con resultados reales, si la Confianza declarada aquí fue honesta.

---

# 13. Referencias

- Gneiting, T., Balabdaoui, F., y Raftery, A.E. (2007). "Probabilistic Forecasts, Calibration and Sharpness." *Journal of the Royal Statistical Society: Series B (Statistical Methodology)*, 69(2), 243-268.
- Der Kiureghian, A. y Ditlevsen, O. (2009). "Aleatory or epistemic? Does it matter?" *Structural Safety*, 31(2), 105-112 — origen de la distinción aleatoria/epistémica adoptada en la sección 2.
- `models/offensive-strength.md`, `models/defensive-strength.md` (`MODEL-001`, `MODEL-002`) — fuente de `C_disponibilidad`, reutilizado sin cambios.

---

# 14. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a datos reales suficientes en `data/results/` y a que `learning/confidence-calibration.md` tenga suficientes predicciones cerradas para evaluar:

- Calibración de todos los coeficientes de la sección 6.
- Validación empírica de si la Confianza declarada corresponde a la frecuencia real de acierto (curva de calibración) — la pregunta central que `learning/confidence-calibration.md` ya está diseñado para responder.
- Revisión de si la superposición conceptual entre `C_diferencia` (aquí) y el factor "equipos de nivel similar" de `engine/04` (Chaos) debería resolverse arquitectónicamente — señalada en la sección 4, no resuelta en esta misión.

---

# Validaciones

- **¿Confidence nunca reemplaza a Poisson?** Confirmado — sección 8: ambas salidas se entregan por separado, ninguna modifica a la otra.
- **¿Solo evalúa la calidad de la predicción?** Sí — ningún término de la fórmula (sección 6) calcula una probabilidad de resultado; todos son factores de calidad/estabilidad de la información.
- **¿Reutiliza exclusivamente Variables Oficiales?** Sí — Variable001, 006, 007, 010, más el estado de completitud ya expuesto por el Objeto de Contexto (`docs/26`) y las salidas ya calculadas de `engine/01`/`02` — ninguna variable nueva.

---

# Cierre obligatorio

**1. ¿Qué mide realmente Confidence?**
La incertidumbre epistémica de la predicción — qué tan completos, recientes y estables son los datos que la sustentan, no la incertidumbre inherente del resultado del partido.

**2. ¿Qué diferencia existe entre probabilidad y confianza?**
La probabilidad es la estimación del resultado en sí (incertidumbre aleatoria, ya incorporada en la distribución de Poisson); la confianza es un juicio de segundo nivel sobre qué tanto se puede confiar en esa estimación (incertidumbre epistémica) — sección 2.

**3. ¿Qué variables aumentan o reducen la confianza?**
Completitud de datos, Disponibilidad de Plantilla y Fatiga (reducen si son desfavorables), estabilidad de Forma Reciente, diferencia de nivel entre equipos, e Historial Directo como ajuste menor acotado — sección 5, todas ya existentes.

**4. ¿Qué documentos deberán referenciar este modelo?**
`engine/05-Confidence.md` (implementación futura), `engine/06-Expected-Value.md` (ya declara que nunca debe ignorar la Confianza), `learning/confidence-calibration.md` (verificará si es honesta con datos reales), y `docs/28` (actualización futura de "Índice de Confianza" a estado "Parcial").

**5. ¿Qué componente consumirá este resultado?**
`engine/06-Expected-Value.md` directamente (ya lo declara en sus restricciones); indirectamente, el Bankroll Manager, si el usuario lo solicita.

**6. ¿Qué misión recomendarías después?**
`models/chaos-index.md` — completaría los tres motores de la Capa 3-4 restantes (Chaos, Confidence ya hecho, Expected Value), y permitiría, de paso, revisar formalmente la superposición conceptual con `C_diferencia` señalada en la sección 4.

**7. ¿Qué parte del modelo matemático queda pendiente?**
Todos los coeficientes numéricos de la sección 6, y la validación empírica de calibración — ambas dependen de datos reales que hoy no existen en `data/results/`.

---

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/05`, el Engine en general, las Variables Oficiales, ni `docs/28`.
- No se fija ningún valor numérico de coeficiente.
- No se resuelve la superposición conceptual con `engine/04-Chaos-Index.md` — se documenta, no se corrige.

---

Fin del documento.
