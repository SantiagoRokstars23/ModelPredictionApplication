# Plan Oficial de Reconciliación Arquitectónica del Engine

**Archivo:** `docs/18-Plan-de-Reconciliacion-Arquitectonica.md`

**Misión:** MR-001 — Reconciliación Arquitectónica del Engine (Architecture Review Board)

**Versión:** 1.0.0

**Estado:** Fotografía objetiva del estado arquitectónico — sin modificaciones aplicadas

---

# Objetivo

Este documento actúa como el informe oficial de un **Architecture Review Board** sobre el Engine del Modelo Santiago. No modifica ningún documento existente. Su único propósito es responder, con evidencia verificable línea por línea, qué inconsistencias existen entre `docs/02` a `docs/17` y `engine/01-06`, por qué existen, cuál debería ser la solución arquitectónica de cada una, y en qué orden deberían resolverse en misiones futuras — y, con eso, emitir un veredicto sobre si el Engine está listo para pasar a implementación.

Este documento se convierte en la referencia oficial para toda futura misión de reconciliación (prefijo `MR-`, distinto del prefijo `MS-` usado para misiones de diseño).

---

# Metodología de esta revisión

Se releyó íntegramente cada uno de los documentos listados en la misión (`docs/02` a `docs/06`, `docs/14` a `docs/17`, y los 6 archivos de `engine/`), y se verificó con `grep` exacto cada referencia cruzada de `engine/` (nombre de archivo citado vs. nombre de archivo real), en lugar de repetir de memoria lo ya señalado en las "Observaciones del Arquitecto" de MS-008, MS-009 y MS-010. Esto permitió confirmar los hallazgos previos, precisarlos con evidencia de línea exacta, y detectar dos inconsistencias que ninguna misión anterior había registrado explícitamente (INC-01, INC-02, ver inventario).

---

# 1. Inventario de inconsistencias

## INC-01 — `docs/06-Flujo-Operacional.md` (Fase 3) contradice textualmente a `docs/15-Capa-de-Preparacion-de-Variables.md`

**Descripción:** `docs/06-Flujo-Operacional.md`, Fase 3, afirma literalmente: *"`engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` — consumen únicamente `data/processed/`"*. `docs/15-Capa-de-Preparacion-de-Variables.md` establece como principio central que los motores **nunca** deben acceder directamente a la Base de Conocimiento — solo a variables ya preparadas. Son dos afirmaciones activas y mutuamente excluyentes sobre el mismo punto del flujo.

**Documentos involucrados:** `docs/06-Flujo-Operacional.md`, `docs/15-Capa-de-Preparacion-de-Variables.md`.
**Gravedad:** Crítica.
**Impacto:** Un lector que implemente siguiendo solo `docs/06` reproduciría exactamente el acoplamiento que `docs/15` fue diseñado para eliminar.
**Riesgo:** Si se escribe código antes de reconciliar, se fija en la implementación una contradicción que hoy solo existe en el papel.
**Clasificación:** documental, arquitectónica, trazabilidad.

## INC-02 — `docs/14-Prediction-Pipeline.md` no menciona la Capa de Preparación de Variables

**Descripción:** La tabla "Orden de consulta de la Base de Conocimiento" (Etapa 2) describe el orden de lectura de los 11 CSV de `data/processed/selecciones-nacionales/` sin mencionar que, desde MS-008, esa lectura es responsabilidad de `docs/15`, no de los motores ni del Predictor directamente.
**Documentos:** `docs/14-Prediction-Pipeline.md`, `docs/15-Capa-de-Preparacion-de-Variables.md`.
**Gravedad:** Media.
**Impacto:** Menor que INC-01 — no es una contradicción activa (`docs/15` sí cita correctamente a `docs/14`), pero la referencia es unidireccional y puede confundir sobre quién ejecuta la lectura.
**Riesgo:** Ambigüedad de responsabilidad si se implementa sin revisar ambos documentos juntos.
**Clasificación:** documental, trazabilidad.

## INC-03 — Numeración interna cruzada e inconsistente en `engine/01` a `engine/06`

**Descripción (verificada con `grep`, evidencia exacta):**

| Archivo | Línea | Texto | Correcto según nombre real de archivo |
|---|---|---|---|
| `engine/01-Offensive-Strength.md` | 170 | `engine/04-Confidence.md` | Incorrecto — Confidence es `engine/05` |
| `engine/02-Defensive-Strength.md` | 171 | `engine/04-Confidence.md` | Incorrecto |
| `engine/03-Poisson.md` | 170 | `engine/04-Confidence.md` | Incorrecto |
| `engine/03-Poisson.md` | 171 | `engine/05-Chaos-Index.md` | Incorrecto — Chaos-Index es `engine/04` |
| `engine/04-Chaos-Index.md` | 3 (encabezado) | `engine/04-Chaos-Index.md` | **Correcto** |
| `engine/04-Chaos-Index.md` | 217 | `engine/05-Confidence.md` | **Correcto** |
| `engine/05-Confidence.md` | 3 (encabezado, autorreferencia) | `engine/04-Confidence.md` | Incorrecto — el propio archivo se nombra mal a sí mismo |
| `engine/05-Confidence.md` | 174 | `engine/05-Chaos-Index.md` | Incorrecto |
| `engine/06-Expected-Value.md` | 46-47 | `engine/04-Chaos-Index.md`, `engine/05-Confidence.md` | **Correcto** |

De seis motores, cuatro (`01`, `02`, `03`, `05`) contienen al menos una referencia cruzada incorrecta a Confidence/Chaos-Index; solo las referencias de `engine/04` y `engine/06` son correctas. Adicionalmente, `engine/04`, `engine/05` y `engine/06` referencian `engine/07-Bankroll-Engine.md` y/o `engine/08-Simulation.md`, inexistentes en el repositorio.

**Documentos:** `engine/01` a `engine/06`.
**Gravedad:** Alta.
**Impacto:** Ninguna referencia cruzada de `engine/` puede asumirse correcta sin verificarla contra el nombre real del archivo.
**Riesgo:** Una resolución automática de dependencias basada en este texto importaría el motor equivocado.
**Clasificación:** documental, lógica, trazabilidad, mantenibilidad.

## INC-04 — Cinco de las doce variables oficiales sin consumidor confirmado en `engine/`

**Descripción:** Variable005 (Compatibilidad Táctica, Nivel A), Variable008 (Calidad de Plantilla), Variable009 (Localía), Variable010 (Historial Directo) y Variable011 (Estado Psicológico) no tienen un motor que las cite por su nombre oficial (MS-009, confirmado independientemente en MS-010). De estas, 008/009/010 son huérfanas confirmadas sin ambigüedad; 005/011 tienen solapamiento textual ambiguo con `engine/04`/`engine/05` ("cambios tácticos relevantes", "cambios recientes de entrenador") pero sin cita explícita.
**Documentos:** `docs/02-modelo.md`, `docs/03-Variables.md`, `docs/16-Contrato-Oficial-de-Variables.md`, `docs/17-Matriz-de-Consumo-de-Variables.md`, `engine/01` a `06`.
**Gravedad:** Crítica para Variable005 (única huérfana de Nivel A); Media para 008/009/010; Media-Baja para 011.
**Impacto:** Riesgo de que variables consideradas importantes en el diseño conceptual nunca se traduzcan en un cálculo real.
**Riesgo:** Implementar el Engine tal como está documentado dejaría a Variable005 sin ningún efecto en la predicción pese a su Nivel A declarado.
**Clasificación:** lógica, trazabilidad, arquitectónica.

## INC-05 — `engine/06-Expected-Value.md` consume `cuotas.csv` directamente de la Base de Conocimiento

**Descripción:** Es el único motor con acceso documentado y directo a `data/processed/` (`docs/14-Prediction-Pipeline.md` ya lo confirma), sin pasar por la Capa de Preparación de Variables ni por el Contrato Oficial de Variables (MS-010).
**Documentos:** `docs/14`, `docs/15`, `docs/16`, `engine/06`.
**Gravedad:** Crítica.
**Impacto:** Rompe, en al menos un punto documentado, la promesa central de `docs/15` ("los motores nunca deben conocer si los datos provienen de CSV").
**Riesgo:** Si cambia el proveedor de cuotas en el futuro, habría que modificar `engine/06` directamente — exactamente el problema que la Capa fue diseñada para evitar en el resto del sistema.
**Clasificación:** arquitectónica, lógica, escalabilidad.

## INC-06 — Duplicación de la señal "Rotaciones" en cuatro motores independientes

**Descripción:** `engine/01`, `02`, `04` y `05` listan "Rotaciones" (y, de forma relacionada, "Fatiga"/"Lesiones") como entrada contextual propia, sin una fuente única.
**Documentos:** `engine/01`, `02`, `04`, `05`; `docs/15`, `docs/17`.
**Gravedad:** Alta.
**Impacto:** Riesgo de que, al implementarse, cada motor derive "rotaciones" de forma ligeramente distinta.
**Riesgo:** Inconsistencia silenciosa entre motores, difícil de detectar sin pruebas cruzadas explícitas.
**Clasificación:** mantenibilidad, lógica, arquitectónica.

## INC-07 — Etiquetas inconsistentes entre `docs/02-modelo.md` ("xG"/"xGA") y `docs/03-Variables.md` (Variable003/004)

**Descripción:** Mismo concepto, nombres distintos entre dos documentos (`docs/02-modelo.md` los llama "xG"/"xGA" en su Nivel A; `docs/03-Variables.md` los llama "Potencial Ofensivo"/"Solidez Defensiva").
**Documentos:** `docs/02-modelo.md`, `docs/03-Variables.md`.
**Gravedad:** Media.
**Impacto:** Posible confusión de un lector nuevo; sin efecto funcional — la trazabilidad real vía `engine/01`/`engine/02` es correcta.
**Clasificación:** documental, trazabilidad.

## INC-08 — Variable011 (Estado Psicológico) sin clasificación de Nivel en `docs/02-modelo.md`

**Descripción:** Es la única de las 12 variables sin nivel de importancia asignado (Nivel A-D).
**Documentos:** `docs/02-modelo.md`, `docs/03-Variables.md`.
**Gravedad:** Media.
**Impacto:** No puede evaluarse si su utilización real (ninguna, hoy) es consistente con su importancia declarada, porque no existe una importancia declarada con la que comparar.
**Clasificación:** documental, lógica.

## INC-09 — Variable006 tiene una utilización real más amplia que su Nivel B declarado

**Descripción:** Es la variable con más consumidores directos confirmados (4 de 6 motores) pese a estar clasificada en un nivel intermedio (Nivel B, no Nivel A).
**Documentos:** `docs/02-modelo.md`, `docs/17-Matriz-de-Consumo-de-Variables.md`.
**Gravedad:** Baja.
**Impacto:** Ninguno funcional inmediato; oportunidad de revisión, no un error.
**Clasificación:** lógica, trazabilidad.

## INC-10 — Rangos/tipos de las 12 variables (`docs/16`) son una propuesta arquitectónica, no una validación estadística

**Descripción:** `docs/03-Variables.md` dejaba las 12 variables con "Escala: Pendiente"; `docs/16-Contrato-Oficial-de-Variables.md` fue la primera propuesta formal, ya señalada en su propio texto como sujeta a ajuste cuando `models/` desarrolle el método de cálculo real.
**Documentos:** `docs/03-Variables.md`, `docs/16-Contrato-Oficial-de-Variables.md`, `models/` (pendiente).
**Gravedad:** Baja — ya gestionado transparentemente en su propio documento.
**Impacto:** Ninguno si se respeta la sección "Versionado" de `docs/16` al momento del ajuste.
**Clasificación:** mantenibilidad, escalabilidad.

## INC-11 — `.claude/agents/statistician.md` no menciona la frontera con la Capa de Preparación de Variables

**Descripción:** El Statistician valida "suficiencia" (Fase 2, `docs/06`); la Capa valida "construcción" (`docs/15`, sección 6). Ambas validaciones son necesarias y no se solapan si se mantiene la distinción, pero el archivo del agente no la menciona.
**Documentos:** `.claude/agents/statistician.md`, `docs/15-Capa-de-Preparacion-de-Variables.md`.
**Gravedad:** Baja.
**Impacto:** Riesgo de interpretación ambigua sobre quién detiene el pipeline y en qué momento exacto.
**Clasificación:** documental, trazabilidad.

---

# 2. Clasificación consolidada

| Inconsistencia | Documental | Arquitectónica | Lógica | Trazabilidad | Mantenibilidad | Escalabilidad |
|---|---|---|---|---|---|---|
| INC-01 | ✓ | ✓ | | ✓ | | |
| INC-02 | ✓ | | | ✓ | | |
| INC-03 | ✓ | | ✓ | ✓ | ✓ | |
| INC-04 | | ✓ | ✓ | ✓ | | |
| INC-05 | | ✓ | ✓ | | | ✓ |
| INC-06 | | ✓ | ✓ | | ✓ | |
| INC-07 | ✓ | | | ✓ | | |
| INC-08 | ✓ | | ✓ | | | |
| INC-09 | | | ✓ | ✓ | | |
| INC-10 | | | | | ✓ | ✓ |
| INC-11 | ✓ | | | ✓ | | |

---

# 3. Causa raíz

Ninguna inconsistencia se atribuye a un error de una misión concreta — todas son consecuencia de decisiones de alcance ya explícitas y correctas en su momento ("No modificar documentos existentes"), aplicadas de forma consistente misión tras misión. Se agrupan en cuatro causas sistémicas:

1. **Evolución natural del proyecto (documentos escritos en momentos distintos).** INC-01, INC-02, INC-05, INC-07, INC-09 existen porque `docs/02`, `docs/04`, `docs/06` y `docs/14` se escribieron antes de que existieran `docs/15`, `docs/16` y `docs/17` — es imposible que un documento anticipe una arquitectura que todavía no se había diseñado.
2. **Responsabilidades no formalizadas hasta que una misión posterior las exigió.** INC-04, INC-08, INC-11 existen porque, hasta MS-008/MS-009/MS-010, no existía ningún mecanismo que verificara sistemáticamente que cada variable tuviera un consumidor, o que cada agente tuviera su frontera de responsabilidad explícita frente a una capa que aún no existía.
3. **Crecimiento incremental de `engine/` sin una convención de verificación cruzada.** INC-03 y INC-06 existen porque los 6 motores se documentaron como unidades autocontenidas, cada uno con su propia sección "Dependencias"/"Entradas" escrita de forma independiente, sin una revisión que comparara los seis documentos entre sí en el momento de crearlos.
4. **Desarrollo incremental deliberado (principio explícito del proyecto).** INC-10 no es un defecto sino una consecuencia intencional de `CLAUDE.md` ("Principio de Desarrollo Incremental": "ningún módulo deberá construirse completamente en su primera implementación").

---

# 4. Propuesta de reconciliación

| Inconsistencia | Documento(s) a modificar (futuro) | Documento(s) que NO deben modificarse | Orden recomendado | Riesgos de la corrección |
|---|---|---|---|---|
| INC-01 | `docs/06-Flujo-Operacional.md` (Fase 3, actualizar redacción) | `docs/15` (ya es correcto; no se toca) | Después de INC-03 (evitar tocar `engine/` y `docs/06` en la misma ventana de cambio) | Bajo — es un cambio de redacción, no de arquitectura; riesgo principal es no actualizar también las referencias cruzadas en el resto de `docs/06` |
| INC-02 | `docs/14-Prediction-Pipeline.md` (Etapa 2, agregar referencia a `docs/15`) | `docs/15` | Junto con INC-01 | Bajo |
| INC-03 | `engine/01`, `02`, `03`, `05` (corregir referencias cruzadas) | `engine/04`, `engine/06` (ya son correctos) | Primero de todos — es aislado, no depende de ninguna otra reconciliación | Bajo, pero requiere verificar cada referencia con `grep` tras el cambio, no solo visualmente (mismo error que originó INC-03) |
| INC-04 | `engine/01` a `06` (declarar consumidor explícito de Variable005/008/009/010/011 o justificar por qué no participan) | `docs/03-Variables.md`, `docs/16`, `docs/17` (ya documentan correctamente el vacío; no se tocan) | Después de INC-03 (evita reescribir `engine/` dos veces) | Medio — requiere una decisión de diseño real (qué motor debería consumir cada variable huérfana), no solo un ajuste editorial |
| INC-05 | `engine/06-Expected-Value.md` y, posiblemente, `docs/16-Contrato-Oficial-de-Variables.md` (si se decide modelar cuotas como variable) | `docs/15` (el principio se mantiene; se corrige la excepción, no la regla) | Junto con INC-04 (misma ventana de cambio sobre `engine/`) | Medio-Alto — requiere decidir entre dos alternativas de diseño (ver Observaciones de MS-010), no es un ajuste trivial |
| INC-06 | `engine/01`, `02`, `04`, `05` (eliminar duplicación de "Rotaciones", delegar a la Capa) | `docs/15` | Junto con INC-04 | Bajo-Medio |
| INC-07 | `docs/02-modelo.md` o `docs/03-Variables.md` (agregar nota cruzada de equivalencia) | El otro de los dos (no se elige reescribir ambos) | Independiente, puede hacerse en cualquier momento | Muy bajo |
| INC-08 | `docs/02-modelo.md` (clasificar Variable011 en un Nivel) | `docs/03-Variables.md` | Después de INC-04 (para que la clasificación considere la utilización real ya decidida) | Bajo, pero requiere criterio explícito, no solo insertar el nombre en una lista |
| INC-09 | `docs/02-modelo.md` (revisar si Variable006 merece Nivel A) | `docs/17` (la trazabilidad ya es correcta) | Junto con INC-08 | Bajo |
| INC-10 | `docs/03-Variables.md`/`docs/16` (cuando `models/` respalde el método de cálculo) | Ninguno hasta entonces | Sin urgencia — depende de un trabajo de `models/` todavía no iniciado | Bajo si se sigue la sección "Versionado" de `docs/16` |
| INC-11 | `.claude/agents/statistician.md` | `docs/15` | Después de INC-01 (para alinear con el texto ya corregido de `docs/06`) | Muy bajo |

Ninguna de estas modificaciones se realiza en esta misión.

---

# 5. Mapa de dependencias (cómo una corrección afecta al resto)

```
INC-03 (numeración engine/)
   │
   ├──► habilita una corrección limpia de INC-04, INC-05, INC-06
   │      (evita reescribir engine/ dos veces)
   │
   ▼
INC-01 (docs/06 Fase 3) ──► habilita INC-11 (statistician.md, alineado a docs/06 ya corregido)
   │
   ▼
INC-02 (docs/14 Etapa 2)

INC-04 (variables huérfanas) ──► debe resolverse junto con INC-05 y INC-06
                                   (mismas secciones de engine/ se tocan)
   │
   ▼
INC-08 (Variable011 sin nivel) ──► se decide mejor después de INC-04
   │
   ▼
INC-09 (Variable006 subvalorada) ──► misma revisión de docs/02-modelo.md que INC-08

INC-07 (etiquetas xG) ──► independiente, sin dependencias

INC-10 (rangos sin validar) ──► depende de un trabajo externo (models/), no de otra inconsistencia
```

**Regla general del mapa:** ninguna corrección sobre `engine/` debería hacerse dos veces — INC-03, INC-04, INC-05 e INC-06 comparten los mismos archivos (`engine/01` a `06`) y deberían resolverse en una única ventana de cambio (ver "Roadmap de reconciliación").

---

# 6. Riesgos

| Escenario | Consecuencia |
|---|---|
| **No se corrige ninguna inconsistencia** | El diseño documental sigue siendo internamente contradictorio (INC-01) e incompleto (INC-04, INC-05). Mientras el proyecto permanezca en fase de documentación esto es tolerable (`CLAUDE.md`: desarrollo incremental); se vuelve inaceptable en el momento en que se escriba la primera línea de código sobre `engine/`. |
| **Se corrige, pero de forma incorrecta** | El riesgo más concreto es repetir el mismo error que originó INC-03: corregir una referencia cruzada "a mano" sin verificarla contra el nombre real del archivo, dejando una inconsistencia nueva en el lugar de la anterior. Por eso el Roadmap (sección 8) exige verificación con `grep` explícita, no solo revisión visual. |
| **Se pospone indefinidamente** | Cada misión nueva que amplíe `engine/` (variables adicionales, nuevos motores) parte de una base ya inconsistente, y el costo de reconciliar crece porque el número de referencias cruzadas a verificar aumenta con cada motor nuevo. Posponer no es gratis: es una deuda que crece con el tiempo, no que se mantiene estable. |

---

# 7. Priorización

| Inconsistencia | Prioridad | Justificación |
|---|---|---|
| INC-01 | **Crítica** | Contradicción activa entre dos documentos que gobiernan la ejecución del Engine; afecta a todo el flujo, no a un motor puntual |
| INC-04 (Variable005) | **Crítica** | Única variable Nivel A sin ningún consumidor — el nivel más alto de importancia declarado del proyecto, sin efecto real documentado |
| INC-05 | **Crítica** | Rompe el principio de desacoplamiento que es la razón de ser de `docs/15`, en un motor que además maneja dinero (Valor Esperado) |
| INC-03 | **Alta** | Afecta la confiabilidad de toda referencia cruzada de `engine/`; bloquea una reconciliación limpia de INC-04/05/06 |
| INC-02 | **Alta** | Mismo tipo de brecha que INC-01, pero sin contradicción activa (atenuante) |
| INC-06 | **Alta** | Duplicación real y ya evidenciada (4 motores), con riesgo concreto de inconsistencia de cálculo si se implementa tal cual |
| INC-07 | **Media** | Sin efecto funcional, solo claridad para nuevos lectores |
| INC-08 | **Media** | Afecta la calidad del diseño conceptual, no bloquea ninguna implementación por sí sola |
| INC-09 | **Media** | Es una observación de mejora, no un defecto |
| INC-10 | **Baja** | Ya gestionado transparentemente; su resolución depende de trabajo externo (`models/`) todavía no iniciado |
| INC-11 | **Baja** | Afecta un único agente, de bajo impacto operativo mientras no exista implementación |

---

# 8. Roadmap de reconciliación

## MR-002 — Corrección editorial de numeración interna de `engine/`

- **Objetivo:** Corregir las referencias cruzadas incorrectas identificadas en INC-03 (`engine/01`, `02`, `03`, `05`) y eliminar/marcar como pendientes las referencias a `engine/07-Bankroll-Engine.md`/`engine/08-Simulation.md` (inexistentes).
- **Documentos afectados:** `engine/01`, `02`, `03`, `05` (y verificación de `04`, `06`, que ya son correctos).
- **Riesgo:** Bajo — cambio puramente editorial, sin lógica ni fórmulas involucradas.
- **Dependencias:** Ninguna — puede ejecutarse de forma aislada y primero.

## MR-003 — Reconciliación de `docs/06-Flujo-Operacional.md` y `docs/14-Prediction-Pipeline.md` con la Capa de Preparación de Variables

- **Objetivo:** Actualizar la Fase 3 de `docs/06` (INC-01) y la Etapa 2 de `docs/14` (INC-02) para reflejar que los motores consumen variables preparadas por `docs/15`, nunca `data/processed/` directamente.
- **Documentos afectados:** `docs/06-Flujo-Operacional.md`, `docs/14-Prediction-Pipeline.md`.
- **Riesgo:** Bajo-Medio — riesgo principal es una actualización parcial que deje otras secciones de `docs/06`/`docs/14` sin alinear.
- **Dependencias:** Ninguna estricta con MR-002, pero se recomienda ejecutarla después para no abrir dos frentes de corrección (`engine/` y `docs/`) en paralelo.

## MR-004 — Cierre de huérfanas, desacoplamiento de cuotas y eliminación de duplicidad en `engine/`

- **Objetivo:** (a) Declarar consumidor explícito para Variable005, 008, 009, 010, 011 o documentar por qué deliberadamente no participan (INC-04); (b) decidir y aplicar el tratamiento de `cuotas.csv` en `engine/06` — variable oficial paralela o paso por la Capa (INC-05); (c) centralizar la señal "Rotaciones" (y contextuales relacionadas) en la Capa de Preparación de Variables, eliminando su re-derivación independiente en 4 motores (INC-06).
- **Documentos afectados:** `engine/01` a `06`, posiblemente `docs/16-Contrato-Oficial-de-Variables.md` (si se decide modelar cuotas como variable).
- **Riesgo:** Medio-Alto — es la única misión de este roadmap que involucra decisiones de diseño, no solo correcciones editoriales.
- **Dependencias:** MR-002 (referencias cruzadas ya correctas) y MR-003 (textos de flujo ya alineados).

## MR-005 — Reconciliación de `docs/02-modelo.md` con la utilización real de variables

- **Objetivo:** Clasificar a Variable011 en un Nivel A-D (INC-08); revisar si el Nivel B de Variable006 sigue siendo apropiado dado su uso real (INC-09); agregar nota cruzada de equivalencia terminológica xG/xGA ↔ Potencial Ofensivo/Solidez Defensiva (INC-07).
- **Documentos afectados:** `docs/02-modelo.md`, `docs/03-Variables.md` (solo nota cruzada, sin redefinir variables).
- **Riesgo:** Bajo.
- **Dependencias:** MR-004 (para que la clasificación considere el consumo real ya decidido, no el actual).

## MR-006 — Formalización de la frontera Statistician / Capa de Preparación de Variables

- **Objetivo:** Actualizar `.claude/agents/statistician.md` para declarar explícitamente la distinción entre validación de suficiencia (Statistician, Fase 2) y validación de construcción (Capa de Preparación de Variables, `docs/15`) — INC-11.
- **Documentos afectados:** `.claude/agents/statistician.md`.
- **Riesgo:** Muy bajo.
- **Dependencias:** MR-003 (para alinear con el texto ya corregido de `docs/06`).

*(INC-10 no genera una misión propia: se resuelve como consecuencia natural del trabajo futuro de `models/` sobre el método de cálculo de cada variable, ya previsto en el roadmap general del proyecto, no como una inconsistencia a reconciliar de forma aislada.)*

---

# 9. Estado de madurez del Engine

| Aspecto | Evaluación | Justificación |
|---|---|---|
| **Cohesión** | Media-Alta | Cada motor tiene un objetivo individual claro y acotado (`engine/01` a `06`), pero a nivel de conjunto existen señales redundantes (INC-06) y variables sin dueño claro (INC-04), lo que reduce la cohesión del sistema como un todo. |
| **Desacoplamiento** | Medio | El principio está bien diseñado (`docs/15`) y la mayoría de los motores lo respetan en su documentación, pero al menos uno (`engine/06`, INC-05) lo rompe de forma documentada, y dos documentos "flagship" (`docs/06`, `docs/14`) todavía describen el acoplamiento directo anterior (INC-01, INC-02). |
| **Mantenibilidad** | Media | INC-03 demuestra que referencias cruzadas manuales ya divergieron de forma silenciosa a través de varias misiones sin que ninguna revisión previa las detectara con precisión de línea — es evidencia directa de que el mecanismo actual de mantenimiento (revisión editorial manual) no escala bien conforme crece `engine/`. |
| **Escalabilidad** | Alta en diseño, condicionada en la práctica | `docs/15`/`docs/16` están explícitamente diseñados para tolerar cambios de infraestructura sin tocar motores — pero esa promesa depende de que INC-05 se resuelva antes de que cualquier motor dependa de una fuente de datos concreta. |
| **Consistencia documental** | Media-Baja | Once inconsistencias activas detectadas en esta única revisión, ninguna corregida todavía — resultado esperado y aceptado de un desarrollo incremental que priorizó completar el diseño antes de reconciliarlo (`CLAUDE.md`, "Principio de Desarrollo Incremental"), pero que ya alcanzó el punto en que reconciliar es más urgente que seguir diseñando. |
| **Preparación para implementación** | Baja-Media | El contrato de variables (`docs/16`) y la matriz de consumo (`docs/17`) son suficientes para empezar a diseñar código en abstracto, pero implementar literalmente el texto actual de `engine/` fijaría en código al menos tres contradicciones activas (INC-01, INC-04, INC-05). |

---

# 10. Veredicto

**El Engine del Modelo Santiago no está listo para pasar a la fase de implementación.**

No porque el diseño conceptual sea débil — al contrario, doce variables con contrato formal, una capa de desacoplamiento explícita y una matriz de trazabilidad completa son una base sólida, infrecuente en un proyecto en esta etapa. La razón es más específica: **implementar código directamente sobre el texto actual de `engine/` fijaría en código tres contradicciones activas que hoy solo existen en el papel** (INC-01, INC-04, INC-05), además de una fuente de bugs de integración concreta y ya evidenciada (INC-03).

**Condiciones mínimas antes de iniciar implementación** (en orden, ver Roadmap sección 8):

1. Resolver **MR-002** (numeración de `engine/`) — sin esto, cualquier desarrollador que siga las referencias cruzadas de "Dependencias" importaría el motor equivocado.
2. Resolver **MR-003** (alinear `docs/06`/`docs/14` con `docs/15`) — sin esto, dos documentos "fuente de verdad" del flujo siguen contradiciéndose.
3. Resolver **MR-004** (huérfanas, cuotas, duplicidad) — sin esto, Variable005 (Nivel A) nunca tendría efecto real, y `engine/06` fijaría un acoplamiento directo a la Base de Conocimiento.

MR-005 y MR-006 son deseables pero no bloqueantes — pueden ejecutarse en paralelo a los primeros pasos de una implementación mínima, siempre que esa implementación no dependa todavía de Variable011, Variable006 o del agente Statistician de forma crítica.

---

# Diagramas

## Mapa de dependencias entre documentos

```
docs/02-modelo.md ──────────────┐
        │                       │
        ▼                       │
docs/03-Variables.md            │ (Niveles A-D)
        │                       │
        ▼                       │
docs/04-Algoritmo.md            │
        │                       │
        ▼                       │
docs/05-Base-de-Conocimiento.md │
        │                       │
        ▼                       │
docs/06-Flujo-Operacional.md ◄──┘   ⚠ INC-01 (contradice a docs/15, Fase 3)
        │
        ▼
docs/14-Prediction-Pipeline.md      ⚠ INC-02 (no menciona a docs/15)
        │
        ▼
docs/15-Capa-de-Preparacion-de-Variables.md
        │
        ▼
docs/16-Contrato-Oficial-de-Variables.md
        │
        ▼
docs/17-Matriz-de-Consumo-de-Variables.md
        │
        ▼
docs/18-Plan-de-Reconciliacion-Arquitectonica.md  (este documento)
```

## Mapa de dependencias entre motores

```
Capa 1 (paralelo):
   engine/01-Offensive-Strength.md  ⚠ INC-03, INC-06
   engine/02-Defensive-Strength.md  ⚠ INC-03, INC-06
        │
        ▼
Capa 2:
   engine/03-Poisson.md             ⚠ INC-03
        │
        ▼
Capa 3 (paralelo):
   engine/04-Chaos-Index.md         ⚠ INC-06
   engine/05-Confidence.md          ⚠ INC-03 (autorreferencia incorrecta), INC-06
        │
        ▼
Capa 4:
   engine/06-Expected-Value.md      ⚠ INC-05 (único con acceso directo a data/processed/)
```

## Mapa de flujo de variables

```
Variable001, 002, 003, 004, 006, 007  ──► consumidas (directa o indirectamente por todos los motores)
Variable012                            ──► consumida por engine/04 (directa), engine/06 (indirecta)
Variable005, 011                       ──► consumo ambiguo, no confirmado (engine/04, engine/05)  ⚠ INC-04
Variable008, 009, 010                  ──► sin consumidor confirmado en ningún motor              ⚠ INC-04
```

## Mapa de inconsistencias detectadas

```
                docs/02 ───INC-07,INC-08,INC-09─── docs/03
                                                       │
docs/06 ───INC-01─── docs/15 ───INC-02─── docs/14      │
   │                    │                              │
   │                 INC-05                          docs/16 ───INC-04─── engine/01-06
   │                    │                              │              │
.claude/agents/    engine/06                        docs/17 ──────────┘
statistician.md ◄──INC-11                              │
                                                    INC-03 (referencias cruzadas internas)
                                                    INC-06 (duplicación "Rotaciones")
```

---

# Observaciones del Architecture Review Board

Más allá de las 11 inconsistencias formalmente inventariadas, esta revisión libre detecta lo siguiente:

1. **El proyecto ha desarrollado, sin proponérselo explícitamente, un patrón de "misión de síntesis" saludable.** MS-008 detectó una duplicación; MS-009 la retomó desde otro ángulo y la refinó; MS-010 la confirmó de forma independiente con un método inverso; esta misión (MR-001) la consolidó con evidencia de línea exacta. Cada misión no solo agregó diseño nuevo, sino que revisó y precisó lo anterior. Esto es exactamente el "Principio de Desarrollo Incremental" de `CLAUDE.md` funcionando como se esperaba — vale la pena preservarlo como práctica explícita para las misiones `MR-` futuras, en lugar de asumir que cada `MS-` debe limitarse a avanzar sin nunca revisar hacia atrás.
2. **No existe todavía una convención que distinga "MS-" (misión de diseño) de "MR-" (misión de reconciliación) en `docs/00-Project-Tracker.md`.** Esta es la primera misión con prefijo `MR-`; se recomienda que el Project Tracker incorpore explícitamente esta distinción (dos series de numeración independientes) para que futuras misiones de reconciliación no compitan por el mismo espacio de numeración que las misiones de diseño.
3. **El mecanismo que originó INC-03 (referencias cruzadas manuales sin verificación automatizada) es un riesgo estructural, no solo un incidente puntual.** Mientras el proyecto sea exclusivamente documental esto es barato de corregir (como en MR-002); en el momento en que exista código, un error equivalente sería un bug de importación real. Se sugiere que, cuando exista implementación, las referencias entre módulos de código se resuelvan por mecanismos del lenguaje (imports, tipos), no por texto libre en comentarios — de modo que este tipo de inconsistencia deje de ser posible por construcción, no solo por disciplina editorial.
4. **`docs/17-Matriz-de-Consumo-de-Variables.md` y `docs/16-Contrato-Oficial-de-Variables.md` fueron escritos por el mismo autor en misiones consecutivas y son mutuamente consistentes** (se verificó cruzando ambas tablas variable por variable) — no se detectó ninguna inconsistencia nueva entre ellos, lo cual sugiere que el proceso de "complementar sin duplicar" exigido en MS-009/MS-010 se aplicó correctamente.
5. **No se auditó `models/` en esta misión** porque no estaba en la lista de "Revisión obligatoria" de MR-001. Dado que `docs/16` y `docs/17` ya delegan expresamente en `models/` la validación estadística de rangos y el método de cálculo de cada variable, se recomienda que una futura misión de reconciliación (`MR-007` o posterior, después de que `models/` desarrolle contenido nuevo) verifique que las 6 investigaciones existentes (`models/poisson.md`, `models/elo.md`, etc.) sean consistentes con los tipos/rangos ya fijados en `docs/16` — esta misión no puede afirmar ni descartar que existan inconsistencias allí, porque no fue parte de su alcance.
6. **El propio Engine, tal como está documentado hoy, ya demuestra el valor de la Capa de Preparación de Variables sin necesidad de implementarla:** el hecho de que este análisis haya podido detectar con precisión qué motor usa qué variable (algo que antes de MS-008/009/010 hubiera requerido releer los 6 motores por separado) es evidencia indirecta de que formalizar el contrato ya mejoró la auditabilidad del proyecto, incluso antes de escribir una sola línea de código.

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se modifica ningún documento existente (`docs/02` a `docs/17`, `engine/01-06`, `.claude/agents/statistician.md`).
- No se crean nuevas variables ni nuevos motores.
- No se alteran pesos matemáticos ni el algoritmo.
- No se rediseña el pipeline.
- Las 11 inconsistencias inventariadas no se resuelven aquí — quedan asignadas al roadmap MR-002 a MR-006 para su resolución futura.

---

# Preguntas respondidas (trazabilidad con la misión)

| Pregunta | Respuesta (sección) |
|---|---|
| 1. Inventario de inconsistencias | Sección 1 |
| 2. Clasificación | Sección 2 |
| 3. Causa raíz | Sección 3 |
| 4. Propuesta de reconciliación | Sección 4 |
| 5. Dependencias | Sección 5 |
| 6. Riesgos | Sección 6 |
| 7. Priorización | Sección 7 |
| 8. Roadmap de reconciliación | Sección 8 |
| 9. Estado de madurez del Engine | Sección 9 |
| 10. Veredicto | Sección 10 |

---

Fin del documento.
