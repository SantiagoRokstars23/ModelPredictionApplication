# Plan Oficial de Reconciliación de la Gobernanza Documental

**Archivo:** `docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md`

**Misión:** GR-001 — Plan Oficial de Reconciliación de la Gobernanza Documental

**Versión:** 1.0.0

**Estado:** Plan oficial — sin modificaciones aplicadas

---

# Objetivo

Este documento actúa como acta de un **Consejo de Gobernanza Arquitectónica**. No modifica ningún documento. Diseña el plan oficial que reconciliará, en misiones futuras, los documentos que gobiernan al Modelo Santiago (`CLAUDE.md`, `README.md`, `data/README.md`, `docs/13-Glosario.md`, `docs/11-Versiones.md`, `CHANGELOG.md`, `docs/00-Project-Tracker.md`, `.claude/agents/`, `prompts/`) — distintos de los documentos de arquitectura del Engine ya cubiertos por `docs/18-Plan-de-Reconciliacion-Arquitectonica.md` (MR-001) y auditados por `docs/19-Architecture-Freeze-Review.md` (AR-001).

Su aprobación cierra la fase de diseño documental de la gobernanza y habilita las reconciliaciones específicas (serie `GR-`).

---

# 1. Estado actual de la gobernanza documental

La gobernanza del Modelo Santiago tiene **dos velocidades claramente distintas**:

- **El proceso de avance está sólidamente gobernado.** Diecinueve misiones consecutivas (`MS-001` a `AR-001`) actualizaron disciplinadamente `CHANGELOG.md` y `docs/00-Project-Tracker.md` sin excepción — existe un mecanismo de facto, aunque no escrito como regla explícita, que garantiza que todo cambio quede registrado y su estado sea consultable.
- **El proceso de sincronización hacia atrás no existe.** Ningún mecanismo actualiza `CLAUDE.md`, `README.md`, `data/README.md`, `docs/13-Glosario.md` o `.claude/agents/` cuando se agrega un documento nuevo a `docs/`. El resultado, ya evidenciado por AR-001, es que el documento de mayor autoridad del proyecto (`CLAUDE.md`) desconoce la existencia de cinco de sus documentos más recientes y arquitectónicamente centrales.

**Conclusión del estado actual:** la gobernanza no está ausente ni mal diseñada en sus fundamentos — está **desactualizada de forma asimétrica**: crece hacia adelante (nuevas misiones) sin un mecanismo equivalente que la sincronice hacia los documentos de nivel superior que la gobiernan.

---

# 2. Inventario de documentos de gobierno

| Documento | Propósito | Autoridad | Alcance | Dependencias |
|---|---|---|---|---|
| `CLAUDE.md` | Fijar el rol, la filosofía, las reglas inquebrantables y el orden de prioridad de todo el proyecto | Máxima — "override[a] cualquier comportamiento por defecto" (declarado en su propio encabezado) | Todo el repositorio, sin excepción | Ninguna — es la raíz de la jerarquía |
| `README.md` | Servir de mapa de navegación público del repositorio para un lector nuevo | Ninguna prescriptiva — es un resumen derivado, nunca una fuente primaria | Todo el repositorio, en forma de índice | `CLAUDE.md`, y refleja (debería reflejar) el estado real de `docs/` |
| `docs/00-Project-Tracker.md` | Registrar el estado real de cada misión: completada, en progreso, pendiente, dependencias | Alta sobre el **proceso** (qué está hecho y qué falta), nula sobre el **contenido técnico** | Todas las misiones `MS-`, `MR-`, `AR-`, `GR-` | `CLAUDE.md` |
| `CHANGELOG.md` | Bitácora técnica granular de qué cambió, cuándo y por qué | Nula prescriptiva — es un registro histórico, no una regla | Todo cambio de cualquier documento del repositorio | `CLAUDE.md` ("Toda mejora deberá registrarse en CHANGELOG.md") |
| `docs/11-Versiones.md` | Registrar el historial de versiones del **modelo predictivo** (no del repositorio) | Nula prescriptiva — es un registro | El comportamiento predictivo del Modelo Santiago a través del tiempo | `docs/06-Flujo-Operacional.md` (Fase 10), `learning/version-history.md` |
| `docs/13-Glosario.md` | Definir de forma centralizada los términos usados en todo el proyecto | Referencial/transversal — no gobierna decisiones, pero todo lo demás depende de su vocabulario | Todo término técnico usado en `docs/`, `engine/`, `models/`, `learning/` | Ninguna formal — debería derivar sus definiciones de donde cada término se originó (`engine/04`, `engine/05`, `docs/16`, etc.) |
| `data/README.md` | Definir la filosofía y estructura de la Base de Conocimiento | Alta sobre `data/`, pero **no** sobre cómo el Engine consume esos datos (esa autoridad pertenece a `docs/15`) | El directorio `data/` y sus 6 subdirectorios | `docs/05-Base-de-Conocimiento.md` |
| `.claude/agents/` (6 archivos) | Especializar el comportamiento de cada agente ejecutor | Autoridad sobre su propio agente únicamente; ninguno puede asumir responsabilidad de otro (regla explícita en cada "Juramento del Agente") | Un agente cada uno | `CLAUDE.md`, `docs/`, `engine/`, y (deberían) `docs/15-17` |
| `prompts/` (4 archivos) | Disparar una tarea concreta con instrucciones reutilizables | Ninguna — "nunca contienen lógica del modelo" (`CLAUDE.md`) | Una tarea específica cada uno (predicción, auditoría, recalibración, análisis de torneo) | `CLAUDE.md`, `docs/`, `engine/`, `data/processed/` |

---

# 3. Inconsistencias de gobernanza (consolidadas, sin repetir las del Engine)

Se consolidan aquí únicamente las ya detectadas por AR-001 que son de naturaleza **de gobernanza** (autoridad, sincronización, definición terminológica, versionado) — no las de arquitectura del Engine (`INC-01` a `INC-11`, ya cubiertas por el roadmap de MR-001), ni las de contenido funcional inmaduro que no involucran autoridad o sincronización (`INC-14`, bandas de `docs/07-Backroll.md`; `INC-16`, sobreestimación de `learning/README.md` sobre `docs/09`/`docs/10`) — estas dos últimas se dejan explícitamente fuera de esta consolidación por no ser, en sentido estricto, problemas de *gobernanza* sino de *madurez de contenido*, y se recomienda tratarlas en una misión de reconciliación de contenido funcional, no de gobernanza.

| ID | Descripción | Gravedad |
|---|---|---|
| INC-12 | `README.md` y `data/README.md` describen el Engine consumiendo `data/processed/` directamente, sin mencionar la Capa de Preparación de Variables | Alta |
| INC-13 | Ningún archivo de `.claude/agents/` menciona `docs/15`, `docs/16` o `docs/17` | Alta |
| INC-15 | `docs/13-Glosario.md` no contiene ninguna definición real | Alta |
| INC-17 | Dos esquemas de versionado sin sincronizar: `CHANGELOG.md` y `docs/11-Versiones.md` | Media |
| INC-18 | El "Orden de Lectura" de `CLAUDE.md` (y su réplica en `README.md`) no incluye `docs/07` a `docs/18` | **Crítica** |
| INC-19 | `README.md` resume solo 6 de los 8 principios reales de `docs/01-principios.md` | Baja |

## Hallazgo nuevo de esta misión: INC-20 — Ambigüedad de identidad del rol "Arquitecto Estadístico"

**Descripción:** `CLAUDE.md`, sección "Tu Rol", asigna el rol de "Arquitecto Estadístico del Modelo Santiago" directamente al asistente de IA ("Actúas como el Arquitecto Estadístico..."). Sin embargo, `docs/06-Flujo-Operacional.md`, Fase 9, exige que ese mismo rol implique explícitamente **"revisión humana obligatoria"** antes de aprobar cualquier propuesta de `learning/weight-adjustment.md`: *"Esa propuesta queda en estado 'pendiente' hasta que el Arquitecto Estadístico del Modelo Santiago (rol definido en CLAUDE.md) la revise y decida explícitamente aprobarla o rechazarla."* Ningún documento aclara si "Arquitecto Estadístico" designa (a) al asistente de IA que opera el repositorio en una sesión dada, (b) al usuario humano propietario del proyecto, o (c) ambos según el contexto. Esta ambigüedad es relevante precisamente en el punto de mayor riesgo del proyecto: la aprobación de cambios de peso, que `CLAUDE.md` protege explícitamente ("Nunca alterar pesos sin evidencia estadística").
**Documentos involucrados:** `CLAUDE.md`, `docs/06-Flujo-Operacional.md`.
**Gravedad:** Alta — no es un problema cosmético: si "Arquitecto Estadístico" pudiera interpretarse como el propio asistente de IA en el contexto de Fase 9, la salvaguarda de "revisión humana obligatoria" quedaría sin efecto real.
**Clasificación:** gobernanza, autoridad, riesgo de control.

---

# 4. Autoridad documental (jerarquía oficial propuesta)

No se asume que la jerarquía implícita actual (el orden en que `CLAUDE.md` lista su "Orden de Lectura") sea correcta — de hecho, esa lista mezcla dos conceptos distintos (orden de *lectura* recomendado vs. autoridad en caso de *conflicto*) sin distinguirlos. Se propone la siguiente jerarquía, justificada por la función real de cada capa:

| Nivel | Documentos | Justificación |
|---|---|---|
| **1 — Gobierna** | `CLAUDE.md` | Es la única capa que se declara a sí misma como override absoluto; ningún otro documento puede contradecirla |
| **2 — Rige el proceso** | `docs/00-Project-Tracker.md` | Autoridad sobre el *estado* del proyecto (qué está completado, pendiente, sus dependencias) — no puede contradecir a `CLAUDE.md`, pero cualquier otro documento debe ser consistente con lo que el Tracker declara como estado real |
| **3 — Define la arquitectura funcional** | `docs/01` a `docs/19` | El "qué" del modelo: filosofía, variables, algoritmo, flujo, contrato de variables, matriz de consumo, reconciliaciones. `docs/13-Glosario.md` es transversal dentro de este nivel: no es jerárquicamente superior a los demás documentos de `docs/`, pero todos ellos dependen de su vocabulario compartido |
| **4 — Investiga y respalda** | `models/` | El "por qué matemático" — ningún motor puede incorporar una fórmula sin respaldo aquí primero (`CLAUDE.md`: "Investigación antes de implementación") |
| **5 — Implementa la lógica** | `engine/` | El "cómo" del cálculo, ejecutando lo que `models/` respalda y `docs/` ordena |
| **6 — Almacena el conocimiento** | `data/` (incl. `data/README.md`) | El dato en sí — gobernado por su propio README, pero **nunca** puede definir cómo el Engine lo consume (esa autoridad es del Nivel 3, específicamente `docs/15`) |
| **7 — Dispara tareas** | `prompts/` | Nunca decide ni calcula — solo activa una fase ya definida en un nivel superior |
| **8 — Ejecuta especializado** | `.claude/agents/` | Aplica todos los niveles anteriores a una tarea concreta; su autoridad es exclusivamente sobre sí mismo |
| **Fuera de la jerarquía (no prevalecen en conflicto)** | `README.md`, `CHANGELOG.md` | `README.md` es un resumen derivado y navegacional, nunca una fuente primaria — si contradice a cualquier `docs/NN`, gana el `docs/NN`. `CHANGELOG.md` es una bitácora histórica pasiva, no emite reglas, por lo que no participa en la resolución de conflictos |

**Regla de conflicto derivada:** ante una contradicción entre dos documentos, prevalece el de menor número de Nivel; dentro de un mismo Nivel, prevalece el documento más específico sobre el más general (ej. `docs/15` sobre `docs/06` en materia de cómo el Engine consume datos, porque `docs/15` es más reciente y más específico en ese punto exacto — mismo criterio que ya aplica `CLAUDE.md`: "Si existe conflicto entre documentos, deberá prevalecer el de mayor prioridad", aquí formalizado con un criterio objetivo en lugar de dejarlo implícito).

---

# 5. Flujo documental oficial (consulta antes de ejecutar una tarea)

```
CLAUDE.md
    │  (autoridad absoluta — siempre primero)
    ▼
docs/00-Project-Tracker.md
    │  (evita duplicar trabajo ya hecho o en curso)
    ▼
README.md
    │  (mapa de navegación — opcional pero recomendado para orientarse rápido)
    ▼
docs/13-Glosario.md
    │  (vocabulario común — hoy vacío, INC-15; la posición en el flujo es correcta,
    │   el contenido todavía no)
    ▼
Arquitectura funcional relevante a la tarea (docs/01-19, solo los pertinentes)
    │
    ▼
models/ (si la tarea toca el Engine)
    │
    ▼
engine/ (los motores relevantes)
    │
    ▼
data/ (estado real de la Base de Conocimiento)
    │
    ▼
prompts/ (la plantilla que dispara la tarea, si aplica)
    │
    ▼
.claude/agents/<agente correspondiente>.md
    │  (confirma los límites y el "Juramento" del agente que ejecutará)
    ▼
Ejecución de la tarea
    │
    ▼
CHANGELOG.md + docs/00-Project-Tracker.md
    (registro posterior, no antes)
```

**Justificación de las diferencias respecto al ejemplo conceptual de la misión** ("CLAUDE.md → README → Arquitectura → Variables → Motores → Prompts → Agentes"): se inserta `docs/00-Project-Tracker.md` inmediatamente después de `CLAUDE.md` (antes que `README.md`) porque su función — evitar iniciar una misión que ya existe o que depende de otra pendiente — es más urgente que la de orientación general; se inserta `docs/13-Glosario.md` antes de la arquitectura funcional porque un vocabulario común mal interpretado puede invalidar la lectura de todo lo que sigue; y se agrega `CHANGELOG.md`/el propio Tracker **al final**, como cierre obligatorio, no como parte de la consulta previa — reflejando la regla ya vigente de que todo cambio se documenta después de ejecutarse, nunca antes.

---

# 6. Gobernanza de agentes

| Agente | Conocimiento mínimo obligatorio (propuesto) | Conocimiento opcional | Brecha actual |
|---|---|---|---|
| `orchestrator.md` | `CLAUDE.md`, `docs/00`, `docs/06-Flujo-Operacional.md`, `docs/14-Prediction-Pipeline.md`, `engine/` (índice, no el detalle interno), `data/processed/` (solo disponibilidad) | `docs/15-17` (detalle que delega en el Predictor) | Ninguna crítica — su rol de coordinación no requiere el detalle interno de variables |
| `predictor.md` | `docs/03-Variables.md`, `docs/04-Algoritmo.md`, **`docs/15`, `docs/16`, `docs/17`** (hoy ausentes — es la brecha más grave de INC-13, porque es el agente que más debería conocerlos), `engine/01-06`, `models/` | `docs/07-Backroll.md` (no le compete) | Crítica — es quien invoca el Engine directamente |
| `statistician.md` | `docs/05-Base-de-Conocimiento.md`, `docs/15` (sección 6, para distinguir su validación de suficiencia de la validación de construcción de la Capa — ya recomendado en MR-006), `docs/03-Variables.md` | `engine/` (no ejecuta motores) | Ya identificada como INC-11 (MR-001) / ampliada por AR-001 (MR-006) |
| `odds-analyzer.md` | `docs/16` (para saber que las cuotas hoy **no** son una Variable Oficial — cierra la ambigüedad de INC-05/INC-13 desde el lado del agente), `engine/06` | `docs/07-Backroll.md` | Alta — hoy dice consultar "data/" directamente, reforzando INC-05 |
| `bankroll-manager.md` | `docs/07-Backroll.md`, con la advertencia explícita de que sus bandas no están reconciliadas con `docs/02-modelo.md` (INC-14) hasta que se resuelva | `docs/16` (Valor Esperado ya calculado, no lo recalcula) | Media |
| `auditor.md` | `docs/09-Auditoria.md`, `docs/11-Versiones.md`, `learning/error-analysis.md`, con la advertencia explícita de que las métricas de `docs/09` no tienen fórmula definida todavía (para no inventarla) | `docs/16` (no consume variables, consume predicciones ya cerradas) | Media |

**Principio general propuesto:** todo agente debe declarar explícitamente, en su propio archivo, tanto su conocimiento obligatorio como las brechas conocidas que todavía no se han reconciliado (ej. "hoy no distingo mi validación de la de la Capa de Preparación de Variables, ver `docs/15`") — en lugar de omitir silenciosamente una referencia que ya no está actualizada. Esto no se aplica en esta misión (no se modifican agentes), pero se deja como criterio de diseño para `MR-006`.

---

# 7. Versionado

**Diagnóstico:** existen dos sistemas de versionado activos, sin relación formal entre sí (INC-17): `CHANGELOG.md` (SemVer, formato Keep a Changelog, cortó una única versión real: `1.0.0`, y desde entonces permanece en `[Unreleased]` pese a ~19 misiones) y `docs/11-Versiones.md` (una secuencia propia `v1.0` a `v1.3` que describe cambios de comportamiento del modelo, aparentemente ilustrativa más que real).

**¿Duplicidad?** No en su propósito — cada uno responde una pregunta distinta: `CHANGELOG.md` responde "¿qué cambió técnicamente y cuándo, a nivel de archivo?"; `docs/11-Versiones.md` está diseñado para responder "¿qué significa ese cambio para el comportamiento predictivo del modelo?" (una capa narrativa, no técnica). **Sí hay duplicidad de facto** en la práctica actual, porque ninguno de los dos referencia al otro, y por tanto ambos terminan siendo, cada uno por separado, la única fuente de verdad de "en qué versión estamos" según a cuál se le pregunte.

**Recomendación (sin aplicarla en esta misión):** no unificar los dos documentos en uno solo — mantenerlos separados, pero con una regla de sincronización explícita: cada versión narrada en `docs/11-Versiones.md` debe corresponder exactamente a una versión (tag) cortada en `CHANGELOG.md`, nunca a una numeración propia e independiente. Esto preserva la separación de altitud (técnica vs. narrativa de producto) que ya existe en `docs/06-Flujo-Operacional.md` (Fase 10: "Actualizar `docs/11-Versiones.md`... Registrar la mejora en `CHANGELOG.md`" — ya se diseñó como una actualización conjunta, solo que `docs/11-Versiones.md` nunca recibió contenido real consistente con esa regla).

---

# 8. Roadmap de reconciliación de gobernanza

## GR-002 — Reconciliación de `CLAUDE.md` y `README.md`

- **Objetivo:** Actualizar el "Orden de Lectura" de `CLAUDE.md` para incluir `docs/07` a `docs/19` (como mínimo referenciar la serie 14-19 explícitamente), y replicar el mismo orden corregido en `README.md`; completar el resumen de principios de `README.md` con los 8 de `docs/01-principios.md`.
- **Documentos afectados:** `CLAUDE.md`, `README.md`.
- **Dependencias:** Ninguna — es aislada y de bajo riesgo (cambio de índice/referencias).
- **Prioridad:** **Crítica** — resuelve INC-18 (la inconsistencia de mayor autoridad formal detectada hasta ahora) e INC-19. Se recomienda ejecutarla **antes que MR-002**, dado que ninguna reconciliación del Engine depende de ella, pero toda futura sesión que abra el proyecto sí depende de que `CLAUDE.md` la refleje.

## GR-003 — Reconciliación de `data/README.md` con la Capa de Preparación de Variables

- **Objetivo:** Actualizar la afirmación "processed/ es la única fuente autorizada para el Engine" y la sección "Dependencias" de `data/README.md` para reflejar que el Engine consume variables preparadas por `docs/15`, no `data/processed/` directamente.
- **Documentos afectados:** `data/README.md`.
- **Dependencias:** Se recomienda ejecutarla junto con `MR-003` (que ya reconcilia el mismo mensaje en `docs/06`/`docs/14`), para mantener un único mensaje consistente en una sola ventana de cambio.
- **Prioridad:** Alta.

## GR-004 — Población real de `docs/13-Glosario.md`

- **Objetivo:** Redactar definiciones reales (no solo listar términos) para xG, ROI, Yield, EV, Poisson, Kelly, Drawdown, Confianza, Índice de Caos, y agregar los términos ausentes identificados por AR-001 (Variable, Predicción, Probabilidad, Versión).
- **Documentos afectados:** `docs/13-Glosario.md`.
- **Dependencias:** Ninguna estricta, aunque se beneficia de que `docs/09-Auditoria.md` ya tenga fórmulas definidas para ROI/Yield/Drawdown (hoy inexistentes en cualquier documento) — si esa reconciliación de contenido funcional no ha ocurrido todavía, el Glosario puede definir estos términos conceptualmente y marcar su fórmula exacta como "pendiente de `docs/09`", en lugar de inventarla.
- **Prioridad:** Alta.

## GR-005 — Regla de sincronización entre `CHANGELOG.md` y `docs/11-Versiones.md`

- **Objetivo:** Documentar explícitamente (probablemente como una sección nueva dentro de `docs/11-Versiones.md`) que cada entrada de ese documento debe corresponder a una versión cortada en `CHANGELOG.md`, y decidir si se corta formalmente una primera versión real (ej. `1.1.0`) que consolide las misiones `MS-002` a `AR-001` ya completadas.
- **Documentos afectados:** `docs/11-Versiones.md`, `CHANGELOG.md`.
- **Dependencias:** Ninguna.
- **Prioridad:** Media.

## GR-006 — Ampliación de `MR-006` (ya definida por AR-001) para los 6 archivos de `.claude/agents/`

- **Objetivo:** Aplicar la tabla de "conocimiento mínimo obligatorio" diseñada en la sección 6 de este documento a los 6 archivos de agentes (no solo `statistician.md`, como preveía `MR-001` originalmente).
- **Documentos afectados:** los 6 archivos de `.claude/agents/`.
- **Dependencias:** `MR-002`, `MR-003` (para que los documentos que los agentes referencian ya estén reconciliados).
- **Prioridad:** Alta. **Nota:** esta misión no crea una entrada `GR-` duplicada de `MR-006` — se remite explícitamente a `MR-006`, ampliado según el detalle de esta sección, para evitar que dos misiones de dos series distintas reconcilien el mismo conjunto de archivos.

## GR-007 — Resolución de la ambigüedad de identidad "Arquitecto Estadístico"

- **Objetivo:** Aclarar en `CLAUDE.md` y/o `docs/06-Flujo-Operacional.md` si "Arquitecto Estadístico" designa al usuario humano, al asistente de IA, o a ambos según el contexto — y, en particular, confirmar explícitamente que la aprobación de cambios de peso (Fase 9 de `docs/06`) requiere una decisión humana real, no una autoaprobación del asistente que en un momento dado actúa "como" Arquitecto Estadístico.
- **Documentos afectados:** `CLAUDE.md`, `docs/06-Flujo-Operacional.md`.
- **Dependencias:** Ninguna.
- **Prioridad:** Alta — toca directamente el control humano sobre cambios de peso, el riesgo de mayor severidad conceptual de todo el inventario de gobernanza.

---

# 9. Riesgos de no corregir la gobernanza antes de implementar

| Riesgo | Consecuencia |
|---|---|
| No resolver INC-18 (Orden de Lectura desactualizado) | Cualquier sesión futura (humana o de IA) seguirá `CLAUDE.md` literalmente y nunca llegará a leer `docs/14-19` por su propia cuenta — perpetuando indefinidamente el resto de inconsistencias del Engine, porque la causa raíz (desconocimiento) nunca se corrige |
| No resolver INC-13/GR-006 (agentes sin conocimiento de la Capa) | El `predictor.md` seguirá invocando el Engine sin saber que existe un contrato de variables — el primer código que se escriba sobre este agente heredará el acoplamiento directo a `data/processed/` que todo el diseño reciente buscaba eliminar |
| No resolver INC-20 (ambigüedad "Arquitecto Estadístico") | Riesgo de que un cambio de peso se autoapruebe sin control humano genuino — es el riesgo más severo de todos porque toca directamente la regla más repetida de `CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística" |
| No resolver INC-15 (Glosario vacío) | Cada nueva misión seguirá inventando su propia forma de explicar "confianza" o "caos" sin una referencia común, incrementando el riesgo de definiciones sutilmente inconsistentes entre documentos nuevos |
| No resolver INC-17 (dos versionados) | Imposibilidad de responder con una única fuente de verdad "qué versión del modelo generó esta predicción", un riesgo directo para cualquier auditoría externa futura |
| Posponer todo el roadmap de gobernanza indefinidamente | Cada misión nueva (`MS-`, `MR-`, `AR-`) seguirá creciendo sobre una base de gobernanza que no se sincroniza sola — el costo de reconciliar crece con cada documento nuevo, igual que ya se observó en el Engine (`docs/18`, sección "Riesgos") |

---

# 10. Veredicto

**La gobernanza documental no está completamente preparada para soportar el crecimiento del Modelo Santiago, pero el motivo no es un defecto de diseño — es la ausencia de un mecanismo de sincronización hacia los documentos de mayor nivel.**

Justificación técnica: los componentes de gobernanza que sí tienen un mecanismo de actualización obligatorio y verificado (`CHANGELOG.md`, `docs/00-Project-Tracker.md`) han demostrado, a lo largo de 19 misiones consecutivas, que funcionan correctamente y escalan bien. Los componentes que **no** tienen ese mecanismo (`CLAUDE.md`, `README.md`, `data/README.md`, `docs/13-Glosario.md`, `.claude/agents/`) son precisamente los que acumularon las 9 inconsistencias de gobernanza detectadas (INC-12, 13, 15, 17, 18, 19, 20). La solución, por tanto, no requiere rediseñar la gobernanza desde cero — requiere ejecutar el roadmap de esta sección (GR-002 a GR-007) y, más importante a largo plazo, **definir un mecanismo de sincronización obligatorio** (por ejemplo, que toda misión que agregue un documento a `docs/` deba, como parte de su propio checklist de cierre, evaluar si `CLAUDE.md`/`README.md` necesitan actualizarse) — de modo que esta clase de deuda no vuelva a acumularse en las próximas 19 misiones.

---

# Diagramas

## Jerarquía documental oficial

```
Nivel 1 — Gobierna:               CLAUDE.md
Nivel 2 — Rige el proceso:        docs/00-Project-Tracker.md
Nivel 3 — Arquitectura funcional: docs/01 … docs/19  (docs/13-Glosario.md, transversal)
Nivel 4 — Investiga y respalda:   models/
Nivel 5 — Implementa la lógica:   engine/
Nivel 6 — Almacena el conocimiento: data/ (incl. data/README.md)
Nivel 7 — Dispara tareas:         prompts/
Nivel 8 — Ejecuta especializado:  .claude/agents/

Fuera de la jerarquía (no prevalecen en conflicto): README.md, CHANGELOG.md
```

## Mapa de dependencias documentales

```
CLAUDE.md
   │
   ├──► docs/00-Project-Tracker.md
   ├──► README.md ──► (debería reflejar) docs/01-19
   ├──► docs/01-19 ──► docs/13-Glosario.md (vocabulario compartido)
   │        │
   │        ├──► models/ ──► engine/
   │        │
   │        └──► data/README.md ──► data/
   │
   ├──► prompts/ ──► (dispara) .claude/agents/
   │
   └──► .claude/agents/ ──► (deberían conocer) docs/15, 16, 17
              │
              ▼
        CHANGELOG.md + docs/00-Project-Tracker.md (registro posterior)
```

## Mapa de autoridad (quién prevalece en un conflicto)

```
CLAUDE.md  >  docs/00-Project-Tracker.md  >  docs/01-19  >  models/  >  engine/  >  data/  >  prompts/  >  .claude/agents/

README.md      nunca prevalece sobre ningún docs/NN (es un resumen derivado)
CHANGELOG.md   nunca prevalece — es histórico, no prescriptivo

Dentro de docs/01-19: el documento más específico y reciente sobre un punto exacto
                       prevalece sobre el más general y antiguo
                       (ej. docs/15 > docs/06 en materia de cómo el Engine consume datos)
```

## Flujo de consulta documental

*(Ver sección 5 — diagrama completo ya presentado allí, no se repite.)*

---

# Observaciones del Consejo de Gobernanza

1. **La causa raíz de casi todas las inconsistencias de gobernanza (INC-12, 13, 18) es la misma**: documentos escritos antes de MS-008 nunca se sincronizaron hacia adelante, por la misma regla de alcance ("no modificar documentos existentes") que cada misión respetó correctamente. Esto no es un fallo de ejecución — es una consecuencia matemática de tener 19 misiones consecutivas, cada una con la restricción de no tocar lo anterior, sin que ninguna tuviera como objetivo explícito la sincronización hacia atrás. Se recomienda que, a partir de ahora, exista una categoría de misión periódica (no solo reactiva, como `MR-`/`AR-`/`GR-`) dedicada exclusivamente a sincronizar documentos de gobierno cada cierto número de misiones de diseño — por ejemplo, cada 5 misiones `MS-`.
2. **El hallazgo INC-20 (identidad de "Arquitecto Estadístico") es, en la valoración de este Consejo, el de mayor importancia conceptual de todo el inventario acumulado (Engine + gobernanza), aunque no el de mayor urgencia inmediata** (todavía no existe una propuesta real de `learning/weight-adjustment.md` que active el riesgo). Se recomienda resolverlo (`GR-007`) con prioridad alta antes de que el módulo `learning/` produzca su primera propuesta real, no después.
3. **El propio proceso de escalar el perímetro de auditoría en cada misión sucesiva (MS-009 → MS-010 → MR-001 → AR-001 → GR-001) es, en sí mismo, la mejor evidencia de que la gobernanza del proyecto funciona a nivel de *proceso*, incluso cuando falla a nivel de *sincronización de contenido*.** Ninguna de las cinco misiones de revisión tuvo que inventar un mecanismo nuevo para producir su hallazgo — todas usaron el mismo patrón (leer todo, comparar, no modificar, proponer roadmap) que ya estaba implícitamente establecido desde MR-001. Vale la pena que una futura versión de `CLAUDE.md` (cuando se ejecute `GR-002`) formalice este patrón como el procedimiento oficial de auditoría del proyecto.
4. **No se detectó ninguna inconsistencia de gobernanza en `prompts/`** — los 4 archivos son consistentes entre sí y con su propósito declarado ("nunca contienen lógica del modelo"). Es, junto con `models/` (ya señalado por AR-001), de los directorios más internamente sólidos del proyecto.

---

# Fuera de alcance de esta misión

- No se modifica ningún documento existente.
- No se reconcilia todavía ninguna inconsistencia — solo se planifica su reconciliación futura (`GR-002` a `GR-007`).
- No se redefine arquitectura, motores, variables, algoritmo ni pesos.
- No se actualizan agentes, `CLAUDE.md`, `README.md`, el Glosario ni el sistema de versionado.

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| 1. Estado actual | Sección 1 |
| 2. Inventario | Sección 2 |
| 3. Inconsistencias | Sección 3 |
| 4. Autoridad documental | Sección 4 |
| 5. Flujo documental | Sección 5 |
| 6. Gobernanza de agentes | Sección 6 |
| 7. Versionado | Sección 7 |
| 8. Roadmap | Sección 8 |
| 9. Riesgos | Sección 9 |
| 10. Veredicto | Sección 10 |

---

Fin del documento.
