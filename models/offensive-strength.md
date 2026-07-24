# Offensive Strength — Fuerza Ofensiva

**Archivo:** `models/offensive-strength.md`

**Misión:** MODEL-001 — Modelo Matemático de Fuerza Ofensiva (primera misión con prefijo "MODEL-") / MODEL-009 — Especificación Oficial de Variable003 para V1 (operacionaliza la sección 6.1 ya existente: fuente exacta, ventana temporal, pesos placeholder con metodología, casos límite y complejidad computacional)

**Versión:** 2.1.0-investigación

**Estado:** Investigación — estructura de la fórmula definida; coeficientes (pesos) **pendientes de calibración estadística** con datos reales, conforme a `CLAUDE.md` ("Nunca alterar pesos sin evidencia estadística"). Desde `MODEL-009`, la construcción de Variable003 (sección 6.1) tiene además una especificación V1 completamente operacional (secciones 17-25) — implementable en código en cuanto existan datos reales, sin requerir más decisiones de diseño.

---

# 1. Objetivo

Investigar y proponer cómo medir la capacidad ofensiva real de un equipo — el fundamento matemático que `engine/01-Offensive-Strength.md` implementará. Este documento es la fuente de verdad de esa fórmula; `engine/01` la ejecuta, no la define (`CLAUDE.md`: "Investigación antes de implementación").

---

# 2. Descripción

La Fuerza Ofensiva representa la capacidad de un equipo para generar peligro y convertir oportunidades de gol de forma **sostenible** — no la cantidad de goles ya anotados, que incluye ruido de finalización (suerte, rachas puntuales). Coincide, en su definición conceptual, con la Variable Oficial `Potencial Ofensivo` (Variable003, `docs/03-Variables.md`): ambas describen el mismo fenómeno. La diferencia es de alcance: Variable003 es la señal de producción ofensiva pura (basada en tiro), mientras que la Fuerza Ofensiva que produce `engine/01` es esa señal **ajustada por el contexto actual del equipo** (forma, disponibilidad de plantilla).

---

# 3. Problema que Resuelve

Convertir múltiples estadísticas ofensivas — algunas de producción pura (xG, disparos), otras de contexto (forma, disponibilidad) — en un único indicador comparable entre cualquier par de equipos, sin depender únicamente de goles anotados y sin mezclar responsabilidades que no le corresponden (el ajuste por rival, por ejemplo, pertenece a `engine/03-Poisson.md`, no a este modelo).

---

# 4. Variables Oficiales utilizadas

*(Verificado contra `docs/17-Matriz-de-Consumo-de-Variables.md` — no se usa ninguna variable que ese documento no asigne a `engine/01`.)*

| Variable | Rol en la fórmula | Por qué participa |
|---|---|---|
| **Variable003** — Potencial Ofensivo | Término base (`P`) | Es la señal primaria de producción ofensiva — `engine/01` la declara "Variables Primarias... representan directamente la producción ofensiva" |
| **Variable001** — Forma Reciente | Modificador multiplicativo de contexto | Declarada "Variable Secundaria" en `engine/01`: "ajusta el contexto de la producción ofensiva" |
| **Variable002** — Rendimiento en el Torneo | Modificador multiplicativo de contexto | Mismo rol que Variable001, mismo origen textual |
| **Variable006** — Disponibilidad de Plantilla | Penalización acotada | "Variable Contextual... modifica el resultado final cuando exista evidencia suficiente" |
| **Variable007** — Fatiga | Penalización acotada | Mismo rol que Variable006 |
| **Variable008** — Calidad de Plantilla (alcance reducido, `MR-004`) | Penalización acotada | Asignada a `engine/01` por `MR-004`; participa con el mismo rol que Variable006/007 |

## Variables que NO participan, y por qué

- **Variable004** (Solidez Defensiva): pertenece a `engine/02`, no a la producción ofensiva.
- **Variable005** (Compatibilidad Táctica): formalmente diferida (`MR-004`) — sin fuente de datos en la Base de Conocimiento actual.
- **Variable009** (Localía): asignada a `engine/03-Poisson.md` (`MR-004`) — afecta el cálculo de goles esperados, no la fuerza ofensiva de base.
- **Variable010** (Historial Directo): asignada a `engine/05-Confidence.md` (`MR-004`).
- **Variable011** (Estado Psicológico): formalmente diferida (`MR-004`).
- **Variable012** (Factores Externos): asignada a `engine/04-Chaos-Index.md`.

Ninguna de estas seis se incorpora aquí — hacerlo contradiría la Matriz de Consumo ya vigente (`docs/17`), y esta misión no está autorizada a modificarla.

---

# 5. Fundamentación estadística

Dos cuerpos de teoría respaldan esta propuesta, sin copiarse ni inventarse:

1. **Expected Goals (xG) como proxy de calidad ofensiva.** Es una metodología pública y ampliamente documentada en el análisis de fútbol moderno (popularizada por proveedores como Opta y Understat): estima la probabilidad de gol de cada disparo según sus características (distancia, ángulo, tipo de jugada), y su suma por partido correlaciona más establemente con el rendimiento ofensivo futuro que los goles reales, que incluyen varianza de finalización.
2. **Modelos de fuerza de ataque/defensa en fútbol**, cuyo origen académico está en Maher, M.J. (1982), *"Modelling Association Football Scores"*, Statistica Neerlandica, 36(3), y su refinamiento en Dixon, M.J. y Coles, S.G. (1997), *"Modelling Association Football Scores and Inefficiencies in the Football Betting Market"*, Journal of the Royal Statistical Society: Series C, 46(2). Ambos establecen el concepto de un parámetro de "fuerza ofensiva" por equipo, estimado a partir de goles marcados, como insumo de un modelo de Poisson.

**Diferencia honesta con Dixon-Coles:** Dixon-Coles estima sus parámetros de ataque por máxima verosimilitud sobre el historial completo de una liga — requiere una temporada de datos de una competición cerrada. El Modelo Santiago opera sobre selecciones nacionales en múltiples competiciones distintas (`data/processed/selecciones-nacionales/competiciones.csv` — MS-006), sin una liga única y con muestras mucho más pequeñas por selección. Por eso esta propuesta usa un método más simple y robusto a datos escasos: un **índice compuesto estandarizado** en lugar de una estimación por máxima verosimilitud. Adoptar un enfoque más cercano a Dixon-Coles queda documentado como posible Versión 3.0 (sección "Versión 2.0" al final), condicionado a que exista suficiente historial acumulado en `data/results/`.

---

# 6. Fórmula propuesta

## 6.1 Construcción del término base (`P`, a partir de Variable003)

Sobre una ventana de los últimos *N* partidos oficiales (*N* a determinar en calibración — no se fija aquí un valor sin evidencia). **De las cinco métricas siguientes, solo 3 tienen campo disponible hoy en `estadisticas_partido.csv`** (`xg`, `disparos_totales`, `disparos_al_arco`) — "grandes oportunidades" no existe en ningún archivo del esquema y "conversión" requiere un cálculo derivado (ver "Limitaciones", sección 13). Se documentan las cinco porque son las declaradas en `docs/03-Variables.md` para Variable003; las dos no disponibles se incorporan cuando exista su fuente:

```
Para cada métrica i ∈ {xG, disparos totales, disparos al arco, grandes oportunidades, conversión}:

    z_i = (x̄_i − μ_i,competición) / σ_i,competición

Z = Σ vᵢ · zᵢ                     (vᵢ = pesos por métrica, Σvᵢ = 1, pendientes de calibración)

P = 100 · Φ(Z / s)                (Φ = función de distribución acumulada normal estándar;
                                    s = factor de escala; P se acota a [0, 100])
```

`P` es, en esta notación, el valor de Variable003 tal como lo entrega la Capa de Preparación de Variables (`docs/15`) — esta subsección documenta cómo se construye, porque ningún documento anterior lo había definido matemáticamente (`docs/03`, Variable003, "Método de cálculo: Pendiente").

## 6.2 Modificador de forma

```
r = (Variable001 − 50) / 50        ∈ [−1, 1]
t = (Variable002 − 50) / 50        ∈ [−1, 1]

M_forma = 1 + clip( w_R·r + w_T·t , −δ_max, +δ_max )
```

`δ_max` es el límite máximo de ajuste (ej. 0.20 = ±20%) — un valor razonable propuesto para acotar el modelo, sujeto también a calibración.

## 6.3 Penalización por disponibilidad

```
Pen = w_D·(1 − Variable006/100) + w_F·(Variable007/100) + w_Q·(1 − Variable008/100)

Pen = clip( Pen , 0, Pen_max )     (ej. Pen_max = 0.30)
```

*(Convención propuesta, no definida en ningún documento anterior: Variable007 "Fatiga" se interpreta 0 = sin fatiga, 100 = fatiga máxima — a confirmar cuando `docs/16` lo formalice.)*

## 6.4 Fórmula final

```
Fuerza Ofensiva = clip( P · M_forma · (1 − Pen) , 0, 100 )
```

**Ningún peso (`vᵢ`, `w_R`, `w_T`, `w_D`, `w_F`, `w_Q`) recibe un valor numérico en este documento** — se define su rol estructural, no su magnitud, para no violar "Nunca alterar pesos sin evidencia estadística" (`CLAUDE.md`). Los valores numéricos requieren calibración contra `data/results/` real, hoy inexistente.

---

# 7. Justificación

La estructura (base × modificador de forma × penalización) refleja exactamente la jerarquía que `engine/01` ya declara por sí mismo, sin que esta misión la redefina: "Variables Primarias" (base), "Variables Secundarias" (ajustan el contexto — de ahí el modificador multiplicativo, no aditivo, porque un ajuste de contexto debe escalar proporcionalmente a la fuerza base, no sumarse en las mismas unidades) y "Variables Contextuales" (modifican el resultado final cuando exista evidencia — de ahí la penalización acotada, que vale 0 cuando no hay evidencia, nunca un valor inventado). Esta correspondencia 1 a 1 con la propia documentación de `engine/01` es, en sí misma, la validación de que la fórmula no contradice al motor que la implementará (ver "Validaciones obligatorias").

---

# 8. Escala de salida

- **Rango:** 0 a 100, siempre — acotado por construcción (`clip` en cada etapa), nunca requiere una validación externa de rango.
- **Interpretación propuesta** (consistente con el estilo ya usado en `docs/02-modelo.md` para Confianza/Caos):

| Rango | Interpretación |
|---|---|
| 81-100 | Ataque de élite |
| 61-80 | Ataque fuerte |
| 41-60 | Ataque promedio |
| 21-40 | Ataque débil |
| 0-20 | Ataque muy débil |

- **Comportamiento en extremos:** el `clip` final impide que un modificador de forma muy favorable empuje la Fuerza Ofensiva por encima de 100 aunque `P` ya esté cerca del máximo — el modelo satura, no se desborda. Un `P` muy bajo (equipo con pobre producción de tiro sostenida) nunca puede compensarse completamente con buena forma, porque `δ_max` acota el modificador — evita que "tres victorias recientes" hagan parecer élite a un equipo con datos de tiro pobres.

---

# 9. Sensibilidad

| Variable | Efecto al aumentar | Naturaleza del efecto |
|---|---|---|
| Variable003 (`P`) | Aumenta la Fuerza Ofensiva de forma directa y proporcional | Lineal — es el término base |
| Variable001 / Variable002 | Aumenta la Fuerza Ofensiva, acotado | Multiplicativo con techo (`δ_max`) — rendimientos marginales decrecientes cerca del límite |
| Variable006 (Disponibilidad) | Al **disminuir**, aumenta la penalización, reduciendo la Fuerza Ofensiva | Lineal dentro del rango acotado por `Pen_max` |
| Variable007 (Fatiga) | Al **aumentar**, aumenta la penalización | Idem |
| Variable008 (Calidad de Plantilla) | Al **disminuir**, aumenta la penalización | Idem, con menor peso esperado que Disponibilidad/Fatiga (alcance ya reducido por `MR-004`) |

Ninguna variable, individualmente, puede llevar la Fuerza Ofensiva a 0 ni a 100 por sí sola salvo que `P` mismo esté en un extremo — es una propiedad deliberada de diseño, no un efecto secundario.

---

# 10. Casos límite

- **Selección muy ofensiva** (P ≈ 95, buena forma): `M_forma` cerca de `1+δ_max`, `Pen` cerca de 0 (plantilla completa) → Fuerza Ofensiva cerca de 100, acotada por el `clip`.
- **Selección muy defensiva / poco ofensiva** (P ≈ 15): incluso con forma excelente, `M_forma` acotado (`δ_max` ≈ 0.20) no puede compensar un `P` bajo — Fuerza Ofensiva permanece en el rango "débil".
- **Selección sin información suficiente:** si Variable003 (obligatoria, Nivel A) no puede construirse, el pipeline se detiene **antes** de llegar a `engine/01` (`docs/06-Flujo-Operacional.md`, tabla "Manejo de errores") — este modelo nunca recibe un `P` inexistente ni lo estima. Si Variable001/002 no están disponibles (ej. debut en el torneo), su término correspondiente se fija en 0 dentro de `M_forma` — sin ajuste, nunca un valor inventado — y la ausencia se propaga como menor confianza hacia `engine/05` (`docs/15`, sección 6).
- **Selección recién creada / sin historial:** mismo caso que el anterior — `M_forma` se reduce a 1 (neutro) si no hay muestra suficiente, y `Pen` se mantiene en 0 si tampoco hay datos de disponibilidad; la Fuerza Ofensiva queda determinada casi enteramente por `P`, con confianza reducida declarada explícitamente.

---

# 11. Supuestos

1. La normalización 0-100 de Variable001, Variable002, Variable006, Variable007 y Variable008, ya realizada por la Capa de Preparación de Variables (`docs/15`), es válida y no se reevalúa aquí.
2. `P` (Variable003) y los modificadores de forma (Variable001/002) son **aproximadamente independientes** — un supuesto simplificador, no demostrado: en la práctica, un equipo en buena forma reciente probablemente también tenga buenos números de tiro recientes, lo que podría producir un doble conteo parcial del mismo efecto. Se documenta como limitación (sección 13), no se ignora.
3. La ventana *N* de partidos usada para construir `P` es suficientemente representativa del nivel actual del equipo — coherente con el Principio 1 del proyecto ("los datos actuales pesan más que la historia", `docs/02-modelo.md`), pero el valor exacto de *N* queda pendiente de calibración.
4. Los componentes de `P` (xG, disparos, disparos al arco, grandes oportunidades, conversión) se distribuyen de forma suficientemente cercana a la normalidad dentro de una competición como para que la transformación `Φ(Z/s)` sea razonable — si la calibración futura muestra lo contrario, se sustituiría por un percentil empírico (alternativa ya prevista, no una redefinición posterior).

---

# 12. Ventajas

- Estructura totalmente trazable a las Variables Oficiales ya contratadas (`docs/16`) — ningún término sin origen documentado.
- Acotada por diseño (0-100 en cada etapa) — nunca requiere validación externa de rango ni produce valores absurdos.
- Separa explícitamente producción (base), contexto reciente (modificador) y disponibilidad (penalización) — refleja, sin contradecirla, la propia estructura de tres niveles que `engine/01` ya declara.
- No fija ningún peso sin evidencia — cumple `CLAUDE.md` de forma literal, no solo en espíritu.

---

# 13. Limitaciones

- Los pesos son, hoy, símbolos sin calibrar — el modelo no puede evaluarse cuantitativamente (RMSE, log-loss, etc.) hasta que existan datos reales suficientes en `data/results/`.
- El supuesto de independencia entre `P` y los modificadores de forma (sección 11, supuesto 2) es una simplificación que podría sobreponderar la forma reciente si ambas señales están correlacionadas.
- No modela explícitamente la calidad del rival — deliberado: ese ajuste pertenece a `engine/03-Poisson.md`, que combina Fuerza Ofensiva propia con Fuerza Defensiva rival. Incluirlo aquí duplicaría esa responsabilidad.
- **Verificado directamente contra el esquema real** (`data/processed/selecciones-nacionales/estadisticas_partido.csv`): de las cinco métricas de la sección 6.1, solo tres tienen campo propio hoy (`xg`, `disparos_totales`, `disparos_al_arco`). "Grandes oportunidades" **no existe como campo en ningún archivo** del módulo — no puede calcularse hasta que se incorpore al esquema. "Conversión" no está almacenada directamente; requeriría un cálculo derivado (goles del equipo en `partidos.csv` ÷ `disparos_totales` de `estadisticas_partido.csv`), no una consulta directa. La fórmula de la sección 6.1 puede ejecutarse hoy con 3 de 5 métricas — las otras dos quedan como componentes futuros del índice, no como bloqueantes de esta investigación.

---

# 14. Aplicación dentro del Modelo Santiago

Es la especificación matemática oficial que `engine/01-Offensive-Strength.md` deberá implementar en su "Versión 2.0" (ya prevista en su propio documento: "Fórmula matemática completa. Método de normalización. Cálculo de ponderaciones."). Su salida (Fuerza Ofensiva) alimenta directamente a `engine/03-Poisson.md` (cálculo de goles esperados) y, transitivamente, a `engine/04`/`05`/`06`.

---

# 15. Referencias

- Maher, M.J. (1982). "Modelling Association Football Scores." *Statistica Neerlandica*, 36(3), 109-118.
- Dixon, M.J. y Coles, S.G. (1997). "Modelling Association Football Scores and Inefficiencies in the Football Betting Market." *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 46(2), 265-280.
- Metodología de Expected Goals (xG): documentación pública de proveedores de datos de fútbol (Opta, Understat) — concepto ampliamente estandarizado en la industria, sin una única fuente académica canónica.
- Estandarización por z-score y construcción de índices compuestos: técnica estadística general de análisis multicriterio, no atribuible a una fuente única.

---

# 16. Versión 2.0 (siguiente iteración de esta investigación — no de la implementación en `engine/`)

Pendiente, condicionado a la existencia de suficiente historial real en `data/results/`:

- Calibración estadística de todos los pesos (`vᵢ`, `w_R`, `w_T`, `w_D`, `w_F`, `w_Q`, `δ_max`, `Pen_max`, `N`) mediante regresión o validación cruzada contra resultados reales.
- Evaluación de si un enfoque más cercano a Dixon-Coles (estimación por máxima verosimilitud) mejora la capacidad predictiva frente a este índice compuesto, una vez exista suficiente volumen de datos por competición.
- Validación del supuesto de independencia entre `P` y los modificadores de forma (sección 11).
- Definición formal, en `docs/16-Contrato-Oficial-de-Variables.md`, de la dirección de Variable007 (Fatiga) — hoy solo una convención propuesta en este documento.

---

# Validaciones obligatorias

- **¿Todas las variables utilizadas pertenecen al Contrato Oficial?** Sí — las 6 de la sección 4 están en `docs/16-Contrato-Oficial-de-Variables.md`; ninguna variable ajena al contrato participa en la fórmula.
- **¿La fórmula puede implementarse posteriormente?** Sí, en cualquier lenguaje — es una composición de operaciones aritméticas estándar (z-score, CDF normal, combinación lineal acotada, `clip`), sin dependencias de una tecnología concreta.
- **¿No contradice al Engine?** Verificado explícitamente en la sección 7 ("Justificación"): la estructura de tres niveles (base/modificador/penalización) es una correspondencia directa, no una redefinición, de los tres niveles ("Primarias/Secundarias/Contextuales") que `engine/01-Offensive-Strength.md` ya declara en su propio texto, sin editarlo.
- **¿La salida es reproducible?** Sí — es una función determinista de sus entradas; los mismos valores de Variable001/002/003/006/007/008 producen siempre la misma Fuerza Ofensiva, una vez fijados los pesos.

---

# Cierre obligatorio

**1. ¿Qué representa matemáticamente la Fuerza Ofensiva?**
Un índice acotado 0-100, resultado de un término base de producción ofensiva (derivado de estadísticas de tiro estandarizadas) ajustado multiplicativamente por la forma reciente y penalizado por la disponibilidad de plantilla.

**2. ¿Qué variables consume?**
Variable003 (base), Variable001 y Variable002 (modificador de forma), Variable006, Variable007 y Variable008 (penalización de disponibilidad) — las 6 confirmadas por `docs/17` como asignadas a `engine/01`.

**3. ¿Por qué esas variables?**
Porque son, exactamente, las que `docs/17-Matriz-de-Consumo-de-Variables.md` ya asigna a este motor — ninguna se eligió de forma independiente a esa matriz ya vigente.

**4. ¿Qué fórmula se propone?**
`Fuerza Ofensiva = clip(P · M_forma · (1 − Pen), 0, 100)`, con `P` derivado de un índice compuesto estandarizado de estadísticas de tiro, `M_forma` un modificador acotado de forma reciente, y `Pen` una penalización acotada por disponibilidad/fatiga/calidad de plantilla — desarrollada en la sección 6.

**5. ¿Qué ventajas tiene?**
Trazabilidad completa a variables ya contratadas, acotación por diseño, y separación fiel a la estructura de tres niveles que el propio `engine/01` ya declaraba (sección 12).

**6. ¿Qué limitaciones tiene?**
Pesos sin calibrar todavía; supuesto de independencia entre producción y forma no demostrado; y una brecha de datos real recién detectada: "grandes oportunidades" no existe en el esquema actual, "conversión" requiere cálculo derivado (sección 13).

**7. ¿Qué necesitará el Engine para implementarla?**
Valores numéricos calibrados para cada peso (`vᵢ`, `w_R`, `w_T`, `w_D`, `w_F`, `w_Q`, `δ_max`, `Pen_max`, `N`) — imposibles de fijar hoy sin violar "Nunca alterar pesos sin evidencia estadística" — y, eventualmente, que el esquema de `estadisticas_partido.csv` incorpore "grandes oportunidades" si se decide que el índice de producción lo necesita completo.

**8. ¿Qué documento recomendarías desarrollar después?**
`models/poisson.md` — es el siguiente motor en la cadena de dependencias (`engine/03` consume directamente la salida de este modelo) y hoy sigue en estado "Investigación" sin fórmula.

**9. ¿Puede considerarse este modelo listo para implementación?**
La **estructura** sí; los **coeficientes**, no — exactamente la misma distinción que ya hizo `docs/26-Runtime-del-Modelo.md` sobre la arquitectura de ejecución en general. Implementar el código hoy produciría una fórmula sintácticamente correcta pero sin calibrar, lo cual no es una predicción confiable todavía.

**10. ¿Qué riesgos estadísticos existen?**
Tres, principalmente: (a) sobreponderación de la forma reciente si realmente correlaciona con `P` (supuesto de independencia no verificado); (b) sobreajuste si los pesos se calibran con una muestra todavía pequeña de resultados reales; (c) el supuesto de normalidad de la sección 6.1 podría no sostenerse con datos reales, en cuyo caso la transformación `Φ(Z/s)` debería sustituirse por un percentil empírico, ya previsto como alternativa (sección 11, supuesto 4) pero no validado.

---

# Fuera de alcance de esta misión

- No se implementa código ni pseudocódigo.
- No se modifica `engine/01-Offensive-Strength.md`, el Runtime, el Pipeline, las Variables Oficiales, `learning/` ni la Base de Conocimiento.
- No se fija ningún valor numérico de peso — solo su rol estructural.
- No se corrige la ausencia de "grandes oportunidades" en el esquema de datos — se documenta como limitación, no se resuelve.

---

# MODEL-009 — Especificación Oficial de Variable003 para V1

*(Secciones agregadas por `MODEL-009`. Origen: `BUILD-017` detectó que `VariablePreparation` no podía producir Variable003 porque, aunque la sección 6.1 ya definía la estructura de la fórmula desde `MODEL-001`, faltaban las decisiones operacionales necesarias para convertirla en código — fuente exacta de cada métrica, ventana temporal, un valor concreto de `s`, y el tratamiento de casos límite. Esta sección cierra ese vacío sin redefinir la fórmula ya aprobada en la sección 6.1 — la opera-cionaliza.)*

## 17. Aclaración de nomenclatura

El brief de `MODEL-009` se refiere a esta variable como "Variable003 (Nivel de Juego)". El nombre oficial, fijado consistentemente desde `docs/03-Variables.md`, `docs/16-Contrato-Oficial-de-Variables.md`, `docs/17-Matriz-de-Consumo-de-Variables.md` y la sección 2 de este mismo documento, es **"Potencial Ofensivo"** — ningún documento del proyecto usa "Nivel de Juego". Se trata como el mismo nombre informal de la misma variable (mismo número, Variable003), no como una variable distinta ni un renombramiento — esta sección lo deja explícito para no introducir una segunda etiqueta en la documentación oficial.

## 18. Por qué no se adopta el ejemplo ilustrativo del brief

El brief ilustra con `NivelJuego = 0.45·Forma + 0.30·Ataque + 0.15·Defensa + 0.10·Rival` — "no necesariamente esta". Verificado antes de continuar: esa estructura, tomada literalmente, incorporaría un componente de **Defensa** (Variable004, asignada exclusivamente a `engine/02` por `docs/17`) y un ajuste de **Rival** (asignado exclusivamente a `engine/03-Poisson.md` por `docs/17` y `models/poisson.md` §6, "Fuerza Base cruzada") dentro de Variable003 — contradiciendo la Matriz de Consumo ya vigente, que esta misión no está autorizada a modificar. No se adopta. La especificación de esta sección permanece dentro del alcance ya fijado por `docs/03`/`docs/17` para Variable003: producción ofensiva pura de un equipo, sin componente defensivo ni ajuste de rival (ese ajuste ya ocurre, correctamente, dentro de `models/poisson.md` §6, sobre la Fuerza Ofensiva ya calculada).

## 19. Definición operacional exacta

**Variable003 (Potencial Ofensivo)** representa la capacidad de una selección para generar y convertir oportunidades de gol, medida como un índice compuesto y estandarizado (0-100) de sus estadísticas de tiro — Expected Goals (`xG`), volumen de disparos y precisión de disparos — durante sus últimos `N` partidos oficiales, expresada en relación con las demás selecciones de la misma competición durante la misma ventana temporal.

No mide goles anotados directamente (esos incluyen varianza de finalización, `models/offensive-strength.md` §2) ni depende de la calidad del rival (ese ajuste pertenece a `engine/03`) ni de la fase del torneo. Es, exclusivamente, una medida relativa de producción ofensiva reciente.

## 20. Fuente de datos

| Métrica | Archivo | Columna | Disponibilidad hoy |
|---|---|---|---|
| `xG` | `data/processed/selecciones-nacionales/estadisticas_partido.csv` | `xg` | Columna existe; **0 filas** (verificado antes de escribir, `BUILD-017`) |
| Disparos totales | `estadisticas_partido.csv` | `disparos_totales` | Igual |
| Disparos al arco | `estadisticas_partido.csv` | `disparos_al_arco` | Igual |
| Ventana de partidos (fecha, resultado, competición) | `partidos.csv` | `fecha`, `id_torneo`, `estado_partido` | Columnas existen; **0 filas** |
| Agrupación por competición | `torneos.csv` → `competiciones.csv` | `id_competicion` | Ya usado en `mu_gol_provider.py` (`BUILD-016`), mismo patrón de `join` |

**Por qué solo estas fuentes, y por qué no ranking FIFA/Elo:** el Contrato Oficial de Variables (`docs/16`) no autoriza ninguna fuente externa para Variable003 — su columna "Fuente" fija exclusivamente "Capa de Preparación de Variables" a partir de la Base de Conocimiento ya modelada (`docs/33`). Incorporar ranking FIFA o un sistema Elo introduciría una variable/fuente nueva no contratada, fuera del alcance de esta misión (`CLAUDE.md`: "Ningún motor podrá incorporar nuevas fórmulas, variables o algoritmos sin una investigación previa documentada"; esta misión investiga Variable003 tal como ya está contratada, no propone una fuente alternativa).

**"Grandes oportunidades" y "Conversión"** (las otras dos métricas que `docs/03` lista para Variable003): se mantienen fuera del cálculo V1, exactamente como ya lo dejó `MODEL-001` §13 — "Grandes oportunidades" no existe como campo en ningún archivo del esquema (no derivable sin ampliar `docs/33`, fuera de alcance); "Conversión" sería técnicamente derivable (goles del equipo, `partidos.csv`, dividido por `disparos_totales`), pero se deja fuera de la fórmula oficial V1 por prudencia metodológica: incorporar una métrica derivada nueva a la construcción de `Z` es una decisión de diseño que esta misión prefiere no tomar unilateralmente sin evidencia de que mejora el índice — queda documentada como candidata explícita de V1.1 (sección 25).

## 21. Fórmula oficial V1 (operacionalización de la sección 6.1)

Restringida a las tres métricas con fuente real hoy (sección 20) — la estructura general de la sección 6.1 no cambia, solo se fija `i ∈ {xG, disparos totales, disparos al arco}` en lugar de las cinco originales:

```
Para cada métrica i ∈ {xG, disparos_totales, disparos_al_arco}:

    x̄_i(equipo)      = promedio de la métrica i del equipo sobre sus últimos N partidos oficiales (sección 22)
    μ_i(competición) = promedio de la métrica i de TODOS los equipos de la misma competición, sobre la misma ventana temporal
    σ_i(competición) = desviación estándar de la métrica i, misma población que μ_i

    z_i = (x̄_i(equipo) − μ_i(competición)) / σ_i(competición)

Z = Σ vᵢ · zᵢ                      (i = 1..3)

P = 100 · Φ(Z / s)                  (Φ = CDF normal estándar; P acotado a [0, 100] por construcción de Φ)
```

**Pesos — placeholder documentado, no calibrado (`CLAUDE.md`: "nunca inventar pesos sin justificar"):**

- `v₁ = v₂ = v₃ = 1/3`: ponderación **igualitaria**, no arbitraria — mismo criterio ya usado en todo el proyecto (`Engine01`/`Engine02`/`Engine04`/`Engine05`, `BUILD-009` a `BUILD-017`) cuando "ninguna evidencia favorece un término sobre otro". No hay, hoy, ningún estudio o dato que indique que `xG` deba pesar más o menos que el volumen o la precisión de disparos.
- `s = √(Σ vᵢ²) = √(3 · (1/3)²) = √(1/3) ≈ 0.577`: **no es un número elegido a mano** — es la desviación estándar teórica de `Z` bajo el supuesto de que cada `zᵢ` es aproximadamente `N(0,1)` e independiente entre sí (mismo supuesto de independencia ya documentado como limitación en la sección 11, supuesto 4). Se deriva matemáticamente de los propios pesos `vᵢ`, no se propone como un valor adicional sin origen. Fijar `s = 1` sin este ajuste comprimiría artificialmente `Z/s` hacia el centro de `Φ` (dado que `Var(Z) ≈ 1/3 < 1`), sin ninguna justificación para esa compresión.

**Metodología de calibración real (futura, no de esta misión):** los tres símbolos (`v₁`, `v₂`, `v₃`) deben re-estimarse mediante uno de los métodos ya catalogados en `models/parameter-calibration.md` §7 — Maximum Likelihood Estimation es el candidato natural (mismo método ya recomendado ahí para parámetros de ataque/defensa, citando Maher 1982/Dixon-Coles 1997), una vez exista suficiente historial en `data/results/`. `s` debería, en ese momento, recalcularse empíricamente a partir de la varianza real observada de `Z` en los datos, no derivarse teóricamente como aquí.

## 22. Variables internas y ventana temporal

**Métricas necesarias** (por equipo, por partido, agregadas sobre la ventana): `xg`, `disparos_totales`, `disparos_al_arco` — exactamente las tres columnas de la sección 20, sin ninguna métrica adicional no listada en `docs/03`.

**Ventana temporal — `N = 10` últimos partidos oficiales.** Placeholder estructural, no calibrado (mismo estatus que los pesos, sección 21): la sección 6.1 original dejaba `N` explícitamente sin fijar ("N a determinar en calibración"). Esta misión propone `N = 10` como valor operacional necesario para que `VariablePreparation` pueda ejecutar una consulta concreta — no una media móvil ni una ponderación exponencial (ambas explícitamente fuera de alcance del brief de esta misión), sino una ventana simple de los `N` partidos oficiales más recientes, sin ponderar por antigüedad dentro de la ventana. Se elige `10` por ser un múltiplo común en métricas de "forma" de análisis de fútbol (ampliamente usado por proveedores de datos públicos, sin una única fuente académica atribuible) — no una calibración estadística contra `data/results/`, que sigue sin existir. **TODO explícito:** recalibrar `N` (`models/parameter-calibration.md` §7) en cuanto exista evidencia suficiente.

`μ_i(competición)`/`σ_i(competición)` se calculan sobre la **misma ventana temporal**, no sobre todo el historial de la competición — mismos partidos recientes de todos los equipos de esa competición, para que la comparación sea contemporánea y no mezcle eras competitivas distintas.

## 23. Normalización

Rango de salida: **0 a 100**, heredado sin cambios de la sección 8 de este mismo documento (ya vigente, `docs/16`: Variable003 es "Índice (0-100)"). `Φ` (CDF normal estándar) satura naturalmente el resultado dentro de `[0,1]`, escalado a `[0,100]` por el factor `100·`. No requiere una segunda normalización ni un `clip` adicional — la propia función `Φ` ya lo garantiza matemáticamente, a diferencia de las etapas de `M_forma`/`Pen` en la sección 6 (que sí usan `clip`, por ser combinaciones lineales sin cota natural).

## 24. Casos límite

| Caso | Comportamiento |
|---|---|
| **Equipo con menos de `N` partidos oficiales disponibles** | Se usa el subconjunto disponible (nunca se completa artificialmente hasta `N`); `muestra_reducida = True` se propaga en `ValorVariable` (`docs/30` §4.3) para que `Engine05` lo refleje en su Índice de Confianza — mismo mecanismo ya usado para Variable006/007/010 |
| **Equipo con cero partidos oficiales con estadísticas válidas en la ventana** | Variable003 se marca `disponible = False` — nunca un valor inventado. Como es obligatoria (Nivel A, `docs/17`), el pipeline se detiene antes de `engine/01` (`docs/06`, tabla "Manejo de errores"; ya el comportamiento exacto que `Engine01`/`VariableObligatoriaNoDisponible` implementan desde `BUILD-009`) |
| **Selección nueva / debut en la Base de Conocimiento** | Mismo caso que la fila anterior — cero partidos históricos equivale a "sin evidencia", no a un caso especial con lógica propia. No se introduce ningún mecanismo de "período de gracia" no solicitado por ningún documento |
| **Cambio completo de plantilla** | Sin mecanismo especial — la ventana de `N` partidos ya es "reciente" por construcción; en cuanto la nueva plantilla acumule partidos dentro de la ventana, el índice los refleja automáticamente. No se requiere detectar el cambio explícitamente (evita inventar una señal no solicitada) |
| **Competición con muy pocos partidos registrados en la ventana** (`σ_i(competición)` indefinida o igual a 0) | Esa métrica `i` se excluye del cálculo de `Z` para todos los equipos de esa competición en ese momento (mismo tratamiento que una variable opcional ausente, sección 6.2: "sin ajuste, nunca un valor inventado"); si las tres métricas quedan excluidas, Variable003 se marca `disponible = False` — nunca se divide por cero ni se sustituye `σ` por un valor arbitrario |

## 25. Complejidad computacional

**Puede precalcularse.** No requiere recalcular sobre todo el historial en cada predicción: `x̄_i(equipo)` es una agregación sobre, como máximo, `N = 10` partidos por equipo (`O(N)`); `μ_i(competición)`/`σ_i(competición)` son una agregación sobre los partidos de la competición dentro de la misma ventana (`O(M)`, `M` = partidos de esa competición en la ventana — en la práctica, decenas, no miles, dado el volumen típico de partidos de selecciones nacionales por competición y por año). Ambas operaciones son lineales y triviales para el volumen de datos de `data/processed/selecciones-nacionales/`.

**Costo esperado:** una consulta por equipo (últimos `N` partidos) más una consulta por competición (partidos de la ventana) — ambas ya resolubles con los mismos patrones de lectura de CSV ya usados en `CsvPreparationRepository`/`HistoricalMuGolProvider` (`BUILD-016`/`BUILD-017`), sin necesitar una base de datos poblada. Recalcular en cada predicción (sin caché) es aceptable en V1 dado el volumen actual; cachear el agregado por selección/competición y actualizarlo incrementalmente tras cada partido nuevo (`docs/03`, Variable001: "Frecuencia de actualización: Después de cada partido" — mismo principio aplicable aquí) es una optimización futura, no bloqueante.

## 26. Dependencias

| Documento | Impacto de esta especificación |
|---|---|
| `docs/03-Variables.md` | Variable003 podría pasar de "Método de cálculo: Pendiente" a "Método: definido, ver `models/offensive-strength.md` §6.1/§17-26" — actualización editorial que pertenece a `docs/`, fuera de alcance de esta misión de `models/` (`CLAUDE.md`: "la investigación pertenece a `models/`... la implementación pertenece al engine"; una actualización de `docs/03` requeriría su propia misión) |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | Sin cambios — ya asigna Variable003 exclusivamente a `engine/01`, consistente con esta especificación (sección 18 confirma que no se amplía ese consumo) |
| `docs/30-Contrato-Oficial-del-Prediction-Context.md` | Sin cambios — el campo `potencial_ofensivo` de `VariablesBlock` ya está tipado `float \| None` (`ValorVariable.valor`), compatible con este resultado numérico 0-100 sin ningún bloqueo de esquema (a diferencia de Variable009/Localía, `BUILD-017`) |
| `app/preparation/preparation.py` (`VariablePreparation`, `BUILD-017`) | Consumidor directo de esta especificación en una futura misión `BUILD-` — hoy declara Variable003 `disponible=False` explícitamente por ausencia de método autorizado; esta misión provee ese método |
| `models/parameter-calibration.md` | Ya cataloga `vᵢ`/`s` como parámetros de `Offensive Strength` (sección 4 de ese documento) — sin cambios, esta misión no altera su catálogo, solo fija el valor placeholder de `s` como derivado matemáticamente de los pesos (sección 21), no como una calibración real |

## 27. Impacto

Una vez que esta especificación sea revisada y aprobada por el Arquitecto Estadístico Humano (Constitución, Art. 2.9 y Art. 5 — nunca autoaprobada por el Arquitecto Estadístico IA):

- **`VariablePreparation` podría implementar el cálculo real de Variable003** en una futura misión `BUILD-`, siguiendo exactamente la fórmula de la sección 21 y los casos límite de la sección 24 — sin ninguna decisión de diseño pendiente.
- **`Engine01` dejaría de detenerse por `VariableObligatoriaNoDisponible`** únicamente cuando, además, existan filas reales en `estadisticas_partido.csv` y `partidos.csv` (hoy ambos con cero filas, verificado en `BUILD-017`) — esta misión resuelve el bloqueo **metodológico** (qué fórmula usar), no el bloqueo de **datos** (que sigue pendiente, `docs/27-Auditoria-de-Variables-Pendientes.md`). Es importante no sobrestimar el impacto: sin datos reales, el resultado práctico inmediato seguiría siendo `disponible=False`, igual que hoy, pero por la razón correcta ("sin evidencia suficiente") en vez de "sin método".
- **`Engine03` podría producir `λ_local`/`λ_visitante` reales** en la misma condición (Variable003 disponible con dato real) — es la última pieza obligatoria de Capa 1 que le faltaba a Fuerza Ofensiva.

---

# Validaciones — MODEL-009

- **¿La especificación V1 contradice la fórmula ya aprobada en la sección 6.1?** No — la restringe a 3 de 5 métricas (ya contemplado como ejecutable por la propia sección 6.1/§13) y fija las decisiones operacionales que esa sección dejaba abiertas deliberadamente (`N`, valor placeholder de `s`), sin cambiar la estructura `Z`/`Φ`/`P`.
- **¿Se fija algún peso sin justificar?** No — `vᵢ` usa ponderación igualitaria (mismo criterio neutral ya aplicado en todo el proyecto) y `s` se deriva matemáticamente de esos mismos pesos bajo un supuesto ya documentado (independencia aproximada, sección 11) — ninguno es un número elegido arbitrariamente.
- **¿Se usa alguna fuente no autorizada (ranking FIFA, Elo)?** No — sección 20 confirma exclusivamente `data/processed/selecciones-nacionales/estadisticas_partido.csv`/`partidos.csv`/`torneos.csv`/`competiciones.csv`, ya parte de la Base de Conocimiento contratada.
- **¿Se adoptó el ejemplo ilustrativo del brief tal cual?** No — sección 18 documenta por qué contradice `docs/17` y se descarta explícitamente.
- **¿Es reproducible?** Sí — una vez fijados `N`, `vᵢ` y `s` (aunque sean placeholders), la fórmula es una función determinista de los datos de entrada.

---

# Cierre obligatorio — MODEL-009

**1. Definición exacta.**
Variable003 (Potencial Ofensivo) mide la capacidad de una selección para generar y convertir oportunidades de gol, como índice compuesto estandarizado (0-100) de `xG`/disparos totales/disparos al arco de sus últimos `N=10` partidos oficiales, relativo a las demás selecciones de la misma competición en la misma ventana — sección 19.

**2. Fuente de datos.**
`estadisticas_partido.csv` (`xg`, `disparos_totales`, `disparos_al_arco`) y `partidos.csv`/`torneos.csv`/`competiciones.csv` (ventana temporal y agrupación por competición) — sección 20. Sin ranking FIFA, Elo ni ninguna fuente externa no contratada.

**3. Fórmula oficial.**
`Z = (1/3)·z_xG + (1/3)·z_disparos + (1/3)·z_disparos_arco`; `P = 100·Φ(Z/√(1/3))` — sección 21. Pesos iguales (neutral, no arbitrario); `s` derivado matemáticamente de los pesos, no calibrado.

**4. Variables internas.**
`xg`, `disparos_totales`, `disparos_al_arco` — sección 22. "Grandes oportunidades" sin fuente (fuera de alcance); "Conversión" derivable pero diferida a V1.1 (sección 20).

**5. Ventana temporal.**
`N = 10` últimos partidos oficiales, sin ponderación exponencial ni media móvil — placeholder estructural, TODO calibración (sección 22).

**6. Normalización.**
0-100, garantizado por construcción de `Φ` — sin `clip` adicional necesario (sección 23).

**7. Casos límite.**
Menos de `N` partidos → `muestra_reducida=True`; cero partidos (equipo nuevo o debut) → `disponible=False`, pipeline se detiene (obligatoria, Nivel A); competición con `σ=0`/indefinida → esa métrica se excluye, o toda la variable si las tres quedan excluidas — sección 24.

**8. Complejidad computacional.**
Precalculable, `O(N)` por equipo + `O(M)` por competición, ambos lineales y triviales al volumen actual de datos — sección 25.

**9. Dependencias.**
`docs/03` (actualización editorial futura, fuera de esta misión), `docs/17` (sin cambios, ya consistente), `docs/30` (sin cambios, sin bloqueo de esquema), `app/preparation/preparation.py` (consumidor futuro), `models/parameter-calibration.md` (sin cambios al catálogo) — sección 26.

**10. Impacto.**
Desbloquea el camino **metodológico** de `VariablePreparation`/`Engine01`/`Engine03` para Variable003 — no desbloquea, por sí solo, una predicción real, porque `estadisticas_partido.csv`/`partidos.csv` siguen sin filas reales (`BUILD-017`). Requiere, además, aprobación explícita del Arquitecto Estadístico Humano antes de implementarse en código (Constitución, Art. 2.9/Art. 5) — sección 27.

---

# Fuera de alcance de MODEL-009

- No se implementa código Python ni pseudocódigo ejecutable.
- No se modifica el Runtime, `PredictionContext` ni `Engine01` (código) — ver sección 26 para lo que sí queda afectado a nivel documental.
- No se calibra ningún peso con evidencia real — `vᵢ`/`s`/`N` son placeholders estructurales, documentados como tales, nunca presentados como calibrados.
- No se corrige la ausencia de "grandes oportunidades" en el esquema ni se incorpora "Conversión" a la fórmula V1 — ambas quedan explícitamente diferidas.
- No se actualiza `docs/03-Variables.md` (columna "Método de cálculo") — pertenece a una misión de `docs/`, no de `models/`.
- No se aprueba esta especificación como definitiva — queda pendiente de revisión por el Arquitecto Estadístico Humano, conforme a la Constitución.

---

Fin del documento.
