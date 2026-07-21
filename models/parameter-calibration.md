# Parameter Calibration — Calibración Oficial de Parámetros del Modelo Santiago

**Archivo:** `models/parameter-calibration.md`

**Misión:** MODEL-008 — Calibración Oficial de Parámetros del Modelo Santiago

**Versión:** 1.0.0-investigación

**Estado:** Investigación — procedimiento metodológico completo; **ningún parámetro se calibra en esta misión**, conforme a su propio alcance

---

# Nota de origen

`MODEL-001` a `MODEL-007` definieron la estructura matemática completa de los 6 motores del Engine, deliberadamente sin fijar ningún valor numérico ("Nunca alterar pesos sin evidencia estadística", `CLAUDE.md`). Esto deja simbólicos más de veinte parámetros distintos, repartidos en seis documentos, sin que ninguno de ellos defina **cómo** se pasará, algún día, de símbolo a número. Este documento — el primero de `models/` que no fundamenta un motor sino un **procedimiento transversal** — cierra ese vacío: cataloga los parámetros existentes, distingue sus tipos, define su origen legítimo, y formaliza el ciclo completo de calibración, sin calibrar nada todavía.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué NO repite este documento |
|---|---|---|
| `models/offensive-strength.md`, `defensive-strength.md`, `poisson.md`, `confidence.md`, `chaos-index.md`, `expected-value.md` | Cada fórmula, con sus parámetros simbólicos propios | Ninguna fórmula se modifica — este documento las cataloga (sección 4), no las redefine |
| `learning/error-analysis.md`, `pattern-discovery.md`, `confidence-calibration.md`, `weight-adjustment.md`, `version-history.md` | El pipeline completo de aprendizaje: diagnóstico → patrón → calibración de Confianza → propuesta → historial | No se redefine ningún documento ni su responsabilidad — este documento identifica la única pieza que ese pipeline todavía no especifica: **con qué método matemático** `weight-adjustment.md` calculará, en su implementación futura, "cuál sería el peso propuesto" |
| `docs/10-Aprendizaje.md` | Ejemplo mínimo ya vigente (marcador de resultado → ajuste cualitativo) | No se amplía ese documento — se referencia como evidencia de que el principio ("ver qué pasó, ajustar con evidencia") ya existía de forma embrionaria |
| `docs/21-Constitucion-del-Modelo-Santiago.md` | Art. 2.5 ("Evidencia antes que opinión"), Art. 2.9 ("No autoaprobación"), Art. 5 (roles), Art. 9 (versión técnica vs. narrativa), Art. 11 (calidad: declarar insuficiencia, nunca inventar) | Ningún principio se redefine — este documento es la aplicación concreta de todos ellos al caso específico de la calibración de parámetros |

Ninguna inconsistencia detectada durante este análisis — el pipeline de `learning/` y los seis documentos de `models/` son mutuamente consistentes; este documento solo llena el hueco entre ambos.

---

# 1. Objetivo

Diseñar el procedimiento oficial mediante el cual el Modelo Santiago obtendrá, validará y actualizará todos sus parámetros matemáticos — sin calibrar ninguno, sin implementar código, sin asignar un solo valor numérico.

**Por qué el Modelo Santiago necesita calibración:** las siete investigaciones anteriores (`MODEL-001` a `007`) dejaron más de veinte símbolos sin valor (sección 4) precisamente porque `CLAUDE.md` prohíbe fijarlos sin evidencia. Sin un procedimiento único, cada futura implementación de código podría calibrar cada motor con un método distinto, sin partición de datos consistente, sin métrica de validación common, o — el riesgo real que este documento existe para prevenir — con un ajuste manual conveniente disfrazado de "calibración". Este documento es la garantía de que, cuando exista suficiente historial real, la transición de símbolo a número seguirá siempre el mismo camino auditable.

---

# 2. Qué es un parámetro

| Concepto | Definición | Ejemplo ya existente |
|---|---|---|
| **Variable Oficial** | Un dato normalizado, validado y preparado por la Capa de Preparación de Variables (`docs/15`/`docs/16`) que entra al Engine como **entrada observada** de un partido concreto — nunca se calibra, se mide | Variable001 (Forma Reciente), Variable009 (Localía) |
| **Parámetro matemático** | Cualquier símbolo introducido por una fórmula de `models/` que no es una Variable Oficial ni un dato físico — necesita un valor numérico, estimado con evidencia, para que la fórmula sea ejecutable | `μ_gol`, `s`, cualquier `vᵢ` |
| **Peso** | Subtipo de parámetro que pondera la contribución relativa de dos o más términos dentro de una combinación — importa su magnitud *relativa* frente a otros pesos, no solo su valor absoluto | `w_R`, `w_T` (`MODEL-001`, ponderan Forma Reciente vs. Rendimiento en el Torneo dentro de `M_forma`) |
| **Restricción** | Un límite estructural que acota el rango de una salida o de otro parámetro — no pondera nada entre sí, solo impone un piso o un techo | `δ_max`, `Pen_max` (`MODEL-001`); `λ_min`, `λ_max` (`MODEL-007`) |
| **Constante** | Un valor fijo derivado de la propia estructura matemática — **no se calibra nunca**, porque no es una estimación estadística sino un hecho matemático | `H_max = ln(3)` (`MODEL-005`) — la entropía máxima posible de tres resultados equiprobables; es aritmética, no evidencia |

**Por qué esta distinción importa:** confundir una Constante con un Parámetro llevaría a "calibrar" algo que no requiere datos (perdiendo tiempo y arriesgando reintroducir un valor incorrecto donde ya existía uno matemáticamente exacto); confundir un Peso con una Restricción llevaría a optimizarlo de forma incorrecta (un peso se ajusta para maximizar ajuste a los datos; una restricción se fija para proteger un caso límite, no para "ajustar mejor").

---

# 3. Problema que resuelve

Sin este documento, la calibración de cada uno de los 6 motores quedaría librada a una decisión ad-hoc de la primera implementación de código real — sin garantía de que use el mismo método, la misma partición de datos, o el mismo criterio de validación entre un motor y otro, y sin ninguna barrera documental explícita contra el ajuste manual conveniente. Este documento fija el procedimiento **antes** de que exista esa tentación, no después.

---

# 4. Catálogo oficial de parámetros

*(Inventario completo de los seis documentos de `models/` — ningún valor numérico se asigna.)*

## `models/offensive-strength.md` (`MODEL-001`)

| Símbolo | Tipo | Rol |
|---|---|---|
| `vᵢ` (uno por métrica: xG, disparos, disparos al arco, grandes oportunidades, conversión) | Peso | Ponderación de cada métrica dentro de `Z` (sección 6.1 de ese documento) |
| `s` | Restricción/escala | Factor de escala de `Φ(Z/s)` |
| `w_R`, `w_T` | Peso | Ponderación de Forma Reciente vs. Rendimiento en el Torneo dentro de `M_forma` |
| `δ_max` | Restricción | Límite del modificador de forma |
| `w_D`, `w_F`, `w_Q` | Peso | Ponderación de Disponibilidad/Fatiga/Calidad de Plantilla dentro de `Pen` |
| `Pen_max` | Restricción | Techo de la penalización |
| `N` | Parámetro (ventana temporal) | Número de partidos recientes considerados |

## `models/defensive-strength.md` (`MODEL-002`)

| Símbolo | Tipo | Rol |
|---|---|---|
| `vᵢ'` (uno por métrica: xGA, goles recibidos, remates permitidos, porterías en cero) | Peso | Análogo a `vᵢ`, símbolos propios |
| `M_forma`, `Pen` (con `w_R`, `w_T`, `δ_max`, `w_D`, `w_F`, `w_Q`, `Pen_max`) | — | **Reutilizados sin redefinir** de `MODEL-001` — no son parámetros nuevos, es la misma calibración compartida |

## `models/poisson.md` (`MODEL-003`/`MODEL-007`)

| Símbolo | Tipo | Rol |
|---|---|---|
| `μ_gol` | Parámetro (dinámico por competición) | Promedio histórico de goles por equipo por partido |
| `κ`, `κ'` | Peso/ajuste | Magnitud del ajuste de Localía (local/visitante) |
| `λ_min`, `λ_max` | Restricción | Piso y techo de `λ` (`MODEL-007`) |

## `models/confidence.md` (`MODEL-004`)

| Símbolo | Tipo | Rol |
|---|---|---|
| `C_datos`, `C_disponibilidad`, `C_forma`, `C_diferencia` | Parámetro (funciones, no coeficientes nombrados individualmente todavía) | Cada uno descrito solo cualitativamente ("función creciente/decreciente") — **sin nombres de peso propios**, a diferencia de `MODEL-001`/`002` (ver sección 9, limitación) |
| `Δ_historial` | Restricción | Rango acotado del ajuste por Historial Directo, deliberadamente pequeño |

## `models/chaos-index.md` (`MODEL-005`)

| Símbolo | Tipo | Rol |
|---|---|---|
| `H_max = ln(3)` | **Constante** (no un parámetro) | Entropía máxima matemática de 3 resultados equiprobables — nunca se calibra |
| `Δ_disponibilidad`, `Δ_fatiga`, `Δ_forma`, `Δ_externos` | Parámetro (funciones, sin coeficientes nombrados individualmente todavía) | Mismo estado que en `MODEL-004` — descritos como "acotados", sin nombre de peso propio |

## `models/expected-value.md` (`MODEL-006`)

| Símbolo | Tipo | Rol |
|---|---|---|
| — | — | `EV = (P_modelo · c) − 1` **no tiene ningún parámetro libre** — es una función pura de `P_modelo` y `c`, deliberadamente sin coeficientes (`MODEL-006`, sección 10) |
| Umbrales de la Clasificación (`engine/06`: EV Muy Alto/Alto/Moderado/Bajo/Negativo) | Restricción (implícita, sin símbolo propio todavía) | Los cinco rangos ya existen cualitativamente en `engine/06` sin cortes numéricos — quedan, aquí, catalogados como parámetros pendientes de nombrar y calibrar |

**Total:** 22 símbolos catalogados como parámetro/peso/restricción (excluyendo la única Constante, `H_max`) — ninguno con valor numérico asignado en ningún documento del proyecto a la fecha de esta misión.

---

# 5. Origen de los parámetros

Todo parámetro de la sección 4 solo puede obtener su valor numérico futuro de una de estas tres fuentes — nunca de una cuarta:

| Fuente legítima | Qué significa |
|---|---|
| **Evidencia estadística** | Estimación a partir de datos reales observados (`data/results/`), usando un método declarado y reproducible (sección 7) |
| **Aprendizaje histórico** | Patrones confirmados por `learning/pattern-discovery.md` con "nivel de confianza estadística" suficiente (ya exigido por ese documento) — nunca un patrón anecdótico de uno o dos partidos |
| **Validación cuantitativa** | Confirmación, con una métrica declarada (sección 8), de que el valor propuesto mejora el modelo frente al conjunto de parámetros vigente — nunca "porque parece razonable" |

**Explícitamente prohibido, sin excepción:** opinión del Arquitecto Estadístico (humano o IA), intuición e impresión subjetiva ("este equipo se ve mejor"), y ajuste manual arbitrario para forzar que el modelo produzca un resultado esperado de antemano. Esto no es una regla nueva de esta misión — es la aplicación literal de `CLAUDE.md` ("Nunca alterar pesos sin evidencia estadística") y de la Constitución, Art. 2.5 y Art. 11 ("Ante evidencia insuficiente, la única respuesta válida es declarar esa insuficiencia... nunca estimarla, inventarla, ni sustituirla por un valor por defecto").

---

# 6. Ciclo de calibración

El flujo pedido por esta misión ya existe, en su mayor parte, como el pipeline de `learning/` (`docs/06`, Fase 9-10) — este documento no lo redefine, lo reconcilia y le agrega la única pieza metodológica que faltaba (**Optimización**, ausente de los cinco documentos de `learning/` ya diseñados):

```
Resultados históricos          →  data/predictions/ + data/results/ (ya existentes, docs/05/14)
        │
        ▼
Preparación                    →  learning/error-analysis.md (ya diseñado — diagnóstico caso a caso)
        │
        ▼
Optimización                   →  APORTE DE ESTA MISIÓN (sección 7) — ausente hasta ahora en
                                   learning/pattern-discovery.md y learning/confidence-calibration.md,
                                   que detectan evidencia pero no calculan un valor numérico candidato.
                                   Ocurre, metodológicamente, dentro de la responsabilidad ya asignada
                                   a learning/weight-adjustment.md ("cuál sería el peso propuesto")
        │
        ▼
Validación                     →  learning/confidence-calibration.md (ya diseñado, hoy específico de
                                   Confianza) + sección 8 de esta misión (generaliza sus métricas a
                                   los demás motores)
        │
        ▼
Comparación                    →  learning/version-history.md (ya diseñado — compara métricas de
                                   auditoría antes/después de cada cambio)
        │
        ▼
Propuesta                      →  learning/weight-adjustment.md (ya diseñado — estado
                                   pendiente/aprobada/rechazada)
        │
        ▼
Aprobación humana              →  docs/06-Flujo-Operacional.md, Fase 9; Constitución Art. 5
                                   (Arquitecto Estadístico Humano, nunca la IA)
        │
        ▼
Nueva versión                  →  docs/06-Flujo-Operacional.md, Fase 10; docs/11-Versiones.md;
                                   CHANGELOG.md; learning/version-history.md
```

Ningún eslabón de `learning/` se modifica — este documento únicamente llena el eslabón "Optimización", que hasta ahora no tenía ningún documento propio, ni de `models/` ni de `learning/`.

---

# 7. Métodos candidatos

*(Catalogados, no elegidos — la selección real requiere datos que hoy no existen.)*

| Método | Qué hace | Candidato natural para |
|---|---|---|
| **Maximum Likelihood Estimation (MLE)** | Estima los parámetros que maximizan la probabilidad de los datos observados bajo el modelo propuesto | `μ_gol`, `κ`, `κ'` (`models/poisson.md`) — es, literalmente, el método que Maher (1982) y Dixon-Coles (1997) ya usan para modelos de ataque/defensa en fútbol, ya citados en `models/poisson.md`/`offensive-strength.md` |
| **Grid Search** | Evalúa exhaustivamente una malla de combinaciones candidatas y selecciona la de mejor métrica de validación | Parámetros de baja dimensión y ya acotados (`λ_min`, `λ_max`, `δ_max`, `Pen_max`) — simple e interpretable cuando el rango ya se conoce |
| **Bayesian Optimization** | Modela la función de validación con un proceso sustituto (ej. Proceso Gaussiano) y elige el siguiente punto a evaluar minimizando el número de evaluaciones necesarias | Escenarios donde evaluar una combinación es costoso (recalcular el Engine completo sobre un historial grande) — no justificado hoy por el volumen actual de `data/results/`, candidato cuando ese volumen crezca |
| **Cross Validation (validación cruzada)** | **Aclaración de terminología, no un método de optimización en sí mismo:** es un *protocolo de evaluación* que se combina con cualquiera de los métodos anteriores, particionando los datos para estimar qué tan bien generalizará una calibración a datos no vistos | Mitiga directamente el riesgo de sobreajuste ya señalado en `MODEL-001` (sección 10: "sobreajuste si los pesos se calibran con una muestra todavía pequeña") — su uso es una restricción de proceso (sección 11), no una elección opcional |
| **Simulación Monte Carlo** | Genera muchas repeticiones aleatorias para estimar la distribución de una métrica de interés bajo incertidumbre paramétrica | Más una herramienta de análisis de sensibilidad/riesgo que de optimización directa — útil para cuantificar cuánto podría variar el ROI esperado antes de aprobar una calibración concreta |
| **Optimización Evolutiva** (algoritmos genéticos y similares) | Búsqueda metaheurística inspirada en selección natural, apta para espacios de parámetros de alta dimensión y no convexos | Candidata solo si Grid Search/MLE no convergen bien sobre los ~9 parámetros simultáneos de `Offensive Strength` — más costosa computacionalmente y menos interpretable, último recurso, no primera opción |

**Ningún método se elige en esta misión.** La elección real requerirá, como mínimo, datos suficientes en `data/results/` y una evaluación empírica de cuál converge mejor para cada motor — tarea de una misión futura de calibración real, no de esta investigación metodológica.

---

# 8. Validación

*(Qué métricas decidirán si una calibración mejora realmente el modelo — ninguna se calcula aquí.)*

## Familia 1 — Calidad probabilística (¿mejoró el modelo estadístico?)

| Métrica | Qué mide |
|---|---|
| **Log Loss** (entropía cruzada) | Penaliza fuertemente las predicciones seguras y equivocadas — evalúa la calidad de la distribución completa de probabilidad, no solo el resultado más probable |
| **Brier Score** | Error cuadrático medio entre la probabilidad declarada y el resultado real (Brier, 1950) — ya prevista como métrica de v2.0 en `data/audit/README.md`; es una *proper scoring rule* (Gneiting et al., 2007, ya citado en `models/confidence.md`): incentiva declarar la probabilidad verdaderamente creída, nunca una inflada o conservadora |
| **Calibration Error** | Brecha entre la confianza/probabilidad declarada y la frecuencia real de acierto observada — exactamente lo que `learning/confidence-calibration.md` ya calcula para el Índice de Confianza; este documento generaliza el mismo concepto para validar, en el futuro, si la propia probabilidad de `engine/03-Poisson.md` está bien calibrada, no solo la Confianza |

## Familia 2 — Resultado financiero (¿mejoró la estrategia de apuesta?)

| Métrica | Qué mide |
|---|---|
| **ROI** (Return on Investment) | Retorno relativo si se hubiera apostado siguiendo las recomendaciones del modelo — ya definida en `docs/09-Auditoria.md` |
| **Yield** | Retorno por unidad apostada acumulada, con una normalización distinta de ROI — también ya prevista en `docs/09` |

## Métrica complementaria (nunca decisiva por sí sola)

| Métrica | Qué mide | Advertencia |
|---|---|---|
| **Accuracy** (Top1/Top4) | Proporción de aciertos | **Métrica ingenua para un modelo probabilístico:** un modelo bien calibrado que declara honestamente "40%" para el resultado que finalmente ocurre no está "equivocado" aunque pierda el 60% restante de las veces — Accuracy no distingue entre un modelo mal calibrado que acierta por suerte y uno bien calibrado que pierde por varianza genuina (mismo principio de *proper scoring rules*, Gneiting et al., 2007). Se cataloga porque `docs/09` ya la usa, pero **nunca debe ser el único criterio** para aprobar una calibración — siempre debe acompañarse de al menos una métrica de la Familia 1 |

**Regla de decisión (no una fórmula, un principio):** una calibración nueva se considera candidata a propuesta solo si mejora simultáneamente la Familia 1 (calidad probabilística) sin empeorar significativamente la Familia 2 (resultado financiero) en el conjunto de validación fuera de muestra (sección 11) — nunca se aprueba una calibración que mejora ROI a costa de una probabilidad peor calibrada, porque eso indicaría sobreajuste a la muestra de calibración, no una mejora real.

---

# 9. Versionado

Cada conjunto de parámetros calibrados pertenece, sin excepción, a una versión narrativa específica del Modelo Santiago (Constitución, Art. 9: versión técnica del repositorio vs. versión narrativa del comportamiento predictivo) — nunca se sobrescribe un conjunto de parámetros anterior. Este documento no redefine el mecanismo ya vigente: `learning/version-history.md` ya es responsable de registrar "variable(s) modificada(s) y valores antes/después" y de permitir revertir si el cambio no mejoró el modelo; `docs/11-Versiones.md` y `CHANGELOG.md` ya son responsables del registro oficial. La única aclaración que aporta esta misión: un **conjunto completo de parámetros de un motor** (ej. los nueve de `Offensive Strength`) debe versionarse como una unidad coherente, no parámetro por parámetro de forma independiente — porque varios de ellos interactúan dentro de la misma fórmula (ej. `w_R`/`w_T` solo tienen sentido relativo entre sí), y calibrar uno sin el otro podría producir una combinación nunca validada conjuntamente.

---

# 10. Responsabilidades

| Rol | Responsabilidad | Nunca hace |
|---|---|---|
| `learning/` (en particular `weight-adjustment.md`) | Producir una **propuesta** documentada de calibración, con el método usado, la evidencia que la respalda y las métricas de validación (secciones 7-8) | Aplicar el cambio por sí mismo, ni siquiera si la evidencia es contundente (`learning/weight-adjustment.md`, ya vigente) |
| **Arquitecto Estadístico Humano** | Revisar y aprobar o rechazar explícitamente cada propuesta de calibración (Constitución, Art. 5) | Delegar esa aprobación en el Arquitecto Estadístico IA, ni aprobar sin evidencia estadística real |
| **Modelo** (`engine/`, una vez versionado) | Usar el conjunto de parámetros ya aprobado y versionado, tal como se le entrega | Ajustar ningún parámetro por su cuenta, ni durante la calibración ni durante una predicción (sección 11) |

---

# 11. Restricciones (del propio procedimiento de calibración)

Prohibiciones explícitas, ninguna nueva en principio — todas ya se derivan de reglas vigentes, aquí aplicadas específicamente a la calibración:

| Prohibición | Por qué |
|---|---|
| **Modificar pesos manualmente** | Viola directamente "Nunca alterar pesos sin evidencia estadística" (`CLAUDE.md`) — todo valor debe originarse en uno de los tres orígenes legítimos de la sección 5 |
| **Ajustar parámetros durante una predicción** | Violaría Reproducibilidad y Determinismo, ya exigidos como principios del Runtime (`docs/26`, sección 9: "el Runtime no introduce aleatoriedad no documentada"; "el orden de ejecución... es fijo") — los parámetros deben estar fijos y versionados *antes* de que comience cualquier ejecución, nunca calculados sobre la marcha |
| **Entrenar usando el mismo partido evaluado** | Es el error clásico de *fuga de datos* (data leakage): calibrar un parámetro con un partido y validar la calibración con ese mismo partido produce una métrica optimista y no generalizable — el conjunto usado para optimizar (sección 7) y el conjunto usado para validar (sección 8) deben ser siempre disjuntos, y preferiblemente el de validación debe ser cronológicamente posterior al de calibración (un modelo de fútbol no debe "aprender" de partidos que, en el tiempo real, todavía no habían ocurrido cuando se calibró) |
| **Autoaprobar nuevas calibraciones** | Constitución, Art. 2.9 ("No autoaprobación") — ninguna entidad, ni `learning/`, ni el Arquitecto Estadístico IA, puede aprobar por sí misma un cambio que ella misma propuso; la aprobación pertenece siempre y exclusivamente al Arquitecto Estadístico Humano (Art. 5) |

---

# Ventajas

- Da, por primera vez, un catálogo único de los más de veinte parámetros pendientes, sin tener que releer seis documentos de `models/` por separado.
- Cierra el único eslabón metodológico ("Optimización") que el pipeline ya diseñado de `learning/` no cubría, sin duplicar ni redefinir ninguno de sus cinco documentos existentes.
- Hace explícita, antes de que exista la tentación, la prohibición de fuga de datos (entrenar y validar con el mismo partido) — un error técnico real y común que ningún documento anterior del proyecto mencionaba.

---

# Limitaciones

- No calibra nada — el procedimiento en sí no acelera la disponibilidad de datos reales (`data/results/` sigue siendo un marcador de posición, `docs/27`).
- Los seis métodos de la sección 7 no están evaluados entre sí para el caso específico del Modelo Santiago — elegir uno requiere una misión futura, con datos reales disponibles, que hoy no existen.
- Dos motores (`Confidence`, `Chaos`) todavía no nombran simbólicamente cada uno de sus coeficientes internos con el mismo rigor que `Offensive`/`Defensive Strength` (sección 4) — el catálogo de esta misión hereda esa asimetría del texto original de `MODEL-004`/`MODEL-005`, sin resolverla (fuera de alcance: no se modifican esos documentos).
- La regla de decisión de la sección 8 (mejorar Familia 1 sin empeorar Familia 2) es un principio, no un umbral cuantitativo — definir "significativamente" con un número requeriría, otra vez, evidencia estadística que hoy no existe.

---

# Aplicación dentro del Modelo Santiago

Este documento es la referencia única que `learning/weight-adjustment.md` deberá seguir, en su implementación futura, para decidir **con qué método** calcula el peso propuesto que hoy solo describe cualitativamente ("cuál sería el peso propuesto"). También es la referencia que cualquier futura calibración de `models/poisson.md`, `offensive-strength.md`, `defensive-strength.md`, `confidence.md` o `chaos-index.md` deberá citar antes de fijar un valor numérico — ninguna calibración futura debería producirse sin declarar explícitamente de cuál de las tres fuentes legítimas (sección 5) proviene, con qué método (sección 7) y qué métrica (sección 8) la valida.

---

# Referencias

- Maher, M.J. (1982). "Modelling Association Football Scores." *Statistica Neerlandica*, 36(3), 109-118 — ya citado en `models/poisson.md`/`offensive-strength.md`; origen del uso de MLE para parámetros de ataque/defensa en fútbol.
- Dixon, M.J. y Coles, S.G. (1997). "Modelling Association Football Scores and Inefficiencies in the Football Betting Market." *Journal of the Royal Statistical Society: Series C*, 46(2), 265-280 — mismo método, refinado.
- Brier, G.W. (1950). "Verification of Forecasts Expressed in Terms of Probability." *Monthly Weather Review*, 78(1), 1-3 — origen del Brier Score (sección 8).
- Gneiting, T., Balabdaoui, F., y Raftery, A.E. (2007). "Probabilistic Forecasts, Calibration and Sharpness." *Journal of the Royal Statistical Society: Series B*, 69(2), 243-268 — ya citado en `models/confidence.md`; fundamento de las *proper scoring rules* y de la advertencia sobre Accuracy (sección 8).
- Jones, D.R., Schonlau, M., y Welch, W.J. (1998). "Efficient Global Optimization of Expensive Black-Box Functions." *Journal of Global Optimization*, 13(4), 455-492 — fundamento clásico de Optimización Bayesiana (sección 7).
- Holland, J.H. (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press — origen de los algoritmos genéticos/optimización evolutiva (sección 7).
- Metropolis, N. y Ulam, S. (1949). "The Monte Carlo Method." *Journal of the American Statistical Association*, 44(247), 335-341 — origen del método de simulación (sección 7).
- `learning/error-analysis.md`, `pattern-discovery.md`, `confidence-calibration.md`, `weight-adjustment.md`, `version-history.md` — pipeline reconciliado, no redefinido (sección 6).

---

# Versión 2.0 (siguiente iteración de esta investigación)

Pendiente, condicionado a la existencia de datos reales suficientes en `data/results/`:

- Selección real de un método de la sección 7 para cada motor (posiblemente distinto por motor, según su dimensionalidad y el volumen de datos disponible).
- Definición cuantitativa de "mejora significativa" en la regla de decisión de la sección 8 (hoy solo un principio cualitativo).
- Nombrado simbólico explícito de los coeficientes de `Confidence`/`Chaos`, hoy solo descritos cualitativamente (limitación señalada arriba) — requeriría una revisión de `MODEL-004`/`MODEL-005`, fuera del alcance de esta misión.
- Implementación real del ciclo de la sección 6 en código, una vez exista el stack ya congelado (`docs/34`) y suficiente historial de partidos.

---

# Validaciones obligatorias

- **¿Todas las fórmulas actuales permanecen sin valores numéricos?** Sí — verificado contra los seis documentos de `models/` (sección 4); ninguno fue editado en esta misión.
- **¿Ningún parámetro depende de opinión humana?** Confirmado — sección 5 define exhaustivamente las tres únicas fuentes legítimas, excluyendo explícitamente opinión, intuición y ajuste manual arbitrario.
- **¿El aprendizaje continúa siendo supervisado?** Sí — sección 10 confirma que toda calibración pasa, sin excepción, por la aprobación del Arquitecto Estadístico Humano antes de aplicarse; `learning/` nunca aplica un cambio por sí mismo.
- **¿El proceso mantiene la reproducibilidad científica?** Sí — sección 11 exige partición fija y disjunta entre datos de calibración y de validación (nunca aleatoria sin declarar), y prohíbe cualquier ajuste dinámico durante una predicción, preservando el principio de Determinismo ya fijado en `docs/26`.

---

# Cierre obligatorio

**1. ¿Qué problema resuelve este procedimiento?**
La ausencia de un método único, reproducible y auditable para transformar los más de veinte parámetros simbólicos ya definidos por `MODEL-001` a `007` en valores numéricos reales — sin él, cada futura calibración correría el riesgo de ser ad-hoc, inconsistente entre motores, o un ajuste manual disfrazado de evidencia.

**2. ¿Qué parámetros existen actualmente?**
22 símbolos catalogados en la sección 4, repartidos en los seis motores (9 en Offensive Strength, reutilizados parcialmente por Defensive Strength más 4 propios, 5 en Poisson, 5 en Confidence, 5 en Chaos, ninguno en Expected Value salvo los umbrales de clasificación todavía sin nombrar) — más una Constante (`H_max`) que nunca debe calibrarse por no ser una estimación estadística.

**3. ¿Cómo se obtendrán en el futuro?**
Mediante el ciclo completo de la sección 6 (que reconcilia el pipeline ya existente de `learning/` con la pieza nueva de "Optimización"), usando uno de los métodos catalogados en la sección 7 (sin elegir cuál todavía), siempre a partir de una de las tres fuentes legítimas de la sección 5.

**4. ¿Qué métricas decidirán si una calibración fue mejor?**
Las de la sección 8: Log Loss, Brier Score y Calibration Error para la calidad probabilística; ROI y Yield para el resultado financiero; Accuracy solo como complemento, nunca como criterio único — una calibración se aprueba solo si mejora la primera familia sin empeorar significativamente la segunda.

**5. ¿Qué papel tendrá `learning/`?**
Exactamente el que ya tiene diseñado (sección 6): diagnosticar (`error-analysis.md`), detectar patrones (`pattern-discovery.md`), calibrar y validar Confianza (`confidence-calibration.md`), y producir la propuesta final (`weight-adjustment.md`) — ahora, además, siguiendo el método de Optimización que esta misión cataloga (sección 7) en lugar de dejarlo indefinido.

**6. ¿Qué papel conservará el Arquitecto Estadístico?**
El ya fijado por la Constitución (Art. 5): el IA diseña, documenta y propone con evidencia — nunca aprueba un cambio de peso por sí mismo; el Humano revisa y aprueba o rechaza cada propuesta explícitamente, sin poder delegar esa decisión de vuelta al IA.

**7. ¿Qué riesgos evita este diseño?**
Tres, explícitamente prohibidos en la sección 11: ajuste manual sin evidencia, recalibración dinámica durante una predicción (rompería reproducibilidad/determinismo), y fuga de datos (calibrar y validar con el mismo partido) — además del riesgo estructural de autoaprobación, ya cubierto por la Constitución.

**8. ¿Qué parte sigue pendiente antes del entrenamiento real?**
Datos reales suficientes en `data/results/` (hoy vacío, `docs/27`); la elección real de un método por motor entre los seis catalogados; y, para dos motores (`Confidence`, `Chaos`), nombrar simbólicamente sus coeficientes internos con el mismo nivel de formalidad que `Offensive`/`Defensive Strength` ya tienen.

**9. ¿Qué misión recomendarías después?**
La misma prioridad ya identificada por `MODEL-007`: una misión de captura de datos (`docs/27`) que provea el historial real necesario — sin ese insumo, ningún método de la sección 7 tiene nada sobre qué ejecutarse, y este procedimiento seguiría siendo, por más completo que esté, enteramente teórico.

**10. ¿Puede considerarse oficialmente diseñado el proceso completo de aprendizaje del Modelo Santiago tras este documento?**
Sí, en el nivel de **procedimiento y metodología** — el pipeline de `learning/` (ya diseñado desde `MS-003`) y el catálogo de parámetros/métodos/métricas de esta misión cubren, juntos, todo el trayecto desde un resultado histórico hasta una nueva versión aprobada del modelo, sin ningún eslabón sin dueño. No puede considerarse diseñado en el nivel de **ejecución real** — ningún método se ha aplicado todavía, porque el dato que lo haría posible (`data/results/` con historial suficiente) sigue sin existir.

---

# Fuera de alcance de esta misión

- No se calibra ningún parámetro — ningún símbolo de la sección 4 recibe valor numérico.
- No se implementa código.
- No se elige un método de la sección 7 para ningún motor específico.
- No se modifica el Engine, las Variables Oficiales, el Runtime, el `Prediction Context`, la Base de Conocimiento, el stack tecnológico (`docs/34`) ni ninguna fórmula matemática ya aprobada (`MODEL-001` a `007`).
- No se modifica ningún documento de `learning/` — se reconcilia su pipeline, sin editarlo.

---

Fin del documento.
