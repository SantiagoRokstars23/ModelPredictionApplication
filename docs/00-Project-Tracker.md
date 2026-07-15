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

---

# Resumen general del proyecto

**Porcentaje global de avance:** ~35%

*(Promedio ponderado por el alcance relativo de cada misión completada/en progreso frente al roadmap conocido en `docs/12-Roadmap.md`; se recalculará cuando se cierre MS-005.)*

## Módulos terminados

- Arquitectura documental base (`docs/`, `models/`, `.claude/agents/`, `prompts/`, `CLAUDE.md`, `README.md`, `LICENSE`, `CHANGELOG.md`).
- Diseño del esquema de la Base de Conocimiento de Selecciones Nacionales (`data/processed/selecciones-nacionales/`, 11 entidades).
- Catálogo maestro `selecciones.csv` (40 selecciones, Top 40 FIFA).
- Diseño arquitectónico del módulo `learning/` (6 documentos).
- Diseño y refinamiento del flujo operacional (`docs/06-Flujo-Operacional.md`).

## Módulos en desarrollo

- Catálogo maestro de la Base de Conocimiento de Selecciones Nacionales: faltan `competiciones.csv`, `torneos.csv`, `estadios.csv`, `arbitros.csv` (MS-002 quedó en pausa tras `selecciones.csv`).
- Este propio sistema de seguimiento (`docs/00-Project-Tracker.md`), recién creado.

## Módulos pendientes

- Entidades relacionales de Selecciones Nacionales: `jugadores.csv`, `convocatorias.csv`, `partidos.csv`, `lesiones.csv`, `cuotas.csv`, `estadisticas_partido.csv` (explícitamente diferidas a una misión futura desde MS-001).
- Implementación matemática (v2.0) de los 6 motores de `engine/`, respaldada por `models/`.
- Implementación matemática (v2.0) de los 5 documentos de `learning/`.
- `scripts/` y `excel/` (no existen todavía).
- Corrección editorial de las inconsistencias detectadas en `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` (referencias a archivos inexistentes, ver MS-004).

## Riesgos identificados

| Riesgo | Impacto | Mitigación propuesta |
|---|---|---|
| `data/predictions/`, `data/results/`, `data/audit/`, `data/raw/` siguen siendo solo marcadores de posición | Sin datos reales, `engine/` y `learning/` no pueden validarse empíricamente | Priorizar completar el catálogo maestro (MS-002/MS-006) antes de avanzar a implementación matemática |
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
- **% Avance:** 20% (1 de 5 archivos: `selecciones.csv`)
- **Dependencias:** MS-001 (Completada)
- **Fecha de inicio:** 2026-07-15
- **Fecha de finalización:** —
- **Observaciones:** Se completó `selecciones.csv` (40 registros, Top 40 FIFA, fuentes web documentadas). Quedan pendientes `competiciones.csv`, `torneos.csv`, `estadios.csv` y `arbitros.csv` — la misión se pausó explícitamente para revisar la calidad de `selecciones.csv` antes de continuar, y no se ha retomado todavía.
- **Próxima misión recomendada:** Retomar MS-002 (archivos restantes) antes de avanzar a misiones que dependan de torneos/estadios reales (ej. partidos).

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
