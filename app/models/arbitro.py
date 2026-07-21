"""Entidad `arbitros` (Árbitro). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.9.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.partido import Partido


class Arbitro(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Persona que dirige un Partido. Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 8.
    """

    __tablename__ = "arbitros"

    id_arbitro: Mapped[str] = mapped_column(Text, unique=True)
    nombre_completo: Mapped[str] = mapped_column(Text)
    nacionalidad: Mapped[str] = mapped_column(Text)
    confederacion_arbitral: Mapped[str] = mapped_column(Text)
    categoria: Mapped[str] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean)

    partidos: Mapped[list["Partido"]] = relationship(back_populates="arbitro")
