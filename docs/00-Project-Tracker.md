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
- Desde MR-001 el proyecto usa **series de numeración independientes** por tipo de misión: `MS-NNN` para misiones de **diseño** (avanzan la arquitectura), `MR-NNN` para misiones de **reconciliación del Engine** (corrigen inconsistencias ya detectadas en el Engine y su entorno inmediato), `AR-NNN` para **auditorías de congelamiento arquitectónico** (revisiones independientes y adversariales que intentan refutar que un inventario de inconsistencias esté completo), `GR-NNN` para **reconciliación de gobernanza documental** (corrigen inconsistencias en los documentos que gobiernan el proyecto), `GOV-NNN` para **gobernanza constitucional** (define principios estables de máxima autoridad conceptual, no técnica), `IMP-NNN` para **implementación conceptual** (sintetiza la arquitectura ya estable en trazados operativos de extremo a extremo) y, desde MAP-001, `MAP-NNN` para **mapas de navegación** (vistas de alto nivel para orientar a un lector nuevo, sin redefinir nada). Se listan en tablas separadas más abajo.
- **Nota práctica:** varios briefs recientes han reutilizado identificadores ya asignados a otra misión (`MR-002` dos veces, `MR-005`, `GOV-001`). Antes de asignar un identificador nuevo, conviene revisar este documento — la sección correspondiente a cada serie lista los identificadores ya reservados.

---

# Resumen general del proyecto

**Porcentaje global de avance:** ~76%

**Veredicto de Architecture Freeze:** No declarable todavía, pero de las 5 críticas originales de AR-002 ya quedan **4 resueltas** (INC-18/INC-21 por GR-002; INC-01 por MR-003; INC-04 completamente resuelto por la implementación de MR-004). Solo queda **INC-05**, y solo en su implementación completa — el principio arquitectónico ya está fijado (las cuotas nunca serán una Variable Oficial), pero `engine/06` todavía lee `cuotas.csv` directamente en espera del futuro Contrato de Datos de Mercado. De los 7 criterios objetivos de `docs/23` (Parte 6), se mantiene formalmente en **4 de 7** (el criterio 5, "ningún motor accede a `data/processed/` directamente", sigue sin cumplirse por esta única excepción ya documentada) — pero el criterio 1 ("cero críticas sin resolver") está a un solo paso de cumplirse. Próximo paso: diseñar el Contrato de Datos de Mercado (cierra INC-05 del todo), resolver INC-06 (Rotaciones), y `GR-003` (`data/README.md`).

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
- **Análisis arquitectónico de INC-04/INC-05** (`docs/24`, fase de análisis de MR-004): revela que 3 de las 5 variables huérfanas ya tienen datos completos (solo falta wiring) mientras 2 carecen de fuente de datos real en el esquema actual; recomienda tratar las cuotas como una categoría de datos de mercado paralela a las Variables Oficiales.
- **Cuarta reconciliación real ejecutada** (fase de implementación de `MR-004`): Localía, Historial Directo y Calidad de Plantilla (alcance reducido) ganan consumidor oficial en `engine/03`/`05`/`01`+`02`; Compatibilidad Táctica y Estado Psicológico quedan clasificadas formalmente como "Pendiente de futura investigación" en `docs/03`/`docs/16`/`docs/17`; principio arquitectónico de Datos de Mercado establecido para las cuotas — `INC-04` resuelto, `INC-05` resuelto en principio.
- **Primer trazado de implementación conceptual** (`IMP-001`): objeto de entrada, traza numérica de ejemplo y objeto de respuesta completo del Prediction Pipeline, con dos campos (`jugadores_destacados`, `mercados_detectados`) documentados explícitamente como fuera del alcance del Engine V1 actual, no inventados.
- **Mapa Maestro del proyecto** (`docs/99-Mapa-Maestro.md`, `MAP-001`): vista de alto nivel navegable en menos de diez minutos, categoriza los 26 documentos de `docs/` sin duplicar el listado de `README.md`.
- **Runtime Oficial** (`docs/26-Runtime-del-Modelo.md`, `DEV-001`): especificación de ejecución independiente del lenguaje, con el primer Objeto de Contexto formalizado (solo-anexado) y el primer registro de eventos de ejecución (logs) del proyecto.
- **Primera investigación matemática real de `models/`** (`models/offensive-strength.md`, `MODEL-001`): fórmula estructural de Fuerza Ofensiva, fundamentada en Maher (1982)/Dixon-Coles (1997), sin pesos numéricos (pendientes de calibración). Detecta que "grandes oportunidades" no existe en el esquema de datos actual.
- **Auditoría completa de datos pendientes** (`docs/27-Auditoria-de-Variables-Pendientes.md`, `DATA-001`): clasifica ~46 datos necesarios de las 12 variables en A-E; encuentra que "Clima" (variable ya activa) no existe en ningún CSV, y que no hay tabla de alineación titular por partido.
- **Catálogo de Variables Derivadas** (`docs/28-Catalogo-de-Variables-Derivadas.md`, `DATA-002`): 27 cantidades calculadas centralizadas en 6 categorías; revela que solo 2 alcanzan el estado "Diseñada" completo.
- **Segunda investigación matemática real** (`models/defensive-strength.md`, `MODEL-002`): reutiliza deliberadamente `M_forma`/`Pen` de `MODEL-001` para no duplicar variables compartidas; su término base no tiene ningún componente bloqueado, a diferencia de Offensive Strength.
- **Núcleo probabilístico completo** (`models/poisson.md`, `MODEL-003`): define por primera vez el mecanismo matemático exacto detrás de Probabilidad Local/Empate/Visitante y Top 4 de marcadores; documenta explícitamente por qué V1 no adopta la corrección de Dixon-Coles.
- **Índice de Confianza formalizado** (`models/confidence.md`, `MODEL-004`): distingue Probabilidad (aleatoria) de Confianza (epistémica); corrige un error del stub anterior que introducía una dependencia incompatible con la ejecución en paralelo del Engine.
- **Índice de Caos formalizado** (`models/chaos-index.md`, `MODEL-005`): primer documento de `models/` creado desde cero (`engine/04` nunca tuvo respaldo); usa entropía de Shannon sobre la distribución ya calculada por Poisson.
- **Núcleo matemático estructuralmente completo para los 6 motores** (`models/expected-value.md`, `MODEL-006`): fórmula `EV = (P_modelo · c) − 1`, derivada desde primeros principios; distingue Probabilidad → Expected Value → Gestión de Bankroll (Kelly queda fuera de alcance, pertenece a `engine/07` futuro); resuelve que `EV` es puro y `Recomendación` es donde se integran Confianza y Caos. Último de los 6 motores en obtener respaldo de investigación — condicionado, en su lado de mercado, al Contrato de Datos de Mercado (`INC-05`) todavía pendiente.
- **Arquitectura de Implementación del Runtime** (`docs/29-Arquitectura-del-Runtime.md`, `DEV-002`): descompone el Runtime de `docs/26` (DEV-001) en siete componentes con nombre y frontera propios (`PredictionRequest`, `PredictionContext`, `VariablePreparation`, `EngineRunner`, `PredictionAssembler`, `PredictionReport`, `Persistence`); formaliza por primera vez la frontera de escritura por sección del Objeto de Contexto y una categorización de estados de ejecución. Sigue condicionada, para producir un cálculo real, a la primera fórmula matemática con Versión 2.0 en `models/`.
- **Contrato Oficial del Prediction Context** (`docs/30-Contrato-Oficial-del-Prediction-Context.md`, `DEV-003`): estructura interna completa del `PredictionContext` en diez bloques (`metadata`, `match`, `variables`, `engine`, `prediction`, `market`, `bankroll`, `errors`, `audit`, `learning`), reutilizando verbatim la "Salida" ya declarada por los 6 motores de `engine/`. Aclara que el objeto en memoria vive solo durante una ejecución y que `audit`/`learning` se agregan después al registro ya persistido, nunca reabriendo el objeto original. Reserva `market` para el futuro Contrato de Datos de Mercado sin diseñarlo (`INC-05` sigue pendiente).
- **Modelo Físico Oficial de la Base de Conocimiento** (`docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md`, `DATA-003`): 13 dominios de información con responsabilidad única, relaciones puramente conceptuales, y la frontera exacta entre la Base de Conocimiento (permanente) y el `PredictionContext` (transitorio, `docs/30`). Detecta, sin corregir, un residuo editorial en el encabezado interno de `docs/05-Base-de-Conocimiento.md`.
- **Modelo Relacional Oficial** (`docs/32-Modelo-Relacional-Oficial.md`, `DATA-004`): 15 entidades conceptuales, relaciones y cardinalidades (exactamente dos N:M en todo el modelo), claves conceptuales sin tipos de dato ni mecanismo físico. Grafo de dependencias acíclico, compatible con el orden de lectura de `docs/14`. Sigue sin resolver si Propuesta de Aprendizaje necesita tabla física propia.
- **Modelo Físico Oficial PostgreSQL** (`docs/33-Modelo-Fisico-PostgreSQL.md`, `DATA-005`): 14 tablas físicas con tipos conceptuales, índices y restricciones; UUID (preferentemente UUIDv7) como estrategia de identificadores, con clave de negocio preservada como `UNIQUE`. Primera misión que compromete una tecnología concreta (PostgreSQL) y asume de facto Java/Spring Boot, sin que ninguna misión `GOV-`/`DEV-` lo haya formalizado todavía (hallazgo pendiente).
- **Decisión Oficial del Stack Tecnológico** (`docs/34-Decision-Oficial-del-Stack-Tecnologico.md`, `ARCH-000`): congela Python + FastAPI + SQLAlchemy 2.x + Alembic + NumPy/Pandas/SciPy + Pydantic + pytest + Ruff/MyPy + uv + Docker + PostgreSQL. Resuelve a favor de Python la ambigüedad que `DATA-005` había dejado pendiente, dejando desactualizada (no incorrecta) la sección 9 de `docs/33` — reconciliación recomendada con prioridad alta.
- **Reconciliación Tecnológica del Modelo Santiago** (`GR-008`): elimina/reemplaza en `docs/33` §9 toda referencia heredada a Java/Spring Boot/Hibernate/JPA/Flyway/Liquibase, sincronizándola con el stack oficial de `ARCH-000`, preservando las menciones históricas como notas explícitas en lugar de borrarlas en silencio. No crea ningún documento nuevo.
- **Calibración Matemática del Modelo de Poisson** (`MODEL-007`, extiende `models/poisson.md`): orden de aplicación, restricciones matemáticas (`λ_min`/`λ_max`, condición `κ' < 1`) y ejemplo simbólico para `λ`. Excluye explícitamente Historial Directo del cálculo por contradecir `docs/03`/`docs/17`/`MR-004` ya vigentes.
- **Calibración Oficial de Parámetros del Modelo Santiago** (`models/parameter-calibration.md`, `MODEL-008`): catálogo de los 22 parámetros pendientes de los 6 motores, su origen legítimo, y reconciliación del ciclo de calibración con el pipeline ya existente de `learning/`, identificando "Optimización" como el único eslabón sin documento propio.
- **Arquitectura Oficial del Proyecto Python** (`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`, `DEV-004`): asigna los 7 componentes del Runtime, los 6 motores y las 14 tablas físicas a paquetes concretos de un futuro proyecto Python (`app/api`, `runtime`, `engine`, `preparation`, `persistence`, `models`, `schemas`, `services`, `config`), con matriz de dependencias unidireccional y mapeo de los 6 agentes documentales al código.
- **Bootstrap Oficial del Proyecto Python** (`BUILD-001`, sin documento propio en `docs/`): primera misión que crea archivos reales de código/configuración. Estructura completa de `app/` (9 subpaquetes, cada uno solo con docstring de responsabilidad), `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, Alembic inicializado sin revisiones, `tests/`, `scripts/`. README técnico creado en `app/README.md` (decisión explícita del usuario) para no sobrescribir el `README.md` raíz. Ningún componente funcional del Modelo Santiago implementado todavía.
- **Implementación del Modelo Relacional SQLAlchemy** (`BUILD-002`, sin documento propio en `docs/`): las 14 entidades ORM de `docs/33` implementadas en `app/models/` (una clase por módulo), con `UUID` técnico, claves de negocio `UNIQUE`, las 15 relaciones de `docs/32` (incluidas las dos N:M) y restricciones simples (`CHECK`/`UniqueConstraint`). Detecta, sin resolver, que el índice único parcial de `jugadores` recomendado en `docs/33` §7 no se traduce con claridad al esquema real de esa tabla. Código no ejecutado (sin Python en este entorno) — verificado solo por revisión manual.
- **Implementación de la capa Persistence** (`BUILD-003`, sin documento propio en `docs/`): Engine único (`get_engine()`), fábrica/gestor de sesiones único (`SessionLocal`/`get_session()`) y `BaseRepository` genérico (`add`/`get`/`list`/`delete`/`update`) en `app/persistence/`. Agrega `psycopg[binary]` a `pyproject.toml`, cerrando la brecha del *driver* de PostgreSQL documentada desde `BUILD-001`. Sin repositorios específicos ni migraciones todavía.
- **Implementación del PredictionContext** (`BUILD-004`, sin documento propio en `docs/`): los diez bloques de `docs/30` como modelos Pydantic en `app/runtime/prediction_context.py` (elección justificada frente a `dataclasses`). Cero métodos, cero lógica — la regla Append Only queda documentada, no implementada. `AuditBlock`/`LearningBlock` documentados explícitamente como ausentes del objeto en memoria.
- **Implementación del Runtime** (`BUILD-005`, sin documento propio en `docs/`): `PredictionRuntime` en `app/runtime/runtime.py` coordina Preparation → EngineRunner → Assembler → Persistence por inyección de dependencias (`typing.Protocol`), sin importar ninguna implementación concreta. Maneja errores y estado de ejecución sin calcular nada; el Assembler se implementó como transformación pura mínima.
- **Implementación de VariablePreparation** (`BUILD-006`, sin documento propio en `docs/`): primera pieza funcional del flujo. Construye `context.variables` con las 9 Variables Oficiales activas en V1, todas "PENDIENTE" (sin calcular). Detectó y reportó una contradicción real entre el brief ("12 variables") y la arquitectura vigente (`docs/03`/`docs/17`/`docs/30`: 9 activas, 2 diferidas) — resuelta por decisión explícita del usuario a favor de la arquitectura ya vigente.
- **Implementación del EngineRunner** (`BUILD-007`, sin documento propio en `docs/`): coordina los 6 motores por capas (`docs/06`/`docs/17`/`docs/29`) mediante 6 interfaces inyectadas (`Engine01Protocol` a `Engine06Protocol`); ningún motor real implementado. Fallo dentro de una capa no bloquea a su par independiente, pero sí bloquea la capa siguiente. Paralelismo real y condicionalidad de `Engine06` documentados, no implementados.
- **Implementación de Persistence del Runtime** (`BUILD-008`, sin documento propio en `docs/`): `RuntimePersistence` satisface `PersistenceProtocol` reutilizando `get_session`/`BaseRepository` de BUILD-003. `persist_prediction` funcional (con la brecha `id_partido`→`partido_id` documentada, no resuelta); `persist_audit`/`persist_learning` como *placeholders*. Cierra los tres colaboradores de `PredictionRuntime`.
- **Implementación del Engine01 — Fuerza Ofensiva** (`BUILD-009`, sin documento propio en `docs/`): primer motor con cálculo matemático real (`models/offensive-strength.md` §6), con pesos sin calibrar como placeholders documentados. Calcula Fuerza Ofensiva de ambos equipos y, desde `BUILD-010`, ya la publica en `PredictionContext` (`Engine01Salida` bipartita).
- **Aplicación en código de GR-009** (`BUILD-010`, sin documento propio en `docs/`): `Engine01Salida` (`app/runtime/prediction_context.py`) pasa a `local`/`visitante` (`Engine01SalidaEquipo`, `docs/30` v2.0.0 §4.4.1); `Engine01.ejecutar()` publica en lugar de bloquear — `PublicacionBloqueadaPorEsquema` eliminada. Sin cambios en la fórmula, los placeholders ni ningún otro motor.
- **Reconciliación del PredictionContext para Motores Bipartitos** (`GR-009`, actualiza `docs/30` v1.0.0 → v2.0.0): analiza los seis motores, no solo Engine01. `engine01`/`engine02` pasan a tener sus cinco campos de "Salida" por equipo (nueva sección 4.4.1); `engine03` se confirma ya correcto; `engine04`/`engine05` se confirman correctamente unipartitos (propiedades del partido/de la predicción, no de un equipo); `engine06` ya adecuado vía su diseño de lista. Exclusivamente documental — no toca código Python.
- **Implementación del Engine02 — Fuerza Defensiva** (`BUILD-011`, sin documento propio en `docs/`): segundo motor con cálculo matemático real (`models/defensive-strength.md` §6), mismo patrón exacto que `Engine01`, reutilizando sin redefinir sus mismos placeholders de `M_forma`/`Pen`. Publica de inmediato `context.engine.engine02` bipartito — detectó que `Engine02Salida` seguía sin actualizar tras `BUILD-010` y, con autorización explícita del usuario, amplió su alcance a `app/runtime/prediction_context.py` para aplicarle el mismo cambio.
- **Implementación del Engine03 — Distribución de Poisson** (`BUILD-012`, sin documento propio en `docs/`): primer motor probabilístico completo (`models/poisson.md` §6-9), calcula `λ_local`/`λ_visitante` vía SciPy, construye la matriz conjunta (truncada en 6 goles + cola `"7+"`) y publica Probabilidades L/E/V y Top 4. Lee Localía (Variable009) directamente y acepta un `MuGolProvider` inyectable para `μ_gol` — ambas contradicciones del brief original detectadas, reportadas y resueltas por autorización explícita del usuario. Sin implementación real de `MuGolProvider` todavía; Engine03 se detiene si no se inyecta uno.

## Módulos en desarrollo

- Catálogo maestro de la Base de Conocimiento de Selecciones Nacionales: faltan `torneos.csv`, `estadios.csv`, `arbitros.csv` (MS-002 quedó en pausa tras `selecciones.csv`; `competiciones.csv` se completó vía MS-006).
- Este propio sistema de seguimiento (`docs/00-Project-Tracker.md`), recién creado.

## Módulos pendientes

- Ediciones reales de torneos (`torneos.csv`) para las 10 competiciones incorporadas en MS-006 (fechas, sedes, formato) — explícitamente diferido a una misión futura desde MS-006.
- Entidades relacionales de Selecciones Nacionales: `jugadores.csv`, `convocatorias.csv`, `partidos.csv`, `lesiones.csv`, `cuotas.csv`, `estadisticas_partido.csv` (explícitamente diferidas a una misión futura desde MS-001).
- Implementación matemática (v2.0) de los 6 motores de `engine/`, respaldada por `models/`.
- Implementación matemática (v2.0) de los 5 documentos de `learning/`.
- `scripts/` existe desde `BUILD-001` (solo un `README.md` de marcador de propósito, sin ningún script real todavía). `excel/` sigue sin existir.
- Corrección editorial de las inconsistencias detectadas en `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` (referencias a archivos inexistentes, ver MS-004).

## Riesgos identificados

*Nota: los riesgos relacionados con inconsistencias de `engine/`/`docs/` listados abajo fueron consolidados, ampliados y evidenciados con precisión en `docs/18-Plan-de-Reconciliacion-Arquitectonica.md` (MR-001, inventario INC-01 a INC-11), ampliados con 8 hallazgos adicionales fuera del perímetro del Engine en `docs/19-Architecture-Freeze-Review.md` (AR-001, INC-12 a INC-19), consolidados en materia de gobernanza en `docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md` (GR-001, INC-20), y verificados/actualizados en `docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md` (AR-002, INC-21). **`INC-18` e `INC-21` (Orden de Lectura de `CLAUDE.md` desactualizado) ya quedaron resueltos por `GR-002`** — el resto sigue abierto. Estos cuatro documentos son la referencia autorizada más detallada; esta tabla mantiene solo un resumen ejecutivo.*

| Riesgo | Impacto | Mitigación propuesta |
|---|---|---|
| `data/predictions/`, `data/results/`, `data/audit/`, `data/raw/` siguen siendo solo marcadores de posición | Sin datos reales, `engine/` y `learning/` no pueden validarse empíricamente | Priorizar completar el catálogo maestro (MS-002/MS-006) antes de avanzar a implementación matemática |
| `engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` documentan internamente pasos de obtención/validación/normalización que ahora duplican la responsabilidad de `docs/15-Capa-de-Preparacion-de-Variables.md` (MS-008), y ambos comparten variables de entrada (ej. Forma Reciente) sin una fuente única | Si se implementa código directamente sobre el texto actual de los motores, se fijaría la duplicación y el riesgo de cálculos inconsistentes entre motores | Misión editorial futura que actualice `engine/01-06` para asumir como precondición la salida de la Capa de Preparación de Variables (ver "Próxima misión recomendada" de MS-008) |
| 5 de las 12 variables oficiales (Compatibilidad Táctica, Calidad de Plantilla, Localía, Historial Directo, Estado Psicológico) no tienen consumidor explícito declarado en ningún `engine/0X.md` — Compatibilidad Táctica es Nivel A en `docs/02-modelo.md` pese a ello, y Estado Psicológico no tiene nivel asignado (MS-009, confirmado independientemente en MS-010) | Riesgo de que variables consideradas importantes en `docs/02-modelo.md`/`docs/03-Variables.md` nunca se implementen realmente en ningún motor, o se implementen sin criterio explícito de cuál motor las usa | Misión editorial de `engine/` (ver MS-008/MS-009/MS-010) que asigne consumidor explícito a cada una, y revisión de `docs/02-modelo.md` para clasificar a Estado Psicológico |
| `engine/06-Expected-Value.md` consume `cuotas.csv` directamente de la Base de Conocimiento, sin pasar por la Capa de Preparación de Variables ni por el Contrato Oficial de Variables (MS-010) | Contradice el principio de desacoplamiento central de MS-008; si se implementa código sobre el texto actual, el Engine quedaría acoplado a la Base de Conocimiento en al menos un punto | Misión futura que decida si las cuotas se modelan como una entrada oficial paralela a las 12 Variables o se hacen pasar por la Capa de Preparación de Variables como cualquier otro dato |
| "Grandes oportunidades" (uno de los 5 "Datos necesarios" de Variable003 en `docs/03-Variables.md`) no existe como campo en ningún CSV de `data/processed/selecciones-nacionales/`; "conversión" requiere cálculo derivado (`MODEL-001`) | La fórmula de Fuerza Ofensiva solo puede construirse con 3 de sus 5 componentes declarados hasta que se amplíe el esquema | Evaluar en una futura misión de datos si se agrega el campo a `estadisticas_partido.csv`, o si se acepta el índice con 3 componentes de forma permanente |
| "Clima" (Variable012, ya activa vía `engine/04`) no tiene ningún campo en ningún CSV; no existe tabla de alineación titular por partido, lo que bloquea "Rotaciones" de Variable006 (la variable más compartida de las 12) (`DATA-001`) | Una variable en uso hoy tiene un componente sin fuente de datos; "Rotaciones" afecta a los 4 motores que consumen Variable006 | Misión de captura de datos priorizada por `DATA-001`: primero "Grandes oportunidades" (más barato), luego tabla de alineación por partido |
| El Engine (v2.0) no tiene todavía respaldo matemático completo en `models/` para Chaos Index ni Confidence | Riesgo de implementar fórmulas sin investigación previa, violando `CLAUDE.md` ("Investigación antes de implementación") | No iniciar la v2.0 de esos motores sin el documento de `models/` correspondiente |
| Inconsistencias editoriales ya detectadas en `engine/04-Chaos-Index.md` y `engine/05-Confidence.md` (numeración interna y referencias a archivos inexistentes) | Puede inducir errores si se usan como referencia sin revisar | Programar una misión editorial dedicada antes de tocar esos motores |
| Alta dependencia de coordinación manual entre misiones (numeración de `docs/`, referencias cruzadas) | Cada nueva misión que inserta un documento numerado obliga a renumerar y actualizar referencias en varios archivos | Preferir, cuando sea posible, agregar documentos al final de la secuencia en lugar de insertarlos; este tracker debe usarse para detectar el conflicto antes de crear el archivo |
| `docs/33-Modelo-Fisico-PostgreSQL.md` §9 ("Compatibilidad") asume Java/Spring Data JPA/Hibernate/Flyway/Liquibase, contradicho por la decisión oficial de `ARCH-000` (Python/SQLAlchemy/Alembic) | Un lector de `docs/33` sin contexto de `ARCH-000` podría asumir un stack Java ya inexistente; riesgo bajo sobre el modelo físico en sí (agnóstico de ORM), alto sobre esa sección puntual | Misión de reconciliación editorial dedicada a la sección 9 de `docs/33`, recomendada con prioridad alta por `ARCH-000` |
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

- **Estado:** En progreso (fase de análisis e implementación de INC-04/INC-05 completadas; INC-06 pendiente)
- **Dependencias:** MR-002 (Completada), MR-003 (Completada)
- **Objetivo (definido en MR-001):** Declarar consumidor explícito de Variable005/008/009/010/011 o justificar su no uso; decidir el tratamiento de `cuotas.csv` en `engine/06`; centralizar la señal "Rotaciones" en la Capa de Preparación de Variables.
- **Fase de análisis (2026-07-17):** Se crea `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md`. Verificado directamente contra los CSV reales: 3 de las 5 variables huérfanas tienen datos completos hoy (Localía, Historial Directo, Calidad de Plantilla parcial); 2 (Compatibilidad Táctica —Nivel A—, Estado Psicológico) carecen de fuente de datos real en el esquema actual.
- **Fase de implementación (2026-07-17, esta misión, solicitada como "MR-005" — identificador ya reservado con otro objetivo, ejecutada como continuación de MR-004):** Aplicadas las recomendaciones de `docs/24`. `INC-04` **resuelto**: Localía → `engine/03-Poisson.md`; Historial Directo → `engine/05-Confidence.md`; Calidad de Plantilla → `engine/01`/`02` (alcance reducido); Compatibilidad Táctica y Estado Psicológico clasificadas consistentemente como "Pendiente de futura investigación" (no "Diferida a V2" — la categoría correcta, porque el bloqueo es de datos, no de prioridad) en `docs/03`, `docs/16` y `docs/17`. `INC-05` **resuelto en principio, no en implementación completa**: se formaliza que las cuotas nunca serán una 13ª Variable Oficial, sino una categoría de Datos de Mercado paralela preparada por `docs/15` — sin diseñar el contrato completo (fuera de alcance); `engine/06` sigue leyendo `cuotas.csv` directamente, ahora con la excepción anotada explícitamente. `INC-06` (Rotaciones) sigue sin resolver — explícitamente fuera del alcance de este brief.
- **Próxima misión recomendada:** Resolver `INC-06` (centralizar "Rotaciones" en la Capa); diseñar el Contrato de Datos de Mercado completo para implementar `INC-05` de forma total; una misión `MS-` de diseño de datos para capturar formación táctica y clasificación/tabla de posiciones, condición previa para reconsiderar Compatibilidad Táctica y Estado Psicológico.

## MR-005 — Reconciliación de `docs/02-modelo.md` con la utilización real de variables

- **Estado:** Pendiente
- **Dependencias:** MR-004
- **Objetivo (definido en MR-001):** Clasificar a Variable011 en un Nivel A-D; revisar el Nivel B de Variable006; agregar nota cruzada de equivalencia terminológica xG/xGA ↔ Potencial Ofensivo/Solidez Defensiva.
- **Nota:** un brief posterior, también nombrado "MR-005", pedía implementar las recomendaciones de `docs/24` (INC-04/INC-05) — se ejecutó como fase de implementación de `MR-004` (ver esa entrada), no aquí, para no reservar dos objetivos bajo el mismo identificador. Este `MR-005` (reconciliación de `docs/02-modelo.md`) sigue vigente sin cambios, y ahora depende de un `MR-004` más completo de lo que tenía cuando se definió originalmente.

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

## GR-008 — Reconciliación Tecnológica del Modelo Santiago

- **Estado:** **Completada**
- **% Avance:** 100%
- **Dependencias:** `docs/33` (DATA-005), `docs/34` (ARCH-000) — ambas Completadas; reconcilia el texto de la primera con la decisión oficial de la segunda
- **Prioridad:** Alta (declarada así por la propia `ARCH-000`)
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Objetivo:** Eliminar toda referencia documental al stack Java (Spring Boot, Spring Data JPA, Hibernate, Flyway/Liquibase) que contradijera la decisión oficial de `ARCH-000` (Python + FastAPI + SQLAlchemy 2.x + Alembic + PostgreSQL), sin modificar ninguna decisión arquitectónica, el Runtime, el Engine, las Variables Oficiales, el `PredictionContext` ni la Base de Conocimiento. **No crea ningún documento nuevo** — misión exclusivamente de reconciliación editorial, mismo patrón que `GR-002`/`MR-002`/`MR-003`.
- **Detección (inventario completo, verificado con `grep` en todo el repositorio, no de memoria):** únicas referencias reales a Java/Spring Boot/Spring Data/Hibernate/JPA/Flyway/Liquibase encontradas en `docs/33-Modelo-Fisico-PostgreSQL.md` (9 puntos: "Nota de verificación previa", fila "Versionado de fila" de la sección 2, la sección 9 completa —4 filas—, "Restricciones", una pregunta de "Validaciones obligatorias", las preguntas 8 y 10 del "Cierre obligatorio", y el hallazgo 1 de "Observaciones"). `docs/34-Decision-Oficial-del-Stack-Tecnologico.md` revisado y ya consistente consigo mismo (menciona Java solo para descartarlo explícitamente, no requiere cambio). `README.md` y `CLAUDE.md` revisados: cero referencias a ningún stack tecnológico (nunca lo tuvieron). `docs/16`, `docs/31`, `docs/32` revisados: mencionan JPA/Hibernate/Java únicamente como ejemplos genéricos dentro de restricciones tipo "no se genera código/JPA/Hibernate" o como ejemplo neutral de "cualquier lenguaje" — no asumen ni contradicen el stack oficial, y además `docs/31`/`docs/32` están explícitamente protegidos de modificación por el alcance de esta misión ("No modificar... Base de Conocimiento") — no se tocaron.
- **Clasificación y reconciliación aplicada (únicamente en `docs/33`, v1.0.0 → v1.1.0):** se agregó una "Nota de reconciliación (GR-008)" explícita al inicio del documento; se preservó la "Nota de verificación previa" original como nota histórica (no se eliminó); se reescribió la sección 9 ("Compatibilidad") reemplazando Flyway/Liquibase/Spring Data JPA/Hibernate por Alembic/SQLAlchemy 2.x, conservando al final una "Nota histórica" explícita con la recomendación original y su resolución; se actualizaron "Restricciones", la pregunta de compatibilidad de "Validaciones obligatorias", las preguntas 8 y 10 de "Cierre obligatorio" (conservando la pregunta original entre paréntesis donde aplicaba) y el hallazgo 1 de "Observaciones" (marcado explícitamente "Resuelto"), y una mención residual a "Flyway" en la Autocrítica. Ninguna referencia se eliminó en silencio — toda mención heredada quedó marcada como nota histórica, nunca borrada sin rastro (Constitución, Art. 8).
- **Confirmación de las validaciones obligatorias:** el repositorio completo referencia ahora un único stack tecnológico (Python/FastAPI/SQLAlchemy/Alembic/PostgreSQL/Docker, `docs/34`); no quedan contradicciones activas con `ARCH-000`; ningún documento continúa asumiendo Java como tecnología oficial (las únicas menciones restantes son notas históricas explícitamente marcadas como tales); la arquitectura (modelo físico de 14 tablas, Runtime, `PredictionContext`, Engine, Variables Oficiales) permanece exactamente idéntica — no se modificó ningún tipo, clave, índice, relación ni regla de negocio de `docs/33`.
- **Próxima misión recomendada:** La primera fórmula matemática real en `models/poisson.md` — con el stack tecnológico ya congelado y reconciliado en todo el repositorio, es el único bloqueante que sigue impidiendo declarar cerrada la fase de diseño e iniciar la fase de construcción real (ver Cierre de esta misión, preguntas 9 y 10).

## GR-009 — Reconciliación del PredictionContext para Motores Bipartitos

- **Estado:** Completada
- **% Avance:** 100% de lo que esta misión podía entregar (exclusivamente documental — actualización de `docs/30`)
- **Dependencias:** `BUILD-004` (`PredictionContext` original), `BUILD-009` (origen del hallazgo), `docs/17`, `models/offensive-strength.md`, `models/defensive-strength.md`, `models/poisson.md`, `models/confidence.md`, `models/chaos-index.md`, `models/expected-value.md` (todas Completadas/vigentes) — reconciliación puramente documental, sin dependencias de código
- **Prioridad:** Alta — recomendada explícitamente por `BUILD-009` como bloqueante para `engine/03-Poisson.md`
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Objetivo:** Revisar si `docs/30-Contrato-Oficial-del-Prediction-Context.md` representa correctamente la naturaleza bipartita de un partido (equipo local vs. visitante) en las seis subsecciones de `engine`, sin asumir que el problema detectado en `BUILD-009` se limitaba a `engine01`. Exclusivamente documental: no modifica código Python, Runtime, Engine, Variables Oficiales ni fórmulas matemáticas.
- **Observaciones:** `docs/30` sube de versión 1.0.0 a **2.0.0** (cambio MAYOR, según su propia regla de versionado semántico: "cambiar la forma de un bloque existente es MAJOR si elimina o redefine un campo ya consumido"). Análisis motor por motor (nueva sección 9 del documento): **`engine01`/`engine02` SÍ requerían el cambio** — sus cinco campos de "Salida" (Fuerza Ofensiva/Defensiva, Nivel de confianza del cálculo, Variables utilizadas, Variables descartadas, Calidad de los datos) pasan a duplicarse por equipo (nueva sección 4.4.1), con evidencia de `docs/30` §4.3 (variables de entrada ya por equipo), `models/poisson.md` §6 (`FO_local`/`FO_visitante` distintos) y, hallazgo adicional no limitado a Poisson, `models/confidence.md` §6 (`C_diferencia` también consume ambos valores directamente). **`engine03` ya era correcto** desde `BUILD-004` (bipartito en goles esperados/distribución de goles, unipartito en probabilidad de resultado y marcadores conjuntos, correctamente por naturaleza matemática). **`engine04` (Caos) y `engine05` (Confianza) permanecen unipartitos** — ambos son, por su propio fundamento en `models/chaos-index.md`/`confidence.md`, propiedades del partido/de la predicción completa, no de un equipo aislado. **`engine06` (Valor Esperado) ya adecuado** vía su diseño de lista existente ("uno por mercado evaluado", ya cubre selecciones como "Victoria Local"/"Victoria Visitante" como entradas distintas). No se detectaron contradicciones nuevas de la misma naturaleza; se confirma, sin resolver por exceder el alcance, la duplicidad ya conocida de cálculo de Variable001/006/007 entre `engine04`/`engine05` (`models/chaos-index.md` §10). Incluye "Cierre obligatorio — GR-009" y "Autocrítica — GR-009" como secciones propias del documento, sin editar las originales de `DEV-003`. **Deja explícitamente pendiente** (fuera del alcance de esta misión, "No modificar código Python"): actualizar `app/runtime/prediction_context.py` (`Engine01Salida`/`Engine02Salida`) conforme a la nueva sección 4.4.1, y ajustar `app/engine/engine01.py` (BUILD-009) para publicar en `PredictionContext` en lugar de lanzar `PublicacionBloqueadaPorEsquema`.
- **Próxima misión recomendada:** Una misión `BUILD-` que actualice `app/runtime/prediction_context.py` conforme a la sección 4.4.1 ya reconciliada, y ajuste `app/engine/engine01.py` para publicar su resultado en lugar de bloquear la ejecución — desbloqueando, de paso, la futura implementación de `app/engine/engine02.py` y `engine/03-Poisson.md`.

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

# Registro de implementación conceptual (IMP-)

Serie independiente de `MS-`/`MR-`/`AR-`/`GR-`/`GOV-`, iniciada en IMP-001. Una misión `IMP-` no diseña arquitectura nueva ni reconcilia inconsistencias — sintetiza documentos ya estables en un trazado operativo de extremo a extremo, como paso previo a que exista implementación de código real.

## IMP-001 — Diseño del Prediction Pipeline del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/06`, `docs/14`, `docs/15`, `docs/16`, `docs/17` (todas Completadas) — sintetiza sin redefinir
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`. El brief referenciaba una ruta obsoleta (`docs/05-Flujo-Operacional.md`); se usó la ruta correcta (`docs/06`). Dado el fuerte solapamiento con `docs/06`/`docs/14`, se diseñó como síntesis (referencia, no repite) y se concentró el aporte original en: el objeto de entrada exacto (nunca antes definido), una traza numérica de ejemplo (reutiliza el ejemplo España-Francia de `docs/08-predicciones.md`), y el objeto de respuesta completo. Documenta explícitamente que `jugadores_destacados` y `mercados_detectados` (pedidos por el brief como ejemplo) **exceden lo que el Engine V1 puede producir hoy** — ningún motor opera a nivel de jugador, `engine/06` no escanea mercados proactivamente — y los deja como brecha explícita en vez de inventarles un origen. Confirma las 4 validaciones obligatorias sin excepción no documentada.
- **Próxima misión recomendada:** Primera investigación matemática real en `models/` (empezando por `models/poisson.md`); en paralelo, `INC-06` (Rotaciones) y el Contrato de Datos de Mercado (`MR-004`).

---

# Registro de mapas de navegación (MAP-)

Serie independiente de `MS-`/`MR-`/`AR-`/`GR-`/`GOV-`/`IMP-`, iniciada en MAP-001. Una misión `MAP-` no diseña, reconcilia, audita ni implementa — produce una vista de alto nivel para orientar a un lector nuevo, sin redefinir nada de lo que resume.

## MAP-001 — Mapa Maestro de la Arquitectura del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** Todo el repositorio (resume, no redefine)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/99-Mapa-Maestro.md` (ruta exacta pedida por el brief, fuera de la secuencia 00-25 a propósito). Solicitada como "GOV-001" (ya usado por la Constitución); registrada como `MAP-001`. Categoriza los 26 documentos de `docs/` sin repetir el listado archivo-por-archivo de `README.md`; el estado del componente "Estado Actual" se basa exclusivamente en este mismo Project Tracker, sin porcentajes nuevos. No modifica ningún documento existente.
- **Próxima misión recomendada:** La misma que recomienda `IMP-001` — primera investigación matemática real en `models/`.

---

# Registro de diseño de ejecución (DEV-)

Serie independiente de `MS-`/`MR-`/`AR-`/`GR-`/`GOV-`/`IMP-`/`MAP-`, iniciada en DEV-001. Una misión `DEV-` especifica **cómo** se ejecutará el sistema (Runtime, independiente del lenguaje) — distinta de `IMP-`, que sintetiza trazados operativos de la arquitectura ya existente sin formalizar un modelo de ejecución nuevo.

## DEV-001 — Runtime Oficial del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/06`, `docs/14`, `docs/15`, `docs/16`, `docs/17`, `docs/25`, `docs/99` (todas Completadas) — sintetiza sin redefinir
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/26-Runtime-del-Modelo.md`, sin colisión de numeración. Corrige, antes de escribir, una discrepancia entre el diagrama de ejemplo del brief (Engine lineal `01→02→03→04→05→06`) y la arquitectura por capas ya verificada en `docs/06`/`docs/17`/`docs/25` (Capa 1: `01`+`02` en paralelo; Capa 3: `04`+`05` en paralelo) — se usa el orden por capas para no contradecir esos tres documentos, cumpliendo la validación 5 exigida por el propio brief. Formaliza, por primera vez, el **Objeto de Contexto** (estructura de solo-anexado que viaja durante toda la ejecución) y el **registro de ejecución (logs)** — ambos aportes genuinamente nuevos, el resto del documento referencia sin duplicar. Confirma en el cierre que la arquitectura de ejecución está lista pero la V0.1 real no, por ausencia de fórmulas matemáticas reales en `models/`.
- **Próxima misión recomendada:** Primera investigación matemática real en `models/poisson.md` — bloqueante compartido con `IMP-001` y `MAP-001`.

## DEV-002 — Arquitectura de Implementación del Runtime

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/06`, `docs/14`, `docs/15`, `docs/17`, `docs/25`, `docs/26`, `docs/99` (todas Completadas) — descompone el Runtime de `docs/26` en componentes, sin redefinirlo
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/29-Arquitectura-del-Runtime.md`, un nivel de diseño más cerca de la implementación que `docs/26-Runtime-del-Modelo.md` (DEV-001). Nombra y delimita siete componentes (`PredictionRequest`, `PredictionContext`, `VariablePreparation`, `EngineRunner`, `PredictionAssembler`, `PredictionReport`, `Persistence`); `EngineRunner` y `PredictionAssembler` son los únicos genuinamente nuevos (antes eran pasos anónimos del Runtime en `docs/26`). Formaliza, por primera vez, la frontera exacta de escritura por sección del Objeto de Contexto (renombrado aquí `PredictionContext`, mismo objeto, misma regla append-only) y una categorización de "Estados de ejecución" (Completa / Completa sin Valor Esperado / Detenida antes o durante el Engine) que ningún documento anterior definía explícitamente. Corrige, antes de escribir, la misma discrepancia orden lineal vs. por capas ya corregida en `docs/26`. Resuelve una ambigüedad propia del brief (si `PredictionRequest` debía persistirse de forma independiente): decide que no, por el Principio de Justificación de Datos — ya queda trazable vía el log de ejecución y el campo `partido` del `PredictionReport`, documentando la decisión y su interpretación alternativa en la Autocrítica. Incluye por primera vez, dentro de la serie `DEV-`, la sección de Autocrítica exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md` (sección 8) — `DEV-001` no la había incluido. No modifica el Engine, variables, algoritmos, pesos, `models/`, el Pipeline ni el Runtime ya definido en `docs/26`; no resuelve `INC-05`, heredado como excepción documentada.
- **Próxima misión recomendada:** La misma ya recomendada por `docs/26`/`docs/25`/`docs/99`: la primera investigación matemática real en `models/poisson.md` sigue siendo el bloqueante compartido para que esta arquitectura, ya completa a nivel de componentes, empiece a producir un cálculo real. En paralelo, sigue pendiente el Contrato de Datos de Mercado (cierra `INC-05` también para `EngineRunner`).

## DEV-003 — Contrato Oficial del Prediction Context

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/06`, `docs/15`, `docs/16`, `docs/17`, `docs/25`, `docs/26`, `docs/29`, `engine/01-06`, `learning/README.md` (todas Completadas) — detalla la estructura interna del `PredictionContext` ya nombrado por `DEV-002`, sin redefinir ninguna
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/30-Contrato-Oficial-del-Prediction-Context.md`. Corrige, antes de escribir, una ruta inexistente del brief (`docs/26-Arquitectura-de-Ejecucion.md`; el documento real es `docs/26-Runtime-del-Modelo.md`) e incorpora `docs/29-Arquitectura-del-Runtime.md` (DEV-002, no mencionado por el brief) como antecedente de lectura obligatoria. Define diez bloques del `PredictionContext` (`metadata`, `match`, `variables`, `engine` con una subsección verbatim por motor, `prediction`, `market`, `bankroll`, `errors`, `audit`, `learning`) sin inventar ningún campo — todos trazables a `engine/01-06` ("Salida"), `docs/16`, `docs/25` §6 o `docs/09`. Aporta una aclaración de diseño nueva: el objeto en memoria vive solo durante una ejecución (se descarta tras la Persistencia, mismo principio de `docs/16` §7); `audit`/`learning` se agregan después, cross-referenciados por `id_prediccion`, al registro ya persistido — nunca reabriendo el objeto original. Reserva el bloque `market` como posición estable para el futuro Contrato de Datos de Mercado sin diseñarlo; `INC-05` sigue sin resolverse y el Architecture Freeze permanece en 4 de 7 criterios (`docs/23`). Incluye Autocrítica (`docs/22`, sección 8). No modifica el Engine, variables, algoritmos, pesos, `models/`, el Pipeline ni el Runtime ya definido.
- **Próxima misión recomendada:** La misma ya recomendada por toda la serie `DEV-`: la primera fórmula matemática real con Versión 2.0 en `models/poisson.md` — es lo único que permitiría que el bloque `engine03` de este contrato contenga un número calculado en lugar de un marcador conceptual. En paralelo, sigue pendiente el Contrato de Datos de Mercado (cierra `INC-05`, bloque `market`).

## DEV-004 — Arquitectura Oficial del Proyecto Python del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/26`, `docs/29`, `docs/30`, `docs/31`, `docs/32`, `docs/33`, `docs/34` (todas Completadas) — asigna cada pieza ya diseñada a un paquete concreto, sin redefinir ninguna
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`, última pieza puramente arquitectónica antes de la implementación real. Asigna los 7 componentes del Runtime, los 6 motores del Engine, las 14 tablas físicas y las tecnologías del stack a paquetes concretos (`app/api`, `runtime`, `engine`, `preparation`, `persistence`, `models`, `schemas`, `services`, `config`, más `tests/`, `migrations/`, `scripts/`), coexistiendo con la estructura documental ya existente sin reemplazarla. Define una matriz de dependencias estrictamente unidireccional y reglas arquitectónicas explícitas (Engine nunca conoce FastAPI/SQLAlchemy; `PredictionContext` sigue siendo el único objeto compartido). Aporta un mapeo completo de los 6 agentes documentales a su equivalente en código, no pedido explícitamente por el brief. Aclara una colisión de nomenclatura real entre `app/engine`/`app/models` (código) y los directorios raíz `engine/`/`models/` (documentación), que coexisten sin renombrarse. Incluye Autocrítica (`docs/22`, sección 8), declarando como supuesto no verificado que el proyecto Python vive en este mismo repositorio. No escribe código, no crea carpetas reales, no modifica el Engine, Variables Oficiales, fórmulas, Runtime ni `PredictionContext`.
- **Próxima misión recomendada:** La misma prioridad ya heredada de `MODEL-007`/`MODEL-008`: una misión de captura de datos reales (`docs/27`), condición para que `app/engine` tenga algo calibrado que ejecutar. En el eje de arquitectura, esta misión cierra la cadena — no queda ninguna pieza puramente conceptual pendiente de diseño.

---

# Registro de investigación matemática (MODEL-)

Serie independiente de `MS-`/`MR-`/`AR-`/`GR-`/`GOV-`/`IMP-`/`MAP-`/`DEV-`, iniciada en MODEL-001. Una misión `MODEL-` desarrolla el contenido real de `models/` — la investigación estadística que `CLAUDE.md` exige antes de que cualquier motor de `engine/` pueda implementar una fórmula ("Investigación antes de implementación").

## MODEL-001 — Modelo Matemático de Fuerza Ofensiva

- **Estado:** Completada
- **% Avance:** 100% (estructura de la fórmula; calibración de pesos queda para una misión futura con datos reales)
- **Dependencias:** `engine/01`, `docs/03`, `docs/16`, `docs/17`, `docs/02-modelo.md` (todas Completadas)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** `models/offensive-strength.md` evoluciona de stub a especificación matemática completa — primer documento de `models/` en hacerlo. Propone `Fuerza Ofensiva = clip(P · M_forma · (1 − Pen), 0, 100)`, con las 6 Variables Oficiales ya asignadas a `engine/01` por `docs/17`, sin pesos numéricos (solo rol estructural, conforme a "Nunca alterar pesos sin evidencia estadística"). Detecta, verificando directamente el esquema real, que "grandes oportunidades" (uno de los 5 datos declarados para Variable003 en `docs/03`) no existe en ningún CSV del módulo, y que "conversión" requiere un cálculo derivado — documentado como limitación, no oculto ni resuelto. Fundamentada en Maher (1982) y Dixon-Coles (1997), con diferencia metodológica explicitada honestamente. No modifica `engine/01`, el Runtime, el Pipeline, las Variables Oficiales ni `learning/`.
- **Próxima misión recomendada:** `models/poisson.md` (siguiente en la cadena de dependencias — `engine/03` consume directamente la salida de este modelo).

---

# Registro de auditoría de datos (DATA-)

Serie independiente de las demás, iniciada en DATA-001. Una misión `DATA-` cruza la especificación de variables/motores contra el esquema real de la Base de Conocimiento — audita, no diseña ni implementa.

## DATA-001 — Auditoría Completa de Variables Pendientes

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/03`, `docs/16`, `docs/17`, `MODEL-001` (todas Completadas) — la origina el hallazgo de "Grandes oportunidades" en `MODEL-001`
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/27-Auditoria-de-Variables-Pendientes.md`. Verifica los 11 CSV reales y confirma que `data/raw/` no tiene datos. Clasifica ~46 datos necesarios en A-E; 8 en categoría D (deben capturarse), 2 en B, 13 en C (ya derivables sin tocar la Base de Conocimiento). Dos hallazgos nuevos: "Posesión" (Variable005) sí existe, contra lo asumido; "Clima" (Variable012, variable ya activa) no existe en ningún CSV. Detecta que no existe tabla de alineación titular por partido (bloquea "Rotaciones", la variable más compartida) y que `estado_convocatoria` nunca formalizó su ENUM. Clasifica "Presión competitiva" como E, justificado. No modifica nada — solo audita.
- **Próxima misión recomendada:** Misión de diseño de datos (`MS-` o `DATA-002`) que capture, en orden de prioridad: "Grandes oportunidades" (más barato), una tabla de alineación por partido (resuelve Rotaciones y sienta base para Minutos jugados), y una evaluación de viabilidad real de Compatibilidad Táctica completa.

## DATA-002 — Catálogo Oficial de Variables Derivadas

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** DATA-001, MODEL-001, `docs/15`, `docs/16`, `docs/17`, `docs/26` (todas Completadas) — las centraliza sin redefinirlas
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Se crea `docs/28-Catalogo-de-Variables-Derivadas.md` (el brief pedía `docs/27`, ya ocupado por `DATA-001` — colisión de archivo, no solo de identificador de misión). Cataloga 27 cantidades calculadas en 6 categorías. Aclara una colisión de terminología real entre "Variable Contextual" (este catálogo, por procedencia del dato) y "Variables Contextuales" (`engine/01`/`02`, por rol dentro de su propia fórmula). Verifica que "Índice disciplinario" e "Índice de lesiones" (ejemplos del propio brief) no existían en ningún documento previo — se catalogan como tal, sin fingir que ya estaban definidos. Solo 2 de 27 entradas en estado "Diseñada" completo; 6 "Parcial"; 19 "Pendiente" — panorama más preciso que la impresión previa de "Engine mayormente listo". No modifica nada de lo que cataloga.
- **Próxima misión recomendada:** `MODEL-002` (`models/defensive-strength.md`, siguiente motor en la cadena, con xGA ya definido como sub-componente listo); o una misión que decida si "Índice disciplinario"/"Índice de lesiones" valen la pena diseñarse, dado que no tenían precedente.

## DATA-003 — Modelo Físico Oficial de la Base de Conocimiento del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/05`, `docs/06`, `docs/14`, `docs/15`, `docs/16`, `docs/25`, `docs/26`, `docs/27`, `docs/28`, `docs/29`, `docs/30`, `docs/99` (todas Completadas) — sitúa un mapa conceptual de dominios entre el flujo genérico de `docs/05` y el esquema campo-por-campo ya existente, sin redefinir ninguno
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md`. Define 13 dominios de información (extiende deliberadamente los ~11 de ejemplo del brief, separando Lesiones e Infraestructura/Oficiales por responsabilidad única, `CLAUDE.md`), sus relaciones puramente conceptuales (sin SQL/ERD/claves) y fija, por primera vez, la frontera exacta entre la Base de Conocimiento (permanente) y el `PredictionContext` (transitorio, `docs/30`): este último nunca se persiste como objeto completo, solo su proyección curada (`PredictionReport`) ingresa al dominio Predicciones. Resuelve una aparente duplicación conceptual (`data/results/` crudo vs. `partidos.csv` validado) mostrando que es el mismo patrón raw/processed ya aplicado al resto del sistema, no una redundancia. Detecta y documenta, sin corregir, una inconsistencia editorial no catalogada antes: el encabezado interno de `docs/05-Base-de-Conocimiento.md` todavía dice "Arquitectura de Datos" / `docs/04-Arquitectura-de-Datos.md`, residuo de una renumeración anterior. Deja abierta la pregunta de si el dominio Aprendizaje necesita persistencia propia en `data/` (hoy no tiene directorio). Incluye Autocrítica (`docs/22`, sección 8). No diseña tablas, SQL, claves ni código; no modifica Variables Oficiales, motores, fórmulas ni el Runtime.
- **Próxima misión recomendada:** En el eje de datos, una misión de captura que resuelva los elementos de categoría D ya priorizados por `docs/27` (empezando por "Grandes oportunidades"). En el eje de arquitectura, la primera fórmula matemática real en `models/poisson.md`, bloqueante compartido de toda la serie `DEV-`/`MODEL-`.

## DATA-004 — Modelo Relacional Oficial del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/15`, `docs/16`, `docs/26`, `docs/29`, `docs/30`, `docs/31`, `docs/99` (todas Completadas) — desciende de dominio a entidad individual sin redefinir ninguna
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/32-Modelo-Relacional-Oficial.md`. Descompone los 13 dominios de `docs/31` en 15 entidades conceptuales (extiende el ejemplo del brief separando Estadio/Árbitro y Competición/Torneo, por responsabilidad única). Define relaciones y cardinalidades puramente conceptuales, confirmando exactamente **dos** relaciones N:M en todo el modelo (Convocatoria: Equipo×Jugador×Torneo; Estadística de Partido: Partido×Equipo), ambas resueltas por entidades asociativas ya existentes. Define claves conceptuales (identidad, natural, técnica ya asignada) sin tipos de dato ni mecanismo de generación física. Confirma que el grafo de dependencias es acíclico y que soporta el orden de lectura ya fijado en `docs/14`. Mantiene abierta, sin resolver, la misma pregunta de `docs/31` sobre la persistencia de Propuesta de Aprendizaje. Incluye Autocrítica (`docs/22`, sección 8). No genera SQL, claves físicas, tipos de dato ni código; no modifica Variables Oficiales, motores, Runtime, `PredictionContext` ni modelos matemáticos.
- **Próxima misión recomendada:** Dos caminos no excluyentes: (a) una misión de diseño físico que traduzca este modelo a un esquema real para un motor relacional concreto (primera decisión de stack de este eje); (b) continuar capturando los datos de categoría D más críticos (`docs/27`) antes de fijar un esquema físico sobre columnas todavía sin dato real.

## DATA-005 — Modelo Físico Oficial PostgreSQL del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `docs/16`, `docs/30`, `docs/31`, `docs/32`, `docs/99` (todas Completadas) — traduce el modelo relacional conceptual a decisiones físicas de PostgreSQL sin redefinirlo
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/33-Modelo-Fisico-PostgreSQL.md`. Primera misión del proyecto que compromete una tecnología de almacenamiento concreta (PostgreSQL) y asume implícitamente Java/Spring Boot (Flyway/Liquibase/Spring Data JPA/Hibernate en su sección de compatibilidad) — anotado explícitamente como hallazgo pendiente de formalizar (ver Observaciones del documento), no como una decisión ya oficializada por una misión `GOV-`/`DEV-` dedicada. Traduce las 15 entidades de `docs/32` a 14 tablas físicas (Propuesta de Aprendizaje queda sin persistencia confirmada, misma nota abierta desde `docs/31`), con convenciones completas (nombres, timestamps diferenciados por mutabilidad, `TEXT`+`CHECK` en vez de `ENUM` nativo), tipos conceptuales por columna, e índices/restricciones justificados. Decide **UUID (preferentemente UUIDv7)** como estrategia de identificadores frente a `BIGSERIAL`/ULID, con análisis explícito de rendimiento/escalabilidad/trazabilidad/sincronización, preservando los códigos de negocio ya existentes como columnas `UNIQUE`. Aclara, como hallazgo nuevo, que `auditorias` (por partido) y las métricas de cartera de `docs/09` (ROI/Yield/Drawdown, agregadas en el tiempo) son conceptos distintos que ningún documento anterior había separado explícitamente. Incluye Autocrítica (`docs/22`, sección 8). No genera SQL, JPA, código ni migraciones; no modifica Variables Oficiales, Runtime, `PredictionContext`, motores ni modelos matemáticos.
- **Próxima misión recomendada:** Formalizar, en una misión `GOV-`/`DEV-` dedicada, la elección de stack (Java + Spring Boot + PostgreSQL) que esta misión ya asume de facto. En paralelo, sigue vigente capturar los datos de categoría D más críticos (`docs/27`) antes de que una futura migración física los deje sin contenido real.

## MODEL-002 — Modelo Matemático de Defensive Strength

- **Estado:** Completada
- **% Avance:** 100% (estructura; calibración pendiente, igual que `MODEL-001`)
- **Dependencias:** MODEL-001, `engine/02`, `docs/03`, `docs/17`, `docs/28` (todas Completadas)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Brief pedía `models/02-defensive-strength.md`, ruta que no existe (`models/` no usa prefijos numéricos) — se evolucionó `models/defensive-strength.md`, el archivo real. Propone `Fuerza Defensiva = clip(P_def · M_forma · (1 − Pen), 0, 100)`, **reutilizando explícitamente** `M_forma`/`Pen` de `MODEL-001` en lugar de redefinirlos, para no duplicar el cálculo de variables ya compartidas (Var001/002/006/007/008) entre `engine/01` y `engine/02` — riesgo ya señalado genéricamente en `docs/15`/`docs/17`, evitado aquí por diseño. Detecta una discrepancia real entre `engine/02` ("Grandes Oportunidades Concedidas") y el contrato oficial de Variable004 en `docs/03` (no la incluye) — documentada, no corregida. A diferencia de `MODEL-001`, el término base de esta fórmula (Variable004) **no tiene ningún componente bloqueado** — los 4 son derivables hoy (`docs/27`). Ningún peso numérico fijado.
- **Próxima misión recomendada:** `models/poisson.md` — con dos de los tres motores base completos, es el siguiente eslabón real de la cadena de cálculo.

## MODEL-003 — Modelo Matemático de Poisson

- **Estado:** Completada
- **% Avance:** 100% (estructura; calibración de `μ_gol`/`κ`/`κ'` pendiente)
- **Dependencias:** MODEL-001, MODEL-002, `engine/03`, `docs/17`, `docs/28` (todas Completadas)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Desarrolla el núcleo probabilístico: `λ` como combinación multiplicativa cruzada (ataque propio × defensa rival, nunca la propia) más ajuste de Localía — estructura de Maher (1982). Documenta explícitamente que la corrección de Dixon-Coles (1997) para marcadores bajos no se adopta en V1 por falta de historial para estimar `ρ`. Define por primera vez el mecanismo exacto detrás de "Probabilidad Local/Empate/Visitante" y "Top 4 de marcadores", que `docs/06`/`14`/`25`/`26` exigían sin definir cómo se calculaban: se derivan de una única matriz de probabilidades conjuntas. Ningún parámetro numérico fijado.
- **Próxima misión recomendada:** `models/chaos-index.md` o `models/confidence.md` — ambos pueden desarrollarse ahora que Poisson define su entrada principal, sin depender uno del otro.

## MODEL-004 — Modelo Matemático de Confidence

- **Estado:** Completada
- **% Avance:** 100% (estructura; coeficientes pendientes de calibración)
- **Dependencias:** MODEL-001, MODEL-002, MODEL-003, `engine/05`, `docs/17`, `docs/28` (todas Completadas)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Corrige un error detectado en el stub anterior (listaba "Índice de Caos" como entrada — incompatible con la ejecución en paralelo de `engine/04`/`05` en Capa 3). Distingue formalmente Probabilidad (incertidumbre aleatoria) de Confianza (incertidumbre epistémica), fundamentado en literatura real (Der Kiureghian y Ditlevsen 2009; Gneiting et al. 2007). Reutiliza Variable006/007 por tercera vez consecutiva (`engine/01`, `02`, ahora `05`) sin duplicar su cálculo. Confirma que la escala cualitativa ya tiene bandas numéricas en `docs/02-modelo.md` — no inventa umbrales nuevos. Documenta, sin resolver, la superposición conceptual con el factor "equipos parejos" de `engine/04`. Ningún peso fijado.
- **Próxima misión recomendada:** `models/chaos-index.md` — completa la Capa 3, y permite revisar formalmente la superposición conceptual ya señalada con Confidence.

## MODEL-005 — Modelo Matemático del Chaos Index

- **Estado:** Completada
- **% Avance:** 100% (estructura; coeficientes pendientes de calibración)
- **Dependencias:** MODEL-001, MODEL-002, MODEL-003, MODEL-004, `engine/04`, `docs/17`, `docs/28` (todas Completadas)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Primer documento de `models/` creado desde cero (no evoluciona un stub) — `engine/04` nunca tuvo respaldo de investigación desde el diseño original, verificado directamente en el directorio. Propone `Base_Caos` = entropía de Shannon normalizada de la distribución de `engine/03`, reutilizada sin recalcular, ajustada aditivamente por Variable001/006/007/012. Comparte variables con `MODEL-004` pero con tratamiento matemático distinto (aditivo vs. multiplicativo) — documentado como solapamiento conocido, no resuelto. Detecta que la categoría "Información" de `engine/04` (datos incompletos, cambios de entrenador) no tiene componente matemático hoy, por falta de Variable Oficial activa que la represente. Concluye explícitamente que `engine/06` **no puede construirse completamente todavía**: falta el Contrato de Datos de Mercado (`INC-05`). Ningún peso fijado.
- **Próxima misión recomendada:** `models/expected-value.md` — con Poisson, Confidence y Chaos completos, es el último de los 6 motores; su fundamento de rendimiento deportivo ya está listo, aunque su lado de mercado (cuotas) seguirá pendiente hasta que exista el Contrato de Datos de Mercado.

## MODEL-006 — Modelo Matemático del Expected Value

- **Estado:** Completada
- **% Avance:** 100% (estructura; coeficientes de la Recomendación y Contrato de Datos de Mercado pendientes)
- **Dependencias:** MODEL-001, MODEL-002, MODEL-003, MODEL-004, MODEL-005, `engine/06`, `docs/17`, `docs/28` (todas Completadas)
- **Fecha de inicio:** 2026-07-17
- **Fecha de finalización:** 2026-07-17
- **Observaciones:** Último de los 6 motores del Engine en obtener respaldo de investigación en `models/`. Deriva `EV = (P_modelo · c) − 1` desde primeros principios de valor esperado; formaliza `P_implícita = 1/c` (ya declarada en el Paso 3 del "Flujo del Motor" de `engine/06`) y documenta, como refinamiento de Versión 2.0, la normalización por margen de la casa (overround). Distingue formalmente Probabilidad (`engine/03`) → Expected Value (este motor) → Gestión de Bankroll (`engine/07`, futuro) — el Criterio de Kelly (Kelly, 1956) queda fuera de alcance conceptual, pertenece al tercer eslabón. Resuelve, con evidencia textual de la propia sección "Salida" de `engine/06`, que `EV` debe ser una función pura de `P_modelo` y cuota, mientras que `Recomendación` es el campo donde sí se integran Confianza y Caos, sin modificar el número de EV. Fundamenta con literatura real (Levitt 2004; Miller & Davidow 2019) una nota de prudencia ante EV extremadamente alto y el concepto de Closing Line Value. Corrige una referencia incorrecta del brief ("`docs/26-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`", que mezclaba nombre de `docs/25` con número de `docs/26`). Concluye en su Cierre (pregunta 8) que el núcleo matemático queda **estructuralmente completo** para los 6 motores por primera vez, pero **no calibrado** (ningún peso tiene valor numérico, `data/results/` sigue siendo marcador de posición) ni completamente desacoplado de sus fuentes de datos (`INC-05` sigue pendiente). Ningún peso fijado; no se modifica `engine/06` ni ningún otro documento existente.
- **Próxima misión recomendada:** Diseñar el Contrato de Datos de Mercado completo (cierra `INC-05` en implementación); resolver `INC-06` (Rotaciones); o iniciar la calibración real de los 6 motores una vez existan datos en `data/results/` — con `MODEL-001` a `006` completos, la investigación estructural del Engine ya no es el bloqueante principal.

## MODEL-007 — Calibración Matemática del Modelo de Poisson

- **Estado:** Completada
- **% Avance:** 100% (estructura; parámetros `μ_gol`, `κ`, `κ'`, `λ_min`, `λ_max` pendientes de calibración)
- **Dependencias:** MODEL-001, MODEL-002, MODEL-003, `docs/03`, `docs/17`, `engine/03` (todas Completadas) — extiende `models/poisson.md` (v2.0.0 → v2.1.0-investigación) sin redefinir su sección 6
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Extiende `models/poisson.md` con el orden exacto de aplicación de los ajustes de `λ` (Fuerza Base → Localía → λ preliminar → restricciones matemáticas → λ final), restricciones matemáticas nunca antes definidas (no negatividad, condición `κ' < 1`, piso `λ_min`, techo `λ_max`, función de saturación), un ejemplo completamente simbólico (sin valores numéricos), y limitaciones adicionales. **Detecta y resuelve, antes de escribir, una contradicción real entre el brief y la arquitectura ya vigente:** el brief pedía incorporar Historial Directo (Variable010) directamente al cálculo de `λ`, lo cual contradice `docs/03-Variables.md` ("Consumidor asignado: `engine/05-Confidence.md`... nunca deberá dominar el modelo"), `docs/17-Matriz-de-Consumo-de-Variables.md` (Variable010 "no utilizada, ni directa ni indirectamente" por `engine/03`) y la propia decisión de `MR-004`. Se documenta la exclusión con justificación completa (nueva sección 19 de `models/poisson.md`), incluyendo un mecanismo hipotético explícitamente no adoptado, en vez de incorporar la variable siguiendo el brief literal — coherente con la Constitución (Art. 6: ningún cambio de variable/motor sin evidencia y sin documentación previa en el nivel correspondiente) y con el límite de que una investigación de `models/` no tiene autoridad para redefinir la Matriz de Consumo ya vigente. Aclara, por separado, que Calidad de Plantilla (Variable008) sí participa en `λ`, pero únicamente de forma indirecta (ya incorporada vía `Pen` dentro de Fuerza Ofensiva/Defensiva desde `MODEL-001`/`MODEL-002`) — no se agrega un segundo término directo, para no duplicar su efecto. No implementa código, no modifica `engine/03`, no modifica Variables Oficiales, no fija ningún peso ni parámetro numérico.
- **Próxima misión recomendada:** Con los 6 motores ya en investigación estructural completa (`MODEL-001` a `007`), la prioridad real pasa al eje de datos: una misión de captura que resuelva los elementos de categoría D ya priorizados por `docs/27` (empezando por "Grandes oportunidades"), condición necesaria para cualquier calibración real. Alternativamente, en el eje de gobernanza, una futura `MR-`/`GR-` podría evaluar formalmente, con evidencia, si Historial Directo debería reconsiderarse como entrada de `engine/03` — fuera del alcance de esta investigación matemática.

## MODEL-008 — Calibración Oficial de Parámetros del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100% (procedimiento metodológico completo; ningún parámetro calibrado, por diseño)
- **Dependencias:** MODEL-001 a MODEL-007, `docs/10`, `learning/` (los 5 documentos), `docs/21` (todas Completadas) — reconcilia el pipeline ya existente sin redefinirlo
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `models/parameter-calibration.md`, primer documento de `models/` que fundamenta un procedimiento transversal en lugar de un motor específico. Cataloga los 22 símbolos pendientes de calibración de `MODEL-001` a `007`, distinguiendo Variable Oficial / Parámetro / Peso / Restricción / Constante (identifica que `H_max = ln(3)` de `chaos-index.md` es una constante matemática, no un parámetro a calibrar — hallazgo nuevo). Define el origen legítimo de todo parámetro (evidencia estadística / aprendizaje histórico / validación cuantitativa, nunca opinión) y reconcilia el ciclo de calibración pedido por el brief con el pipeline de `learning/` ya diseñado desde `MS-003`, identificando que el único eslabón sin documento propio era "Optimización" — lo cubre con un catálogo de 6 métodos candidatos (MLE, Grid Search, Bayesian Optimization, Cross Validation, Monte Carlo, Optimización Evolutiva), sin elegir ninguno, aclarando que Cross Validation es un protocolo de evaluación, no un método de optimización. Cataloga métricas de validación en dos familias (probabilística: Log Loss/Brier Score/Calibration Error; financiera: ROI/Yield), con advertencia explícita de que Accuracy es ingenua para un modelo probabilístico. Prohíbe explícitamente ajuste manual, recalibración en tiempo de predicción, fuga de datos (entrenar y validar con el mismo partido) y autoaprobación. No calibra ningún parámetro, no implementa código, no modifica el Engine, Runtime, Variables Oficiales, stack tecnológico ni ningún documento de `learning/`/`models/` ya existente.
- **Próxima misión recomendada:** Una misión de captura de datos (ya priorizada por `docs/27`) que provea el historial real necesario en `data/results/` — sin ese insumo, ningún método catalogado en esta misión tiene sobre qué ejecutarse.

---

# Registro de decisiones de stack tecnológico (ARCH-)

Serie independiente de todas las anteriores, iniciada en ARCH-000. Una misión `ARCH-` no diseña arquitectura funcional (eso es `MS-`/`DEV-`) ni modela datos (eso es `DATA-`) — congela una decisión tecnológica concreta (lenguaje, framework, motor de base de datos, herramientas), obligatoria para toda implementación futura.

## ARCH-000 — Decisión Oficial del Stack Tecnológico del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `CLAUDE.md`, `docs/21`, `docs/26`, `docs/29`, `docs/30`, `docs/33` (todas Completadas) — congela una decisión que las tres primeras dejaron deliberadamente abierta
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Se crea `docs/34-Decision-Oficial-del-Stack-Tecnologico.md`, primera misión de la nueva serie `ARCH-`. Congela oficialmente: Python (justificado por continuidad con `docs/12-Roadmap.md`, "v2: Python", y por el ecosistema científico que exige `models/`), PostgreSQL (ya diseñado a nivel físico en `docs/33`), FastAPI, SQLAlchemy 2.x, Alembic, NumPy/Pandas/SciPy, Pydantic, pytest, Ruff+MyPy (Black descartado por redundancia con `ruff format`), `uv`+`pyproject.toml`, Docker, y pisos mínimos de versión con advertencia explícita de incertidumbre por el corte de conocimiento del Arquitecto IA (enero 2026) frente a la fecha real del proyecto (julio 2026). **Detecta y documenta con prioridad alta una contradicción activa real:** `docs/33-Modelo-Fisico-PostgreSQL.md` §9 había asumido de facto Java/Spring Data JPA/Hibernate/Flyway/Liquibase sin mandato oficial (ya señalado allí mismo como hallazgo pendiente, `DATA-005`) — esta misión resuelve la ambigüedad a favor de Python/SQLAlchemy/Alembic, dejando desactualizada (no incorrecta en su modelo físico, agnóstico de ORM) la sección 9 de `docs/33`, y recomienda expresamente una misión de reconciliación editorial con prioridad sobre la siguiente investigación matemática (Constitución, Art. 7). Incluye Autocrítica (`docs/22`, sección 8). No implementa código, no crea estructura de carpetas, no modifica Runtime, Engine, Variables Oficiales, modelos matemáticos, `PredictionContext` ni Base de Conocimiento.
- **Próxima misión recomendada:** Con prioridad alta: reconciliación editorial de `docs/33` §9 (Compatibilidad) para alinearla con Python/SQLAlchemy/Alembic. En paralelo, sigue vigente la primera fórmula matemática real en `models/poisson.md`.

---

# Registro de construcción del proyecto Python (BUILD-)

Serie independiente de todas las anteriores, iniciada en BUILD-001. Una misión `BUILD-` no diseña arquitectura ni investiga matemática — crea o modifica archivos reales del proyecto Python (código, configuración, estructura de carpetas), siguiendo exactamente lo ya aprobado por `ARCH-`/`DEV-`/`DATA-`. Es, por diseño, la única serie de misiones que no produce un documento propio en `docs/` — su entregable es el propio proyecto, y su cierre queda registrado directamente en esta entrada del tracker (mismo patrón ya usado por `GR-008`, que tampoco generó un documento nuevo).

## BUILD-001 — Bootstrap Oficial del Proyecto Python del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100% (bootstrap completo; ningún componente funcional todavía, por diseño de la misión)
- **Dependencias:** `docs/34`, `docs/35`, `docs/29`, `docs/30`, `docs/33` (todas Completadas) — sigue exactamente la arquitectura ya aprobada, sin redefinir ninguna decisión
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Primera misión que crea archivos reales de código/configuración en lugar de documentación. Crea la estructura oficial completa de `docs/35` (`app/` con sus 9 subpaquetes — `api`, `runtime`, `preparation`, `engine`, `persistence`, `models`, `schemas`, `services`, `config` —, `tests/`, `migrations/` con Alembic inicializado sin revisiones, `scripts/`) y los 7 archivos base (`pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `.gitignore`, `alembic.ini`, más `app/main.py`). Cada paquete de `app/` contiene únicamente un docstring de responsabilidad citando `docs/35` — ninguna lógica de negocio. Registra exactamente las 11 dependencias aprobadas por el brief (sin agregar ninguna adicional, ni siquiera un *driver* de PostgreSQL como `psycopg`, documentado explícitamente como brecha pendiente en `.env.example`); agrega `[build-system]`/`[tool.setuptools]` a `pyproject.toml` como plomería de empaquetado no pedida literalmente por el brief pero indispensable para que `pip install .` funcione, documentada explícitamente como decisión, no como incumplimiento del alcance. **Decisión explícita del usuario (no del brief original):** el README técnico de instalación se crea en `app/README.md`, dejando intacto el `README.md` raíz — evita la colisión real que se habría producido si se hubiera seguido el brief literalmente (que pedía `README.md` en la raíz del nuevo proyecto). No implementa Runtime, `PredictionContext`, Engine, Variables, fórmulas, persistencia real ni endpoints funcionales — verificado explícitamente antes de cerrar la misión.
- **Próxima misión recomendada:** Dos caminos no excluyentes: (a) una misión de captura de datos reales (`docs/27`), que sigue siendo el bloqueante transversal para que `app/engine` tenga algo calibrado que ejecutar; (b) una misión `BUILD-`/`DEV-` que implemente el primer componente real (razonablemente, `app/models` — las 14 tablas de `docs/33` como clases SQLAlchemy — por ser la dependencia de la que todo lo demás, incluida la primera migración de Alembic, depende).

## BUILD-002 — Implementación del Modelo Relacional SQLAlchemy

- **Estado:** Completada
- **% Avance:** 100% (14 entidades implementadas; sin migraciones, sin conexión real, sin pruebas ejecutadas)
- **Dependencias:** `BUILD-001`, `docs/32`, `docs/33` (todas Completadas) — traduce el modelo físico ya diseñado a código, sin redefinir ninguna decisión
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `app/models/base.py` (clase `Base` declarativa + `UUIDPrimaryKeyMixin`/`TimestampMixin`/`CreatedAtOnlyMixin`) y las 14 entidades de `docs/33` en un módulo por clase, con `Mapped[]`/`mapped_column()`, `UUID` como clave técnica (generación Python, `uuid.uuid4`), claves de negocio preservadas como `UNIQUE`, y las 15 relaciones de `docs/32` como `relationship()`/`back_populates` bidireccionales — incluidas las dos N:M (`Convocatoria`, `EstadisticaPartido`) y las dos relaciones distintas de `Partido` hacia `Seleccion` (local/visitante), desambiguadas con `foreign_keys=`. Implementa las restricciones simples de `docs/33` §7 (`CHECK`/`UniqueConstraint`/integridad referencial) sin implementar los valores exactos de cada `ENUM` textual ni la restricción cruzada de `Auditoria` (ambas ya señaladas en `docs/33` como fuera del alcance de una implementación simple). **Detecta y documenta, sin resolver, una observación real** (no una mera limitación conocida): la recomendación de `docs/33` §7 de un índice único parcial sobre `jugadores.activo_seleccion` no se traduce con claridad al esquema real de esa tabla (una fila por jugador, no un historial) — documentado en el docstring de `jugador.py`, sin forzar una reinterpretación del esquema para justificarlo. No implementa `PropuestaAprendizaje` (ya excluida por `docs/33`, sección 4.15). El código no pudo ejecutarse en este entorno (sin Python disponible) — se verificó por revisión manual e inspección sistemática de imports (`grep`), no por ejecución real; se documenta esta limitación explícitamente en lugar de afirmar una validación que no ocurrió. No implementa repositorios, servicios, FastAPI, Runtime, `PredictionContext`, Engine, Variables Oficiales ni migraciones de Alembic.
- **Próxima misión recomendada:** Dos caminos no excluyentes: (a) una misión que ejecute y valide realmente este código en un entorno con Python/PostgreSQL disponibles, generando la primera migración de Alembic (`alembic revision --autogenerate`) a partir de `Base.metadata`; (b) continuar con `app/schemas` (contratos Pydantic de `PredictionRequest`/`PredictionReport`), que no depende de que `app/persistence`/Alembic estén resueltos todavía.

## BUILD-003 — Implementación de la Capa de Persistence

- **Estado:** Completada
- **% Avance:** 100% (infraestructura genérica completa; sin repositorios específicos, sin migraciones, sin conexión real probada)
- **Dependencias:** `BUILD-001`, `BUILD-002`, `docs/33`, `docs/34` (todas Completadas) — construye la infraestructura de acceso a datos sobre las 14 entidades ya implementadas
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `app/persistence/database.py` (`get_engine()`: Engine único, creación perezosa, lee `DATABASE_URL` vía `app/config`, `pool_pre_ping=True`, `echo=False` sin afinación de pool por falta de evidencia de carga), `session.py` (`SessionLocal`/`get_session()`: fábrica y gestor de contexto únicos con `commit`/`rollback`/`close` seguros), y `repositories/base_repository.py` (`BaseRepository` genérico parametrizado por tipo: `add`/`get`/`list`/`delete`/`update`, sin ninguna consulta específica). Agrega `psycopg[binary]>=3.1` a `pyproject.toml`, cerrando la brecha del *driver* de PostgreSQL ya documentada como pendiente desde `BUILD-001`/`BUILD-002` — primera dependencia añadida fuera de la lista original de `ARCH-000`, justificada explícitamente porque sin ella `create_engine()` no puede funcionar. No implementa `PredictionRepository`/`MatchRepository`/`SelectionRepository` ni ninguna consulta o filtro de negocio (explícitamente fuera de alcance del brief). No implementa Runtime, Engine, Variables Oficiales, `PredictionContext` ni migraciones de Alembic. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección sistemática de imports, no por ejecución real.
- **Próxima misión recomendada:** Dos caminos no excluyentes: (a) ejecutar y validar realmente este código junto con `app/models` (BUILD-002) en un entorno con Python/PostgreSQL disponibles, y generar la primera migración de Alembic; (b) implementar `app/schemas` (contratos Pydantic), que no depende de que Alembic/la conexión real estén resueltas todavía.

## BUILD-004 — Implementación del PredictionContext

- **Estado:** Completada
- **% Avance:** 100% (contrato de datos completo; sin Runtime, sin Engine, sin FastAPI)
- **Dependencias:** `BUILD-001`, `BUILD-002`, `BUILD-003`, `docs/30` (todas Completadas) — traduce el contrato ya diseñado a código, sin redefinir ningún bloque
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `app/runtime/prediction_context.py` con los diez bloques exactos de `docs/30` como modelos Pydantic (`BaseModel`), eligiendo explícitamente Pydantic sobre `dataclasses` porque los cinco requisitos del brief (mutable/serializable/tipado/fácil de persistir/fácil de auditar) son capacidades ya incorporadas sin código adicional (`.model_dump()`/`.model_dump_json()`). El bloque `engine` reutiliza, verbatim, la "Salida" ya declarada por cada uno de los 6 motores; `MarcadorProbabilidad` se comparte entre `engine03` y `prediction` para no duplicar estructura. Documenta explícitamente, en los docstrings de `AuditBlock`/`LearningBlock`, que ambos bloques nunca deben tener valor en el objeto en memoria de una ejecución (docs/30, "Nota central de diseño") -- se agregan solo al registro ya persistido. Cero métodos y cero lógica: la regla Append Only no se hace cumplir aquí (queda documentada como responsabilidad del futuro Runtime, no de este contrato de datos), conforme a "no implementar lógica del modelo". No implementa Engine, Preparation, FastAPI, persistencia real, consultas, cálculos, Variables Oficiales ni métodos matemáticos. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** Implementar el propio Runtime (el coordinador que construye este `PredictionContext` e invoca `VariablePreparation`/`EngineRunner`/`PredictionAssembler`/`Persistence`, docs/29) — es la pieza que consumirá este contrato por primera vez. En paralelo, sigue vigente ejecutar/validar el código ya escrito (`BUILD-002`/`003`/`004`) en un entorno real con Python disponible.

## BUILD-005 — Implementación del Runtime del Modelo Santiago

- **Estado:** Completada
- **% Avance:** 100% (coordinación completa; sin lógica interna de Preparation/EngineRunner/Persistence, por diseño explícito de la misión)
- **Dependencias:** `BUILD-001` a `BUILD-004`, `docs/29` (todas Completadas) — implementa el coordinador sobre el `PredictionContext` ya construido, sin redefinir el flujo ya diseñado
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `PredictionRuntime` en `app/runtime/runtime.py`: construye el `PredictionContext` (bloques `metadata`+`match`) e invoca, en el orden fijo de `docs/29` §4, `VariablePreparation` → `EngineRunner` → Assembler (interno, `docs/29` §2) → `Persistence`. Los tres colaboradores externos se inyectan como interfaces `typing.Protocol` (`VariablePreparationProtocol`, `EngineRunnerProtocol`, `PersistenceProtocol`) — ninguna implementación concreta se importa, cumpliendo literalmente "solo preparar las interfaces de invocación". Maneja errores marcando `errors` (`ErrorEntry`) y `estado_ejecucion` (reutilizando `EstadoEjecucion` de `BUILD-004`) sin propagar la excepción original. Registra `timestamp_creacion`/`timestamp_cierre`. El paso "Assembler" se implementó como transformación pura mínima (dict provisional, no el `PredictionReport` tipado que pertenece a `app/schemas`) — decisión documentada, ya que el brief no lo excluyó explícitamente de la lista de componentes sin lógica interna. Validado: el Runtime no calcula (ningún operador aritmético/estadístico en todo el archivo), toda la coordinación pasa por `PredictionContext`, cada fase tiene un único punto de entrada (`_crear_contexto`/`_invocar_preparation`/`_invocar_engine_runner`/`_ensamblar_reporte`/`_invocar_persistence`/`_registrar_error`), y no existe ningún import de FastAPI. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** Implementar `app/preparation` (VariablePreparation real, satisfaciendo `VariablePreparationProtocol`) — es el primer colaborador en el orden del flujo y no depende de que exista ninguna fórmula calibrada en `models/` todavía (solo de las Variables Oficiales ya contratadas en `docs/16`). `EngineRunner` sigue bloqueado hasta que exista al menos una fórmula real.

## BUILD-006 — Implementación de VariablePreparation

- **Estado:** Completada
- **% Avance:** 100% (estructura completa de las 9 variables activas; sin cálculo real, por diseño explícito de la misión)
- **Dependencias:** `BUILD-004`, `BUILD-005`, `docs/03`, `docs/16`, `docs/17`, `docs/30` (todas Completadas) — implementa el primer colaborador inyectado en `PredictionRuntime`
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `VariablePreparation` en `app/preparation/preparation.py`, satisfaciendo `VariablePreparationProtocol` (BUILD-005). Construye `context.variables` con las 9 Variables Oficiales activas en V1, cada una marcada `valor=None`/`disponible=False` ("PENDIENTE") — ningún cálculo, ninguna consulta SQL, ninguna decisión de suficiencia de datos (responsabilidad del Statistician, fuera de esta clase). Acepta un `PreparationRepositoryProtocol` opcional, no invocado en esta misión. **Detectó y reportó al usuario, antes de resolverla, una contradicción real:** el brief exigía "las 12 Variables Oficiales, no más, no menos", pero `docs/03`/`docs/17`/`docs/30` §4.3 ya establecen Variable005/011 como formalmente diferidas (`MR-004`), ausentes del `VariablesBlock` de BUILD-004 (9 campos) — agregar 2 campos habría violado, además, la restricción de esta misma misión de no modificar `PredictionContext`. Tras consultar, el usuario decidió explícitamente: implementar solo las 9 activas, documentar la discrepancia como observación, no editar `docs/03`/`docs/17`/`docs/30`. No implementa ningún motor (Fuerza Ofensiva/Defensiva/Poisson/Chaos/Confidence/Expected Value); no modifica Runtime, Persistence, `app/models` ni `PredictionContext`. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** Implementar `EngineRunner` (satisfaciendo `EngineRunnerProtocol`, BUILD-005) — sigue bloqueado en su lógica real hasta que exista al menos una fórmula calibrada en `models/` (`models/poisson.md`), pero su estructura de invocación por capas (`docs/29` §4) ya podría prepararse como *stub*, siguiendo el mismo patrón que esta misión. En paralelo, sigue vigente la captura de datos reales (`docs/27`).

## BUILD-007 — Implementación del EngineRunner

- **Estado:** Completada
- **% Avance:** 100% (coordinación por capas completa; ningún motor real implementado, por diseño explícito de la misión)
- **Dependencias:** `BUILD-004`, `BUILD-005`, `docs/06`, `docs/17`, `docs/29` (todas Completadas) — implementa el segundo colaborador inyectado en `PredictionRuntime`
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `EngineRunner` en `app/engine/engine_runner.py`, satisfaciendo `EngineRunnerProtocol` (BUILD-005) mediante tipado estructural. Coordina los 6 motores por capas (`docs/06`/`docs/17`/`docs/29`): Capa 1 (`Engine01`+`Engine02`), Capa 2 (`Engine03`), Capa 3 (`Engine04`+`Engine05`), Capa 4 (`Engine06`), cada uno inyectado vía una interfaz propia (`Engine01Protocol` a `Engine06Protocol`, seis en total, más `MotorProtocol` genérico para tipado interno). Implementa una semántica de fallo más fiel que un corte inmediato: dentro de una capa, un motor que falla no bloquea a su par independiente, pero si cualquiera de los motores de la capa falla, la capa siguiente no se ejecuta. Documenta explícitamente, sin implementar, dos simplificaciones: paralelismo real de Capa 1/3 (secuencial en este *stub*, con el punto exacto de un futuro reemplazo señalado en el código) y la condicionalidad de `Engine06` (Fase 4, solo si hay cuotas — tratado aquí igual que los otros cinco). Registra errores en `context.errors` sin propagar la excepción original. No implementa ningún motor real, no modifica Runtime, `PredictionContext` ni `Preparation`. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** Implementar `Persistence` (satisfaciendo `PersistenceProtocol`, BUILD-005, usando los repositorios de `app/persistence`, BUILD-003) — es el último colaborador que falta para que `PredictionRuntime` pueda ejecutar un flujo completo con *stubs* reales en sus tres puntos de inyección. En paralelo, sigue vigente la captura de datos reales (`docs/27`) y al menos una fórmula calibrada en `models/` para que los seis motores dejen de ser interfaces vacías.

## BUILD-008 — Implementación de Persistence del Runtime

- **Estado:** Completada
- **% Avance:** 100% (`persist_prediction` funcional; `persist_audit`/`persist_learning` como *placeholders* documentados, por diseño explícito de la misión)
- **Dependencias:** `BUILD-003`, `BUILD-004`, `BUILD-005`, `BUILD-006`, `BUILD-007` (todas Completadas) — cierra el tercer y último colaborador inyectado en `PredictionRuntime`, reutilizando exclusivamente la infraestructura ya construida
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Implementa `RuntimePersistence` en `app/persistence/runtime_persistence.py`, satisfaciendo `PersistenceProtocol` (BUILD-005) mediante `get_session`/`BaseRepository` (BUILD-003) — ninguna sesión, motor o conexión nueva. Reconcilia una diferencia de nomenclatura entre el brief (`persist_prediction`/`persist_audit`/`persist_learning`) y el nombre ya fijado por el Protocol (`guardar_prediccion`, no modificable): implementa ambos, con `guardar_prediccion` delegando en `persist_prediction`. **Detecta y documenta, sin resolver, una brecha real:** persistir una `Prediccion` exige `partido_id` (UUID técnico de `partidos.id`), mientras `context.match.id_partido` es solo el código de negocio — resolver uno del otro exigiría una búsqueda específica, prohibida por esta misión y ya excluida desde BUILD-003 (sin `MatchRepository`); `persist_prediction` recibe `partido_id` como parámetro explícito en vez de inventar una resolución interna. `persist_audit`/`persist_learning` quedan como *placeholders* documentados (`NotImplementedError` explícito, sin calcular ninguna métrica ni ejecutar `learning/`). Confirmado: ningún Engine conoce SQLAlchemy, ningún Runtime conoce SQLAlchemy directamente (ambos siguen dependiendo únicamente de `PredictionContext`/interfaces `Protocol`, sin cambios). No implementa lógica del modelo, consultas complejas ni endpoints; no modifica Runtime, Engine, Preparation, `PredictionContext`, modelos matemáticos ni Variables Oficiales. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** Implementar `app/schemas` (contratos Pydantic de `PredictionRequest`/`PredictionReport`) y, después, `app/api` (FastAPI) — con los tres colaboradores de `PredictionRuntime` ya resueltos (aunque dos con lógica *stub*/placeholder), la infraestructura del Runtime queda completa; lo que falta para una predicción real es contenido, no arquitectura: datos reales (`docs/27`), al menos una fórmula calibrada en `models/`, y la resolución de la brecha `id_partido` → `partido_id` (un futuro `MatchRepository`).

---

## BUILD-009 — Implementación del Engine01 (Fuerza Base)

- **Estado:** Completada, con un bloqueo arquitectónico documentado que impide la publicación completa del resultado en `PredictionContext`
- **% Avance:** 100% de lo que esta misión podía entregar dentro de su alcance real (cálculo matemático completo de Fuerza Ofensiva para ambos equipos); 0% de publicación en `PredictionContext` (bloqueada, ver Observaciones)
- **Dependencias:** `BUILD-004` (`PredictionContext`), `BUILD-006` (`VariablePreparation`, hoy entrega todas las variables como "PENDIENTE" — Engine01 se detendrá siempre en la validación de Variable003 hasta que exista una implementación real), `BUILD-007` (`EngineRunner`, ya captura las excepciones de este motor)
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Primer motor con cálculo matemático real del proyecto — implementa la fórmula completa de `models/offensive-strength.md` §6 (`Fuerza Ofensiva = clip(P · M_forma · (1 − Pen), 0, 100)`) en `app/engine/engine01.py`. **Dos contradicciones de alto impacto detectadas antes de escribir código, ambas reportadas y resueltas por decisión explícita del usuario, nunca de forma unilateral:**
  1. **Alcance del motor:** el brief pedía que Engine01 calculara también Fuerza Defensiva — contradice `docs/17` (asignada exclusivamente a `engine/02`), la separación ya implementada `Engine01Salida`/`Engine02Salida` (BUILD-004) y el propio "Fuera de alcance" del brief ("No implementar Engine02"). Resuelto: Engine01 calcula únicamente Fuerza Ofensiva.
  2. **Bloqueo arquitectónico de publicación (alto impacto, sin resolver):** `Engine01Salida.fuerza_ofensiva` (BUILD-004) es un único `float`, pero un partido tiene dos equipos y `models/poisson.md` §6 exige `FO_local`/`FO_visitante` como valores distintos. El motor calcula ambos correctamente (método interno `_calcular_fuerza_ofensiva_equipo`, invocado una vez por equipo) pero los retiene únicamente en un objeto interno no persistente (`_ResultadoEquipo`) — no los escribe en `context.engine.engine01`, porque BUILD-009 no tiene autoridad para modificar `app/runtime/prediction_context.py`/`docs/30`. Registra un `ErrorEntry` específico documentando el bloqueo (con ambos valores calculados y el tiempo de ejecución) y lanza `PublicacionBloqueadaPorEsquema`, que `EngineRunner` ya captura, deteniendo las capas siguientes — comportamiento correcto, ya que `engine/03-Poisson.md` no podría ejecutarse sin ambos valores reales.

  **Recomendación formal de esta misión: abrir `GR-009`** — misión de gobernanza para evolucionar oficialmente el contrato de `Engine01Salida` (y, por simetría, `Engine02Salida`) a una forma que admita un valor por equipo, **antes** de implementar `engine/03-Poisson.md`.

  Usa placeholders documentados (`TODO`) para los pesos sin calibrar: `DELTA_MAX=0.20`/`PEN_MAX=0.30` (citados literalmente de los ejemplos ya propuestos en `models/offensive-strength.md`); ponderación igualitaria para `w_R`/`w_T` y `w_D`/`w_F`/`w_Q` (sin ejemplo en ningún documento — placeholder neutral, no un valor "mágico"). Valida disponibilidad de Variable003 (Nivel A, obligatoria) para ambos equipos antes de calcular — si falta, registra `ErrorEntry` y lanza `VariableObligatoriaNoDisponible`, sin producir ningún resultado parcial inventado. Dado que `VariablePreparation` (BUILD-006) entrega hoy todas las variables como "PENDIENTE", **en el estado actual del proyecto Engine01 siempre se detendrá en esta validación** — comportamiento esperado y correcto, no un defecto de esta misión. No implementa Engine02 a Engine06, Runtime, Persistence, API ni repositorios; no modifica ningún otro motor, `EngineRunner` ni `PredictionContext`. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** `GR-009` (evolución del contrato de `Engine01Salida`/`Engine02Salida` para admitir Fuerza Ofensiva/Defensiva por equipo) — bloqueante para que `engine/03-Poisson.md` pueda implementarse con datos reales. Alternativamente, si se prioriza avanzar en paralelo, podría implementarse `app/engine/engine02.py` (Fuerza Defensiva, misma fórmula estructural de `models/defensive-strength.md`), que tiene el mismo bloqueo de publicación y se beneficiaría de resolverlo en la misma reconciliación.
- **Nota de cierre (BUILD-010):** el bloqueo de publicación descrito en el punto 2 y en la "Próxima misión recomendada" quedó resuelto a nivel de especificación por `GR-009` (`docs/30` v2.0.0 §4.4.1) y aplicado en código por `BUILD-010` — `Engine01` ya publica `context.engine.engine01`, `PublicacionBloqueadaPorEsquema` ya no existe. Este registro se conserva sin editar como evidencia histórica del hallazgo original.

---

## BUILD-010 — Aplicación en Código de GR-009 (PredictionContext Bipartito)

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `BUILD-004` (`PredictionContext` original), `BUILD-009` (`Engine01`, origen del bloqueo), `GR-009` (`docs/30` v2.0.0 §4.4.1, ya aprobado — todas Completadas)
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Sincroniza el código con el contrato ya reconciliado, sin rediseñar el Runtime ni tocar ninguna fórmula. `Engine01Salida` (`app/runtime/prediction_context.py`) deja de ser un único `fuerza_ofensiva: float` y pasa a contener dos instancias de la nueva clase `Engine01SalidaEquipo` (`local`, `visitante`), cada una con los mismos cinco campos ya declarados por `engine/01-Offensive-Strength.md` — sin campos nuevos, sin tocar ningún otro bloque del `PredictionContext` (`Engine02Salida` permanece exactamente igual, fuera de alcance). `Engine01.ejecutar()` (`app/engine/engine01.py`) ya no bloquea la publicación: construye `Engine01Salida(local=..., visitante=...)` a partir de los mismos dos resultados que ya calculaba y los escribe en `context.engine.engine01` — la fórmula, los placeholders (`DELTA_MAX`, `PEN_MAX`, ponderaciones igualitarias) y la lógica de disponibilidad de variables permanecen idénticos a `BUILD-009`. Se elimina `PublicacionBloqueadaPorEsquema` (ya sin uso) y la clase interna `_ResultadoEquipo` (redundante frente a `Engine01SalidaEquipo`, ahora pública). **Ajuste consecuencial, no una expansión de alcance:** `app/engine/__init__.py` re-exportaba `PublicacionBloqueadaPorEsquema`; se actualizó su import/`__all__` para que el paquete siguiera siendo importable — ningún otro contenido de ese archivo cambió, y no forma parte de la lista de archivos declarada como "puede modificar" en el brief, pero omitirlo habría dejado `app/engine` con un `ImportError` (un bloqueo nuevo, exactamente lo que la misión pide evitar). No se detectó ninguna contradicción nueva durante la verificación. No modifica `Engine02`, `Engine03`, Runtime, `VariablePreparation`, Persistence, API, Schemas, fórmulas matemáticas ni modelos SQLAlchemy. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** `app/engine/engine02.py` (Fuerza Defensiva, misma fórmula estructural de `models/defensive-strength.md`, mismo patrón bipartito ya validado aquí) — sin ningún bloqueo arquitectónico pendiente. Después, `engine/03-Poisson.md`, que ya puede consumir `FO_local`/`FO_visitante` reales de `engine01` (y, una vez exista, `FD_local`/`FD_visitante` de `engine02`).
- **Nota de cierre (BUILD-011):** contrario a lo previsto aquí, `Engine02Salida` **no** llegó ya bipartita a `BUILD-011` — esa misión detectó la misma brecha (por su propio alcance, `BUILD-010` la había dejado sin tocar) y la resolvió con autorización explícita del usuario. Este registro se conserva sin editar como evidencia histórica.

---

## BUILD-011 — Implementación de Engine02 (Fuerza Defensiva)

- **Estado:** Completada
- **% Avance:** 100%
- **Dependencias:** `BUILD-009`/`BUILD-010` (patrón arquitectónico y `Engine01SalidaEquipo` como precedente directo), `docs/17`, `models/defensive-strength.md`, `docs/30` v2.0.0 (todas Completadas/vigentes)
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Segundo motor con cálculo matemático real, implementando `models/defensive-strength.md` §6 en `app/engine/engine02.py` — mismo patrón exacto que `Engine01` (misma estructura de clase, mismos métodos, mismo manejo de errores/tiempos), sin decisiones de diseño nuevas. Reutiliza sin redefinir los placeholders de `M_forma`/`Pen` ya usados por `engine01` (`DELTA_MAX`, `PEN_MAX`, ponderaciones igualitarias), conforme a `models/defensive-strength.md` §6.1 ("se reutiliza M_forma y Pen... sin redefinirlos"). Lee Variable004 (obligatoria, Nivel A) y Variable001/002/006/007/008 (opcionales), exactamente lo asignado por `docs/17` a `engine/02`. **Contradicción real detectada antes de escribir código, detenida y reportada, resuelta por autorización explícita del usuario (ampliación de alcance):** el brief asumía que `Engine02Salida` ya era bipartita (`context.engine.engine02.local`/`.visitante`), pero `BUILD-010` la había dejado con su forma original de un único `float` a propósito (fuera de su propio alcance), y el "Alcance" original de `BUILD-011` no incluía `app/runtime/prediction_context.py` y prohibía explícitamente tocar `PredictionContext`. El usuario autorizó ampliar el alcance a ese archivo: se aplicó a `Engine02Salida` el mismo cambio ya validado en `Engine01Salida` (`BUILD-010`) — nueva clase `Engine02SalidaEquipo` (los cinco campos ya declarados por `engine/02-Defensive-Strength.md`), `Engine02Salida` con dos instancias (`local`/`visitante`), ningún campo nuevo, ningún otro bloque del `PredictionContext` tocado. `app/engine/__init__.py` actualizado para exportar `Engine02`; las dos clases `VariableObligatoriaNoDisponible` (una por motor, no intercambiables — una referencia Variable003, la otra Variable004) se re-exportan con alias distintos (`Engine01VariableObligatoriaNoDisponible`/`Engine02VariableObligatoriaNoDisponible`) para evitar que una oculte a la otra. No modifica `Engine01`, `Engine03`, Runtime, `VariablePreparation`, Persistence, API, Schemas, Services, Variables Oficiales ni ninguna fórmula matemática. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** `engine/03-Poisson.md` — con `Engine01` y `Engine02` ya publicando `FO_local`/`FO_visitante` y `FD_local`/`FD_visitante` reales (aunque con pesos placeholder sin calibrar), la Capa 2 del Engine ya tiene todas sus entradas disponibles por primera vez.

---

## BUILD-012 — Implementación de Engine03 (Distribución de Poisson)

- **Estado:** Completada
- **% Avance:** 100% de lo que esta misión podía entregar (matriz conjunta, λ, probabilidades y Top 4 funcionales); 0% de calibración (`μ_gol`, `κ`, `κ'`, `λ_min`, `λ_max` sin evidencia real) y 0% de datos reales (ningún `MuGolProvider` implementado todavía)
- **Dependencias:** `BUILD-010` (`Engine01Salida` bipartita), `BUILD-011` (`Engine02Salida` bipartita), `docs/17`, `models/poisson.md`, `docs/06`, `docs/30` v2.0.0 (todas Completadas/vigentes)
- **Fecha de inicio:** 2026-07-21
- **Fecha de finalización:** 2026-07-21
- **Observaciones:** Primer motor probabilístico completo — implementa `models/poisson.md` §6-9 en `app/engine/engine03.py`: `λ_local`/`λ_visitante` (Fuerza Ofensiva propia cruzada con Defensiva rival, `μ_gol`, Ajuste de Localía, restricciones `λ_min`/`λ_max` de `MODEL-007` §18), distribución de goles vía `scipy.stats.poisson` (sin implementación manual), matriz conjunta truncada en 6 goles con celda de cola agregada `"7+"` por equipo, Probabilidad Local/Empate/Visitante como suma de regiones, Top 4 de marcadores específicos (excluye celdas de cola). **Dos contradicciones de alto impacto detectadas antes de escribir código, ambas detenidas, reportadas y resueltas por decisión explícita del usuario:**
  1. **Localía directa:** el brief prohibía leer Variables Oficiales directamente, restringiendo las entradas a `Engine01Salida`/`Engine02Salida` — pero `docs/06` (línea 182), `docs/17` y `models/poisson.md` §6 coinciden, de forma independiente, en que Localía (Variable009) es una entrada **directa** de `engine/03`. Resuelto: Engine03 lee `context.variables.localia` además de las salidas de Engine01/02.
  2. **μ_gol sin fuente real:** `models/poisson.md` exige `μ_gol` "calculado dinámicamente... no un valor fijo", pero no es Variable Oficial, no es salida de Engine01/02, y ningún repositorio ya construido lo provee — fijarlo como constante habría contradicho el propio documento de investigación. Resuelto: `MuGolProvider` (`Protocol`) inyectable opcional, mismo patrón que `PreparationRepositoryProtocol` (`app/preparation`, BUILD-006); sin proveedor o sin dato para la competición, Engine03 registra `ErrorEntry` y se detiene, nunca inventa un valor.

  **Hallazgo #3, documentado pero no bloqueante (fuera de alcance de esta misión):** `docs/16-Contrato-Oficial-de-Variables.md` define Variable009 como ENUM de texto (`local`/`visitante`/`neutral`), pero `ValorVariable.valor` (`app/runtime/prediction_context.py`, BUILD-004) está tipado `float | None` — sin codificación numérica documentada de ese ENUM. Como Variable009 es opcional (Nivel D), Engine03 trata cualquier valor no interpretable como no disponible y aplica `Adj_Localía` neutral (`=1`), igual que el tratamiento ya establecido para variables opcionales ausentes en `Engine01`/`Engine02`. Hoy `VariablePreparation` entrega Variable009 siempre como no disponible, por lo que este es, en la práctica, el único camino alcanzable — no bloquea la misión. Candidato de una futura reconciliación `GR-` (`docs/16`/`ValorVariable`).

  Usa placeholders documentados sin cita textual en `models/poisson.md` (a diferencia de `DELTA_MAX`/`PEN_MAX` en `engine01`/`engine02`, que sí tenían "ej." explícito): `KAPPA_LOCAL`/`KAPPA_VISITANTE = 0.0` (sin ajuste de localía, opción menos informativa posible), `LAMBDA_MIN = 0.01` (épsilon técnico, evita el `λ=0` degenerado), `LAMBDA_MAX = 10.0` (techo estructural, señalado explícitamente en el código como el placeholder con la justificación más débil de todo el Engine, sin ninguna cita de respaldo). No implementa Chaos, Confidence, Expected Value, recomendaciones, mercado, Kelly ni ajustes manuales; no modifica `Engine01`, `Engine02`, `PredictionContext`, Runtime, Persistence ni `VariablePreparation`. Código no ejecutado en este entorno (sin Python disponible) — verificado por revisión manual e inspección de imports.
- **Próxima misión recomendada:** Diseñar e implementar una fuente real de `μ_gol` (`MuGolProvider` concreto, probablemente sobre `partidos.csv`/`data/processed/selecciones-nacionales/`) — es, junto con la ausencia de datos reales en `data/results/`, el bloqueante más directo para que Engine03 pueda ejecutarse de principio a fin con un resultado real. En paralelo, podría iniciarse `app/engine/engine04.py`/`engine05.py` (Chaos/Confidence, Capa 3), que ya podrían consumir la salida de Engine03 una vez exista un `MuGolProvider`.

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
