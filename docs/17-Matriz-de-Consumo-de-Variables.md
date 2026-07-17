# Matriz Oficial de Consumo de Variables del Engine

**Archivo:** `docs/17-Matriz-de-Consumo-de-Variables.md`

**Versión:** 1.1.0

**Estado:** Especificación oficial — Trazabilidad del Engine (sin implementación)

---

# Objetivo

Este documento es la referencia oficial que describe, motor por motor y variable por variable, qué consume cada uno de los 6 motores del Engine (`engine/01` a `engine/06`), en qué momento, para qué, qué ocurre si la variable falta, y cómo participa en la construcción de la predicción final.

Cierra el diseño lógico del Engine antes de iniciar cualquier diseño de almacenamiento o implementación de código: la Base de Conocimiento, las 12 variables oficiales, la Capa de Preparación de Variables y el Contrato Oficial de Variables ya estaban especificados (MS-001 a MS-009); lo que faltaba era la trazabilidad explícita entre esas variables y los motores que realmente las usan.

```
Base de Conocimiento
        │
        ▼
Preparación de Variables
        │
        ▼
Variables Oficiales
        │
        ▼
Motores
        │
        ▼
Predicción
```

---

# Análisis previo obligatorio (metodología)

Este documento se construyó cruzando, línea por línea, la sección "Entradas" (y, donde aplica, "Factores"/"Flujo del Motor") de los 6 archivos de `engine/` contra las 12 variables de `docs/03-Variables.md`, la jerarquía de `docs/02-modelo.md` y el contrato de `docs/16-Contrato-Oficial-de-Variables.md`. A diferencia de MS-009 (que partió *de la variable* y buscó su consumidor), este análisis parte *del motor* y busca su variable — un cruce en sentido inverso que sirve como segunda validación independiente de los mismos hallazgos (ver "Observaciones del Arquitecto", punto 6).

Ninguna inconsistencia detectada se corrige en este documento — se registra únicamente en "Observaciones del Arquitecto", conforme al alcance de esta misión.

---

# 1. ¿Qué significa consumir una variable?

Que un motor **lea** el valor ya construido de una Variable Oficial (`docs/16-Contrato-Oficial-de-Variables.md`) y lo utilice como entrada de su propio cálculo.

**Implica:**

- Confiar en el valor entregado por la Capa de Preparación de Variables tal como llega — ya validado, normalizado y con su tipo/rango fijados por el contrato.
- Declarar explícitamente cuando una variable consumida no está disponible, en lugar de omitirlo en silencio (`docs/15`, `docs/16`).
- Poder combinar una variable con las salidas de otros motores (ej. `engine/03` combina las salidas de `engine/01` y `engine/02`, no variables directamente — ver sección 2).

**No implica:**

- Modificar la variable — está prohibido por `docs/16` (sección "Inmutabilidad"): los motores únicamente leen.
- Conocer cómo se construyó ni de qué archivo de `data/processed/` proviene — esa es precisamente la responsabilidad que la Capa de Preparación de Variables oculta a los motores (`docs/15`, sección 8).
- Volver a validar o normalizar la variable — ya llega validada; un motor solo puede declarar su propia salida como no confiable si la variable llega marcada como no disponible, nunca "corregirla".
- Almacenar la variable de forma permanente — las variables son temporales (`docs/16`, sección 7).

---

# 2. ¿Qué variables consume cada motor?

## `engine/01-Offensive-Strength.md`

| Categoría | Contenido |
|---|---|
| Variables consumidas (directas) | **Variable003** (Potencial Ofensivo) — entrada primaria; **Variable001** (Forma Reciente), **Variable002** (Rendimiento en el Torneo) — secundarias; **Variable006** (Disponibilidad de Plantilla), **Variable007** (Fatiga), **Variable008** (Calidad de Plantilla, alcance reducido — MR-004) — contextuales |
| Variables opcionales | Variable006, Variable007, Variable008 (contextuales: "modifican el resultado final cuando exista evidencia suficiente" — el propio motor las trata como no obligatorias) |
| Variables indirectas | Ninguna — es un motor de Capa 1 (`docs/06-Flujo-Operacional.md`), no consume salidas de otro motor |
| Variables no utilizadas | Variable004, 005 (diferida, MR-004), 009, 010, 011 (diferida, MR-004), 012 |
| Información consumida que **no** proviene de una Variable Oficial | "Calidad del Rival", "Posesión en Campo Rival", "Ataques Peligrosos" (declaradas en "Variables Secundarias" del documento, sin equivalente en `docs/03-Variables.md`) |

## `engine/02-Defensive-Strength.md`

| Categoría | Contenido |
|---|---|
| Variables consumidas (directas) | **Variable004** (Solidez Defensiva) — primaria; **Variable001**, **Variable002** — secundarias; **Variable006**, **Variable007**, **Variable008** (alcance reducido — MR-004) — contextuales |
| Variables opcionales | Variable006, Variable007, Variable008 |
| Variables indirectas | Ninguna — Capa 1 |
| Variables no utilizadas | Variable003, 005 (diferida, MR-004), 009, 010, 011 (diferida, MR-004), 012 |
| Información no oficial | "Calidad Ofensiva de los Rivales", "Recuperaciones", "Intercepciones", "Presión Defensiva" |

## `engine/03-Poisson.md`

| Categoría | Contenido |
|---|---|
| Variables consumidas (directas) | **Variable009** (Localía — MR-004: ajusta el cálculo de goles esperados según condición de local/visitante/sede neutral). El resto de su entrada declarada originalmente es indirecta: "recibe información proveniente de otros motores" (Fuerza Ofensiva y Fuerza Defensiva de ambos equipos) |
| Variables opcionales | Variable009 (Localía puede no estar definida si la sede aún no se conoce) |
| Variables indirectas | Variable001, 002, 003, 004, 006, 007, 008 (todas las que alimentan a `engine/01`/`engine/02`, transitivamente, a través de Fuerza Ofensiva/Defensiva) |
| Variables no utilizadas (ni directa ni indirectamente) | Variable005 (diferida, MR-004), 010, 011 (diferida, MR-004), 012 |
| Información no oficial | Ninguna — el resto de su entrada son salidas de motores, no datos de negocio |

## `engine/04-Chaos-Index.md`

| Categoría | Contenido |
|---|---|
| Variables consumidas (directas) | **Variable006** (vía "Lesiones importantes, Suspensiones, Jugadores en duda"), **Variable007** (vía "Descanso insuficiente, Rotaciones"), **Variable012** (vía "Clima adverso, Viajes largos"), **Variable001** (vía "Alta variabilidad en resultados recientes") |
| Variables opcionales | Las cuatro anteriores — el documento las trata como factores que "podrá considerar", no como entradas obligatorias |
| Variables indirectas | Variable002, 003, 004 (vía las salidas de `engine/01`, `engine/02`, `engine/03` que declara consumir) |
| Consumo ambiguo, no confirmado | **Variable005** (Compatibilidad Táctica) y **Variable011** (Estado Psicológico), posiblemente aludidas por "Cambios tácticos relevantes" y "Cambios recientes de entrenador" — el documento nunca las cita por su nombre oficial (ver "Observaciones del Arquitecto") |
| Variables no utilizadas | Variable008, 009, 010 |
| Información no oficial | "Eliminación directa", "Prórroga posible" (metadatos de fase del partido/torneo, no una Variable Oficial); "Pocos partidos disponibles", "Datos incompletos" (señales de calidad del dato, no una variable) |

## `engine/05-Confidence.md`

*(Nota: la inconsistencia de autorreferencia en el encabezado de este archivo, documentada desde MS-004, fue corregida editorialmente en `MR-002`.)*

| Categoría | Contenido |
|---|---|
| Variables consumidas (directas) | **Variable006** (vía "Lesiones confirmadas, Suspensiones, Rotaciones esperadas"), **Variable007** (vía "Estado físico de los equipos"), **Variable010** (Historial Directo — MR-004, factor contextual menor) |
| Variables opcionales | Las tres — el documento las lista como información adicional que "además podrá considerar" |
| Variables indirectas | Variable001, 002, 003, 004, 008, 009 (vía las salidas de `engine/01`, `engine/02`, `engine/03` que declara consumir) |
| Consumo ambiguo, no confirmado | **Variable005**, **Variable011** — vía "Cambios recientes de entrenador", mismo patrón que `engine/04`; ambas formalmente diferidas por MR-004 |
| Variables no utilizadas | Variable012 |
| Información no oficial | "Calidad de los datos disponibles" (meta-señal sobre la confianza de la Capa de Preparación de Variables, no una variable en sí); "Competición poco predecible" (metadato de `competiciones.tipo`, definido en `data/processed/selecciones-nacionales/competiciones.csv` — no forma parte de las 12 Variables Oficiales) |

## `engine/06-Expected-Value.md`

| Categoría | Contenido |
|---|---|
| Variables consumidas (directas) | **Ninguna de las 12** |
| Variables opcionales | No aplica |
| Variables indirectas | Variable001, 002, 003, 004, 006, 007, 012 (vía las salidas de `engine/03`, `engine/04`, `engine/05` que declara consumir) |
| Variables no utilizadas (ni directa ni indirectamente) | Variable008, 009, 010 |
| Información consumida que **no** proviene de una Variable Oficial ni de la Base de Conocimiento vía la Capa | **"Cuotas del operador"** — consumida **directamente** de `data/processed/selecciones-nacionales/cuotas.csv` (`docs/14-Prediction-Pipeline.md`, Etapa 2), sin pasar por la Capa de Preparación de Variables ni por el Contrato Oficial de Variables; además "Mercado seleccionado" y "Tipo de apuesta", que son parámetros de la solicitud del usuario, no datos del partido |

---

# 3. ¿Qué variables no tienen actualmente consumidor?

**Actualizado por MR-004** (implementación de las recomendaciones de `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md`): de las 5 variables huérfanas identificadas en MS-009/MS-010, **3 ya tienen consumidor confirmado** y las **2 restantes quedan formalmente diferidas** — no huérfanas por omisión, sino excluidas de V1 por una razón documentada: ausencia de fuente de datos real en la Base de Conocimiento.

| Variable | Nivel (`docs/02-modelo.md`) | Estado de consumo |
|---|---|---|
| **Variable008** (Calidad de Plantilla) | Nivel C | **Resuelta (MR-004)** — `engine/01`, `engine/02`, alcance reducido (solo "profundidad de plantilla") |
| **Variable009** (Localía) | Nivel D | **Resuelta (MR-004)** — `engine/03-Poisson.md` |
| **Variable010** (Historial Directo) | Nivel D | **Resuelta (MR-004)** — `engine/05-Confidence.md`, factor contextual menor |
| **Variable005** (Compatibilidad Táctica) | **Nivel A** | **Diferida formalmente (MR-004)** — no existe fuente de datos (formación/estilo táctico) en ningún CSV de `data/processed/selecciones-nacionales/`; requiere una misión de diseño de datos antes de asignarle motor |
| **Variable011** (Estado Psicológico) | Sin nivel asignado (`INC-08`) | **Diferida formalmente (MR-004)** — falta "Clasificación" (tabla de posiciones) en la Base de Conocimiento, y no tiene Nivel asignado |

Las 2 variables diferidas no se ocultan: quedan documentadas de forma consistente en `docs/03-Variables.md` ("Estado en V1"), `docs/16-Contrato-Oficial-de-Variables.md` y aquí. Compatibilidad Táctica sigue siendo la de mayor severidad conceptual por su Nivel A, pero su ausencia ya no es una omisión sin explicar — es una limitación de datos documentada.

---

# 4. ¿Existe algún motor que consuma información que no provenga de una Variable Oficial?

**Sí, en los seis motores, en distinto grado.** Consolidado (detalle por motor en la sección 2):

| Motor | Información no oficial consumida |
|---|---|
| `engine/01` | Calidad del Rival, Posesión en Campo Rival, Ataques Peligrosos |
| `engine/02` | Calidad Ofensiva de los Rivales, Recuperaciones, Intercepciones, Presión Defensiva |
| `engine/03` | Ninguna |
| `engine/04` | Eliminación directa, Prórroga posible, Pocos partidos disponibles, Datos incompletos |
| `engine/05` | Calidad de los datos disponibles, Competición poco predecible |
| `engine/06` | **Cuotas del operador** (dato de negocio, directo desde `data/processed/`), Mercado seleccionado, Tipo de apuesta (parámetros de solicitud) |

El caso de `engine/06` es cualitativamente distinto y el más grave: no es una señal contextual sin nombre oficial (como en los otros cinco casos), sino un **acceso documentado y directo a la Base de Conocimiento** (`cuotas.csv`), que contradice el principio central de `docs/15-Capa-de-Preparacion-de-Variables.md` ("los motores nunca deben conocer si los datos provienen de CSV"). Ver "Observaciones del Arquitecto", punto 2.

---

# 5. ¿Cómo participa cada variable dentro del motor?

Ejemplo trazado de extremo a extremo (Variable003, la de mayor recorrido):

```
Variable003 (Potencial Ofensivo)
        │
        ▼
engine/01-Offensive-Strength.md
        │
        ▼
Resultado parcial: Fuerza Ofensiva
        │
        ▼
engine/03-Poisson.md
        │
        ▼
Resultado parcial: Goles Esperados + distribución de marcadores
        │
        ▼
engine/04 / engine/05 (Caos / Confianza) + engine/06 (Valor Esperado, si hay cuotas)
        │
        ▼
Resultado final: Predicción consolidada (`docs/06-Flujo-Operacional.md`, Fase 1, "el Orchestrator consolida")
```

Segundo ejemplo, para una variable compartida (Variable006):

```
Variable006 (Disponibilidad de Plantilla)
        │
        ├──► engine/01 ──► ajusta Fuerza Ofensiva
        ├──► engine/02 ──► ajusta Fuerza Defensiva
        ├──► engine/04 ──► ajusta Índice de Caos
        └──► engine/05 ──► ajusta Índice de Confianza
                │
                ▼
        Las cuatro salidas parciales convergen en la Predicción final
```

No se explica aquí ninguna fórmula — solo el propósito y el recorrido, conforme al alcance de esta misión.

---

# 6. ¿Qué ocurre si una variable obligatoria falta?

Se consolida (no se modifica) la regla ya vigente en `docs/15-Capa-de-Preparacion-de-Variables.md` (sección 6) y `docs/16-Contrato-Oficial-de-Variables.md` (sección 6):

**Se detiene el cálculo.** Ninguna variable de Nivel A (Variable001, 002, 003, 004, 005) puede faltar sin detener el pipeline completo antes de invocar cualquier motor — no se estima, no se continúa con un valor sustituto, y se informa explícitamente qué variable falta y por qué (`docs/06-Flujo-Operacional.md`, tabla "Manejo de errores").

Única excepción ya documentada: Variable002 puede llegar nula si el equipo debuta en el torneo actual, sin que eso detenga el pipeline (continúa con confianza reducida).

---

# 7. ¿Qué ocurre si una variable opcional falta?

Se consolida la misma regla: **el cálculo continúa**, la variable se entrega marcada explícitamente como "no disponible" (nunca se omite en silencio ni se sustituye por un valor inventado), y esa ausencia se propaga como una señal de menor confianza hacia `engine/05-Confidence.md` — que ya contempla explícitamente "pocos partidos analizados" y factores de incertidumbre equivalentes.

---

# 8. Variables compartidas entre motores

| Variable | Motores que la consumen (directo) | Riesgo de duplicidad |
|---|---|---|
| Variable001 | `engine/01`, `engine/02` | Bajo — ambos la usan como ajuste secundario, mismo significado |
| Variable002 | `engine/01`, `engine/02` | Bajo |
| Variable006 | `engine/01`, `engine/02`, `engine/04`, `engine/05` | **Alto** — es la variable más compartida (4 de 6 motores); en particular, la señal "Rotaciones" aparece de forma independiente en los cuatro documentos, con riesgo de que cada motor la interprete o pondere de forma distinta si se implementara sin pasar por una única Capa de Preparación de Variables |
| Variable007 | `engine/01`, `engine/02`, `engine/04` | Medio — mismo patrón que Variable006, con "Fatiga"/"Descanso" repetido en los tres |
| Variable008 | `engine/01`, `engine/02` (MR-004, alcance reducido) | Bajo — ambos consumen solo el componente "profundidad de plantilla", mismo significado |

Ninguna variable de Nivel A (Variable003, 004) activa en V1 es compartida por más de un motor de forma directa — cada una tiene un único motor "dueño" (`engine/01` para Variable003, `engine/02` para Variable004). Variable005 (Nivel A) queda formalmente diferida por MR-004, sin motor asignado (sección 3).

---

# 9. ¿Existe algún motor con responsabilidades excesivas?

**`engine/04-Chaos-Index.md`** es el candidato más claro: declara cuatro categorías de factores (Deportivos, Contextuales, Disponibilidad, Información) y es, de los seis motores, el que introduce más señales sin trazabilidad a una Variable Oficial (cuatro: "Eliminación directa", "Prórroga posible", "Pocos partidos disponibles", "Datos incompletos") y el único, junto a `engine/05`, con consumo ambiguo de Variable005/Variable011. Esto no significa que su objetivo (medir incertidumbre) esté mal definido — significa que su superficie de entrada es la más amplia y la menos formalizada de los seis motores, y por lo tanto la más costosa de mantener si se implementa tal como está documentada hoy.

**`engine/06-Expected-Value.md`** tiene un problema distinto, no de exceso de variables sino de **acoplamiento indebido a la Base de Conocimiento** (sección 4) — su responsabilidad declarada (comparar probabilidad del modelo vs. probabilidad implícita) es acotada y correcta, pero su implementación documentada rompe el desacoplamiento que exige `docs/15`.

**`engine/01` y `engine/02`** están razonablemente acotados en su objetivo (fuerza ofensiva/defensiva), pero cada uno introduce 3-4 señales sin variable oficial (sección 4) que, de mantenerse así, se sumarían a los datos que la Capa de Preparación de Variables tendría que resolver sin que exista todavía una Variable Oficial que las represente.

Ninguna de estas observaciones implica refactorizar nada en esta misión — quedan como oportunidades para una futura misión editorial de `engine/` (ya recomendada desde MS-008).

---

# 10. ¿Existe alguna variable cuya importancia declarada no coincida con su utilización real?

**Parcialmente — era el hallazgo central de esta misión, ya identificado en MS-009 y confirmado aquí de forma independiente; MR-004 resolvió 3 de las 5 discrepancias originales** (Variable008, 009, 010), dejando solo Variable005 y Variable011 como discrepancias reales entre importancia declarada y utilización, ambas ahora documentadas como diferidas por ausencia de datos, no como omisiones.

| Variable | Importancia declarada (`docs/02-modelo.md`) | Utilización real (`engine/`, esta misión) | ¿Coincide? |
|---|---|---|---|
| Variable001 | Nivel A | Consumida por 2 motores directamente, 4 indirectamente | Sí |
| Variable002 | Nivel A | Consumida por 2 motores directamente, 4 indirectamente | Sí |
| Variable003 | Nivel A (como "xG") | Consumida por `engine/01` (primaria) | Sí (con inconsistencia de etiqueta ya señalada en MS-009) |
| Variable004 | Nivel A (como "xGA") | Consumida por `engine/02` (primaria) | Sí (misma nota de etiqueta) |
| **Variable005** | **Nivel A** | **Diferida formalmente (MR-004) — sin consumidor por ausencia de fuente de datos**, no por omisión | Ya no es una inconsistencia sin explicar, pero sigue siendo la de mayor severidad conceptual: una variable Nivel A no contribuye a V1 |
| Variable006 | Nivel B | Consumida por 4 motores directamente — la más utilizada de las 12 | Utilización real **superior** a lo que su Nivel B sugeriría |
| Variable007 | Nivel B | Consumida por 3 motores directamente | Consistente con Nivel B |
| Variable008 | Nivel C | Consumida por `engine/01`, `engine/02` (MR-004, alcance reducido) | Sí, ahora consistente |
| Variable009 | Nivel D | Consumida por `engine/03` (MR-004) | Sí, ahora consistente |
| Variable010 | Nivel D | Consumida por `engine/05` (MR-004), factor contextual menor; `docs/03-Variables.md` ya advertía "esta variable tendrá poca influencia" | Sí — consistente con su propia documentación |
| Variable011 | Sin nivel asignado | Diferida formalmente (MR-004) — sin consumidor por ausencia de fuente de datos y de nivel | No se puede evaluar coincidencia porque no existe una importancia declarada con la que comparar |
| Variable012 | Nivel D | Consumida por `engine/04` | Utilización real **superior** a lo que Nivel D sugeriría, aunque razonable (factores externos son el núcleo de Chaos Index) |

**Conclusión:** la inconsistencia de mayor severidad es **Variable005 (Compatibilidad Táctica)** — Nivel A declarado, cero consumo confirmado. La segunda observación relevante, en sentido inverso, es que **Variable006 (Disponibilidad de Plantilla)** tiene una utilización real (4 motores) más amplia de lo que su Nivel B sugeriría — no es necesariamente un problema, pero vale la pena que una futura revisión de `docs/02-modelo.md` confirme si su nivel de importancia debería reconsiderarse a la luz de cuánto la usan realmente los motores.

---

# Matriz oficial (las 12 variables)

| Variable | Motor(es) consumidor(es) | Uso | Obligatoria | Consecuencia si falta | Resultado que afecta |
|---|---|---|---|---|---|
| Variable001 — Forma Reciente | `engine/01`, `engine/02` (directo); `engine/03-06` (indirecto) | Ajuste de contexto reciente en fuerza ofensiva/defensiva | Sí (Nivel A) | Detener el pipeline | Fuerza Ofensiva/Defensiva → Goles Esperados → toda salida posterior |
| Variable002 — Rendimiento en el Torneo | `engine/01`, `engine/02` (directo); `engine/03-06` (indirecto) | Ajuste de contexto dentro del torneo actual | Sí (Nivel A), tolera nulo en debut | Detener, salvo debut (continúa con confianza reducida) | Igual que Variable001 |
| Variable003 — Potencial Ofensivo | `engine/01` (directo, primaria) | Base del cálculo de Fuerza Ofensiva | Sí (Nivel A) | Detener el pipeline | Fuerza Ofensiva → Goles Esperados → Probabilidades → Marcadores → EV |
| Variable004 — Solidez Defensiva | `engine/02` (directo, primaria) | Base del cálculo de Fuerza Defensiva | Sí (Nivel A) | Detener el pipeline | Igual estructura que Variable003 |
| Variable005 — Compatibilidad Táctica | **Ninguno — diferida (MR-004)** | No implementado; falta fuente de datos (formación/estilo táctico) | No en V1 (Nivel A nominal, diferida) | No aplica — diferida hasta que exista fuente de datos | Ninguno (diferida, ver `docs/24`) |
| Variable006 — Disponibilidad de Plantilla | `engine/01`, `engine/02`, `engine/04`, `engine/05` (directo) | Ajuste por lesiones/suspensiones/rotaciones | No (Nivel B) | Continuar, marcar no disponible, propagar a Confidence | Fuerza Ofensiva/Defensiva, Índice de Caos, Índice de Confianza |
| Variable007 — Fatiga | `engine/01`, `engine/02`, `engine/04` (directo) | Ajuste por desgaste físico/descanso | No (Nivel B) | Continuar, marcar no disponible | Fuerza Ofensiva/Defensiva, Índice de Caos |
| Variable008 — Calidad de Plantilla | `engine/01`, `engine/02` (directo, MR-004, alcance reducido) | Ajuste por profundidad de plantilla | No (Nivel C) | Continuar, marcar no disponible | Fuerza Ofensiva/Defensiva |
| Variable009 — Localía | `engine/03-Poisson.md` (directo, MR-004) | Ajuste de goles esperados por condición de local/visitante/neutral | No (Nivel D) | Continuar, marcar no disponible | Goles Esperados → Probabilidades → Marcadores |
| Variable010 — Historial Directo | `engine/05-Confidence.md` (directo, MR-004) | Factor contextual menor de confianza | No (Nivel D) | Continuar, marcar no disponible | Índice de Confianza |
| Variable011 — Estado Psicológico | **Ninguno — diferida (MR-004)** | No implementado; falta fuente de datos (clasificación) y Nivel asignado | No en V1 (sin nivel, diferida) | No aplica — diferida hasta que exista fuente de datos | Ninguno (diferida, ver `docs/24`) |
| Variable012 — Factores Externos | `engine/04` (directo) | Ajuste por clima/viajes | No (Nivel D) | Continuar, marcar no disponible | Índice de Caos |

---

# Diagramas

## Diagrama general de la arquitectura

```
Base de Conocimiento
        │
        ▼
Preparación de Variables
        │
        ▼
Variables Oficiales
        │
        ▼
Motores
        │
        ▼
Predicción
```

## Diagrama de viaje de una variable (construcción → resultado final)

```
Base de Conocimiento (dato crudo)
        │
        ▼
Capa de Preparación de Variables (construye VariableNNN)
        │
        ▼
VariableNNN (validada, normalizada, entregada — docs/16)
        │
        ▼
Motor consumidor directo (ej. engine/01 o engine/02)
        │
        ▼
Resultado parcial (ej. Fuerza Ofensiva / Fuerza Defensiva)
        │
        ▼
Motor consumidor indirecto (engine/03 — Poisson)
        │
        ▼
Resultado parcial siguiente (Goles Esperados, distribución de marcadores)
        │
        ▼
Motores finales (engine/04 Caos, engine/05 Confianza, engine/06 Valor Esperado)
        │
        ▼
Predicción final (consolidada por el Orchestrator, docs/06-Flujo-Operacional.md)
```

---

# Observaciones del Arquitecto

*(Actualización MR-004, 2026-07-17): el hallazgo 1 y el hallazgo 2 de esta sección quedaron resueltos, total o parcialmente, por la implementación descrita en `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md` y aplicada en esta misma revisión de este documento — se mantienen íntegros a continuación como registro histórico de cómo se detectaron, con una nota de cierre en cada uno.*

1. **Confirmación independiente del hallazgo de MS-009, con mayor precisión.** El cruce inverso (motor → variable, en lugar de variable → motor) realizado en esta misión confirma exactamente el mismo conjunto de variables sin consumidor: Variable005, 008, 009, 010, 011. La coincidencia entre dos métodos de análisis independientes refuerza la fiabilidad del hallazgo — no es un artefacto de cómo se hizo el cruce en MS-009. Con este análisis se puede además distinguir con más precisión dos grupos: huérfanas **confirmadas sin ambigüedad** (Variable008, 009, 010 — ningún motor las menciona ni siquiera de forma indirecta) y huérfanas **con solapamiento textual ambiguo, no confirmado** (Variable005, 011 — hay lenguaje en `engine/04`/`engine/05` que podría referirse a ellas, pero ningún motor las cita por su nombre oficial).
2. **Hallazgo nuevo y de mayor severidad: `engine/06-Expected-Value.md` consume `cuotas.csv` directamente de la Base de Conocimiento**, sin pasar por la Capa de Preparación de Variables ni por el Contrato Oficial de Variables (sección 4). Esto contradice el principio central de `docs/15-Capa-de-Preparacion-de-Variables.md`. Es consistente con lo que ya documenta `docs/14-Prediction-Pipeline.md` (que declara que `cuotas.csv` se lee directamente para alimentar `engine/06`), pero nunca se había señalado como una inconsistencia arquitectónica hasta ahora. Se recomienda que una misión futura decida explícitamente entre dos caminos: (a) definir las cuotas como una entrada oficial paralela a las 12 Variables (con su propio contrato, ya que no son una medida de rendimiento deportivo y no encajan naturalmente en `docs/03-Variables.md`), o (b) hacer pasar las cuotas por la Capa de Preparación de Variables como cualquier otro dato de negocio, tratándolas como una "Variable de mercado" distinta de las 12 "Variables de rendimiento".
3. **Duplicación concreta de la señal "Rotaciones"**, re-derivada de forma independiente en `engine/01`, `engine/02`, `engine/04` y `engine/05` (sección 8) — evidencia específica del riesgo genérico ya señalado en `docs/15-Capa-de-Preparacion-de-Variables.md`. Se reitera la recomendación de que la futura misión editorial de `engine/` (MS-008) centralice esta señal en Variable006, calculada una única vez.
4. **`engine/04-Chaos-Index.md` tiene la superficie de entrada más amplia y menos formalizada de los seis motores** (sección 9): cuatro categorías de factores, cuatro señales sin variable oficial y las dos únicas ambigüedades de consumo (Variable005, 011). Es candidato natural a una revisión de alcance en una futura misión, para decidir si sus señales adicionales deben formalizarse como variables oficiales nuevas (fuera del alcance de esta misión: "No inventar nuevas variables") o quedar explícitamente documentadas como metadatos de proceso, no como variables.
5. **Variable006 se usa más de lo que su Nivel B sugeriría** (sección 10) — es la variable con más consumidores directos (4 de 6 motores). No es necesariamente un defecto, pero se sugiere que una futura revisión de `docs/02-modelo.md` confirme si su nivel de importancia declarado sigue siendo el correcto a la luz de su uso real.
6. Se reitera, sin corregirla, la inconsistencia de numeración interna ya conocida desde MS-004: `engine/05-Confidence.md` se autodenomina `engine/04-Confidence.md` en su propio encabezado, y tanto `engine/04-Chaos-Index.md` como `engine/05-Confidence.md` referencian `engine/07-Bankroll-Engine.md` y `engine/08-Simulation.md`, inexistentes en el repositorio.

Ninguna de estas observaciones se implementa en esta misión — quedan documentadas como insumo para la misión editorial de `engine/` ya recomendada desde MS-008 y ampliada en MS-009, y para el roadmap del proyecto (`docs/12-Roadmap.md`).

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se modifican motores, variables, el algoritmo ni ningún otro documento existente.
- No se crean nuevos motores ni nuevas variables.
- No se alteran pesos matemáticos ni el Pipeline ya definido en `docs/06-Flujo-Operacional.md`/`docs/14-Prediction-Pipeline.md`.
- No se resuelven las inconsistencias detectadas — quedan registradas en "Observaciones del Arquitecto" para una misión futura.

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| 1. ¿Qué significa consumir una variable? | Sección 1 |
| 2. ¿Qué variables consume cada motor? | Sección 2 |
| 3. ¿Qué variables no tienen consumidor? | Sección 3 |
| 4. ¿Algún motor consume información que no proviene de una Variable Oficial? | Sección 4 |
| 5. ¿Cómo participa cada variable dentro del motor? | Sección 5 |
| 6. ¿Qué ocurre si falta una variable obligatoria? | Sección 6 |
| 7. ¿Qué ocurre si falta una variable opcional? | Sección 7 |
| 8. ¿Variables compartidas entre motores? | Sección 8 |
| 9. ¿Motor con responsabilidades excesivas? | Sección 9 |
| 10. ¿Importancia declarada vs. utilización real? | Sección 10 |

---

Fin del documento.
