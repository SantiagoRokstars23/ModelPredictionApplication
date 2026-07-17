# Constitución del Modelo Santiago

**Archivo:** `docs/21-Constitucion-del-Modelo-Santiago.md`

**Misión:** GOV-001 — Constitución del Modelo Santiago

**Versión:** 1.0.0

**Estado:** Activa — máxima referencia conceptual del proyecto

---

## Preámbulo

Este documento consolida, en un único lugar estable, los principios que ya gobernaban al Modelo Santiago de forma implícita o dispersa entre `CLAUDE.md`, `README.md` y los 20 documentos de `docs/`. No sustituye a ninguno de ellos: `CLAUDE.md` sigue gobernando el comportamiento operativo día a día; `README.md` sigue siendo el mapa de navegación; la arquitectura, el Engine, las Variables y los Algoritmos siguen siendo la especificación técnica vigente. La Constitución es la fuente de principios de la que todos ellos deben poder derivarse sin contradicción — no un documento que compite por su mismo rol.

Su naturaleza es deliberadamente distinta a la del resto del proyecto: mientras `docs/01` a `docs/20` han cambiado en cada una de las 20 misiones anteriores, esta Constitución debe permanecer estable durante toda la vida del proyecto. Solo debe modificarse ante un cambio fundamental de propósito, nunca para acomodar una decisión técnica puntual (Artículo 12).

---

## Artículo 1 — Propósito

El Modelo Santiago existe para generar predicciones probabilísticas de fútbol que sean **explicables, auditables y rentables a largo plazo**. No existe para adivinar resultados ni para justificar apuestas por intuición. El éxito del proyecto se mide por la calidad y consistencia de sus probabilidades, nunca por el acierto aislado de un marcador.

---

## Artículo 2 — Principios fundamentales

1. **Objetividad.** Ninguna probabilidad se genera sin datos verificables que la respalden.
2. **Trazabilidad.** Toda predicción y todo cambio del modelo debe poder reconstruirse hasta su origen.
3. **Reproducibilidad.** Las mismas entradas deben producir siempre el mismo resultado.
4. **Transparencia.** Toda decisión del modelo debe poder explicarse; el proyecto no admite cajas negras.
5. **Evidencia antes que opinión.** Ningún peso, variable o fórmula cambia sin evidencia estadística que lo justifique.
6. **Separación de responsabilidades.** Cada componente del proyecto tiene una única función; ninguno asume la responsabilidad de otro.
7. **Desarrollo incremental.** Ningún módulo se construye completo en su primera versión; el proyecto avanza por iteraciones auditables.
8. **Preservación de la historia.** Ninguna evidencia, predicción o resultado histórico se elimina, aunque haya quedado obsoleto.
9. **No autoaprobación.** Ninguna entidad puede aprobar, por sí sola, un cambio que ella misma propuso cuando ese cambio afecte pesos, variables o algoritmos (desarrollado en el Artículo 5).
10. **Autocrítica institucionalizada** *(principio nuevo, propuesto en esta misión — ver justificación más abajo)*.

> **Justificación del Principio 10:** el proyecto ya practica este principio desde hace varias misiones (`MS-009` y `MS-010` se auditaron entre sí con métodos independientes; `MR-001` auditó el Engine; `AR-001` auditó a `MR-001` intentando activamente refutarlo; `GR-001` auditó la gobernanza) — pero nunca se había declarado como una regla explícita, solo como un patrón repetido. Es atemporal, aplica a todo el proyecto y no contradice nada existente: solo nombra una práctica que el proyecto ya demostró que funciona. Se eleva aquí a principio constitucional para que no se pierda cuando el proyecto crezca y ya no quede memoria de por qué se auditaba dos veces cada hallazgo.

---

## Artículo 3 — Jerarquía documental

La autoridad del proyecto se organiza en niveles (consolidado de `docs/20-Plan-de-Reconciliacion-de-Gobernanza-Documental.md`, sin repetir su detalle operativo):

**Constitución (este documento) → `CLAUDE.md` (gobierna el comportamiento operativo) → Estado del proyecto (`docs/00-Project-Tracker.md`) → Arquitectura funcional (`docs/01-20`) → Investigación y ejecución (`models/`, `engine/`) → Base de Conocimiento (`data/`) → Activación de tareas (`prompts/`) → Ejecución especializada (`.claude/agents/`).**

`README.md` y `CHANGELOG.md` nunca prevalecen en un conflicto: son, respectivamente, un resumen navegacional y una bitácora histórica, no fuentes prescriptivas.

**Regla de conflicto:** prevalece el documento de menor nivel numérico; dentro de un mismo nivel, prevalece el más específico y reciente sobre el punto exacto en disputa. Ningún documento de un nivel inferior puede contradecir a uno superior; si lo hace, es una inconsistencia a reconciliar (`MR-`/`AR-`/`GR-`), nunca una excepción válida.

---

## Artículo 4 — Propiedad de conceptos

Todo concepto transversal del proyecto (ej. Variable, Confianza, Índice de Caos, ROI) debe tener **un único propietario documental explícito**. Ningún otro documento puede redefinirlo — solo puede remitir a su propietario. Cuando un concepto se usa repetidamente sin que exista ese propietario (el caso ya detectado de `docs/13-Glosario.md`, `docs/20` INC-15), el proyecto reconoce una deuda pendiente, no una definición implícita válida por repetición.

---

## Artículo 5 — Gobernanza

El proyecto reconoce tres roles, deliberadamente distintos entre sí:

| Rol | Responsabilidad | Nunca puede |
|---|---|---|
| **Arquitecto Estadístico IA** | Diseñar, documentar, auditar y proponer cambios de arquitectura, variables o pesos, con evidencia | Aprobar por sí mismo un cambio que afecte pesos, variables o algoritmos |
| **Arquitecto Estadístico Humano** | Revisar y aprobar o rechazar explícitamente toda propuesta de cambio que afecte pesos, variables o algoritmos | Delegar esa aprobación de vuelta al Arquitecto Estadístico IA |
| **Product Owner** | Definir el alcance y la prioridad de las misiones (qué se ejecuta y cuándo) | Aprobar por sí solo un cambio matemático sin el Arquitecto Estadístico Humano, aunque sea la misma persona en distinto rol funcional |

Este artículo resuelve, a nivel de **principio**, la ambigüedad identificada como `INC-20` en `docs/20` (`GR-001`): el rol de "Arquitecto Estadístico" que `CLAUDE.md` asigna al asistente de IA nunca incluye la potestad de autoaprobar un cambio de peso — esa potestad pertenece siempre y exclusivamente al Arquitecto Estadístico Humano. La aplicación concreta de este principio al texto de `CLAUDE.md` y `docs/06-Flujo-Operacional.md` sigue siendo responsabilidad de una futura misión de reconciliación (`GR-007`), no de esta Constitución.

---

## Artículo 6 — Gestión de cambios

Ningún cambio de arquitectura, modelo, fórmula matemática, variable o motor se aplica sin que, antes:

1. Exista evidencia que lo respalde.
2. Exista documentación previa en el nivel correspondiente (`models/` antes que `engine/`; `docs/` antes que su implementación — nunca al revés).
3. Cuando el cambio afecte pesos, variables o algoritmos, exista aprobación explícita del Arquitecto Estadístico Humano (Artículo 5).

Toda nueva variable o motor debe, además, justificar su propia existencia antes de incorporarse (principio ya vigente en el proyecto desde `MS-001`). Este artículo no define procedimientos — el "cómo" de cada paso pertenece a `docs/06-Flujo-Operacional.md` y a los documentos de arquitectura correspondientes.

---

## Artículo 7 — Resolución de conflictos

Ante una contradicción entre dos documentos, se aplica la jerarquía del Artículo 3. Ninguna contradicción se resuelve por conveniencia, por omisión, o "quedándose" con la interpretación más cómoda para la tarea en curso. Toda contradicción detectada debe **documentarse explícitamente** (como ya lo hicieron `MR-001`, `AR-001` y `GR-001`) hasta que una misión de reconciliación la resuelva formalmente — nunca ocultarse ni ignorarse silenciosamente.

---

## Artículo 8 — Trazabilidad

Todo cambio relevante del proyecto —de una variable, un peso, una regla, o un documento de gobierno— debe poder reconstruirse desde la evidencia que lo originó hasta el documento donde se aplicó, sin excepción y sin importar si el cambio lo originó un humano o el Arquitecto Estadístico IA.

---

## Artículo 9 — Versionado

El proyecto reconoce dos dimensiones de versión, deliberadamente distintas: la **versión técnica** del repositorio (qué documentos o código cambiaron) y la **versión narrativa** del comportamiento predictivo del modelo (qué significa ese cambio para sus predicciones). Ambas deben poder rastrearse la una a la otra en todo momento; ninguna evoluciona como un sistema aislado sin relación declarada con la otra. Este artículo no define el procedimiento exacto de sincronización — eso corresponde a `docs/11-Versiones.md`, `CHANGELOG.md` y a la misión `GR-005` ya prevista para reconciliarlos.

---

## Artículo 10 — Implementación

Ningún componente del Modelo Santiago puede pasar de diseño a implementación de código mientras existan, en su cadena de gobernanza inmediata, inconsistencias documentadas de gravedad Crítica sin resolver — principio ya demostrado operativamente por los veredictos de `MR-001` y `AR-001`. Las condiciones mínimas para considerar iniciada la implementación de cualquier componente son: (a) ausencia de contradicciones activas de gravedad Crítica sobre ese componente; (b) existencia de un contrato de datos/variables definido para lo que ese componente consume o produce; (c) una línea de aprobación humana clara para cualquier cambio de peso que ese componente pueda originar.

---

## Artículo 11 — Calidad

Ninguna decisión importante del modelo —una variable, un peso, un motor, una predicción— puede tomarse sin evidencia suficiente. Ante evidencia insuficiente, la única respuesta válida es declarar esa insuficiencia de forma explícita; nunca estimarla, inventarla, ni sustituirla por un valor por defecto.

---

## Artículo 12 — Evolución

El Modelo Santiago puede cambiar de tecnología, estructura de datos, motores matemáticos o infraestructura sin perder coherencia, siempre que todo cambio permanezca compatible con esta Constitución. La Constitución misma es la parte del proyecto que debe cambiar con menor frecuencia: solo debe modificarse ante una revisión fundamental del propósito o de los principios del Artículo 2, nunca para justificar o acomodar una decisión técnica puntual.

---

# Cierre obligatorio

**1. ¿Qué problema resolvió esta misión?**
Consolidó en un único documento, estable y de máxima autoridad conceptual, los principios que hasta ahora existían solo de forma implícita o dispersa entre `CLAUDE.md` y los 20 documentos previos de `docs/` — sin duplicar su contenido técnico, solo elevando sus principios subyacentes a un nivel que no cambiará con cada misión de diseño futura.

**2. ¿Qué nuevos hallazgos encontró?**
El hallazgo principal no fue una contradicción, sino una **ausencia de articulación**: el proyecto ya practicaba la autocrítica institucionalizada (`MS-009` → `MS-010` → `MR-001` → `AR-001` → `GR-001`) y el principio de no autoaprobación (implícito en la "revisión humana obligatoria" de `docs/06`, Fase 9) sin haberlos declarado nunca como principios explícitos. Se proponen aquí como el Principio 9 y el Principio 10 del Artículo 2, justificados por ser atemporales, aplicables a todo el proyecto, y no contradecir nada existente — solo nombran prácticas ya demostradas.

**3. ¿Qué documentos podrían necesitar adaptación futura para alinearse con la Constitución (sin modificarlos aquí)?**

- `CLAUDE.md` — para incorporar explícitamente la distinción de roles del Artículo 5 (ya recomendado como `GR-007`).
- `docs/06-Flujo-Operacional.md` — misma razón, en su Fase 9.
- `docs/13-Glosario.md` — para asumir formalmente el rol de propietario único de conceptos del Artículo 4 (ya recomendado como `GR-004`).
- `docs/11-Versiones.md` y `CHANGELOG.md` — para reflejar la distinción de dos dimensiones de versión del Artículo 9 (ya recomendado como `GR-005`).
- `README.md` — para reflejar, en su tabla de navegación, la existencia de esta Constitución como el documento de mayor autoridad conceptual (ya parte del alcance más amplio de `GR-002`).

Ninguna de estas adaptaciones se realiza en esta misión.

**4. ¿Cómo afecta esta misión al Índice de Madurez Arquitectónica (IMA)?**
No existe todavía, en ningún documento del proyecto, una definición formal de un "Índice de Madurez Arquitectónica" — esta misión no inventa esa métrica, por no estar dentro de su alcance ("crear un nuevo documento", no "definir un índice nuevo"). En términos cualitativos: esta misión no cambia la madurez del Engine (ya evaluada por `MR-001`) ni la de la gobernanza operativa (ya evaluada por `GR-001`) — añade una tercera dimensión de madurez, la **constitucional**, que antes no existía en absoluto (no había ningún documento de principios estables) y que ahora queda cubierta. Si en el futuro se formaliza un IMA real, esta Constitución debería ser uno de sus componentes de entrada, no un resultado que ese índice mida.

---

# Fuera de alcance de esta misión

- No se modifica ningún documento existente.
- No se reconcilia ninguna inconsistencia — los artículos remiten a las misiones `GR-004`, `GR-005` y `GR-007` ya previstas para su aplicación concreta.
- No se redefine arquitectura, motores, variables, algoritmos ni pesos.
- No se define un Índice de Madurez Arquitectónica formal.

---

Fin del documento.
