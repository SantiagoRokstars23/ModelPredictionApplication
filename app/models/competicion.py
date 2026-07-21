"""Entidad `competiciones` (Competición). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.4.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.torneo import Torneo


class Competicion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Marco organizativo permanente (ej. "Copa Mundial FIFA"). Fuente de
    campos: `data/processed/selecciones-nacionales/README.md`, entidad 10.
    """

    __tablename__ = "competiciones"
    __table_args__ = (
        CheckConstraint(
            "periodicidad_anios IS NULL OR periodicidad_anios > 0",
            name="ck_competiciones_periodicidad_positiva",
        ),
    )

    id_competicion: Mapped[str] = mapped_column(Text, unique=True)
    nombre: Mapped[str] = mapped_column(Text, unique=True)
    confederacion_organizadora: Mapped[str] = mapped_column(Text)
    tipo: Mapped[str] = mapped_column(Text)
    periodicidad_anios: Mapped[int | None] = mapped_column(Integer)
    activa: Mapped[bool] = mapped_column(Boolean)

    torneos: Mapped[list["Torneo"]] = relationship(back_populates="competicion")
