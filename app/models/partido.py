"""Entidad `partidos` (Partido — entidad central). Ver
docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.6.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

import uuid
from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.arbitro import Arbitro
    from app.models.cuota import Cuota
    from app.models.estadio import Estadio
    from app.models.estadistica_partido import EstadisticaPartido
    from app.models.lesion import Lesion
    from app.models.prediccion import Prediccion
    from app.models.resultado import Resultado
    from app.models.seleccion import Seleccion
    from app.models.torneo import Torneo


class Partido(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """El enfrentamiento entre dos Equipos. Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 4.

    `torneo_id` es obligatorio siempre, incluidos los amistosos (convención
    "Amistosos Internacionales", `MS-001`) -- docs/33, seccion 4.6.
    """

    __tablename__ = "partidos"
    __table_args__ = (
        CheckConstraint(
            "seleccion_local_id <> seleccion_visitante_id",
            name="ck_partidos_equipos_distintos",
        ),
        CheckConstraint(
            "asistencia IS NULL OR asistencia >= 0", name="ck_partidos_asistencia_no_negativa"
        ),
    )

    id_partido: Mapped[str] = mapped_column(Text, unique=True)
    torneo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("torneos.id"))
    seleccion_local_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("selecciones.id")
    )
    seleccion_visitante_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("selecciones.id")
    )
    estadio_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("estadios.id")
    )
    arbitro_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("arbitros.id")
    )
    fecha: Mapped[date] = mapped_column(Date)
    hora_local: Mapped[time | None] = mapped_column(Time)
    fase: Mapped[str] = mapped_column(Text)
    jornada: Mapped[int | None] = mapped_column(Integer)
    goles_local: Mapped[int | None] = mapped_column(Integer)
    goles_visitante: Mapped[int | None] = mapped_column(Integer)
    estado_partido: Mapped[str] = mapped_column(Text)
    asistencia: Mapped[int | None] = mapped_column(Integer)

    torneo: Mapped["Torneo"] = relationship(back_populates="partidos")
    seleccion_local: Mapped["Seleccion"] = relationship(
        back_populates="partidos_como_local", foreign_keys=[seleccion_local_id]
    )
    seleccion_visitante: Mapped["Seleccion"] = relationship(
        back_populates="partidos_como_visitante", foreign_keys=[seleccion_visitante_id]
    )
    estadio: Mapped["Estadio | None"] = relationship(back_populates="partidos")
    arbitro: Mapped["Arbitro | None"] = relationship(back_populates="partidos")
    estadisticas: Mapped[list["EstadisticaPartido"]] = relationship(back_populates="partido")
    lesiones_originadas: Mapped[list["Lesion"]] = relationship(back_populates="partido_origen")
    cuotas: Mapped[list["Cuota"]] = relationship(back_populates="partido")
    prediccion: Mapped["Prediccion | None"] = relationship(
        back_populates="partido", uselist=False
    )
    resultado: Mapped["Resultado | None"] = relationship(
        back_populates="partido", uselist=False
    )
