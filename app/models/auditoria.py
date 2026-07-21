"""Entidad `auditorias` (Auditoría). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.14.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.

Nota (docs/33, seccion 2/14): tabla inmutable -- `CreatedAtOnlyMixin`. Registra
la comparación *por partido* de una Predicción contra su Resultado (Top1/Top4/
error de calibración); las métricas agregadas de cartera (ROI, Yield,
Drawdown, `docs/09`) son series calculadas sobre muchas filas de esta tabla,
no columnas de una sola -- no se modelan aquí.

Restricción de negocio NO implementada aquí, a propósito (docs/33, seccion 4.14):
`prediccion_id` y `resultado_id` deben referirse al mismo `partido_id` -- un
`CHECK` de PostgreSQL no puede comparar valores de otra tabla directamente;
esa regla pertenece a la capa de aplicación (o a un mecanismo declarativo más
avanzado), fuera del alcance de BUILD-002 ("no incluir lógica").
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtOnlyMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.prediccion import Prediccion
    from app.models.resultado import Resultado


class Auditoria(UUIDPrimaryKeyMixin, CreatedAtOnlyMixin, Base):
    """Comparación cuantitativa entre una Predicción y su Resultado
    correspondiente -- exige que ambos existan simultáneamente (docs/32,
    seccion 8: "nunca antes").
    """

    __tablename__ = "auditorias"

    prediccion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("predicciones.id"), unique=True
    )
    resultado_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resultados.id"), unique=True
    )
    acierto_top1: Mapped[bool] = mapped_column(Boolean)
    acierto_top4: Mapped[bool] = mapped_column(Boolean)
    error_calibracion: Mapped[Decimal | None] = mapped_column(Numeric)
    valor_esperado_realizado: Mapped[Decimal | None] = mapped_column(Numeric)
    fecha_auditoria: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    prediccion: Mapped["Prediccion"] = relationship(back_populates="auditoria")
    resultado: Mapped["Resultado"] = relationship(back_populates="auditoria")
