# Auditoría Completa de Variables Pendientes

**Archivo:** `docs/27-Auditoria-de-Variables-Pendientes.md`

**Misión:** DATA-001 — Auditoría Completa de Variables Pendientes (primera misión con prefijo "DATA-")

**Versión:** 1.0.0

**Estado:** Auditoría — sin modificaciones aplicadas

---

# Objetivo

Cruzar, dato por dato, las 12 Variables Oficiales (`docs/03-Variables.md`) contra el esquema real de `data/processed/` y `data/raw/` (verificado directamente, no de memoria) para determinar qué se puede calcular hoy, qué requiere transformación, qué es derivable, qué falta capturar, y qué no vale la pena perseguir — antes de continuar con más investigación matemática (`MODEL-`).

---

# Metodología

Se leyó el encabezado real de los 11 CSV de `data/processed/selecciones-nacionales/` y se confirmó que `data/raw/` no contiene ningún archivo de datos (solo `README.md`) — por lo tanto, ningún dato "falta en `processed/` pero existe en `raw/`"; si no está en `processed/`, no está en ningún lado del repositorio hoy. Cada "Dato necesario" declarado en `docs/03-Variables.md` para las 12 variables se contrastó contra ese esquema real.

---

# Clasificación

| Categoría | Significado |
|---|---|
| **A** | Existe exactamente como campo |
| **B** | Existe pero requiere transformación o definición adicional (ej. un ENUM sin valores formalizados) |
| **C** | No existe como campo, pero es derivable matemáticamente de campos que sí existen |
| **D** | No existe y debe capturarse en una futura recolección — no hay forma de derivarlo de lo ya disponible |
| **E** | No vale la pena incluirlo (razón justificada caso por caso) |

---

# Revisión por Variable Oficial

## Variable001 — Forma Reciente (Nivel A · consumida por `engine/01`, `engine/02`, indirectamente `03-06`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| Últimos partidos oficiales | A | `partidos.csv` |
| Resultado | C | Derivable de `goles_local`/`goles_visitante` |
| Rival | A | `id_seleccion_local`/`visitante` en `partidos.csv` |
| Competición | A | `id_torneo` → `id_competicion` (join `torneos.csv`) |
| Fecha | A | `fecha` en `partidos.csv` |

**Sin elementos pendientes de nivel D o E.**

## Variable002 — Rendimiento en el Torneo (Nivel A · `engine/01`, `engine/02`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| Partidos del torneo | A | `partidos.csv` filtrado por `id_torneo` |
| Victorias/Empates/Derrotas | C | Derivable de `goles_local`/`goles_visitante` |
| Goles | A | `partidos.csv` |
| Rendimiento ofensivo | C | Agregación de `xg`/`disparos_totales` en `estadisticas_partido.csv` |
| Rendimiento defensivo | C | Mismo campo, vía self-join con el rival |

**Sin elementos pendientes de nivel D o E.**

## Variable003 — Potencial Ofensivo (Nivel A · `engine/01`, primaria)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| xG | A | `estadisticas_partido.csv.xg` |
| Disparos | A | `disparos_totales` |
| Disparos al arco | A | `disparos_al_arco` |
| **Grandes oportunidades** | **D** | No existe ningún campo equivalente en ningún CSV — ya detectado en `MODEL-001` |
| Conversión | C | Derivable: goles del equipo (`partidos.csv`) ÷ `disparos_totales` (`estadisticas_partido.csv`), vía join |

## Variable004 — Solidez Defensiva (Nivel A · `engine/02`, primaria)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| xGA | C | Self-join: `xg` del rival en el mismo `id_partido` (decisión de diseño ya documentada en MS-001, "Campo excluido") |
| Goles recibidos | C | Derivable de `partidos.csv` (goles del rival) |
| Remates permitidos | C | Self-join de `disparos_totales` del rival |
| Porterías en cero | C | Derivable: ¿goles recibidos = 0? |

**Sin elementos de nivel D — toda la variable es calculable hoy vía derivación, ninguno requiere nueva captura.**

## Variable005 — Compatibilidad Táctica (Nivel A · sin consumidor, diferida `MR-004`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| Formación | D | No existe ningún campo |
| Estilo de presión | D | No existe, sin proxy razonable |
| **Posesión** | **A** | `estadisticas_partido.csv.posesion_pct` — **hallazgo nuevo: 1 de los 5 datos de esta variable sí existe**, algo no señalado explícitamente antes de esta auditoría |
| Juego directo | D | No existe, sin proxy razonable |
| Contraataque | D | No existe, sin proxy razonable |

## Variable006 — Disponibilidad de Plantilla (Nivel B · la más consumida: `engine/01`, `02`, `04`, `05`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| Lesiones | A | `lesiones.csv` (completo: tipo, gravedad, fechas, estado) |
| **Suspensiones** | **B** | `convocatorias.csv.estado_convocatoria` existe como campo, pero **sus valores ENUM permitidos nunca se formalizaron** en ninguna misión — no está confirmado que "suspendido" sea uno de sus valores válidos |
| **Rotaciones** | **D** | No existe ninguna tabla de alineación titular por partido — `convocatorias.csv` es a nivel de *torneo*, no de partido individual; sin eso no puede derivarse qué jugadores rotaron entre partidos |

## Variable007 — Fatiga (Nivel B · `engine/01`, `02`, `04`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| Días de descanso | C | Derivable de la diferencia de fechas entre partidos consecutivos de la misma selección (`partidos.csv`) |
| **Minutos jugados** | **D** | No existe — estadística individual de jugador por partido, explícitamente diferida desde `MS-001` |
| Viajes | C | Aproximable comparando ciudad/país del estadio (`estadios.csv`) entre partidos consecutivos — una aproximación geográfica, no una medición exacta |

## Variable008 — Calidad de Plantilla (Nivel C · `engine/01`, `02`, alcance reducido `MR-004`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| **Valor de mercado** | **D** | No existe ningún campo — ya detectado en `MR-004` |
| Profundidad | C | Derivable contando jugadores convocados por posición (`convocatorias.csv` + `jugadores.csv`) — ya usado en `MR-004` |
| Experiencia | C | Aproximable contando convocatorias históricas de cada jugador — **aproximación imperfecta**: cuenta convocatorias, no partidos realmente jugados (no existe campo de "internacionalidades"/caps) |

## Variable009 — Localía (Nivel D · `engine/03`, `MR-004`)

Todos los datos necesarios (`id_seleccion_local`/`visitante`, país del estadio) son **A** — completos. **Sin elementos pendientes.**

## Variable010 — Historial Directo (Nivel D · `engine/05`, `MR-004`)

Todos los datos necesarios (`partidos.csv` filtrado por ambas selecciones) son **A** — completos. **Sin elementos pendientes.**

## Variable011 — Estado Psicológico (sin Nivel asignado, `INC-08` · sin consumidor, diferida `MR-004`)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| Racha de victorias | C | Derivable de `partidos.csv` |
| Eliminación reciente | C | Derivable de `partidos.csv` + `torneos.csv` (fase + resultado) |
| **Clasificación** (tabla de posiciones) | **D** | No existe ninguna tabla de posiciones; reconstruirla requeriría lógica de puntos/desempate específica de cada torneo, no capturada en `torneos.csv` (`formato` es texto libre, no estructurado) |
| **Presión competitiva** | **E** | Sin una definición operacional objetiva y verificable — `docs/03-Variables.md` exige explícitamente "solo hechos verificables, no interpretaciones subjetivas" para esta variable, y "presión competitiva" no tiene, hoy, ningún hecho medible que la represente sin caer en subjetividad |

## Variable012 — Factores Externos (Nivel D · `engine/04`, activa)

| Dato necesario | Clasificación | Fuente / derivación |
|---|---|---|
| **Clima** | **D** | No existe ningún campo de clima/temperatura en ningún CSV — **hallazgo nuevo de esta auditoría**, no detectado en misiones anteriores; relevante porque, a diferencia de Variable005/011, Variable012 **ya tiene consumidor activo** (`engine/04`) |
| Altitud | A | `estadios.csv.altitud_metros` |
| Viajes | C | Mismo tratamiento que Variable007 |
| **Estado del campo** | **B** | `estadios.csv.tipo_superficie` existe, pero es un atributo **estático del estadio**, no el estado real del campo en el momento del partido (clima, mantenimiento) — aproximación parcial, no el dato literal |
| Árbitro | A | `arbitros.csv` + `partidos.csv.id_arbitro` |

---

# Tabla consolidada de elementos pendientes (B, C, D, E)

| Nombre | Variable oficial | Motor que lo necesita | Documento que lo consume | Nivel de importancia | Impacto V1 | Impacto V2 |
|---|---|---|---|---|---|---|
| Grandes oportunidades | Variable003 | `engine/01` | `docs/03`, `docs/16`, `docs/17`, `models/offensive-strength.md` | **Crítico** | El índice de Potencial Ofensivo se construye hoy con 3 de 5 componentes declarados | Bloquea el índice completo hasta capturarse |
| Conversión | Variable003 | `engine/01` | Mismos | Alto | Ninguno — ya derivable hoy vía join | Ninguno |
| xGA / Goles recibidos / Remates permitidos / Porterías en cero | Variable004 | `engine/02` | `docs/03`, `docs/16`, `docs/17` | Alto (Nivel A de la variable) | Ninguno — todo derivable hoy | Ninguno |
| Formación / Estilo de presión / Juego directo / Contraataque | Variable005 | Ninguno (diferida) | `docs/03`, `docs/16`, `docs/17` | **Crítico** | Variable005 (Nivel A) sigue sin poder construirse en absoluto | Bloquea toda la variable |
| Suspensiones (ENUM sin definir) | Variable006 | `engine/01`, `02`, `04`, `05` | `docs/03`, `docs/16`, `docs/17` | Medio | Riesgo de que la variable ignore suspensiones silenciosamente si el ENUM no las contempla | Se resuelve solo con documentación, no con nueva captura |
| Rotaciones | Variable006 | `engine/01`, `02`, `04`, `05` | Mismos | **Alto** | Variable006 es la más compartida (4 motores) — un componente ausente afecta a los cuatro | Requiere nueva tabla de alineación por partido |
| Minutos jugados | Variable007 | `engine/01`, `02`, `04` | `docs/03`, `docs/16`, `docs/17` | Medio | Mitigado — "Días de descanso" ya cubre parcialmente el mismo fenómeno | Requiere estadística individual, ya diferida desde MS-001 |
| Días de descanso / Viajes | Variable007 | `engine/01`, `02`, `04` | Mismos | Bajo | Ninguno — ya derivables | Ninguno |
| Valor de mercado | Variable008 | `engine/01`, `02` | `docs/03`, `docs/16`, `docs/17` | Medio | Ya mitigado — `MR-004` asignó alcance reducido sin este componente | Requiere nueva fuente de datos externa |
| Experiencia (aproximada) | Variable008 | `engine/01`, `02` | Mismos | Bajo | Ninguno — aproximación ya suficiente para Nivel C | Podría mejorarse con un campo de "caps" real |
| Clasificación (tabla de posiciones) | Variable011 | Ninguno (diferida) | `docs/03`, `docs/16`, `docs/17` | Alto | Variable011 sigue sin poder construirse | Requiere lógica de puntos/desempate por torneo |
| Presión competitiva | Variable011 | Ninguno (diferida) | Mismos | Bajo / **E** | Ninguno — se recomienda no perseguir | No aplica |
| Clima | Variable012 | `engine/04` (activo) | `docs/03`, `docs/16`, `docs/17` | **Alto** | Variable012 ya tiene consumidor activo — este componente falta en una variable que sí se usa hoy | Requiere fuente de datos meteorológicos |
| Estado del campo (aproximado) | Variable012 | `engine/04` | Mismos | Medio | Mitigado por `tipo_superficie`, aproximación aceptable | Podría mejorarse con dato dinámico por partido |

---

# Conteo por categoría

| Categoría | Cantidad de elementos |
|---|---|
| A (existe exactamente) | 19 de los ~46 datos necesarios revisados en total (mayoría en Variable001, 002, 004, 009, 010) |
| B (requiere transformación/definición) | 2 (Suspensiones, Estado del campo) |
| C (derivable matemáticamente) | 13 |
| D (debe capturarse) | 8 (Grandes oportunidades, 4 componentes de Compatibilidad Táctica, Rotaciones, Minutos jugados, Valor de mercado, Clasificación, Clima) |
| E (no vale la pena) | 1 (Presión competitiva) |

---

# Validaciones

- **¿Las 12 Variables Oficiales fueron revisadas?** Sí, una por una, sección por sección.
- **¿Todos los motores fueron considerados?** Sí — cada elemento pendiente indica qué motor(es) lo necesitan, verificado contra `docs/17-Matriz-de-Consumo-de-Variables.md`.
- **¿Ningún dato faltante quedó sin clasificar?** Confirmado — todos los ~46 datos necesarios de las 12 variables recibieron una clasificación A-E explícita.

---

# Cierre obligatorio

**1. ¿Cuántos datos faltantes existen realmente?**
8 de categoría D (deben capturarse) y 2 de categoría B (requieren transformación/definición, no captura nueva) — 10 en total requieren alguna acción; los 13 de categoría C ya son calculables hoy sin tocar la Base de Conocimiento.

**2. ¿Cuáles son críticos para V1?**
Dos: "Grandes oportunidades" (Variable003, Nivel A, motor activo) y los cuatro componentes no capturados de Compatibilidad Táctica (Variable005, Nivel A, sin consumidor). Ambos bloquean, total o parcialmente, una variable de la máxima prioridad declarada.

**3. ¿Cuáles pueden calcularse sin modificar la Base de Conocimiento?**
Los 13 elementos de categoría C — Resultado, Victorias/Empates/Derrotas, Rendimiento ofensivo/defensivo, Conversión, xGA, Goles recibidos, Remates permitidos, Porterías en cero, Días de descanso, Viajes (×2), Racha de victorias, Eliminación reciente, Profundidad, Experiencia.

**4. ¿Cuáles requieren nuevos CSV o campos?**
Los 8 de categoría D: Grandes oportunidades, los 4 componentes de Compatibilidad Táctica, Rotaciones (requiere una tabla de alineación por partido, no solo un campo nuevo), Minutos jugados, Valor de mercado, Clasificación, Clima.

**5. ¿Qué motores son los más afectados?**
`engine/01` y `engine/02` — son los que más elementos pendientes acumulan (Grandes oportunidades, Rotaciones, Minutos jugados, Valor de mercado, además de los ya derivables de Variable004). `engine/04` es el más afectado entre los motores que consumen variables *activas* (Clima, Rotaciones, Viajes).

**6. ¿Qué Variable Oficial es actualmente la más incompleta?**
Variable005 (Compatibilidad Táctica) — 4 de sus 5 datos necesarios son categoría D, y es Nivel A. Le sigue Variable011 (Estado Psicológico), con 2 de 4 en D/E y sin Nivel asignado.

**7. ¿Qué misión recomendarías después?**
Una misión de diseño de datos (`MS-` o una nueva serie `DATA-002`) que capture, en orden de prioridad: (a) "Grandes oportunidades" en `estadisticas_partido.csv` — el más barato de los críticos, un solo campo nuevo; (b) una tabla de alineación titular por partido, que resolvería simultáneamente "Rotaciones" (Variable006) y sentaría la base para "Minutos jugados" (Variable007) en el futuro; (c) evaluar si Compatibilidad Táctica completa (Variable005) es viable con los datos que el proyecto puede obtener realmente, antes de seguir tratándola como "pendiente" indefinidamente.

**8. ¿La implementación matemática puede continuar inmediatamente o conviene completar primero la Base de Conocimiento?**
Puede continuar **de forma selectiva**: `models/poisson.md` (siguiente recomendado) depende de las salidas de `engine/01`/`02`, no directamente de los datos crudos — no está bloqueado por esta auditoría. Pero cualquier investigación matemática futura sobre Variable005 o Variable011 completas sí debería **esperar** a que exista al menos parte de sus datos de categoría D, para no repetir lo ya visto en `MODEL-001`: una fórmula bien fundamentada que igual no puede ejecutarse con datos reales completos.

---

# Fuera de alcance de esta misión

- No se modifican variables, pesos, modelos, motores ni algoritmos.
- No se inventa ningún campo — todo lo clasificado D permanece sin fuente hasta una misión de captura futura.
- No se propone la implementación de ninguna solución — solo se audita y clasifica.

---

Fin del documento.
