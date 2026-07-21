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

BUILD-008: implementado `RuntimePersistence` (runtime_persistence.py) --
satisface `PersistenceProtocol` (`app/runtime/runtime.py`, BUILD-005),
reutilizando exclusivamente `get_session`/`BaseRepository` ya construidos en
BUILD-003 (ninguna sesión, motor o conexión nueva). Implementa
`persist_prediction` (persistencia real de una `Prediccion`, con la brecha
de resolución de `partido_id` documentada explícitamente en el módulo);
`persist_audit`/`persist_learning` quedan como *placeholders* documentados,
sin lógica de auditoría ni aprendizaje real.

Ningún repositorio específico (`PredictionRepository`, `MatchRepository`,
`SelectionRepository`, etc.), ninguna consulta de negocio, ningún filtro --
explícitamente fuera del alcance de esta serie de misiones. Ningún paquete
de `app/` distinto de éste debe crear un `Engine` o una `Session` por su
cuenta: éste es el único punto oficial de acceso a PostgreSQL (docs/35,
sección 6).
"""

from app.persistence.database import get_engine
from app.persistence.repositories.base_repository import BaseRepository
from app.persistence.runtime_persistence import RuntimePersistence
from app.persistence.session import SessionLocal, get_session

__all__ = [
    "BaseRepository",
    "RuntimePersistence",
    "SessionLocal",
    "get_engine",
    "get_session",
]
