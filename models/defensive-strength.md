# Defensive Strength — Fuerza Defensiva

**Archivo:** `models/defensive-strength.md`

**Misión:** MODEL-002 — Modelo Matemático de Defensive Strength / MODEL-010 — Especificación Oficial de Variable004 para V1 (operacionaliza la sección 6.2 ya existente: fuente exacta, ventana temporal, pesos placeholder con metodología, corrección de consistencia interna de signo, casos límite y complejidad computacional — mismo patrón que `MODEL-009` sobre `models/offensive-strength.md`)

**Versión:** 2.1.0-investigación

**Estado:** Investigación — estructura de la fórmula definida; coeficientes (pesos) **pendientes de calibración estadística**, conforme a `CLAUDE.md` ("Nunca alterar pesos sin evidencia estadística"). Desde `MODEL-010`, la construcción de Variable004 (sección 6.2) tiene además una especificación V1 completamente operacional (secciones 13-21) — implementable en código en cuanto existan datos reales, sin requerir más decisiones de diseño.

---

## Nota de ruta

El brief pedía `models/02-defensive-strength.md`. `models/` no usa prefijos numéricos (a diferencia de `engine/`) — los 6 documentos existentes (`poisson.md`, `elo.md`, `expected-value.md`, `confidence.md`, `offensive-strength.md`, `defensive-strength.md`) no tienen número. Se evoluciona `models/defensive-strength.md`, el archivo real, en el mismo patrón que `MODEL-001` evolucionó `models/offensive-strength.md`.

---

# 1. Objetivo

Investigar y proponer cómo medir la capacidad defensiva real de un equipo — el fundamento matemático que `engine/02-Defensive-Strength.md` implementará, sin editarlo.

---

# 2. Descripción — Fundamento estadístico

La Fuerza Defensiva representa la capacidad **sostenible** de un equipo para impedir que el rival genere y convierta oportunidades — no los goles recibidos por sí solos, que mezclan la calidad defensiva real con la varianza de finalización del rival y del portero. **Qué mide:** la solidez estructural (organización, presión, calidad de portero) que reduce sistemáticamente la producción ofensiva rival. **Qué no mide:** el rendimiento ofensivo propio (`Variable003`, ajeno a este motor) ni el ajuste por la calidad específica del rival de un partido concreto (responsabilidad de `engine/03-Poisson.md`, que combina Fuerza Ofensiva y Defensiva de ambos equipos).

---

# 3. Problema que Resuelve

Convertir estadísticas defensivas — de producción rival concedida (xGA, remates recibidos) y de contexto (forma, disponibilidad) — en un único indicador comparable entre cualquier par de equipos, sin depender únicamente de goles recibidos.

---

# 4. Literatura científica

Los mismos dos trabajos que fundamentan `MODEL-001` son igualmente relevantes aquí — Maher (1982) y Dixon-Coles (1997) modelan explícitamente **un parámetro de defensa por equipo junto al de ataque**, no por separado: el concepto dual ataque/defensa es, en ambos papers, una única estructura. El Modelo Santiago toma de ellos ese principio dual (fuerza ofensiva y defensiva como parámetros simétricos que alimentan un mismo modelo de goles esperados, `engine/03-Poisson.md`).

**Misma diferencia honesta que en `MODEL-001`:** Dixon-Coles estima sus parámetros por máxima verosimilitud sobre una liga cerrada con una temporada de datos; el Modelo Santiago usa un índice compuesto estandarizado, más apto para selecciones nacionales en múltiples competiciones con muestras pequeñas. No se repite aquí el argumento completo — ver `models/offensive-strength.md`, sección 5.

---

# 5. Variables utilizadas

*(Verificado contra `docs/17-Matriz-de-Consumo-de-Variables.md` — exactamente las mismas seis variables que `engine/01`, con Variable004 en el rol de Variable003.)*

| Variable | Rol | Por qué participa |
|---|---|---|
| **Variable004** — Solidez Defensiva | Primaria (término base) | "Variables Primarias... representan directamente el rendimiento defensivo" (`engine/02`) |
| **Variable001** — Forma Reciente | Secundaria (modificador de contexto) | Declarada "Variable Secundaria" en `engine/02` |
| **Variable002** — Rendimiento en el Torneo | Secundaria | Mismo origen textual |
| **Variable006** — Disponibilidad de Plantilla | Contextual (penalización) | "Variables Contextuales... podrán modificar el resultado final cuando exista evidencia suficiente" |
| **Variable007** — Fatiga | Contextual | Mismo rol |
| **Variable008** — Calidad de Plantilla (alcance reducido, `MR-004`) | Contextual | Asignada a `engine/02` por `MR-004` |

**Hallazgo de compatibilidad (sección 8):** `engine/02` menciona, en sus "Variables Primarias", **"Grandes Oportunidades Concedidas"** — un dato que **no aparece** entre los "Datos necesarios" oficiales de Variable004 en `docs/03-Variables.md` (que declara solo xGA, Goles recibidos, Remates permitidos, Porterías en cero). Es una señal no oficial adicional, del mismo tipo ya catalogado en `docs/17` (sección 4) y `docs/28` (Categoría E) — y, además, no existe como campo en ningún CSV (mismo problema que "Grandes oportunidades" de Variable003, `MODEL-001`/`DATA-001`). Se documenta, no se resuelve — no se modifica `engine/02` ni `docs/03`.

`engine/02` también menciona "Calidad Ofensiva de los Rivales", "Recuperaciones", "Intercepciones", "Presión Defensiva" (Secundarias) — las cuatro ya catalogadas en `docs/28`, Categoría E, sin fórmula ni origen físico confirmado. No participan en la fórmula de esta sección.

---

# 6. Fórmula propuesta

## 6.1 Reutilización deliberada de `M_forma` y `Pen` (no se redefinen)

`Variable001`, `Variable002`, `Variable006`, `Variable007` y `Variable008` son **exactamente las mismas** que ya usa `models/offensive-strength.md` para construir `M_forma` (modificador de forma) y `Pen` (penalización de disponibilidad) — `docs/17`, sección 8, ya señala a Variable006/007 como las más compartidas entre motores, con riesgo de duplicidad si cada uno las recalcula por separado. Para no repetir ese riesgo, este documento **reutiliza `M_forma` y `Pen` tal como los define `MODEL-001`** (mismos símbolos `w_R`, `w_T`, `δ_max`, `w_D`, `w_F`, `w_Q`, `Pen_max` — sin redefinirlos), en lugar de crear una segunda versión con nombres distintos para el mismo cálculo.

## 6.2 Construcción del término base (`P_def`, a partir de Variable004)

Análogo a la construcción de `P` en `MODEL-001`, sección 6.1, sobre la misma ventana de *N* partidos:

```
Para cada métrica i ∈ {xGA, goles recibidos, remates permitidos, porterías en cero}:

    z_i = (x̄_i − μ_i,competición) / σ_i,competición

Z_def = Σ vᵢ' · zᵢ                (vᵢ' = pesos por métrica, Σvᵢ' = 1, pendientes de calibración
                                    — símbolos propios, distintos de los vᵢ de Variable003)

P_def = 100 · (1 − Φ(Z_def / s))  (nota de signo: a diferencia de P, aquí un Z_def ALTO
                                    representa peor desempeño defensivo — más goles/xGA
                                    concedidos de lo esperado — por eso se invierte con
                                    "1 − Φ(...)", para que P_def alto siga significando
                                    "buena defensa", igual que P alto significa "buen ataque")
```

## 6.3 Fórmula final

```
Fuerza Defensiva = clip( P_def · M_forma · (1 − Pen) , 0, 100 )
```

Misma estructura de tres niveles que `MODEL-001` (base × modificador × penalización) — corresponde, sin redefinirla, a la jerarquía "Primarias/Secundarias/Contextuales" que `engine/02` ya declara.

**Ningún peso recibe valor numérico** (`vᵢ'`, y los reutilizados de `MODEL-001`) — misma razón que en `MODEL-001`: no violar "Nunca alterar pesos sin evidencia estadística".

---

# 7. Variables derivadas necesarias

*(Verificado contra `docs/28-Catalogo-de-Variables-Derivadas.md` — ninguna variable derivada se usa aquí sin estar ya catalogada.)*

| Variable derivada | ¿Catalogada en `docs/28`? | Categoría | Estado |
|---|---|---|---|
| xGA | Sí — Categoría B | Sub-componente de Variable004 | **Diseñada** (self-join, fijado desde `MS-001`) |
| `M_forma` | Sí — Categoría C | Cantidad intermedia de motor | Parcial (`MODEL-001`) |
| `Pen` | Sí — Categoría C | Cantidad intermedia de motor | Parcial (`MODEL-001`) |
| Goles recibidos, Remates permitidos, Porterías en cero | No catalogadas individualmente en `docs/28` — son análogas por simetría a "Conversión de tiros" (Categoría B) | Se documenta la dependencia; no se agregan a `docs/28` en esta misión (fuera de alcance: "no crearla, solo documentar") | Pendiente de catalogación formal |

---

# 8. Datos realmente disponibles

*(Verificado directamente contra `data/processed/selecciones-nacionales/`, no asumido.)*

| Dato | Clasificación | Fuente |
|---|---|---|
| xGA | Derivable | Self-join de `estadisticas_partido.csv.xg` sobre `id_partido` |
| Goles recibidos | Derivable | `partidos.csv` (goles del rival en el mismo partido) |
| Remates permitidos | Derivable | Self-join de `disparos_totales` |
| Porterías en cero | Derivable | Cálculo booleano sobre goles recibidos = 0 |
| Variable001, Variable002 (forma) | Disponible/Derivable | Mismos que `MODEL-001` — no se repiten |
| Variable006, Variable007, Variable008 (contextuales) | Mixto — ver `docs/27-Auditoria-de-Variables-Pendientes.md` | Idéntico a `MODEL-001`: "Rotaciones" y "Minutos jugados" y "Valor de mercado" siguen bloqueados (categoría D); el resto, derivable |

**Hallazgo positivo, a diferencia de `MODEL-001`:** los **4 componentes** de Variable004 (`P_def`) son Derivables **hoy**, sin ningún bloqueo de categoría D — Variable003 tenía "Grandes oportunidades" bloqueado (`DATA-001` ya lo confirmó: Variable004 no tuvo ningún elemento D en esa auditoría). El término base de Fuerza Defensiva es, en ese sentido, más completo que el de Fuerza Ofensiva.

---

# 9. Limitaciones

- Los pesos (`vᵢ'` y los reutilizados de `MODEL-001`) siguen sin calibrar — misma limitación que `MODEL-001`.
- El signo invertido de `P_def` (sección 6.2) es una convención propuesta, no validada — si `Z_def` no se comporta simétricamente al `Z` de Variable003, la transformación `1 − Φ(...)` podría no ser la correcta.
- Mismo supuesto de independencia entre el término base y los modificadores de forma que `MODEL-001` (sección 11 de ese documento) — no se revalida aquí, aplica igual.
- La reutilización de `M_forma`/`Pen` (sección 6.1) asume que el **mismo** modificador de forma y la **misma** penalización de disponibilidad son apropiados tanto para el ataque como para la defensa — no está demostrado que una selección "en buena forma" lo esté de forma idéntica en ambas fases del juego; es una simplificación deliberada para evitar duplicidad, documentada como tal, no una verdad estadística confirmada.

---

# 10. Aplicación dentro del Modelo Santiago

Especificación matemática oficial que `engine/02-Defensive-Strength.md` implementará en su "Versión 2.0" (ya prevista en su propio documento). Su salida (Fuerza Defensiva) alimenta directamente a `engine/03-Poisson.md`, junto con la Fuerza Ofensiva del rival — ambas combinadas determinan los goles esperados de cada equipo.

---

# 11. Referencias

- Maher, M.J. (1982). "Modelling Association Football Scores." *Statistica Neerlandica*, 36(3), 109-118.
- Dixon, M.J. y Coles, S.G. (1997). "Modelling Association Football Scores and Inefficiencies in the Football Betting Market." *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 46(2), 265-280.
- `models/offensive-strength.md` (`MODEL-001`) — fuente de `M_forma` y `Pen`, reutilizados sin cambios en este documento.

---

# 12. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a datos reales suficientes en `data/results/`:

- Calibración de todos los pesos, incluidos los reutilizados de `MODEL-001` (deberá verificarse si conviene calibrarlos una sola vez para ambos motores o de forma independiente).
- Validación del signo invertido de `P_def` (sección 6.2) con datos reales.
- Validación o refutación del supuesto de que `M_forma`/`Pen` deben ser idénticos entre ataque y defensa (sección 9) — si se refuta, se necesitarían versiones separadas, revirtiendo la decisión de reutilización de esta misión.
- Catalogación formal en `docs/28` de "Goles recibidos", "Remates permitidos" y "Porterías en cero" como Variables Derivadas de Categoría B (pendiente, fuera de esta misión).

---

# Validaciones

- **¿Consistencia con `MODEL-001`?** Sí — misma estructura de tres niveles, misma filosofía (arquitectura antes que pesos), y reutilización explícita de `M_forma`/`Pen` en lugar de una segunda definición paralela.
- **¿Consistencia con `engine/02`?** Sí, con una discrepancia detectada y documentada, no oculta: "Grandes Oportunidades Concedidas" aparece en `engine/02` sin estar en el contrato oficial de Variable004 (sección 5).
- **¿Consistencia con `docs/28`?** Sí — cada variable derivada usada ya estaba catalogada; las tres que no lo estaban individualmente se documentan como pendientes de catalogación, no se inventan.

---

# Cierre obligatorio

**1. ¿Qué representa matemáticamente Defensive Strength?**
Un índice acotado 0-100: producción defensiva estandarizada (xGA y afines) ajustada por la misma forma reciente y penalización de disponibilidad que ya usa la Fuerza Ofensiva.

**2. ¿Qué datos físicos necesita?**
`xg` (para el self-join de xGA), `disparos_totales` (self-join de remates permitidos), y los goles de `partidos.csv` — todos ya verificados como existentes.

**3. ¿Qué Variables Derivadas consume?**
Variable004 (base), Variable001/002 (forma, reutilizadas de `MODEL-001`), Variable006/007/008 (disponibilidad, reutilizadas de `MODEL-001`).

**4. ¿Qué partes pueden calcularse hoy?**
El término base completo (`P_def`) — los 4 componentes de Variable004 son derivables sin bloqueos, a diferencia de Variable003. Los modificadores `M_forma`/`Pen` tienen la misma disponibilidad parcial ya establecida en `MODEL-001`.

**5. ¿Qué partes siguen bloqueadas?**
Solo indirectamente, vía los componentes ya bloqueados de Variable006/007/008 (Rotaciones, Minutos jugados, Valor de mercado) — ninguna de Variable004 en sí.

**6. ¿Qué diferencia existe respecto a Offensive Strength?**
Dos: (a) el signo se invierte en la construcción del término base (`1 − Φ(...)`, porque un Z alto en métricas defensivas concedidas significa peor desempeño); (b) el término base está más completo hoy — Variable004 no tiene ningún componente bloqueado, mientras Variable003 sí ("grandes oportunidades").

**7. ¿Qué documentos deberán referenciar este modelo?**
`engine/02-Defensive-Strength.md` (cuando implemente su Versión 2.0), `docs/28-Catalogo-de-Variables-Derivadas.md` (al catalogar formalmente "Goles recibidos"/"Remates permitidos"/"Porterías en cero"), y `models/poisson.md` (próxima investigación, consume esta salida junto con la de `MODEL-001`).

**8. ¿Qué misión recomendarías después?**
`models/poisson.md` — con `MODEL-001` y `MODEL-002` completos, es el siguiente eslabón real de la cadena (`engine/03` combina ambas salidas) y el más urgente para que el Engine empiece a producir un número calculable de principio a fin.

---

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/02`, el Runtime, el Pipeline, las Variables Oficiales, `docs/28` ni ninguna fórmula existente.
- No se fija ningún valor numérico de peso.
- No se cataloga formalmente en `docs/28` ninguna variable derivada nueva — solo se documenta su dependencia.
- No se corrige la discrepancia de "Grandes Oportunidades Concedidas" en `engine/02` — se documenta, no se resuelve.

---

# MODEL-010 — Especificación Oficial de Variable004 para V1

*(Secciones agregadas por `MODEL-010`, mismo patrón editorial que `MODEL-009` sobre `models/offensive-strength.md` — extiende este documento en lugar de crear uno nuevo, conforme al brief. Origen: `BUILD-018` implementó Variable003 siguiendo `MODEL-009`; esta misión hace lo mismo para Variable004, condición previa de una futura `BUILD-019`.)*

## 13. Definición operacional exacta

**Variable004 (Solidez Defensiva)** representa la capacidad de una selección para impedir que sus rivales generen y conviertan oportunidades de gol, medida como un índice compuesto y estandarizado (0-100) de cuatro métricas de producción ofensiva **concedida** — Expected Goals en contra (`xGA`), goles recibidos, remates permitidos y frecuencia de porterías en cero — durante sus últimos `N` partidos oficiales, expresada en relación con las demás selecciones de la misma competición durante la misma ventana temporal.

Mismo patrón definicional que Variable003 (`models/offensive-strength.md` §19, `MODEL-009`), con los términos invertidos: donde Variable003 mide producción propia, Variable004 mide producción **rival concedida**. No mide goles recibidos en sí mismos (varianza de finalización rival y del portero, sección 2) ni depende de la calidad del rival de un partido concreto (ese ajuste pertenece a `engine/03`, sección 2).

## 14. Fuente de datos

| Métrica | Archivo | Columna / cálculo | Disponibilidad hoy |
|---|---|---|---|
| `xGA` | `data/processed/selecciones-nacionales/estadisticas_partido.csv` | *Self-join* sobre `id_partido`: el `xg` de la fila del **rival** en ese mismo partido (§8, ya confirmado "Derivable") | Columna existe; **0 filas** (verificado antes de escribir, mismo estado que `BUILD-017`/`BUILD-018`) |
| Goles recibidos | `data/processed/selecciones-nacionales/partidos.csv` | Goles del rival en el mismo partido (`goles_visitante` si el equipo fue local, `goles_local` si fue visitante) — §8 | Columnas existen; **0 filas** |
| Remates permitidos | `estadisticas_partido.csv` | *Self-join* sobre `id_partido`: `disparos_totales` de la fila del rival (§8, "Derivable") — **no** `disparos_al_arco`, tal como ya lo fija §8 explícitamente | Igual |
| Porterías en cero | Derivado de "Goles recibidos" | Booleano por partido: `1` si goles recibidos `= 0`, `0` en caso contrario (§8, "Cálculo booleano") | Igual |
| Ventana de partidos / competición | `partidos.csv` → `torneos.csv` → `competiciones.csv` | Idéntico a Variable003 (`MODEL-009` §20) | Igual |

**A diferencia de Variable003, las 4 métricas están confirmadas como derivables hoy, sin ningún componente bloqueado** (§8, "Hallazgo positivo" — ya lo señalaba el documento original antes de esta misión). No se usa ranking FIFA, Elo ni ninguna fuente externa, por la misma razón ya fijada en `MODEL-009` §20 (`docs/16` no autoriza otra fuente para Variable004).

## 15. Fórmula oficial V1 (operacionalización de la sección 6.2)

```
Para cada métrica i ∈ {xGA, goles_recibidos, remates_permitidos, tasa_sin_porteria_en_cero}:

    x̄_i(equipo)      = promedio de la métrica i del equipo sobre sus últimos N partidos oficiales (sección 16)
    μ_i(competición) = promedio de la métrica i de TODOS los equipos de la misma competición, sobre la misma ventana temporal
    σ_i(competición) = desviación estándar de la métrica i, misma población que μ_i

    z_i = (x̄_i(equipo) − μ_i(competición)) / σ_i(competición)

Z_def = Σ vᵢ' · zᵢ                        (i = 1..4)

P_def = 100 · (1 − Φ(Z_def / s_def))       (Φ = CDF normal estándar; P_def acotado a [0, 100] por construcción)
```

**Corrección de consistencia interna — no una hipótesis nueva (ver "Gobernanza" en el brief de `MODEL-010`).** La sección 6.2 original ya fija el invariante: "un `Z_def` ALTO representa peor desempeño defensivo". `xGA`, `goles_recibidos` y `remates_permitidos` ya cumplen esa dirección por sí solos (más goles/xG/remates concedidos = peor defensa = `z_i` más alto). **"Porterías en cero" no la cumple**: más porterías en cero es **mejor** defensa, no peor — si se usara tal cual, su `z_i` apuntaría en sentido contrario a los otros tres dentro de la misma suma `Z_def`, contradiciendo el invariante que el propio documento ya declaraba antes de esta misión. Esto no es una decisión de diseño nueva: es una corrección exigida por dos hechos ya fijados en el texto (el invariante de `Z_def`, sección 6.2; y el significado de "portería en cero" como resultado defensivo positivo, `docs/03-Variables.md`, Variable004). La cuarta métrica se redefine, por tanto, como **`tasa_sin_porteria_en_cero`** = proporción de partidos de la ventana en los que el equipo **concedió al menos un gol** (`1 − tasa de porterías en cero`) — matemáticamente equivalente a invertir el signo de `z_i` de "porterías en cero", expresado como una métrica que ya apunta en la misma dirección que las otras tres, sin introducir ningún peso ni transformación adicional.

**Pesos — placeholder documentado, no calibrado, mismo criterio que `MODEL-009`:**

- `v₁' = v₂' = v₃' = v₄' = 1/4`: ponderación **igualitaria** entre las 4 métricas — mismo criterio neutral que `vᵢ` en Variable003 (`MODEL-009` §21), símbolos propios (`vᵢ'`) ya distinguidos desde la sección 6.1 de este documento. Ninguna evidencia hoy indica que `xGA` deba pesar más o menos que goles recibidos, remates permitidos o la tasa sin portería en cero.
- `s_def = √(Σ vᵢ'²) = √(4 · (1/4)²) = √(1/4) = 0.5`: misma metodología de derivación que `s` en Variable003 (`MODEL-009` §21: desviación estándar teórica de `Z_def` bajo independencia aproximada) — **el valor numérico difiere del `s` de Variable003 (√(1/3) ≈ 0.577) porque el número de métricas difiere (4, no 3)**, no porque se use un criterio distinto. Diverge de Variable003 en el número, converge en el método.

**Metodología de calibración real (futura, no de esta misión):** igual que `MODEL-009` §21 — `vᵢ'` mediante MLE u otro método de `models/parameter-calibration.md` §7, `s_def` recalculado empíricamente, una vez exista historial suficiente en `data/results/`.

## 16. Variables internas y ventana temporal

**Métricas necesarias** (por equipo, por partido, agregadas sobre la ventana): `xGA`, `goles_recibidos`, `remates_permitidos`, `tasa_sin_porteria_en_cero` — exactamente las cuatro de la sección 14/15, sin ninguna métrica adicional no listada en `docs/03`/§5 de este documento.

**Ventana temporal — `N = 10` últimos partidos oficiales, reutilizado explícitamente de Variable003.** La sección 6.2 de este documento ya autoriza esta reutilización literalmente: "sobre la misma ventana de *N* partidos" (refiriéndose a la construcción de `P` en `MODEL-001`) — a diferencia de los pesos `vᵢ'` (símbolos propios, sección 6.1), el documento nunca distingue un `N` propio de Variable004. Reutilizar `N = 10` (`MODEL-009` §22) es, por tanto, un espejo explícito, no una decisión independiente de esta misión.

**Tratamiento de amistosos y de competiciones — mismo criterio que `MODEL-009` §20, sin excepción.** "Amistosos Internacionales" (`COMP-000001`, `competiciones.csv`) se trata como cualquier otra competición: la resolución `nombre → id_competición → conjunto de id_torneo` no distingue tipo de competición. Ningún documento (`docs/03`, `docs/16`, este archivo) pide un tratamiento diferenciado para amistosos, y esta misión no introduce uno.

`μ_i(competición)`/`σ_i(competición)` se calculan sobre la misma ventana temporal que `MODEL-009` §22 fija para Variable003 (rango de fechas de los propios `N` partidos del equipo) — mismo mecanismo, aplicado aquí a la población de las 4 métricas defensivas.

## 17. Normalización

Rango de salida: **0 a 100**, heredado sin cambios de `docs/16` (Variable004 es "Índice (0-100)", igual convención que Variable003). `Φ` satura naturalmente `[0,1]`, escalado por `100·`; la inversión `1 − Φ(...)` no altera el rango, solo el sentido (`P_def` alto = buena defensa, igual que `P` alto = buen ataque, sección 6.2). No requiere `clip` adicional — misma justificación que `MODEL-009` §23.

## 18. Tratamiento de datos faltantes / casos límite

| Caso | Comportamiento |
|---|---|
| **Equipo con menos de `N` partidos oficiales disponibles** | Se usa el subconjunto disponible; `muestra_reducida = True` se propaga en `ValorVariable` — mismo mecanismo que Variable003 (`MODEL-009` §24) |
| **Equipo con cero partidos oficiales con estadísticas válidas en la ventana** | Variable004 se marca `disponible = False` — nunca un valor inventado. Es obligatoria (Nivel A, `docs/17`); el pipeline se detiene antes de `engine/02` (`docs/06`, tabla "Manejo de errores"), mismo comportamiento que `VariableObligatoriaNoDisponible` en `Engine02` desde `BUILD-011` |
| **Selección nueva / debut** | Mismo caso que la fila anterior — sin mecanismo especial, mismo criterio que `MODEL-009` §24 |
| **Estadísticas incompletas** (una fila de `estadisticas_partido.csv` con `xg`/`disparos_totales` no numérico o negativo) | Esa fila se descarta individualmente (mismo tratamiento que una fila corrupta en la implementación de Variable003, `BUILD-018`) — no invalida el resto de la ventana |
| **`σ_i(competición) = 0` o indefinida** (menos de 2 observaciones en la población) | Esa métrica se excluye del cálculo de `Z_def`, sin renormalizar los pesos restantes — idéntico a `MODEL-009` §24. Si las 4 quedan excluidas, Variable004 se marca `disponible = False` |
| **Competición sin suficientes registros** (población total insuficiente para cualquier métrica) | Mismo caso que la fila anterior — se excluye la métrica afectada, o toda la variable si las 4 lo están |

## 19. Complejidad computacional

**Puede precalcularse**, igual que Variable003 (`MODEL-009` §25). El *self-join* adicional que exigen `xGA` y `remates_permitidos` (resolver el rival de cada partido vía `partidos.csv` antes de leer su fila en `estadisticas_partido.csv`) es una operación `O(1)` por partido ya indexado por `id_partido` — no cambia el orden de complejidad general: `O(N)` por equipo, `O(M)` por competición (`M` = partidos de la competición en la ventana), ambos lineales. Mismo patrón de lectura de CSV ya usado en `CsvPotencialOfensivoRepository` (`BUILD-018`), extendido con la resolución de rival por partido.

## 20. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable004 podría pasar de "Método: Pendiente" a "definido, ver `models/defensive-strength.md` §6.2/§13-21" — actualización editorial futura de `docs/`, fuera de alcance de `models/` (mismo criterio que `MODEL-009` §26) |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Sin cambios — ya asigna Variable004 exclusivamente a `engine/02`, consistente |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Sin cambios — `solidez_defensiva` en `VariablesBlock` ya está tipado `float \| None`, compatible sin bloqueo de esquema (mismo caso que Variable003, a diferencia de Variable009) |
| `app/preparation/preparation.py` (`VariablePreparation`) | Consumidor directo en una futura `BUILD-019`, siguiendo exactamente el mismo patrón ya validado por `BUILD-018` para Variable003 |
| `models/offensive-strength.md` | Sin cambios — Variable004 reutiliza `N` de esa especificación (sección 16), pero no sus pesos ni su `s` (símbolos propios, sección 15) |
| `models/parameter-calibration.md` | Ya cataloga `vᵢ'` como parámetros de `Defensive Strength` (sección 4 de ese documento) — sin cambios, esta misión solo fija el valor placeholder de `s_def` como derivado matemáticamente, no calibrado |

## 21. Impacto

Una vez que esta especificación sea revisada y aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2.9/Art. 5 — nunca autoaprobada por el Arquitecto Estadístico IA):

- **`VariablePreparation` podría implementar el cálculo real de Variable004** en una futura `BUILD-019`, siguiendo exactamente la fórmula de la sección 15 y los casos límite de la sección 18 — mismo patrón que `BUILD-018` aplicó para Variable003, sin ninguna decisión de diseño pendiente.
- **`Engine02` dejaría de detenerse por `VariableObligatoriaNoDisponible`** únicamente cuando, además, existan filas reales en `estadisticas_partido.csv` y `partidos.csv` (hoy ambos con cero filas) — esta misión resuelve el bloqueo **metodológico**, no el de **datos**. Mismo matiz honesto que `MODEL-009` §27: el resultado práctico inmediato de `BUILD-019` seguiría siendo `disponible=False` hasta que existan datos reales.
- **`Engine03` podría producir `λ_local`/`λ_visitante` reales** en la misma condición — Variable004 es, junto con Variable003, la última pieza obligatoria de Capa 1 que le faltaba a la Fuerza Defensiva.
- **`Engine05` (Confidence)** también se beneficia indirectamente: `C_diferencia` (`models/confidence.md` §6) consume `Fuerza Ofensiva`/`Defensiva` de ambos equipos — con Variable003 y Variable004 ambas operacionalizadas, esa entrada deja de depender de datos inexistentes por falta de fórmula, aunque siga dependiendo de que existan filas reales.

---

# Validaciones — MODEL-010

- **¿La especificación V1 contradice la fórmula ya aprobada en la sección 6.2?** No — la transcribe completa, corrigiendo únicamente la dirección de "porterías en cero" para que sea consistente con el invariante que el propio documento ya declaraba ("`Z_def` alto = peor desempeño").
- **¿Se fija algún peso sin justificar?** No — `vᵢ'` usa ponderación igualitaria (mismo criterio que `MODEL-009`) y `s_def` se deriva matemáticamente de esos pesos, con la misma metodología, ajustada al número real de métricas (4, no 3).
- **¿Se reutiliza algo de Offensive Strength sin que el documento lo autorice?** No — `N` se reutiliza porque la sección 6.2 ya lo dice explícitamente ("misma ventana de N partidos"); `M_forma`/`Pen` ya estaban reutilizados desde la sección 6.1 original, sin cambios de esta misión. Los pesos `vᵢ'` y `s_def` son símbolos propios, nunca reutilizados de Variable003.
- **¿Se introdujo alguna hipótesis nueva no anclada en el texto?** Una sola, declarada explícitamente como corrección de consistencia interna (sección 15) — no como un hallazgo experimental ni una preferencia de diseño: la dirección de "porterías en cero" queda determinada por dos hechos que el documento ya afirmaba (el invariante de `Z_def` y el significado positivo de una portería en cero), no por una elección arbitraria de esta misión.
- **¿Es reproducible?** Sí — una vez fijados `N`, `vᵢ'` y `s_def` (aunque sean placeholders), la fórmula es una función determinista de los datos de entrada.

---

# Cierre obligatorio — MODEL-010

**1. Definición operacional.**
Variable004 (Solidez Defensiva) mide la capacidad de una selección para impedir producción ofensiva rival, como índice compuesto estandarizado (0-100) de `xGA`/goles recibidos/remates permitidos/tasa sin portería en cero de sus últimos `N=10` partidos oficiales, relativo a las demás selecciones de la misma competición en la misma ventana — sección 13.

**2. Fuente de datos.**
`estadisticas_partido.csv` (`xGA` y remates permitidos, ambos vía *self-join* sobre `id_partido` contra la fila del rival) y `partidos.csv` (goles recibidos, directo) — sección 14. Las 4 métricas confirmadas derivables hoy, sin ningún componente bloqueado (a diferencia de Variable003).

**3. Métricas internas.**
`xGA`, `goles_recibidos`, `remates_permitidos`, `tasa_sin_porteria_en_cero` — sección 16. La cuarta reemplaza a "porterías en cero" tal cual, por consistencia de signo (sección 15).

**4. Fórmula matemática oficial.**
`Z_def = (1/4)·z_xGA + (1/4)·z_goles_recibidos + (1/4)·z_remates_permitidos + (1/4)·z_tasa_sin_porteria_en_cero`; `P_def = 100·(1 − Φ(Z_def/0.5))` — sección 15. Pesos iguales (neutral); `s_def` derivado matemáticamente de los pesos, no calibrado.

**5. Ventana temporal.**
`N = 10` últimos partidos oficiales, reutilizado explícitamente de Variable003 (autorizado por la sección 6.2 original) — sección 16. Amistosos y competiciones sin tratamiento diferenciado.

**6. Rango.**
0 a 100, garantizado por construcción de `Φ` — sección 17.

**7. Casos límite.**
Menos de `N` partidos → `muestra_reducida=True`; cero partidos → `disponible=False`, pipeline se detiene (Nivel A); fila individual corrupta → se descarta sola; `σ=0`/indefinida → esa métrica se excluye, o toda la variable si las 4 lo están — sección 18.

**8. Documentos afectados.**
`docs/03` (actualización editorial futura, fuera de esta misión), `docs/17`/`docs/30` (sin cambios, ya consistentes), `app/preparation/preparation.py` (consumidor futuro de `BUILD-019`), `models/offensive-strength.md` (fuente de `N` reutilizado), `models/parameter-calibration.md` (sin cambios al catálogo) — sección 20.

**9. Impacto inmediato sobre BUILD-019.**
Desbloquea el camino metodológico completo para que una futura `BUILD-019` implemente Variable004 en `VariablePreparation`, siguiendo exactamente el patrón ya validado por `BUILD-018` — sin ninguna decisión de diseño pendiente. No desbloquea, por sí sola, una predicción real: `estadisticas_partido.csv`/`partidos.csv` siguen sin filas reales. Requiere, además, aprobación explícita del Arquitecto Estadístico Humano antes de implementarse en código (Constitución, Art. 2.9/Art. 5) — sección 21.

---

# Fuera de alcance de MODEL-010

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext` ni `Engine02` (código).
- No se calibra ningún peso con evidencia real — `vᵢ'`/`s_def`/`N` son placeholders estructurales, documentados como tales.
- No se corrige la discrepancia de "Grandes Oportunidades Concedidas" en `engine/02` (ya documentada, sin resolver, desde la sección 5 original).
- No se actualiza `docs/03-Variables.md` (columna "Método de cálculo") — pertenece a una misión de `docs/`, no de `models/`.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano.

---

Fin del documento.
