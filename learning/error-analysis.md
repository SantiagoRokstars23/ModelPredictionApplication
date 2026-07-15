# Error Analysis

**Módulo:** `learning/error-analysis.md`

**Versión:** 1.0.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

Diagnosticar, partido por partido, por qué el Modelo Santiago acertó o falló una vez que el resultado oficial está disponible.

No mide rendimiento agregado (eso corresponde a `pattern-discovery.md`); mide **un caso a la vez**, con el mismo nivel de detalle con el que se generó la predicción original.

---

# Responsabilidad

- Comparar cada predicción cerrada (`data/predictions/`) contra su resultado oficial (`data/results/`).
- Clasificar el resultado de esa comparación (acierto exacto, acierto de resultado 1X2, error de marcador, error de resultado).
- Para cada error, identificar qué variable(s) del algoritmo (`docs/04-Algoritmo.md`, `docs/03-Variables.md`) más probablemente explican la desviación entre lo predicho y lo ocurrido (ej. "se sobrevaloró el Potencial Ofensivo del equipo local").
- Producir un registro individual por partido, reutilizable por los documentos siguientes del pipeline.

No decide si hay que cambiar un peso — solo documenta la evidencia cruda de cada caso.

---

# Entradas

- `data/predictions/`: probabilidades declaradas, Top 4 de marcadores, variables utilizadas, Índice de Confianza e Índice de Caos de la predicción original.
- `data/results/`: resultado oficial del partido.
- `docs/04-Algoritmo.md`: para saber qué variables y pasos participaron en la predicción y así ubicar el origen de una desviación.

---

# Salidas

Un registro estructurado por partido con, como mínimo:

- Identificador del partido (trazable a `data/processed/selecciones-nacionales/partidos.csv` vía `id_partido`).
- Tipo de resultado (acierto exacto / acierto 1X2 / error).
- Magnitud del error (diferencia entre probabilidad asignada al resultado real y 100%).
- Variable(s) señalada(s) como posible causa de la desviación.
- Observaciones cualitativas (ej. lesión de último momento no reflejada a tiempo).

Este registro individual se acumula como insumo agregado para `pattern-discovery.md` y como evidencia puntual para `weight-adjustment.md`. Los indicadores agregados que se deriven de él (no el detalle partido a partido) se consolidan en `data/audit/`.

---

# Dependencias

- `data/predictions/` y `data/results/` (obligatorias — sin ambas, el análisis no puede ejecutarse).
- `docs/03-Variables.md` y `docs/04-Algoritmo.md` (para nombrar correctamente las variables señaladas).
- `docs/09-Auditoria.md` (definición oficial de qué se considera acierto/error).

---

# Cómo interactúa con el resto del Modelo Santiago

- Es el primer eslabón del pipeline de `learning/`: alimenta directamente a `pattern-discovery.md`.
- Es operado conceptualmente por el agente `auditor.md` (`.claude/agents/auditor.md`), cuyo objetivo ya es "comparar las predicciones con los resultados reales".
- Es disparado, en la versión implementada, por `prompts/audit-template.md`.
- Nunca modifica `data/predictions/` ni `data/results/`: solo los lee y produce un análisis derivado.

---

Fin del documento.
