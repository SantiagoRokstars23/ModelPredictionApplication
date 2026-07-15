# Algoritmo del Modelo Santiago

**Versión:** 1.0.0

**Estado:** En desarrollo

---

# Objetivo

Este documento define el flujo de ejecución del Modelo Santiago.

El algoritmo establece el orden en el que se procesan las variables para producir una predicción.

No define las fórmulas matemáticas.

Las implementaciones matemáticas se documentan en la carpeta `models/`.

---

# Principios

El algoritmo deberá ser:

- Determinístico.
- Reproducible.
- Auditable.
- Modular.
- Independiente del torneo.

Cada paso deberá producir un resultado verificable.

Ningún paso podrá omitirse.

---

# Flujo General

Entrada

↓

Validación

↓

Normalización

↓

Análisis

↓

Modelado

↓

Predicción

↓

Evaluación

↓

Registro

---

# Paso 1
## Recolección de Datos

Objetivo

Obtener toda la información necesaria para el partido.

Entradas

- Equipos
- Competición
- Fecha
- Estadísticas
- Lesiones
- Suspensiones
- Cuotas
- Jugadores disponibles

Salida

Conjunto de datos del partido.

---

# Paso 2
## Validación

Objetivo

Verificar que los datos sean completos.

Validaciones

- Datos duplicados
- Datos faltantes
- Estadísticas inconsistentes
- Lesiones confirmadas

Si la información es insuficiente:

El algoritmo deberá detenerse.

Nunca inventará información.

---

# Paso 3
## Normalización

Objetivo

Convertir todas las variables a una escala común.

Ejemplo

No todas las variables estarán originalmente entre los mismos valores.

El algoritmo deberá prepararlas para ser comparables.

La metodología exacta se documentará posteriormente.


Ver:
models/offensive-strength.md

Ver:
models/poisson.md

Ver:
models/confidence.md

---

# Paso 4
## Cálculo de Variables

Objetivo

Calcular todas las variables definidas en Variables.md

Ejemplos

Forma reciente

Potencial ofensivo

Solidez defensiva

Fatiga

Compatibilidad táctica

Disponibilidad

Cada variable generará un valor numérico.

---

# Paso 5
## Cálculo de Fuerzas

Objetivo

Determinar la fuerza real de ambos equipos.

El algoritmo calculará al menos

- Fuerza ofensiva
- Fuerza defensiva
- Fuerza general

Estas fuerzas servirán como entrada para los modelos probabilísticos.

---

# Paso 6
## Modelado Matemático

Objetivo

Aplicar uno o varios modelos estadísticos.

Ejemplos

- Poisson
- Elo
- Modelos Bayesianos
- Machine Learning (futuro)

El algoritmo no limita el modelo utilizado.

Siempre deberá quedar registrado cuál fue utilizado.

---

# Paso 7
## Probabilidades

Objetivo

Calcular

- Victoria Local
- Empate
- Victoria Visitante

La suma deberá ser exactamente:

100%

---

# Paso 8
## Simulación de Marcadores

Objetivo

Generar los marcadores más probables.

Resultado esperado

Top 4 marcadores.

Cada marcador incluirá

- Probabilidad
- Justificación
- Nivel de confianza

---

# Paso 9
## Índice de Confianza

Objetivo

Calcular qué tan confiable es la predicción.

La confianza dependerá de

- Calidad de los datos
- Consistencia de las variables
- Diferencia entre equipos
- Consenso de los modelos

No dependerá de intuición.

---

# Paso 10
## Índice de Caos

Objetivo

Medir la incertidumbre del partido.

Factores

- Equipos muy parejos
- Lesiones
- Rotaciones
- Eliminación directa
- Alta variabilidad estadística

Resultado

Valor entre 0 y 100.

---

# Paso 11
## Valor Esperado

Objetivo

Comparar

Probabilidad calculada

vs

Probabilidad implícita en las cuotas.

El sistema deberá identificar mercados con valor esperado positivo.

---

# Paso 12
## Recomendación

Objetivo

Generar una recomendación final.

La recomendación incluirá

- Resultado principal
- Resultados secundarios
- Confianza
- Índice de caos
- Valor esperado
- Recomendación de bankroll

---

# Paso 13
## Registro

Objetivo

Guardar toda la información del análisis.

Se almacenará

- Variables
- Probabilidades
- Marcadores
- Cuotas
- Resultado real

Esta información alimentará el aprendizaje futuro.

---

# Paso 14
## Auditoría

Objetivo

Comparar

Predicción

vs

Resultado real.

El algoritmo identificará

- Variables sobrevaloradas
- Variables subvaloradas
- Errores del modelo

Toda modificación futura deberá basarse en esta auditoría.

---

# Reglas

El algoritmo nunca podrá

- Inventar datos.
- Saltar pasos.
- Cambiar pesos automáticamente.
- Justificar resultados sin evidencia.

Todo cálculo deberá poder reproducirse.

---

Fin del documento.