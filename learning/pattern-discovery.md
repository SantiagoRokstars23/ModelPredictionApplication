# Pattern Discovery

**Módulo:** `learning/pattern-discovery.md`

**Versión:** 1.0.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

Detectar sesgos o comportamientos **recurrentes** del Modelo Santiago a lo largo de múltiples partidos, torneos o contextos — a diferencia de `error-analysis.md`, que evalúa un partido aislado.

Ejemplo del tipo de hallazgo que produce: "el modelo sobrevalora sistemáticamente a la selección favorita en fases eliminatorias" o "el Índice de Caos subestima el impacto real de lesiones ocurridas en la semana previa al partido".

---

# Responsabilidad

- Agregar los registros individuales producidos por `error-analysis.md` a través del tiempo, del torneo, de la confederación, de la fase de competición, etc.
- Identificar si una misma variable aparece repetidamente señalada como causa de desviación, y con qué frecuencia y magnitud.
- Determinar si el patrón es estadísticamente relevante (frecuencia mínima, consistencia en el tiempo) o si es ruido de muestra pequeña.
- Priorizar los patrones encontrados según su impacto potencial en el ROI y en la calibración del modelo.

No propone un nuevo peso concreto — solo documenta el patrón y su evidencia (esa traducción a un peso concreto es responsabilidad de `weight-adjustment.md`).

---

# Entradas

- Registros acumulados de `error-analysis.md` (múltiples partidos).
- `data/audit/` (métricas históricas ya consolidadas, para contrastar el patrón con el rendimiento agregado conocido).
- Metadatos de contexto de `data/processed/selecciones-nacionales/` (fase del torneo, confederación, tipo de competición) para segmentar dónde ocurre el patrón.

---

# Salidas

Un informe de patrones detectados, cada uno con:

- Descripción del patrón.
- Variable(s) del modelo asociada(s) (`docs/03-Variables.md`).
- Evidencia cuantitativa (frecuencia, magnitud, número de partidos/torneos donde se observa).
- Segmento donde aplica (ej. "solo en fases eliminatorias", "solo en confederaciones con alta densidad de amistosos").
- Nivel de confianza estadística del hallazgo (para evitar actuar sobre ruido, en línea con `CLAUDE.md`: "nunca alterar pesos sin evidencia estadística").

Los patrones confirmados con evidencia suficiente pasan como insumo a `weight-adjustment.md`. Si un patrón sugiere una variable **no contemplada** en `docs/03-Variables.md`, se documenta como propuesta de investigación para `models/`, no se incorpora directamente.

---

# Dependencias

- `error-analysis.md` (insumo directo y obligatorio).
- `docs/03-Variables.md` (para asociar cada patrón a una variable existente).
- `models/` (para verificar si el patrón ya tiene fundamento teórico documentado o si requiere investigación nueva antes de actuar sobre él).

---

# Cómo interactúa con el resto del Modelo Santiago

- Recibe su insumo de `error-analysis.md` y entrega su resultado a `weight-adjustment.md`: es el segundo eslabón del pipeline.
- Operado conceptualmente por `.claude/agents/auditor.md`, con revisión de `.claude/agents/statistician.md` para validar la suficiencia estadística del patrón antes de que se considere "evidencia" válida.
- Si un patrón excede el alcance de una variable existente, genera una recomendación explícita hacia `models/` (nueva investigación), respetando la regla de `CLAUDE.md`: "Ningún motor podrá incorporar nuevas fórmulas, variables o algoritmos sin una investigación previa documentada".

---

Fin del documento.
