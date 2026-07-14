# Modelo Poisson

**Archivo:** `models/poisson.md`

**Versión:** 1.0.0

**Estado:** Investigación

---

# Objetivo

Documentar la Distribución de Poisson y evaluar su utilidad para la predicción de marcadores en partidos de fútbol.

---

# Descripción

La Distribución de Poisson es uno de los modelos estadísticos más utilizados para estimar la cantidad de goles que un equipo puede anotar durante un partido.

Asume que los goles ocurren como eventos independientes dentro de un intervalo de tiempo.

---

# Problema que Resuelve

Permite transformar la fuerza ofensiva y defensiva de dos equipos en probabilidades de marcadores exactos.

---

# Ventajas

- Modelo ampliamente validado.
- Fácil de implementar.
- Buen desempeño en ligas profesionales.
- Base de numerosos modelos modernos.

---

# Limitaciones

- Asume independencia entre goles.
- No modela cambios tácticos durante el partido.
- Puede perder precisión en marcadores altos.

---

# Aplicación dentro del Modelo Santiago

Servirá como motor base para generar los cuatro marcadores más probables.

La implementación matemática se realizará en `engine/03-Poisson.md`.

---

# Referencias

Pendiente de investigación.

---

# Versión 2.0

Documentar:

- Fórmula completa.
- Parámetro λ.
- Ajustes.
- Comparación con Dixon-Coles.