"""Entidad `estadios` (Estadio). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.8.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.partido import Partido


class Estadio(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Recinto donde se juega un Partido. Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 9.

    `altitud_metros` no lleva CHECK de signo -- puede ser negativo
    (docs/33, seccion 4.8: "puede ser negativo, sin CHECK de signo").
    """

    __tablename__ = "estadios"
    __table_args__ = (
        CheckConstraint("capacidad > 0", name="ck_estadios_capacidad_positiva"),
    )

    id_estadio: Mapped[str] = mapped_column(Text, unique=True)
    nombre: Mapped[str] = mapped_column(Text)
    ciudad: Mapped[str] = mapped_column(Text)
    pais: Mapped[str] = mapped_column(Text)
    capacidad: Mapped[int] = mapped_column(Integer)
    tipo_superficie: Mapped[str] = mapped_column(Text)
    altitud_metros: Mapped[int] = mapped_column(Integer)
    techado: Mapped[bool] = mapped_column(Boolean)

    partidos: Mapped[list["Partido"]] = relationship(back_populates="estadio")
