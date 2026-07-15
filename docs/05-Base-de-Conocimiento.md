# Arquitectura de Datos

**Archivo:** `docs/04-Arquitectura-de-Datos.md`

**Versión:** 1.0.0

**Estado:** Activo

---

# Objetivo

Este documento define la Base de Conocimiento del Modelo Santiago.

Su propósito es establecer cómo el modelo adquiere, valida, organiza, almacena, consulta y preserva toda la información utilizada para generar predicciones.

La Base de Conocimiento constituye la única fuente oficial de datos del Modelo Santiago.

Ningún motor del sistema podrá consumir información que no haya sido previamente validada y almacenada conforme a las reglas definidas en este documento.

---

# Filosofía

La Base de Conocimiento representa la memoria permanente del Modelo Santiago.

Los motores del sistema nunca accederán directamente a fuentes externas.

Toda información deberá incorporarse primero a la Base de Conocimiento antes de ser utilizada.

---

# Flujo de los Datos

Todo dato deberá seguir el siguiente flujo.

```
Fuentes Externas
        │
        ▼
Recolección
        │
        ▼
data/raw
        │
        ▼
Validación
        │
        ▼
Normalización
        │
        ▼
data/processed
        │
        ▼
Engine
        │
        ▼
Predicción
        │
        ▼
data/predictions
        │
Partido Finaliza
        │
        ▼
data/results
        │
        ▼
data/audit
        │
        ▼
Aprendizaje del Modelo
```

Ningún paso podrá omitirse.

---

# Fuentes de Información

El Modelo Santiago podrá utilizar información proveniente de:

- APIs deportivas.
- Sitios oficiales de competiciones.
- Estadísticas públicas.
- Bases de datos deportivas.
- Archivos CSV.
- Entrada manual validada.

Toda fuente deberá ser identificable y verificable.

---

# Recolección

La información deberá obtenerse antes de iniciar cualquier predicción.

La recolección deberá incluir únicamente información necesaria para el modelo.

No se almacenarán datos irrelevantes.

---

# Validación

Antes de almacenar cualquier dato deberán verificarse como mínimo:

- Integridad.
- Formato.
- Fecha.
- Duplicados.
- Valores nulos.
- Consistencia.

Si un dato no supera la validación deberá descartarse o marcarse para revisión.

Nunca deberá corregirse automáticamente sin evidencia.

---

# Normalización

Todos los datos deberán almacenarse bajo un formato uniforme.

Ejemplos:

Fechas

```
YYYY-MM-DD
```

Porcentajes

```
0 - 100
```

Probabilidades

```
0.00 - 1.00
```

Nombres de equipos

Siempre deberán utilizar el mismo identificador.

Nunca se permitirán múltiples nombres para un mismo equipo.

---

# Organización de la Base de Conocimiento

Toda la información del Modelo Santiago deberá almacenarse dentro del directorio:

```
data/
```

La estructura oficial es:

```
data/
│
├── raw/
├── processed/
├── predictions/
├── results/
├── audit/
└── archive/
```

Cada directorio tiene una única responsabilidad.

Ningún archivo deberá almacenarse fuera de esta estructura sin una justificación documentada.

---

# Responsabilidad de cada Directorio

## raw/

Contiene la información obtenida desde fuentes externas.

Los archivos almacenados aquí nunca deberán modificarse.

Representan la fuente original.

---

## processed/

Contiene información validada y normalizada.

Todos los motores del Modelo Santiago deberán consultar únicamente esta carpeta.

---

## predictions/

Almacena todas las predicciones generadas por el modelo.

Cada predicción deberá conservarse para futuras auditorías.

---

## results/

Contiene los resultados oficiales de los partidos.

Sirve como referencia para validar las predicciones.

---

## audit/

Almacena métricas históricas del rendimiento del modelo.

Ejemplos:

- ROI
- Precisión Top 1
- Precisión Top 4
- Error de calibración

---

## archive/

Contiene información histórica que ya no participa en el procesamiento diario.

Nunca deberá eliminarse.

---

# Principio Fundamental

La Base de Conocimiento constituye la única fuente oficial de información del Modelo Santiago.

Los motores nunca accederán directamente a Internet.

Toda actualización deberá realizarse mediante el proceso:

Recolección → Validación → Normalización → Almacenamiento.

---

# Versionado

Los datos nunca deberán sobrescribirse.

Toda modificación importante deberá quedar registrada.

El historial constituye parte del proceso de aprendizaje del modelo.

---

# Calidad de Datos

Cada conjunto de datos deberá indicar:

- Fecha de actualización.
- Fuente.
- Nivel de confianza.
- Cobertura.
- Observaciones.

---

# Principio de Justificación de Datos

Todo campo definido en cualquier entidad de la Base de Conocimiento deberá poder justificarse mediante al menos una de las siguientes razones:

- Es insumo directo de una variable definida en `docs/03-Variables.md`.
- Es insumo directo de un paso del algoritmo definido en `docs/04-Algoritmo.md`.
- Es insumo directo de un motor definido en `engine/`.
- Es necesario para garantizar integridad referencial, trazabilidad o auditabilidad del dato (identificadores, fechas de vigencia, fuente).

Ningún campo podrá incorporarse a una entidad si no puede justificarse mediante al menos una de estas razones.

Este principio extiende la regla general "Nunca modificar una variable sin justificar el cambio" (`CLAUDE.md`) al diseño de la Base de Conocimiento: toda incorporación, eliminación o modificación de un campo deberá quedar justificada y registrada en `CHANGELOG.md`.

---

# Reglas

El Modelo Santiago nunca deberá:

- Inventar datos faltantes.
- Modificar estadísticas oficiales.
- Eliminar historial.
- Utilizar datos sin validar.
- Mezclar competiciones incompatibles.
- Incorporar campos a una entidad sin justificación documentada (ver Principio de Justificación de Datos).

---

# Dependencias

Este documento también aplica a:

- agents/
- prompts/
- models/

---

# Auditoría

Periódicamente deberá verificarse:

- Integridad de los archivos.
- Calidad de las fuentes.
- Datos duplicados.
- Valores inconsistentes.
- Cobertura de estadísticas.

Toda incidencia deberá documentarse.

---

# Evolución

La Base de Conocimiento podrá evolucionar sin afectar el funcionamiento del Engine.

En futuras versiones podrá migrarse desde archivos CSV hacia:

- SQLite
- PostgreSQL
- APIs internas
- Bases de datos distribuidas

Siempre respetando la misma arquitectura lógica.

---

# Versión 2.0

La siguiente versión definirá:

- Esquema completo de cada entidad.
- Relaciones entre datos.
- Identificadores únicos.
- Reglas de sincronización.
- Actualización automática.
- Versionado interno.
- Trazabilidad completa.
- Caché de información.
---

Fin del documento.