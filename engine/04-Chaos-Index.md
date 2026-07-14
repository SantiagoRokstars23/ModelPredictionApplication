# Motor de Índice de Caos

**Archivo:** `engine/04-Chaos-Index.md`

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Estado del Motor

Arquitectura: ✅ Completa

Matemática: ⏳ Pendiente (Versión 2.0)

Validación Estadística: ⏳ Pendiente

---

# Objetivo

El Motor de Índice de Caos mide el nivel de incertidumbre inherente a un partido.

Su propósito es identificar aquellos encuentros donde las probabilidades tradicionales pueden ser menos fiables debido a factores deportivos, tácticos o contextuales.

Este índice complementa las probabilidades calculadas por el Motor de Poisson y será utilizado posteriormente por el Motor de Confianza y el Motor de Bankroll.

---

# Definición

El Índice de Caos representa la dificultad de predecir correctamente el desarrollo de un partido.

No mide quién es mejor.

Mide qué tan impredecible es el encuentro.

Dos partidos pueden tener exactamente la misma probabilidad de victoria y, sin embargo, presentar niveles de caos completamente diferentes.

---

# Entradas

El motor podrá utilizar información proveniente de:

- engine/01-Offensive-Strength.md
- engine/02-Defensive-Strength.md
- engine/03-Poisson.md

Además podrá considerar variables contextuales definidas en:

- docs/02-Variables.md

---

# Factores de Caos

Inicialmente el modelo evaluará los siguientes factores.

## Deportivos

- Equipos de nivel similar.
- Alta variabilidad en resultados recientes.
- Baja diferencia de fuerza ofensiva.
- Baja diferencia de fuerza defensiva.

---

## Contextuales

- Eliminación directa.
- Prórroga posible.
- Clima adverso.
- Viajes largos.
- Descanso insuficiente.
- Rotaciones.

---

## Disponibilidad

- Lesiones importantes.
- Suspensiones.
- Jugadores en duda.

---

## Información

- Pocos partidos disponibles.
- Datos incompletos.
- Cambios recientes de entrenador.
- Cambios tácticos relevantes.

---

# Flujo del Motor

## Paso 1

Recibir las probabilidades del Motor de Poisson.

---

## Paso 2

Analizar la diferencia competitiva entre ambos equipos.

---

## Paso 3

Evaluar factores deportivos.

---

## Paso 4

Evaluar factores contextuales.

---

## Paso 5

Evaluar calidad y cantidad de información disponible.

---

## Paso 6

Calcular un Índice de Caos preliminar.

---

## Paso 7

Aplicar ajustes finales.

---

## Paso 8

Generar el Índice Final de Caos.

---

# Salida

El motor devolverá:

- Índice de Caos (0 a 100)
- Nivel de Caos
- Factores que aumentan el caos
- Factores que reducen el caos
- Justificación del resultado

---

# Escala

0 - 20

Caos Muy Bajo

Partido altamente predecible.

---

21 - 40

Caos Bajo

Predicción estable.

---

41 - 60

Caos Moderado

Existe incertidumbre relevante.

---

61 - 80

Caos Alto

El partido presenta alta variabilidad.

---

81 - 100

Caos Muy Alto

No recomendable confiar únicamente en probabilidades tradicionales.

---

# Restricciones

El motor nunca deberá:

- Basarse únicamente en la diferencia entre probabilidades.
- Ignorar factores contextuales relevantes.
- Modificar el índice manualmente.
- Confundir caos con calidad de los equipos.

---

# Dependencias

Este motor será utilizado por:

- engine/05-Confidence.md
- engine/06-Expected-Value.md
- engine/07-Bankroll-Engine.md

---

# Auditoría

Después de cada torneo deberá responderse:

- ¿Los partidos con mayor Índice de Caos fueron realmente más impredecibles?
- ¿Qué factores aportaron mayor incertidumbre?
- ¿Qué variables sobreestimaron el caos?
- ¿Qué variables fueron ignoradas y deberían incorporarse?

Toda mejora deberá registrarse en CHANGELOG.md.

---

# Mejoras Futuras

Versiones posteriores podrán incorporar:

- Índice dinámico durante el torneo.
- Factores psicológicos.
- Estabilidad táctica.
- Historial de sorpresas por selección o club.
- Modelos de incertidumbre bayesianos.

---

# Versión 2.0 (Pendiente)

La versión 2.0 deberá definir:

- Fórmula matemática.
- Variables participantes.
- Ponderaciones.
- Calibración.
- Validación estadística.
- Casos de estudio.
- Ejemplos completos.

---

Fin del documento.