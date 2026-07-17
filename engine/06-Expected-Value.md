# Motor de Valor Esperado (Expected Value)

**Archivo:** `engine/06-Expected-Value.md`

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Estado del Motor

Arquitectura: ✅ Completa

Matemática: ⏳ Pendiente (Versión 2.0)

Validación Estadística: ⏳ Pendiente

---

# Objetivo

El Motor de Valor Esperado determina si una apuesta ofrece una ventaja matemática para el apostador.

Su función es comparar las probabilidades calculadas por el Modelo Santiago con las probabilidades implícitas en las cuotas ofrecidas por la casa de apuestas.

El objetivo es identificar oportunidades con Valor Esperado Positivo (EV+).

---

# Definición

Una apuesta tiene Valor Esperado Positivo cuando la probabilidad estimada por el modelo es superior a la probabilidad implícita de la cuota.

No todas las apuestas con alta probabilidad son buenas apuestas.

Una apuesta solo será recomendable si presenta una expectativa matemática favorable.

---

# Entradas

El motor recibe información proveniente de:

- engine/03-Poisson.md
- engine/04-Chaos-Index.md
- engine/05-Confidence.md

Además utilizará:

- Cuotas del operador.
- Mercado seleccionado.
- Tipo de apuesta.

---

# Mercados Compatibles

El motor podrá evaluar cualquier mercado soportado por el Modelo Santiago.

Ejemplos:

- Ganador del partido.
- Doble oportunidad.
- Marcador exacto.
- Ambos anotan.
- Más/Menos goles.
- Hándicap.
- Tiros.
- Tarjetas.
- Corners.

Cada mercado deberá disponer de una probabilidad calculada por el modelo.

---

# Flujo del Motor

## Paso 1

Recibir las probabilidades calculadas por el modelo.

---

## Paso 2

Obtener las cuotas disponibles.

---

## Paso 3

Calcular la probabilidad implícita de cada cuota.

---

## Paso 4

Comparar ambas probabilidades.

---

## Paso 5

Calcular el Valor Esperado de cada mercado.

---

## Paso 6

Clasificar las oportunidades según su rentabilidad esperada.

---

## Paso 7

Descartar mercados con valor esperado negativo.

---

## Paso 8

Generar una lista priorizada de apuestas recomendadas.

---

# Salida

El motor devolverá:

- Valor Esperado (EV)
- Probabilidad del Modelo
- Probabilidad Implícita
- Diferencia porcentual
- Nivel de confianza
- Índice de Caos asociado
- Recomendación

---

# Clasificación

EV Muy Alto

Oportunidad excepcional.

---

EV Alto

Muy recomendable.

---

EV Moderado

Apuesta aceptable.

---

EV Bajo

Beneficio esperado limitado.

---

EV Negativo

No recomendable apostar.

---

# Restricciones

El motor nunca deberá:

- Recomendar apuestas con EV negativo.
- Ignorar el Índice de Caos.
- Ignorar el Nivel de Confianza.
- Basarse únicamente en cuotas altas.
- Favorecer apuestas por reputación del equipo.

---

# Dependencias

Este motor será utilizado por:

- engine/07-Bankroll-Engine.md *(futuro, no implementado todavía)*
- engine/08-Simulation.md *(futuro, no implementado todavía)*

---

# Auditoría

Después de cada torneo deberá responderse:

- ¿Las apuestas EV+ fueron realmente rentables?
- ¿Qué mercados ofrecieron mayor retorno?
- ¿Existieron falsos positivos?
- ¿Qué mercados deben recalibrarse?
- ¿Cómo evolucionó el ROI?

Toda modificación deberá registrarse en CHANGELOG.md.

---

# Mejoras Futuras

Versiones posteriores podrán incorporar:

- EV dinámico durante el partido.
- Comparación entre múltiples casas de apuestas.
- Detección automática de Value Bets.
- Optimización de portafolios.
- Kelly Criterion adaptativo.

---

# Versión 2.0 (Pendiente)

La versión 2.0 deberá definir:

- Fórmula matemática del Valor Esperado.
- Cálculo de probabilidad implícita.
- Cálculo del EV.
- Umbrales mínimos para recomendar una apuesta.
- Casos de estudio.
- Ejemplos completos.
- Validación estadística.

---

Fin del documento.