# Motor de Confianza

**Archivo:** `engine/05-Confidence.md`

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Estado del Motor

Arquitectura: ✅ Completa

Matemática: ⏳ Pendiente (Versión 2.0)

Validación Estadística: ⏳ Pendiente

---

# Objetivo

El Motor de Confianza estima el nivel de fiabilidad de la predicción generada por el Modelo Santiago.

Su propósito no es determinar quién ganará un partido, sino medir qué tan sólida es la predicción realizada.

Este índice será utilizado para la toma de decisiones y la gestión del bankroll.

---

# Definición

La confianza representa el grado de certeza que tiene el modelo sobre sus propias predicciones.

Un partido puede tener un favorito claro y, aun así, presentar una confianza baja debido a la incertidumbre de los datos o al contexto competitivo.

---

# Entradas

El motor recibe información proveniente de:

- engine/01-Offensive-Strength.md
- engine/02-Defensive-Strength.md
- engine/03-Poisson.md

Además podrá considerar:

- Calidad de los datos disponibles.
- Lesiones confirmadas.
- Suspensiones.
- Rotaciones esperadas.
- Estado físico de los equipos.

---

# Flujo del Motor

## Paso 1

Recibir las probabilidades calculadas por el Motor de Poisson.

---

## Paso 2

Analizar la diferencia de nivel entre ambos equipos.

---

## Paso 3

Evaluar la estabilidad de las variables utilizadas.

---

## Paso 4

Detectar factores de incertidumbre.

Ejemplos:

- Muchas lesiones.
- Pocos partidos analizados.
- Cambios recientes de entrenador.
- Rotaciones masivas.
- Competición poco predecible.

---

## Paso 5

Calcular un índice preliminar de confianza.

---

## Paso 6

Aplicar ajustes según la calidad de la información disponible.

---

## Paso 7

Generar el Índice Final de Confianza.

---

# Salida

El motor devolverá:

- Índice de Confianza (0 a 100)
- Nivel de confianza
- Factores positivos
- Factores negativos
- Justificación del resultado

---

# Escala

90 - 100

Confianza Muy Alta

---

80 - 89

Confianza Alta

---

70 - 79

Confianza Buena

---

60 - 69

Confianza Moderada

---

50 - 59

Confianza Baja

---

Menor a 50

No recomendable apostar.

---

# Restricciones

El motor nunca deberá:

- Basarse únicamente en la diferencia de probabilidades.
- Ignorar lesiones importantes.
- Ignorar la calidad de los datos.
- Modificar manualmente el índice.

---

# Dependencias

Este motor será utilizado por:

- engine/04-Chaos-Index.md
- engine/06-Expected-Value.md
- engine/07-Bankroll-Engine.md *(futuro, no implementado todavía)*

---

# Auditoría

Después de cada torneo deberá responderse:

- ¿Los partidos con mayor confianza acertaron con mayor frecuencia?
- ¿El índice estuvo bien calibrado?
- ¿Se sobreestimó la confianza?
- ¿Se subestimó la incertidumbre?

Toda mejora deberá registrarse en CHANGELOG.md.

---

# Mejoras Futuras

Versiones posteriores podrán incorporar:

- Calibración automática.
- Ensemble de modelos.
- Intervalos de confianza.
- Aprendizaje automático.

---

# Versión 2.0 (Pendiente)

La versión 2.0 deberá definir:

- Fórmula matemática.
- Variables participantes.
- Ponderaciones.
- Calibración.
- Validación estadística.
- Ejemplos completos.

---

Fin del documento.