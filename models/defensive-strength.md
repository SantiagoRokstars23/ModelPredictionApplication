# Defensive Strength — Fuerza Defensiva

**Archivo:** `models/defensive-strength.md`

**Misión:** MODEL-002 — Modelo Matemático de Defensive Strength

**Versión:** 2.0.0-investigación

**Estado:** Investigación — estructura de la fórmula definida; coeficientes (pesos) **pendientes de calibración estadística**, conforme a `CLAUDE.md` ("Nunca alterar pesos sin evidencia estadística")

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

Fin del documento.
