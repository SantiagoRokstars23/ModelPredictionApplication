# Catálogo Oficial de Variables Derivadas

**Archivo:** `docs/28-Catalogo-de-Variables-Derivadas.md`

**Misión:** DATA-002 — Catálogo Oficial de Variables Derivadas

**Versión:** 1.0.0

**Estado:** Catálogo — sin modificaciones aplicadas

---

## Nota de numeración

El brief pedía `docs/27-Catalogo-de-Variables-Derivadas.md`; esa posición ya la ocupa `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`, creado en la misión inmediatamente anterior). Se usa `docs/28`, siguiente posición libre.

---

# Objetivo

Centralizar, en un único catálogo, todas las cantidades **calculadas** que el Modelo Santiago usa o menciona hoy — hasta ahora dispersas entre `engine/`, `docs/03`, `docs/15`, `docs/16`, `docs/17` y `models/` — sin modificar ninguna de ellas.

---

# 1. Definición

**Dato físico:** un valor almacenado literalmente como columna en un CSV de `data/processed/` (ej. `xg`, `posesion_pct`, `goles_local`). No se calcula — se lee.

**Variable Derivada:** cualquier cantidad que **no** es un dato físico — se obtiene aplicando una operación (conteo, razón, self-join, combinación ponderada, transformación estadística) sobre uno o más datos físicos, u otras variables derivadas. Incluye desde las 12 Variables Oficiales (`docs/16`) hasta las cantidades intermedias de una fórmula de motor (ej. `P`, `M_forma` de `MODEL-001`).

**Variable Contextual (de este catálogo):** una variable derivada cuyo dato físico de origen **no proviene de la Base de Conocimiento interna**, sino de una fuente externa (hoy, únicamente cuotas de mercado).

**Aclaración de terminología, para evitar una confusión real:** `engine/01-Offensive-Strength.md` (y `02`) usan la etiqueta "Variables Contextuales" para un concepto **distinto**: un nivel de *rol* dentro de su propia fórmula (Lesiones, Suspensiones, Rotaciones, Fatiga — que modifican el resultado "cuando exista evidencia"), sin relación con el origen físico del dato. Este catálogo usa "Variable Contextual" únicamente por **procedencia** (interna vs. externa). Son dos ejes de clasificación distintos que comparten la misma palabra — no se contradicen, pero no deben confundirse.

**Diferencia con una Variable Oficial:** toda Variable Oficial (`docs/16`) es una Variable Derivada, pero no toda Variable Derivada es una Variable Oficial — muchas son componentes intermedios sin su propio contrato (ej. "Conversión de tiros" no tiene tipo/rango/nulabilidad propios; es un paso dentro del cálculo de Variable003).

---

# 2. Clasificación

| Categoría | Contenido |
|---|---|
| **A** — Variables Oficiales | Las 12 de `docs/16-Contrato-Oficial-de-Variables.md` |
| **B** — Sub-componentes de una Variable Oficial | Cantidades derivadas que alimentan una sola Variable Oficial, sin contrato propio |
| **C** — Cantidades intermedias de una fórmula de motor | Términos definidos dentro de un documento `models/` (hoy, solo `MODEL-001`) |
| **D** — Resultados parciales de motor | Las salidas de cada `engine/0X`, ya formalizadas como "Resultados parciales" en el Objeto de Contexto (`docs/26`, sección 3) |
| **E** — Señales referenciadas sin definición propia | Mencionadas en `engine/01-06` pero sin fórmula, sin origen físico confirmado, o sin ninguna presencia previa en el proyecto |
| **F** — Variables Contextuales (fuente externa) | Derivadas de datos de mercado, no de la Base de Conocimiento interna |

---

# 3. Catálogo

## Categoría A — Variables Oficiales (referencia, no se repite el detalle ya en `docs/16`/`docs/03`)

| Nombre | Documento donde se define | Motor que la consume | Estado |
|---|---|---|---|
| Forma Reciente (Var001) | `docs/03`, `docs/16` | `engine/01`, `02` (indirecto `03-06`) | Pendiente (fórmula) |
| Rendimiento en el Torneo (Var002) | Ídem | `engine/01`, `02` | Pendiente |
| Potencial Ofensivo (Var003) | Ídem + `models/offensive-strength.md` | `engine/01` | **Parcial** (estructura definida, `MODEL-001`; pesos pendientes) |
| Solidez Defensiva (Var004) | `docs/03`, `docs/16` | `engine/02` | Pendiente |
| Compatibilidad Táctica (Var005) | Ídem | Ninguno (diferida) | Pendiente (sin fuente de datos) |
| Disponibilidad de Plantilla (Var006) | Ídem | `engine/01`, `02`, `04`, `05` | Pendiente |
| Fatiga (Var007) | Ídem | `engine/01`, `02`, `04` | Pendiente |
| Calidad de Plantilla (Var008) | Ídem | `engine/01`, `02` (alcance reducido) | Pendiente |
| Localía (Var009) | Ídem | `engine/03` | Pendiente |
| Historial Directo (Var010) | Ídem | `engine/05` | Pendiente |
| Estado Psicológico (Var011) | Ídem | Ninguno (diferida) | Pendiente (sin fuente de datos) |
| Factores Externos (Var012) | Ídem | `engine/04` | Pendiente |

## Categoría B — Sub-componentes de una Variable Oficial

| Nombre | Descripción | Origen | Variables físicas | Fórmula | Documento | Motor | Estado |
|---|---|---|---|---|---|---|---|
| Conversión de tiros | Goles ÷ disparos totales | Componente de Var003 | `goles_local`/`visitante` (`partidos.csv`), `disparos_totales` (`estadisticas_partido.csv`) | `goles / disparos_totales` | `models/offensive-strength.md` (`MODEL-001`) | `engine/01` (vía Var003) | **Parcial** |
| xGA (Expected Goals Against) | xG del rival en el mismo partido | Componente de Var004 | `xg` (self-join sobre `id_partido`) | Self-join, sin transformación adicional | `data/processed/selecciones-nacionales/README.md` (MS-001, "Campo excluido") | `engine/02` (vía Var004) | Diseñada |
| Días de descanso | Diferencia de fechas entre partidos consecutivos | Componente de Var007 | `fecha` (`partidos.csv`) | Resta de fechas | `docs/27-Auditoria-de-Variables-Pendientes.md` (`DATA-001`) | `engine/01`, `02`, `04` (vía Var007) | Diseñada |
| Profundidad de plantilla | Conteo de convocados por posición | Componente de Var008 | `convocatorias.csv` + `jugadores.csv.posicion_principal` | Conteo, sin fórmula exacta fijada | `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md` (`MR-004`) | `engine/01`, `02` (vía Var008) | **Parcial** |

## Categoría C — Cantidades intermedias de una fórmula de motor

| Nombre | Descripción | Origen | Variables utilizadas | Fórmula | Documento | Motor | Estado |
|---|---|---|---|---|---|---|---|
| `P` (índice de producción) | Base del cálculo de Fuerza Ofensiva | Interna a `MODEL-001` | Componentes de Var003 | `P = 100·Φ(Z/s)` (sección 6.1) | `models/offensive-strength.md` | `engine/01` | **Parcial** |
| `M_forma` (modificador de forma) | Ajuste multiplicativo acotado | Interna a `MODEL-001` | Var001, Var002 | `1 + clip(w_R·r + w_T·t, ±δ_max)` (sección 6.2) | `models/offensive-strength.md` | `engine/01` | **Parcial** |
| `Pen` (penalización de disponibilidad) | Ajuste multiplicativo acotado | Interna a `MODEL-001` | Var006, Var007, Var008 | `clip(Σ wᵢ·..., 0, Pen_max)` (sección 6.3) | `models/offensive-strength.md` | `engine/01` | **Parcial** |

*(Los equivalentes para `engine/02` a `06` todavía no existen — dependen de que `MODEL-002` en adelante investigue cada motor restante.)*

## Categoría D — Resultados parciales de motor (ya formalizados en `docs/26`, sección 3 — no se redefinen)

| Nombre | Motor que lo produce | Estado |
|---|---|---|
| Fuerza Ofensiva | `engine/01` | **Parcial** (fórmula estructural, `MODEL-001`) |
| Fuerza Defensiva | `engine/02` | Pendiente |
| Goles Esperados | `engine/03` | Pendiente |
| Índice de Caos | `engine/04` | Pendiente |
| Índice de Confianza | `engine/05` | Pendiente |
| Valor Esperado | `engine/06` | Pendiente |
| Probabilidad Implícita | Interna a `engine/06`, Paso 3 | Ya excluida como campo bruto en `data/processed/selecciones-nacionales/README.md` (MS-001); fórmula trivial (`1/cuota_decimal`) nunca escrita formalmente | Pendiente |

## Categoría E — Señales referenciadas por `engine/` sin definición propia

*(Ninguna tiene fórmula, contrato ni origen físico confirmado — ya señaladas como "información no oficial" en `docs/17`, sección 4; se consolidan aquí, sin resolverlas.)*

| Nombre | Mencionada en | Posible origen físico | Estado |
|---|---|---|---|
| Calidad del Rival | `engine/01` | No confirmado — posible Var008 del rival | Pendiente |
| Posesión en Campo Rival | `engine/01` | `posesion_pct` (parcial, sin fórmula de "en campo rival") | Pendiente |
| Ataques Peligrosos | `engine/01` | No confirmado | Pendiente |
| Calidad Ofensiva de los Rivales | `engine/02` | No confirmado — posible Var003 del rival | Pendiente |
| Recuperaciones | `engine/02` | No existe campo en ningún CSV | Pendiente |
| Intercepciones | `engine/02` | No existe campo en ningún CSV | Pendiente |
| Presión Defensiva | `engine/02` | No existe campo en ningún CSV | Pendiente |
| Rotaciones | `engine/01`, `02`, `04`, `05` (duplicada) | Bloqueada — no existe tabla de alineación por partido (`DATA-001`) | Pendiente |
| **Índice disciplinario** | Mencionado solo en el brief de esta misión — **no existe en ningún documento del proyecto** | `tarjetas_amarillas`/`tarjetas_rojas`/`faltas_cometidas` (`estadisticas_partido.csv`) — candidato razonable, no diseñado | **Pendiente (no existía antes de esta auditoría)** |
| **Índice de lesiones** | Mencionado solo en el brief de esta misión — **no existe en ningún documento del proyecto** | `lesiones.csv` — candidato razonable, ya cubierto conceptualmente por Var006 sin un índice propio separado | **Pendiente (no existía antes de esta auditoría)** |

## Categoría F — Variables Contextuales (fuente externa)

| Nombre | Descripción | Origen | Documento | Motor | Estado |
|---|---|---|---|---|---|
| Cuotas de mercado (preparadas) | Categoría de Datos de Mercado, paralela a las Variables Oficiales | `cuotas.csv` (externo por naturaleza — precio de mercado, no rendimiento deportivo) | `docs/15`, `docs/16` (principio, `MR-004`) | `engine/06` | **Parcial** (principio arquitectónico fijado; contrato completo pendiente, `INC-05`) |

---

# 4. Relación con `docs/15-Capa-de-Preparacion-de-Variables.md`

No se redefine — se confirma que **todas** las Variables Derivadas de Categoría A (las 12 Oficiales) son responsabilidad exclusiva de la Capa de Preparación de Variables, que las construye antes de que cualquier motor se ejecute (`docs/15`, secciones 1-6). Las Categorías B y C (sub-componentes y cantidades intermedias de una fórmula) son responsabilidad del **motor correspondiente**, no de la Capa — la Capa entrega Variables Oficiales ya preparadas; lo que cada motor haga internamente con ellas (como `P`, `M_forma`, `Pen` de `MODEL-001`) es lógica de `engine/`/`models/`, no de la Capa.

---

# 5. Relación con `models/`

No se redefine — se confirma el patrón ya establecido por `MODEL-001`: los documentos de `models/` consumen **Variables Oficiales** (Categoría A) como entrada declarada, nunca datos físicos directamente (`CLAUDE.md`: "Investigación antes de implementación"; `docs/15`: los motores nunca conocen el origen físico). Las cantidades de Categoría C (`P`, `M_forma`, `Pen`) son productos internos de esa investigación, no nuevas entradas externas — se calculan a partir de Variables Oficiales ya preparadas.

---

# 6. Beneficios

- **Reduce duplicación:** antes de este catálogo, "Rotaciones" aparecía referenciada por separado en 4 motores sin un punto único de verdad (`docs/15`, `docs/17`, ya señalado). Este catálogo es ahora ese punto único para consultar el estado de cualquier cantidad calculada.
- **Mejora la trazabilidad:** cada entrada indica su documento de origen — antes, encontrar dónde se definía "xGA" requería conocer que estaba en un README de datos, no en un documento de arquitectura.
- **Expone honestamente el tamaño real de la deuda de diseño:** de ~27 cantidades catalogadas, solo 6 están en estado "Parcial" y ninguna en "Diseñada" completa salvo dos sub-componentes triviales (xGA, Días de descanso) — un panorama más preciso que "el Engine está mayormente listo".
- **Facilita futuras implementaciones:** un desarrollador que necesite saber "¿de dónde sale esta cantidad?" tiene una única tabla que consultar, en lugar de rastrear 6 documentos de `engine/` más `docs/03/15/16/17` más `models/`.

---

# Validaciones

- **¿Todas las variables derivadas existentes fueron inventariadas?** Sí, hasta donde el repositorio actual permite verificar — 27 entradas en 6 categorías, cruzadas contra `engine/01-06`, `docs/03`, `docs/15`, `docs/16`, `docs/17` y `models/offensive-strength.md`.
- **¿Ninguna variable física fue clasificada incorrectamente?** Verificado — ningún campo que exista literalmente como columna de un CSV (`xg`, `posesion_pct`, `disparos_totales`, etc.) aparece en este catálogo como "derivada"; son los **insumos** de las entradas de Categoría B/C, no entradas por sí mismos.
- **¿El catálogo puede convertirse en la referencia única para futuras implementaciones?** Sí — cada entrada indica su documento de autoridad; este catálogo no compite con ellos, los indexa.

---

# Cierre obligatorio

**1. ¿Cuántas Variables Derivadas existen actualmente?**
27 catalogadas: 12 Variables Oficiales (Categoría A), 4 sub-componentes (B), 3 cantidades intermedias de motor (C), 7 resultados parciales (D), 10 señales sin definición propia (E), 1 variable contextual externa (F).

**2. ¿Cuáles están completamente definidas ("Diseñada")?**
Solo 2: xGA (self-join, ya fijado desde `MS-001`) y Días de descanso (aritmética simple, sin ambigüedad). Ninguna Variable Oficial completa alcanza todavía el estado "Diseñada" — la más avanzada es Potencial Ofensivo, en "Parcial".

**3. ¿Cuáles siguen pendientes?**
19 de las 27 — la mayoría (Categoría E completa, 9 de las 12 Variables Oficiales, 5 de los 6 resultados parciales de motor).

**4. ¿Qué motores consumen más Variables Derivadas?**
`engine/01` (Categorías A, B y C combinadas: Var003, Var001, Var002, Var006-008, más `P`/`M_forma`/`Pen`, más 3 señales de Categoría E) y `engine/02` (patrón similar, sin la Categoría C todavía). Ambos muy por delante de `engine/06`, que hoy depende casi enteramente de una única variable de Categoría F.

**5. ¿Qué beneficios aporta este catálogo?**
Los cuatro de la sección 6 — reducción de duplicación, trazabilidad, honestidad sobre el estado real del proyecto, y un punto único de consulta.

**6. ¿Qué documentos deberían referenciarlo?**
`docs/17-Matriz-de-Consumo-de-Variables.md` (para no repetir su propia sección 4 de "información no oficial"), cualquier futuro `MODEL-00X` (para verificar si la cantidad que va a definir ya está catalogada como "Pendiente" aquí), y `docs/99-Mapa-Maestro.md` en su próxima actualización.

**7. ¿Qué misión recomendarías después?**
`MODEL-002` sobre `models/defensive-strength.md` (siguiente motor en la cadena, ya con `xGA` definido como sub-componente listo en la Categoría B de este catálogo) — o, alternativamente, una misión que diseñe formalmente "Índice disciplinario" e "Índice de lesiones" si el Arquitecto Estadístico Humano decide que valen la pena, dado que esta misión los encontró sin ningún precedente en el proyecto.

**8. ¿Acerca al proyecto a una implementación real?**
Indirectamente sí, pero no por sí mismo: no diseña ninguna fórmula nueva, solo revela con precisión cuánto trabajo de `models/` falta — 25 de 27 entradas sin definición completa. Es un mapa de lo que falta, no un avance en resolverlo.

---

# Fuera de alcance de esta misión

- No se modifican `engine/`, `models/`, `docs/03`, `docs/15` ni ninguna fórmula existente.
- No se diseñan "Índice disciplinario" ni "Índice de lesiones" — se documenta que no existían antes de esta auditoría, sin definirlos.
- No se resuelve ninguna de las 19 entradas "Pendiente" — se catalogan, no se completan.

---

Fin del documento.
