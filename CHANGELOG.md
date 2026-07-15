# Changelog

Todas las modificaciones notables del Modelo Santiago se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [Unreleased]

### Added

- `README.md`: se documenta el propósito del proyecto, la filosofía y principios, la estructura completa del repositorio (`docs/`, `engine/`, `models/`, `prompts/`, `.claude/agents/`, `data/`), el flujo de trabajo de una predicción, el orden de lectura recomendado, las reglas del proyecto y el estado actual del repositorio.

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
