# Variables del Modelo Santiago

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Objetivo

Este documento define todas las variables utilizadas por el Modelo Santiago.

Cada variable deberá ser:

- Objetiva.
- Medible.
- Reproducible.
- Auditable.

Una variable solo podrá incorporarse al modelo si puede obtenerse mediante datos verificables.

Los pesos de cada variable NO pertenecen a este documento.

---

# Estructura de una Variable

Cada variable deberá documentarse utilizando el siguiente formato.

## Nombre

Nombre oficial de la variable.

## Objetivo

¿Por qué existe esta variable?

## Descripción

¿Qué representa?

## Datos necesarios

¿Qué información necesita?

## Método de cálculo

¿Cómo se transforma en un valor numérico?

## Escala

¿Cuál será el rango?

Ejemplo:

0 - 100

o

0.0 - 1.0

## Frecuencia de actualización

Cada cuánto debe actualizarse.

## Observaciones

Notas adicionales.

---

# Variables

---

# Variable 001

## Nombre

Forma Reciente

## Objetivo

Representar el rendimiento competitivo actual del equipo.

## Descripción

Evalúa el comportamiento del equipo en sus partidos oficiales más recientes.

Busca responder:

"¿Cómo está jugando actualmente este equipo?"

No pretende medir la historia del club.

Solo su estado deportivo reciente.

## Datos necesarios

- Últimos partidos oficiales.
- Resultado.
- Rival.
- Competición.
- Fecha.

## Método de cálculo

(Pendiente de definir en Algoritmo.md)

## Escala

Pendiente.

## Frecuencia de actualización

Después de cada partido.

## Observaciones

Esta variable tendrá mayor importancia que el historial.

---

# Variable 002

## Nombre

Rendimiento en el Torneo

## Objetivo

Medir el desempeño dentro del torneo actual.

## Descripción

Analiza únicamente los partidos disputados en la competición que se está prediciendo.

Un equipo puede llegar con mala forma reciente pero mejorar considerablemente durante el torneo.

El modelo deberá reconocer esa mejora.

## Datos necesarios

- Partidos del torneo.
- Victorias.
- Empates.
- Derrotas.
- Goles.
- Rendimiento ofensivo.
- Rendimiento defensivo.

## Método de cálculo

Pendiente.

## Escala

Pendiente.

## Frecuencia

Después de cada jornada.

---

# Variable 003

## Nombre

Potencial Ofensivo

## Objetivo

Medir la capacidad ofensiva real del equipo.

## Descripción

No mide únicamente los goles anotados.

También evalúa la cantidad y calidad de oportunidades creadas.

## Datos necesarios

- xG
- Disparos
- Disparos al arco
- Grandes oportunidades
- Conversión

## Método

Pendiente.

---

# Variable 004

## Nombre

Solidez Defensiva

## Objetivo

Medir la capacidad del equipo para impedir ocasiones de gol.

## Datos necesarios

- xGA
- Goles recibidos
- Remates permitidos
- Porterías en cero

## Método

Pendiente.

---

# Variable 005

## Nombre

Compatibilidad Táctica

## Objetivo

Medir cómo interactúan los estilos de juego de ambos equipos.

## Descripción

No todos los rivales afectan igual.

Algunos estilos favorecen o perjudican a otros.

El modelo deberá considerar esa interacción.

## Datos necesarios

- Formación.
- Estilo de presión.
- Posesión.
- Juego directo.
- Contraataque.

## Método

Pendiente.

## Estado en V1 (MR-004)

**Pendiente de futura investigación.** No existe todavía, en la Base de Conocimiento (`data/processed/selecciones-nacionales/`), ninguna fuente de datos para Formación/Estilo de presión/Juego directo/Contraataque. Se requiere una misión de diseño de esquema de datos antes de poder asignarle un motor — no forma parte del consumo activo de `engine/` en V1. Ver `docs/24-Analisis-Arquitectonico-INC-04-INC-05.md` y `docs/16-Contrato-Oficial-de-Variables.md`.

---

# Variable 006

## Nombre

Disponibilidad de Plantilla

## Objetivo

Medir el impacto de bajas importantes.

## Datos necesarios

- Lesiones.
- Suspensiones.
- Rotaciones.

## Método

Pendiente.

---

# Variable 007

## Nombre

Fatiga

## Objetivo

Evaluar el desgaste físico acumulado.

## Datos necesarios

- Días de descanso.
- Minutos jugados.
- Viajes.

## Método

Pendiente.

---

# Variable 008

## Nombre

Calidad de Plantilla

## Objetivo

Medir el potencial general del equipo.

## Datos necesarios

- Valor de mercado.
- Profundidad.
- Experiencia.

## Método

Pendiente.

## Estado en V1 (MR-004)

**Activa en V1, con alcance reducido.** Consumida por `engine/01-Offensive-Strength.md` y `engine/02-Defensive-Strength.md` únicamente en su componente "profundidad de plantilla" (derivable de `convocatorias.csv` + `jugadores.csv`). El componente "valor de mercado" queda diferido: no existe ese campo en ningún archivo de la Base de Conocimiento actual.

---

# Variable 009

## Nombre

Localía

## Objetivo

Determinar el efecto de jugar como local.

## Observación

En torneos en sede única esta variable podrá tener poco o ningún peso.

## Estado en V1 (MR-004)

**Activa en V1.** Consumidor asignado: `engine/03-Poisson.md` — ajusta el cálculo de goles esperados según la condición de local, visitante o sede neutral. Dato completo y disponible hoy en `partidos.csv`/`estadios.csv`/`torneos.csv`.

---

# Variable 010

## Nombre

Historial Directo

## Objetivo

Registrar enfrentamientos anteriores entre ambos equipos.

## Observación

Esta variable tendrá poca influencia.

Nunca deberá dominar el modelo.

## Estado en V1 (MR-004)

**Activa en V1.** Consumidor asignado: `engine/05-Confidence.md`, como factor contextual menor — consistente con la autolimitación ya declarada arriba. Dato completo y disponible hoy en `partidos.csv`.

---

# Variable 011

## Nombre

Estado Psicológico

## Objetivo

Representar factores emocionales medibles.

## Datos

- Racha de victorias.
- Eliminación reciente.
- Clasificación.
- Presión competitiva.

No se utilizarán interpretaciones subjetivas.

Solo hechos verificables.

## Estado en V1 (MR-004)

**Pendiente de futura investigación.** Dos de sus cuatro datos necesarios (Racha de victorias, Eliminación reciente) son derivables hoy de `partidos.csv`/`torneos.csv`, pero "Clasificación" (tabla de posiciones) no existe en ningún archivo de la Base de Conocimiento. Además, esta variable no tiene todavía un Nivel de importancia asignado en `docs/02-modelo.md` (inconsistencia ya identificada, ver `docs/23`, INC-08). Ambas condiciones deben resolverse antes de asignarle un motor — no forma parte del consumo activo de `engine/` en V1.

---

# Variable 012

## Nombre

Factores Externos

## Objetivo

Medir condiciones ajenas al rendimiento deportivo.

## Datos

- Clima.
- Altitud.
- Viajes.
- Estado del campo.
- Árbitro.

Solo se utilizarán cuando exista evidencia de impacto.