"""Entidad `convocatorias` (asociativa N:M: Equipo x Jugador x Torneo). Ver
docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.3.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.jugador import Jugador
    from app.models.seleccion import Seleccion
    from app.models.torneo import Torneo


class Convocatoria(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Vínculo entre un Jugador, un Equipo y un Torneo concreto -- entidad
    asociativa de la única N:M de este tipo en el modelo (docs/32, seccion 4).
    Fuente de campos: `data/processed/selecciones-nacionales/README.md`,
    entidad 3.
    """

    __tablename__ = "convocatorias"
    __table_args__ = (
        UniqueConstraint(
            "torneo_id", "seleccion_id", "jugador_id", name="uq_convocatorias_torneo_seleccion_jugador"
        ),
        UniqueConstraint(
            "torneo_id", "seleccion_id", "dorsal", name="uq_convocatorias_torneo_seleccion_dorsal"
        ),
        CheckConstraint("dorsal > 0", name="ck_convocatorias_dorsal_positivo"),
    )

    id_convocatoria: Mapped[str] = mapped_column(Text, unique=True)
    torneo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("torneos.id"))
    seleccion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("selecciones.id")
    )
    jugador_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jugadores.id")
    )
    dorsal: Mapped[int] = mapped_column(Integer)
    posicion_convocatoria: Mapped[str] = mapped_column(Text)
    fecha_convocatoria: Mapped[date] = mapped_column(Date)
    estado_convocatoria: Mapped[str] = mapped_column(Text)

    torneo: Mapped["Torneo"] = relationship(back_populates="convocatorias")
    seleccion: Mapped["Seleccion"] = relationship(back_populates="convocatorias")
    jugador: Mapped["Jugador"] = relationship(back_populates="convocatorias")
