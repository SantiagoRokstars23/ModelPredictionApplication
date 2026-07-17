# Mapa Maestro del Modelo Santiago

**Archivo:** `docs/99-Mapa-Maestro.md`

**Misión:** solicitada como "GOV-001 — Mapa Maestro de la Arquitectura del Modelo Santiago"; registrada como **MAP-001** (ver nota de numeración)

**Versión:** 1.0.0

**Estado:** Vista de más alto nivel del proyecto — punto de entrada recomendado

---

## Nota de numeración

El brief pedía el identificador "GOV-001", ya usado por `docs/21-Constitucion-del-Modelo-Santiago.md`. Para no romper esa entrada, esta misión se registra como **`MAP-001`**, primera de una nueva serie que encaja mejor con su propósito real (mapa de navegación, no principios constitucionales). El **archivo** sí se crea exactamente donde se pidió: `docs/99-Mapa-Maestro.md` — la posición 99 se respeta tal cual, fuera de la secuencia numérica 00-25, precisamente porque este documento no es "uno más" en esa secuencia sino su índice conceptual.

---

# 1. Visión General

**¿Qué es?** Un sistema probabilístico para predicción de partidos de fútbol y evaluación de mercados de apuestas deportivas.

**¿Cuál es su objetivo?** Generar probabilidades explicables, auditables y rentables a largo plazo — nunca adivinar resultados ni operar por intuición (`CLAUDE.md`; `docs/21`, Art. 1).

**¿Qué problema resuelve?** Reemplaza el criterio subjetivo ("me parece", "tengo la sensación" — expresamente prohibido, `docs/02-modelo.md`) por un proceso estadístico reproducible: cada probabilidad debe poder rastrearse hasta la evidencia que la originó.

---

# 2. Arquitectura General

```
Usuario
   │
   ▼
Agentes (Orchestrator coordina; Statistician valida)
   │
   ▼
Capa de Preparación de Variables (docs/15)
   │
   ▼
Engine — 6 motores (docs/06, docs/17)
   │
   ▼
Predictor consolida → Reporte al usuario
   │
   ▼
Persistencia (data/predictions/)
   │
   ▼
(el partido se juega)
   │
   ▼
Resultado oficial (data/results/) → Auditoría (data/audit/)
   │
   ▼
Learning (propuesta, nunca aplicación automática)
   │
   ▼
Aprobación humana → Nueva versión
```

*(Versión simplificada del flujo completo — detalle exacto en `docs/06-Flujo-Operacional.md` y `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`.)*

---

# 3. Mapa de Directorios

| Directorio/archivo | Responsabilidad |
|---|---|
| `CLAUDE.md` | Gobierna el comportamiento operativo — máxima autoridad de facto |
| `docs/21-Constitucion...` | Principios estables — máxima autoridad conceptual |
| `docs/` | Documentación oficial: reglas, arquitectura, reconciliación (ver desglose abajo) |
| `engine/` | Motores matemáticos (6, uno por responsabilidad) |
| `models/` | Fundamentos estadísticos — investigación previa a toda fórmula |
| `learning/` | Aprendizaje posterior — analiza predicciones ya cerradas |
| `data/` | Base de Conocimiento (raw, processed, predictions, results, audit, archive) |
| `prompts/` | Plantillas operativas — disparan tareas, nunca contienen lógica |
| `.claude/agents/` | Especialistas IA — ejecutan una tarea concreta |
| `CHANGELOG.md` | Bitácora histórica de cambios |

## Desglose de `docs/` (categorizado — el listado completo, archivo por archivo, ya está en `README.md`; no se repite aquí)

| Rango | Categoría |
|---|---|
| `00`, `21`, `22` | Gobernanza y meta: Project Tracker, Constitución, Manual Operativo del Arquitecto IA |
| `01`-`05` | Fundamentos del modelo: Principios, Modelo, Variables, Algoritmo, Base de Conocimiento |
| `06`-`13` | Operación: Flujo Operacional, Bankroll, Predicciones, Auditoría, Aprendizaje, Versiones, Roadmap, Glosario |
| `14`-`17` | Arquitectura de datos del Engine: Prediction Pipeline, Capa de Preparación, Contrato de Variables, Matriz de Consumo |
| `18`-`20`, `23`-`24` | Reconciliación: inventarios de inconsistencias, auditoría independiente, gobernanza, plan maestro, análisis INC-04/INC-05 |
| `25` | Implementación conceptual: trazado de ejecución del Prediction Pipeline |
| `99` | Este mapa maestro |

---

# 4. Relaciones — qué puede consumir cada módulo, qué nunca debe

| Módulo | Puede consumir | Nunca debe consumir |
|---|---|---|
| `CLAUDE.md` / Constitución | — (máxima autoridad) | Ser contradicho por ningún otro documento |
| `docs/` | Constitución, `CLAUDE.md` | `engine/`, `data/` directamente — es especificación, no ejecución |
| `models/` | `docs/` (investigación) | Ejecutar cálculos sobre un partido real |
| `engine/` | Variables Oficiales (vía la Capa de Preparación), salidas de otros motores | `data/processed/` directamente (excepción documentada y no resuelta: `engine/06`/cuotas, `INC-05`) |
| Capa de Preparación (`docs/15`) | `data/processed/` | Calcular probabilidades, fuerzas, caos o valor esperado |
| `data/` | — (fuente de la verdad) | Modificarse retroactivamente (`raw/`, `results/`, `archive/` son inmutables una vez escritos) |
| `prompts/` | — | Contener lógica del modelo |
| `.claude/agents/` | `docs/`, `engine/`, `models/`, `data/` (según el rol de cada uno) | Asumir la responsabilidad de otro agente |
| `learning/` | `data/predictions/`, `data/results/` (ya cerrados) | Modificar automáticamente `docs/`, `engine/`, `models/` o cualquier variable |

---

# 5. Flujo Completo (resumen)

Desde la solicitud hasta el aprendizaje — 10 fases, ya especificadas en detalle en `docs/06-Flujo-Operacional.md`:

1. **Solicitud** — el usuario pide una predicción; la recibe siempre el Orchestrator primero.
2. **Validación** — el Statistician confirma que hay datos suficientes; si no, se detiene.
3. **Preparación de Variables** — la Capa transforma `data/processed/` en las 12 Variables Oficiales.
4. **Ejecución del Engine** — 6 motores, por capas de dependencia (`docs/17`).
5. **Valor Esperado** (condicional) — solo si hay cuotas y mercado solicitado.
6. **Bankroll** (opcional) — solo si el usuario lo pide.
7. **Registro** — la predicción se guarda en `data/predictions/`, inmutable, antes del partido.
8. **Resultado oficial** — se registra en `data/results/` cuando el partido termina.
9. **Auditoría** — compara predicción vs. resultado, nunca antes de que ambos existan.
10. **Aprendizaje y Versionado** — `learning/` propone; el Arquitecto Estadístico **Humano** aprueba o rechaza; solo entonces existe una nueva versión.

---

# 6. Estado Actual

*(Basado exclusivamente en `docs/00-Project-Tracker.md` — sin porcentajes nuevos ni inventados; el único porcentaje citado es el que ese documento ya mantiene.)*

| Componente | Estado |
|---|---|
| Arquitectura documental (`docs/00-25`, `engine/`, `models/`, `learning/`, `prompts/`, `.claude/agents/`) | **Completa** |
| Catálogo maestro de datos (`selecciones.csv`, `competiciones.csv`) | **Parcial** — 2 de 5 archivos con datos reales; `torneos.csv`, `estadios.csv`, `arbitros.csv` pendientes (`MS-002`) |
| Entidades relacionales (`jugadores`, `convocatorias`, `partidos`, `lesiones`, `cuotas`, `estadisticas_partido`) | **Pendiente** — solo encabezados, diferido desde `MS-001` |
| Reconciliación del Engine (`MR-001` a `MR-004`) | **Mayormente completa** — quedan `INC-06` (Rotaciones) y el Contrato de Datos de Mercado completo |
| Reconciliación de gobernanza (`GR-001` a `GR-007`) | **Parcial** — `GR-001`/`GR-002` completadas; `GR-003` a `GR-007` pendientes |
| Auditorías independientes (`AR-001`, `AR-002`) | **Completas** |
| Gobernanza constitucional (`GOV-001`, `GOV-002`) | **Completa** |
| Implementación conceptual (`IMP-001`) | **Completa** |
| Investigación matemática (`models/`, Versión 2.0 de cada documento) | **Pendiente en su totalidad** — los 6 documentos permanecen en estado "Investigación" |
| Código ejecutable | **No existe** — el repositorio es, por diseño, exclusivamente documentación hasta la fecha |
| `scripts/`, `excel/` | **No existen** |

Avance global citado por el Project Tracker: **~66%** (`docs/00-Project-Tracker.md`).

---

# 7. Roadmap

```
Arquitectura
   │  (docs/00-25, engine/, models/ stubs, learning/, prompts/, agentes — Completa)
   ▼
Implementación V0.1
   │  (IMP-001 completado: trazado del Prediction Pipeline)
   │  Pendiente: models/ Versión 2.0 de cada motor, catálogo maestro completo,
   │  reconciliaciones abiertas (INC-06, Contrato de Datos de Mercado, GR-003 a GR-007)
   ▼
V0.2
   │  (docs/12-Roadmap.md, v2: migración a Python; primeras predicciones reales
   │   auditadas contra resultados oficiales)
   ▼
Futuras versiones
   (docs/12-Roadmap.md, v3 Machine Learning · v4 Dashboard · v5 Automatización completa)
```

---

# 8. Principios (resumen — el detalle completo vive en `docs/21-Constitucion-del-Modelo-Santiago.md`, no se repite aquí)

Objetividad · Trazabilidad · Reproducibilidad · Transparencia · Evidencia antes que opinión · Separación de responsabilidades · Desarrollo incremental · Preservación de la historia · No autoaprobación (ningún cambio de peso se aprueba a sí mismo) · Autocrítica institucionalizada (el proyecto se audita a sí mismo de forma recurrente, ver `docs/18` a `docs/24`).

---

# Validaciones

- **¿Todo componente existente aparece representado?** Sí — los 7 directorios de primer nivel (`docs/`, `engine/`, `models/`, `learning/`, `data/`, `prompts/`, `.claude/agents/`) y los archivos raíz (`CLAUDE.md`, `README.md`, `CHANGELOG.md`) están en la sección 3; los 26 documentos de `docs/00-25` están categorizados, no listados uno a uno.
- **¿Las relaciones son correctas?** Verificadas contra `docs/20` (Jerarquía Documental) y `docs/15` (reglas de la Capa) — sin contradicción.
- **¿Existe duplicación con `README.md`?** No — `README.md` mantiene el listado completo archivo-por-archivo; este mapa aporta la categorización conceptual y el diagrama de flujo que `README.md` no tiene.
- **¿Sirve como punto de entrada para un nuevo desarrollador?** Sí — en menos de diez minutos de lectura, cubre qué es el proyecto, cómo fluye una predicción, qué existe y qué falta, y hacia dónde va.

---

# Cierre obligatorio

**1. ¿El mapa representa toda la arquitectura actual?**
Sí, a nivel de directorio y de categoría — no enumera cada uno de los 26 documentos de `docs/` individualmente (esa lista ya vive en `README.md`, y repetirla habría violado la restricción de no duplicar).

**2. ¿Qué módulos son el núcleo del Modelo Santiago?**
`docs/` (la especificación), la Capa de Preparación de Variables, `engine/` (los 6 motores) y `data/processed/` (la Base de Conocimiento) — sin estos cuatro no existe predicción posible.

**3. ¿Qué módulos son complementarios?**
`learning/` (mejora el modelo, pero el modelo funciona sin él), `prompts/` (facilitan el uso, no son indispensables para el cálculo), `.claude/agents/bankroll-manager.md` (explícitamente fuera del núcleo, `CLAUDE.md`), y `models/`/`scripts/`/`excel/` en su rol de apoyo (investigación, automatización, análisis externo).

**4. ¿Qué parte del proyecto se encuentra actualmente en implementación?**
Ninguna en el sentido de código ejecutable — el proyecto completo sigue siendo documentación. Lo más cercano a "implementación" hoy es conceptual: `IMP-001` (trazado de ejecución) y las reconciliaciones ya aplicadas sobre el texto (`MR-002`, `MR-003`, `MR-004`, `GR-002`).

**5. ¿Qué recomendarías construir después?**
La primera investigación matemática real en `models/` (empezando por `models/poisson.md`, el motor con más dependientes) — es el paso que falta para que este mapa dejе de describir un sistema calculable en teoría y empiece a describir uno calculable en la práctica.

---

# Fuera de alcance de esta misión

- No se modifica ningún documento existente.
- No se redefine ningún componente, regla ni principio.
- No se renombra ni reorganiza ningún archivo o carpeta.
- No se repite el contenido de `README.md` ni de `docs/21-Constitucion-del-Modelo-Santiago.md` — se referencian.

---

Fin del documento.
