"""Utilidad de emparejamiento por nombre normalizado -- resuelve el hallazgo
de `DATA-012A` (preparación): `EstadiosImporter` deriva `id_estadio` como
`EST-{venue_id de API-Football}`, mientras que `estadios.csv` ya tiene 76
filas curadas manualmente con el esquema secuencial `EST-000001`, `EST-000002`,
... Como los dos esquemas de clave nunca van a coincidir por diseño, una
ejecución real duplicaría cada estadio ya existente bajo una segunda clave.

## Estrategia elegida (`DATA-012B` §2)

Antes de escribir un estadio nuevo, se busca en las filas ya existentes una
que coincida por `(nombre, país)` **normalizados**: minúsculas, sin acentos,
espacios colapsados. Si hay coincidencia, el estadio importado reutiliza la
clave de negocio ya existente (`id_estadio`) en lugar de la derivada de la
API -- así `CsvUpsertWriter` lo trata como una actualización de la fila ya
existente (con la Política de Preservación ya aplicada campo a campo), nunca
como un alta nueva.

## Por qué `(nombre, país)` y no otro criterio

Es el único par de campos que **ambas** fuentes (curación manual y
API-Football) completan siempre con evidencia confirmada (`docs/43` §6.3) --
`capacidad`/`tipo_superficie` también están confirmados pero son más
propensos a discrepancias legítimas entre fuentes (remodelación de aforo) y
no identifican de forma fiable *qué* estadio es. No se usa ningún ID externo
porque los datos curados manualmente nunca lo registraron (no existía este
pipeline cuando se cargaron).

## Limitación aceptada, no resuelta aquí

Un estadio renombrado en la fuente (ej. cambio de patrocinador) no
coincidirá con el registro existente bajo su nombre anterior -- se creará
como alta nueva, no como actualización. Resolverlo exigiría un identificador
externo estable almacenado en el CSV (tabla de correspondencia,
`docs/43` §5), fuera del alcance de `DATA-012B` (solo endurece el
comportamiento ya implementado, no incorpora infraestructura nueva).
"""

from __future__ import annotations

import re
import unicodedata


def normalizar_texto(valor: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", sin_acentos).strip().casefold()


def encontrar_coincidencia(
    nombre: str,
    pais: str,
    existentes: dict[str, dict[str, str]],
    columna_nombre: str = "nombre",
    columna_pais: str = "pais",
) -> str | None:
    """Devuelve la clave de negocio (ej. `id_estadio`) de la fila existente
    cuyo `(nombre, país)` normalizado coincide con el buscado, o `None` si
    ninguna coincide. `existentes` es el `dict[clave, fila]` que ya produce
    `CsvUpsertWriter.leer_existentes()`.
    """
    objetivo = (normalizar_texto(nombre), normalizar_texto(pais))
    for clave, fila in existentes.items():
        candidato = (
            normalizar_texto(fila.get(columna_nombre, "")),
            normalizar_texto(fila.get(columna_pais, "")),
        )
        if candidato == objetivo:
            return clave
    return None
