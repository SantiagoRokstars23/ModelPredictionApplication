# Chaos Index — Índice de Caos

**Archivo:** `models/chaos-index.md`

**Misión:** MODEL-005 — Modelo Matemático del Chaos Index

**Versión:** 1.0.0-investigación

**Estado:** Investigación — primer documento de este archivo (no existía como stub previo, a diferencia de `MODEL-001` a `004`)

---

## Nota de origen

`engine/04-Chaos-Index.md` nunca tuvo un documento de `models/` correspondiente entre los 6 archivos originales del proyecto (`poisson.md`, `elo.md`, `expected-value.md`, `confidence.md`, `offensive-strength.md`, `defensive-strength.md`) — verificado directamente en el directorio antes de escribir. Este documento se crea desde cero, no evoluciona un stub, cerrando una brecha de "Investigación antes de implementación" (`CLAUDE.md`) que existía desde el diseño original del proyecto.

---

# 1. Objetivo

Desarrollar el fundamento matemático y conceptual del Índice de Caos — la base científica de `engine/04-Chaos-Index.md` — sin implementar código, sin modificar pesos ni el comportamiento del Engine.

---

# 2. Descripción — ¿Qué representa el Chaos Index?

**Qué mide:** qué tan susceptible es un partido concreto a desviarse del escenario esperado por el modelo — no la calidad de los datos que sustentan la predicción (eso es `MODEL-004`), sino la **volatilidad intrínseca** de ese encuentro específico: equipos parejos, alta exigencia competitiva (eliminación directa), plantillas inestables.

**Qué NO mide:** no mide si el modelo tiene suficiente información (eso es Confianza), y no mide quién va a ganar (eso es Probabilidad, de `engine/03`). Un partido puede tener **Confianza alta** (datos completos, plantillas estables, forma consistente) y **Caos alto** al mismo tiempo — por ejemplo, una final entre dos selecciones de nivel casi idéntico, con toda la información disponible: se sabe todo lo que hay que saber, y aun así el resultado es genuinamente difícil de anticipar. Caos y Confianza responden preguntas distintas y pueden moverse de forma independiente (sección 4).

**Por qué Chaos no representa "malos datos" ni "baja confianza":** un dato ausente reduce la Confianza (`MODEL-004`), pero no necesariamente aumenta el Caos — ausencia de datos es un problema de *información*, mientras que Caos describe la *naturaleza del partido en sí*, incluso bajo información perfecta.

---

# 3. Problema que Resuelve

Advertir, de forma explícita y separada de la probabilidad y de la confianza, cuándo un resultado favorito calculado por `engine/03` debe interpretarse con cautela adicional — no porque el cálculo esté mal fundamentado, sino porque el propio partido tiene una probabilidad estructuralmente mayor de sorprender.

---

# 4. Diferencia con Confidence

| | `engine/03` — Poisson | `engine/05` — Confidence | `engine/04` — Chaos |
|---|---|---|---|
| Pregunta que responde | ¿Qué podría pasar? | ¿Cuánto puedo confiar en ese cálculo? | ¿Qué tan volátil es este partido en sí? |
| Tipo de incertidumbre | Aleatoria (inherente al fútbol) | Epistémica (calidad/cantidad de datos) | Mayormente aleatoria, con un componente epistémico ya reconocido (sección 10) |
| Puede ser alto/bajo de forma independiente de los otros dos | — | Sí — datos completos no implican partido predecible | Sí — partido volátil no implica datos incompletos |

Ambos conceptos (Caos y Confianza) son **independientes por diseño** — `docs/06-Flujo-Operacional.md` ya los ejecuta en paralelo (Capa 3), precisamente porque ninguno depende del resultado del otro.

---

# 5. Fundamento matemático y literatura

**Entropía de Shannon como medida de incertidumbre de resultado.** Dado que `engine/03-Poisson.md` ya produce una distribución de probabilidad completa (Local/Empate/Visitante), existe una medida matemática estándar y bien establecida para cuantificar qué tan "incierta" es esa distribución: la entropía de Shannon (Shannon, 1948, "A Mathematical Theory of Communication", *The Bell System Technical Journal*) — cuanto más equiprobables son los tres resultados, mayor la entropía; cuanto más domina un resultado, menor. Es una herramienta de teoría de la información, no específica de fútbol, aplicada aquí sobre una distribución que el proyecto ya calcula, sin necesidad de una fuente de datos nueva.

**Balance competitivo.** La idea de que la "cercanía" entre competidores predice mayor incertidumbre de resultado tiene una tradición larga en la economía del deporte (la "hipótesis de incertidumbre de resultado", originada en la literatura sobre balance competitivo de ligas deportivas) — se usa aquí únicamente el concepto general (paridad ⇒ mayor incertidumbre), no un modelo económico de demanda de audiencia, que no es relevante para este documento.

---

# 6. Variables que aumentan el caos

*(Únicamente Variables Oficiales ya existentes — ninguna nueva.)*

| Variable | Efecto | Estado de disponibilidad (`docs/27`) |
|---|---|---|
| Distribución de probabilidad de `engine/03` (deriva de Variable001-004, indirectamente) | Mayor entropía (equipos parejos) → mayor caos base | Depende de `MODEL-001`/`002`/`003`, ya definidos |
| Variable006 (Disponibilidad de Plantilla) | Más lesiones/bajas → mayor caos | Derivable, con "Rotaciones" bloqueada (`DATA-001`) |
| Variable007 (Fatiga) | Menor descanso → mayor caos | Derivable |
| Variable001 (Forma Reciente) | Mayor inestabilidad/varianza reciente → mayor caos | Derivable |
| Variable012 (Factores Externos) | Condiciones externas adversas → mayor caos | Parcial — "Clima" bloqueado, "Altitud"/"Árbitro" disponibles (`DATA-001`) |

---

# 7. Construcción matemática

*(Estructura únicamente — ningún peso recibe valor numérico.)*

## 7.1 Base entrópica

```
H = − ( P_local·ln(P_local) + P_empate·ln(P_empate) + P_visitante·ln(P_visitante) )

H_max = ln(3)                          (máxima entropía posible: los tres resultados equiprobables)

H_norm = H / H_max ∈ [0, 1]

Base_Caos = 100 · H_norm
```

`P_local`, `P_empate`, `P_visitante` son, exactamente, la salida ya calculada por `engine/03-Poisson.md` (`MODEL-003`, sección 8) — no se recalculan aquí, se reutilizan directamente, consistente con que `docs/06` ya declara que `engine/04` "requiere Capa 1 + Capa 2" (Poisson incluido).

## 7.2 Ajustes contextuales (aditivos, acotados — no multiplicativos)

```
Chaos = clip( Base_Caos + Δ_disponibilidad + Δ_fatiga + Δ_forma + Δ_externos , 0, 100 )
```

Cada `Δ` es un término acotado (ej. rango simbólico `±Δ_max_x`, sin fijar el número) construido sobre Variable006, Variable007, Variable001 y Variable012 respectivamente.

**Decisión de diseño explícita, distinta de `MODEL-002`:** a diferencia de la reutilización literal de `M_forma`/`Pen` en `MODEL-002` (mismas variables, misma fórmula exacta), aquí se reutilizan las **variables** (Variable001, 006, 007 — las mismas que ya usa `MODEL-004`) pero con un **tratamiento matemático distinto**: aditivo sobre un piso entrópico, no multiplicativo sobre un techo de 100. La razón: Confidence responde "¿cuánto reducir mi confianza desde el máximo?"; Chaos responde "¿cuánta incertidumbre adicional existe sobre la que ya revela la propia distribución de probabilidad?" — son preguntas distintas aplicadas a las mismas variables, no el mismo cálculo repetido (ver sección 10).

---

# 8. Interpretación

`engine/04-Chaos-Index.md` **ya fija**, en su propia sección "Escala", las cinco bandas numéricas (0-20 Muy Bajo, 21-40 Bajo, 41-60 Moderado, 61-80 Alto, 81-100 Muy Alto, cada una con su interpretación) — este documento no las redefine, solo confirma que son compatibles con la estructura de la sección 7 y las relaciona con las categorías pedidas por esta misión (mapeando "Moderado" ↔ "Medio"), sin fijar ningún umbral nuevo:

| Categoría (esta misión) | Banda ya vigente (`engine/04`) |
|---|---|
| Muy bajo | 0-20 |
| Bajo | 21-40 |
| Medio | 41-60 (etiquetado "Moderado" en `engine/04`) |
| Alto | 61-80 |
| Muy alto | 81-100 |

---

# 9. Relación con Poisson

`engine/03-Poisson.md` genera la distribución de probabilidad. `engine/04-Chaos-Index.md` **nunca la reemplaza y nunca modifica directamente `λ`** — la consume como entrada de solo lectura (sección 7.1) y produce, en paralelo, un índice complementario. El Chaos Index no cambia ninguna probabilidad — únicamente informa qué tan susceptible es el partido a desviarse del escenario que esas probabilidades describen.

---

# 10. Relación con Confidence — solapamientos detectados

*(Verificación explícita pedida por esta misión — se documenta, no se resuelve modificando otros documentos.)*

Existe una superposición de variables **ya presente en el diseño original de ambos motores**, antes de esta misión y antes de `MODEL-004`: `engine/04` y `engine/05` comparten Variable001, Variable006 y Variable007 como entradas contextuales. Esta misión no introduce esa superposición — la hereda y la vuelve explícita:

| Variable compartida | Uso en Chaos (esta misión) | Uso en Confidence (`MODEL-004`) |
|---|---|---|
| Variable001 | `Δ_forma`: inestabilidad reciente **suma** incertidumbre | `C_forma`: inestabilidad reciente **resta** confianza |
| Variable006 | `Δ_disponibilidad`: bajas **suman** caos | `C_disponibilidad`: bajas **restan** confianza |
| Variable007 | `Δ_fatiga`: fatiga **suma** caos | `C_disponibilidad` (mismo factor): fatiga **resta** confianza |

Las mismas variables producen, matemáticamente, **direcciones de efecto coherentes entre sí** (más lesiones → más caos Y menos confianza, nunca lo contrario) — no hay contradicción lógica. Pero el hecho de que dos motores deriven, cada uno por su cuenta, un ajuste a partir de las mismas tres variables es una duplicidad de cálculo real, del mismo tipo ya señalado en `docs/15`/`docs/17` para "Rotaciones". **No se resuelve aquí** — modificar `engine/04` o `engine/05` para centralizar este cálculo está fuera del alcance de esta misión ("no modificar el Engine").

Adicionalmente, ya señalado en `MODEL-004`: `Base_Caos` (entropía) y `C_diferencia` (diferencia de Fuerza Ofensiva/Defensiva, `MODEL-004`) capturan el mismo fenómeno general ("equipos parejos") por **rutas matemáticas distintas** (entropía de una distribución vs. diferencia directa de índices) — ninguna reemplaza a la otra, pero ambas existen.

---

# 11. Limitaciones

| Limitación | Explicación |
|---|---|
| Eventos extraordinarios | Ninguna variable de la sección 6 anticipa un evento único e irrepetible (una lesión de una estrella en el calentamiento, por ejemplo) |
| Expulsiones | Cambian la dinámica *durante* el partido; el Chaos Index es un pronóstico *previo* al inicio — no se actualiza en vivo. Un "Índice disciplinario" (ya identificado como no diseñado, `docs/28`, Categoría E) podría mejorar esta limitación en el futuro, como proxy previo de riesgo de expulsión, pero no la elimina |
| Penales (tanda) | Proceso completamente distinto al modelo de goles de Poisson del que deriva `Base_Caos` — fuera de alcance por naturaleza |
| Errores arbitrales | Imposibles de anticipar por definición; la categoría/confederación del árbitro (`arbitros.csv`, ya disponible vía Variable012) es, a lo sumo, un proxy débil de rigor esperado, no un predictor de errores |
| Goles tempranos | Un gol en los primeros minutos altera la dinámica del resto del partido de forma que el `λ` fijo (pre-partido) no captura — el Chaos Index puede señalar mayor probabilidad de un partido volátil, pero no predice el momento ni el efecto específico de un gol temprano |
| Factores imposibles de anticipar | Decisiones tácticas de última hora, motivación extra-deportiva — misma limitación epistémica ya reconocida en `MODEL-004`, aplicable aquí también |

---

# 12. Compatibilidad

- **Con `MODEL-001`/`002`:** `Base_Caos` no usa Fuerza Ofensiva/Defensiva directamente — las consume indirectamente vía la distribución de `engine/03`, consistente con `docs/17` (`engine/04` requiere Capa 1 solo transitivamente, a través de Poisson).
- **Con `MODEL-003`:** reutiliza literalmente `P_local`/`P_empate`/`P_visitante`, sin recalcularlas — consistente con que `docs/06` ya declara esa dependencia.
- **Con `MODEL-004`:** comparte variables, no cálculos — documentado explícitamente en la sección 10, no oculto ni resuelto.
- **Con `engine/04` (texto actual, sin editarlo):** las cuatro categorías que `engine/04` ya declara (Deportivos, Contextuales, Disponibilidad, Información) se corresponden con los términos de la sección 7 así: Deportivos ↔ `Base_Caos` + `Δ_forma`; Contextuales ↔ `Δ_externos` + parte de `Δ_disponibilidad` (rotaciones); Disponibilidad ↔ `Δ_disponibilidad`. La categoría **"Información"** de `engine/04` ("pocos partidos disponibles", "datos incompletos", "cambios de entrenador", "cambios tácticos") **no tiene componente matemático correspondiente en esta fórmula** — no existe hoy una Variable Oficial activa que la represente (Compatibilidad Táctica, `Variable005`, sigue diferida). Se documenta como limitación honesta, no se inventa un término para cubrirla.
- **Con `docs/17`/`docs/28`:** ninguna variable usada excede lo ya asignado a `engine/04`; "Índice de Caos" (`docs/28`, Categoría D) pasa de "Pendiente" a estructura definida, sin editar el catálogo.

---

# 13. Ventajas

- Reutiliza una salida ya calculada (`engine/03`) en lugar de re-derivar "cercanía entre equipos" desde cero — más eficiente y mejor fundamentado matemáticamente (entropía) que una simple resta de índices.
- Estructura aditiva sobre un piso entrópico, distinta de la multiplicativa de Confidence — permite que ambos motores compartan variables sin producir literalmente el mismo número.
- Documenta honestamente su propia brecha (categoría "Información" de `engine/04` sin cobertura matemática) en lugar de forzar una variable que no existe.

---

# 14. Aplicación dentro del Modelo Santiago

Acompaña a cada predicción de `engine/03` con una advertencia estructurada de volatilidad — insumo directo para `engine/06-Expected-Value.md` (que ya declara "Ignorar el Índice de Caos" entre sus restricciones) y para el Bankroll Manager, si se solicita.

---

# 15. Referencias

- Shannon, C.E. (1948). "A Mathematical Theory of Communication." *The Bell System Technical Journal*, 27(3), 379-423 — origen de la entropía como medida de incertidumbre, adoptada en la sección 7.1.
- Literatura de balance competitivo / "hipótesis de incertidumbre de resultado" en economía del deporte — concepto general adoptado (paridad ⇒ incertidumbre), sin una fuente académica única citada.
- `models/poisson.md` (`MODEL-003`) — fuente de `P_local`/`P_empate`/`P_visitante`, reutilizadas sin recalcular.
- `models/confidence.md` (`MODEL-004`) — comparación directa de estructura, sección 10.

---

# 16. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a datos reales suficientes en `data/results/`:

- Calibración de todos los `Δ` de la sección 7.2.
- Validación empírica de si la entropía normalizada realmente correlaciona con sorpresas observadas (resultados que se desvían del favorito).
- Decisión arquitectónica (fuera de esta misión) sobre si centralizar el cálculo de Variable001/006/007 compartido entre `engine/04` y `engine/05` en la Capa de Preparación de Variables, en lugar de que cada motor lo derive por separado (sección 10).
- Diseño, si se aprueba en el futuro, de un "Índice disciplinario" (`docs/28`) que cubra parcialmente la limitación de expulsiones (sección 11).

---

# Validaciones

- **¿Chaos es independiente de Confidence?** Sí — ambos consumen variables compartidas pero no el resultado del otro; se ejecutan en paralelo (Capa 3, `docs/06`) sin dependencia mutua.
- **¿No existe dependencia circular?** Confirmado — Chaos depende de Poisson (Capa 2, anterior); Poisson no depende de Chaos.
- **¿Reutiliza únicamente Variables Oficiales?** Sí — Variable001, 006, 007, 012, más la distribución ya calculada por `engine/03` (que a su vez deriva de Variables Oficiales ya establecidas en `MODEL-001`/`002`).
- **¿No modifica directamente Poisson?** Confirmado — sección 9, `Base_Caos` lee la distribución, nunca la escribe.

---

# Cierre obligatorio

**1. ¿Qué mide realmente el Chaos Index?**
La volatilidad intrínseca de un partido específico — qué tan susceptible es de desviarse del escenario esperado, combinando la entropía de la propia distribución de probabilidad con ajustes contextuales de disponibilidad, fatiga, forma y factores externos.

**2. ¿En qué se diferencia de Confidence?**
Chaos pregunta "¿qué tan volátil es este partido?" (mayormente aleatorio); Confidence pregunta "¿cuánto puedo confiar en el cálculo?" (epistémico) — pueden ser altos o bajos de forma completamente independiente (sección 4).

**3. ¿Qué variables aumentan el caos?**
Variable001 (inestabilidad de forma), Variable006 (menor disponibilidad), Variable007 (mayor fatiga), Variable012 (factores externos adversos) — todas ya existentes, más la entropía de la distribución de `engine/03`.

**4. ¿Qué documentos deberán referenciar este modelo?**
`engine/04-Chaos-Index.md` (implementación futura), `engine/06-Expected-Value.md` (ya declara no ignorar el Caos), y `docs/28` (actualización futura de "Índice de Caos" a estado "Parcial").

**5. ¿Qué componente consumirá este resultado?**
`engine/06-Expected-Value.md` directamente; indirectamente, el Bankroll Manager.

**6. ¿Qué posibles solapamientos detectaste?**
Dos: (a) Variable001/006/007 compartidas con Confidence, con tratamiento matemático distinto (aditivo vs. multiplicativo) pero mismo origen de dato — sección 10; (b) la categoría "Información" que `engine/04` ya declaraba en su propio texto no tiene, hoy, ningún componente matemático correspondiente en esta fórmula, por falta de una Variable Oficial activa que la represente.

**7. ¿Qué parte del modelo matemático queda pendiente?**
Todos los coeficientes de la sección 7.2, la validación empírica de la entropía como predictor real de sorpresas, y la decisión arquitectónica (fuera de esta misión) sobre centralizar el cálculo de las variables compartidas con Confidence.

**8. ¿Puede Expected Value construirse completamente después de este documento?**
No completamente. Con `MODEL-001` a `005`, el lado de *rendimiento deportivo* de `engine/06` (Probabilidad, Confianza, Caos) ya está conceptualmente fundamentado. Pero `engine/06` también depende de las cuotas de mercado, cuyo Contrato de Datos de Mercado sigue pendiente de diseño completo (`INC-05`, "resuelto en principio" desde `MR-004`, no en implementación) — `models/expected-value.md` necesitará, además de esta base, esa pieza todavía sin resolver.

---

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/04`, el Engine en general, las Variables Oficiales, ni `docs/28`.
- No se fija ningún valor numérico de coeficiente.
- No se resuelve la duplicidad de cálculo de Variable001/006/007 entre `engine/04` y `engine/05` — se documenta, no se corrige.
- No se diseña el "Índice disciplinario" mencionado como mejora futura en la sección 11.

---

Fin del documento.
