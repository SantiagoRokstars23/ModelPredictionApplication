"""Entidad `lesiones` (Lesión). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.10.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.jugador import Jugador
    from app.models.partido import Partido


class Lesion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Episodio médico de un Jugador. Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 6.
    `id_seleccion` no se almacena (se deriva de `jugadores.id_jugador`,
    campo excluido desde `MS-001`).
    """

    __tablename__ = "lesiones"
    __table_args__ = (
        CheckConstraint(
            "fecha_estimada_retorno IS NULL OR fecha_estimada_retorno >= fecha_inicio",
            name="ck_lesiones_fecha_estimada_retorno_coherente",
        ),
    )

    id_lesion: Mapped[str] = mapped_column(Text, unique=True)
    jugador_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jugadores.id")
    )
    tipo_lesion: Mapped[str] = mapped_column(Text)
    gravedad: Mapped[str] = mapped_column(Text)
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_estimada_retorno: Mapped[date | None] = mapped_column(Date)
    fecha_retorno_real: Mapped[date | None] = mapped_column(Date)
    partido_origen_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("partidos.id")
    )
    estado: Mapped[str] = mapped_column(Text)
    fuente: Mapped[str] = mapped_column(Text)

    jugador: Mapped["Jugador"] = relationship(back_populates="lesiones")
    partido_origen: Mapped["Partido | None"] = relationship(
        back_populates="lesiones_originadas"
    )
