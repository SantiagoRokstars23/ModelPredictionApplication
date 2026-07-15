# Changelog

Todas las modificaciones notables del Modelo Santiago se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [Unreleased]

### Added

- `README.md`: se documenta el propósito del proyecto, la filosofía y principios, la estructura completa del repositorio (`docs/`, `engine/`, `models/`, `prompts/`, `.claude/agents/`, `data/`), el flujo de trabajo de una predicción, el orden de lectura recomendado, las reglas del proyecto y el estado actual del repositorio.
- `LICENSE`: se establece licencia propietaria (todos los derechos reservados) a nombre de Santiago Grueso, dado el potencial valor comercial del modelo (ROI en mercados de apuestas).
- `docs/04-Base-de-Conocimiento.md`: se agrega el "Principio de Justificación de Datos" — todo campo de la Base de Conocimiento debe justificarse mediante una variable (`docs/02-Variables.md`), un paso del algoritmo (`docs/03-Algoritmo.md`), un motor (`engine/`) o una necesidad de integridad/trazabilidad. Se añade la regla correspondiente en la sección "Reglas".
- `data/processed/selecciones-nacionales/`: Misión 001 — primer módulo de la Base de Conocimiento (Selecciones Nacionales). 11 entidades (`selecciones`, `jugadores`, `convocatorias`, `partidos`, `estadisticas_partido`, `lesiones`, `cuotas`, `arbitros`, `estadios`, `competiciones`, `torneos`) con esquema documentado en `README.md` del módulo, incluyendo justificación por campo. Se elimina `campeon_id_seleccion` de `torneos` por ser un dato derivado; se difiere explícitamente a una misión futura la estadística individual de jugador por partido; se define la competición `Amistosos Internacionales` y un torneo contenedor por año calendario (`TOR-2026-AMISTOSOS`) para evitar `id_torneo` nulo en partidos amistosos. Los CSV se crean solo con encabezados (sin datos reales), salvo las filas de catálogo de `competiciones.csv` y `torneos.csv` para amistosos.
- `data/processed/selecciones-nacionales/selecciones.csv`: Misión 002 — se incorporan las primeras 40 selecciones nacionales (Top 40 del ranking FIFA vigente al 2026-06-11), con federación oficial, confederación, seleccionador actual y estado de actividad, verificados mediante fuentes web (ver detalle de fuentes en el reporte de la misión). Rusia se marca `activa: false` por su suspensión de competiciones FIFA/UEFA desde 2022.
- `learning/`: Misión 003 — diseño arquitectónico del módulo de aprendizaje continuo (`README.md`, `error-analysis.md`, `pattern-discovery.md`, `confidence-calibration.md`, `weight-adjustment.md`, `version-history.md`). Define un pipeline de solo lectura sobre `data/predictions/`/`data/results/` que nunca calcula probabilidades, nunca predice y nunca modifica la Base de Conocimiento: produce diagnósticos, patrones, calibración y propuestas de ajuste de peso que requieren aprobación humana explícita antes de aplicarse en `docs/02-Variables.md`/`engine/`. Sin implementación de algoritmos (queda pendiente de respaldo en `models/`, igual que `engine/`).
- `docs/05-Flujo-Operacional.md`: Misión 004 — diseño del flujo operacional completo del Modelo Santiago (orquestación, validación de datos, orden de ejecución del Engine por capas de dependencia, manejo de errores, integración con `data/`, `engine/` y `learning/`). Al insertarse en la posición 05, se renumeran los documentos `05-Backroll.md`→`06-Backroll.md`, `06-predicciones.md`→`07-predicciones.md`, `07-Auditoria.md`→`08-Auditoria.md`, `08-aprendizaje.md`→`09-aprendizaje.md`, `09-Versiones.md`→`10-Versiones.md`, `10-Roadmap.md`→`11-Roadmap.md` y `11-Glosario.md`→`12-Glosario.md`, con actualización de todas las referencias cruzadas en `README.md`, `CLAUDE.md`, `learning/` y `data/processed/selecciones-nacionales/README.md`. Se documenta además una inconsistencia preexistente en `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` (referencias a archivos inexistentes `engine/07-Bankroll-Engine.md` y `engine/08-Simulation.md`), sin corregirla por estar fuera del alcance de esta misión.

### Changed

- `docs/05-Flujo-Operacional.md` (v1.0.0 → v1.1.0): Misión 004A — refinamiento arquitectónico. Se incorpora explícitamente la participación de `CLAUDE.md` (gobierna todo el flujo), `prompts/` (dispara cada fase) y `models/` (define la lógica matemática que `engine/` ejecuta) como capas propias del flujo, con secciones dedicadas de integración para cada una. Se refuerza que `learning/` nunca puede modificar automáticamente `docs/`, `engine/`, `models/` ni ninguna variable — su única salida es una propuesta que requiere aprobación explícita del Arquitecto Estadístico del Modelo Santiago. Se agrega la Fase 10 — Versionado como cierre final del flujo (`learning/` → Versionado → nueva versión del modelo), que solo se ejecuta tras una aprobación explícita y documenta el cambio en `docs/10-Versiones.md`, `learning/version-history.md` y `CHANGELOG.md`.
- `docs/00-Project-Tracker.md`: Misión 005 — sistema de seguimiento oficial del proyecto (lista de misiones MS-001 a MS-005 con estado, % de avance, dependencias, fechas y observaciones; resumen general con % global, módulos terminados/en desarrollo/pendientes y riesgos identificados). El número `00` ya estaba ocupado por `docs/00-principios.md`; por decisión explícita del usuario se renumeraron los 13 documentos existentes de `docs/` (`00-principios.md`→`01-principios.md` ... `12-Glosario.md`→`13-Glosario.md`) para que el tracker ocupe literalmente la posición `00`, actualizando todas las referencias cruzadas en `README.md`, `CLAUDE.md`, `engine/`, `learning/` y `data/processed/selecciones-nacionales/README.md`.

---

## [1.0.0] - 2026-07-14

### Added

- Estructura inicial del proyecto: `docs/`, `engine/`, `models/`, `prompts/`, `data/` y `.claude/agents/`.
- Documentación funcional en `docs/` (principios, modelo, variables, algoritmo, base de conocimiento, bankroll, predicciones, auditoría, aprendizaje, versiones, roadmap, glosario).
- Motores de predicción en `engine/`: Offensive Strength, Defensive Strength, Poisson, Chaos Index, Confidence y Expected Value.
- Investigación matemática en `models/`: Poisson, Elo, Expected Value, Confidence, Offensive Strength y Defensive Strength.
- Plantillas reutilizables en `prompts/`: predicción, recalibración, auditoría y análisis de torneo.
- Agentes especializados en `.claude/agents/`: orchestrator, predictor, statistician, odds-analyzer, bankroll-manager y auditor.
- Reglas de arquitectura y comportamiento definidas en `CLAUDE.md`.
