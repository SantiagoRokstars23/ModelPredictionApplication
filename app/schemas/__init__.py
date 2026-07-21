"""Paquete schemas -- contratos Pydantic de entrada/salida de la API.

Responsabilidad (docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 4
y 6): declarar `PredictionRequest` y `PredictionReport` (docs/25, docs/29) como
esquemas validados por Pydantic. Nunca conoce SQLAlchemy -- se mantiene
deliberadamente desacoplado de app/models, igual que la Base de Conocimiento
se mantiene desacoplada del Engine (docs/15).

Bootstrap oficial (BUILD-001): paquete vacio.
"""
