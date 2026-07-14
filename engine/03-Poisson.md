# Motor de Distribución de Poisson

**Archivo:** `engine/03-Poisson.md`

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Estado del Motor

Arquitectura: ✅ Completa

Matemática: ⏳ Pendiente (Versión 2.0)

Validación Estadística: ⏳ Pendiente

---

# Objetivo

El Motor de Distribución de Poisson transforma la fuerza ofensiva y defensiva de ambos equipos en una distribución probabilística de goles esperados.

A partir de esta distribución, el modelo podrá estimar:

- Probabilidad de victoria.
- Probabilidad de empate.
- Probabilidad de derrota.
- Probabilidad de cada marcador.
- Top de marcadores más probables.

Este motor constituye el núcleo estadístico del Modelo Santiago.

---

# ¿Por qué Poisson?

En fútbol, la cantidad de goles suele ser baja y discreta.

La Distribución de Poisson ha demostrado ser una de las herramientas más utilizadas para modelar este tipo de eventos.

Sin embargo, el Modelo Santiago no dependerá exclusivamente de Poisson.

Este motor podrá ser reemplazado o complementado en futuras versiones.

---

# Entradas

El motor recibe información proveniente de otros motores.

## Equipo Local

- Fuerza Ofensiva
- Fuerza Defensiva

## Equipo Visitante

- Fuerza Ofensiva
- Fuerza Defensiva

---

# Dependencias

Este motor depende de:

- engine/01-Offensive-Strength.md
- engine/02-Defensive-Strength.md

---

# Flujo del Motor

## Paso 1

Recibir la fuerza ofensiva de ambos equipos.

---

## Paso 2

Recibir la fuerza defensiva de ambos equipos.

---

## Paso 3

Calcular los goles esperados para cada equipo.

La metodología matemática será definida en la Versión 2.0.

---

## Paso 4

Generar una distribución de probabilidad de goles para ambos equipos.

---

## Paso 5

Construir la matriz de marcadores posibles.

Ejemplo:

0-0

0-1

1-0

2-1

3-2

...

---

## Paso 6

Calcular la probabilidad individual de cada marcador.

---

## Paso 7

Ordenar los marcadores por probabilidad.

---

## Paso 8

Seleccionar el Top de resultados más probables.

---

# Salidas

El motor devolverá:

- Goles esperados del Equipo Local.
- Goles esperados del Equipo Visitante.
- Distribución de goles.
- Probabilidad de cada marcador.
- Top de marcadores.
- Probabilidad de victoria.
- Probabilidad de empate.
- Probabilidad de derrota.

---

# Restricciones

El motor nunca deberá:

- Inventar valores de entrada.
- Modificar probabilidades manualmente.
- Ajustar resultados para coincidir con cuotas.
- Ignorar la incertidumbre estadística.

---

# Integración

Las salidas de este motor alimentan directamente:

- engine/04-Confidence.md
- engine/05-Chaos-Index.md
- engine/06-Expected-Value.md

---

# Limitaciones

La Distribución de Poisson presenta limitaciones conocidas.

Entre ellas:

- Independencia entre goles.
- Dificultad para modelar partidos muy abiertos.
- Menor precisión en marcadores con muchos goles.
- No considera directamente aspectos tácticos.

Estas limitaciones podrán mitigarse mediante motores complementarios.

---

# Auditoría

Después de cada torneo deberán analizarse:

- Precisión de los goles esperados.
- Precisión de los marcadores.
- Precisión del Top 4.
- Distribución real de goles.
- Desviación respecto a los resultados observados.

Toda mejora deberá documentarse en CHANGELOG.md.

---

# Mejoras Futuras

Versiones futuras podrán incorporar:

- Dixon-Coles.
- Bivariate Poisson.
- Bayesian Poisson.
- Machine Learning.
- Simulaciones Monte Carlo.

La incorporación de nuevos modelos deberá demostrar una mejora estadísticamente significativa respecto a la versión anterior.

---

# Versión 2.0 (Pendiente)

La versión 2.0 de este documento deberá incluir:

- Fórmula matemática completa.
- Cálculo de λ (lambda).
- Construcción de la matriz de probabilidades.
- Ejemplo paso a paso.
- Validación matemática.
- Casos límite.
- Estrategia de calibración.

La implementación matemática no deberá realizarse hasta validar que el modelo propuesto mejora la capacidad predictiva del Modelo Santiago.

---

Fin del documento.