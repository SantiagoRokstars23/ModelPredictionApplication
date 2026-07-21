"""Base declarativa y mixins comunes a las 14 entidades ORM.

Ver docs/33-Modelo-Fisico-PostgreSQL.md, seccion 2 (Convenciones generales).

BUILD-002: unicamente declaraciones de mapeo (columnas, tipos, valores por
defecto de columna) -- ningun metodo, ninguna logica de negocio, ninguna
consulta.

Nota de alcance (aplica a las 14 entidades, no se repite en cada archivo):
los campos categoricos tipo ENUM (`confederacion`, `tipo`, `fase`, `gravedad`,
`mercado`, `estado_ejecucion`, etc.) se implementan como TEXT sin una lista
`CHECK ... IN (...)` -- docs/33, seccion 2, ya decide "TEXT restringido por
CHECK" en principio, pero esta mision se limita a las restricciones simples
explicitamente enumeradas en docs/33, seccion 7 (NOT NULL, UNIQUE, CHECK de
rango/comparacion, integridad referencial). Enumerar cada valor permitido de
cada ENUM es una decision de validacion mas amplia (algunos, como
`estado_convocatoria`, siguen "pendientes de formalizar del todo", docs/27) y
queda, deliberadamente, fuera del alcance de BUILD-002.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa comun a las 14 entidades del Modelo Fisico (docs/33)."""


class UUIDPrimaryKeyMixin:
    """Clave tecnica UUID, uniforme en las 14 tablas (docs/33, secciones 2 y 8).

    Generacion en Python (`uuid.uuid4`), no en el servidor -- consistente con
    el argumento de generacion distribuida ya fundamentado en docs/33, seccion 8
    ("generable en cualquier nodo sin coordinacion central"). Migrar a UUIDv7
    (misma seccion, cuando el driver/motor lo soporte comodamente) es un
    cambio futuro localizado a este mixin, sin tocar ninguna entidad individual.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    """`creado_en` + `actualizado_en` -- tablas mutables (docs/33, seccion 2)."""

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CreatedAtOnlyMixin:
    """Solo `creado_en` -- tablas inmutables por regla de negocio (docs/33,
    seccion 2): `predicciones`, `resultados`, `auditorias`, `cuotas`. La
    ausencia deliberada de `actualizado_en` hace visible el principio de
    inmutabilidad (`docs/14`: "nunca se modifica una predicción") en el
    propio esquema, sin necesitar un trigger.
    """

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
