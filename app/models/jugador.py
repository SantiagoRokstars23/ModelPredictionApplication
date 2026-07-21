"""Entidad `jugadores` (Jugador). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.2.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.

Observacion (no resuelta en esta mision, documentada conforme a la filosofia
de "detenerse y reportar antes de resolver una contradiccion"): docs/33,
seccion 7, recomienda un "indice unico parcial... jugadores, condicion
activo_seleccion = true, unico por jugador" para implementar fisicamente
"un jugador solo puede tener una id_seleccion activa a la vez". Esa
recomendacion no se traduce con claridad al esquema real de esta tabla
(seccion 4.2): cada jugador ya es una unica fila, con una unica columna
`seleccion_id` y un unico `activo_seleccion` -- no existen multiples filas
por jugador entre las que un indice parcial deba elegir "la activa". Se
documenta la observacion, sin inventar una reinterpretacion del esquema para
forzar que el indice tenga sentido.
"""

from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Date, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.convocatoria import Convocatoria
    from app.models.lesion import Lesion
    from app.models.seleccion import Seleccion


class Jugador(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Futbolista individual. Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 2.
    """

    __tablename__ = "jugadores"
    __table_args__ = (
        CheckConstraint(
            "altura_cm IS NULL OR altura_cm > 0", name="ck_jugadores_altura_positiva"
        ),
    )

    id_jugador: Mapped[str] = mapped_column(Text, unique=True)
    nombre_completo: Mapped[str] = mapped_column(Text)
    nombre_conocido: Mapped[str | None] = mapped_column(Text)
    fecha_nacimiento: Mapped[date] = mapped_column(Date)
    posicion_principal: Mapped[str] = mapped_column(Text)
    pie_habil: Mapped[str | None] = mapped_column(Text)
    altura_cm: Mapped[int | None] = mapped_column(Integer)
    seleccion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("selecciones.id")
    )
    club_actual: Mapped[str | None] = mapped_column(Text)
    activo_seleccion: Mapped[bool] = mapped_column(Boolean)

    seleccion: Mapped["Seleccion"] = relationship(
        back_populates="jugadores", foreign_keys=[seleccion_id]
    )
    convocatorias: Mapped[list["Convocatoria"]] = relationship(back_populates="jugador")
    lesiones: Mapped[list["Lesion"]] = relationship(back_populates="jugador")
