"""`BaseRepository` -- operaciones CRUD genéricas sobre cualquier entidad ORM.

Ver docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, sección 4 (app/persistence).

BUILD-003: únicamente las cinco operaciones comunes (`add`, `get`, `list`,
`delete`, `update`) -- ninguna consulta específica de un modelo concreto (ej.
"predicciones de un partido"), ningún filtro de negocio. Los repositorios
específicos (`PredictionRepository`, `MatchRepository`, `SelectionRepository`)
quedan explícitamente fuera del alcance de esta misión.
"""

from __future__ import annotations

import uuid
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Repositorio genérico, parametrizado por tipo -- una única clase
    reutilizable para las 14 entidades de `app/models` (docs/33), sin ninguna
    consulta específica (validación obligatoria de BUILD-003: "BaseRepository
    completamente genérico").
    """

    def __init__(self, session: Session, model: type[ModelType]) -> None:
        self._session = session
        self._model = model

    def add(self, entidad: ModelType) -> ModelType:
        """Agrega una entidad nueva a la sesión."""
        self._session.add(entidad)
        self._session.flush()
        return entidad

    def get(self, id_: uuid.UUID) -> ModelType | None:
        """Recupera una entidad por su clave técnica (`id`), o `None`."""
        return self._session.get(self._model, id_)

    def list(self) -> list[ModelType]:
        """Recupera todas las filas de la entidad -- sin filtros ni orden;
        cualquier consulta más específica pertenece a un repositorio propio,
        fuera del alcance de esta misión.
        """
        return list(self._session.scalars(select(self._model)).all())

    def delete(self, entidad: ModelType) -> None:
        """Marca una entidad ya recuperada de la sesión para su eliminación."""
        self._session.delete(entidad)

    def update(self, entidad: ModelType) -> ModelType:
        """Confirma en la sesión los cambios ya aplicados a una entidad
        existente. No decide qué campo cambiar -- eso es responsabilidad de
        quien llama, nunca de este repositorio.
        """
        self._session.add(entidad)
        self._session.flush()
        return entidad
