"""Punto de entrada de la aplicacion FastAPI.

Ver docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 3 (app/api)
y seccion 8 del brief de BUILD-001 ("Crear unicamente: app/main.py, con una
aplicacion vacia. No crear endpoints.").

Esta instancia se crea deliberadamente vacia -- sin routers, sin endpoints,
sin ninguna dependencia de app/runtime, app/engine ni app/persistence. Los
endpoints reales se agregaran en una mision futura de implementacion (ver
docs/35, seccion 8: "Estrategia de crecimiento").
"""

from fastapi import FastAPI

app = FastAPI(
    title="Modelo Santiago",
    version="0.1.0",
)
