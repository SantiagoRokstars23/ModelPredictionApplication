# Motor de Fuerza Defensiva

**Archivo:** `engine/02-Defensive-Strength.md`

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Estado del Motor

Arquitectura: ✅ Completa

Matemática: ⏳ Pendiente (Versión 2.0)

Validación Estadística: ⏳ Pendiente

---

# Objetivo

El Motor de Fuerza Defensiva tiene como objetivo medir la capacidad real de un equipo para impedir que el rival genere y convierta oportunidades de gol.

El resultado será un único valor numérico que represente la calidad defensiva actual del equipo.

Este valor será utilizado por el Motor de Distribución de Poisson y otros motores del Modelo Santiago.

---

# Principios

Una buena defensa no se mide únicamente por los goles recibidos.

Un equipo puede recibir pocos goles debido a la falta de eficacia del rival.

El objetivo del motor es medir la capacidad defensiva sostenible del equipo.

---

# Entradas

El motor utilizará información proveniente de las variables oficiales definidas en `docs/03-Variables.md`.

## Variables Primarias

- Expected Goals Against (xGA)
- Disparos Recibidos
- Disparos a Puerta Recibidos
- Grandes Oportunidades Concedidas
- Goles Recibidos

Estas variables representan directamente el rendimiento defensivo.

---

## Variables Secundarias

- Forma Reciente
- Rendimiento en el Torneo
- Calidad Ofensiva de los Rivales
- Recuperaciones
- Intercepciones
- Presión Defensiva

Estas variables aportan contexto al rendimiento defensivo.

---

## Variables Contextuales

- Lesiones defensivas
- Suspensiones
- Rotaciones
- Fatiga
- Descanso
- Calidad de Plantilla propia (MR-004, alcance reducido: solo "profundidad de plantilla" — el componente "valor de mercado" queda diferido, ver `docs/03-Variables.md`)

Estas variables podrán modificar el resultado final cuando exista evidencia suficiente.

---

# Procesamiento

El cálculo de la Fuerza Defensiva seguirá las siguientes etapas.

## Paso 1

Obtener todas las variables disponibles.

---

## Paso 2

Validar la calidad de los datos.

Si falta información crítica, el motor deberá indicarlo.

Nunca estimará datos inexistentes.

---

## Paso 3

Normalizar todas las variables.

Cada variable deberá convertirse a una escala común antes de combinarse.

La metodología exacta será documentada en la Versión 2.0.

---

## Paso 4

Calcular una puntuación individual para cada variable.

Cada variable producirá un valor independiente.

---

## Paso 5

Aplicar ponderaciones.

Las ponderaciones serán definidas tras el proceso de calibración del modelo.

Nunca deberán asignarse de forma arbitraria.

---

## Paso 6

Generar la Fuerza Defensiva.

La salida será un único valor numérico comparable entre todos los equipos.

---

# Salida

El motor devolverá:

- Fuerza Defensiva
- Nivel de confianza del cálculo
- Variables utilizadas
- Variables descartadas
- Calidad de los datos

---

# Reglas

El motor nunca deberá:

- Basarse únicamente en goles recibidos.
- Ignorar la calidad ofensiva del rival.
- Ignorar lesiones importantes.
- Mezclar datos de competiciones incompatibles.
- Inventar estadísticas inexistentes.

---

# Dependencias

Este motor depende de:

- docs/03-Variables.md

Será utilizado por:

- engine/03-Poisson.md
- engine/05-Confidence.md

---

# Auditoría

Después de cada torneo deberá evaluarse:

- ¿La Fuerza Defensiva explicó correctamente los goles recibidos?
- ¿Sobrevaloró equipos que enfrentaron rivales débiles?
- ¿Infravaloró equipos con buen rendimiento defensivo frente a rivales fuertes?
- ¿Qué variables aportaron mayor capacidad predictiva?
- ¿Qué variables introdujeron ruido?

Toda modificación deberá registrarse en CHANGELOG.md.

---

# Mejoras Futuras

Las siguientes características podrán incorporarse en versiones posteriores:

- Ajustes automáticos de ponderaciones.
- Modelos específicos por competición.
- Ajustes según estilo táctico.
- Integración con Machine Learning.
- Corrección por calidad ofensiva del rival.

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