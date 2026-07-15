# Módulo: learning/

**Versión:** 1.0.0

**Estado:** Diseño (Arquitectura) — sin implementación

---

# Objetivo

`learning/` es el módulo responsable del **aprendizaje continuo** del Modelo Santiago: analiza el historial de predicciones ya resueltas para generar conocimiento auditable que permita mejorar futuras versiones del modelo.

Es la contraparte de `engine/` (que predice) dentro del ciclo de vida del modelo: `engine/` mira hacia adelante (genera una predicción), `learning/` mira hacia atrás (evalúa qué tan bien predijo el sistema y por qué).

---

# Límites de responsabilidad (obligatorios)

`learning/` **nunca**:

- Calcula probabilidades de un partido.
- Genera o modifica una predicción.
- Escribe, sobrescribe o elimina información en `data/raw/`, `data/processed/`, `data/predictions/` o `data/results/` — estas siguen siendo la única fuente oficial de la Base de Conocimiento (`docs/05-Base-de-Conocimiento.md`).
- Aplica automáticamente un cambio de peso, variable o algoritmo.

`learning/` **siempre**:

- Lee información ya existente y cerrada (predicciones resueltas + resultados oficiales).
- Produce **conocimiento documentado**: diagnósticos, patrones, métricas de calibración y propuestas de mejora respaldadas por evidencia.
- Entrega sus conclusiones como **recomendaciones para revisión humana** (el Arquitecto Estadístico del Modelo Santiago), nunca como cambios directos a `docs/`, `engine/` o `data/`.

Esto respeta directamente las reglas de `CLAUDE.md`: "Nunca alterar pesos sin evidencia estadística" y "Nunca modificar un algoritmo sin documentarlo" — `learning/` produce la evidencia y la propuesta, pero la decisión y la modificación siguen perteneciendo al ciclo de diseño (`docs/`/`engine/`/`models/`), no a este módulo.

---

# Estructura y pipeline

```
data/predictions/  +  data/results/
              │
              ▼
     error-analysis.md          (¿qué pasó en cada partido, partido a partido?)
              │
              ▼
    pattern-discovery.md        (¿se repite en muchos partidos?)
              │
              ▼
  confidence-calibration.md     (¿el nivel de confianza declarado es honesto?)
              │
              ▼
   weight-adjustment.md         (propuesta documentada de recalibración)
              │
              ▼
    version-history.md          (registro auditable de qué cambió y por qué)
```

Cada documento consume el resultado del anterior. Ninguno puede saltarse (mismo principio que `docs/04-Algoritmo.md`: "Ningún paso podrá omitirse").

---

# Relación con el resto del Modelo Santiago

| Componente | Relación con `learning/` |
|---|---|
| `data/predictions/`, `data/results/` | Fuente de entrada de solo lectura. |
| `data/audit/` | Destino de las métricas históricas agregadas (ROI, Top1/Top4, calibración) que `learning/` calcula — coherente con `docs/05-Base-de-Conocimiento.md`, que ya define `audit/` como el repositorio de estas métricas. `learning/` calcula; `data/audit/` almacena el resultado. |
| `docs/09-Auditoria.md`, `docs/10-aprendizaje.md` | Definen QUÉ se audita y la filosofía del aprendizaje; `learning/` define CÓMO se ejecuta ese proceso paso a paso. |
| `docs/03-Variables.md`, `engine/` | Destino final (fuera de este módulo) de cualquier cambio de peso o variable que `weight-adjustment.md` proponga y que sea aprobado. |
| `models/` | Respaldo científico obligatorio antes de que `learning/` incorpore una fórmula concreta (Brier Score, técnicas de calibración, etc.) en su versión 2.0 — misma relación que ya existe entre `engine/` y `models/` (`CLAUDE.md`: "Investigación antes de implementación"). |
| `.claude/agents/auditor.md` | Es el agente que opera `error-analysis.md`, `pattern-discovery.md` y `confidence-calibration.md`. |
| `.claude/agents/statistician.md` | Revisa la evidencia detrás de cada propuesta de `weight-adjustment.md` antes de que se apruebe un cambio. |
| `prompts/audit-template.md`, `prompts/recalibration-template.md` | Plantillas ya existentes que, en la versión implementada, dispararán la ejecución de este módulo. |
| `docs/11-Versiones.md` | Registro oficial de versiones del modelo; `version-history.md` es su contraparte técnica/estadística (el porqué detrás de cada versión). |

---

# Versión 2.0 (fuera de alcance de esta misión)

La implementación matemática de cada documento (fórmulas de calibración, umbrales de significancia estadística para un patrón, la fórmula exacta de ajuste de peso) deberá respaldarse primero en un documento de `models/`, siguiendo el estándar de 8 secciones ya definido en `CLAUDE.md`. Ningún documento de `learning/` implementará fórmulas directamente — igual que `engine/`, la lógica matemática pertenece a `models/` primero y luego a una capa de implementación.

---

Fin del documento.
