# Modelo Santiago

Sistema probabilístico para la predicción de partidos de fútbol y la evaluación de mercados de apuestas deportivas.

Este repositorio **no es una aplicación de software tradicional**: es un repositorio de documentación, investigación y prompts en Markdown pensado para ser operado por agentes de Claude Code. No contiene código fuente ejecutable, por lo que no existen comandos de build, lint ni test.

El objetivo del proyecto no es adivinar resultados, sino construir un modelo estadístico capaz de generar probabilidades **explicables, auditables y rentables a largo plazo**.

---

## Principios

1. Nunca enamorarse del favorito.
2. Los datos actuales pesan más que la historia.
3. Toda predicción debe ser auditable.
4. Nunca modificar pesos sin evidencia.
5. Si el modelo recomienda no apostar, no se apuesta.
6. El objetivo es maximizar el ROI, no acertar un partido.

Ver detalle en [`docs/00-principios.md`](docs/00-principios.md).

---

## Estructura del repositorio

```
ModelPredictionApplication/
│
├── README.md
├── CLAUDE.md
│
├── .claude/
│   └── agents/            # Definición de los agentes especializados
│
├── docs/                  # Documentación funcional del modelo
├── engine/                # Motores lógicos de predicción
├── models/                # Investigación matemática y estadística
├── prompts/               # Plantillas reutilizables para tareas específicas
│
└── data/                  # Base de conocimiento del modelo
    ├── raw/               # Datos crudos desde fuentes externas (nunca se modifican)
    ├── processed/         # Datos validados y normalizados (única fuente para engine/)
    ├── predictions/        # Predicciones generadas por el modelo
    ├── results/            # Resultados oficiales para auditoría
    ├── audit/              # Métricas históricas de rendimiento
    └── archive/            # Información histórica (nunca se elimina)
```

> `LICENSE`, `scripts/` y `excel/` forman parte de la arquitectura objetivo pero todavía no existen en este repositorio. Antes de asumir que existen, verifica el estado real del directorio.

### docs/ — Reglas y filosofía del modelo

| Documento | Contenido |
|---|---|
| [`00-principios.md`](docs/00-principios.md) | Principios rectores del modelo |
| [`01-modelo.md`](docs/01-modelo.md) | Descripción general del Modelo Santiago |
| [`02-Variables.md`](docs/02-Variables.md) | Variables utilizadas por el modelo |
| [`03-Algoritmo.md`](docs/03-Algoritmo.md) | Algoritmo de predicción |
| [`04-Base-de-Conocimiento.md`](docs/04-Base-de-Conocimiento.md) | Arquitectura de datos |
| [`05-Backroll.md`](docs/05-Backroll.md) | Gestión de bankroll |
| [`06-predicciones.md`](docs/06-predicciones.md) | Formato y ejemplos de predicciones |
| [`07-Auditoria.md`](docs/07-Auditoria.md) | Métricas de auditoría (ROI, Yield) |
| [`08-aprendizaje.md`](docs/08-aprendizaje.md) | Aprendizaje y recalibración del modelo |
| [`09-Versiones.md`](docs/09-Versiones.md) | Historial de versiones del modelo |
| [`10-Roadmap.md`](docs/10-Roadmap.md) | Hoja de ruta del proyecto |
| [`11-Glosario.md`](docs/11-Glosario.md) | Glosario de términos (xG, ROI, Yield, etc.) |

### engine/ — Motores de predicción

Cada motor tiene una única responsabilidad y consume exclusivamente información desde `data/processed/`. Nunca acceden directamente a Internet.

| Motor | Responsabilidad |
|---|---|
| [`01-Offensive-Strength.md`](engine/01-Offensive-Strength.md) | Fuerza ofensiva de los equipos |
| [`02-Defensive-Strength.md`](engine/02-Defensive-Strength.md) | Fuerza defensiva de los equipos |
| [`03-Poisson.md`](engine/03-Poisson.md) | Distribución de probabilidades de marcadores |
| [`04-Chaos-Index.md`](engine/04-Chaos-Index.md) | Índice de imprevisibilidad del partido |
| [`05-Confidence.md`](engine/05-Confidence.md) | Nivel de confianza de la predicción |
| [`06-Expected-Value.md`](engine/06-Expected-Value.md) | Valor esperado frente a las cuotas de mercado |

### models/ — Investigación y fundamento científico

Documenta el respaldo estadístico/matemático de cada componente del engine, siguiendo la estructura obligatoria de 8 secciones (Objetivo, Descripción, Problema que resuelve, Ventajas, Limitaciones, Aplicación, Referencias, Versión 2.0).

- [`poisson.md`](models/poisson.md)
- [`elo.md`](models/elo.md)
- [`expected-value.md`](models/expected-value.md)
- [`confidence.md`](models/confidence.md)
- [`offensive-strength.md`](models/offensive-strength.md)
- [`defensive-strength.md`](models/defensive-strength.md)

**Ningún motor puede incorporar fórmulas, variables o algoritmos nuevos sin una investigación previa documentada aquí.**

### prompts/ — Plantillas de tareas

Instrucciones reutilizables, sin lógica del modelo:

- [`prediction-template.md`](prompts/prediction-template.md)
- [`recalibration-template.md`](prompts/recalibration-template.md)
- [`audit-template.md`](prompts/audit-template.md)
- [`tournament-analysis-template.md`](prompts/tournament-analysis-template.md)

### .claude/agents/ — Agentes especializados

Cada agente tiene una única responsabilidad y termina con un "Juramento del Agente" que fija su compromiso con la arquitectura del modelo.

| Agente | Rol |
|---|---|
| [`orchestrator.md`](.claude/agents/orchestrator.md) | Coordinador principal; no predice ni analiza estadísticas |
| [`predictor.md`](.claude/agents/predictor.md) | Estima probabilidades y los marcadores más probables |
| [`statistician.md`](.claude/agents/statistician.md) | Valida que las estadísticas sean suficientes y confiables |
| [`odds-analyzer.md`](.claude/agents/odds-analyzer.md) | Compara probabilidades del modelo con las cuotas de mercado |
| [`bankroll-manager.md`](.claude/agents/bankroll-manager.md) | Propone distribución de capital (fuera del núcleo del modelo) |
| [`auditor.md`](.claude/agents/auditor.md) | Compara predicciones con resultados reales |

---

## Flujo de trabajo de una predicción

1. Leer la documentación en `docs/`.
2. Consultar los motores en `engine/`.
3. Obtener información desde `data/processed/`.
4. Si faltan datos, consultar `data/raw/`.
5. Generar la predicción.
6. Guardar la predicción en `data/predictions/`.
7. Cuando el partido finalice, registrar el resultado en `data/results/`.
8. Actualizar las métricas en `data/audit/`.

## Orden de lectura recomendado

Antes de realizar cualquier modificación, revisar en este orden:

1. `CLAUDE.md`
2. `docs/01-modelo.md`
3. `docs/02-Variables.md`
4. `docs/03-Algoritmo.md`
5. `engine/`
6. `CHANGELOG.md`

Si existe conflicto entre documentos, prevalece el de mayor prioridad.

---

## Reglas del proyecto

- Nunca inventar datos.
- Nunca modificar un algoritmo sin documentarlo.
- Nunca modificar una variable sin justificar el cambio.
- Nunca alterar pesos sin evidencia estadística.
- Nunca mezclar documentación funcional (`docs/`) con implementaciones matemáticas (`models/`) o lógica del engine.
- Toda modificación debe poder ser auditada.
- Toda mejora debe registrarse en `CHANGELOG.md`.

Ver el detalle completo de reglas, estándares y responsabilidades en [`CLAUDE.md`](CLAUDE.md).

---

## Estado actual

Proyecto en desarrollo activo (**v1.0**). Estructura de `docs/`, `models/` y `.claude/agents/` ya operativa; `engine/` cuenta con un documento por motor (la separación formal en v1.0 Arquitectura / v2.0 Implementación matemática está pendiente); `data/` contiene únicamente marcadores de posición, sin datos reales todavía. `LICENSE`, `scripts/` y `excel/` aún no se han creado. Todo cambio relevante se registra en [`CHANGELOG.md`](CHANGELOG.md).

Consultar [`docs/10-Roadmap.md`](docs/10-Roadmap.md) para la hoja de ruta.

---

## Objetivo

Construir el sistema probabilístico de predicción deportiva más consistente, transparente y mantenible posible, priorizando siempre la calidad del modelo sobre la velocidad de desarrollo.
