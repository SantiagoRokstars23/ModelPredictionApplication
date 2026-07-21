"""Entidad `predicciones` (Predicción). Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 4.12.

BUILD-002: solo columnas, claves y relaciones ORM -- ninguna logica de negocio.

Nota (docs/33, seccion 2): tabla inmutable -- `CreatedAtOnlyMixin`, sin
`actualizado_en` ("nunca se modifica una predicción", `docs/14`). Los campos
`top_marcadores`/`variables_influyentes` usan JSONB por ser estructuras de
forma variable que se leen siempre completas junto con el resto de la
predicción (docs/33, seccion 3) -- únicos dos campos JSONB de todo el modelo.
"""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtOnlyMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.auditoria import Auditoria
    from app.models.partido import Partido


class Prediccion(UUIDPrimaryKeyMixin, CreatedAtOnlyMixin, Base):
    """Registro inmutable de qué predijo el modelo para un Partido, antes de
    que ocurriera. `partido_id` es único -- cardinalidad 1:1 con Partido
    (docs/32, seccion 4; regla de negocio: nunca una segunda predicción
    silenciosa para el mismo partido, `docs/06`).
    """

    __tablename__ = "predicciones"
    __table_args__ = (
        CheckConstraint(
            "probabilidad_local >= 0 AND probabilidad_local <= 1",
            name="ck_predicciones_probabilidad_local_rango",
        ),
        CheckConstraint(
            "probabilidad_empate >= 0 AND probabilidad_empate <= 1",
            name="ck_predicciones_probabilidad_empate_rango",
        ),
        CheckConstraint(
            "probabilidad_visitante >= 0 AND probabilidad_visitante <= 1",
            name="ck_predicciones_probabilidad_visitante_rango",
        ),
        CheckConstraint(
            "confianza >= 0 AND confianza <= 100", name="ck_predicciones_confianza_rango"
        ),
        CheckConstraint(
            "indice_caos >= 0 AND indice_caos <= 100", name="ck_predicciones_indice_caos_rango"
        ),
    )

    id_prediccion: Mapped[str] = mapped_column(Text, unique=True)
    partido_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("partidos.id"), unique=True
    )
    version_modelo: Mapped[str] = mapped_column(Text)
    probabilidad_local: Mapped[Decimal] = mapped_column(Numeric)
    probabilidad_empate: Mapped[Decimal] = mapped_column(Numeric)
    probabilidad_visitante: Mapped[Decimal] = mapped_column(Numeric)
    top_marcadores: Mapped[list[dict[str, Any]]] = mapped_column(JSONB)
    variables_influyentes: Mapped[list[Any]] = mapped_column(JSONB)
    confianza: Mapped[Decimal] = mapped_column(Numeric)
    indice_caos: Mapped[Decimal] = mapped_column(Numeric)
    valor_esperado: Mapped[Decimal | None] = mapped_column(Numeric)
    estado_ejecucion: Mapped[str] = mapped_column(Text)

    partido: Mapped["Partido"] = relationship(back_populates="prediccion")
    auditoria: Mapped["Auditoria | None"] = relationship(
        back_populates="prediccion", uselist=False
    )
