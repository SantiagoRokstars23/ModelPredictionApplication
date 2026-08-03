"""Clasificación de calidad por registro importado -- brief de `DATA-012`:
"Cada registro deberá indicar: Completo / Incompleto / Condicional".

Referencia de autoridad: `docs/44-Reconciliacion-del-Esquema.md` §2, que ya
define la distinción reutilizada aquí -- un campo `CONDICIONAL` (obligatorio
en el esquema, sin fuente hoy) nunca es un error de importación, es la
política ya aprobada por `GOV-003`; un campo `OBLIGATORIO` ausente sí lo es
(`docs/38` §5: "si falta un campo obligatorio, la fila se rechaza").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CalidadRegistro(str, Enum):
    """Tres valores, exactamente los que pide el brief -- ningún cuarto
    valor se introduce aquí (`NO DISPONIBLE`/`OPCIONAL`/`DERIVADO` de
    `docs/44` son categorías de *campo*, no de *registro*; a nivel de
    registro solo importa si algo obligatorio real falta o no).
    """

    COMPLETO = "completo"
    """Todos los campos obligatorios están presentes y ningún campo
    CONDICIONAL/NO DISPONIBLE de la entidad quedó vacío (es decir, para esta
    fila en particular, la fuente sí entregó algo en esos campos -- caso
    posible pero no garantizado, ej. si una futura versión de la fuente
    empieza a proveer un campo hoy CONDICIONAL)."""

    CONDICIONAL = "condicional"
    """Todos los campos obligatorios reales están presentes, pero al menos
    un campo CONDICIONAL/NO DISPONIBLE (`docs/44`) quedó vacío -- exactamente
    la política ya aprobada, nunca un error. Es el caso esperado y normal
    para la mayoría de los registros mientras esos campos no tengan fuente."""

    INCOMPLETO = "incompleto"
    """Falta al menos un campo declarado OBLIGATORIO con fuente confirmada
    (`docs/44`) -- un fallo real, no una brecha de fuente ya conocida. La
    fila se omite del CSV (`docs/38` §5: "la fila se rechaza"), nunca se
    escribe con el campo vacío."""


@dataclass(frozen=True)
class ResultadoCalidad:
    calidad: CalidadRegistro
    campos_obligatorios_faltantes: tuple[str, ...] = field(default_factory=tuple)
    campos_condicionales_vacios: tuple[str, ...] = field(default_factory=tuple)


def evaluar_calidad(
    fila: dict[str, str | None],
    campos_obligatorios: tuple[str, ...],
    campos_condicionales: tuple[str, ...],
) -> ResultadoCalidad:
    """Evalúa una fila ya normalizada (valores `str`/`None`, nunca crudos de
    la API) contra las dos listas de campos que cada importador declara según
    la clasificación de `docs/44`. Un campo se considera "vacío" si es
    `None` o una cadena vacía tras `strip()` -- nunca se interpreta `"0"` ni
    `"False"` como vacío (serían valores reales, no ausencia de dato).
    """

    def _vacio(valor: str | None) -> bool:
        return valor is None or valor.strip() == ""

    faltantes = tuple(campo for campo in campos_obligatorios if _vacio(fila.get(campo)))
    if faltantes:
        return ResultadoCalidad(
            calidad=CalidadRegistro.INCOMPLETO, campos_obligatorios_faltantes=faltantes
        )

    condicionales_vacios = tuple(
        campo for campo in campos_condicionales if _vacio(fila.get(campo))
    )
    if condicionales_vacios:
        return ResultadoCalidad(
            calidad=CalidadRegistro.CONDICIONAL,
            campos_condicionales_vacios=condicionales_vacios,
        )

    return ResultadoCalidad(calidad=CalidadRegistro.COMPLETO)
