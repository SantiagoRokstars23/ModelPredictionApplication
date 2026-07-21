"""Paquete api -- capa de transporte HTTP (FastAPI).

Responsabilidad (docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 4):
recibir la solicitud, validarla contra app/schemas, invocar app/runtime, y
devolver la respuesta. Nunca calcula una probabilidad ni conoce SQLAlchemy o
PostgreSQL directamente.

Bootstrap oficial (BUILD-001): sin routers ni endpoints todavia. Ver app/main.py.
"""
