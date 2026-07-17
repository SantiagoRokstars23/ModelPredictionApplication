# Análisis Arquitectónico de Decisiones Críticas del Engine (INC-04 / INC-05)

**Archivo:** `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md`

**Misión:** MR-004 — Fase de Análisis (la implementación queda para una misión futura, ver Cierre Q9)

**Versión:** 1.0.0

**Estado:** Recomendación arquitectónica — sin implementar, pendiente de aprobación del Arquitecto Estadístico Humano

---

# Objetivo

Analizar en profundidad las dos únicas inconsistencias críticas que quedan abiertas tras `MR-002`/`MR-003` (`INC-04`, `INC-05`) y producir una recomendación arquitectónica formal — sin modificar Engine, variables, algoritmos, pesos, pipeline ni ningún documento existente. Es una decisión de diseño, no una edición: por eso se separa en su propia misión de análisis antes de tocar nada.

---

# Metodología

Antes de analizar, se verificó con lectura directa de los CSV reales (no de memoria) qué campos existen hoy en `data/processed/selecciones-nacionales/` para cada "Dato necesario" que `docs/03-Variables.md` declara para las 5 variables de `INC-04`. Este paso resultó decisivo: reveló que `INC-04` no es un problema homogéneo — dos de las cinco variables carecen de fuente de datos real en el esquema actual, no solo de un motor que las consuma (ver sección INC-04).

---

# INC-04 — Variables sin consumidor confirmado

## Problema

Cinco de las 12 Variables Oficiales (`Compatibilidad Táctica`, `Calidad de Plantilla`, `Localía`, `Historial Directo`, `Estado Psicológico`) no tienen un consumidor explícito en ningún motor de `engine/` (`docs/17-Matriz-de-Consumo-de-Variables.md`).

## Análisis variable por variable

| Variable | Nivel (`docs/02`) | ¿Dato disponible hoy en la Base de Conocimiento? | Conclusión |
|---|---|---|---|
| **Localía** (009) | D | **Sí, completo.** `partidos.csv` (`id_seleccion_local`/`visitante`), `estadios.csv`, `torneos.csv` (`paises_organizadores`) ya contienen todo lo necesario. | Brecha puramente de *wiring* — no hay barrera de datos. |
| **Historial Directo** (010) | D | **Sí, completo.** `partidos.csv` permite filtrar enfrentamientos directos entre dos selecciones. `docs/03` ya se autolimita: "tendrá poca influencia, nunca deberá dominar el modelo". | Brecha puramente de *wiring*, de bajo riesgo por diseño propio. |
| **Calidad de Plantilla** (008) | C | **Parcial.** "Profundidad del banco"/"experiencia" son derivables de `convocatorias.csv` + `jugadores.csv` (conteo, veteranía). "Valor de mercado" **no existe** como campo en ningún CSV (`jugadores.csv` no tiene `valor_mercado`, verificado directamente). | Brecha mixta: parte de wiring, parte de datos. |
| **Compatibilidad Táctica** (005) | **A** | **No existe.** Sus "Datos necesarios" (Formación, Estilo de presión, Juego directo, Contraataque) no tienen campo en ningún CSV del módulo — no hay tabla de formaciones ni de estilo táctico en `data/processed/selecciones-nacionales/`. | **Brecha real de datos**, no de wiring — asignarle un motor hoy no la resolvería. |
| **Estado Psicológico** (011) | Sin asignar (`INC-08`) | **Parcial.** "Racha de victorias"/"Eliminación reciente" son derivables de `partidos.csv`/`torneos.csv`. "Clasificación" (tabla de posiciones) **no existe** — no hay `clasificacion.csv` ni campo equivalente en ningún archivo verificado. | Brecha mixta, agravada por no tener Nivel de importancia asignado. |

**Conclusión central:** `INC-04` mezcla dos problemas de naturaleza distinta que las misiones anteriores trataron como uno solo — un vacío de *asignación* (Localía, Historial Directo, y parcialmente Calidad de Plantilla, resolubles hoy sin tocar la Base de Conocimiento) y un vacío de *datos* (Compatibilidad Táctica y, parcialmente, Estado Psicológico, que requieren una misión de diseño de esquema nueva antes de poder resolverse).

## Alternativas

### Alternativa A — Asignar consumidor a las 5 ahora, sin distinción

- **Ventajas:** cierra el inventario completo de una sola vez; el Contrato de Variables queda 100% consumido.
- **Desventajas:** para Compatibilidad Táctica y Estado Psicológico no existe dato real que consumir — forzar un consumidor sin datos requeriría inventar valores o aproximar con datos que no corresponden a lo que la variable dice medir.
- **Riesgos:** Alto — contradice directamente "Nunca inventar datos" (`CLAUDE.md`, Constitución Art. 2 "Objetividad" y "Calidad").
- **Impacto futuro:** Negativo — crea la apariencia de estar resuelto mientras oculta una brecha real de datos.
- **Compatibilidad con Architecture Freeze:** Aparente, pero frágil — el criterio 4 de `docs/23` (Parte 6) quedaría marcado como cumplido de forma engañosa.

### Alternativa B — Diferenciar por disponibilidad real de datos

- Asignar consumidor **ahora** a Localía y Historial Directo (datos completos); asignar con alcance reducido a Calidad de Plantilla (solo la parte derivable); **diferir explícitamente**, con la razón documentada, Compatibilidad Táctica y Estado Psicológico hasta que exista una fuente de datos real.
- **Ventajas:** honesta con el estado real de la Base de Conocimiento; no inventa nada; cierra lo que sí puede cerrarse hoy; dofoja trazabilidad clara para lo que falta.
- **Desventajas:** dos variables (una de Nivel A) siguen sin consumidor tras esta misión — pero de forma documentada, no oculta, que es exactamente lo que el criterio 4 de `docs/23` exige ("consumidor confirmado **o** nota documentada explicando por qué no participa").
- **Riesgos:** Bajo — es la alternativa más alineada con los principios ya vigentes del proyecto.
- **Impacto futuro:** Positivo — separa con precisión "deuda barata" (wiring) de "deuda cara" (diseño de nuevo esquema de datos), permitiendo priorizarlas por separado.
- **Compatibilidad con Architecture Freeze:** Alta — el criterio 4 puede declararse cumplido honestamente para las 5, incluidas las 2 diferidas.

### Alternativa C — Diferir las 5 completas a una versión futura

- **Ventajas:** cero riesgo de una asignación apresurada.
- **Desventajas:** desperdicia que 2-3 de las 5 ya tienen datos completos hoy — deja el modelo más pobre de lo necesario sin ninguna razón técnica real.
- **Riesgos:** Bajo, pero con costo de oportunidad significativo (Localía es, en la literatura de predicción de fútbol, uno de los factores más establecidos y baratos de incorporar).
- **Compatibilidad con Architecture Freeze:** Sí, pero deja más sin resolver de lo estrictamente necesario.

## Recomendación final (INC-04)

**Alternativa B.** Específicamente, para una futura misión de implementación:

- **Localía** → asignar a `engine/03-Poisson.md` (ajuste directo del cálculo de goles esperados por condición de local — es el motor donde el efecto de localía se aplica de forma más natural en la literatura de modelos Poisson de fútbol).
- **Historial Directo** → asignar como factor contextual menor a `engine/04-Chaos-Index.md` o `engine/05-Confidence.md`, consistente con su autolimitación ya documentada en `docs/03`.
- **Calidad de Plantilla** → asignar con alcance reducido (solo "profundidad de plantilla", derivable de `convocatorias.csv`+`jugadores.csv`) a `engine/01`/`engine/02` como variable contextual; diferir "valor de mercado" hasta que exista esa fuente de datos.
- **Compatibilidad Táctica** → diferir formalmente a una futura misión de diseño de datos (`MS-`) que defina cómo capturar formación/estilo táctico en la Base de Conocimiento — no asignar motor hasta entonces.
- **Estado Psicológico** → diferir de la misma forma para su componente "Clasificación"; adicionalmente, recomendar que `docs/02-modelo.md` le asigne un Nivel de importancia (cierra `INC-08` de paso).

**Motivo:** es la única alternativa que resuelve honestamente lo resoluble hoy sin inventar datos para lo que no lo es.
**Impacto esperado:** el Contrato de Variables pasaría de "5 huérfanas sin distinción" a "3 resueltas + 2 formalmente diferidas con causa documentada" — una mejora real y verificable del estado del Engine.

---

# INC-05 — Acceso directo de `engine/06-Expected-Value.md` a `cuotas.csv`

## Problema

```
Base de Conocimiento
        │
        ▼
cuotas.csv
        │
        ▼
engine/06-Expected-Value.md
```

contradice el principio ya vigente:

```
Base de Conocimiento
        │
        ▼
Capa de Preparación de Variables
        │
        ▼
Motores
```

`engine/06` es, hoy, el único motor con esta excepción — confirmado y documentado explícitamente en `docs/06`/`docs/14` durante `MR-003`.

## Alternativas

### Alternativa A — Modelar las cuotas como una 13ª Variable Oficial dentro de `docs/16`

- Incorporar las cuotas al mismo Contrato Oficial de Variables que las 12 actuales (mismo esquema de tipo/unidad/rango/nulabilidad).
- **Ventajas:** desacoplamiento total y uniforme — todos los motores, sin excepción, consumen exclusivamente `docs/16`.
- **Desventajas:** las 12 Variables actuales describen **rendimiento deportivo de un equipo** (`docs/03-Variables.md` es explícito en esto); las cuotas son **datos de mercado** — de naturaleza distinta: múltiples casas de apuestas, múltiples mercados por partido, cambiantes en tiempo real, no atribuibles a "un equipo". Forzarlas dentro del mismo contrato diluiría su cohesión conceptual y obligaría a estirar un esquema pensado para otra cosa.
- **Riesgos:** Medio — riesgo de sobregeneralizar `docs/16` para un caso que no encaja naturalmente en su diseño actual.
- **Impacto futuro:** Alto si se ejecuta bien; genera deuda conceptual si se fuerza el encaje.
- **Compatibilidad con Architecture Freeze:** Alta si se resuelve — cierra `INC-05` por completo.

### Alternativa B — Las cuotas pasan por la Capa de Preparación de Variables como una categoría paralela, no como una Variable Oficial más

- `docs/15-Capa-de-Preparacion-de-Variables.md` sigue siendo la única responsable de leer `data/processed/` — pero entrega dos salidas tipadas y distintas: las 12 Variables Oficiales de rendimiento (para los 5 motores restantes) y un **paquete de datos de mercado preparado** (exclusivamente para `engine/06`), ya validado y normalizado, con su propio contrato (análogo a `docs/16` pero para cuotas, en un documento futuro).
- **Ventajas:** preserva el desacoplamiento total (ningún motor lee un CSV) sin forzar las cuotas dentro de un contrato diseñado para otra cosa; mantiene `docs/16` conceptualmente enfocado; es coherente con "Separación de Responsabilidades" (Constitución, Art. 2).
- **Desventajas:** introduce una segunda categoría de contrato — trabajo adicional (un documento nuevo, acotado) para especificarla.
- **Riesgos:** Bajo-Medio — es una extensión limpia de un diseño ya existente, no una improvisación.
- **Impacto futuro:** Alto y positivo — escala naturalmente a múltiples casas de apuestas o proveedores de cuotas futuros sin tocar el contrato de variables de rendimiento.
- **Compatibilidad con Architecture Freeze:** Alta.

### Alternativa C — Mantener la excepción, documentada como decisión permanente aceptada

- **Ventajas:** cero esfuerzo, cero riesgo inmediato.
- **Desventajas:** `engine/06` maneja directamente el componente que decide si se recomienda o no una apuesta con dinero real — es, de los seis motores, el que más se beneficiaría de estar aislado de la fuente física de datos (cambio de proveedor de cuotas, múltiples casas, migración a API).
- **Riesgos:** Bajo a corto plazo, medio-alto a largo plazo (escalabilidad).
- **Compatibilidad con Architecture Freeze:** Cuestionable como decisión pasiva ("no se corrigió"); aceptable únicamente si se documenta como una decisión arquitectónica deliberada y aprobada — no como un descuido.

## Recomendación final (INC-05)

**Alternativa B.** Preserva el principio de desacoplamiento sin forzar un encaje conceptual artificial entre datos de rendimiento deportivo y datos de mercado financiero. Requiere, en una futura misión de implementación: (1) extender `docs/15` o crear un documento hermano que defina el "Contrato de Datos de Mercado" (tipo, unidad, rango, nulabilidad de una cuota preparada — análogo a `docs/16`); (2) actualizar `engine/06-Expected-Value.md` para declarar que consume ese paquete preparado, no `cuotas.csv` directamente.

**Motivo:** de las tres alternativas, es la única que resuelve el problema de raíz (acoplamiento directo a la Base de Conocimiento) sin comprometer la cohesión conceptual de `docs/16` ni dejar una excepción permanente sin resolver.
**Impacto esperado:** `engine/06` pasaría a ser, como los otros 5 motores, completamente ciego al origen físico de sus datos.

---

# Cierre obligatorio

**1. ¿INC-04 es un problema real de diseño o solo documental?**
Es mixto, y esta es la aportación central de este análisis: para 3 de las 5 variables (Localía, Historial Directo, y parcialmente Calidad de Plantilla) es un problema puramente documental/de asignación — el dato ya existe. Para 2 (Compatibilidad Táctica, y parcialmente Estado Psicológico) es un problema real de diseño: falta la fuente de datos en la Base de Conocimiento, no solo un motor que la consuma.

**2. ¿Qué variables deberían pertenecer realmente al modelo V1?**
Localía, Historial Directo y Calidad de Plantilla (con alcance reducido) — con datos ya disponibles hoy. Compatibilidad Táctica y Estado Psicológico deberían diferirse formalmente a una versión futura, condicionadas a que exista primero una misión de diseño de datos que capture formación/estilo táctico y clasificación/tabla de posiciones.

**3. ¿INC-05 contradice la arquitectura definida?**
Sí, de forma directa: contradice el principio de desacoplamiento de `docs/15`, ya confirmado como excepción única entre los 6 motores tras `MR-003`.

**4. ¿Cuál es la solución recomendada para cuotas?**
Alternativa B: que pasen por la Capa de Preparación de Variables como una categoría de datos de mercado paralela y distinta a las 12 Variables Oficiales de rendimiento, con su propio contrato futuro.

**5. ¿Qué cambios serían necesarios después del análisis?**
Para INC-04: actualizar las secciones "Entradas" de `engine/03`, `engine/04`/`05`, `engine/01`/`02` (según la asignación recomendada) y `docs/17`; documentar explícitamente en `docs/03`/`docs/16` que Compatibilidad Táctica y Estado Psicológico quedan diferidas. Para INC-05: crear el Contrato de Datos de Mercado y actualizar `engine/06`. Ninguno de estos cambios se aplica en esta misión.

**6. ¿Qué riesgos aparecen al implementar cada alternativa?**
Ya detallados por alternativa en cada sección — el riesgo transversal más importante es el de la Alternativa A en ambos casos (INC-04 y INC-05): resolver "en apariencia" sin resolver en sustancia, lo cual sería peor que dejarlo documentado como está.

**7. ¿Cuál alternativa protege mejor la arquitectura a largo plazo?**
La Alternativa B en ambos casos — son las que priorizan la honestidad del estado real de los datos y la cohesión conceptual del Contrato de Variables por encima de cerrar el inventario rápidamente.

**8. ¿El Engine está preparado para Architecture Freeze después de resolver estas decisiones?**
Todavía no de forma automática: esta misión **recomienda**, no implementa. Una vez aprobadas estas recomendaciones por el Arquitecto Estadístico Humano y ejecutada la implementación correspondiente (más allá del alcance de esta misión), el criterio 1 (cero críticas) y el criterio 5 (ningún motor accede a `data/processed/` directamente) de `docs/23` podrían declararse cumplidos — quedaría además pendiente `INC-06` (duplicación de "Rotaciones"), que el `MR-004` original de `MR-001` incluía y que esta misión de análisis, enfocada exclusivamente en `INC-04`/`INC-05` según su propio brief, no cubre.

**9. ¿Qué misión debería ejecutarse después de esta?**
Dos, en paralelo o en secuencia según prioridad: (a) una misión de **implementación** (podría numerarse como continuación de `MR-004` o como una nueva `MR-008`) que aplique, tras aprobación humana, las recomendaciones aquí formuladas más la resolución de `INC-06`; (b) una misión de **diseño de datos** (`MS-`) que capture formación/estilo táctico y clasificación/tabla de posiciones en la Base de Conocimiento, condición previa para que Compatibilidad Táctica y Estado Psicológico dejen de estar diferidas.

**10. ¿Qué decisiones requieren aprobación del Arquitecto Estadístico Humano antes de implementarse?**
Todas las de esta misión, sin excepción — cualquier cambio que afecte qué motor consume qué variable, o cómo se estructura el Contrato de Variables/Datos de Mercado, es exactamente el tipo de decisión que la Constitución (Art. 2, "No autoaprobación"; Art. 5) reserva al Arquitecto Estadístico Humano. El Arquitecto Estadístico IA (este análisis) solo puede proponer, nunca decidir ni aplicar.

---

# Fuera de alcance de esta misión

- No se implementa ninguna de las recomendaciones.
- No se modifica ningún documento, motor, variable, algoritmo, peso ni el pipeline.
- No se resuelve `INC-06` (duplicación de "Rotaciones") — fuera del alcance declarado de este brief.
- No se diseña el esquema de datos tácticos/clasificación necesario para Compatibilidad Táctica/Estado Psicológico — se recomienda como misión futura, no se ejecuta aquí.

---

Fin del documento.
