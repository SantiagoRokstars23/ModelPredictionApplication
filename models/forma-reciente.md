# Forma Reciente — Variable001

**Archivo:** `models/forma-reciente.md`

**Misión:** MODEL-011 — Especificación Oficial de Variable001 para V1

**Versión:** 1.0.0-investigación

**Estado:** Investigación — primer documento de `models/` dedicado a Variable001 (no evoluciona un stub, se crea desde cero, mismo patrón que `MODEL-005`/`models/chaos-index.md` para `engine/04`)

---

## Nota de origen

Variable001 (Forma Reciente) nunca tuvo un documento propio en `models/`, pese a ser Nivel A y una de las variables más compartidas del proyecto (consumida directamente por `engine/01`/`engine/02`, indirectamente por `engine/03-06`). `docs/28-Catalogo-de-Variables-Derivadas.md` ya lo confirma explícitamente: "Forma Reciente (Var001) | `docs/03`, `docs/16` | ... | **Pendiente (fórmula)**" — a diferencia de Variable003, que sí tenía una fórmula parcial en `models/offensive-strength.md` antes de `MODEL-009`. Los dos únicos lugares donde Variable001 aparece en `models/` (`offensive-strength.md` §6.2, `defensive-strength.md` §6.1) la consumen como modificador ya construido (`r = (Variable001 − 50)/50`) sin definir nunca cómo se construye. Este documento cierra esa brecha desde cero — no extiende ningún documento existente, porque ninguno define la construcción de Variable001 en sí misma (verificado por búsqueda directa en `models/` antes de escribir, igual que hizo `MODEL-005`).

---

# 1. Objetivo

Desarrollar el fundamento matemático y conceptual de Variable001 (Forma Reciente) — la base científica que permitirá a `VariablePreparation` calcularla con dato real — sin implementar código, sin modificar el Runtime, `PredictionContext`, `Engine01`, `Engine04` ni `Engine05`.

---

# 2. Definición operacional exacta

**Variable001 (Forma Reciente)** representa el rendimiento competitivo inmediato de una selección, medido como el porcentaje de puntos obtenidos (sistema estándar 3-1-0: victoria=3, empate=1, derrota=0) sobre sus últimos `N` partidos oficiales, sin distinguir tipo de competición ni ajustar por la fuerza del rival.

Responde exactamente la pregunta que `docs/03-Variables.md` ya fija para esta variable: "¿Cómo está jugando actualmente este equipo?" — no cuánto ha anotado o concedido (eso son Variable003/004), no su historia (`docs/03`: "No pretende medir la historia del club. Solo su estado deportivo reciente"), y no la calidad de sus rivales recientes (ver sección 4).

---

# 3. Problema que Resuelve

`engine/01`/`engine/02` ya declaran que Variable001 es una "Variable Secundaria" que ajusta el contexto de la producción base (`M_forma`, `models/offensive-strength.md` §6.2) — pero, hasta este documento, ningún lugar del proyecto definía qué número real debía entregar `VariablePreparation` para ese ajuste. Sin esta especificación, `M_forma` no puede calcularse con dato real aunque Variable003/004 ya lo tengan (`MODEL-009`/`MODEL-010`).

---

# 4. Fundamento y divergencia deliberada del enfoque de Variable003/004

**Por qué esta especificación NO reutiliza el mecanismo de z-score/Φ de `MODEL-009`/`MODEL-010`:** ese mecanismo existe porque `xG`/disparos/`xGA` no tienen una escala acotada natural — se necesita comparar contra la población de la competición para obtener un índice 0-100 con sentido. Los puntos de un partido (`0`, `1` o `3`) **ya están acotados por construcción**: la proporción de puntos obtenidos sobre el máximo posible es, por definición, un número en `[0, 1]`, escalable a `[0, 100]` sin ningún paso de normalización estadística adicional. Introducir aquí el mismo aparato de z-score que Variable003/004 sería una complejidad no justificada por la naturaleza del dato (`CLAUDE.md`: "Si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse") — Variable001 es, por diseño, más simple de construir que Variable003/004, no una omisión.

**Por qué no se pondera por fuerza del rival ("Rival" en `docs/03` es identificación, no ponderación):** `docs/03-Variables.md` lista "Rival" entre los "Datos necesarios" de Variable001, pero nunca dice que el resultado deba ajustarse por la fuerza de ese rival. Ajustar por calidad del rival es, explícitamente, responsabilidad exclusiva de `engine/03-Poisson.md` (`docs/17-Matriz-de-Consumo-de-Variables.md`; `models/offensive-strength.md` §3: "el ajuste por rival... pertenece a `engine/03-Poisson.md`, no a este modelo" — mismo principio, aplicado aquí a Variable001). "Rival" se usa únicamente para **identificar** el partido (confirmar que existió un oponente real registrado), nunca para ponderar el resultado.

**Por qué no se usan goles ni diferencia de gol:** `docs/03-Variables.md` distingue explícitamente los "Datos necesarios" de Variable001 ("Últimos partidos oficiales, Resultado, Rival, Competición, Fecha") de los de Variable002 ("Partidos del torneo, Victorias, Empates, Derrotas, **Goles**, Rendimiento ofensivo, Rendimiento defensivo") — "Goles" aparece únicamente en la lista de Variable002, nunca en la de Variable001. Incorporar diferencia de gol a Variable001 excedería lo que `docs/03` autoriza para esta variable específica y duplicaría, sin necesidad, una señal ya reservada a Variable002 — la separación entre "resultado puro" (Variable001) y "rendimiento detallado del torneo" (Variable002) queda así preservada, no inventada.

---

# 5. Fuente de datos

| Dato (`docs/03`) | Archivo | Columna / cálculo | Disponibilidad (`docs/27`) |
|---|---|---|---|
| Últimos partidos oficiales | `data/processed/selecciones-nacionales/partidos.csv` | `fecha` (orden cronológico), `id_torneo` (confirma partido oficial) | Categoría A — columnas existen; **0 filas** (verificado antes de escribir, mismo estado que `BUILD-017`/`018`) |
| Resultado | `partidos.csv` | Comparación `goles_local` vs. `goles_visitante`, según el lado (`local`/`visitante`) del equipo evaluado en ese partido | Categoría C — derivable |
| Rival (identificación, no ponderación — sección 4) | `partidos.csv` | `id_seleccion_local`/`id_seleccion_visitante` (el que no es el equipo evaluado) | Categoría A |
| Competición | `torneos.csv` → `competiciones.csv` | Mismo patrón de resolución que `MODEL-009`/`MODEL-010` (`id_torneo → id_competicion`) — sin tratamiento diferenciado por tipo (sección 8) | Categoría A |
| Fecha | `partidos.csv` | Orden cronológico para seleccionar los `N` partidos más recientes | Categoría A |

**No se usa `estadisticas_partido.csv`** — a diferencia de Variable003/004, ningún dato de esa tabla (`xg`, `disparos_totales`, etc.) está entre los "Datos necesarios" de Variable001 en `docs/03`. Ninguna fuente externa (ranking FIFA, Elo) — mismo principio ya fijado en `MODEL-009` §20: `docs/16` no autoriza otra fuente para ninguna Variable Oficial de rendimiento.

---

# 6. Fórmula oficial V1

Sistema de puntos estándar de fútbol (universal desde 1994, FIFA y todas las confederaciones — no una convención propia de este proyecto):

```
Para cada uno de los últimos N partidos oficiales del equipo (sección 8):

    puntos_j = 3   si el equipo ganó
    puntos_j = 1   si el equipo empató
    puntos_j = 0   si el equipo perdió

n = número de partidos válidos encontrados en la ventana (n ≤ N)

Forma_Reciente = 100 · ( Σⱼ puntos_j ) / (3 · n)
```

**Ningún peso ni coeficiente libre** — a diferencia de Variable003/004, esta fórmula no tiene ningún símbolo pendiente de calibración: es una proporción directa, determinada enteramente por los resultados observados. No hay, por tanto, ninguna cita de `models/parameter-calibration.md` que agregar a su catálogo (sección 13).

---

# 7. Variables internas

Una sola métrica cruda: el resultado de cada partido (`W`/`D`/`L`, traducido a puntos). No se requiere ninguna otra estadística (a diferencia de las 3-4 métricas de tiro que exigen Variable003/004).

---

# 8. Ventana temporal

**`N = 5` últimos partidos oficiales.** Placeholder estructural, no calibrado — elegido independientemente de `N = 10` (Variable003/004, `MODEL-009`/`MODEL-010`), **no reutilizado**: `docs/03` describe Variable001 con un énfasis explícito en lo inmediato ("solo su estado deportivo reciente", "no pretende medir la historia") más marcado que Variable003/004 ("sostenible", `models/offensive-strength.md` §2) — una ventana más corta es coherente con esa diferencia de énfasis textual, no una elección arbitraria. `N = 5` es, además, la convención más extendida en medios y proveedores de datos de fútbol para "forma reciente" ("últimos 5 partidos"), sin una única fuente académica atribuible — mismo tipo de justificación de convención pública ya usada en `MODEL-009` §22 para `N = 10`. **TODO explícito:** recalibrar `N` (`models/parameter-calibration.md` §7) en cuanto exista evidencia suficiente en `data/results/`.

**Ponderación dentro de la ventana: ninguna (todos los partidos pesan igual).** Mismo criterio ya establecido en `MODEL-009` §22 para Variable003 ("ventana simple... sin ponderar por antigüedad dentro de la ventana"): el Principio 1 de `docs/02-modelo.md` ("los datos actuales pesan más que la historia") ya queda satisfecho por el propio recorte de la ventana a `N = 5` partidos — no por una ponderación adicional dentro de ella. Introducir una media móvil o ponderación exponencial sin evidencia de que mejora el modelo violaría `CLAUDE.md` ("si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse").

**Tratamiento de amistosos y competiciones: sin distinción, mismo criterio que `MODEL-009`/`MODEL-010` §20.** "Amistosos Internacionales" (`COMP-000001`) cuenta igual que cualquier otro partido oficial registrado en `partidos.csv` — ningún documento (`docs/03`, `docs/16`) pide ponderar por tipo de competición, y esta misión no introduce esa distinción.

---

# 9. Normalización

Rango de salida: **0 a 100**, acotado por construcción aritmética (`0 ≤ Σpuntos_j ≤ 3n`, por lo que el cociente ya cae en `[0,1]` sin necesidad de `clip`) — consistente con `docs/16-Contrato-Oficial-de-Variables.md` (Variable001: "Índice (0-100)"). A diferencia de Variable003/004, no depende de `Φ` ni de ninguna transformación estadística — la acotación es una propiedad directa de la fórmula, no una garantía matemática de una función externa.

---

# 10. Estabilidad — respuesta al "Punto de especial interés"

**¿Puede derivarse una medida de dispersión/varianza de forma natural? Sí, parcialmente — con una limitación de exposición que debe declararse con la misma honestidad que el resto de este documento.**

La misma secuencia de valores `puntos_j` (`j = 1..n`) que produce la media (`Forma_Reciente`, sección 6) permite calcular, sin ningún dato adicional, su dispersión:

```
Estabilidad_Forma = desviación estándar muestral de { puntos_1, ..., puntos_n }
```

- **Definición:** cuanto menor la dispersión, más consistente el rendimiento reciente (ej. un equipo que empata sus 5 últimos partidos tiene `Estabilidad_Forma = 0`, perfectamente consistente, incluso con `Forma_Reciente` moderada); cuanto mayor la dispersión, más errático (ej. alternar victorias contundentes y derrotas). Esto es, conceptualmente, exactamente el tipo de señal que `models/chaos-index.md` §6 ya reclama para `Δ_forma` ("inestabilidad/varianza reciente") y que `models/confidence.md` §5-6 reclama para `C_forma` ("estabilidad de forma reciente... momento de segundo orden (varianza)").
- **Requiere `n ≥ 2`** para ser calculable (varianza muestral indefinida con un solo dato) — mismo tratamiento de indefinición que `σ_i(competición)` en `MODEL-009`/`MODEL-010` §24: si `n < 2`, `Estabilidad_Forma` no se calcula, no se sustituye por 0.
- **Rango:** teóricamente `[0, √3]` aproximadamente (la dispersión máxima posible de una secuencia de valores en `{0, 1, 3}` con media fija) — no se fija una escala 0-100 para esta cantidad en este documento, porque **no es Variable001**: es una cantidad derivada distinta, candidata a "Variable Derivada" propia (`docs/28`, no modificado en esta misión).

**Por qué esto NO desbloquea automáticamente los placeholders de `Engine04`/`Engine05` (limitación declarada explícitamente, no forzada):**

1. `ValorVariable` (`app/runtime/prediction_context.py`) solo tiene un campo `valor: float` por variable — Variable001 ya publica `Forma_Reciente` en ese campo (sección 6); `Estabilidad_Forma` no tiene dónde publicarse sin **modificar `PredictionContext`**, explícitamente fuera de alcance de esta misión (Restricciones del brief).
2. `docs/17-Matriz-de-Consumo-de-Variables.md` ya clasifica Variable001 como **indirecta** para `engine/05` (`BUILD-014`, Contradicción A) — el mismo bloqueo de autorización de lectura que impidió calcular `C_forma` con dato real sigue vigente; esta misión no modifica `docs/17`.
3. Publicar `Estabilidad_Forma` exigiría, como mínimo, una futura misión de gobernanza (`GR-`/`MR-`) que decida **dónde** vive esa cantidad (¿nueva Variable Derivada en `docs/28`? ¿nuevo campo en `PredictionContext`? ¿cálculo propio dentro de `Engine04`/`05` a partir del mismo historial de partidos, sin pasar por Variable001 en absoluto?) — ninguna de esas tres opciones está autorizada por el alcance de `MODEL-011`.

**Conclusión honesta:** la respuesta no es "sí, esto resuelve `Δ_forma`/`C_forma`" ni "no, es imposible" — es **"sí, la fórmula existe y queda completamente definida (arriba), pero exponerla a `Engine04`/`Engine05` requiere una misión de arquitectura adicional, no incluida ni forzada aquí"**. Se documenta como candidata de alto valor para esa futura misión (sección 14), sin fingir que esta investigación ya la resolvió.

---

# 11. Casos límite

| Caso | Comportamiento |
|---|---|
| **Equipo con menos de `N = 5` partidos oficiales disponibles** | Se usa el subconjunto disponible (`n < N`); `muestra_reducida = True` se propaga en `ValorVariable` — mismo mecanismo ya usado para Variable003/004 (`MODEL-009`/`MODEL-010` §24) |
| **Equipo con cero partidos oficiales registrados** | Variable001 se marca `disponible = False` — nunca un valor inventado. Es obligatoria (Nivel A, `docs/17`); el pipeline se detiene antes de `engine/01`/`engine/02` (`docs/06`, tabla "Manejo de errores") |
| **Selección nueva / debut** | Mismo caso que la fila anterior — sin mecanismo especial, mismo criterio ya aplicado en `MODEL-009`/`MODEL-010` |
| **Cambios recientes de entrenador** | **Sin mecanismo de detección** — no existe, en ningún archivo de `data/processed/`, un registro histórico de fechas de nombramiento de seleccionador (`selecciones.csv` solo tiene `seleccionador_actual`, un valor puntual sin historial). La ventana de `N = 5` partidos ya refleja, sin necesidad de detectar el cambio explícitamente, el rendimiento bajo el entrenador actual en cuanto se acumulen partidos dentro de la ventana — mismo principio ya aplicado a "cambio completo de plantilla" en `MODEL-009` §24 |
| **Muestras pequeñas (`n` bajo pero `> 0`)** | Cubierto por la fila de `muestra_reducida` — no hay un umbral adicional distinto: cualquier `n < N` ya activa la señal de muestra reducida, sin un segundo nivel de gravedad no solicitado por ningún documento |
| **Partido con resultado no parseable** (goles corruptos o no numéricos en una fila puntual) | Esa fila se descarta individualmente, no invalida el resto de la ventana — mismo tratamiento que una fila corrupta en `MODEL-009`/`MODEL-010` |

---

# 12. Complejidad computacional

**Puede precalcularse — más simple que Variable003/004.** No requiere ninguna agregación a nivel de competición (`μ`/`σ` de una población de rivales, `MODEL-009`/`MODEL-010` §25): la fórmula es una función directa de los propios últimos `N = 5` partidos del equipo, `O(N)` estrictamente, sin ningún término `O(M)` adicional. Es, de las cuatro Variables Oficiales operacionalizadas hasta ahora (003, 004, y esta), la de menor complejidad computacional — consistente con ser, también, la de menor complejidad matemática (sección 4).

---

# 13. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable001 podría pasar de "Método: Pendiente de definir en Algoritmo.md" a "definido, ver `models/forma-reciente.md`" — actualización editorial futura de `docs/`, fuera de alcance de esta misión de `models/` (mismo criterio que `MODEL-009`/`MODEL-010`) |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Sin cambios — ya asigna Variable001 directa a `engine/01`/`engine/02`, indirecta a `03-06`; esta especificación no amplía ni reduce ese consumo |
| `docs/28-Catalogo-de-Variables-Derivadas.md` | Podría, en una futura misión (no esta), pasar la entrada "Forma Reciente (Var001)" de "Pendiente (fórmula)" a "Diseñada", y ganar una entrada nueva para "Estabilidad de Forma" (sección 10) — ninguna de las dos se edita aquí |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Sin cambios — `forma_reciente` en `VariablesBlock` ya está tipado `float \| None`, compatible sin bloqueo de esquema con el resultado 0-100 de esta especificación |
| `app/preparation/preparation.py` (`VariablePreparation`) | Consumidor directo en una futura `BUILD-020`, mismo patrón ya validado por `BUILD-018`/`BUILD-019` |
| `models/offensive-strength.md` / `models/defensive-strength.md` | Sin cambios a sus fórmulas — pero `M_forma` (que ya consume Variable001 como `r = (Variable001−50)/50`) podría, por primera vez, recibir un valor real en lugar de un input externo sin definición propia |
| `models/chaos-index.md` / `models/confidence.md` | Sin cambios — se documenta (sección 10) que `Estabilidad_Forma` es una candidata directa para `Δ_forma`/`C_forma`, pero publicarla requeriría una misión de gobernanza aparte que decida su exposición; ninguno de los dos documentos se edita aquí |

---

# 14. Impacto

Una vez que esta especificación sea revisada y aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5 — nunca autoaprobada por el Arquitecto Estadístico IA):

- **`VariablePreparation` podría implementar el cálculo real de Variable001** en una futura `BUILD-020`, siguiendo exactamente la fórmula de la sección 6 y los casos límite de la sección 11 — mismo patrón ya validado por `BUILD-018` (Variable003) y la especificación de `BUILD-019` pendiente (Variable004, `MODEL-010`).
- **`M_forma` (dentro de `Engine01`/`Engine02`) recibiría, por primera vez, un valor real de Variable001** en lugar de depender de una variable sin fórmula propia — condicionado, igual que siempre, a que existan filas reales en `partidos.csv` (hoy sin filas, verificado antes de escribir). Mismo matiz honesto que `MODEL-009`/`MODEL-010`: el impacto inmediato es metodológico, no de datos.
- **El placeholder `C_forma = 1.0` de `Engine05`** (fijo desde `BUILD-014` por falta de una medida de varianza de Variable001) tiene, por primera vez, una fórmula candidata completamente definida (`Estabilidad_Forma`, sección 10) — pero **no queda desbloqueado por esta misión**: requiere una futura misión de gobernanza que decida cómo exponerla sin modificar `PredictionContext` fuera de este alcance.
- **El placeholder `Δ_forma = 0.0` de `Engine04`** (fijo desde `BUILD-013`, mismo motivo) queda en la misma situación exacta que `C_forma` — misma fórmula candidata, mismo bloqueo de exposición, misma necesidad de una misión de gobernanza aparte.
- **No desbloquea, por sí sola, ninguna ejecución real** — `partidos.csv` sigue sin filas reales, y esta especificación, como toda la serie `MODEL-`, es investigación pendiente de aprobación, no una implementación.

---

# 15. Ventajas

- Fórmula sin ningún peso libre — a diferencia de Variable003/004, no introduce ningún símbolo nuevo al catálogo de `models/parameter-calibration.md`.
- Menor complejidad computacional de las tres variables operacionalizadas hasta ahora (sección 12) — no requiere agregación a nivel de competición.
- Produce, como subproducto directo y sin costo adicional, una fórmula completamente especificada para una medida de estabilidad que dos motores (`Engine04`, `Engine05`) ya necesitan y hoy no tienen (sección 10) — documentada con honestidad sobre su limitación de exposición, no presentada como una solución ya aplicada.

---

# 16. Limitaciones

- El sistema de puntos 3-1-0 trata todos los empates igual, independientemente del marcador — un empate 0-0 y un empate 3-3 puntúan idéntico; esto es una propiedad conocida y aceptada del sistema de puntos estándar de fútbol, no un defecto de esta especificación.
- Un equipo que empata sistemáticamente (`puntos_j = 1` siempre) obtiene `Forma_Reciente ≈ 33`, no `50` — el punto medio de la escala (`50`) no corresponde exactamente a "un empate típico", sino a un equilibrio aproximado entre victorias y derrotas. Es una consecuencia aritmética conocida del sistema 3-1-0 aplicado a una escala 0-100, documentada aquí como limitación honesta, no oculta.
- No pondera por fuerza del rival (sección 4, decisión deliberada) — dos equipos con la misma `Forma_Reciente` pueden haber logrado sus puntos contra rivales de nivel muy distinto; esa distinción, por diseño, pertenece a `engine/03-Poisson.md`, no a esta variable.
- `N = 5` y la ausencia de ponderación temporal son placeholders sin calibrar (sección 8) — al igual que en `MODEL-009`/`MODEL-010`, ninguno tiene todavía evidencia estadística real que lo respalde.
- `Estabilidad_Forma` (sección 10) queda completamente definida matemáticamente pero sin mecanismo de exposición aprobado — limitación arquitectónica, no matemática, declarada explícitamente en lugar de forzarse.

---

# 17. Aplicación dentro del Modelo Santiago

Es la especificación matemática oficial que `VariablePreparation` deberá implementar para Variable001, alimentando directamente `M_forma` en `engine/01`/`engine/02` (`models/offensive-strength.md` §6.2, `models/defensive-strength.md` §6.1) y, transitivamente, `engine/03-06`. `Estabilidad_Forma` queda documentada como candidata directa para enriquecer `engine/04`/`engine/05` en una futura misión de gobernanza, sin comprometer a esta investigación con esa implementación.

---

# 18. Referencias

- Sistema de puntos 3-1-0: convención estándar de la FIFA y todas las confederaciones desde su adopción generalizada en la década de 1990 — no atribuible a una única fuente académica, ampliamente documentado en cualquier reglamento de competición de fútbol vigente.
- "Forma reciente" como métrica de últimos 5 partidos: convención periodística y de proveedores de datos deportivos ampliamente extendida (tablas de "forma" en medios deportivos y plataformas de estadísticas) — sin una única fuente académica atribuible, mismo tipo de justificación de convención pública ya usada en `MODEL-009` §22 para `N = 10`.
- `models/offensive-strength.md` (`MODEL-001`), `models/defensive-strength.md` (`MODEL-002`) — consumidores ya existentes de Variable001 vía `M_forma`, sin cambios en esta misión.
- `models/chaos-index.md` (`MODEL-005`), `models/confidence.md` (`MODEL-004`) — documentan la necesidad de una medida de estabilidad de Variable001 que esta misión, por primera vez, define matemáticamente (sección 10).

---

# 19. Versión 2.0 (siguiente iteración de esta investigación)

Pendiente, condicionado a datos reales suficientes en `data/results/`:

- Calibración de `N` (hoy `5`, placeholder) mediante validación cruzada contra resultados reales.
- Evaluación empírica de si una ponderación temporal dentro de la ventana (ej. exponencial) mejora la capacidad predictiva frente a la media simple — hoy descartada por falta de evidencia, no por imposibilidad.
- Diseño, en una misión de gobernanza dedicada, de cómo exponer `Estabilidad_Forma` a `Engine04`/`Engine05` sin violar el contrato actual de `PredictionContext` (sección 10) — la pieza de mayor valor pendiente de esta especificación.
- Evaluación de si "Rival" debería, con evidencia real, incorporarse como ajuste de fuerza de oponente — hoy excluido por diseño (sección 4), no por imposibilidad técnica.

---

# Validaciones

- **¿La fórmula usa solo datos autorizados por `docs/03` para Variable001?** Sí — únicamente "Resultado" (vía puntos), "Rival" (solo identificación), "Competición" y "Fecha" (sección 5); no se usan goles ni estadísticas de tiro, reservadas a Variable002/003 respectivamente.
- **¿Se fija algún peso sin justificar?** No aplica — la fórmula no tiene ningún peso libre (sección 6), a diferencia de Variable003/004.
- **¿Se reutiliza indebidamente algo de Variable003/004?** No — ni el mecanismo de z-score/Φ, ni `N`, ni ningún símbolo; toda coincidencia (ej. el valor numérico de `N` en `MODEL-009`) es una elección independiente, justificada por separado (sección 8).
- **¿Se resuelve el "Punto de especial interés" con honestidad?** Sí — sección 10 concluye explícitamente que la fórmula de estabilidad existe pero su exposición requiere una misión adicional, sin forzar ni negar la respuesta.
- **¿Es reproducible?** Sí — es una función determinista de los resultados observados, sin aleatoriedad ni estimación.

---

# Cierre obligatorio

**1. ¿Qué definición operacional quedó aprobada?**
Variable001 = porcentaje de puntos obtenidos (sistema 3-1-0) sobre los últimos `N=5` partidos oficiales de la selección, sin ajuste por rival ni por tipo de competición — sección 2.

**2. ¿Qué fuente de datos consume?**
`partidos.csv` (resultado, fecha, identificación de rival) y `torneos.csv`/`competiciones.csv` (resolución de competición) — sección 5. No usa `estadisticas_partido.csv` ni ninguna fuente externa.

**3. ¿Qué fórmula matemática quedó definida?**
`Forma_Reciente = 100 · (Σ puntos_j) / (3n)`, con `puntos_j ∈ {0,1,3}` según resultado — sección 6. Sin pesos ni coeficientes libres.

**4. ¿Qué ventana temporal utiliza?**
`N = 5` últimos partidos oficiales, sin ponderación interna, sin distinción de amistosos/competiciones — sección 8. Elegida independientemente del `N=10` de Variable003/004, justificada por el mayor énfasis de `docs/03` en lo "reciente" para esta variable específica.

**5. ¿Qué rango produce?**
0 a 100, acotado por construcción aritmética directa, sin necesidad de `Φ` ni `clip` — sección 9.

**6. ¿Puede derivarse una medida de estabilidad?**
Sí, matemáticamente: `Estabilidad_Forma` = desviación estándar muestral de los puntos por partido en la misma ventana — completamente definida en la sección 10. No puede, sin embargo, exponerse a `Engine04`/`Engine05` dentro del alcance de esta misión: requiere una futura misión de gobernanza que decida su punto de exposición sin modificar `PredictionContext`.

**7. ¿Qué casos límite contempla?**
Menos de `N` partidos → `muestra_reducida=True`; cero partidos → `disponible=False`, pipeline se detiene (Nivel A); cambios de entrenador → sin mecanismo de detección (sin fuente de datos), la ventana los refleja naturalmente; fila corrupta → se descarta sola — sección 11.

**8. ¿Qué documentos quedaron afectados?**
Solo `models/forma-reciente.md` (creado). `docs/03`, `docs/17`, `docs/28`, `docs/30`, `app/preparation/preparation.py`, `models/offensive-strength.md`/`defensive-strength.md`, `models/chaos-index.md`/`confidence.md` quedan documentados como afectados a futuro, ninguno modificado — sección 13.

**9. ¿Qué desbloquea BUILD-020?**
El camino metodológico completo para implementar Variable001 en `VariablePreparation`, mismo patrón que `BUILD-018`/`BUILD-019`. No desbloquea, por sí solo, `Δ_forma`/`C_forma` (sección 10) ni una predicción real (`partidos.csv` sigue sin filas) — sección 14.

**10. ¿Qué misión recomendarías después?**
La misma aprobación pendiente que `MODEL-009`/`MODEL-010` (Arquitecto Estadístico Humano), seguida de `BUILD-020` (implementación de Variable001, mismo patrón). En paralelo, una futura misión de gobernanza (`GR-`/`MR-`) que decida formalmente cómo exponer `Estabilidad_Forma` a `Engine04`/`Engine05` — la pieza de mayor valor identificada en esta investigación, deliberadamente no resuelta aquí.

---

# Fuera de alcance de esta misión

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext`, `Engine01`, `Engine04` ni `Engine05`.
- No se calibra `N` ni ningún otro placeholder con evidencia real.
- No se decide ni se implementa el mecanismo de exposición de `Estabilidad_Forma` a `Engine04`/`Engine05` — se documenta como pendiente, no se resuelve.
- No se actualiza `docs/03-Variables.md` ni `docs/28-Catalogo-de-Variables-Derivadas.md` — pertenece a una misión de `docs/`, no de `models/`.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano.

---

Fin del documento.
