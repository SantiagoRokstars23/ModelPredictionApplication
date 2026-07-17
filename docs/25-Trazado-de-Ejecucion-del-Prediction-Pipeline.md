# Trazado de Ejecución del Prediction Pipeline

**Archivo:** `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`

**Misión:** IMP-001 — Diseño del Prediction Pipeline del Modelo Santiago (primera misión de la serie `IMP-`, fase de implementación conceptual)

**Versión:** 1.0.0

**Estado:** Especificación operativa — sin implementar código

---

# Objetivo

Describir, en un único recorrido continuo, exactamente qué ocurre desde que el usuario solicita una predicción hasta que ésta queda almacenada — incluyendo el objeto de entrada exacto, una traza numérica de ejemplo a través de los 6 motores, y el objeto de respuesta completo (no su formato visual).

---

# Relación con `docs/06-Flujo-Operacional.md` y `docs/14-Prediction-Pipeline.md` (léase antes de continuar)

**Nota de verificación previa:** el brief de esta misión referenciaba `docs/05-Flujo-Operacional.md`, una ruta que no existe — ese documento se desplazó a `docs/06-Flujo-Operacional.md` en la Misión 005 (renumeración de `docs/`). Este documento usa la ruta actual.

Este documento **no redefine** la arquitectura de fases (`docs/06`), el orden de lectura de archivos (`docs/14`), el contrato de variables (`docs/16`) ni la Capa de Preparación (`docs/15`) — los cuatro ya especifican, con detalle suficiente y sin contradicción entre sí (verificado en `MR-003`/`MR-004`), casi todo lo que este brief pide. Repetirlo aquí sería duplicación, no diseño.

Lo que este documento aporta, y que ningún documento anterior cubre todavía:

1. El **objeto de entrada** exacto que necesita el pipeline (ningún documento anterior lo define en términos de campos concretos — todos parten de "el usuario solicita una predicción" sin especificar qué contiene esa solicitud).
2. Una **traza numérica de ejemplo**, extremo a extremo, mostrando cómo un valor concreto viaja desde la Base de Conocimiento hasta la predicción final.
3. El **objeto de respuesta completo** — incluyendo dos campos que el brief pide (`jugadores destacados`, `mercados detectados`) que **exceden lo que el Engine V1 actual puede producir**, y que se documentan aquí como brecha explícita, no se inventan.

Cada sección remite al documento que ya posee la autoridad sobre ese punto, en lugar de repetirlo.

---

# 1. Entrada

*(Ningún documento anterior define el objeto de solicitud en términos de campos — se diseña aquí por primera vez.)*

| Campo | Obligatorio | Cómo se resuelve |
|---|---|---|
| Selección local | Sí | `id_seleccion` o nombre, resuelto contra `selecciones.csv` |
| Selección visitante | Sí | Idem |
| Competición | Sí | `id_competicion` o nombre, resuelto contra `competiciones.csv` |
| Torneo/edición | Sí | `id_torneo`, resuelto contra `torneos.csv` — se exige explícito (no se infiere de competición+fecha) para evitar ambigüedad cuando existan ediciones simultáneas |
| Fecha del partido | Sí | Fecha `YYYY-MM-DD` (`docs/05-Base-de-Conocimiento.md`) |
| Hora local | No | Solo si ya está definida; afecta Factores Externos (calor/humedad) |
| Mercado(s) para Valor Esperado | No | Si se omite, la Fase 4 (`docs/06`) se salta explícitamente — nunca se asume un mercado por defecto |
| Gestión de bankroll | No | Activa la Fase 5 (`docs/06`) solo si el usuario lo pide explícitamente |

Validación de esta entrada: si Selección local, Selección visitante, Competición, Torneo o Fecha faltan, el Orchestrator detiene el flujo antes de la Fase 1 (`docs/06`) — no es una fase nueva, es la puerta de entrada ya definida allí.

---

# 2. Validaciones iniciales

Ya especificadas en `docs/06-Flujo-Operacional.md`, Fase 2 (Statistician) — no se repiten. Resumen de referencia: existencia de ambos equipos y del partido en `data/processed/selecciones-nacionales/`, suficiencia de estadísticas por `docs/03-Variables.md`, integridad referencial (IDs válidos, sin duplicados). Si falla: el flujo se detiene, nunca se estima con datos parciales (`docs/06`, tabla "Manejo de errores").

---

# 3. Construcción del contexto

Ya especificado, archivo por archivo y en el orden exacto de lectura, en `docs/14-Prediction-Pipeline.md`, Etapa 2 (tabla de 10 archivos: `selecciones.csv` → `competiciones.csv` → `torneos.csv` → `estadios.csv` → `arbitros.csv` → `partidos.csv` → `estadisticas_partido.csv` → `jugadores.csv`+`convocatorias.csv` → `lesiones.csv` → `cuotas.csv`). No se repite aquí. Esta etapa **no calcula nada** — solo recupera datos de negocio; el cálculo empieza en la Etapa 4.

---

# 4. Preparación de Variables

Ya especificado en `docs/15-Capa-de-Preparacion-de-Variables.md` (secciones 3-6) y `docs/16-Contrato-Oficial-de-Variables.md`. Resumen de referencia:

- **Recibe:** los datos de negocio recuperados en la Etapa 3 (sin conocer de qué archivo provienen).
- **Devuelve:** las 12 Variables Oficiales (`docs/16`), cada una validada, normalizada, y marcada como disponible o no disponible — nunca inventada. Tras `MR-004`: 10 activas con consumidor confirmado, 2 (Compatibilidad Táctica, Estado Psicológico) formalmente diferidas, sin construirse en V1.
- **Contrato que utiliza:** `docs/16-Contrato-Oficial-de-Variables.md` (tipo, unidad, rango, nulabilidad de cada variable).

---

# 5. Ejecución del Engine — traza numérica de ejemplo

El orden de capas ya está definido en `docs/06-Flujo-Operacional.md` ("Diagrama de dependencias del Engine") y el consumo exacto por motor en `docs/17-Matriz-de-Consumo-de-Variables.md`. Se ilustra aquí con una traza concreta, usando el mismo ejemplo ya presente en `docs/08-predicciones.md` (España vs. Francia), para mantener continuidad con el resto del proyecto:

```
Variables Oficiales preparadas (docs/15)
   │  (Forma Reciente, Rendimiento en el Torneo, Potencial Ofensivo, Solidez
   │   Defensiva, Disponibilidad de Plantilla, Fatiga, Calidad de Plantilla,
   │   Localía, Historial Directo, Factores Externos)
   ▼
engine/01-Offensive-Strength.md  ──►  Fuerza Ofensiva: España 78 · Francia 82
engine/02-Defensive-Strength.md  ──►  Fuerza Defensiva: España 74 · Francia 70
   │
   ▼
engine/03-Poisson.md (+ Variable009 Localía, directa)
   ──►  Goles esperados: España 1.8 · Francia 1.6
   ──►  Probabilidades: Local 41% · Empate 28% · Visitante 31%
   ──►  Top 4 marcadores: 2-1 (22%) · 1-1 (18%) · 2-0 (15%) · 1-2 (12%)
   │
   ├──► engine/04-Chaos-Index.md         ──►  Índice de Caos: 31
   └──► engine/05-Confidence.md          ──►  Índice de Confianza: 84
          (+ Variable010 Historial Directo, directa, contextual menor)
   │
   ▼
engine/06-Expected-Value.md (si hay cuotas y mercado solicitado)
   ──►  Valor Esperado: Positivo
   ⚠ excepción documentada: consume cuotas.csv directamente, no vía la Capa (INC-05,
     resuelto en principio en MR-004, pendiente de implementación completa)
```

Los valores numéricos son ilustrativos (coinciden con el ejemplo ya publicado en `docs/08-predicciones.md`); ninguna fórmula real está definida todavía (`models/`, estado "Investigación" en los 6 documentos revisados — `AR-001`).

---

# 6. Construcción de la respuesta

*(El objeto exacto que produce el modelo — no su formato visual.)*

| Campo | Contenido | Fuente / Estado |
|---|---|---|
| `partido` | Selecciones, competición, torneo, fecha, estadio | Etapa 3 |
| `probabilidades` | Local / Empate / Visitante (suma 100%) | `engine/03` |
| `top_marcadores` | 4 marcadores con su probabilidad | `engine/03` |
| `variables_influyentes` | Lista explícita de qué variables pesaron más, nunca implícita | Predictor, ya exigido en `docs/14`, Etapa 2 |
| `confianza` | Valor 0-100 y nivel (`docs/02-modelo.md` §7) | `engine/05` |
| `indice_caos` | Valor 0-100 y nivel (`docs/02-modelo.md` §8) | `engine/04` |
| `valor_esperado` | Valor y mercado, o "no disponible — sin cuotas registradas" | `engine/06`, condicional |
| `version_modelo` | Versión del Modelo Santiago usada (`docs/11-Versiones.md`) | Obligatorio (`data/predictions/README.md`) |
| `id_prediccion` | Identificador único, `id_partido` + timestamp | Etapa de registro (sección 7) |
| **`jugadores_destacados`** | — | **No disponible en V1.** Ningún motor de `engine/01-06` produce salida a nivel de jugador individual — todos operan a nivel de equipo. Se documenta como campo futuro del contrato de respuesta, condicionado a que un motor (o una extensión de uno existente) empiece a producir esa salida. No se inventa un origen para este campo. |
| **`mercados_detectados`** | — | **No disponible en V1, en el sentido de "escaneo automático".** `engine/06-Expected-Value.md` evalúa el mercado que se le solicite explícitamente (Entrada, sección 1) — no escanea proactivamente todos los mercados con cuotas disponibles para detectar valor por su cuenta. Ese comportamiento requeriría una extensión de diseño de `engine/06`, fuera del alcance de esta misión ("no modificar el Engine"). |

Esta es la diferencia central entre lo que el brief ejemplifica y lo que el Engine V1 ya definido puede sostener hoy — se deja explícita en vez de rellenarse con una interpretación conveniente.

---

# 7. Persistencia

Ya especificado en `docs/14-Prediction-Pipeline.md`, Etapa 3. Resumen de referencia: se registra en `data/predictions/` inmediatamente después de la Etapa 6, siempre antes del inicio del partido; identificador = `id_partido`; nunca se sobrescribe ni se regenera silenciosamente una vez registrada. **Nunca podrá modificarse posteriormente:** la predicción en sí (`data/predictions/README.md`, "Nunca sobrescribir"), y una vez iniciado el partido, ni siquiera para corregirla. El esquema exacto de columnas sigue diferido a una misión de diseño de datos futura (`docs/14`, ya declarado, no se redefine aquí).

---

# 8. Integración con Auditoría

Ya especificado en `docs/06-Flujo-Operacional.md`, Fase 8. El Auditor utilizará, de este pipeline: el objeto de respuesta completo registrado en `data/predictions/` (sección 6 de este documento) comparado contra `data/results/` una vez el partido finalice — nunca antes.

---

# 9. Integración con Learning

Ya especificado en `docs/06-Flujo-Operacional.md`, Fase 9, y `learning/README.md`. `learning/` utilizará, de este pipeline: las Variables Oficiales que efectivamente participaron en cada predicción (sección 4-5) y el resultado de la comparación de Auditoría (sección 8), para producir diagnósticos y, eventualmente, una propuesta de recalibración — nunca aplicada automáticamente (Constitución, Art. 2, "No autoaprobación").

---

# Validaciones obligatorias

- **¿El flujo puede ejecutarse de principio a fin?** Sí, con dos excepciones ya documentadas y no bloqueantes: `engine/06` accede a `cuotas.csv` directamente (`INC-05`, resuelto en principio) y 2 de 12 variables están formalmente diferidas sin impedir el resto del cálculo.
- **¿Ningún motor depende directamente del usuario?** Confirmado — la solicitud del usuario (sección 1) la procesa siempre el Orchestrator primero (`docs/06`, Fase 1); ningún motor de `engine/` recibe la solicitud original, solo Variables Oficiales o salidas de otros motores.
- **¿Todas las Variables Oficiales provienen de la Base de Conocimiento?** Confirmado, vía la Capa de Preparación de Variables (sección 4) — única excepción documentada: cuotas (dato de mercado, nunca una Variable Oficial, `docs/16`).
- **¿El pipeline puede ejecutarse con información disponible antes del partido?** Confirmado — las 10 variables activas se derivan de historial y datos previos al partido (forma reciente, plantilla, localía, etc.); ninguna requiere el resultado del propio partido. Las cuotas de mercado también son, por naturaleza, un dato previo al partido.

---

# Cierre obligatorio

**1. ¿El Prediction Pipeline ya puede generar una predicción completa?**
Conceptualmente sí — el recorrido completo (entrada → validación → contexto → variables → 6 motores → respuesta → persistencia) está especificado sin saltos lógicos. Lo que falta es exclusivamente matemático (`models/`, estado "Investigación") y de implementación (código), no de diseño de flujo.

**2. ¿Qué información mínima necesita?**
Selección local, selección visitante, competición, torneo y fecha (sección 1) — el resto (hora, mercado, bankroll) es opcional y condiciona qué fases adicionales se activan.

**3. ¿Qué módulos participan?**
Orchestrator → Statistician → Capa de Preparación de Variables → Predictor (invoca `engine/01-06`) → Odds Analyzer (condicional) → Bankroll Manager (opcional) → registro en `data/predictions/` → (tiempo después) Auditor → `learning/`.

**4. ¿Qué información produce?**
El objeto de respuesta de la sección 6 — con dos campos explícitamente marcados como no disponibles en V1 (`jugadores_destacados`, `mercados_detectados`), no simulados.

**5. ¿Qué información almacena?**
El objeto completo de la sección 6, en `data/predictions/`, identificado por `id_prediccion` (`id_partido` + timestamp), inmutable una vez registrado (sección 7).

**6. ¿Qué parte queda pendiente para la implementación real?**
Tres cosas concretas: (a) las fórmulas matemáticas de los 6 motores (`models/`, ninguna tiene Versión 2.0 todavía); (b) el Contrato de Datos de Mercado para cerrar `INC-05` en implementación completa (`MR-004`); (c) cualquier extensión de diseño necesaria si en el futuro se decide que `jugadores_destacados`/`mercados_detectados` sí formen parte del contrato de respuesta — hoy no tienen motor que los produzca.

**7. ¿Qué misión recomendarías después de IMP-001?**
La primera investigación matemática real en `models/` (empezando por `models/poisson.md`, que ya tiene el mayor número de motores dependientes) — es la pieza que, una vez completada, empieza a convertir este trazado conceptual en un pipeline calculable de verdad. En paralelo, sigue pendiente `INC-06` (Rotaciones) y el Contrato de Datos de Mercado ya identificados por `MR-004`.

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se modifica el Engine, variables, algoritmos, pesos, ni ningún documento existente.
- No se diseña la fórmula matemática de ningún motor — pertenece a `models/`.
- No se define el esquema exacto de columnas de `data/predictions/` — ya diferido desde `docs/14`.
- No se diseña el mecanismo para producir `jugadores_destacados` ni `mercados_detectados` — se documenta la brecha, no se cierra.

---

Fin del documento.
