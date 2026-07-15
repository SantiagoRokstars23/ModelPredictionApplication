# Weight Adjustment

**Módulo:** `learning/weight-adjustment.md`

**Versión:** 1.0.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

Traducir la evidencia producida por `error-analysis.md`, `pattern-discovery.md` y `confidence-calibration.md` en una **propuesta documentada** de ajuste de peso para una o más variables del modelo (`docs/03-Variables.md`).

Es deliberadamente el único documento del pipeline que mira hacia una posible modificación del modelo — y por eso mismo es el que tiene el control más estricto: nunca aplica el cambio, solo lo propone.

---

# Responsabilidad

- Consolidar la evidencia de los tres documentos anteriores del pipeline en una propuesta concreta: qué variable, cuál es su peso actual, cuál sería el peso propuesto y por qué.
- Verificar que la propuesta cumple el `Principio de Justificación de Datos` (`docs/05-Base-de-Conocimiento.md`) y la regla de `CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística".
- Dejar explícito qué pasa si la propuesta **no** se aprueba (el peso actual se mantiene sin cambios; no hay aplicación parcial ni automática).

No modifica `docs/03-Variables.md` ni `engine/` directamente. La propuesta es un documento de salida que requiere revisión y aprobación explícita del Arquitecto Estadístico antes de convertirse en un cambio real.

---

# Entradas

- Reporte de `error-analysis.md` (casos individuales de error).
- Reporte de `pattern-discovery.md` (patrones recurrentes con evidencia estadística).
- Reporte de `confidence-calibration.md` (brechas de calibración atribuibles a variables concretas).
- `docs/03-Variables.md` (pesos y variables actuales).
- `prompts/recalibration-template.md` (plantilla ya existente para ejecutar esta tarea).

---

# Salidas

Una propuesta de ajuste con, como mínimo:

- Variable afectada.
- Peso actual vs. peso propuesto.
- Evidencia que respalda el cambio (referencia directa a los hallazgos de `pattern-discovery.md`/`confidence-calibration.md` que lo justifican).
- Impacto estimado en las métricas de auditoría (`docs/09-Auditoria.md`) si se aplicara.
- Estado de la propuesta: pendiente / aprobada / rechazada.

Una propuesta **aprobada** se convierte en la entrada de `version-history.md`, que es quien documenta el cambio ya aplicado a `docs/03-Variables.md`/`engine/`.

---

# Dependencias

- `error-analysis.md`, `pattern-discovery.md`, `confidence-calibration.md` (las tres son insumo obligatorio; una propuesta sin evidencia de al menos una de ellas se rechaza por diseño).
- `docs/03-Variables.md` (estado actual de pesos).
- `prompts/recalibration-template.md`.

---

# Cómo interactúa con el resto del Modelo Santiago

- Es el punto de cierre del análisis y el punto de partida de cualquier cambio real: su salida es revisada por `.claude/agents/statistician.md` y aprobada por el Arquitecto Estadístico (rol definido en `CLAUDE.md`), nunca aplicada de forma autónoma por el módulo.
- Una vez aprobada, el cambio efectivo se documenta en `docs/03-Variables.md` (fuera de `learning/`) y se registra en `version-history.md` y en `CHANGELOG.md`.
- Si no hay evidencia suficiente, la propuesta se marca como rechazada y el peso actual permanece — esto también queda registrado, para no perder el intento y su justificación.

---

Fin del documento.
