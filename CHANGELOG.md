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
