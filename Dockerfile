# Modelo Santiago -- imagen base de la aplicacion Python (bootstrap oficial, BUILD-001)
# Sin logica de negocio, sin endpoints funcionales, sin conexion real a base de datos.
# Referencia: docs/34-Decision-Oficial-del-Stack-Tecnologico.md (Python 3.12+, Docker 24.x)
#             docs/35-Arquitectura-Oficial-del-Proyecto-Python.md (app/main.py)

FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
