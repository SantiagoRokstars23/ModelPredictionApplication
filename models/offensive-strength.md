# Offensive Strength — Fuerza Ofensiva

**Archivo:** `models/offensive-strength.md`

**Misión:** MODEL-001 — Modelo Matemático de Fuerza Ofensiva (primera misión con prefijo "MODEL-")

**Versión:** 2.0.0-investigación

**Estado:** Investigación — estructura de la fórmula definida; coeficientes (pesos) **pendientes de calibración estadística** con datos reales, conforme a `CLAUDE.md` ("Nunca alterar pesos sin evidencia estadística")

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

Fin del documento.
