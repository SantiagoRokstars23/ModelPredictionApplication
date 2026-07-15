# Version History

**Módulo:** `learning/version-history.md`

**Versión:** 1.0.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

Mantener el registro histórico y auditable de **qué cambió en el modelo, cuándo y por qué**, con foco en el respaldo estadístico de cada cambio — es la memoria a largo plazo del ciclo de aprendizaje.

Es la contraparte técnica de `docs/11-Versiones.md`: ese documento registra QUÉ versión existe y un resumen del cambio; `version-history.md` registra el razonamiento y la evidencia estadística completos detrás de cada cambio, con trazabilidad hacia la propuesta de `weight-adjustment.md` que lo originó.

---

# Responsabilidad

- Registrar cada cambio aplicado al modelo que se haya originado en una propuesta aprobada de `weight-adjustment.md`.
- Vincular cada entrada con la evidencia que la justificó (referencia a `pattern-discovery.md`/`confidence-calibration.md`) y con la versión de `docs/11-Versiones.md` en la que se incorporó.
- Permitir, hacia atrás, comparar las métricas de auditoría (`data/audit/`) antes y después de cada cambio, para confirmar si realmente mejoró el modelo o si debe revertirse.

No decide si un cambio se aplica (eso ya ocurrió en `weight-adjustment.md`); solo lo documenta de forma permanente y auditable una vez aplicado.

---

# Entradas

- Propuestas aprobadas de `weight-adjustment.md`.
- `docs/11-Versiones.md` (registro oficial de versiones).
- `CHANGELOG.md` (registro general de cambios del repositorio).
- `data/audit/` (métricas antes/después del cambio, para evaluar su efecto real).

---

# Salidas

Un historial estructurado de cambios, cada uno con:

- Versión del modelo afectada.
- Variable(s) modificada(s) y valores antes/después.
- Evidencia y propuesta de origen (referencia a `weight-adjustment.md`).
- Métrica de auditoría antes del cambio y después de un período de observación posterior.
- Conclusión: el cambio se mantiene, se ajusta de nuevo, o se revierte.

Esta salida retroalimenta `docs/11-Versiones.md` (actualización del resumen oficial de versión) y `CHANGELOG.md`.

---

# Dependencias

- `weight-adjustment.md` (fuente de cada entrada nueva).
- `docs/11-Versiones.md` y `CHANGELOG.md` (deben mantenerse sincronizados con este historial).
- `data/audit/` (para el seguimiento de métricas antes/después).

---

# Cómo interactúa con el resto del Modelo Santiago

- Es el último eslabón del pipeline de `learning/`: cierra el ciclo iniciado en `error-analysis.md`.
- Cierra también el `Principio de Desarrollo Incremental` de `CLAUDE.md` (Diseño → Implementación mínima funcional → Auditoría → Correcciones → Ampliación), ya que permite verificar si una "corrección" aplicada realmente resultó en una "ampliación" válida del modelo o si debe descartarse.
- Es la fuente de verdad que cualquier agente (`.claude/agents/`) debe consultar antes de asumir cuál es el peso o algoritmo vigente de una variable, evitando decisiones basadas en documentación desactualizada.

---

Fin del documento.
