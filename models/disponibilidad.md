# Disponibilidad de Plantilla — Variable006 (alcance reducido V1)

**Archivo:** `models/disponibilidad.md`

**Misión:** MODEL-015 — Especificación Matemática Oficial de Variable006 (Disponibilidad)

**Versión:** 1.0.0-investigación

**Estado:** Investigación — primer documento de `models/` dedicado a Variable006 (no evoluciona un stub, se crea desde cero, mismo patrón que `MODEL-005`/`MODEL-011`/`MODEL-012`/`MODEL-013`/`MODEL-014`)

---

## Nota de origen y alcance exacto de esta misión

Variable006 (Disponibilidad de Plantilla) tiene, según `docs/03-Variables.md`, tres señales: "Lesiones", "Suspensiones", "Rotaciones". `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) ya evaluó su disponibilidad de dato (`docs/27-Auditoria-de-Variables-Pendientes.md`, sección Variable006) y concluyó: "Lesiones" es categoría A (100% derivable de `lesiones.csv` hoy mismo); "Suspensiones" es categoría B (`convocatorias.csv.estado_convocatoria` existe, pero sus valores ENUM permitidos nunca se formalizaron); "Rotaciones" es categoría D (no existe ninguna tabla de alineación titular por partido). `docs/36` autoriza explícitamente: **"Implementable en V1 con alcance reducido (solo 'Lesiones', categoría A), mismo patrón que `MR-004` ya aplicó a Variable008"**. Esta misión especifica exactamente ese alcance reducido — no Variable006 completa. Se responde de forma explícita, como exige el brief: **Variable006 completa (con "Suspensiones" y "Rotaciones") no puede especificarse ni calcularse con el esquema de datos actual** — sección 10 desarrolla este hallazgo con evidencia directa.

Ningún documento de arquitectura funcional (`docs/17-Matriz-de-Consumo-de-Variables.md`) fija todavía una fuente y forma exactas para Variable006, a diferencia de Variable008 (`MODEL-013`, que ya partía de "conteo, sin fórmula fijada"). Esta misión, por lo tanto, fija tanto la fuente/forma como la fórmula matemática — mismo nivel de trabajo que `MODEL-011`/`MODEL-012`/`MODEL-014` hicieron para sus respectivas variables.

---

# 1. Objetivo

Definir la fórmula matemática completa que transforma "Lesiones" en el índice `Disponibilidad_Plantilla` (0-100) que `VariablePreparation` podrá implementar para Variable006 en su alcance reducido V1, eliminando el estado "método pendiente" (`docs/03`, `docs/28`: "Pendiente") para esa señal — sin implementar código, sin modificar el Runtime, `PredictionContext`, `Engine01`, `Engine02`, `Engine04`, `Engine05` ni `VariablePreparation`.

---

# 2. Definición operacional exacta

**Disponibilidad de Plantilla**, en su alcance reducido V1, mide el porcentaje de la plantilla convocada por un equipo a un torneo específico que **no tiene una lesión activa** en la fecha del partido a predecir. Esta es, literalmente, la definición ya fijada por la máxima autoridad documental disponible para esta variable — `docs/16-Contrato-Oficial-de-Variables.md`, línea 86: **"Disponibilidad de Plantilla = % de la plantilla convocada disponible"** — esta misión no la reinterpreta, solo la opera-cionaliza con el único dato hoy autorizado y derivable ("Lesiones").

**Convención de dirección:** valores altos de `Disponibilidad_Plantilla` representan **mayor** disponibilidad (mejor estado), consistente con `models/confidence.md` §5 ("Disponibilidad de Plantilla: a menor disponibilidad, menor confianza") y `models/chaos-index.md` §6 ("Variable006: más lesiones/bajas → mayor caos"). Es la misma dirección que Variable008 (alto = mejor) y la dirección opuesta a Variable007/Fatiga (alto = peor, `models/fatiga.md` §2).

No mide "Suspensiones" ni "Rotaciones" (sección 10) ni ningún otro insumo no autorizado por `docs/03` — es, exclusivamente, una medida de disponibilidad física de la plantilla convocada por ausencia de lesión activa.

---

# 3. Problema que resuelve

`docs/03`/`docs/28` marcan Variable006 con "Método: Pendiente" pese a que una de sus tres señales ("Lesiones") ya es 100% derivable hoy sin ninguna captura nueva (`docs/27`, `docs/36`/`GR-010`) — es, de hecho, la única señal categoría A (dato completo: tipo, gravedad, fechas, estado) de las tres. Sin una fórmula matemática oficial, `VariablePreparation` no puede publicar Variable006 con dato real aunque el alcance reducido y la fuente ya estén disponibles — la misma brecha que `MODEL-011`/`MODEL-012`/`MODEL-013`/`MODEL-014` ya cerraron para Variable001/002/008/007. `GR-010` (`docs/36`) recomienda esta investigación como la prioridad inmediatamente posterior a `MODEL-014`, y advierte, con razón: Variable006 es la variable con más consumidores directos de las 12 (`engine/01`, `02`, `04`, `05` — `docs/17` sección 10) — cerrar su método desbloquea metodológicamente el mayor número de motores de una sola vez.

---

# 4. Fundamento — por qué un porcentaje directo, sin z-score/Φ, y por qué se evita la columna `estado` de `lesiones.csv`

**Por qué un porcentaje directo (sin z-score/Φ, a diferencia de Variable003/004/007-Descanso/008):** `docs/16` ya fija el significado exacto de Variable006 como una **proporción real medible** ("% de la plantilla convocada disponible"), no un índice relativo a una población de comparación. A diferencia de Variable003/004 (métricas de tiro sin escala natural, `MODEL-009`/`MODEL-010`) o de Variable007-Descanso (días sin escala natural, `MODEL-014`), aquí el numerador y el denominador ya son conteos directos de la misma naturaleza (jugadores convocados, jugadores lesionados) — el cociente cae en `[0,100]` por construcción aritmética, mismo principio ya aplicado por `MODEL-011`/`MODEL-012` (`Forma_Reciente`, `Rendimiento_Torneo`) a proporciones ya acotadas. Introducir un z-score aquí sería una complejidad adicional sin ninguna base documental que la exija (`CLAUDE.md`: "si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse").

**Por qué NO se usa `lesiones.csv.estado` para determinar si una lesión está activa (hallazgo explícito, verificado antes de escribir):** `docs/33-Modelo-Fisico-PostgreSQL.md` (§4.10) tipa `estado` como `TEXT (CHECK ENUM)`, pero **ningún documento del proyecto enumera sus valores permitidos** — mismo vacío de gobernanza de datos ya detectado por `MODEL-013` §10 para `posicion_principal`/`posicion_convocatoria`, y por `docs/27`/`GR-010` para `estado_convocatoria`. El único valor de `estado` confirmado textualmente en cualquier documento es `"recuperado"` (`data/processed/selecciones-nacionales/README.md`, restricción: *"`fecha_retorno_real` solo si `estado = recuperado`"*) — ningún documento nombra el valor complementario (ej. "activa"/"en curso"/"lesionado"). Filtrar por un valor de texto no confirmado (ej. comparar `estado != "recuperado"`) sería la única alternativa basada en texto, pero **no es necesaria**: las tres columnas de fecha de `lesiones.csv` (`fecha_inicio`, `fecha_estimada_retorno`, `fecha_retorno_real`) ya son suficientes, por sí solas, para determinar si una lesión cubre la fecha del partido a predecir, sin depender de ningún valor de texto sin formalizar. Esta misión, por lo tanto, **no usa la columna `estado` en absoluto** — reduce el riesgo de gobernanza de datos a cero para esta señal, en lugar de solo documentarlo como limitación no bloqueante (a diferencia de `MODEL-013`, que sí tuvo que aceptar ese riesgo para la agrupación por posición, sin una alternativa numérica disponible).

**Por qué no se necesita `jugadores.csv` (a diferencia de Variable008/`MODEL-013`):** `lesiones.csv.id_jugador` ya vincula directamente con `convocatorias.csv.id_jugador` — ningún atributo adicional del jugador (posición, nombre, fecha de nacimiento) es necesario para esta señal. `docs/03` no lista ningún dato de `jugadores.csv` entre los "Datos necesarios" de Variable006.

**Por qué no se necesita `partidos.csv`:** la fecha del partido a predecir ya está disponible directamente en `context.match.fecha` (`docs/30` §4.2) — no se requiere ninguna consulta adicional a `partidos.csv` para obtenerla, a diferencia de Variable007 (`MODEL-014`), que sí necesita ese archivo para localizar el partido anterior de cada equipo.

---

# 5. Fuente de datos

| Dato | Archivo | Columna | Rol |
|---|---|---|---|
| Convocatoria del equipo al torneo específico | `convocatorias.csv` | `id_torneo`, `id_seleccion`, `id_jugador` | Define la plantilla convocada (`Convocados`), mismo criterio de fuente ya usado por Variable008 (`MODEL-013` §5) |
| Ventana de la lesión | `lesiones.csv` | `id_jugador`, `fecha_inicio`, `fecha_estimada_retorno`, `fecha_retorno_real` | Determina si un jugador convocado tiene una lesión activa en la fecha del partido a predecir (sección 6) |
| Identificación del partido a predecir | `context.match` (`docs/30` §4.2) | `torneo`, `fecha` | Ya disponible directamente en `PredictionContext`, sin consulta adicional a `partidos.csv` |

**No se usa** `jugadores.csv` ni `partidos.csv` (sección 4) — ninguno de los dos aporta un dato que esta señal necesite. **No se usa** `lesiones.csv.tipo_lesion`/`gravedad`: `docs/03`/`docs/16` no piden ponderar el impacto de una lesión por su tipo o severidad para Variable006 (a diferencia de lo que su justificación en el README del módulo de datos sugiere posiblemente para una versión futura, sección 20) — en el alcance reducido V1, cada lesión activa cuenta igual, sin distinción de gravedad, mismo criterio de "no inventar una ponderación sin evidencia" ya aplicado en toda la investigación de este proyecto. **No se usa** `lesiones.csv.estado` (sección 4, hallazgo explícito) ni `lesiones.csv.fuente`/`id_partido_origen` (trazabilidad, sin rol en el cálculo).

---

# 6. Fórmula oficial V1

```
Sea Tor = context.match.torneo (resuelto a id_torneo), F = context.match.fecha
Sea T el equipo evaluado (local o visitante)

Convocados(T, Tor) = { id_jugador distintos : fila en convocatorias.csv
                        con id_torneo = Tor, id_seleccion = T }

Para cada lesión L de lesiones.csv con id_jugador ∈ Convocados(T, Tor):

    fecha_fin_efectiva(L) = fecha_retorno_real(L)          si está presente
                           = fecha_estimada_retorno(L)      si no, y esta sí está presente
                           = indefinida (sin cota superior)  si ninguna de las dos está presente

    L cubre F  ⟺  fecha_inicio(L) ≤ F
                   Y (fecha_fin_efectiva(L) es indefinida  O  F ≤ fecha_fin_efectiva(L))

Lesionados_activos(T, Tor, F) = |{ j ∈ Convocados(T, Tor) :
    existe al menos una lesión L de j que cubre F }|

Disponibilidad_Plantilla(T) = 100 · (|Convocados(T, Tor)| − Lesionados_activos(T, Tor, F))
                                    / |Convocados(T, Tor)|
```

Definida solo si `|Convocados(T, Tor)| > 0` (sección 11). Ningún peso, ningún z-score, ninguna transformación estadística — proporción directa, ya acotada `[0,100]` por construcción aritmética (`0 ≤ Lesionados_activos ≤ |Convocados|`, sección 9), mismo principio que `Forma_Reciente`/`Rendimiento_Torneo` (`MODEL-011`/`MODEL-012`).

**Por qué `fecha_fin_efectiva` prioriza `fecha_retorno_real` sobre `fecha_estimada_retorno`:** `fecha_retorno_real`, cuando existe, es el dato observado (el jugador ya regresó, en la fecha real registrada) — estrictamente más confiable que una estimación hecha en el momento de la lesión. `fecha_estimada_retorno` se usa únicamente como respaldo mientras no exista un retorno real confirmado (mismo principio de "preferir el dato observado sobre el estimado" que cualquier metodología estadística rigurosa exigiría, sin necesitar cita externa adicional — es una regla de precedencia entre dos columnas del mismo esquema, no una fórmula estadística nueva).

**Por qué una lesión sin ninguna fecha de retorno (ni real ni estimada) se trata como "sin cota" (activa indefinidamente desde `fecha_inicio`), y no se descarta:** no existe evidencia de que el jugador haya vuelto a estar disponible — tratar la ausencia de una fecha de retorno como "disponible" inventaría una recuperación no registrada, violando `CLAUDE.md` ("nunca inventes información"). Tratarla como "aún activa" es la única lectura que no asume nada no observado en los datos (documentado también como limitación, sección 16).

---

# 7. Variables internas / Métricas necesarias

- `Convocados(T, Tor)`: conjunto de `id_jugador` distintos convocados por `T` al torneo específico del partido a predecir.
- `fecha_fin_efectiva(L)`: fecha de retorno real o estimada de una lesión, con la regla de precedencia de la sección 6.
- `Lesionados_activos(T, Tor, F)`: conteo de convocados con al menos una lesión que cubre `F`.
- `Disponibilidad_Plantilla(T)`: resultado final, `[0,100]`.

Ninguna métrica adicional: no tipo de lesión, no gravedad, no posición, no edad — ninguno autorizado por `docs/03`/`docs/16` para esta señal en su alcance reducido.

---

# 8. Ventana temporal

**Ninguna de las tres opciones literales del brief aplica sin matización — se responde con la que sí está respaldada por la evidencia del esquema:**

- **"¿Solo convocatoria del partido?"** No existe ese concepto en el esquema actual: `convocatorias.csv` es a nivel de **torneo**, no de partido individual (`docs/36`/`GR-010`, mismo hallazgo ya usado para descartar "Rotaciones", sección 10) — no hay una convocatoria distinta por cada partido dentro de un mismo torneo.
- **"¿Última convocatoria?"** Ambiguo sin una fuente adicional: "última" respecto a qué referencia temporal, y de qué torneo — introduciría una interpretación no respaldada por ningún documento.
- **"¿Acumulado?"** No aplica a una señal de disponibilidad puntual: acumular convocatorias de múltiples torneos mezclaría plantillas de eras/competiciones distintas, sin ningún fundamento en `docs/03`/`docs/16`.

**Respuesta correcta, con evidencia:** la convocatoria del **torneo específico** del partido a predecir (`context.match.torneo`, resuelto a `id_torneo`) — exactamente el mismo criterio ya establecido y aprobado para Variable008 (`MODEL-013` §8: "la convocatoria es una fotografía única por torneo, no una serie temporal"). No hay ventana de `N` partidos que fijar: la convocatoria es una fotografía única, y la fecha del partido a predecir (`F`) se usa únicamente para evaluar qué lesiones están activas en ese instante puntual (sección 6) — no para definir una ventana de partidos históricos, mismo tipo de uso puntual de una fecha ya validado por `MODEL-014` §10 para Fatiga.

---

# 9. Normalización

Rango de salida: **0 a 100**, acotado por construcción aritmética (`0 ≤ Lesionados_activos(T,Tor,F) ≤ |Convocados(T,Tor)|`, por lo que el cociente ya cae en `[0,1]` sin necesidad de `clip`) — consistente con `docs/16` (Variable006: "Porcentaje (0-100)"). A diferencia de Variable003/004/007-Descanso/008, no depende de `Φ` ni de ninguna transformación estadística.

---

# 10. Suspensiones y Rotaciones — por qué quedan fuera de esta especificación (hallazgo explícito, respuesta directa a la restricción del brief)

**Suspensiones — categoría B (`docs/27`):** `convocatorias.csv.estado_convocatoria` existe como campo, pero sus valores ENUM permitidos **nunca se formalizaron** en ningún documento del proyecto — no está confirmado que `"suspendido"` (o cualquier otro valor) sea uno de sus valores válidos. Filtrar por un valor de texto no verificado arriesgaría descartar o incluir convocados por un criterio inventado — mismo riesgo, y misma decisión de no filtrar por ese campo, ya tomada por `MODEL-013` §5 para Profundidad de Plantilla (que, por esa misma razón, cuenta *toda* fila de `convocatorias.csv` sin filtrar por `estado_convocatoria`). Esta misión hereda esa misma prudencia: no inventa el valor "suspendido", y por lo tanto no puede excluir a un jugador suspendido de `Convocados` ni contarlo como no disponible.

**Rotaciones — categoría D (`docs/27`):** no existe ninguna tabla de alineación titular por partido — `convocatorias.csv` es a nivel de *torneo* (quién fue convocado), no de *partido* (quién efectivamente jugó ese partido específico); sin esa tabla, no puede derivarse qué jugadores rotaron entre partidos. `docs/36`/`GR-010` ya lo confirma: "Rotaciones... requiere una tabla nueva de alineación por partido, ninguna planeada todavía."

**Conclusión explícita exigida por el brief:** **Variable006 completa, con sus tres señales ("Lesiones", "Suspensiones", "Rotaciones"), no puede especificarse ni calcularse con el esquema de datos actual.** Esta misión no inventa un ENUM de suspensión ni una tabla de alineación por partido — se detiene explícitamente en ambos puntos, cumpliendo las restricciones del brief ("No inventar suspensiones", "No asumir información que la Base de Conocimiento no tenga"). Lo que sí queda completamente especificado, y es la única fracción de Variable006 con evidencia suficiente hoy, es el **alcance reducido de una señal** ("Lesiones") — mismo patrón de alcance parcial ya aplicado por `MR-004`/`MODEL-013` a Variable008 y por `MODEL-014` a Variable007.

**Vía de resolución futura, no aplicada aquí:** (1) Suspensiones se resolvería formalizando el ENUM de `estado_convocatoria` — trabajo documental, sin captura nueva (`docs/36`); (2) Rotaciones requeriría una tabla nueva de alineación por partido (`id_partido` × `id_jugador` × titular/suplente, como mínimo) — la misma tabla que `docs/36` ya sugiere podría resolver simultáneamente "Minutos jugados" de Variable007 (ambas son estadísticas a nivel jugador-partido, `MODEL-014` §11).

---

# 11. Casos límite

| Caso | Comportamiento |
|---|---|
| Equipo sin ninguna fila en `convocatorias.csv` para el torneo específico (`Convocados` vacío) | `disponible = False` — nunca un valor inventado |
| Jugador convocado sin ninguna fila en `lesiones.csv` | Se cuenta como disponible (sin evidencia de lesión) — nunca se asume una lesión no registrada |
| Lesión con `fecha_inicio` no parseable | Se descarta esa fila individual de lesión — no invalida el resto de la convocatoria ni las demás lesiones del mismo jugador |
| Lesión con `fecha_inicio` posterior a `F` (lesión futura respecto al partido a predecir) | No cubre `F` — no cuenta como activa (sección 6) |
| Lesión sin `fecha_retorno_real` ni `fecha_estimada_retorno` (ninguna cota de fin) | Tratada como activa indefinidamente desde `fecha_inicio` — nunca se asume una recuperación no registrada (sección 6, limitación documentada en sección 16) |
| Jugador con varias lesiones simultáneas o superpuestas que cubren `F` | Cuenta una sola vez en `Lesionados_activos` (conteo por jugador, no por lesión) — nunca se resta más de una vez al mismo convocado |
| Fila de `lesiones.csv` cuyo `id_jugador` no aparece en la convocatoria evaluada | Se ignora para este cálculo — no afecta a `T` si el jugador no fue convocado por `T` a ese torneo |
| Resultado fuera de `[0,100]` (no debería ocurrir por construcción) | Se descarta como fallo de cálculo, `disponible = False`, registrado como error — mismo criterio que `MODEL-009`/`010`/`013`/`014` |

---

# 12. Complejidad computacional

**Precalculable, `O(C_Tor + L)`** — donde `C_Tor` es el número de convocados de `T` al torneo específico (`O(C_Tor)`, una pasada sobre `convocatorias.csv` restringida a `id_torneo`/`id_seleccion`) y `L` es el total de filas de `lesiones.csv` (`O(L)`, una pasada para indexar lesiones por `id_jugador`). Sin ventana de `N` partidos, sin población de comparación entre selecciones, sin `Φ` — es la **más simple** de las variables de rendimiento especificadas hasta ahora, incluso más simple que Variable008/Profundidad (`MODEL-013`, que sí necesita `z`/`Φ` sobre una población de selecciones del mismo torneo).

---

# 13. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable006 podría pasar de "Método: Pendiente" a "definido (alcance reducido: Lesiones), ver `models/disponibilidad.md`" — actualización editorial futura, fuera de alcance de esta misión de `models/` |
| `docs/16-Contrato-Oficial-de-Variables.md` | Sin cambios — su definición literal ("% de la plantilla convocada disponible") es la autoridad que esta misión opera-cionaliza, no redefine |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Sin cambios — ya asigna Variable006 a `engine/01`, `02`, `04`, `05`; esta especificación no amplía ni reduce ese consumo |
| `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) | Sin cambios — confirma que "Lesiones" es categoría A y "Suspensiones"/"Rotaciones" son categorías B/D, consistente con esta especificación |
| `docs/28-Catalogo-de-Variables-Derivadas.md` | Disponibilidad de Plantilla (Var006) podría pasar de "Pendiente" a "Definida (alcance reducido)" — actualización editorial futura, no aplicada aquí |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Sin cambios — confirma que `context.match.torneo`/`fecha` están siempre disponibles, compatible sin ajustes con esta especificación |
| `docs/33-Modelo-Fisico-PostgreSQL.md` | Sin cambios — confirma el tipo `TEXT (CHECK ENUM)` de `lesiones.estado` y la ausencia de sus valores permitidos formalizados (sección 4), motivo por el cual esta especificación evita esa columna por completo |
| `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) | Resuelve la investigación matemática que esa misión recomendó explícitamente como siguiente prioridad tras `MODEL-014` |
| `models/profundidad-plantilla.md` (`MODEL-013`) | Sin cambios — se reutiliza su convención de "convocatoria del torneo específico" (sección 8) y su decisión de no filtrar por `estado_convocatoria` (sección 10) |
| `models/fatiga.md` (`MODEL-014`) | Sin cambios — se reutiliza su patrón de "declarar explícitamente no implementable" para una señal sin fuente de datos (sección 10), y su uso puntual de una fecha de referencia sin ventana de `N` (sección 8) |
| `models/confidence.md`, `models/chaos-index.md` | Sin cambios — confirman la convención de dirección de `Disponibilidad_Plantilla` ("a menor disponibilidad, menor confianza"; "más lesiones/bajas → mayor caos") ya usada aquí (sección 2) |
| `models/parameter-calibration.md` | Sin cambios — ya cataloga `w_D` (peso de Disponibilidad dentro de `Pen`, `MODEL-001`/`002`) como parámetro de otro nivel, distinto de esta fórmula interna, que no introduce ningún peso nuevo que catalogar |
| `app/preparation/preparation.py` | Consumidor directo en una futura `BUILD-024`, mismo patrón ya validado por `BUILD-018` a `BUILD-023` |

---

# 14. Impacto

Una vez que esta especificación sea revisada y aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5 — nunca autoaprobada por el Arquitecto Estadístico IA):

- **`VariablePreparation` podría implementar el cálculo real de Variable006 en su alcance reducido** en una futura `BUILD-024`, siguiendo exactamente la fórmula de la sección 6 y los casos límite de la sección 11 — sin ninguna decisión de diseño pendiente para ese alcance.
- **Es la variable con más consumidores directos de las 12** (`engine/01`, `02`, `04`, `05` — `docs/17` sección 10) — cerrar su método desbloquea metodológicamente el mayor número de motores de una sola vez, de todas las especificaciones de `models/` completadas hasta ahora.
- **No desbloquea, por sí sola, ninguna ejecución real** — `convocatorias.csv`/`lesiones.csv` siguen con 0 filas reales hoy (verificado antes de escribir, mismo estado que el resto de la Base de Conocimiento de Selecciones Nacionales salvo `selecciones.csv`/`competiciones.csv`/`torneos.csv`). El impacto inmediato es metodológico, no de datos — mismo matiz honesto que `MODEL-009`/`010`/`011`/`012`/`013`/`014`.
- **Con esta especificación, las 9 Variables Oficiales activas de V1 quedan, por primera vez, todas con un veredicto explícito de implementabilidad** (con o sin alcance reducido) — solo Variable009 permanece bloqueada exclusivamente por un problema de esquema (`ValorVariable.valor: float | None`), no de método ni de dato.

---

# 15. Ventajas

- Reutiliza la definición literal ya fijada por `docs/16` ("% de la plantilla convocada disponible") en lugar de reinterpretarla — máxima fidelidad documental posible.
- Es la especificación matemáticamente más simple de las variables de rendimiento operacionalizadas hasta ahora (sección 12) — sin z-score, sin `Φ`, sin población de comparación, sin ventana de `N`.
- Elimina por completo el riesgo de gobernanza de datos que sí afectó a `MODEL-013` (posiciones sin ENUM formalizado): al basar la actividad de una lesión enteramente en columnas de fecha (`DATE`, sin ambigüedad de valores permitidos), evita depender de `lesiones.csv.estado` (`TEXT CHECK ENUM` sin valores formalizados, sección 4).
- No requiere ninguna fuente de datos nueva ni ninguna tabla adicional — se deriva enteramente de `convocatorias.csv`/`lesiones.csv`, ya existentes en el esquema aprobado.
- Deja "Suspensiones" y "Rotaciones" explícitamente fuera, con un hallazgo documentado y verificable para cada una, en lugar de aproximarlas con un valor no autorizado.

---

# 16. Limitaciones

- **Lesiones sin ninguna fecha de retorno (ni real ni estimada) se tratan como activas indefinidamente** (sección 6) — puede sobreestimar la duración real de una lesión si el dato de retorno simplemente no se capturó, en lugar de no haber ocurrido todavía.
- **No pondera por gravedad ni tipo de lesión** (sección 5) — una lesión leve y una grave cuentan igual en el alcance reducido V1; ninguna evidencia respalda hoy una ponderación diferenciada.
- **No excluye "Suspensiones" ni "Rotaciones"** (sección 10) — la limitación central de esta misión, ya extensamente documentada y no bloqueante para el alcance reducido.
- **No valida integridad referencial contra `jugadores.csv`** (a diferencia de Variable008/`MODEL-013`, que sí la necesitaba para posición) — esta señal no requiere ese archivo en absoluto, por lo que un `id_jugador` inexistente en `jugadores.csv` no afecta el cálculo de Disponibilidad, aunque sí podría indicar un problema de calidad de datos en otra parte del esquema, fuera del alcance de esta especificación.
- **Sin datos reales hoy:** `convocatorias.csv`/`lesiones.csv` tienen actualmente 0 filas (verificado antes de escribir) — esta especificación resuelve el bloqueo metodológico, no el de datos.

---

# 17. Aplicación dentro del Modelo Santiago

Es la especificación matemática oficial que `VariablePreparation` deberá implementar para Variable006 en su alcance reducido V1 (solo "Lesiones"), alimentando `engine/01`, `engine/02`, `engine/04` y `engine/05` como variable contextual/opcional (`docs/17`). No alimenta "Suspensiones" ni "Rotaciones" (sección 10), que permanecen sin especificación matemática hasta que exista, respectivamente, un ENUM formalizado y una fuente de datos de alineación por partido.

---

# 18. Referencias

- `docs/03-Variables.md` — define las tres señales originales de Variable006 y su objetivo ("medir el impacto de bajas importantes").
- `docs/16-Contrato-Oficial-de-Variables.md` — fija el tipo/rango/significado literal de Variable006 ("% de la plantilla convocada disponible").
- `docs/17-Matriz-de-Consumo-de-Variables.md` — confirma los cuatro motores consumidores (`engine/01`, `02`, `04`, `05`) y que es la variable más compartida de las 12.
- `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) — clasificación de categoría de disponibilidad de cada señal (Lesiones A, Suspensiones B, Rotaciones D).
- `docs/33-Modelo-Fisico-PostgreSQL.md` — confirma el tipo `TEXT (CHECK ENUM)` de `lesiones.estado`/`convocatorias.estado_convocatoria` y la ausencia de sus valores permitidos formalizados.
- `docs/36-Estrategia-Oficial-de-Variables-Pendientes.md` (`GR-010`) — autoriza el alcance reducido y recomienda esta investigación como siguiente prioridad.
- `data/processed/selecciones-nacionales/README.md` — confirma el único valor de `estado` textualmente citado en cualquier documento ("recuperado") y la restricción de `fecha_retorno_real`.
- `models/profundidad-plantilla.md` (`MODEL-013`) — origen de la convención de "convocatoria del torneo específico" reutilizada aquí, y de la decisión de no filtrar por `estado_convocatoria`.
- `models/fatiga.md` (`MODEL-014`) — origen del patrón de "declarar explícitamente no implementable" para una señal sin fuente de datos, y del uso puntual de una fecha de referencia sin ventana de `N`.
- `models/confidence.md`, `models/chaos-index.md` — confirman la convención de dirección de `Disponibilidad_Plantilla`.

---

# 19. Versión 2.0 (siguiente iteración de esta investigación)

Pendiente, condicionado a datos reales suficientes y, en algunos casos, a gobernanza de datos o captura adicional:

- Formalización del ENUM de `estado_convocatoria` (recomendación ya compartida con `GR-010`) — permitiría incorporar "Suspensiones" como segunda señal.
- Captura de una tabla de alineación titular por partido (`id_partido` × `id_jugador` × titular/suplente) — permitiría incorporar "Rotaciones" como tercera señal, posiblemente la misma tabla que resolvería "Minutos jugados" de Variable007 (`MODEL-014` §20).
- Evaluación empírica de si ponderar por `gravedad`/`tipo_lesion` (ej. una lesión "grave" descuenta más que una "leve") mejora la capacidad predictiva frente al conteo binario actual — hoy descartado por falta de evidencia, no por imposibilidad; requeriría además formalizar el ENUM de `gravedad` (mismo vacío de gobernanza que `estado`, sección 4).
- Evaluación de si una lesión sin fecha de retorno (sección 16) debería tratarse de forma distinta (ej. excluir esa lesión del cálculo en lugar de tratarla como activa indefinidamente) una vez exista evidencia suficiente sobre la calidad real de captura de `fecha_estimada_retorno`/`fecha_retorno_real`.

---

# Validaciones

- **¿La fórmula usa solo datos autorizados por `docs/03` para Variable006?** Sí — únicamente "Lesiones", la única señal de categoría A confirmada por `docs/27`/`docs/36`. "Suspensiones" y "Rotaciones" quedan explícitamente fuera (sección 10).
- **¿Se fija algún peso sin justificar?** No — la fórmula es un cociente directo de conteos, sin ningún peso, z-score ni transformación estadística (sección 4, sección 6).
- **¿Se inventó alguna lesión, suspensión o fuente de datos?** No — se verificó explícitamente que ninguna lesión se infiere de la ausencia de dato (sección 11: sin evidencia de lesión, el jugador cuenta como disponible; sin fecha de retorno, se trata como activa, nunca como recuperada sin evidencia) y que ninguna suspensión se infiere de un ENUM no formalizado (sección 10).
- **¿Se introdujo alguna API externa (Transfermarkt u otra)?** No.
- **¿Es reproducible?** Sí — función determinista de las fechas de convocatoria y lesión observadas, sin aleatoriedad ni estimación subjetiva.
- **¿Se detuvo la misión por falta de rigor matemático?** Parcialmente — se detiene explícitamente para "Suspensiones" y "Rotaciones" (sección 10, exigido por el brief), pero no para el alcance reducido de una señal, que queda completamente especificado.

---

# Cierre obligatorio

**1. ¿Qué definición operacional quedó aprobada?**
Disponibilidad de Plantilla (alcance reducido) = porcentaje de la plantilla convocada al torneo específico del partido a predecir que no tiene una lesión activa en la fecha de ese partido — cita literal de `docs/16` operacionalizada con la única señal derivable hoy — sección 2.

**2. ¿Qué fuente consume?**
`convocatorias.csv` (torneo/selección/jugador convocado) y `lesiones.csv` (fechas de inicio y retorno de cada lesión) — sección 5. No usa `jugadores.csv`, no usa `partidos.csv`, no usa `lesiones.csv.estado`/`tipo_lesion`/`gravedad` (justificado explícitamente por qué no).

**3. ¿Qué métricas utiliza?**
`Convocados(T,Tor)`, `fecha_fin_efectiva` por lesión (con regla de precedencia real-sobre-estimada), `Lesionados_activos(T,Tor,F)` — sección 7. Ninguna métrica de gravedad, tipo, posición ni suspensión.

**4. ¿Qué fórmula matemática quedó definida?**
`Disponibilidad_Plantilla = 100·(|Convocados| − Lesionados_activos)/|Convocados|` — sección 6. Ningún peso, ningún z-score, ninguna `Φ`.

**5. ¿Qué rango produce?**
0 a 100, acotado por construcción aritmética — sección 9.

**6. ¿Qué casos límite contempla?**
Equipo sin convocatoria → `disponible=False`; jugador sin lesión registrada → cuenta como disponible; lesión con fecha no parseable → se descarta individualmente; lesión futura respecto a `F` → no cuenta; lesión sin ninguna fecha de retorno → activa indefinidamente; múltiples lesiones del mismo jugador → cuenta una sola vez — sección 11.

**7. ¿Qué documentos quedaron afectados?**
Solo `models/disponibilidad.md` (creado). `docs/03`, `docs/17`, `docs/28` quedan documentados como afectados a futuro por una misión editorial, ninguno modificado en esta misión de `models/` — sección 13.

**8. ¿Qué desbloqueará BUILD-024?**
El camino metodológico completo para implementar Variable006 en su alcance reducido (Lesiones) en `VariablePreparation`, mismo patrón que `BUILD-018` a `BUILD-023` — con el mayor impacto potencial de motores desbloqueados (`engine/01`, `02`, `04`, `05`, los cuatro consumidores directos ya vigentes) de todas las especificaciones completadas hasta ahora. No desbloquea, por sí solo, una predicción real — `convocatorias.csv`/`lesiones.csv` siguen con 0 filas reales hoy.

**9. ¿Queda implementable en V1?**
Sí, para el alcance reducido ("Lesiones") — la fórmula queda completamente definida, sin ningún elemento pendiente de investigación adicional para ese alcance. Variable006 **completa** (con "Suspensiones" y "Rotaciones") **no es implementable en V1**: no existe ENUM formalizado ni tabla de alineación por partido, y esta misión lo declara explícitamente en lugar de asumirlo o inventar un dato (sección 10).

**10. ¿Se actualizaron `CHANGELOG.md` y `docs/00-Project-Tracker.md`?**
Sí, ambos — ver entradas de esta misma misión (`MODEL-015`).

---

# Fuera de alcance de esta misión

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext`, `Engine01`, `Engine02`, `Engine04`, `Engine05` ni `VariablePreparation`.
- No se modifica `docs/03`, `docs/16`, `docs/17`, `docs/28`, `docs/30`, `docs/33` ni ningún otro documento existente de `docs/`.
- No se especifican "Suspensiones" ni "Rotaciones" — declaradas explícitamente no implementables con el esquema de datos actual (sección 10), no un simple diferimiento de alcance.
- No se formaliza el ENUM de `estado_convocatoria`/`estado` (lesiones) ni se diseña una tabla de alineación por partido — se documenta como hallazgo pendiente, no se resuelve aquí.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5).

---

Fin del documento.
