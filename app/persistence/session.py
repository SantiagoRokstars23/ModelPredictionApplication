"""Fábrica de sesiones de SQLAlchemy y gestor de contexto seguro.

Ver docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, sección 4 (app/persistence).

BUILD-003: únicamente la fábrica de sesiones y su manejo seguro -- ninguna
consulta de negocio, ningún repositorio específico (ver repositories/).
"""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.orm import Session, sessionmaker

from app.persistence.database import get_engine

# Fábrica única de sesiones de toda la aplicación (validación obligatoria de
# BUILD-003: "una única Session Factory"). No se vincula (`bind=`) a un Engine
# en tiempo de importación -- cada sesión se crea, en `get_session()`, con el
# Engine único ya perezosamente inicializado por `get_engine()`.
SessionLocal: sessionmaker[Session] = sessionmaker(autoflush=False, autocommit=False)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Único punto oficial para obtener una sesión (docs/35: "una única forma
    oficial de acceder a PostgreSQL"). Ningún otro paquete debe instanciar una
    `Session` por su cuenta.

    Manejo seguro de sesiones: confirma (`commit`) la transacción si el bloque
    `with` termina sin errores; la deshace (`rollback`) si ocurre una
    excepción; siempre cierra la sesión al salir, ocurra lo que ocurra.
    """
    session = SessionLocal(bind=get_engine())
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
