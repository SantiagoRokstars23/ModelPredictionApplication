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
7. Nunca inventar datos.
8. Toda decisión debe ser explicable.

Ver detalle en [`docs/01-principios.md`](docs/01-principios.md). Los principios estables y de máxima autoridad conceptual del proyecto se consolidan en [`docs/21-Constitucion-del-Modelo-Santiago.md`](docs/21-Constitucion-del-Modelo-Santiago.md).

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
├── learning/              # Aprendizaje continuo: análisis de errores y recalibración
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

> `scripts/` y `excel/` forman parte de la arquitectura objetivo pero todavía no existen en este repositorio. Antes de asumir que existen, verifica el estado real del directorio.

### docs/ — Reglas y filosofía del modelo

| Documento | Contenido |
|---|---|
| [`00-Project-Tracker.md`](docs/00-Project-Tracker.md) | Seguimiento oficial del estado de todas las misiones del proyecto |
| [`01-principios.md`](docs/01-principios.md) | Principios rectores del modelo |
| [`02-modelo.md`](docs/02-modelo.md) | Descripción general del Modelo Santiago |
| [`03-Variables.md`](docs/03-Variables.md) | Variables utilizadas por el modelo |
| [`04-Algoritmo.md`](docs/04-Algoritmo.md) | Algoritmo de predicción |
| [`05-Base-de-Conocimiento.md`](docs/05-Base-de-Conocimiento.md) | Arquitectura de datos |
| [`06-Flujo-Operacional.md`](docs/06-Flujo-Operacional.md) | Flujo de ejecución completo del modelo |
| [`07-Backroll.md`](docs/07-Backroll.md) | Gestión de bankroll |
| [`08-predicciones.md`](docs/08-predicciones.md) | Formato y ejemplos de predicciones |
| [`09-Auditoria.md`](docs/09-Auditoria.md) | Métricas de auditoría (ROI, Yield) |
| [`10-aprendizaje.md`](docs/10-aprendizaje.md) | Aprendizaje y recalibración del modelo |
| [`11-Versiones.md`](docs/11-Versiones.md) | Historial de versiones del modelo |
| [`12-Roadmap.md`](docs/12-Roadmap.md) | Hoja de ruta del proyecto |
| [`13-Glosario.md`](docs/13-Glosario.md) | Glosario de términos (xG, ROI, Yield, etc.) |
| [`14-Prediction-Pipeline.md`](docs/14-Prediction-Pipeline.md) | Especificación V0.1 del proceso de predicción a nivel de archivo |
| [`15-Capa-de-Preparacion-de-Variables.md`](docs/15-Capa-de-Preparacion-de-Variables.md) | Capa que transforma la Base de Conocimiento en variables normalizadas para el Engine |
| [`16-Contrato-Oficial-de-Variables.md`](docs/16-Contrato-Oficial-de-Variables.md) | Tipo, unidad, rango y ciclo de vida de las 12 variables oficiales |
| [`17-Matriz-de-Consumo-de-Variables.md`](docs/17-Matriz-de-Consumo-de-Variables.md) | Qué motor consume cada variable, y qué ocurre si falta |
| [`18-Plan-de-Reconciliacion-Arquitectonica.md`](docs/18-Plan-de-Reconciliacion-Arquitectonica.md) | Inventario de inconsistencias del Engine y roadmap de reconciliación (MR-001) |
| [`19-Architecture-Freeze-Review.md`](docs/19-Architecture-Freeze-Review.md) | Auditoría independiente del inventario anterior (AR-001) |
| [`20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md`](docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md) | Jerarquía de autoridad y roadmap de gobernanza documental (GR-001) |
| [`21-Constitucion-del-Modelo-Santiago.md`](docs/21-Constitucion-del-Modelo-Santiago.md) | Principios estables de máxima autoridad conceptual (GOV-001) |
| [`22-Manual-Operativo-del-Arquitecto-IA.md`](docs/22-Manual-Operativo-del-Arquitecto-IA.md) | Protocolo operativo de toda misión de arquitectura (GOV-002) |
| [`23-Plan-Maestro-de-Reconciliacion-Operativa.md`](docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md) | Matriz de reconciliación y criterios de Architecture Freeze (AR-002) |

### engine/ — Motores de predicción

Cada motor tiene una única responsabilidad. Consume exclusivamente variables ya preparadas por la Capa de Preparación de Variables ([`docs/15-Capa-de-Preparacion-de-Variables.md`](docs/15-Capa-de-Preparacion-de-Variables.md)) — nunca lee `data/processed/` directamente ni conoce su origen físico. Nunca accede directamente a Internet.

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

### learning/ — Aprendizaje continuo

Analiza el historial de predicciones ya resueltas para generar conocimiento auditable. Nunca calcula probabilidades, nunca predice y nunca modifica `data/`; solo lee predicciones/resultados cerrados y produce diagnósticos, patrones y propuestas de ajuste para revisión humana.

| Documento | Responsabilidad |
|---|---|
| [`README.md`](learning/README.md) | Marco general, límites del módulo y pipeline completo |
| [`error-analysis.md`](learning/error-analysis.md) | Diagnóstico de acierto/error partido a partido |
| [`pattern-discovery.md`](learning/pattern-discovery.md) | Sesgos recurrentes a través de múltiples partidos |
| [`confidence-calibration.md`](learning/confidence-calibration.md) | Verifica si el Índice de Confianza declarado es honesto |
| [`weight-adjustment.md`](learning/weight-adjustment.md) | Propuesta documentada de recalibración de pesos (nunca la aplica) |
| [`version-history.md`](learning/version-history.md) | Registro auditable de qué cambió entre versiones y por qué |

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
3. Obtener información desde `data/processed/` a través de la Capa de Preparación de Variables ([`docs/15-Capa-de-Preparacion-de-Variables.md`](docs/15-Capa-de-Preparacion-de-Variables.md)) — los motores nunca leen `data/processed/` directamente.
4. Si faltan datos, consultar `data/raw/`.
5. Generar la predicción.
6. Guardar la predicción en `data/predictions/`.
7. Cuando el partido finalice, registrar el resultado en `data/results/`.
8. Actualizar las métricas en `data/audit/`.

## Orden de lectura recomendado

Antes de realizar cualquier modificación, revisar en este orden (detalle completo y justificación en `CLAUDE.md`, secciones "Orden de Lectura" y "Jerarquía Documental"):

1. `docs/21-Constitucion-del-Modelo-Santiago.md` — principios estables, máxima autoridad conceptual.
2. `CLAUDE.md` — gobierna el comportamiento operativo.
3. `docs/22-Manual-Operativo-del-Arquitecto-IA.md` — protocolo de trabajo para toda misión de arquitectura.
4. `docs/00-Project-Tracker.md` — estado real de cada misión.
5. El resto de `docs/` relevante a la tarea, en orden numérico ascendente (regla que cubre automáticamente cualquier documento nuevo).
6. `engine/`, `models/`, `data/`, según corresponda.
7. `CHANGELOG.md`.

Si existe conflicto entre documentos, prevalece el de mayor prioridad según la Jerarquía Documental (`CLAUDE.md`).

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

Proyecto en desarrollo activo (**v1.0**). Estructura de `docs/`, `models/` y `.claude/agents/` ya operativa; `engine/` cuenta con un documento por motor (la separación formal en v1.0 Arquitectura / v2.0 Implementación matemática está pendiente); la mayor parte de `data/` contiene únicamente marcadores de posición, salvo [`data/processed/selecciones-nacionales/`](data/processed/selecciones-nacionales/README.md), que ya tiene datos reales (`selecciones.csv`, `competiciones.csv`). `scripts/` y `excel/` aún no se han creado.

El diseño arquitectónico del Engine y su gobernanza documental completó una fase de reconciliación (`docs/18` a `docs/23`: inventario de inconsistencias, auditoría independiente, jerarquía de gobernanza, Constitución del Modelo Santiago y Manual Operativo del Arquitecto IA) — la ejecución efectiva de esas correcciones sobre `engine/` y el resto de `docs/` sigue en curso. Todo cambio relevante se registra en [`CHANGELOG.md`](CHANGELOG.md). El estado detallado de cada misión, incluyendo el roadmap de reconciliación pendiente, se mantiene en [`docs/00-Project-Tracker.md`](docs/00-Project-Tracker.md), la referencia oficial para saber qué está completado, en progreso o pendiente.

## Licencia

Software y documentación propietarios. Todos los derechos reservados — ver [`LICENSE`](LICENSE).

Consultar [`docs/12-Roadmap.md`](docs/12-Roadmap.md) para la hoja de ruta.

---

## Objetivo

Construir el sistema probabilístico de predicción deportiva más consistente, transparente y mantenible posible, priorizando siempre la calidad del modelo sobre la velocidad de desarrollo.


# Principio de Justificación de Datos

Todo dato almacenado dentro de la Base de Conocimiento deberá justificar su existencia.

Antes de incorporar un nuevo campo o una nueva entidad, deberá responderse obligatoriamente las siguientes preguntas:

1. ¿Qué variable(s) del Modelo Santiago utilizan este dato?
2. ¿Cómo mejora la precisión de las predicciones?
3. ¿Puede obtenerse a partir de otro dato ya existente?
4. ¿Es información permanente o información temporal?
5. ¿Pertenece realmente a la Base de Conocimiento o debe calcularse durante la ejecución del modelo?

Si un dato no aporta valor directo o indirecto al cálculo de probabilidades, no deberá formar parte de la versión 1.0.

El objetivo del Modelo Santiago no es construir una base de datos completa de fútbol.

El objetivo es almacenar únicamente la información necesaria para maximizar la calidad de las predicciones.

Se priorizarán:

- Calidad sobre cantidad.
- Información útil sobre información interesante.
- Datos necesarios sobre datos decorativos.
- Simplicidad sobre complejidad.

Todo campo deberá tener una razón de existir.
