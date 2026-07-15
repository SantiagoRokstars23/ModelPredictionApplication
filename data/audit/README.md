# Audit

**Directorio:** `data/audit/`

**Versión:** 1.0.0

**Estado:** Activo

---

# Objetivo

Almacenar los indicadores históricos del rendimiento del Modelo Santiago.

---

# Responsabilidad

Medir la calidad del modelo a lo largo del tiempo.

---

# Contenido

Ejemplos:

- roi.csv
- accuracy.csv
- calibration.csv
- drawdown.csv

---

# Indicadores

- ROI
- Hit Rate
- Top 1 Accuracy
- Top 2 Accuracy
- Top 4 Accuracy
- Expected Value
- Brier Score (v2.0)

---

# Reglas

Nunca eliminar auditorías históricas.

Toda auditoría deberá indicar la versión del modelo evaluada.

---

# Consumidores

- Auditor
- Statistician

---

# Versión 2.0

Dashboard automático de métricas.