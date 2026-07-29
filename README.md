# Modelo Santiago

Sistema probabilístico para la predicción de partidos de fútbol y la evaluación de mercados de apuestas deportivas.

Este repositorio nació como un repositorio de documentación, investigación y prompts en Markdown, pensado para ser operado por agentes de Claude Code. **Ya no es únicamente eso**: desde `BUILD-001` existe, además, una aplicación Python real (`app/`) que implementa esa documentación — Runtime, Capa de Preparación de Variables, los 6 motores del Engine, Persistencia (SQLAlchemy/PostgreSQL/Alembic) y una API mínima (FastAPI) — junto con una Base de Conocimiento (`data/processed/`) que ya contiene datos reales para varias entidades. `docs/`, `models/` y `engine/` siguen siendo la fuente de verdad conceptual y matemática; `app/` es su implementación en código, sin redefinir nada de lo que esos documentos ya deciden.

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
├── LICENSE
├── CHANGELOG.md
│
├── pyproject.toml         # Dependencias y metadatos del paquete Python (FastAPI, SQLAlchemy, Alembic, pytest...)
├── Dockerfile             # Imagen de la aplicación (Python 3.12-slim + uvicorn)
├── docker-compose.yml     # Orquestación mínima de desarrollo: app + PostgreSQL 16
├── alembic.ini            # Configuración de migraciones de base de datos
├── .env.example           # Variables de entorno de ejemplo (nunca el archivo .env real)
│
├── .claude/
│   └── agents/            # Definición de los agentes especializados
│
├── app/                   # Aplicación Python real — ver sección dedicada más abajo
├── migrations/            # Migraciones Alembic (versions/ vacío: sin datos aún poblados en PostgreSQL)
├── tests/                 # Bootstrap del paquete de pruebas (sin casos de prueba todavía)
├── scripts/               # Bootstrap del directorio (sin scripts todavía — ver scripts/README.md)
│
├── docs/                  # Documentación funcional del modelo (40 documentos)
├── engine/                # Especificación conceptual de los 6 motores (Markdown) — no confundir con app/engine/
├── models/                # Investigación matemática y estadística (16 documentos)
├── learning/              # Aprendizaje continuo: análisis de errores y recalibración
├── prompts/                # Plantillas reutilizables para tareas específicas
│
└── data/                  # Base de conocimiento del modelo
    ├── raw/               # Datos crudos desde fuentes externas (nunca se modifican) — sin archivos de datos todavía
    ├── processed/         # Datos validados y normalizados (única fuente para engine/) — ver estado real abajo
    ├── predictions/        # Predicciones generadas por el modelo — sin poblar todavía
    ├── results/            # Resultados oficiales para auditoría — sin poblar todavía
    ├── audit/              # Métricas históricas de rendimiento — sin poblar todavía
    └── archive/            # Información histórica (nunca se elimina) — sin poblar todavía
```

> `excel/` forma parte de la arquitectura objetivo original de `CLAUDE.md` pero todavía no existe en este repositorio.

### `app/` — La aplicación Python real

Materializa, paquete por paquete, la arquitectura fijada en [`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`](docs/35-Arquitectura-Oficial-del-Proyecto-Python.md). El Engine (`app/engine/`) nunca conoce FastAPI, SQLAlchemy ni PostgreSQL — su única entrada es el `PredictionContext`.

| Paquete | Contenido | Estado |
|---|---|---|
| `app/api/` | `predict_controller.py` — único endpoint, `POST /predict`, invoca `PredictMatchUseCase` | Creado (`BUILD-026`); aún no montado en `app/main.py` |
| `app/application/` | `predict_match.py` — `PredictMatchUseCase`, primer caso de uso de punta a punta | Implementado (`BUILD-025`) |
| `app/runtime/` | `prediction_context.py` (el objeto `PredictionContext`, append-only), `runtime.py` (`PredictionRuntime`), `engine_pipeline.py` (`EnginePipeline`, integra Preparación + Engine) | Implementado (`BUILD-004`/`BUILD-005`/`INT-001`) |
| `app/preparation/` | `preparation.py` (`VariablePreparation`) — transforma la Base de Conocimiento en las 12 Variables Oficiales | Implementado para las 9 de 9 variables activas (`BUILD-017` a `BUILD-024`, `FIX-002`) |
| `app/engine/` | `engine01.py` a `engine06.py` (los 6 motores) + `engine_runner.py` (orquestador por capas). `engine03.py` incluye la corrección Dixon-Coles (`IMP-003`), desactivada por defecto (`RHO_DIXON_COLES=0.0`) | Implementado (`BUILD-007`, `BUILD-009` a `BUILD-015`, `IMP-003`) — produce un número final real para los partidos con historial suficiente (`VALID-003`/`VALID-004`: 35 de 124 evaluables) |
| `app/persistence/` | Acceso a datos: sesión SQLAlchemy, repositorios, `CsvPreparationRepository`, `HistoricalMuGolProvider`, `RuntimePersistence` | Implementado (`BUILD-003`, `BUILD-008`, `BUILD-016`, `BUILD-017`) |
| `app/models/` | Clases SQLAlchemy de las 14 tablas físicas (`docs/33`) | Declaradas; ninguna tabla poblada en PostgreSQL todavía |
| `app/schemas/` | Contratos Pydantic de la API | Bootstrap, sin esquemas propios todavía |
| `app/services/` | Validación previa, auditoría, bankroll (fuera del camino crítico del Runtime) | Bootstrap, sin implementación todavía |
| `app/config/` | Configuración transversal | Bootstrap |

**Cadena ya integrada, de punta a punta:** `PredictMatchUseCase → EnginePipeline → VariablePreparation → EngineRunner → Engine01…Engine06`. El único tramo que falta para que sea alcanzable por HTTP es montar el router de `app/api/` en `app/main.py`. `Engine03` ya incluye, desde `IMP-003`, la corrección Dixon-Coles sobre la matriz de marcadores (`ρ=0` por defecto — desactivada en la práctica, ver "Estado actual"). Predicciones reales **ya son posibles** para un subconjunto de partidos: `data/processed/` tiene hoy 124 partidos reales y 133 filas de estadísticas (`DATA-006` a `DATA-009`), de los cuales 35 resultan evaluables por el Engine con el histórico disponible (`VALID-003`/`VALID-004`) — ver "Estado actual" para el detalle completo.

### docs/ — Reglas y filosofía del modelo

| Documento | Contenido |
|---|---|
| [`00-Project-Tracker.md`](docs/00-Project-Tracker.md) | Seguimiento oficial del estado de **todas** las misiones del proyecto — la referencia más actualizada del repositorio |
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
| [`18-Plan-de-Reconciliacion-Arquitectonica.md`](docs/18-Plan-de-Reconciliacion-Arquitectonica.md) | Inventario de inconsistencias del Engine y roadmap de reconciliación (`MR-001`) |
| [`19-Architecture-Freeze-Review.md`](docs/19-Architecture-Freeze-Review.md) | Auditoría independiente del inventario anterior (`AR-001`) |
| [`20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md`](docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md) | Jerarquía de autoridad y roadmap de gobernanza documental (`GR-001`) |
| [`21-Constitucion-del-Modelo-Santiago.md`](docs/21-Constitucion-del-Modelo-Santiago.md) | Principios estables de máxima autoridad conceptual (`GOV-001`) |
| [`22-Manual-Operativo-del-Arquitecto-IA.md`](docs/22-Manual-Operativo-del-Arquitecto-IA.md) | Protocolo operativo de toda misión de arquitectura (`GOV-002`) |
| [`23-Plan-Maestro-de-Reconciliacion-Operativa.md`](docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md) | Matriz de reconciliación y criterios de Architecture Freeze (`AR-002`) |
| [`24-Analisis-Arquitectonico-INC-04-INC-05.md`](docs/24-Analisis-Arquitectonico-INC-04-INC-05.md) | Resolución de las incidencias de Compatibilidad Táctica y Contrato de Datos de Mercado (`MR-004`) |
| [`25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`](docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md) | `PredictionRequest`, traza numérica de fases y `PredictionReport` |
| [`26-Runtime-del-Modelo.md`](docs/26-Runtime-del-Modelo.md) | El Runtime, el Objeto de Contexto append-only, logs y manejo de errores (`DEV-001`) |
| [`27-Auditoria-de-Variables-Pendientes.md`](docs/27-Auditoria-de-Variables-Pendientes.md) | Clasificación A-E de disponibilidad real de dato, variable por variable (`DATA-001`) |
| [`28-Catalogo-de-Variables-Derivadas.md`](docs/28-Catalogo-de-Variables-Derivadas.md) | Catálogo de variables derivadas/intermedias (`DATA-002`) |
| [`29-Arquitectura-del-Runtime.md`](docs/29-Arquitectura-del-Runtime.md) | Los 7 componentes de implementación del Runtime, con nombre propio (`DEV-002`) |
| [`30-Contrato-Oficial-del-Prediction-Context.md`](docs/30-Contrato-Oficial-del-Prediction-Context.md) | Especificación completa de `PredictionContext` y sus 10 bloques (`DEV-003`) |
| [`31-Modelo-Fisico-de-la-Base-de-Conocimiento.md`](docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md) | Modelo físico conceptual de la Base de Conocimiento (`DATA-003`) |
| [`32-Modelo-Relacional-Oficial.md`](docs/32-Modelo-Relacional-Oficial.md) | Entidades, relaciones, dependencias y claves conceptuales (`DATA-004`) |
| [`33-Modelo-Fisico-PostgreSQL.md`](docs/33-Modelo-Fisico-PostgreSQL.md) | Modelo físico PostgreSQL: tipos, restricciones, índices, UUID (`DATA-005`) |
| [`34-Decision-Oficial-del-Stack-Tecnologico.md`](docs/34-Decision-Oficial-del-Stack-Tecnologico.md) | Python + FastAPI + SQLAlchemy + Alembic + pytest como stack oficial (`ARCH-000`) |
| [`35-Arquitectura-Oficial-del-Proyecto-Python.md`](docs/35-Arquitectura-Oficial-del-Proyecto-Python.md) | Árbol de paquetes de `app/` y matriz de dependencias entre ellos (`DEV-004`) |
| [`36-Estrategia-Oficial-de-Variables-Pendientes.md`](docs/36-Estrategia-Oficial-de-Variables-Pendientes.md) | Veredicto de implementabilidad de Variable006/007/008/009 (`GR-010`) |
| [`37-Estrategia-Poblacion-Base-Conocimiento.md`](docs/37-Estrategia-Poblacion-Base-Conocimiento.md) | Orden oficial de población de CSV y Conjunto Mínimo Viable (`MS-011`) |
| [`38-Protocolo-Oficial-Ingesta-Datos.md`](docs/38-Protocolo-Oficial-Ingesta-Datos.md) | Flujo de ingesta, fuentes por entidad y reglas de aceptación/rechazo de datos (`MS-012`) |
| [`99-Mapa-Maestro.md`](docs/99-Mapa-Maestro.md) | Mapa de navegación de alto nivel de toda la arquitectura (`MAP-001`) |

### engine/ — Especificación conceptual de los motores (Markdown)

Cada motor tiene una única responsabilidad. Consume exclusivamente variables ya preparadas por la Capa de Preparación de Variables ([`docs/15-Capa-de-Preparacion-de-Variables.md`](docs/15-Capa-de-Preparacion-de-Variables.md)) — nunca lee `data/processed/` directamente ni conoce su origen físico. Nunca accede directamente a Internet.

> **No confundir con `app/engine/`**: este directorio (`engine/`) contiene la especificación conceptual en Markdown de cada motor; `app/engine/` contiene su implementación real en Python (`engine01.py` a `engine06.py`). El primero es la fuente de verdad matemática (junto con `models/`); el segundo es su traducción a código, sin redefinir nada.

| Motor | Responsabilidad | Implementación en `app/engine/` |
|---|---|---|
| [`01-Offensive-Strength.md`](engine/01-Offensive-Strength.md) | Fuerza ofensiva de los equipos | `engine01.py` |
| [`02-Defensive-Strength.md`](engine/02-Defensive-Strength.md) | Fuerza defensiva de los equipos | `engine02.py` |
| [`03-Poisson.md`](engine/03-Poisson.md) | Distribución de probabilidades de marcadores | `engine03.py` |
| [`04-Chaos-Index.md`](engine/04-Chaos-Index.md) | Índice de imprevisibilidad del partido | `engine04.py` |
| [`05-Confidence.md`](engine/05-Confidence.md) | Nivel de confianza de la predicción | `engine05.py` |
| [`06-Expected-Value.md`](engine/06-Expected-Value.md) | Valor esperado frente a las cuotas de mercado | `engine06.py` |

### models/ — Investigación y fundamento científico

Documenta el respaldo estadístico/matemático de cada componente del engine, siguiendo la estructura obligatoria de 8 secciones (Objetivo, Descripción, Problema que resuelve, Ventajas, Limitaciones, Aplicación, Referencias, Versión 2.0).

- [`poisson.md`](models/poisson.md) — fundamento de `Engine03`; §16 investiga Dixon-Coles (`MODEL-019`)
- [`elo.md`](models/elo.md)
- [`expected-value.md`](models/expected-value.md)
- [`confidence.md`](models/confidence.md)
- [`offensive-strength.md`](models/offensive-strength.md)
- [`defensive-strength.md`](models/defensive-strength.md)
- [`chaos-index.md`](models/chaos-index.md)
- [`parameter-calibration.md`](models/parameter-calibration.md) — catálogo de parámetros/pesos pendientes de calibración real
- [`forma-reciente.md`](models/forma-reciente.md) — Variable001, ya implementada en `app/preparation/`
- [`rendimiento-torneo.md`](models/rendimiento-torneo.md) — Variable002, ya implementada
- [`profundidad-plantilla.md`](models/profundidad-plantilla.md) — Variable008 (componente Profundidad), ya implementada
- [`fatiga.md`](models/fatiga.md) — Variable007 (alcance reducido), ya implementada
- [`disponibilidad.md`](models/disponibilidad.md) — Variable006 (alcance reducido), ya implementada
- [`estabilizacion-muestras-pequenas.md`](models/estabilizacion-muestras-pequenas.md) — diseño del Shrinkage de Variable003/004 (`MODEL-017`/`018`, implementado en `IMP-002`); investigación de si Variable001 (`MODEL-021`) y Variable007 (`MODEL-022`) necesitan el mismo mecanismo
- [`dixon-coles.md`](models/dixon-coles.md) — diseño matemático/arquitectónico completo de la corrección Dixon-Coles (`MODEL-020`), implementada en `IMP-003` y validada en `VALID-004`
- [`error-modelo.md`](models/error-modelo.md) — descomposición cuantitativa del error residual del modelo en 8 dimensiones (`ANL-004`); hallazgo central: ~90-95% del error medido es inherente al Poisson, no corregible por mejor calibración

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

En código, este mismo flujo (etapas 3-5) ya existe implementado como `PredictMatchUseCase → EnginePipeline → VariablePreparation → EngineRunner → Engine01…Engine06` (`app/application/`, `app/runtime/`, `app/preparation/`, `app/engine/`) — ver "Estado actual" para qué falta para que produzca una predicción real.

## Orden de lectura recomendado

Antes de realizar cualquier modificación, revisar en este orden (detalle completo y justificación en `CLAUDE.md`, secciones "Orden de Lectura" y "Jerarquía Documental"):

1. `docs/21-Constitucion-del-Modelo-Santiago.md` — principios estables, máxima autoridad conceptual.
2. `CLAUDE.md` — gobierna el comportamiento operativo.
3. `docs/22-Manual-Operativo-del-Arquitecto-IA.md` — protocolo de trabajo para toda misión de arquitectura.
4. `docs/00-Project-Tracker.md` — estado real de cada misión.
5. El resto de `docs/` relevante a la tarea, en orden numérico ascendente (regla que cubre automáticamente cualquier documento nuevo).
6. `engine/`, `models/`, `app/`, `data/`, según corresponda.
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

Ver el detalle completo de reglas, estándares y responsabilidades en [`CLAUDE.md`](CLAUDE.md). El principio de justificación de datos (todo campo de la Base de Conocimiento debe responder qué variable lo usa, si es derivable de otro dato ya existente, y si debe persistirse o calcularse en ejecución) está desarrollado en [`docs/05-Base-de-Conocimiento.md`](docs/05-Base-de-Conocimiento.md) — no se repite aquí.

---

## Estado actual

**Versión:** `1.1.0` (ver [`CHANGELOG.md`](CHANGELOG.md)) — primera versión que incluye una aplicación funcional completa, backtesting real y una corrección matemática (Dixon-Coles) diseñada, implementada y validada de punta a punta.

**Arquitectura:** completa en su eje de diseño. Los tres ejes — arquitectura del Engine (`docs/18` a `docs/23`), gobernanza documental y modelo de datos (`docs/31` a `docs/35`) — ya tienen una respuesta documentada de extremo a extremo. `app/` implementa esa arquitectura en Python: `PredictionContext`, `VariablePreparation`, los 6 motores del Engine (incluida la corrección Dixon-Coles en `Engine03`), `EngineRunner`, `EnginePipeline`, `PredictMatchUseCase` y un primer endpoint HTTP ya existen como código real, no solo como especificación.

**Variables Oficiales:** de las 9 activas en V1, **las 9 tienen método de cálculo real** — Forma Reciente, Rendimiento en el Torneo, Potencial Ofensivo, Solidez Defensiva, Disponibilidad de Plantilla y Fatiga en alcance reducido, Calidad de Plantilla en su componente Profundidad, Historial Directo, y **Localía**, cuyo bloqueo de esquema (`ValorVariable.valor` no admitía texto) quedó resuelto en `FIX-002`. Localía se calcula correctamente hoy, pero **no tiene efecto numérico todavía** sobre `λ`: `KAPPA_LOCAL`/`KAPPA_VISITANTE` permanecen en `0.0`, placeholders sin calibrar (`CAL-002` probó calibrarlos y decidió no aplicar el cambio por evidencia insuficiente). Ver [`docs/17-Matriz-de-Consumo-de-Variables.md`](docs/17-Matriz-de-Consumo-de-Variables.md) y las investigaciones matemáticas en `models/` (`MODEL-009` a `MODEL-015`) — completadas y, en el caso de Variable003/004, ya implementadas con Shrinkage (`IMP-002`) tras la aprobación explícita del cambio.

**Base de Conocimiento (`data/processed/selecciones-nacionales/`):** de las 11 entidades del módulo, **7 ya tienen datos reales**: `selecciones.csv` (62 selecciones), `competiciones.csv` (11 competiciones), `estadios.csv` (76 estadios), `arbitros.csv` (51 árbitros designados oficialmente por FIFA para el Mundial 2026), `torneos.csv` (15 ediciones reales), **`partidos.csv` (124 partidos reales, `DATA-006` a `DATA-009`, vía StatsBomb Open Data: Eurocopa 2020/2024, Copa América 2024)** y **`estadisticas_partido.csv` (133 filas de estadísticas reales por equipo/partido)**. Las 4 entidades restantes (`jugadores`, `convocatorias`, `lesiones`, `cuotas`) solo tienen el encabezado — por eso Variable006 (Disponibilidad, componente Lesiones) y Variable008 (Calidad de Plantilla, componente Valor de Mercado/Experiencia) siguen sin aportar señal real, y `Engine06` (Valor Esperado) nunca puede completarse sin cuotas. El orden oficial de captura y el Conjunto Mínimo Viable están definidos en [`docs/37-Estrategia-Poblacion-Base-Conocimiento.md`](docs/37-Estrategia-Poblacion-Base-Conocimiento.md); el protocolo de ingesta en [`docs/38-Protocolo-Oficial-Ingesta-Datos.md`](docs/38-Protocolo-Oficial-Ingesta-Datos.md).

**Backtesting y validación (Fase I):** con los 124 partidos reales, **35 resultan evaluables** por el Engine (el resto queda bloqueado por falta de historial previo del rival — cobertura de StatsBomb limitada a Eurocopa/Copa América, sin Mundial/Eliminatorias/Nations League). Sobre ese conjunto: Accuracy del ganador `60.0%`, Log Loss `0.889`, Brier `0.544` (`VALID-003`/`VALID-004`). La corrección Dixon-Coles (`MODEL-019`/`020`, `IMP-003`) fue diseñada, implementada y validada con un valor de referencia de la literatura (`ρ=-0.13`): mejora Log Loss (`-3.2%`) y Brier (`-2.0%`), pero **no se activa por defecto** (`ρ=0.0`) porque solo 3 de 9 métricas obligatorias mejoraron — no alcanza el criterio de aceptación de `VALID-004`. Una descomposición completa del error (`ANL-004`, [`models/error-modelo.md`](models/error-modelo.md)) encontró que **~90-95% del error observado es matemáticamente inevitable** dado el diseño Poisson-independiente (persistiría incluso con `λ` perfectos) — solo un 5-10% es, en principio, corregible por calibración. **Veredicto explícito, vigente:** la Fase I **no puede declararse cerrada** — el sesgo estructural hacia nunca predecir empates (recall `0%`) persiste sin resolver.

**`scripts/` y `tests/`:** ambos existen como directorios bootstrap (sin script ni caso de prueba real todavía) — todo el backtesting real de la Fase I se ejecutó mediante harnesses temporales de sesión, nunca comprometidos al repositorio (mismo patrón documentado en cada misión `VALID-`/`ANL-` del Tracker). `excel/` aún no se ha creado.

Todo cambio relevante se registra en [`CHANGELOG.md`](CHANGELOG.md). El estado detallado de cada misión — incluidas las series `MS-`, `MR-`, `AR-`, `GR-`, `GOV-`, `DEV-`, `DATA-`, `IMP-`, `MAP-`, `MODEL-`, `BUILD-`, `INT-`, `FIX-`, `CAL-`, `VALID-` y `ANL-` — se mantiene en [`docs/00-Project-Tracker.md`](docs/00-Project-Tracker.md), la referencia oficial para saber qué está completado, en progreso o pendiente.

## Licencia

Software y documentación propietarios. Todos los derechos reservados — ver [`LICENSE`](LICENSE).

Consultar [`docs/12-Roadmap.md`](docs/12-Roadmap.md) para la hoja de ruta.

---

## Objetivo

Construir el sistema probabilístico de predicción deportiva más consistente, transparente y mantenible posible, priorizando siempre la calidad del modelo sobre la velocidad de desarrollo.
