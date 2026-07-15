# Processed Data

**Directorio:** `data/processed/`

**Versión:** 1.0.0

**Estado:** Activo

---

# Objetivo

Almacenar información validada, limpia y normalizada.

Este directorio constituye la única fuente autorizada para alimentar el Engine del Modelo Santiago.

---

# Responsabilidad

Transformar datos provenientes de `raw/` en información lista para el análisis.

---

# Contenido

Ejemplos:

- equipos.csv
- partidos.csv
- estadisticas.csv
- jugadores.csv

---

# Reglas

Toda información deberá estar validada.

No se permiten duplicados.

Todos los formatos deberán ser consistentes.

Nunca almacenar información incompleta.

---

# Consumidores

- Engine
- Predictor
- Statistician

---

# Versión 2.0

Validación automática mediante reglas de negocio.