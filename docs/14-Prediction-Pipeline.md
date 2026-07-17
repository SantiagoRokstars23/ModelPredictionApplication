# Prediction Pipeline (V0.1)

**Archivo:** `docs/14-Prediction-Pipeline.md`

**Versión del documento:** 1.1.0

**Estado:** Especificación oficial del proceso de predicción — V0.1

---

# Objetivo

Este documento es la **especificación oficial del proceso de predicción V0.1** del Modelo Santiago: el recorrido exacto, a nivel de archivo, que sigue el sistema desde que un usuario solicita una predicción hasta que la Base de Conocimiento queda actualizada tras la finalización del partido.

Responde ocho preguntas concretas (ver "Preguntas respondidas" al final) sobre qué archivo se consulta primero, en qué orden se recorre la Base de Conocimiento, qué motores se ejecutan, qué se entrega al usuario, cómo se registra la predicción, cómo se actualiza la Base de Conocimiento al finalizar el partido, qué información nunca debe sobrescribirse y qué archivos se actualizan automáticamente.

---

# Relación con `docs/06-Flujo-Operacional.md` y `docs/15-Capa-de-Preparacion-de-Variables.md`

Este documento **no redefine** la arquitectura de fases, agentes ni el diagrama de dependencias del Engine — eso ya está definido en `docs/06-Flujo-Operacional.md` (Fases 0-10) y en `docs/04-Algoritmo.md` (los 14 pasos matemáticos/lógicos). Este documento tampoco modifica ninguno de esos archivos.

**Principio de desacoplamiento (`docs/15-Capa-de-Preparacion-de-Variables.md`):** la Base de Conocimiento (`data/processed/`) nunca entrega datos directamente a los motores. Toda la información pasa primero por la Capa de Preparación de Variables, que la transforma en las 12 Variables Oficiales (`docs/16-Contrato-Oficial-de-Variables.md`) ya validadas y normalizadas. Los motores (`engine/01` a `engine/06`) únicamente consumen esas variables — nunca leen un CSV, nunca conocen su origen físico. La tabla de la Etapa 2 (más abajo) describe el orden en que **la Capa** lee `data/processed/selecciones-nacionales/`, no un acceso directo del Engine.

Lo que aporta `docs/14-Prediction-Pipeline.md` es el **nivel de detalle de archivo** que `docs/06-Flujo-Operacional.md` deja intencionalmente a nivel de directorio (`data/processed/`, `data/predictions/`, etc.):

- Qué CSV concreto de `data/processed/selecciones-nacionales/` se lee primero y por qué.
- En qué orden se recorren los 11 archivos del módulo para una predicción concreta.
- Qué contrato exacto de salida recibe el usuario.
- Qué archivos concretos se tocan al registrar una predicción y al cerrar un partido.

Este documento cubre únicamente el tramo **Fase 0 a Fase 7** de `docs/06-Flujo-Operacional.md` (solicitud → predicción → registro → resultado oficial). No cubre Auditoría (Fase 8), Aprendizaje (Fase 9) ni Versionado (Fase 10) — esas fases ya están completamente especificadas en `docs/06-Flujo-Operacional.md` y no se duplican aquí.

---

# Flujo completo (visión general)

```
Solicitud del usuario
        │
        ▼
Predicción
        │
        ▼
Registro
        │
        ▼
(el partido se juega)
        │
        ▼
Actualización posterior de la Base de Conocimiento
```

Cada una de estas cuatro etapas se detalla a continuación.

---

# Etapa 1 — Solicitud del usuario → Archivos consultados primero

*(Responde la pregunta 1: "¿Qué archivos consulta primero?")*

Antes de leer un solo dato del partido, el sistema consulta siempre, en este orden fijo:

1. `CLAUDE.md` — gobierna el rol, las reglas y la prioridad entre documentos.
2. `docs/06-Flujo-Operacional.md` — determina qué agente actúa primero (Orchestrator) y en qué orden se invoca al resto.
3. `docs/04-Algoritmo.md` y `docs/03-Variables.md` — determinan qué variables y pasos son necesarios para calcular la predicción.
4. `prompts/prediction-template.md` — la plantilla que dispara el ciclo y define el contrato de salida esperado por el usuario.

Solo después de esto el sistema entra a la Base de Conocimiento (`data/processed/`) para el partido concreto solicitado — a través de la Capa de Preparación de Variables (`docs/15-Capa-de-Preparacion-de-Variables.md`), nunca mediante un acceso directo del Predictor o del Engine.

---

# Etapa 2 — Predicción → Orden de consulta de la Base de Conocimiento

*(Responde la pregunta 2: "¿En qué orden consulta la Base de Conocimiento?")*

Esta lectura la ejecuta la Capa de Preparación de Variables (`docs/15`), no el Engine ni el Predictor directamente. Dentro de `data/processed/selecciones-nacionales/`, el orden de lectura no es arbitrario: cada archivo se consulta en el momento en que una variable de `docs/03-Variables.md` lo necesita, nunca antes. El orden es:

| Orden | Archivo | Qué resuelve | Variable(s) que alimenta |
|---|---|---|---|
| 1 | `selecciones.csv` | Identidad de ambas selecciones (`id_seleccion`, ranking FIFA, seleccionador) | Insumo base para todo lo demás; Variable 008 (Calidad de Plantilla, vía ranking) |
| 2 | `competiciones.csv` | Tipo de competición (`tipo`, `confederacion_organizadora`) del partido solicitado | Índice de Caos (`engine/04`); ponderación por tipo de partido |
| 3 | `torneos.csv` | Edición concreta del torneo (fechas, sede, formato, fase) | Variable 002 (Rendimiento en el Torneo); Variable 009 (Localía, si sede única) |
| 4 | `estadios.csv` | Estadio asignado al partido (si ya está definido) | Variable 012 (Factores Externos: altitud, clima, superficie) |
| 5 | `arbitros.csv` | Árbitro asignado (si ya está definido) | Variable 012 (Factores Externos) |
| 6 | `partidos.csv` | Historial reciente de cada selección y enfrentamientos directos entre ambas | Variable 001 (Forma Reciente); Variable 010 (Historial Directo); Variable 002 (Rendimiento en el Torneo) |
| 7 | `estadisticas_partido.csv` | xG, posesión, disparos, tarjetas de esos partidos históricos | Variable 003 (Potencial Ofensivo); Variable 004 (Solidez Defensiva) |
| 8 | `jugadores.csv` + `convocatorias.csv` | Plantilla convocada para el torneo/partido | Variable 005 (Compatibilidad Táctica); Variable 008 (Calidad de Plantilla) |
| 9 | `lesiones.csv` | Bajas activas al momento del partido | Variable 006 (Disponibilidad de Plantilla) |
| 10 | `cuotas.csv` | Cuotas de mercado vigentes (si existen) | `engine/06-Expected-Value.md` — se consulta al final porque es la única entrada exclusiva de la Fase 4 (condicional) |

**Excepción documentada, no resuelta en esta misión:** `cuotas.csv` es, hoy, el único archivo de esta tabla que `engine/06-Expected-Value.md` consume directamente, sin pasar por la Capa de Preparación de Variables ni formar parte del Contrato Oficial de Variables (`docs/16`) — contradicción funcional ya identificada como `INC-05` en `docs/18-Plan-de-Reconciliacion-Arquitectonica.md` y `docs/23-Plan-Maestro-de-Reconciliacion-Operativa.md`. Resolverla requeriría una decisión de diseño (modelar las cuotas como variable oficial o hacerlas pasar por la Capa) que está fuera del alcance de esta misión, exclusivamente editorial.

**Regla de orden:** ningún archivo posterior en esta tabla se consulta si el anterior no pudo resolverse y esa variable es crítica (ver "Manejo de errores" en `docs/06-Flujo-Operacional.md`, ya vigente y no redefinido aquí). `cuotas.csv` es la única excepción explícita: su ausencia nunca detiene el flujo (Fase 4 es condicional).

---

# Etapa 2 (continuación) — Motores que ejecuta

*(Responde la pregunta 3: "¿Qué motores ejecuta?")*

El pipeline ejecuta exactamente los motores y en el orden por capas ya definido en `docs/06-Flujo-Operacional.md` ("Diagrama de dependencias del Engine"). Este documento no redefine ese orden, solo lo referencia como parte del pipeline de predicción:

```
Capa 1: engine/01-Offensive-Strength.md + engine/02-Defensive-Strength.md   (en paralelo)
Capa 2: engine/03-Poisson.md
Capa 3: engine/04-Chaos-Index.md + engine/05-Confidence.md                 (en paralelo)
Capa 4: engine/06-Expected-Value.md                                        (solo si hay cuotas)
```

---

# Etapa 2 (continuación) — Información que debe devolver al usuario

*(Responde la pregunta 4: "¿Qué información debe devolver al usuario?")*

El contrato de salida es el ya definido en `prompts/prediction-template.md`, formalizado aquí como el contrato oficial de la V0.1. Toda predicción entregada al usuario debe incluir, siempre en este orden:

1. Resumen del partido (selecciones, competición, fecha, estadio si aplica).
2. Variables más influyentes (declaradas explícitamente, nunca implícitas).
3. Probabilidad Local, Empate, Visitante (suma exacta 100%).
4. Top 4 de marcadores más probables, cada uno con su probabilidad.
5. Nivel de Confianza (escala 0-100, `docs/02-modelo.md` sección 7).
6. Índice de Caos (escala 0-100, `docs/02-modelo.md` sección 8).
7. Valor Esperado — o, explícitamente, "no disponible — sin cuotas registradas" si no existen cuotas (nunca se omite en silencio).
8. Explicación de las razones principales de la predicción.

Ninguna predicción puede omitir un ítem de esta lista sustituyéndolo por un valor inventado; si un dato no está disponible, se declara como no disponible (mismo principio que la Fase 2 de `docs/06-Flujo-Operacional.md`).

---

# Etapa 3 — Registro de la predicción

*(Responde la pregunta 5: "¿Cómo registra la predicción?")*

1. **Cuándo:** inmediatamente después de que el Predictor entrega el resultado del contrato de salida (Etapa 2), y siempre **antes** de que el partido comience. Nunca después.
2. **Dónde:** `data/predictions/`, siguiendo la convención ya anunciada en `data/predictions/README.md` (un archivo por torneo o por lote, identificable por `id_partido`).
3. **Qué se registra como mínimo:** el partido (`id_partido`), la fecha de la predicción, las probabilidades Local/Empate/Visitante, el Top 4 de marcadores, la Confianza, el Índice de Caos, el Valor Esperado (o su ausencia declarada), y la **versión del Modelo Santiago utilizada** (`data/predictions/README.md`: "Toda predicción deberá incluir la versión del modelo utilizada").
4. **Inmutabilidad:** una vez registrada, la predicción no se modifica ni se regenera silenciosamente. Si el usuario vuelve a solicitar una predicción para el mismo partido, el sistema informa que ya existe un registro en vez de generar un duplicado (regla ya vigente en `docs/06-Flujo-Operacional.md`, tabla "Manejo de errores").

El **esquema exacto de columnas** de los CSV de `data/predictions/` (nombres de campo, tipos, clave primaria) queda fuera del alcance de esta misión — requiere su propia misión de diseño de Base de Conocimiento, con el mismo nivel de rigor aplicado a `competiciones.csv` en MS-006.

---

# Etapa 4 — Actualización de la Base de Conocimiento al finalizar el partido

*(Responde la pregunta 6: "¿Cómo debe actualizar la Base de Conocimiento cuando el partido finaliza?")*

Cuando el partido finaliza, la actualización sigue el flujo ya definido en `docs/05-Base-de-Conocimiento.md` (Recolección → Validación → Normalización → Almacenamiento), aplicado aquí a dos destinos concretos y en este orden:

1. **`data/results/`** — se registra primero el resultado oficial verificado (fuente identificable, `docs/05-Base-de-Conocimiento.md`). Este dato es externo y crudo: no ha sido normalizado todavía.
2. **`data/processed/selecciones-nacionales/partidos.csv`** — una vez validado el resultado, se actualiza la fila del partido correspondiente: `estado_partido` pasa a `finalizado`, y se completan `goles_local`/`goles_visitante` (campos que, según el esquema de MS-001, solo se completan cuando `estado_partido = finalizado`).
3. **`data/processed/selecciones-nacionales/estadisticas_partido.csv`** — se incorporan, si están disponibles, las estadísticas finales del partido (xG, posesión, disparos, tarjetas) para ambas selecciones.

Solo después de que estos tres registros existen, la Fase 8 (Auditoría) de `docs/06-Flujo-Operacional.md` puede ejecutarse — ese paso ya está especificado allí y no se repite aquí.

---

# Información que nunca debe sobrescribirse

*(Responde la pregunta 7: "¿Qué información nunca debe sobrescribirse?")*

Consolidando las reglas ya declaradas en cada README de `data/` (no se redefinen, se listan aquí como referencia única para el pipeline de predicción):

| Dato | Regla | Fuente de la regla |
|---|---|---|
| `data/raw/` | Nunca se modifica una vez recolectado | `docs/05-Base-de-Conocimiento.md` |
| `data/predictions/*` | Nunca se sobrescribe una predicción; nunca se modifica después de iniciado el partido | `data/predictions/README.md` |
| `data/results/*` | Nunca se modifica un resultado oficial ya almacenado | `data/results/README.md` |
| `data/audit/*` | Nunca se elimina una auditoría histórica | `data/audit/README.md` |
| `data/archive/` | Nunca se elimina información histórica | `CLAUDE.md` |
| `id_seleccion`, `id_jugador`, `id_partido`, `id_competicion`, `id_torneo` | Identificadores inmutables una vez asignados (integridad referencial) | `data/processed/selecciones-nacionales/README.md` |
| `torneos.campeon_id_seleccion` | No existe como campo almacenado — siempre se deriva de `partidos.csv`, nunca se guarda ni se sobrescribe un valor fijo | MS-001 |

---

# Archivos que deben actualizarse automáticamente

*(Responde la pregunta 8: "¿Qué archivos deben actualizarse automáticamente?")*

| Archivo | Se actualiza automáticamente cuando... | Requiere aprobación humana |
|---|---|---|
| `data/predictions/*` | El Predictor entrega una predicción completa (Etapa 3) | No |
| `data/results/*` | El partido finaliza y el resultado oficial es verificable (Etapa 4, paso 1) | No (es un dato externo, no una decisión del modelo) |
| `data/processed/selecciones-nacionales/partidos.csv` | El resultado oficial ya fue validado (Etapa 4, paso 2) | No |
| `data/processed/selecciones-nacionales/estadisticas_partido.csv` | Existen estadísticas finales verificadas del partido (Etapa 4, paso 3) | No |
| `data/audit/*` | Existen tanto la predicción como el resultado para el mismo partido (Fase 8 de `docs/06-Flujo-Operacional.md`) | No |
| `docs/03-Variables.md`, `engine/`, `models/`, cualquier peso del modelo | — | **Sí, siempre.** Nunca se actualizan automáticamente; requieren una propuesta de `learning/` aprobada explícitamente por el Arquitecto Estadístico (Fases 9-10 de `docs/06-Flujo-Operacional.md`, fuera del alcance de este documento) |

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| 1. ¿Qué archivos consulta primero? | Etapa 1 |
| 2. ¿En qué orden consulta la Base de Conocimiento? | Etapa 2 — tabla de orden de archivos |
| 3. ¿Qué motores ejecuta? | Etapa 2 — Motores que ejecuta |
| 4. ¿Qué información debe devolver al usuario? | Etapa 2 — Información que debe devolver al usuario |
| 5. ¿Cómo registra la predicción? | Etapa 3 |
| 6. ¿Cómo actualiza la Base de Conocimiento cuando el partido finaliza? | Etapa 4 |
| 7. ¿Qué información nunca debe sobrescribirse? | "Información que nunca debe sobrescribirse" |
| 8. ¿Qué archivos deben actualizarse automáticamente? | "Archivos que deben actualizarse automáticamente" |

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se modifica ningún otro documento existente (`docs/06-Flujo-Operacional.md`, `docs/04-Algoritmo.md`, `engine/`, `prompts/prediction-template.md` se referencian, no se editan).
- No se diseña el esquema exacto de columnas de `data/predictions/`, `data/results/` ni `data/audit/` — queda diferido a una misión futura dedicada, siguiendo el mismo estándar aplicado a `competiciones.csv` en MS-006.
- No se crean torneos, partidos ni predicciones reales — este documento es únicamente la especificación del proceso.

---

Fin del documento.
