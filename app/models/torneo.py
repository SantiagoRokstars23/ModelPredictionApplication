"""Entidad `torneos` (Torneo). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.5.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.competicion import Competicion
    from app.models.convocatoria import Convocatoria
    from app.models.partido import Partido


class Torneo(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Edición concreta de una Competición (ej. "Mundial 2026"). Fuente de
    campos: `data/processed/selecciones-nacionales/README.md`, entidad 11.
    El campo derivado `campeon_id_seleccion` (eliminado desde MS-001) no se
    incluye aquí -- se obtiene consultando `partidos` con `fase = final`.
    """

    __tablename__ = "torneos"
    __table_args__ = (
        CheckConstraint("fecha_fin >= fecha_inicio", name="ck_torneos_fechas_orden"),
        CheckConstraint(
            "numero_selecciones_participantes IS NULL OR numero_selecciones_participantes > 0",
            name="ck_torneos_participantes_positivo",
        ),
    )

    id_torneo: Mapped[str] = mapped_column(Text, unique=True)
    competicion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("competiciones.id")
    )
    edicion: Mapped[str] = mapped_column(Text)
    paises_organizadores: Mapped[str | None] = mapped_column(Text)
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_fin: Mapped[date] = mapped_column(Date)
    formato: Mapped[str | None] = mapped_column(Text)
    numero_selecciones_participantes: Mapped[int | None] = mapped_column(Integer)

    competicion: Mapped["Competicion"] = relationship(back_populates="torneos")
    convocatorias: Mapped[list["Convocatoria"]] = relationship(back_populates="torneo")
    partidos: Mapped[list["Partido"]] = relationship(back_populates="torneo")
