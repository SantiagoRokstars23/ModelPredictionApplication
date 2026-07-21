"""Paquete persistence -- acceso a datos.

Responsabilidad (docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 4):
ejecutar consultas y escrituras contra PostgreSQL usando app/models. Nunca
ejecuta logica matematica o de negocio -- cualquier calculo que aparezca
aqui duplicaria una responsabilidad ya asignada a app/engine o app/preparation.

BUILD-003: primera version funcional. Expone:

- `get_engine()` (database.py) -- el único Engine de SQLAlchemy de toda la
  aplicación, de creación perezosa, leyendo `DATABASE_URL` desde `app/config`.
- `get_session()` / `SessionLocal` (session.py) -- la única fábrica y el
  único gestor de contexto para obtener una sesión.
- `BaseRepository` (repositories/base_repository.py) -- operaciones CRUD
  genéricas (`add`, `get`, `list`, `delete`, `update`), sin ninguna consulta
  específica de un modelo concreto.

Ningún repositorio específico (`PredictionRepository`, `MatchRepository`,
`SelectionRepository`, etc.), ninguna consulta de negocio, ningún filtro --
explícitamente fuera del alcance de BUILD-003. Ningún paquete de `app/`
distinto de éste debe crear un `Engine` o una `Session` por su cuenta: éste
es el único punto oficial de acceso a PostgreSQL (docs/35, sección 6).
"""

from app.persistence.database import get_engine
from app.persistence.repositories.base_repository import BaseRepository
from app.persistence.session import SessionLocal, get_session

__all__ = ["BaseRepository", "SessionLocal", "get_engine", "get_session"]
