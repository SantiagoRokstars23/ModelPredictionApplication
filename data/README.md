# Base de Conocimiento del Modelo Santiago

**Versión:** 1.0.0

**Estado:** Activo

---

# Objetivo

El directorio `data/` constituye la Base de Conocimiento del Modelo Santiago.

Su propósito es almacenar, organizar y versionar toda la información utilizada por el sistema de predicción.

Toda la información consumida por el Engine deberá provenir de este directorio.

Ningún agente podrá utilizar datos externos sin que estos hayan sido previamente validados e incorporados a la Base de Conocimiento.

---

# Filosofía

Los datos representan el activo más importante del Modelo Santiago.

Una predicción nunca será mejor que la calidad de la información utilizada.

Por esta razón, toda información deberá ser:

- Verificable.
- Consistente.
- Reutilizable.
- Versionable.
- Trazable.

---

# Estructura

data/

├── raw/

├── processed/

├── predictions/

├── results/

├── audit/

└── archive/

---

# Descripción de cada directorio

## raw/

Contiene información obtenida desde fuentes externas.

No debe modificarse manualmente.

Representa la copia original de los datos.

---

## processed/

Contiene información validada y normalizada.

Es la única fuente autorizada para el Engine.

---

## predictions/

Almacena todas las predicciones generadas por el Modelo Santiago.

Nunca deberán sobrescribirse.

Cada predicción representa un registro histórico.

---

## results/

Contiene los resultados oficiales de los partidos.

Se utilizará para validar las predicciones.

---

## audit/

Almacena indicadores históricos del rendimiento del modelo.

Ejemplos:

- ROI
- Hit Rate
- Brier Score (v2.0)
- Calibration
- Drawdown

---

## archive/

Almacena información histórica que ya no participa en el proceso activo, pero que debe conservarse para fines de auditoría o investigación.

Nunca deberá eliminarse información de este directorio.

---

# Flujo de los datos

Internet

↓

raw/

↓

Validación

↓

processed/

↓

Engine

↓

Predictions

↓

Results

↓

Audit

↓

Aprendizaje

---

# Reglas

Nunca modificar archivos históricos.

Nunca eliminar información utilizada por auditoría.

Nunca consumir información directamente desde Internet.

Toda información deberá pasar por `processed/`.

Toda modificación deberá ser trazable.

---

# Dependencias

Este directorio es utilizado por:

- Engine
- Predictor
- Statistician
- Auditor
- Odds Analyzer

---

# Versión 2.0

La versión 2.0 incorporará:

- Base de datos relacional.
- Versionado automático.
- Actualización incremental.
- Sincronización mediante APIs.
- Caché inteligente.
- Validación automática de integridad.