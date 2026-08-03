"""Utilidades compartidas de valores -- extraídas para que la Política de
Preservación (`DATA-012B` §1) y el descubrimiento de IDs externos del runner
(`runner.py`) usen exactamente la misma regla que ya validaban por separado
`calidad.py` y `selecciones_importer.py`, en lugar de duplicarla.
"""

from __future__ import annotations


def es_vacio(valor: str | None) -> bool:
    """Un valor se considera vacío si es `None` o, tras `strip()`, una cadena
    vacía -- nunca se interpreta `"0"`/`"False"` como vacío (son valores
    reales, no ausencia de dato). Misma regla que ya usaba `calidad.py`.
    """
    return valor is None or valor.strip() == ""


def normalizar_codigo_iso3(codigo_raw: object) -> str | None:
    """Código de negocio de 3 letras (`docs/38` §9: `id_seleccion` único de 3
    letras). Un valor que no cumple ese formato se trata como ausente --
    nunca se trunca ni se completa artificialmente. Extraído de
    `SeleccionesImporter` para que el runner pueda derivar el mismo
    `id_seleccion` al descubrir IDs externos, sin duplicar la regla.
    """
    if not isinstance(codigo_raw, str):
        return None
    codigo = codigo_raw.strip().upper()
    if len(codigo) == 3 and codigo.isalpha():
        return codigo
    return None
