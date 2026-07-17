# Project Tracker del Modelo Santiago

**Archivo:** `docs/00-Project-Tracker.md`

**Versión:** 1.0.0

**Estado:** Activo — referencia oficial del estado del proyecto

---

# Objetivo

Este documento es el sistema de seguimiento oficial del desarrollo del Modelo Santiago: registra qué misiones se han ejecutado, en qué estado están, qué depende de qué, y cuál es el siguiente paso recomendado.

Es un documento **vivo**: deberá actualizarse cada vez que se inicie, avance o cierre una misión. Ninguna misión se considera completada hasta que este documento refleje su estado real.

---

# Cómo leer este documento

- **Estado** usa exactamente uno de: `Pendiente`, `En progreso`, `En revisión`, `Completada`.
- **% Avance** es una estimación del propio autor de la misión al momento de la última actualización, no una métrica calculada automáticamente.
- **Dependencias** lista las misiones que deben estar `Completada` antes de que esta pueda iniciarse (o antes de que sus resultados sean confiables).
- Las fechas usan el formato `YYYY-MM-DD` (`docs/05-Base-de-Conocimiento.md`).
- Desde MR-001 el proyecto usa **series de numeración independientes** por tipo de misión: `MS-NNN` para misiones de **diseño** (avanzan la arquitectura), `MR-NNN` para misiones de **reconciliación del Engine** (corrigen inconsistencias ya detectadas en el Engine y su entorno inmediato), `AR-NNN` para **auditorías de congelamiento arquitectónico** (revisiones independientes y adversariales que intentan refutar que un inventario de inconsistencias esté completo), `GR-NNN` para **reconciliación de gobernanza documental** (corrigen inconsistencias en los documentos que gobiernan el proyecto) y, desde GOV-001, `GOV-NNN` para **gobernanza constitucional** (define principios estables de máxima autoridad conceptual, no técnica). Se listan en tablas separadas más abajo.

---

# Resumen general del proyecto

**Porcentaje global de avance:** ~60%

**Veredicto de Architecture Freeze:** No declarable todavía, pero muy cerca. De las 5 críticas identificadas por AR-002 (INC-01, INC-04, INC-05, INC-18, INC-21), **3 ya están resueltas** (INC-18/INC-21 por GR-002; INC-01 por MR-003) — quedan solo **2 críticas abiertas: INC-04 e INC-05**, ambas dentro de `engine/`, ambas requieren una decisión de diseño real (no solo edición). De los 7 criterios objetivos de `docs/23` (Parte 6), ahora **4 de 7 cumplidos** (Orden de Lectura completo, referencias cruzadas de `engine/` correctas, variables con consumidor o nota documentada, Arquitecto Estadístico sin ambigüedad — este último recién completado por `MR-003`). Próximo paso: `MR-004` (huérfanas, cuotas, rotaciones — resuelve INC-04/INC-05, las 2 críticas restantes) y `GR-003` (`data/README.md`).

**Veredicto de madurez del Engine (MR-001):** el diseño lógico del Engine está completo, pero **no listo para implementación** hasta resolver las 3 inconsistencias críticas inventariadas (ver "Registro de misiones de reconciliación" más abajo: MR-002 a MR-004).

**Veredicto de la auditoría independiente (AR-001):** confirma lo anterior y añade que la fase de diseño arquitectónico **tampoco puede darse por cerrada** hasta ampliar el análisis al perímetro documental que gobierna al Engine (`CLAUDE.md`, `README.md`, `data/README.md`, `.claude/agents/`) — ver "Registro de auditorías de congelamiento arquitectónico" más abajo. Veredicto textual: **C) la arquitectura necesita ampliar el análisis**, no lista todavía para B) ni A).

**Veredicto de gobernanza documental (GR-001):** la gobernanza no está completamente lista para soportar el crecimiento del proyecto, pero no por un defecto de diseño — por la ausencia de un mecanismo que la sincronice hacia `CLAUDE.md`/`README.md`/agentes cada vez que se agrega un documento nuevo. Propone jerarquía de autoridad de 8 niveles y roadmap GR-002 a GR-007 (ver "Registro de misiones de gobernanza documental" más abajo).

*(Promedio ponderado por el alcance relativo de cada misión completada/en progreso frente al roadmap conocido en `docs/12-Roadmap.md`; se recalculará cuando se cierre MS-002.)*

## Módulos terminados

- Arquitectura documental base (`docs/`, `models/`, `.claude/agents/`, `prompts/`, `CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`).
- Diseño del esquema de la Base de Conocimiento de Selecciones Nacionales (`data/processed/selecciones-nacionales/`, 11 entidades).
- Catálogo maestro `selecciones.csv` (40 selecciones, Top 40 FIFA).
- Catálogo maestro `competiciones.csv` (11 competiciones: Amistosos Internacionales + 10 competiciones internacionales reales, MS-006).
- Diseño arquitectónico del módulo `learning/` (6 documentos).
- Diseño y refinamiento del flujo operacional (`docs/06-Flujo-Operacional.md`).
- Especificación oficial del proceso de predicción V0.1 a nivel de archivo (`docs/14-Prediction-Pipeline.md`, MS-007).
- Especificación oficial de la Capa de Preparación de Variables (`docs/15-Capa-de-Preparacion-de-Variables.md`, MS-008).
- Contrato oficial de variables: tipo, unidad, rango y ciclo de vida de las 12 variables (`docs/16-Contrato-Oficial-de-Variables.md`, MS-009).
- Matriz oficial de consumo de variables por motor, cerrando el diseño lógico del Engine (`docs/17-Matriz-de-Consumo-de-Variables.md`, MS-010).
- Plan oficial de reconciliación arquitectónica del Engine, con inventario de 11 inconsistencias y roadmap de 5 misiones futuras (`docs/18-Plan-de-Reconciliacion-Arquitectonica.md`, MR-001).
- Auditoría independiente de congelamiento arquitectónico, con 8 inconsistencias adicionales fuera del perímetro original del Engine (`docs/19-Architecture-Freeze-Review.md`, AR-001).
- Plan oficial de reconciliación de la gobernanza documental, con jerarquía de autoridad, flujo de consulta y roadmap de 6 misiones (`docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md`, GR-001).
- Constitución del Modelo Santiago: 12 artículos de principios estables, de máxima autoridad conceptual (`docs/21-Constitucion-del-Modelo-Santiago.md`, GOV-001).
- Manual Operativo del Arquitecto IA: protocolo de trabajo con listas de verificación previa/durante/cierre (`docs/22-Manual-Operativo-del-Arquitecto-IA.md`, GOV-002).
- Plan Maestro de Reconciliación Operativa: matriz de 21 inconsistencias, plan de 8 pasos y 7 criterios objetivos de Architecture Freeze (`docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md`, AR-002).
- **Primera reconciliación real ejecutada** (`GR-002`): `CLAUDE.md` y `README.md` actualizados — Orden de Lectura autoactualizable, distinción IA/Humano en "Tu Rol", mención de la Capa de Preparación de Variables, principios completos, índice de `docs/` hasta la posición 23.
- **Segunda reconciliación real ejecutada** (`MR-002`): los 6 documentos de `engine/` reconciliados editorialmente — referencias cruzadas corregidas y verificadas con `grep`, referencias a motores futuros anotadas explícitamente, estructura de `engine/01` alineada con sus 5 pares.
- **Tercera reconciliación real ejecutada** (`MR-003`): `docs/06-Flujo-Operacional.md` y `docs/14-Prediction-Pipeline.md` ahora integran explícitamente la Capa de Preparación de Variables y distinguen Arquitecto Estadístico IA/Humano — `INC-01`, `INC-02` e `INC-20` quedan completamente resueltos en el texto.

## Módulos en desarrollo

- Catálogo maestro de la Base de Conocimiento de Selecciones Nacionales: faltan `torneos.csv`, `estadios.csv`, `arbitros.csv` (MS-002 quedó en pausa tras `selecciones.csv`; `competiciones.csv` se completó vía MS-006).
- Este propio sistema de seguimiento (`docs/00-Project-Tracker.md`), recién creado.

## Módulos pendientes

- Ediciones reales de torneos (`torneos.csv`) para las 10 competiciones incorporadas en MS-006 (fechas, sedes, formato) — explícitamente diferido a una misión futura desde MS-006.
- Entidades relacionales de Selecciones Nacionales: `jugadores.csv`, `convocatorias.csv`, `partidos.csv`, `lesiones.csv`, `cuotas.csv`, `estadisticas_partido.csv` (explícitamente diferidas a una misión futura desde MS-001).
- Implementación matemática (v2.0) de los 6 motores de `engine/`, respaldada por `models/`.
- Implementación matemática (v2.0) de los 5 documentos de `learning/`.
- `scripts/` y `excel/` (no existen todavía).
- Corrección editorial de las inconsistencias detectadas en `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` (referencias a archivos inexistentes, ver MS-004).

## Riesgos identificados

*Nota: los riesgos relacionados con inconsistencias de `engine/`/`docs/` listados abajo fueron consolidados, ampliados y evidenciados con precisión en `docs/18-Plan-de-Reconciliacion-Arquitectonica.md` (MR-001, inventario INC-01 a INC-11), ampliados con 8 hallazgos adicionales fuera del perímetro del Engine en `docs/19-Architecture-Freeze-Review.md` (AR-001, INC-12 a INC-19), consolidados en materia de gobernanza en `docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md` (GR-001, INC-20), y verificados/actualizados en `docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md` (AR-002, INC-21). **`INC-18` e `INC-21` (Orden de Lectura de `CLAUDE.md` desactualizado) ya quedaron resueltos por `GR-002`** — el resto sigue abierto. Estos cuatro documentos son la referencia autorizada más detallada; esta tabla mantiene solo un resumen ejecutivo.*

| Riesgo | Impacto | Mitigación propuesta |
|---|---|---|
| `data/predictions/`, `data/results/`, `data/audit/`, `data/raw/` siguen siendo solo marcadores de posición | Sin datos reales, `engine/` y `learning/` no pueden validarse empíricamente | Priorizar completar el catálogo maestro (MS-002/MS-006) antes de avanzar a implementación matemática |
| `engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` documentan internamente pasos de obtención/validación/normalización que ahora duplican la responsabilidad de `docs/15-Capa-de-Preparacion-de-Variables.md` (MS-008), y ambos comparten variables de entrada (ej. Forma Reciente) sin una fuente única | Si se implementa código directamente sobre el texto actual de los motores, se fijaría la duplicación y el riesgo de cálculos inconsistentes entre motores | Misión editorial futura que actualice `engine/01-06` para asumir como precondición la salida de la Capa de Preparación de Variables (ver "Próxima misión recomendada" de MS-008) |
| 5 de las 12 variables oficiales (Compatibilidad Táctica, Calidad de Plantilla, Localía, Historial Directo, Estado Psicológico) no tienen consumidor explícito declarado en ningún `engine/0X.md` — Compatibilidad Táctica es Nivel A en `docs/02-modelo.md` pese a ello, y Estado Psicológico no tiene nivel asignado (MS-009, confirmado independientemente en MS-010) | Riesgo de que variables consideradas importantes en `docs/02-modelo.md`/`docs/03-Variables.md` nunca se implementen realmente en ningún motor, o se implementen sin criterio explícito de cuál motor las usa | Misión editorial de `engine/` (ver MS-008/MS-009/MS-010) que asigne consumidor explícito a cada una, y revisión de `docs/02-modelo.md` para clasificar a Estado Psicológico |
| `engine/06-Expected-Value.md` consume `cuotas.csv` directamente de la Base de Conocimiento, sin pasar por la Capa de Preparación de Variables ni por el Contrato Oficial de Variables (MS-010) | Contradice el principio de desacoplamiento central de MS-008; si se implementa código sobre el texto actual, el Engine quedaría acoplado a la Base de Conocimiento en al menos un punto | Misión futura que decida si las cuotas se modelan como una entrada oficial paralela a las 12 Variables o se hacen pasar por la Capa de Preparación de Variables como cualquier otro dato |
| El Engine (v2.0) no tiene todavía respaldo matemático completo en `models/` para Chaos Index ni Confidence | Riesgo de implementar fórmulas sin investigación previa, violando `CLAUDE.md` ("Investigación antes de implementación") | No iniciar la v2.0 de esos motores sin el documento de `models/` correspondiente |
| Inconsistencias editoriales ya detectadas en `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` (numeración interna y referencias a archivos inexistentes) | Puede inducir errores si se usan como referencia sin revisar | Programar una misión editorial dedicada antes de tocar esos motores |
| Alta dependencia de coordinación manual entre misiones (numeración de `docs/`, referencias cruzadas) | Cada nueva misión que inserta un documento numerado obliga a renumerar y actualizar referencias en varios archivos | Preferir, cuando sea posible, agregar documentos al final de la secuencia en lugar de insertarlos; este tracker debe usarse para detectar el conflicto antes de crear el archivo |
| Selecciones nacionales con datos altamente volátiles (entrenadores, ranking) capturados en un punto en el tiempo | Los datos de `selecciones.csv` pueden quedar desactualizados rápido (varios cargos ya estaban vacantes al capturarse) | Definir en una misión futura una rutina de refresco periódico, documentada en `data/processed/selecciones-nacionales/README.md` |

---

# Registro de misiones

## MS-001 — Diseño de la Base de Conocimiento (Selecciones Nacionales)

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** Ninguna
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** 2026-07-15
- **Observaciones:** Diseño aprobado de las 11 entidades tras una ronda de revisión. Se aplicaron 5 decisiones arquitectónicas correctivas antes de la aprobación final: Principio de Justificación de Datos, ubicación en `data/processed/selecciones-nacionales/`, eliminación de `campeon_id_seleccion` (dato derivado), diferimiento de estadísticas individuales de jugador, y convención de "Amistosos Internacionales" para evitar `id_torneo` nulo.
- **Próxima misión recomendada (en su momento):** MS-002.

## MS-002 — Construcción del Catálogo Maestro

- **Estado:** En progreso
- **% Avance:** 40% (2 de 5 archivos: `selecciones.csv`, `competiciones.csv`)
- **Dependencias:** MS-001 (Completada)
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** —
- **Observaciones:** Se completó `selecciones.csv` (40 registros, Top 40 FIFA, fuentes web documentadas). `competiciones.csv` quedó completado mediante una misión dedicada y separadamente numerada (MS-006, ver más abajo) en lugar de retomarse dentro de esta misión — se deja registrado aquí para no duplicar el conteo de avance. Quedan pendientes `torneos.csv`, `estadios.csv` y `arbitros.csv`.
- **Próxima misión recomendada:** Completar `torneos.csv`, `estadios.csv` y `arbitros.csv` (pueden numerarse como misiones dedicadas al estilo MS-006, o retomarse dentro de MS-002) antes de avanzar a misiones que dependan de torneos/estadios reales (ej. partidos).

## MS-003 — Diseño del Sistema de Aprendizaje

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** Ninguna (diseño puramente arquitectónico, no requiere datos reales)
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** 2026-07-15
- **Observaciones:** Se diseñaron los 6 documentos de `learning/` (`README.md`, `error-analysis.md`, `pattern-discovery.md`, `confidence-calibration.md`, `weight-adjustment.md`, `version-history.md`). Límite de diseño clave: el módulo es de solo lectura sobre `data/predictions/`/`data/results/` y nunca aplica cambios automáticamente.
- **Próxima misión recomendada (en su momento):** MS-004.

## MS-004 — Diseño del Flujo Operacional

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** MS-003 (Completada) — el flujo integra `learning/`
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** 2026-07-15
- **Observaciones:** Se creó `docs/06-Flujo-Operacional.md` (originalmente numerado `05-`, ver historial de renumeraciones más abajo). Requirió resolver un conflicto de numeración con el entonces `docs/05-Backroll.md`, renumerando 7 documentos. Se documentó una inconsistencia preexistente en `engine/04-Chaos-Index.md`/`engine/05-Confidence.md` (referencias a archivos inexistentes), sin corregirla por estar fuera de alcance.
- **Próxima misión recomendada (en su momento):** MS-004A.

## MS-004A — Refinamiento del Flujo Operacional

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** MS-004 (Completada)
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** 2026-07-15
- **Observaciones:** Refinamiento de `docs/06-Flujo-Operacional.md` (v1.0.0 → v1.1.0): se incorporó explícitamente `CLAUDE.md`, `prompts/` y `models/` al flujo; se reforzó que `learning/` nunca modifica automáticamente `docs/`, `engine/`, `models/` ni variables; se agregó la Fase 10 — Versionado como cierre final del ciclo (`learning/` → Versionado → nueva versión del modelo).
- **Próxima misión recomendada (en su momento):** MS-005.

## MS-005 — Project Tracker

- **Estado:** En revisión
- **% Avance:** 100% (documento creado; pendiente de tu validación)
- **Dependencias:** Ninguna funcionalmente, pero documenta el estado de todas las anteriores (MS-001 a MS-004A)
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** —
- **Observaciones:** El documento debía crearse como `docs/00-Project-Tracker.md`, pero el número `00` ya estaba ocupado por `docs/00-principios.md`. Se resolvió, por decisión explícita tuya, renumerando los 13 documentos existentes de `docs/` (`00-12` → `01-13`) para que el Project Tracker ocupe literalmente la posición `00`, con actualización de todas las referencias cruzadas en `README.md`, `CLAUDE.md`, `engine/`, `learning/` y `data/processed/selecciones-nacionales/README.md`. Esto se apartó puntualmente de la instrucción "no modificar otros documentos" de esta misión, de forma consciente y autorizada.
- **Próxima misión recomendada:** Retomar MS-002 (archivos restantes del catálogo maestro) — es la dependencia más antigua sin cerrar y bloquea misiones futuras sobre partidos/torneos reales.

## MS-006 — Construcción de la Base de Conocimiento (Competiciones)

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** MS-001 (Completada) — reutiliza el esquema de `competiciones.csv` ya diseñado
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se finaliza en `README.md` del módulo la definición de los valores ENUM de `confederacion_organizadora` (incluida la excepción `CONMEBOL-UEFA` para organización conjunta) y de `tipo` (`amistoso`, `mundial`, `eliminatoria_mundial`, `continental`, `liga_naciones`, `interconfederacion`). Se pueblan 10 competiciones internacionales de selecciones absolutas masculinas (`COMP-000002` a `COMP-000011`: Copa Mundial FIFA, Eliminatorias Mundial FIFA, Eurocopa, UEFA Nations League, Copa América, CONCACAF Gold Cup, Copa Asiática, Copa Africana de Naciones, OFC Nations Cup, Finalissima), verificadas mediante fuentes públicas reconocidas (ver `CHANGELOG.md` para el detalle de fuentes por competición). No se crean ediciones específicas en `torneos.csv` — queda explícitamente fuera del alcance de esta misión. Esta misión cubre y completa el archivo `competiciones.csv` que estaba pendiente dentro de MS-002 (ver observaciones de esa misión).
- **Próxima misión recomendada:** Completar `torneos.csv` con ediciones reales de estas 10 competiciones (fechas, sedes, formato), seguido de `estadios.csv` y `arbitros.csv` — son la dependencia más antigua sin cerrar del catálogo maestro (MS-002) y bloquean misiones futuras sobre partidos reales.

## MS-007 — Prediction Pipeline

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/06-Flujo-Operacional.md` (Completada, MS-004/MS-004A) y `docs/05-Base-de-Conocimiento.md` (esquema de MS-001) — este documento los referencia sin modificarlos
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/14-Prediction-Pipeline.md`, la especificación oficial V0.1 del proceso de predicción a nivel de archivo (orden exacto de lectura de los 11 CSV de `data/processed/selecciones-nacionales/`, contrato de salida al usuario, registro de la predicción, actualización de la Base de Conocimiento al finalizar el partido, y consolidación de reglas de inmutabilidad). Se decide **agregar el documento al final de la secuencia** (`14-`) en lugar de insertarlo en una posición intermedia, para evitar una tercera renumeración de `docs/` (riesgo ya identificado en este mismo tracker tras MS-004 y MS-005). No se modifica ningún documento existente; el detalle de fases/agentes/motores sigue perteneciendo exclusivamente a `docs/06-Flujo-Operacional.md`, que esta misión referencia pero no redefine. Queda explícitamente fuera de alcance el diseño del esquema de columnas de `data/predictions/`, `data/results/` y `data/audit/`.
- **Próxima misión recomendada:** Diseñar el esquema de columnas de `data/predictions/`, `data/results/` y `data/audit/` (mismo estándar aplicado a `competiciones.csv` en MS-006), o alternativamente retomar MS-002 (`torneos.csv`, `estadios.csv`, `arbitros.csv`) si se prioriza completar el catálogo maestro antes que el pipeline de registro.

## MS-008 — Diseño de la Capa de Preparación de Variables (Arquitectura Oficial)

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/03-Variables.md`, `docs/04-Algoritmo.md`, `docs/06-Flujo-Operacional.md`, `docs/14-Prediction-Pipeline.md` (todas Completadas) — este documento se integra con las cuatro sin modificarlas
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/15-Capa-de-Preparacion-de-Variables.md`, la especificación oficial de la nueva capa arquitectónica que transforma la Base de Conocimiento en variables normalizadas para el Engine. Se evaluaron y descartaron formalmente "Feature Builder", "Feature Engineering Layer" y "Variable Builder" antes de adoptar "Capa de Preparación de Variables", por ser el único nombre consistente con el vocabulario ya establecido del proyecto ("Variable", no "Feature") y que cubre sus tres responsabilidades reales (leer, validar, normalizar). El análisis crítico obligatorio identificó una duplicación de responsabilidad ya existente en `engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` (ambos documentan pasos internos de obtención/validación/normalización que esta nueva capa formaliza, y ambos comparten variables como "Forma Reciente" sin fuente única) — documentada en la sección "Observaciones del Arquitecto" como candidata a una misión editorial futura, sin corregirla en esta misión (fuera de alcance: "No modificar motores"). Se agrega al final de la secuencia de `docs/` (posición 15), replicando la decisión de MS-007 de no insertar en una posición intermedia.
- **Próxima misión recomendada:** Misión editorial dedicada a `engine/01-06` que (a) actualice sus secciones "Procesamiento" para asumir como precondición la salida de `docs/15-Capa-de-Preparacion-de-Variables.md` en lugar de duplicar los pasos de obtención/validación/normalización, y (b) corrija la inconsistencia de numeración interna de `engine/04-Chaos-Index.md`/`engine/05-Confidence.md` ya documentada desde MS-004. Alternativamente, retomar MS-002 (`torneos.csv`, `estadios.csv`, `arbitros.csv`) o diseñar el esquema de `data/predictions/`/`data/results/`/`data/audit/` (pendiente desde MS-007).

## MS-009 — Contrato Oficial de Variables del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/03-Variables.md`, `docs/02-modelo.md`, `docs/05-Base-de-Conocimiento.md`, `docs/14-Prediction-Pipeline.md`, `docs/15-Capa-de-Preparacion-de-Variables.md` (todas Completadas) — este documento se integra con las cinco sin modificarlas
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/16-Contrato-Oficial-de-Variables.md`, fijando por primera vez tipo, unidad, rango y nulabilidad de las 12 variables (todas tenían "Escala: Pendiente" en `docs/03-Variables.md`). El análisis obligatorio (cruce sistemático de `docs/02-modelo.md` Niveles A-D contra la sección "Entradas" de cada motor) encontró que 5 de las 12 variables no tienen consumidor explícito en ningún `engine/0X.md` actual: Compatibilidad Táctica (Variable005 — grave, es Nivel A), Calidad de Plantilla (Variable008), Localía (Variable009), Historial Directo (Variable010) y Estado Psicológico (Variable011, que además no tiene nivel de importancia asignado en `docs/02-modelo.md`). Documentado en "Observaciones del Arquitecto" sin corregirlo (fuera de alcance: "No modificar motores/variables/algoritmo"). Se agrega al final de la secuencia de `docs/` (posición 16).
- **Próxima misión recomendada:** Ampliar la misión editorial de `engine/` ya recomendada en MS-008 para que, además de eliminar la duplicación de pasos 1-3, declare explícitamente qué motor consume cada una de las 5 variables huérfanas detectadas aquí (o documente por qué deliberadamente no participan aún); y una revisión de `docs/02-modelo.md` que clasifique a Estado Psicológico en un Nivel A-D.

## MS-010 — Matriz Oficial de Consumo de Variables del Engine

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/02-modelo.md`, `docs/03-Variables.md`, `docs/04-Algoritmo.md`, `docs/06-Flujo-Operacional.md`, `docs/16-Contrato-Oficial-de-Variables.md`, `engine/01-06` (todas Completadas) — este documento se integra con todas sin modificarlas
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/17-Matriz-de-Consumo-de-Variables.md`, cerrando el diseño lógico del Engine con trazabilidad completa motor-por-motor y variable-por-variable. El análisis en sentido inverso al de MS-009 (motor → variable) confirma independientemente las mismas 5 variables sin consumidor, refinándolas en huérfanas confirmadas (Variable008, 009, 010) vs. huérfanas con solapamiento textual ambiguo no confirmado (Variable005 — grave, Nivel A —, y Variable011). Hallazgo nuevo de mayor severidad: `engine/06-Expected-Value.md` consume `cuotas.csv` directamente de la Base de Conocimiento, sin pasar por la Capa de Preparación de Variables, contradiciendo el principio de desacoplamiento de MS-008. También se documenta una duplicación concreta de la señal "Rotaciones" en 4 de los 6 motores, y que `engine/04-Chaos-Index.md` es el motor con la superficie de entrada más amplia y menos formalizada. Todo esto queda registrado en "Observaciones del Arquitecto" sin corregirse (fuera de alcance: "No modificar motores/variables/algoritmo").
- **Próxima misión recomendada:** Misión editorial de `engine/` (acumulando las recomendaciones de MS-008, MS-009 y MS-010) que: (a) elimine la duplicación de pasos 1-3 y de la señal "Rotaciones"; (b) declare consumidor explícito para las 5 variables huérfanas o documente por qué no participan aún; (c) decida si las cuotas deben modelarse como una entrada oficial paralela a las 12 Variables o pasar por la Capa de Preparación de Variables; (d) corrija la numeración interna de `engine/04-05` ya conocida desde MS-004. **Esta recomendación fue formalizada como el roadmap MR-002 a MR-006 en MR-001 (ver tabla de misiones de reconciliación más abajo).**

---

# Registro de misiones de reconciliación (MR-)

Serie independiente de `MS-`, iniciada en MR-001. Una misión `MR-` nunca agrega diseño nuevo — únicamente audita y, cuando se ejecuta su corrección, reconcilia inconsistencias ya detectadas entre documentos existentes.

## MR-001 — Reconciliación Arquitectónica del Engine (Architecture Review Board)

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** MS-008, MS-009, MS-010 (todas Completadas) — consolida y verifica sus hallazgos
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/18-Plan-de-Reconciliacion-Arquitectonica.md`. Inventaría 11 inconsistencias (INC-01 a INC-11), dos de ellas nunca antes registradas explícitamente: INC-01 (`docs/06-Flujo-Operacional.md` Fase 3 contradice textualmente a `docs/15`) e INC-02 (`docs/14-Prediction-Pipeline.md` no menciona la Capa de Preparación de Variables). Precisa con evidencia de línea exacta (`grep`) la numeración cruzada inconsistente de `engine/01, 02, 03, 05` (INC-03), ya señalada de forma genérica desde MS-004 sin nunca haberse catalogado por completo. Propone el roadmap MR-002 a MR-006 y emite veredicto: el Engine **no** está listo para implementación hasta resolver las tres inconsistencias críticas (INC-01, INC-04, INC-05). No modifica ningún documento existente.
- **Próxima misión recomendada:** MR-002 (corrección editorial de numeración de `engine/` — la única sin dependencias, primera del roadmap).

## MR-002 — Reconciliación Editorial del Engine

- **Estado:** **Completada**
- **% Avance:** 100%
- **Dependencias:** MR-001 (Completada)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Objetivo (definido en MR-001, ejecutado con este alcance ampliado):** Corregir las referencias cruzadas incorrectas de `engine/01, 02, 03, 05` hacia Confidence/Chaos-Index, tratar las referencias a `engine/07`/`engine/08` (inexistentes), y reconciliar editorialmente los 6 documentos de `engine/` (terminología, consistencia estructural, enlaces) sin tocar fórmulas, variables, pesos ni arquitectura.
- **Nota (AR-002):** un brief intermedio solicitó una misión distinta bajo el mismo identificador "MR-002"; para no romper esta entrada ni las dependencias de MR-003/MR-004, se registró como `AR-002`.
- **Nota 2 (GR-002):** otro brief intermedio, también nombrado "MR-002" ("Reconciliación Real Fase I — Documentos Raíz"), se ejecutó como `GR-002` (ya reservada con ese alcance).
- **Observaciones:** Verificado con `grep` antes y después del cambio (mismo método que MR-001/AR-001). Corregidas 6 referencias cruzadas incorrectas (`INC-03`): Confidence citado como "engine/04" en `engine/01,02,03` (correcto: `05`); Chaos-Index citado como "engine/05" en `engine/03` (correcto: `04`); autorreferencia incorrecta en el propio encabezado de `engine/05-Confidence.md`. Las 4 referencias a `engine/07-Bankroll-Engine.md`/`engine/08-Simulation.md` (inexistentes) se anotan como "(futuro, no implementado todavía)" en lugar de eliminarse (preserva la intención de diseño ya declarada en "Mejoras Futuras" de esos motores). Se detectó y corrigió una inconsistencia estructural no catalogada previamente: `engine/01` era el único de los 6 motores sin las secciones "Estado del Motor" y "Versión 2.0 (Pendiente)" — se agregaron con el mismo patrón que `engine/02`, sin contenido matemático nuevo. Se documentaron sin resolver (fuera de alcance, ya conocidas): duplicación de Pasos 1-3 con la Capa de Preparación de Variables, acceso directo de `engine/06` a `cuotas.csv` (`INC-05`), 5 variables sin consumidor confirmado (`INC-04`), señales de entrada no oficiales, y duplicación de "Rotaciones" (`INC-06`). Ninguna inconsistencia funcional nueva detectada. No se modificó ninguna fórmula, algoritmo, variable, peso ni el comportamiento del modelo (validado explícitamente).
- **Próxima misión recomendada:** `MR-003` (`docs/06`/`docs/14`/`data/README.md`, ahora que la numeración de `engine/` es confiable) y `GR-003` (`data/README.md`, mismo mensaje).

## MR-003 — Reconciliación Operativa del Flujo de Predicción (`docs/06` + `docs/14`)

- **Estado:** **Completada**
- **% Avance:** 100%
- **Dependencias:** MR-002 (Completada)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Objetivo (definido en MR-001):** Actualizar la Fase 3 de `docs/06` y la Etapa 2 de `docs/14` para reflejar que los motores consumen variables preparadas por `docs/15`, nunca `data/processed/` directamente.
- **Observaciones:** Resuelve textualmente `INC-01` e `INC-02` (contradicción activa entre `docs/06`/`docs/14` y el principio de desacoplamiento de `docs/15`) en los 4 puntos donde aparecía: diagrama de alto nivel, "Diagrama de dependencias del Engine", Fase 3, tabla "Integración con `data/`" y tabla "Responsabilidades por módulo" de `docs/06`; y la relación con `docs/15`, Etapa 1 y Etapa 2 de `docs/14`. Resuelve también la mitad de `INC-20` correspondiente a `docs/06`: la Fase 9 y la tabla de responsabilidades ahora dicen "Arquitecto Estadístico Humano" explícitamente (distinto del IA, `docs/21` Art. 5), cerrando `GR-007` para este documento (queda solo la parte ya resuelta en `CLAUDE.md` por `GR-002`, es decir, `INC-20` queda completamente resuelto en el texto tras esta misión). Se documenta, sin resolver (fuera de alcance, decisión de diseño): la excepción de `engine/06` con `cuotas.csv` (`INC-05`), anotada explícitamente en 4 puntos de ambos documentos para que quede visible y no se pierda. `docs/06` sube a v1.2.0, `docs/14` a v1.1.0. Ninguna fórmula, variable, peso, fase nueva ni componente nuevo introducido — verificado explícitamente contra las 4 validaciones obligatorias de la misión.
- **Próxima misión recomendada:** `GR-003` (`data/README.md`, misma familia de `INC-12` ya resuelta parcialmente en `README.md` por `GR-002`) y `MR-004` (huérfanas, cuotas, rotaciones — ahora que `docs/06`/`docs/14` documentan explícitamente la excepción de `engine/06` a resolver).

## MR-004 — Cierre de huérfanas, desacoplamiento de cuotas y eliminación de duplicidad en `engine/`

- **Estado:** Pendiente
- **Dependencias:** MR-002, MR-003
- **Objetivo (definido en MR-001):** Declarar consumidor explícito de Variable005/008/009/010/011 o justificar su no uso; decidir el tratamiento de `cuotas.csv` en `engine/06`; centralizar la señal "Rotaciones" en la Capa de Preparación de Variables.

## MR-005 — Reconciliación de `docs/02-modelo.md` con la utilización real de variables

- **Estado:** Pendiente
- **Dependencias:** MR-004
- **Objetivo (definido en MR-001):** Clasificar a Variable011 en un Nivel A-D; revisar el Nivel B de Variable006; agregar nota cruzada de equivalencia terminológica xG/xGA ↔ Potencial Ofensivo/Solidez Defensiva.

## MR-006 — Formalización de la frontera Statistician / Capa de Preparación de Variables

- **Estado:** Pendiente (ver ampliación de alcance recomendada por AR-001, más abajo)
- **Dependencias:** MR-003
- **Objetivo (definido en MR-001):** Actualizar `.claude/agents/statistician.md` para declarar explícitamente la distinción entre validación de suficiencia y validación de construcción.

---

# Registro de auditorías de congelamiento arquitectónico (AR-)

Serie independiente de `MS-`/`MR-`, iniciada en AR-001. Una misión `AR-` es una revisión externa y adversarial: parte de la premisa de que el inventario de una misión `MR-` puede estar incompleto e intenta activamente refutarlo, ampliando el perímetro de documentos auditados.

## AR-001 — Architecture Freeze Review 1.0

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** MR-001 (Completada) — audita si su inventario está completo
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/19-Architecture-Freeze-Review.md`. Amplía la revisión a documentos nunca antes auditados por ninguna misión previa: `README.md`, `data/README.md`, `CLAUDE.md`, `docs/01/07/09/10/11/13`, una muestra de `models/`, `learning/README.md` y `weight-adjustment.md`, los 4 archivos de `prompts/`, y los 6 archivos de `.claude/agents/` en su totalidad (MR-001 solo había revisado 1 de los 6). Encuentra 8 inconsistencias nuevas (INC-12 a INC-19), la más grave (INC-18, Crítica): el "Orden de Lectura" de `CLAUDE.md` — el documento de mayor autoridad del proyecto — no incluye ninguno de los documentos `docs/07` a `docs/18`, ni siquiera los 5 más recientes y centrales para el Engine. También encuentra que `README.md`/`data/README.md` repiten la misma contradicción que INC-01/INC-02 de MR-001 (INC-12); que ningún agente menciona la Capa de Preparación de Variables (INC-13); bandas de confianza incompatibles entre `docs/02` y `docs/07-Backroll.md` (INC-14); un Glosario (`docs/13`) sin ninguna definición real (INC-15); `learning/README.md` sobreestimando la madurez de `docs/09`/`docs/10` (INC-16); y dos esquemas de versionado no sincronizados, `CHANGELOG.md` vs. `docs/11-Versiones.md` (INC-17). Veredicto: **C) la arquitectura necesita ampliar el análisis** — recomienda ampliar el alcance de MR-003 (para cubrir `README.md`/`data/README.md`) y MR-006 (para cubrir los 6 agentes, no solo `statistician.md`), y ejecutar una reconciliación de INC-18 (Orden de Lectura) **antes que MR-002**, por ser aislada, de bajo riesgo y de gravedad Crítica. INC-14/15/16/17 quedan sin una misión asignada todavía (fuera del alcance del Engine que cubría el roadmap de MR-001).
- **Próxima misión recomendada:** Una misión de reconciliación aislada para INC-18 (Orden de Lectura de `CLAUDE.md`/`README.md`), ejecutable antes que MR-002 por no tener dependencias; ampliar el alcance ya definido de MR-003 y MR-006 según el detalle de AR-001; y definir una misión nueva (fuera de la serie actual de `MR-`) para INC-14/15/16/17, que quedan fuera del alcance original del roadmap de MR-001. **Esta recomendación fue formalizada como el roadmap GR-002 a GR-007 en GR-001 (ver "Registro de misiones de gobernanza documental" más abajo).**

## AR-002 — Plan Maestro de Reconciliación Operativa y Preparación para Architecture Freeze 1.0

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** MR-001, AR-001, GR-001, GOV-001, GOV-002 (todas Completadas) — las consolida
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md`. Solicitada bajo el identificador "MR-002" (ya reservado con otro objetivo desde MR-001); registrada como `AR-002` para no romper esa entrada ni las dependencias de MR-003/MR-004 hacia ella. Verifica el estado de las 20 inconsistencias previas: ninguna reconciliada en el texto todavía; `INC-18` e `INC-20` resueltas "en principio" por la Constitución (`GOV-001`), no en el texto operativo. Detecta `INC-21`: el hueco del Orden de Lectura de `CLAUDE.md` (`INC-18`) creció durante las propias misiones de gobernanza (`docs/20-22` tampoco están incluidos). Construye matriz de reconciliación de 21 filas, plan maestro de 8 pasos en orden de dependencia (Paso 1: `CLAUDE.md`/`README.md`, antes que cualquier corrección de `engine/`), y 7 criterios objetivos para declarar Architecture Freeze 1.0 (1 de 7 cumplido hoy). Estima ~70-75% de preparación cualitativa para implementación. Propone 7 dimensiones candidatas para un futuro IMA, sin diseñarlo. No modifica ningún documento existente.
- **Próxima misión recomendada:** Ejecutar el Paso 1 del plan maestro (ampliar `GR-002` para cubrir también `INC-21`) junto con `MR-002` (ya reservado), ambas aisladas y sin dependencias entre sí — ver Parte 4 y Cierre Q8 de `docs/23`.

---

# Registro de misiones de gobernanza documental (GR-)

Serie independiente de `MS-`/`MR-`/`AR-`, iniciada en GR-001. Una misión `GR-` reconcilia documentos de **gobierno** del proyecto (`CLAUDE.md`, `README.md`, `data/README.md`, `docs/13-Glosario.md`, `docs/11-Versiones.md`, `CHANGELOG.md`, `.claude/agents/`) — distinto de `MR-`, que reconcilia el Engine y su entorno inmediato.

## GR-001 — Plan Oficial de Reconciliación de la Gobernanza Documental

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** AR-001 (Completada) — consolida sus hallazgos de gobernanza
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md`. Consolida INC-12, 13, 15, 17, 18, 19 (de AR-001) como inconsistencias de gobernanza, dejando explícitamente fuera INC-14/INC-16 (madurez de contenido funcional, no gobernanza). Detecta un hallazgo nuevo, INC-20: ambigüedad de identidad del rol "Arquitecto Estadístico" entre `CLAUDE.md` (se lo asigna al asistente de IA) y `docs/06-Flujo-Operacional.md` (exige "revisión humana obligatoria" para ese mismo rol al aprobar cambios de peso) — el hallazgo de mayor importancia conceptual del inventario acumulado, por tocar directamente el control humano sobre cambios de peso. Propone una jerarquía documental de 8 niveles justificada, un flujo de consulta oficial, conocimiento mínimo obligatorio por agente, y un roadmap de 6 misiones (GR-002 a GR-007). Recomienda mantener `CHANGELOG.md` y `docs/11-Versiones.md` separados pero sincronizados (no unificarlos). Veredicto: la gobernanza no está completamente lista, por ausencia de un mecanismo de sincronización hacia documentos de mayor nivel, no por defecto de diseño. No modifica ningún documento existente.
- **Próxima misión recomendada:** GR-002 (reconciliación de `CLAUDE.md`/`README.md` — Orden de Lectura y principios, prioridad Crítica, sin dependencias, ejecutable antes que cualquier misión `MR-`).

## GR-002 — Reconciliación de `CLAUDE.md` y `README.md`

- **Estado:** **Completada**
- **% Avance:** 100%
- **Dependencias:** GR-001 (Completada)
- **Prioridad:** Crítica
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Objetivo (definido en GR-001, ampliado por AR-002 con INC-21):** Actualizar el "Orden de Lectura" de `CLAUDE.md`, replicarlo en `README.md`, y completar el resumen de principios de `README.md`. Era, según `docs/23`, el primer paso del roadmap acumulado.
- **Observaciones:** Solicitada bajo el identificador "MR-002" (tercera colisión de numeración de la sesión — ver nota en la entrada de `MR-002` más abajo); ejecutada como esta misma `GR-002`, sin crear un identificador nuevo. Primera reconciliación **real** del proyecto: todo lo anterior desde `MR-001` había sido análisis o principios, nunca una edición de documentos existentes. En lugar de extender la lista fija del Orden de Lectura hasta `docs/23` (que volvería a quedar obsoleta en la próxima misión, repitiendo `INC-21`), se rediseñó como una **regla autoactualizable** ("todo `docs/01` en adelante, en orden numérico ascendente") — resuelve `INC-18` de raíz, no solo su síntoma. Resuelve también, textualmente: `INC-19` (principios completos en `README.md`); la mitad de `INC-20` correspondiente a `CLAUDE.md` (Arquitecto Estadístico IA nunca se autoaprueba — la mitad de `docs/06-Flujo-Operacional.md` sigue pendiente de `GR-007`); y la mitad de `INC-12` correspondiente a `README.md` (Capa de Preparación de Variables mencionada en "Flujo de trabajo" y en la sección `engine/` — `data/README.md` sigue pendiente de `GR-003`). Se corrigieron además dos afirmaciones obsoletas de `CLAUDE.md` no catalogadas previamente como inconsistencia formal: que `CHANGELOG.md`/`LICENSE` no existían (sí existen desde la Misión 001) y que `data/processed/` no tenía datos reales (`selecciones-nacionales/` sí los tiene desde MS-002/MS-006).
- **Próxima misión recomendada:** `MR-002` (ya reservada, aislada) y `GR-003` (`data/README.md`, misma familia de mensaje que la mitad de `INC-12` ya resuelta aquí).

## GR-003 — Reconciliación de `data/README.md` con la Capa de Preparación de Variables

- **Estado:** Pendiente
- **Dependencias:** Recomendado junto con MR-003
- **Prioridad:** Alta
- **Objetivo (definido en GR-001):** Actualizar `data/README.md` para reflejar que el Engine consume variables preparadas, no `data/processed/` directamente.

## GR-004 — Población real de `docs/13-Glosario.md`

- **Estado:** Pendiente
- **Dependencias:** Ninguna estricta
- **Prioridad:** Alta
- **Objetivo (definido en GR-001):** Redactar definiciones reales de los términos ya listados y agregar Variable/Predicción/Probabilidad/Versión.

## GR-005 — Regla de sincronización entre `CHANGELOG.md` y `docs/11-Versiones.md`

- **Estado:** Pendiente
- **Dependencias:** Ninguna
- **Prioridad:** Media
- **Objetivo (definido en GR-001):** Documentar que cada entrada de `docs/11-Versiones.md` debe corresponder a una versión cortada en `CHANGELOG.md`.

## GR-006 — Ampliación de MR-006 a los 6 archivos de `.claude/agents/`

- **Estado:** Pendiente (remite a MR-006 ampliado; no es una misión duplicada)
- **Dependencias:** MR-002, MR-003
- **Prioridad:** Alta
- **Objetivo (definido en GR-001):** Aplicar la tabla de "conocimiento mínimo obligatorio" (sección 6 de `docs/20`) a los 6 agentes.

## GR-007 — Resolución de la ambigüedad de identidad "Arquitecto Estadístico"

- **Estado:** **Completada**
- **Dependencias:** Ninguna
- **Prioridad:** Alta
- **Objetivo (definido en GR-001):** Aclarar en `CLAUDE.md`/`docs/06-Flujo-Operacional.md` si "Arquitecto Estadístico" es el humano, el asistente de IA, o ambos según contexto, y confirmar que la aprobación de cambios de peso requiere siempre decisión humana real.
- **Observaciones:** La mitad de `CLAUDE.md` se completó en `GR-002`; la mitad de `docs/06-Flujo-Operacional.md` (tabla de responsabilidades y Fase 9) se completó en `MR-003`. `INC-20` queda resuelto en el texto de ambos documentos.

---

# Registro de gobernanza constitucional (GOV-)

Serie independiente de `MS-`/`MR-`/`AR-`/`GR-`, iniciada en GOV-001. Una misión `GOV-` define principios estables de máxima autoridad **conceptual** (no técnica) — extremadamente infrecuente por diseño; no reconcilia, no audita, no diseña arquitectura.

## GOV-001 — Constitución del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** Ninguna funcionalmente, pero consolida principios ya presentes en `CLAUDE.md` y en `docs/01-20`
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/21-Constitucion-del-Modelo-Santiago.md` (12 artículos). Propone dos principios constitucionales nuevos: "No autoaprobación" (Artículo 2, punto 9) y "Autocrítica institucionalizada" (Artículo 2, punto 10), ambos justificados como prácticas ya demostradas por el propio proyecto (la secuencia MS-009→MS-010→MR-001→AR-001→GR-001) pero nunca antes declaradas como regla. El Artículo 5 resuelve, a nivel de principio, la ambigüedad `INC-20` detectada por GR-001 (Arquitecto Estadístico IA nunca puede autoaprobar un cambio de peso), remitiendo su aplicación textual concreta a `GR-007`. Se evaluó y descartó ubicarlo como archivo raíz (`CONSTITUCION.md`, junto a `CLAUDE.md`/`README.md`) en favor de mantener la convención de numeración de `docs/` ya usada consistentemente en las 7 misiones anteriores — se deja constancia de esta decisión por si una futura misión de gobernanza prefiere reconsiderarla. Documento deliberadamente breve (principios, no especificaciones técnicas). No modifica ningún documento existente.
- **Próxima misión recomendada:** Ejecutar `GR-002` (Crítica, sin dependencias) como primera reconciliación concreta; considerar en el futuro si `CLAUDE.md`/`docs/06-Flujo-Operacional.md` deben incorporar una referencia explícita a esta Constitución al reconciliarse.

## GOV-002 — Manual Operativo del Arquitecto IA

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** GOV-001 (Completada) — lo complementa sin redefinirlo
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/22-Manual-Operativo-del-Arquitecto-IA.md`. Formaliza el protocolo operativo del Arquitecto IA (rol y límites, flujo de misión, listas de verificación previa/durante/cierre, sincronización documental, gestión de hallazgos, autocrítica estructurada, restricciones permanentes), aclarando explícitamente que no gobierna a los 6 agentes de `.claude/agents/` (esos operan predicciones individuales bajo `docs/06`; este manual gobierna al Arquitecto IA que ejecuta misiones `MS-`/`MR-`/`AR-`/`GR-`/`GOV-` sobre el propio repositorio). Extiende el "Cierre obligatorio" de 4 a 6 preguntas (añade impacto sobre el riesgo arquitectónico e impacto cualitativo sobre el IMA). Identifica que la "Autocrítica" estructurada (sección 8) nunca se había ejecutado antes de forma explícita en ninguna misión anterior, y que la "Gestión de hallazgos" (sección 7) ya había ocurrido dos veces (`INC-18`, `INC-20`) sin una regla explícita sobre si debía alterar el roadmap. No modifica ningún documento existente, incluida la Constitución.
- **Próxima misión recomendada:** Aplicar este manual como protocolo estándar en toda misión futura, comenzando por `GR-002`; considerar si `CLAUDE.md`/`README.md` deben referenciarlo junto a la Constitución al reconciliarse.

---

# Historial de renumeraciones de `docs/`

Para evitar confusión futura, se deja registro explícito de los dos eventos de renumeración:

| Evento | Cambio |
|---|---|
| MS-004 | Inserción de `05-Flujo-Operacional.md`; `05-Backroll.md` → `06-Backroll.md`, ..., `11-Glosario.md` → `12-Glosario.md` |
| MS-005 | Inserción de `00-Project-Tracker.md`; `00-principios.md` → `01-principios.md`, ..., `12-Glosario.md` → `13-Glosario.md` |

Numeración vigente tras MS-005: `00-Project-Tracker.md`, `01-principios.md`, `02-modelo.md`, `03-Variables.md`, `04-Algoritmo.md`, `05-Base-de-Conocimiento.md`, `06-Flujo-Operacional.md`, `07-Backroll.md`, `08-predicciones.md`, `09-Auditoria.md`, `10-aprendizaje.md`, `11-Versiones.md`, `12-Roadmap.md`, `13-Glosario.md`.

---

Fin del documento.
