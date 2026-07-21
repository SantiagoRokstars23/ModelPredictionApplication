"""Entidad `selecciones` (Equipo). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.1.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Date, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.convocatoria import Convocatoria
    from app.models.estadistica_partido import EstadisticaPartido
    from app.models.jugador import Jugador
    from app.models.partido import Partido


class Seleccion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Selección nacional (Equipo, docs/32). Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 1.
    """

    __tablename__ = "selecciones"
    __table_args__ = (
        CheckConstraint(
            "ranking_fifa_actual > 0", name="ck_selecciones_ranking_fifa_positivo"
        ),
    )

    id_seleccion: Mapped[str] = mapped_column(Text, unique=True)
    nombre_pais: Mapped[str] = mapped_column(Text)
    nombre_federacion: Mapped[str] = mapped_column(Text)
    confederacion: Mapped[str] = mapped_column(Text)
    ranking_fifa_actual: Mapped[int] = mapped_column(Integer)
    ranking_fifa_fecha: Mapped[date] = mapped_column(Date)
    seleccionador_actual: Mapped[str | None] = mapped_column(Text)
    activa: Mapped[bool] = mapped_column(Boolean)

    jugadores: Mapped[list["Jugador"]] = relationship(
        back_populates="seleccion", foreign_keys="Jugador.seleccion_id"
    )
    convocatorias: Mapped[list["Convocatoria"]] = relationship(back_populates="seleccion")
    estadisticas_partido: Mapped[list["EstadisticaPartido"]] = relationship(
        back_populates="seleccion"
    )
    partidos_como_local: Mapped[list["Partido"]] = relationship(
        back_populates="seleccion_local", foreign_keys="Partido.seleccion_local_id"
    )
    partidos_como_visitante: Mapped[list["Partido"]] = relationship(
        back_populates="seleccion_visitante",
        foreign_keys="Partido.seleccion_visitante_id",
    )
