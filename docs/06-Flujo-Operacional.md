# Flujo Operacional del Modelo Santiago

**Archivo:** `docs/06-Flujo-Operacional.md`

**Versión:** 1.3.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

Definir el flujo operacional completo del Modelo Santiago: qué ocurre desde que un usuario solicita una predicción hasta que esa predicción se audita, retroalimenta al sistema de aprendizaje y —si corresponde— produce una nueva versión del modelo.

Este documento **no redefine** el cálculo interno de probabilidades — eso ya lo define `docs/04-Algoritmo.md` (los 14 pasos matemáticos/lógicos del cálculo). `docs/06-Flujo-Operacional.md` define el nivel superior: quién invoca ese algoritmo, en qué momento, qué pasa antes y después, qué módulo/agente es responsable de cada fase, y cómo se integra con `CLAUDE.md`, `docs/`, `models/`, `engine/`, `data/`, `prompts/`, `learning/` y `.claude/agents/` — es decir, con **todos** los directorios que definen la arquitectura del proyecto, no solo con el cálculo de probabilidades.

---

# Alcance y límites

Este documento:

- No implementa código.
- No crea nuevos motores (los motores siguen siendo únicamente los 6 ya definidos en `engine/`).
- No modifica la Base de Conocimiento (`data/`).
- No redefine variables, pesos ni fórmulas.

Su única responsabilidad es la **arquitectura del flujo**: orden de ejecución, dependencias, validaciones y manejo de errores.

---

# Principio rector: qué gobierna, qué piensa y qué ejecuta

Tres capas distintas participan en cada predicción, y este flujo nunca debe confundirlas:

- **`CLAUDE.md` gobierna.** Es la autoridad última del proyecto: define roles, reglas y el orden de prioridad entre documentos. Ninguna fase de este flujo puede contradecirlo; en caso de conflicto entre documentos, prevalece `CLAUDE.md` (`CLAUDE.md`, "Orden de Lectura": "Si existe conflicto entre documentos, deberá prevalecer el de mayor prioridad").
- **`models/` piensa.** Define la lógica matemática y el fundamento estadístico de cada motor (fórmulas, validaciones, comparaciones). Ningún motor puede incorporar una fórmula nueva sin que exista primero su respaldo documentado en `models/` (`CLAUDE.md`: "Investigación antes de implementación").
- **`engine/` ejecuta.** Aplica la lógica ya definida y respaldada por `models/` para producir un resultado numérico concreto (Fuerza Ofensiva, Poisson, Caos, Confianza, Valor Esperado). `engine/` nunca inventa una metodología propia por fuera de lo ya investigado en `models/`.

En resumen: **`models/` define la lógica matemática; `engine/` ejecuta dicha lógica.** Este documento (`docs/06-Flujo-Operacional.md`) no compite con ninguna de las dos capas — solo ordena cuándo y en qué secuencia se invocan.

`prompts/` participa como una cuarta capa, ortogonal a las anteriores: no gobierna, no piensa ni ejecuta cálculos — es la capa de **disparo**. Cada plantilla de `prompts/` es la que activa una fase concreta de este flujo (ver "Integración con `prompts/`" más abajo).

---

# Flujo general (visión de alto nivel)

```
                    CLAUDE.md (gobierna todas las fases — autoridad última en caso de conflicto)
                              │
Usuario ── prompts/prediction-template.md ──► dispara el ciclo de predicción
  │
  ▼
Orchestrator ──────────────────────────────► (coordina, no calcula)
  │
  ▼
Statistician ───► Validación de datos (data/processed/)
  │
  ├── datos insuficientes ──► DETENER, informar al usuario (ver "Manejo de errores")
  │
  ▼ datos suficientes
Predictor ───► Capa de Preparación de Variables (docs/15) ───► Variables Oficiales (docs/16)
  │             (transforma data/processed/ en las 12 variables ya validadas y normalizadas;
  │              ningún motor accede a data/processed/ directamente)
  ▼
Predictor ───► invoca el Engine con las Variables Oficiales ya preparadas
  │             (docs/04-Algoritmo.md ordena los pasos;
  │              models/ define la lógica matemática; engine/01-06 la ejecuta)
  ▼
Odds Analyzer ───► Valor Esperado (solo si existen cuotas en data/processed/ —
                    excepción documentada y no resuelta, ver Fase 3 y `docs/23`, INC-05)
  │
  ▼
Bankroll Manager ───► (opcional, solo si el usuario lo solicita explícitamente)
  │
  ▼
Registro de la predicción ───► data/predictions/
  │
  ▼
(el partido se juega — tiempo después)
  │
  ▼
Resultado oficial ───► data/results/
  │
  ▼
Auditor ── prompts/audit-template.md ──► compara predicción vs. resultado ───► data/audit/
  │
  ▼
learning/ ── prompts/recalibration-template.md ──► error-analysis → pattern-discovery →
              confidence-calibration → weight-adjustment
  │
  │   learning/ NUNCA modifica automáticamente: docs/, engine/, models/, ni variables.
  │   Solo puede generar una propuesta de mejora documentada.
  ▼
Propuesta de mejora ───► Arquitecto Estadístico del Modelo Santiago (revisión humana obligatoria)
  │
  ├── rechazada ──► el peso/variable/fórmula actual se mantiene sin cambios; se documenta el intento
  │
  ▼ aprobada explícitamente
Versionado ───► actualiza docs/03-Variables.md / engine/ / models/ según corresponda,
                registra el cambio en docs/11-Versiones.md y CHANGELOG.md
  │
  ▼
Nueva versión del Modelo Santiago
```

---

# Diagrama de dependencias del Engine

Basado en las "Entradas" declaradas por cada motor (`engine/01` a `engine/06`), el orden real de ejecución es por capas, no estrictamente secuencial motor-a-motor:

```
Capa 1 (en paralelo, ambos consumen Variables Oficiales ya preparadas por docs/15 — nunca leen data/processed/ directamente):
   engine/01-Offensive-Strength.md
   engine/02-Defensive-Strength.md
        │
        ▼
Capa 2:
   engine/03-Poisson.md   (requiere la salida de la Capa 1)
        │
        ▼
Capa 3 (en paralelo, ambos requieren Capa 1 + Capa 2):
   engine/04-Chaos-Index.md
   engine/05-Confidence.md
        │
        ▼
Capa 4:
   engine/06-Expected-Value.md   (requiere Poisson + Chaos Index + Confidence + cuotas)
```

Ningún motor de una capa puede ejecutarse antes de que sus dependencias de la capa anterior hayan producido salida — mismo principio que `docs/04-Algoritmo.md`: "Ningún paso podrá omitirse."

**Observación histórica (resuelta):** los documentos `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` contenían referencias internas inconsistentes con su propio nombre de archivo (p. ej. `engine/05-Confidence.md` se autodenominaba en su encabezado `engine/04-Confidence.md`). Esta inconsistencia, señalada aquí desde el diseño original de este documento (MS-004), fue corregida editorialmente en `MR-002` (verificado con `grep`, ver `CHANGELOG.md`). Las referencias a `engine/07-Bankroll-Engine.md` y `engine/08-Simulation.md` (motores futuros, no implementados todavía) permanecen anotadas como tales en los propios archivos de `engine/`.

---

# Fases del flujo operacional

## Fase 0 — Solicitud del usuario

*(Responde: "¿Qué sucede cuando un usuario solicita una predicción?")*

El usuario solicita una predicción para un partido específico (dos selecciones, fecha, torneo). Esta solicitud llega siempre primero al **Orchestrator** — ningún otro agente atiende una solicitud directamente, para evitar que un agente asuma responsabilidades ajenas (`.claude/agents/orchestrator.md`: "Nunca resolverás una tarea que pertenezca a otro agente").

## Fase 1 — Orquestación

*(Responde: "¿Qué módulo se ejecuta primero?")*

El **Orchestrator** es siempre el primer módulo en ejecutarse. No calcula nada; su única función es:

1. Leer `CLAUDE.md` y la documentación relevante en `docs/`.
2. Verificar que el partido solicitado sea identificable (selecciones, fecha, torneo válidos en `data/processed/selecciones-nacionales/`).
3. Determinar qué agentes deben participar (mínimo: Statistician → Predictor; opcionalmente Odds Analyzer y Bankroll Manager).
4. Invocar a cada agente en el orden correcto.
5. Consolidar la respuesta final para el usuario.

## Fase 2 — Validación de datos

*(Responde: "¿Qué validaciones deben realizarse antes de calcular probabilidades?" y "¿Qué ocurre si falta información?")*

El **Statistician** valida, antes de que el Predictor calcule nada:

- Que existan registros del partido y ambas selecciones en `data/processed/selecciones-nacionales/`.
- Que las estadísticas necesarias (`docs/03-Variables.md`) estén disponibles y no vacías para ambos equipos.
- Integridad referencial mínima (IDs existentes, sin duplicados, formatos válidos) — mismas verificaciones ya definidas en `docs/05-Base-de-Conocimiento.md`.
- Suficiencia de la muestra (partidos recientes disponibles para calcular Forma Reciente, Potencial Ofensivo, etc.).

**Si falta información crítica:** el flujo se detiene en este punto. Ni el Statistician ni el Predictor inventan datos faltantes (`CLAUDE.md`: "Nunca inventar datos"; `docs/04-Algoritmo.md`, Paso 2: "Si la información es insuficiente, el algoritmo deberá detenerse"). El Orchestrator informa explícitamente al usuario qué información falta y por qué no puede continuar, en vez de degradar silenciosamente la calidad de la predicción.

Si la información es suficiente pero incompleta en variables secundarias (ej. falta el árbitro asignado), el flujo continúa, pero el Predictor debe declarar explícitamente esa variable como "no disponible" en su salida (nunca omitirlo silenciosamente).

## Fase 3 — Ejecución del Engine

*(Responde: "¿Qué motores dependen de otros?" y "¿Qué información consume cada motor?")*

Antes de invocar cualquier motor, el Predictor invoca la **Capa de Preparación de Variables** (`docs/15-Capa-de-Preparacion-de-Variables.md`), que transforma `data/processed/` en las 12 Variables Oficiales (`docs/16-Contrato-Oficial-de-Variables.md`), ya validadas y normalizadas. **Ningún motor de `engine/` accede directamente a `data/processed/` ni conoce su origen físico** — reciben exclusivamente las variables ya preparadas por esa capa (`docs/17-Matriz-de-Consumo-de-Variables.md` detalla qué motor consume cada una).

El **Predictor** ejecuta el Engine siguiendo el diagrama de dependencias de la sección anterior, y el detalle de `docs/04-Algoritmo.md` (Pasos 4 a 11). En cada motor, `models/` es quien define la fórmula/lógica matemática aplicada y `engine/` es quien la ejecuta con las Variables Oficiales ya preparadas — el Predictor invoca `engine/`, nunca `models/` directamente, porque `models/` no ejecuta, solo investiga y respalda:

1. `engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` — consumen las Variables Oficiales ya preparadas (Forma Reciente, Rendimiento en el Torneo, Potencial Ofensivo/Solidez Defensiva, Disponibilidad de Plantilla, Fatiga, Calidad de Plantilla propia con alcance reducido — MR-004). Se ejecutan en paralelo, uno no depende del otro.
2. `engine/03-Poisson.md` — consume las salidas de ambos motores anteriores (Fuerza Ofensiva y Defensiva de ambos equipos), más la Variable Oficial Localía directamente (MR-004, ajuste de goles esperados por condición de local).
3. `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` — consumen las salidas de Poisson y de las Fuerzas, más Variables Oficiales contextuales ya preparadas (Disponibilidad de Plantilla, Fatiga, Factores Externos, e Historial Directo para Confidence — MR-004, factor contextual menor). Se ejecutan en paralelo entre sí.
4. `engine/06-Expected-Value.md` — consume las salidas de Poisson, Chaos Index y Confidence, más las cuotas de mercado (si existen en `data/processed/`). **Excepción documentada, no resuelta:** a diferencia de los cinco motores anteriores, `engine/06` consume las cuotas directamente de `data/processed/`, sin pasar por la Capa de Preparación de Variables ni formar parte del Contrato Oficial de Variables — contradicción funcional ya identificada como `INC-05` (`docs/18-Plan-de-Reconciliacion-Arquitectonica.md`, `docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md`). Resolverla requiere una decisión de diseño (modelar las cuotas como variable oficial o hacerlas pasar por la Capa) fuera del alcance de esta reconciliación editorial.

## Fase 4 — Valor Esperado (condicional)

*(Complementa la Fase 3)*

El **Odds Analyzer** ejecuta `engine/06-Expected-Value.md` únicamente si existen cuotas registradas para el partido. Si no existen, esta fase se omite explícitamente y la predicción final lo indica ("Valor Esperado: no disponible — sin cuotas registradas"), en lugar de estimarlo o inventarlo.

## Fase 5 — Gestión de bankroll (opcional, fuera del núcleo)

El **Bankroll Manager** solo se invoca si el usuario lo solicita explícitamente. No forma parte del núcleo del Modelo Santiago (`.claude/agents/bankroll-manager.md`) y nunca se ejecuta automáticamente como parte de una predicción estándar.

## Fase 6 — Registro de la predicción

*(Responde: "¿Cuándo se registra una predicción?")*

Toda predicción completa (haya o no Valor Esperado disponible) se registra en `data/predictions/` inmediatamente después de que el Predictor entrega su resultado — antes de que el partido se juegue, nunca después. Este registro es la única fuente que `learning/` y la auditoría podrán usar más adelante; una predicción que no se registra en este momento no puede auditarse retroactivamente sin evidencia.

## Fase 7 — Resultado oficial

Cuando el partido finaliza, el resultado oficial se registra en `data/results/`, siguiendo el flujo ya definido en `docs/05-Base-de-Conocimiento.md` (Recolección → Validación → Normalización → Almacenamiento). Este paso es independiente del Modelo Santiago (es un dato externo verificado), pero es el que habilita la siguiente fase.

## Fase 8 — Auditoría

*(Responde: "¿Cuándo se ejecuta la auditoría?")*

La auditoría se ejecuta **únicamente después** de que exista tanto la predicción (`data/predictions/`) como el resultado oficial (`data/results/`) para el mismo partido — nunca antes, porque no hay nada que comparar. El **Auditor** compara ambos, calcula las métricas de `docs/09-Auditoria.md` (ROI, Top1, Top4, etc.) y las consolida en `data/audit/`.

La auditoría puede ejecutarse partido a partido (apenas hay resultado disponible) o de forma agregada al cierre de un torneo (`prompts/audit-template.md`, `prompts/tournament-analysis-template.md`) — ambas modalidades son válidas y no son mutuamente excluyentes.

## Fase 9 — Aprendizaje

*(Responde: "¿En qué momento interviene el sistema de aprendizaje?")*

`learning/` interviene **después** de la Fase 8, nunca antes: necesita que la auditoría ya haya producido una comparación predicción-vs-resultado. Su pipeline dentro de este flujo es:

```
error-analysis.md  →  pattern-discovery.md  →  confidence-calibration.md  →  weight-adjustment.md
```

`learning/` nunca se ejecuta como parte de la generación de una predicción — es exclusivamente un proceso posterior, retrospectivo, sobre partidos ya cerrados.

**Límite estricto (obligatorio):** `learning/` **nunca** puede modificar automáticamente ninguno de los siguientes elementos:

- `docs/` (incluyendo `docs/03-Variables.md`).
- `engine/`.
- `models/`.
- Cualquier variable o peso del modelo.

Su única salida posible es una **propuesta de mejora documentada** (`learning/weight-adjustment.md`), con la evidencia que la respalda. Esa propuesta queda en estado "pendiente" hasta que el **Arquitecto Estadístico Humano** (rol definido y distinguido del Arquitecto Estadístico IA en `docs/21-Constitucion-del-Modelo-Santiago.md`, Artículo 5) la revise y decida explícitamente aprobarla o rechazarla. Ninguna otra fase, agente, ni el propio Arquitecto Estadístico IA, puede aprobarla en su lugar — es, por diseño, la única decisión de todo este flujo que requiere una persona humana.

- Si se **rechaza**: el peso, variable, fórmula o algoritmo actual se mantiene sin cambios. El intento y su justificación quedan igualmente documentados (no se descarta la evidencia, solo se descarta el cambio).
- Si se **aprueba**: el cambio pasa a la Fase 10 (Versionado) — `learning/` en sí mismo no aplica el cambio ni siquiera después de la aprobación; quien lo aplica es el proceso de diseño normal (edición documentada de `docs/03-Variables.md`, `engine/` o `models/`, según corresponda), y quien lo registra es Versionado.

## Fase 10 — Versionado (fase final del flujo)

*(Cierra el ciclo completo: `learning/` → `Versionado` → nueva versión del Modelo)*

Versionado es la última fase del flujo operacional y **solo se ejecuta si una propuesta de `weight-adjustment.md` fue aprobada explícitamente** en la Fase 9. Nunca se dispara automáticamente ni en paralelo con el resto del flujo.

Responsabilidades de esta fase:

1. Confirmar que el cambio aprobado ya fue aplicado (edición documentada de `docs/03-Variables.md`, `engine/` o `models/` — fuera de `learning/`, por el Arquitecto Estadístico).
2. Registrar el cambio en `learning/version-history.md` (evidencia estadística, versión afectada, valores antes/después).
3. Actualizar `docs/11-Versiones.md` (registro oficial de versiones del modelo).
4. Registrar la mejora en `CHANGELOG.md` (`CLAUDE.md`: "Toda mejora deberá registrarse en CHANGELOG.md").
5. Dejar trazabilidad completa hacia la propuesta y la evidencia que la originó, para poder auditar en el futuro si esa versión realmente mejoró el modelo.

El resultado de esta fase es una **nueva versión del Modelo Santiago**, con su cambio completamente documentado y auditable — cerrando el ciclo iniciado en la Fase 0.

---

# Responsabilidades por módulo

| Módulo | Responsabilidad en el flujo | Nunca hace |
|---|---|---|
| `CLAUDE.md` | Gobierna todo el flujo: reglas, roles y prioridad entre documentos (todas las fases) | Ser contradicho por ninguna otra fase o documento |
| `prompts/` | Dispara cada fase (plantillas de predicción, auditoría, recalibración, análisis de torneo) | Contener lógica del modelo |
| `.claude/agents/orchestrator.md` | Primer punto de entrada; coordina el orden de ejecución | Calcular, predecir, inventar datos |
| `.claude/agents/statistician.md` | Validación de datos antes del cálculo (Fase 2) | Predecir resultados |
| `.claude/agents/predictor.md` | Ejecuta el Engine (Fase 3) | Recomendar apuestas, modificar pesos |
| `models/` | Define la lógica matemática y el fundamento estadístico de cada motor | Ejecutar cálculos sobre datos de un partido real |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | Transforma `data/processed/` en las 12 Variables Oficiales, ya validadas y normalizadas (Fase 3, antes de invocar cualquier motor) | Calcular probabilidades, fuerzas, caos o valor esperado; almacenar variables permanentemente |
| `engine/01-06` | Ejecuta la lógica ya definida en `models/` para calcular fuerzas, probabilidades, caos, confianza y valor esperado, a partir de las Variables Oficiales ya preparadas | Acceder a Internet, inventar estadísticas, definir su propia metodología sin respaldo de `models/`, acceder directamente a `data/processed/` (excepción documentada y no resuelta: `engine/06` y las cuotas, ver Fase 3) |
| `.claude/agents/odds-analyzer.md` | Valor Esperado condicional a cuotas (Fase 4) | Generar predicciones |
| `.claude/agents/bankroll-manager.md` | Gestión de capital opcional (Fase 5) | Modificar probabilidades o el Engine |
| `data/predictions/` | Registro inmutable de cada predicción (Fase 6) | Sobrescribirse |
| `data/results/` | Registro del resultado oficial (Fase 7) | — |
| `.claude/agents/auditor.md` | Comparación predicción vs. resultado (Fase 8) | Modificar predicciones históricas, cambiar pesos |
| `learning/` | Análisis retrospectivo y generación de **propuestas** de mejora (Fase 9) | Modificar automáticamente `docs/`, `engine/`, `models/` o cualquier variable; calcular probabilidades; predecir |
| Arquitecto Estadístico **Humano** (distinto del Arquitecto Estadístico IA, ver `docs/21-Constitucion-del-Modelo-Santiago.md`, Art. 5) | Revisa y aprueba/rechaza cada propuesta de `learning/` (Fase 9→10) | Aprobar cambios sin evidencia estadística (`CLAUDE.md`); delegar esta aprobación en el Arquitecto Estadístico IA |
| Versionado (`docs/11-Versiones.md`, `learning/version-history.md`, `CHANGELOG.md`) | Documenta el cambio aprobado y cierra el ciclo con una nueva versión (Fase 10, final) | Ejecutarse sin una aprobación explícita previa |

---

# Orden de ejecución (resumen canónico)

1. Orchestrator recibe la solicitud.
2. Statistician valida los datos disponibles.
3. Predictor ejecuta `engine/01` y `engine/02` (en paralelo).
4. Predictor ejecuta `engine/03` (Poisson).
5. Predictor ejecuta `engine/04` y `engine/05` (en paralelo).
6. Odds Analyzer ejecuta `engine/06` (si hay cuotas).
7. Orchestrator consolida y entrega la predicción al usuario.
8. Bankroll Manager (opcional, si el usuario lo pide).
9. Registro en `data/predictions/`.
10. *(Tiempo después)* Registro del resultado en `data/results/`.
11. Auditor compara y actualiza `data/audit/`.
12. `learning/` ejecuta su pipeline (error-analysis → pattern-discovery → confidence-calibration → weight-adjustment) y genera, como máximo, una propuesta de mejora — nunca un cambio aplicado.
13. El Arquitecto Estadístico del Modelo Santiago revisa la propuesta y decide explícitamente: aprobarla o rechazarla.
14. *(Solo si se aprueba)* Versionado registra el cambio en `docs/11-Versiones.md`, `learning/version-history.md` y `CHANGELOG.md`, produciendo una nueva versión del Modelo Santiago.

Ningún paso puede omitirse ni reordenarse sin justificación documentada (`CLAUDE.md`: "Toda modificación deberá poder ser auditada"). En particular, los pasos 13 y 14 nunca pueden fusionarse ni automatizarse: la aprobación humana es un paso obligatorio y distinto del registro de Versionado.

---

# Manejo de errores

| Situación | Acción del flujo |
|---|---|
| Faltan datos críticos de un equipo | Detener antes de la Fase 3; informar al usuario qué falta |
| Faltan datos de una variable secundaria/contextual | Continuar, pero declarar la variable como "no disponible" en la salida |
| No existen cuotas para el partido | Omitir la Fase 4 (Valor Esperado); indicarlo explícitamente, nunca estimarlo |
| El partido ya tiene una predicción registrada | No se genera una segunda predicción silenciosamente; se informa la existente (evita duplicados en `data/predictions/`) |
| El resultado oficial aún no existe | La Fase 8 (Auditoría) no se ejecuta; no hay error, es un estado de espera normal |
| Un motor del Engine no puede calcular su salida (datos insuficientes en su capa) | Las capas siguientes tampoco se ejecutan — el fallo se propaga hacia adelante, nunca se sustituye por un valor estimado |
| Una propuesta de `weight-adjustment.md` es rechazada por el Arquitecto Estadístico | La Fase 10 (Versionado) no se ejecuta; el peso/variable/fórmula actual se mantiene; el rechazo y su motivo quedan documentados |
| Un cambio en `docs/`, `engine/` o `models/` se intenta aplicar sin una propuesta aprobada de `learning/` | No es un flujo válido: todo cambio de peso/variable/fórmula debe originarse en una propuesta documentada y aprobada (`CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística") |

---

# Integración con `data/`

| Fase | Lee de | Escribe en |
|---|---|---|
| Validación (2) | `data/processed/` | — |
| Ejecución del Engine (3-4) | Variables Oficiales preparadas por `docs/15` (que a su vez lee `data/processed/` — nunca el Engine directamente; excepción documentada: `engine/06` lee `cuotas.csv` directamente, ver Fase 3) | — |
| Registro de predicción (6) | — | `data/predictions/` |
| Resultado oficial (7) | — | `data/results/` |
| Auditoría (8) | `data/predictions/`, `data/results/` | `data/audit/` |
| Aprendizaje (9) | `data/predictions/`, `data/results/`, `data/audit/` | *(ninguna — solo produce una propuesta, ver `learning/README.md`)* |
| Versionado (10) | Propuesta aprobada de `learning/weight-adjustment.md` | `docs/11-Versiones.md`, `learning/version-history.md`, `CHANGELOG.md` — nunca `data/` |

`data/raw/` y `data/archive/` no participan en el flujo operacional de una predicción individual: son insumo del proceso de recolección (`docs/05-Base-de-Conocimiento.md`), previo y externo a este flujo.

---

# Integración con `CLAUDE.md`

`CLAUDE.md` no es una fase del flujo — es la capa que **gobierna** todas las fases simultáneamente. El Orchestrator lo lee primero en la Fase 1 (antes que cualquier otro documento), y ninguna fase posterior puede tomar una decisión que lo contradiga. Si cualquier otro documento (`docs/`, `engine/`, `models/`, `learning/`) entra en conflicto con `CLAUDE.md`, prevalece `CLAUDE.md` (`CLAUDE.md`, "Orden de Lectura"). En particular, los roles que este flujo asigna (Orchestrator, Predictor, Statistician, Odds Analyzer, Bankroll Manager, Auditor, y el propio Arquitecto Estadístico) son los mismos y con las mismas restricciones ya definidas en `CLAUDE.md` y `.claude/agents/`.

---

# Integración con `models/` y `engine/`

`models/` y `engine/` participan juntos en la Fase 3, pero con responsabilidades estrictamente distintas:

- **`models/` define la lógica matemática**: fórmulas, fundamento estadístico, comparaciones y validaciones de cada motor (Poisson, Elo, Expected Value, Confidence, Offensive/Defensive Strength). No ejecuta cálculos sobre un partido real — es investigación, no implementación.
- **`engine/` ejecuta dicha lógica**: cada motor (`engine/01` a `engine/06`) aplica, sobre las Variables Oficiales del partido ya preparadas por `docs/15-Capa-de-Preparacion-de-Variables.md`, la fórmula ya investigada y respaldada en `models/`.

Este documento no altera ni reemplaza `docs/04-Algoritmo.md`: el detalle matemático/lógico interno de cada motor sigue perteneciendo exclusivamente a `models/` (la lógica) y `engine/` (la ejecución). Lo que este documento aporta es el **orden de invocación** entre motores (el diagrama de dependencias por capas) y quién es responsable de invocar cada uno (el Predictor, vía el Engine completo; el Odds Analyzer, específicamente para `engine/06`). Ningún motor puede ejecutar una lógica que no esté antes respaldada en `models/` (`CLAUDE.md`: "Investigación antes de implementación").

---

# Integración con `prompts/`

`prompts/` no participa como una fase que calcula o decide — es la capa que **dispara** cada fase. Cada plantilla ya existente se corresponde con un tramo específico de este flujo:

| Plantilla | Fase(s) que dispara |
|---|---|
| `prompts/tournament-analysis-template.md` | Previo a la Fase 0 — construye contexto de torneo, no genera predicciones individuales |
| `prompts/prediction-template.md` | Fases 0 a 6 (ciclo completo de generación y registro de una predicción) |
| `prompts/audit-template.md` | Fase 8 (Auditoría) |
| `prompts/recalibration-template.md` | Fase 9 (Aprendizaje), específicamente `weight-adjustment.md` |

`prompts/` nunca contiene lógica del modelo (`CLAUDE.md`: "prompts/ nunca contienen lógica del modelo. Solo instrucciones") — por eso no aparece como una fase propia en el flujo, sino como el mecanismo de activación de las fases ya definidas.

---

# Integración con `learning/`

`learning/` se integra en un único punto del flujo: **después** de la Fase 8 (Auditoría), nunca antes ni en paralelo con la generación de una predicción. Esto es intencional y coincide con el límite ya definido en `learning/README.md`: el módulo es de solo lectura sobre predicciones y resultados ya cerrados.

Dentro de este flujo, el límite de `learning/` es absoluto: **nunca puede modificar automáticamente `docs/`, `engine/`, `models/` ni ninguna variable**. Su única salida es una propuesta documentada (`learning/weight-adjustment.md`), que pasa obligatoriamente por la revisión y aprobación explícita del Arquitecto Estadístico del Modelo Santiago antes de que exista cualquier cambio real. Ese cambio, una vez aprobado, se aplica fuera de `learning/` (en `docs/`, `engine/` o `models/`, según corresponda) y se documenta en la Fase 10 (Versionado) — nunca dentro del propio módulo de aprendizaje.

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| ¿Qué sucede cuando un usuario solicita una predicción? | Fase 0 |
| ¿Qué módulo se ejecuta primero? | Fase 1 (Orchestrator) |
| ¿Qué motores dependen de otros? | Diagrama de dependencias del Engine |
| ¿Qué información consume cada motor? | Fase 3 |
| ¿Qué validaciones deben realizarse antes de calcular probabilidades? | Fase 2 |
| ¿Qué ocurre si falta información? | Fase 2, tabla "Manejo de errores" |
| ¿En qué momento interviene el sistema de aprendizaje? | Fase 9, "Integración con `learning/`" |
| ¿Cuándo se ejecuta la auditoría? | Fase 8 |
| ¿Cuándo se registra una predicción? | Fase 6 |

---

Fin del documento.
