# Modelo Santiago -- Proyecto Python (bootstrap)

Este documento es la referencia **tecnica** para instalar y ejecutar el proyecto
Python que implementa el Modelo Santiago
(`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`).

No describe la filosofia, las reglas ni la arquitectura conceptual del modelo --
eso sigue viviendo exclusivamente en `docs/`, `engine/` y `models/` (raiz del
repositorio). Este archivo vive dentro de `app/` deliberadamente, para no
sobrescribir ni duplicar el `README.md` raiz del proyecto, que sigue siendo la
referencia navegacional oficial de todo el Modelo Santiago.

---

## Estado actual (BUILD-001 -- bootstrap oficial)

Estructura de paquetes creada, sin logica de negocio, sin motores, sin
endpoints funcionales y sin conexion real a base de datos. Ningun componente
del Modelo Santiago (Runtime, Prediction Context, Engine, Variables Oficiales,
formulas matematicas) esta implementado todavia -- ver
`docs/00-Project-Tracker.md`, entrada `BUILD-001`.

## Instalacion

Requiere Python 3.12 o superior (`docs/34-Decision-Oficial-del-Stack-Tecnologico.md`,
seccion 13).

1. Crear un entorno virtual, desde la raiz del repositorio:

   ```bash
   python -m venv .venv
   ```

2. Activar el entorno virtual:

   - Linux/macOS: `source .venv/bin/activate`
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`

3. Instalar las dependencias del proyecto:

   ```bash
   pip install -e .
   ```

   Para incluir tambien las herramientas de desarrollo (pytest, Ruff, MyPy):

   ```bash
   pip install -e ".[dev]"
   ```

## Configuracion

Copiar `.env.example` a `.env` y completar los valores reales antes de ejecutar:

```bash
cp .env.example .env
```

## Ejecucion (modo desarrollo)

```bash
uvicorn app.main:app --reload
```

La aplicacion queda disponible en `http://localhost:8000` -- hoy sin ningun
endpoint funcional (`app/main.py` expone unicamente una instancia vacia de
FastAPI, conforme al alcance de BUILD-001).

## Docker

Construir y levantar la aplicacion junto con PostgreSQL:

```bash
docker compose up --build
```

Esto levanta exactamente dos servicios (`app`, `db`) -- ningun servicio
adicional (`docker-compose.yml`; BUILD-001, seccion 5).

## Migraciones (Alembic)

La estructura de Alembic ya esta inicializada (`migrations/`), pero **no
existe ninguna revision todavia** -- `app/models` no declara ningun modelo
aun. Ejecutar `alembic revision`/`alembic upgrade` no producira ningun cambio
real hasta que exista esa implementacion (mision futura).

## Pruebas

```bash
pytest
```

Hoy no existe ninguna prueba real -- `tests/` esta vacio, listo para recibir
las primeras pruebas cuando se implemente el primer componente de `app/`.
