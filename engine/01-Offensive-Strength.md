# Motor de Fuerza Ofensiva

**Archivo:** `engine/01-Offensive-Strength.md`

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Estado del Motor

Arquitectura: ✅ Completa

Matemática: ⏳ Pendiente (Versión 2.0)

Validación Estadística: ⏳ Pendiente

---

# Objetivo

El Motor de Fuerza Ofensiva tiene como objetivo medir la capacidad real de un equipo para generar peligro y convertir oportunidades de gol.

El resultado será un único valor numérico que represente la calidad ofensiva del equipo en el momento actual.

Este valor será utilizado posteriormente por otros motores del Modelo Santiago, especialmente:

- Motor de Poisson
- Motor de Simulación
- Motor de Confianza

---

# Principios

La fuerza ofensiva NO representa únicamente la cantidad de goles anotados.

Un equipo puede atacar muy bien y marcar pocos goles.

Del mismo modo, un equipo puede marcar muchos goles por circunstancias excepcionales.

El motor busca medir la capacidad ofensiva sostenible del equipo.

---

# Entradas

El motor utilizará información proveniente de distintas variables definidas en `docs/03-Variables.md`.

Inicialmente se contemplan las siguientes:

## Variables Primarias

- Expected Goals (xG)
- Disparos Totales
- Disparos a Puerta
- Grandes Oportunidades Creadas
- Conversión de Disparos a Gol

Estas variables representan directamente la producción ofensiva.

---

## Variables Secundarias

- Forma Reciente
- Rendimiento en el Torneo
- Calidad del Rival
- Posesión en Campo Rival
- Ataques Peligrosos

Estas variables ajustan el contexto de la producción ofensiva.

---

## Variables Contextuales

- Lesiones ofensivas
- Suspensiones
- Rotaciones
- Fatiga

Estas variables modifican el resultado final cuando exista evidencia suficiente.

---

# Procesamiento

El cálculo de la Fuerza Ofensiva seguirá las siguientes etapas.

## Paso 1

Obtener todas las variables disponibles.

---

## Paso 2

Validar calidad de los datos.

Si falta información crítica, el motor deberá indicarlo.

Nunca estimará datos inexistentes.

---

## Paso 3

Normalizar todas las variables.

Cada variable deberá convertirse a una escala común antes de combinarse.

La metodología de normalización será definida posteriormente.

---

## Paso 4

Calcular una puntuación individual para cada variable.

Cada variable producirá un valor independiente.

---

## Paso 5

Aplicar ponderaciones.

Las ponderaciones serán documentadas una vez finalice la fase de calibración del modelo.

No se asignarán pesos arbitrarios.

---

## Paso 6

Generar la Fuerza Ofensiva.

La salida será un único valor numérico.

Este valor deberá ser comparable entre cualquier equipo.

---

# Salida

El motor devolverá una estructura con la siguiente información.

- Fuerza Ofensiva
- Nivel de confianza del cálculo
- Variables utilizadas
- Variables descartadas
- Calidad de los datos

---

# Reglas

El motor nunca deberá:

- Basarse únicamente en goles anotados.
- Ignorar la calidad del rival.
- Ignorar lesiones importantes.
- Mezclar datos de competiciones incompatibles.
- Inventar estadísticas faltantes.

---

# Dependencias

Este motor depende de:

- docs/03-Variables.md

Será utilizado por:

- engine/02-Defensive-Strength.md
- engine/03-Poisson.md
- engine/05-Confidence.md

---

# Auditoría

Después de cada torneo deberá evaluarse:

- ¿La Fuerza Ofensiva explicó correctamente los goles esperados?
- ¿Sobrevaloró equipos muy efectivos?
- ¿Infravaloró equipos con alto xG?
- ¿Qué variables aportaron mayor capacidad predictiva?
- ¿Qué variables aportaron ruido?

Toda modificación deberá quedar registrada en `CHANGELOG.md`.

---

# Mejoras Futuras

Las siguientes características podrán incorporarse en versiones posteriores:

- Ajuste automático de ponderaciones.
- Modelos específicos por competición.
- Ajustes según estilo táctico.
- Modelos independientes para selecciones y clubes.
- Integración con modelos de Machine Learning.

---

# Versión 2.0 (Pendiente)

La versión 2.0 deberá incluir:

- Fórmula matemática completa.
- Método de normalización.
- Cálculo de ponderaciones.
- Ejemplo paso a paso.
- Validación estadística.
- Casos límite.
- Estrategia de calibración.

La implementación matemática deberá realizarse únicamente después de validar su capacidad predictiva.

---

Fin del documento.