"""Entidad `estadisticas_partido` (asociativa N:M: Partido x Equipo). Ver
docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.7.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.partido import Partido
    from app.models.seleccion import Seleccion


class EstadisticaPartido(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Rendimiento de un Equipo dentro de un Partido ya jugado -- entidad
    asociativa de la segunda y última N:M del modelo (docs/32, seccion 4).
    Fuente de campos: `data/processed/selecciones-nacionales/README.md`,
    entidad 5. `xga` no se almacena (se deriva por self-join sobre `xg`,
    campo excluido desde `MS-001`).
    """

    __tablename__ = "estadisticas_partido"
    __table_args__ = (
        UniqueConstraint(
            "partido_id", "seleccion_id", name="uq_estadisticas_partido_partido_seleccion"
        ),
        CheckConstraint("xg >= 0", name="ck_estadisticas_partido_xg_no_negativo"),
        CheckConstraint(
            "posesion_pct >= 0 AND posesion_pct <= 100",
            name="ck_estadisticas_partido_posesion_rango",
        ),
        CheckConstraint(
            "precision_pases_pct >= 0 AND precision_pases_pct <= 100",
            name="ck_estadisticas_partido_precision_pases_rango",
        ),
        CheckConstraint("disparos_totales >= 0", name="ck_estadisticas_partido_disparos_no_negativo"),
        CheckConstraint(
            "disparos_al_arco >= 0 AND disparos_al_arco <= disparos_totales",
            name="ck_estadisticas_partido_disparos_al_arco_coherente",
        ),
        CheckConstraint("corners >= 0", name="ck_estadisticas_partido_corners_no_negativo"),
        CheckConstraint(
            "faltas_cometidas >= 0", name="ck_estadisticas_partido_faltas_no_negativas"
        ),
        CheckConstraint(
            "tarjetas_amarillas >= 0", name="ck_estadisticas_partido_amarillas_no_negativas"
        ),
        CheckConstraint("tarjetas_rojas >= 0", name="ck_estadisticas_partido_rojas_no_negativas"),
        CheckConstraint(
            "pases_completados >= 0", name="ck_estadisticas_partido_pases_no_negativos"
        ),
    )

    id_estadistica_partido: Mapped[str] = mapped_column(Text, unique=True)
    partido_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("partidos.id")
    )
    seleccion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("selecciones.id")
    )
    xg: Mapped[Decimal] = mapped_column(Numeric)
    posesion_pct: Mapped[Decimal] = mapped_column(Numeric)
    disparos_totales: Mapped[int] = mapped_column(Integer)
    disparos_al_arco: Mapped[int] = mapped_column(Integer)
    corners: Mapped[int] = mapped_column(Integer)
    faltas_cometidas: Mapped[int] = mapped_column(Integer)
    tarjetas_amarillas: Mapped[int] = mapped_column(Integer)
    tarjetas_rojas: Mapped[int] = mapped_column(Integer)
    pases_completados: Mapped[int] = mapped_column(Integer)
    precision_pases_pct: Mapped[Decimal] = mapped_column(Numeric)

    partido: Mapped["Partido"] = relationship(back_populates="estadisticas")
    seleccion: Mapped["Seleccion"] = relationship(back_populates="estadisticas_partido")
