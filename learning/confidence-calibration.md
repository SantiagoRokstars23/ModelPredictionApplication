# Confidence Calibration

**Módulo:** `learning/confidence-calibration.md`

**Versión:** 1.0.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

Verificar si el Índice de Confianza que declara el modelo (`engine/05-Confidence.md`) es **honesto**: si el modelo dice tener 90% de confianza en un grupo de predicciones, ese grupo debería acertar aproximadamente el 90% de las veces — ni más, ni menos.

Sin esta verificación, un Índice de Confianza mal calibrado invalida silenciosamente las decisiones de bankroll que dependen de él (`docs/07-Backroll.md`), aunque las probabilidades del partido en sí sean razonables.

---

# Responsabilidad

- Agrupar las predicciones resueltas por rango de confianza declarado (ej. 90-100, 80-89, 70-79, <60, según la escala ya definida en `docs/02-modelo.md`).
- Calcular, para cada rango, la tasa real de acierto observada.
- Construir la curva de calibración (confianza declarada vs. acierto real) y cuantificar la brecha entre ambas.
- Determinar si el motor de Confianza sobreestima o subestima sistemáticamente, y en qué rango.

No calcula la confianza de una predicción nueva (eso es `engine/05-Confidence.md`) — solo audita si el motor, en retrospectiva, cumplió lo que prometió.

---

# Entradas

- `data/predictions/`: nivel de Índice de Confianza declarado por cada predicción.
- `data/results/`: resultado real, para saber si esa predicción concreta acertó o no.
- `docs/02-modelo.md`: escala e interpretación oficial del Índice de Confianza (0-100, con sus tramos de interpretación).
- `data/audit/`: histórico de calibración de versiones anteriores, para ver si la calibración mejora o empeora entre versiones.

---

# Salidas

Reporte de calibración con, como mínimo:

- Curva de calibración (confianza declarada vs. frecuencia real de acierto, por tramo).
- Error de calibración por tramo (sobreestimación o subestimación, y su magnitud).
- Señalización de qué tramos de confianza son actualmente confiables para tomar decisiones de bankroll y cuáles no.

Este reporte se consolida como métrica histórica en `data/audit/` (coherente con la métrica "Calibration" ya prevista en `data/README.md` para la versión 2.0) y se entrega como evidencia a `weight-adjustment.md` cuando la descalibración es atribuible a variables concretas que alimentan `engine/05-Confidence.md`.

---

# Dependencias

- `data/predictions/`, `data/results/` (obligatorias).
- `engine/05-Confidence.md` (el motor bajo evaluación).
- `docs/02-modelo.md` (definición oficial de la escala de confianza).
- `error-analysis.md` (para saber, caso a caso, si un error ya fue explicado por otra causa antes de atribuirlo a mala calibración).

---

# Cómo interactúa con el resto del Modelo Santiago

- Es un afluente adicional hacia `weight-adjustment.md`: junto con `pattern-discovery.md`, aporta evidencia sobre qué ajustar y por qué.
- Su resultado afecta indirectamente a `agents/bankroll-manager.md`, ya que la gestión de capital depende de que el Índice de Confianza sea fiable (`docs/07-Backroll.md`: "Si confianza >90 → invertir 100%" solo tiene sentido si esa confianza está bien calibrada).
- Operado conceptualmente por `.claude/agents/auditor.md`.
- Cualquier fórmula concreta de calibración (ej. Brier Score) requiere primero un documento de investigación en `models/`, antes de implementarse — no se define aquí.

---

Fin del documento.
