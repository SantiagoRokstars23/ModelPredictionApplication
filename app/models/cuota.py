"""Entidad `cuotas` (Cuota). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.11.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.

Nota (docs/33, seccion 2/12): tabla inmutable -- cada captura es un evento
nuevo, nunca se actualiza una fila ya escrita, por eso usa `CreatedAtOnlyMixin`
(sin `actualizado_en`). Las cuotas no son una Variable Oficial (`docs/16`,
"Reglas generales") -- son Datos de Mercado, categoría paralela, con contrato
completo todavía pendiente (`INC-05`).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtOnlyMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.partido import Partido


class Cuota(UUIDPrimaryKeyMixin, CreatedAtOnlyMixin, Base):
    """Precio de mercado de un resultado de un Partido, capturado de una casa
    de apuestas en un instante concreto. Fuente de campos:
    `data/processed/selecciones-nacionales/README.md`, entidad 7.
    `probabilidad_implicita` no se almacena (se calcula, `1 / cuota_decimal`,
    dato derivado, no bruto).
    """

    __tablename__ = "cuotas"
    __table_args__ = (
        UniqueConstraint(
            "partido_id",
            "casa_apuestas",
            "mercado",
            "seleccion_o_resultado",
            "fecha_captura",
            name="uq_cuotas_partido_casa_mercado_resultado_captura",
        ),
        CheckConstraint("cuota_decimal > 1.00", name="ck_cuotas_cuota_decimal_valida"),
    )

    id_cuota: Mapped[str] = mapped_column(Text, unique=True)
    partido_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("partidos.id")
    )
    casa_apuestas: Mapped[str] = mapped_column(Text)
    mercado: Mapped[str] = mapped_column(Text)
    seleccion_o_resultado: Mapped[str] = mapped_column(Text)
    cuota_decimal: Mapped[Decimal] = mapped_column(Numeric)
    fecha_captura: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    estado_cuota: Mapped[str] = mapped_column(Text)

    partido: Mapped["Partido"] = relationship(back_populates="cuotas")
