# Arquitectura de la Fase II — Optimización del Modelo Santiago

**Archivo:** `docs/39-Fase-II.md`

**Misión:** FII-001 — Arquitectura de la Fase II (Optimización del Modelo)

**Versión:** 1.0.0

**Estado:** Documento oficial de gobierno de la Fase II — sin código, sin CSV, sin Engines, sin Variables, sin pesos ni fórmulas modificados. Rige a partir de `v1.1.0`.

---

## Nota de numeración (verificación previa, obligatoria antes de escribir — `docs/22` §3)

El brief de esta misión pide crear `docs/11-Fase-II.md`. Verificado antes de escribir: **`docs/11-Versiones.md` ya existe** ("Historial de versiones del modelo", catalogado desde la reorganización de `docs/` descrita en `CLAUDE.md`). Sobrescribirlo o renombrarlo violaría dos reglas ya vigentes y explícitas:

1. `CLAUDE.md`, sección "Estado Actual del Repositorio": *"A partir de la posición 14, `docs/` se extendió **por adición, nunca por inserción** (política adoptada explícitamente desde `MS-007` para no repetir una tercera renumeración)"*.
2. Constitución del Modelo Santiago, Art. 7 (citado ya en `docs/23`, mismo tipo de colisión resuelta allí): *"toda contradicción debe documentarse, nunca ocultarse"*.

**Resolución, mismo patrón ya usado en `docs/23` (AR-002, solicitada como "MR-002" pero registrada distinto por colisión con un `MR-002` ya reservado):** este documento se crea como **`docs/39-Fase-II.md`** — el siguiente número libre en la secuencia por adición (`docs/38` es el último documento secuencial antes del especial `docs/99-Mapa-Maestro.md`) — sin tocar `docs/11-Versiones.md`. La misión sigue registrándose como **`FII-001`** en `docs/00-Project-Tracker.md`, exactamente como la nombró el usuario; solo cambia la ruta del archivo.

---

## 1. Objetivo de la Fase II

La Fase I construyó el modelo: arquitectura, Variables, Engines, investigación matemática previa a cada cambio, backtesting reproducible. La Fase II **no busca aumentar la complejidad matemática del modelo** — busca **optimizar su rentabilidad práctica** sobre la arquitectura ya construida y ya congelada en su diseño.

Los cinco objetivos específicos de la Fase II, en el orden en que el Roadmap (sección 5) los ataca:

1. **Aumentar la cobertura** — hoy el modelo solo puede evaluarse sobre el 28.2% de los partidos reales disponibles (`VALID-003`); ninguna optimización posterior es confiable sobre una base tan estrecha.
2. **Mejorar la calibración** — que la probabilidad que el modelo asigna a un resultado coincida, en la práctica, con la frecuencia real de ese resultado (evidencia de sobreconfianza ya medida en `ANL-001`/`ANL-004`).
3. **Mejorar la cobertura de mercados** — Ganador es el único mercado por encima del 60% de acierto; BTTS, Over/Under, Marcador Exacto y Top-4 quedan todos por debajo (`ANL-004`).
4. **Aumentar el ROI y activar el EV** — `Engine06` (Valor Esperado) existe en código desde `BUILD-015` pero nunca ha podido ejecutarse con datos reales: `cuotas.csv` sigue vacío.
5. **Reducir errores prácticos** — no en el sentido de "modelo más sofisticado", sino de menos fricción operativa: gestión de riesgo, bankroll, automatización del flujo de predicción → registro → auditoría.

**Lo que la Fase II explícitamente NO es:** una nueva ronda de investigación matemática sobre `λ`, Poisson o las fórmulas de Variables ya congeladas. `ANL-004` ya demostró que ese camino tiene un techo matemático bajo (~90-95% del error actual es inherente al diseño Poisson-independiente, no corregible por más matemática). Seguir ese camino contradice la evidencia ya producida por la propia Fase I.

---

## 2. Estado heredado de la Fase I (resumen ejecutivo — sin repetir documentación)

| Eje | Estado al cierre de `v1.1.0` |
|---|---|
| Arquitectura | Completa y congelada en su diseño (`docs/18`-`docs/23`, `docs/29`-`docs/35`) — `PredictionContext`, `VariablePreparation`, los 6 Engines, `EngineRunner`, `EnginePipeline`, `PredictMatchUseCase` |
| Variables Oficiales | 9 de 9 activas con método de cálculo real (`FIX-002` resolvió el último bloqueo, Localía) |
| Estabilización estadística | Implementada donde la evidencia la justificó (Variable003/004, `MODEL-017`/`018`→`IMP-002`, validada en `VALID-002`); investigada y **descartada con evidencia** donde no la justificó (Variable001 `MODEL-021`, Variable007 `MODEL-022`) |
| Dixon-Coles | Ciclo completo — investigado (`MODEL-019`), diseñado (`MODEL-020`), implementado (`IMP-003`), validado (`VALID-004`) — **rechazado para uso por defecto** (`ρ=0`, solo 3/9 métricas obligatorias mejoraron) |
| Backtesting | Reproducible mediante una técnica de snapshot temporal, reutilizada sin cambios en 10+ misiones (`VALID-001` a `004`, `ANL-001` a `004`, `CAL-002`/`004`, `MODEL-021`/`022`) |
| Descomposición de error | Completa — `ANL-003` (origen de `λ`), `ANL-004` (~90-95% del error es inherente al Poisson, no a la calibración) |
| Base de Conocimiento | Separada de la Aplicación (`KB-001`, copia independiente de solo lectura) |
| Versionado | Modelo completamente versionado — `v1.1.0` tageada, `CHANGELOG.md` cerrado |

**Veredicto heredado, sin ambigüedad:** la Fase I está cerrada como fase de *construcción*. No está, y nunca declaró estar, cerrada como fase de *rentabilidad* — esa es, precisamente, la Fase II.

---

## 3. Problemas abiertos (solo evidencia ya documentada, ninguno inventado)

| # | Problema | Evidencia |
|---|---|---|
| 1 | **Cobertura incompleta** | 35 de 124 partidos evaluables (28.2%, `VALID-003`); solo 2 de 5 competiciones activas tienen algún partido evaluable (Eurocopa, Copa América — `ANL-004` §6.5); Mundial 2026, Eliminatorias y Nations League sin ninguna cobertura de StatsBomb |
| 2 | **Sesgo estructural hacia los empates** | Recall de empates = **0%** en las 4 muestras donde se midió (`VALID-001`, `VALID-002`, `VALID-003`, `VALID-004`) — con y sin Dixon-Coles activo |
| 3 | **Baja cobertura del Top-4** | El marcador real queda **fuera del Top-4 el 57.1%** de las veces (`ANL-004` §6.3) — no es un problema de orden (posiciones #2-#4 explican solo 5.7% cada una), es de cobertura de la matriz |
| 4 | **Mercados aún no optimizados** | Solo Ganador supera 60% de accuracy; BTTS 42.9%, Over/Under 48.6%, Marcador Exacto 25.7%, Top-4 42.9% (`ANL-004` §6.4) |
| 5 | **Falta de calibración de probabilidades** | Patrón de sobreconfianza medido dos veces de forma independiente: `ANL-001` (`P(favorito)` media 78.6% vs. accuracy real 62.5%) y `ANL-004` (partidos de "favorito claro" con peor Accuracy/Brier que el tercio intermedio); `KAPPA_LOCAL`/`KAPPA_VISITANTE` nunca calibrados (`CAL-002` los probó y descartó por evidencia insuficiente) |
| 6 | **Ausencia de EV real** | `Engine06` existe en código desde `BUILD-015` pero `cuotas.csv` solo tiene encabezado — nunca se ha ejecutado con datos de mercado reales |
| 7 | **Ausencia de gestión automática del riesgo** | `bankroll-manager.md` es una especificación de agente, sin ninguna lógica implementada en `app/services/` (bootstrap, sin código) |

**Nota de honestidad, no un problema adicional:** `ANL-004` ya acotó cuánto de los problemas 2-5 es realmente corregible — aproximadamente el 90-95% del error observado es matemáticamente inevitable dado el diseño Poisson-independiente. La Fase II debe optimizar dentro de ese margen real (~5-10%), no perseguir una meta que la propia Fase I ya demostró inalcanzable con esta arquitectura.

---

## 4. Principios de la Fase II

1. **No aumentar complejidad sin evidencia.** Mismo principio ya vigente en `CLAUDE.md` ("si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse"), reafirmado aquí como principio rector explícito de toda la Fase II, no solo de `models/`.
2. **Toda modificación requiere investigación previa.** Mismo patrón ya demostrado en cada ciclo de la Fase I (`MODEL-01X` → `IMP-00X` → `VALID-00X`) — ninguna misión de la Fase II puede saltarse directamente a la implementación.
3. **Toda modificación debe demostrar mejora mediante backtesting.** Reutilizando la infraestructura ya validada (snapshot temporal, mismo conjunto de partidos evaluables o uno ampliado por el Bloque A).
4. **Ningún cambio podrá disminuir métricas ya ganadas.** Mismo criterio de aceptación ya aplicado en `VALID-002`/`VALID-004` — si una métrica mejora a costa de degradar otra sin justificación explícita, el cambio se rechaza.
5. **Siempre priorizar ROI sobre sofisticación matemática.** Es el cambio de eje central de la Fase II (sección 1) — una mejora matemáticamente elegante que no mueve ROI/EV no es una prioridad de esta fase.
6. **No autoaprobación.** Ningún cambio de peso, fórmula, Variable o Engine puede aprobarse sin el Arquitecto Estadístico Humano (Constitución, Art. 2/5) — la Fase II no relaja esta regla, la hereda sin excepción.
7. **Ningún número de cierre se fija sin evidencia propia.** Los criterios de la sección 6 se dejan deliberadamente sin umbral numérico hasta que exista suficiente volumen de datos para fijarlos con evidencia — mismo principio ya aplicado a `κ_local`/`κ_visitante`/`k` del Shrinkage a lo largo de toda la Fase I.

---

## 5. Roadmap

Seis bloques, en el orden de dependencia real (cada bloque depende de que el anterior produzca la evidencia/datos que necesita, no es un orden arbitrario):

### Bloque A — Cobertura

**Por qué primero:** ningún resultado de los Bloques B-F es confiable si se mide sobre el 28.2% de cobertura actual, o sobre solo 2 de 5 competiciones. Objetivo: ampliar `estadisticas_partido.csv`/`partidos.csv` más allá de Eurocopa/Copa América (`docs/37`/`docs/38` ya definen el protocolo de ingesta) y/o reducir el bloqueo estructural que impide evaluar partidos con rival sin historial previo.

### Bloque B — Calibración

Depende del Bloque A (más partidos = curvas de calibración más confiables). Objetivo: cerrar la brecha entre probabilidad asignada y frecuencia real ya medida en `ANL-001`/`ANL-004` — candidatos ya identificados sin implementar: calibración de `KAPPA_LOCAL`/`KAPPA_VISITANTE` (`CAL-002`, pendiente de más evidencia), técnicas de recalibración post-hoc (ej. Platt scaling/isotonic regression) todavía no investigadas en ningún `MODEL-`.

### Bloque C — Mercados

Depende del Bloque B (probabilidades mal calibradas distorsionan cualquier mercado derivado). Objetivo: atacar específicamente BTTS, Over/Under, Marcador Exacto y la cobertura del Top-4 (`ANL-004` §6.3/§6.4) — el 57.1% de marcadores reales fuera del Top-4 es, con la evidencia actual, el problema individual de mayor tamaño medido en toda la Fase I.

### Bloque D — Valor Esperado (EV)

Depende de que exista dato real en `cuotas.csv` (fuera del control exclusivo de esta arquitectura — depende de una fuente de datos de mercado, `docs/38`). Objetivo: primera ejecución real de `Engine06`, nunca lograda hasta ahora.

### Bloque E — Bankroll inteligente

Depende del Bloque D (sin EV real, no hay señal que gestionar). Objetivo: primera implementación real de `app/services/` para bankroll — hoy solo existe como especificación de agente (`bankroll-manager.md`).

### Bloque F — Automatización

Último bloque, depende de que A-E ya produzcan una señal estable. Objetivo: montar el router de `app/api/` en `app/main.py` (pendiente desde `BUILD-026`), automatizar el flujo predicción → registro (`data/predictions/`) → resultado (`data/results/`) → auditoría (`data/audit/`), hoy completamente manual.

---

## 6. Criterios para cerrar la Fase II

Condiciones objetivas, **sin fijar ningún número arbitrario** — cada una indica explícitamente qué métrica queda pendiente de definir con evidencia real, nunca por conveniencia:

| Criterio | Métrica que deberá definirse (pendiente, no fijada aquí) |
|---|---|
| Cobertura suficiente | % mínimo de partidos evaluables sobre el total real disponible — a definir cuando el Bloque A tenga resultados, con el mismo rigor ya usado en `VALID-003` para medir cobertura, nunca un número elegido a priori |
| ROI positivo sostenido | Umbral de ROI y ventana temporal mínima de sostenimiento — requiere que exista, por primera vez, un historial real en `data/results/`/`data/audit/` (hoy vacíos) |
| EV positivo | Umbral de EV agregado y tamaño de muestra mínimo — depende de que el Bloque D ya haya producido evidencia real, no simulada |
| Backtesting estable | Mismo criterio de aceptación ya validado en `VALID-002`/`VALID-004` ("mejora la mayoría de métricas, ninguna se degrada"), aplicado de forma consistente en cada cierre de bloque |
| Empates correctamente modelados o justificados | Umbral de recall aceptable, **o** una justificación cuantitativa explícita (ya adelantada por `ANL-004`: el "piso de Poisson") de por qué ese recall no puede mejorar más con esta arquitectura — cualquiera de las dos formas es un cierre válido, nunca "sin resolver y sin explicar" |
| Calibración aceptable | Métrica de calibración a elegir (ej. *reliability diagram*, *Expected Calibration Error*) y umbral — ninguna de las dos existe todavía en el proyecto, quedan para el Bloque B |
| Modelo listo para producción | Router HTTP montado, persistencia poblada con predicciones/resultados reales, al menos un ciclo completo predicción→resultado→auditoría ejecutado de punta a punta — condición binaria, no requiere un umbral numérico nuevo |

**Regla de cierre:** la Fase II se declara cerrada únicamente cuando cada fila de esta tabla tenga, además de evidencia real, una decisión explícita del Arquitecto Estadístico Humano confirmando que el umbral alcanzado es aceptable (Constitución, Art. 2/5) — igual que cada cierre de misión ya lo exigió durante toda la Fase I.

---

## 7. Criterios para iniciar la Fase III (Clubes)

**La incorporación de clubes NO pertenece a la Fase II.** Solo podrá iniciarse cuando la Fase II esté **oficialmente cerrada** conforme a los criterios de la sección 6 — nunca en paralelo, nunca como atajo si la Fase II se estanca.

La Fase III implica, como mínimo, los siguientes cambios estructurales que la justifican como una fase propia, no una extensión de la Fase II:

- **Nueva arquitectura de datos** — clubes no son selecciones nacionales; el módulo `selecciones-nacionales/` de `data/processed/` no es directamente reutilizable sin rediseño.
- **Nuevas competiciones** — ligas domésticas, copas nacionales, competiciones continentales de clubes (Champions League, Copa Libertadores, etc.), con calendarios y formatos distintos a los torneos ya modelados.
- **Nuevos calendarios** — temporadas de liga (partido a partido, muchos más partidos por equipo) frente a torneos cortos concentrados, cambiando por completo la ventana `N` de Variable001/003/004/007.
- **Nuevos modelos de fatiga** — clubes juegan múltiples competiciones simultáneas (liga + copa + continental), un patrón de acumulación de fatiga que `models/fatiga.md` (alcance reducido, diseñado para selecciones) no cubre.
- **Nuevos modelos de rotación** — plantillas de club rotan jugadores entre competiciones de forma sistemática, sin equivalente en el fútbol de selecciones.
- **Nuevos modelos de localía** — estadios propios fijos por temporada completa (a diferencia de las sedes de torneo, ya de por sí con `KAPPA` sin calibrar en el modelo actual).

**Versionado:** la incorporación de clubes será considerada, oficialmente, la versión **`v2.0.0`** del Modelo Santiago — consistente con el criterio de Versionado Semántico ya aplicado en `v1.1.0` (`CHANGELOG.md`): un cambio de esta magnitud, aunque técnicamente aditivo en el sentido de que no rompe ningún contrato público existente, representa un salto de dominio lo bastante grande (selecciones → selecciones + clubes) como para merecer la version MAYOR, a diferencia del salto `1.0.0→1.1.0` (que fue exclusivamente funcionalidad aditiva dentro del mismo dominio ya existente).

---

## Cierre obligatorio

**1. ¿Documento creado?** Sí — `docs/39-Fase-II.md` (no `docs/11-Fase-II.md`, ver "Nota de numeración").

**2. ¿Secciones incluidas?** Las 7 exigidas por el brief: Objetivo de la Fase II, Estado heredado de la Fase I, Problemas abiertos, Principios de la Fase II, Roadmap, Criterios para cerrar la Fase II, Criterios para iniciar la Fase III — más la "Nota de numeración" (obligatoria antes de escribir, `docs/22` §3) y este cierre.

**3. ¿Roadmap definido?** Sí — 6 bloques (A: Cobertura, B: Calibración, C: Mercados, D: EV, E: Bankroll inteligente, F: Automatización), en orden de dependencia real, cada uno con su condición de entrada explícita.

**4. ¿Problemas abiertos documentados?** Sí — 7, todos con cita directa a la misión que los midió (`VALID-001` a `004`, `ANL-001`/`004`, `CAL-002`) — ninguno inventado.

**5. ¿Criterios de cierre definidos?** Sí, como condiciones cualitativas objetivas — sin ningún número arbitrario; cada fila indica explícitamente qué métrica queda pendiente de fijar con evidencia real.

**6. ¿Criterios para iniciar Clubes definidos?** Sí — condicionados al cierre oficial de la Fase II, con los 6 cambios estructurales que lo justifican como `v2.0.0`.

**7. ¿Archivos modificados?** `docs/39-Fase-II.md` (nuevo), `CHANGELOG.md`, `docs/00-Project-Tracker.md`. Ningún archivo de `app/`, `engine/`, CSV, Variable, peso ni fórmula.

**8. ¿CHANGELOG actualizado?** Sí (ver `CHANGELOG.md`, entrada `FII-001`).

**9. ¿Project Tracker actualizado?** Sí (ver `docs/00-Project-Tracker.md`, entrada `FII-001`).

**10. ¿Primera misión recomendada de la Fase II (`FII-002`)?** Un diagnóstico de cobertura (Bloque A): determinar qué fuentes de datos reales existen para ampliar `estadisticas_partido.csv`/`partidos.csv` más allá de Eurocopa/Copa América — empezando por Mundial 2026 y Eliminatorias, ya identificadas como sin cobertura de StatsBomb desde `VALID-001`, nunca resuelto. Es la base de la que dependen, en cadena, los Bloques B-F — cualquier otra prioridad se mediría hoy sobre una muestra que la propia Fase I ya demostró insuficiente (`N=35`, `28.2%` de cobertura).

---

Fin del documento.
