"""Configuracion minima leida desde variables de entorno.

Bootstrap oficial (BUILD-001): unicamente prepara la lectura de variables de
entorno, sin conectar la base de datos ni ejecutar ninguna migracion
(docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 3; brief de
BUILD-001, seccion 6).

Nota de diseno: no se usa un framework de configuracion dedicado (ej.
"pydantic-settings") porque esa libreria no forma parte de la lista de
dependencias aprobada por esta mision (BUILD-001, seccion 4) -- Pydantic v2
ya no incluye `BaseSettings` en el paquete base. Se usa `os.environ` de la
biblioteca estandar en su lugar, sin agregar ninguna dependencia nueva.
"""

import os

DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
MODEL_VERSION: str = os.environ.get("MODEL_VERSION", "0.1.0")
