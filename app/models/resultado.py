"""Entidad `resultados` (Resultado). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.13.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.

Nota (docs/33, seccion 2): tabla inmutable -- `CreatedAtOnlyMixin`, sin
`actualizado_en` ("nunca modificar un resultado oficial ya almacenado").
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtOnlyMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.auditoria import Auditoria
    from app.models.partido import Partido


class Resultado(UUIDPrimaryKeyMixin, CreatedAtOnlyMixin, Base):
    """Resultado oficial verificado de un Partido finalizado. `partido_id`
    es único -- cardinalidad 1:1 con Partido (docs/32, seccion 4).
    """

    __tablename__ = "resultados"
    __table_args__ = (
        CheckConstraint("goles_local >= 0", name="ck_resultados_goles_local_no_negativo"),
        CheckConstraint(
            "goles_visitante >= 0", name="ck_resultados_goles_visitante_no_negativo"
        ),
    )

    partido_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("partidos.id"), unique=True
    )
    goles_local: Mapped[int] = mapped_column(Integer)
    goles_visitante: Mapped[int] = mapped_column(Integer)
    fuente: Mapped[str] = mapped_column(Text)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    partido: Mapped["Partido"] = relationship(back_populates="resultado")
    auditoria: Mapped["Auditoria | None"] = relationship(
        back_populates="resultado", uselist=False
    )
