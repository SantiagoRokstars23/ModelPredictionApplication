"""Paquete api -- capa de transporte HTTP (FastAPI).

Responsabilidad (docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 4):
recibir la solicitud, validarla contra app/schemas, invocar app/runtime, y
devolver la respuesta. Nunca calcula una probabilidad ni conoce SQLAlchemy o
PostgreSQL directamente.

Bootstrap oficial (BUILD-001): sin routers ni endpoints todavia. Ver app/main.py.

BUILD-026: primer router real (`predict_controller.py`), `POST /predict` --
unico endpoint del sistema, reutiliza exclusivamente `PredictMatchUseCase`
(`app/application`, BUILD-025). Se exporta `router` para que una futura
mision (con permiso para modificar `app/main.py`, fuera del alcance de
BUILD-026) pueda montarlo con `app.include_router(router)` sin conocer la
ruta interna del modulo.
"""

from app.api.predict_controller import router

__all__ = ["router"]
