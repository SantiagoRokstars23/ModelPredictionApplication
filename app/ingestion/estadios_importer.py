"""`EstadiosImporter` -- construye `estadios.csv` a partir de `GET /venues`
de API-Football, con evidencia directa y completa (`docs/42-Verificacion-
Manual-API-Football.md` §3.18, objeto real de "Old Trafford" leído en su
totalidad: `id, name, address, city, country, capacity, surface, image`).

## Clasificación aplicada (`docs/44-Reconciliacion-del-Esquema.md` §3.6)

| Campo | Clasificación | Razón |
|---|---|---|
| `nombre`, `ciudad`, `pais`, `capacidad`, `tipo_superficie` | OBLIGATORIO | Fuente confirmada, objeto completo leído |
| `altitud_metros`, `techado` | CONDICIONAL | `docs/33` los declara obligatorios; confirmado ausentes del objeto completo (`DATA-010A` §3.18) -- quedan vacíos, nunca inventados |

`tipo_superficie` se preserva **sin transformar** el valor devuelto por la
fuente (ej. `"grass"`) -- el ENUM oficial del proyecto para esta columna
nunca fue formalizado con sus valores permitidos (mismo tipo de hallazgo ya
documentado para otros ENUM en `docs/38` §10.1); inventar aquí un mapeo a
valores no definidos violaría el mismo principio que ya protege a esos otros
campos.

## Matching contra estadios ya existentes (`DATA-012B` §2)

Hallazgo de la preparación de `DATA-012A`: `estadios.csv` ya tiene 76 filas
curadas manualmente con clave secuencial (`EST-000001`, `EST-000002`, ...),
mientras que este importador deriva `id_estadio` como `EST-{venue.id de
API-Football}` (ej. `EST-556`). Los dos esquemas nunca coinciden por diseño
-- sin una resolución previa, cada estadio ya existente se duplicaría bajo
una segunda clave en la primera ejecución real.

La estrategia (ver `app/ingestion/matching.py` para el detalle y las
limitaciones aceptadas) es: antes de escribir, buscar entre las filas ya
existentes una que coincida por `(nombre, país)` normalizados; si la hay, el
estadio importado reutiliza esa clave ya existente en lugar de la derivada
de la API, para que `CsvUpsertWriter` lo trate como actualización (con
Política de Preservación) y nunca como alta nueva.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from app.ingestion.api_football_client import ApiFootballClientProtocol, ApiFootballError
from app.ingestion.calidad import CalidadRegistro, evaluar_calidad
from app.ingestion.csv_upsert_writer import CsvUpsertWriter, ResumenEscritura
from app.ingestion.matching import encontrar_coincidencia

logger = logging.getLogger(__name__)

COLUMNAS = (
    "id_estadio",
    "nombre",
    "ciudad",
    "pais",
    "capacidad",
    "tipo_superficie",
    "altitud_metros",
    "techado",
)
CAMPOS_OBLIGATORIOS = ("id_estadio", "nombre", "ciudad", "pais", "capacidad", "tipo_superficie")
CAMPOS_CONDICIONALES = ("altitud_metros", "techado")
_ARCHIVO = "estadios.csv"
_PREFIJO_ID = "EST"


@dataclass(frozen=True)
class ResumenImportacionEstadios:
    escritura: ResumenEscritura
    completos: int = 0
    condicionales: int = 0
    incompletos: int = 0
    advertencias_pais: tuple[str, ...] = field(default_factory=tuple)


class EstadiosImporter:
    """Importa estadios vía `GET /venues?id={id}` -- un `venue.id` de
    API-Football por llamada (la única forma de consulta puntual ya
    confirmada; `/venues?country=` también existe pero devolvería el listado
    completo de un país, fuera del alcance mínimo verificado de esta
    misión).
    """

    def __init__(
        self,
        cliente: ApiFootballClientProtocol,
        data_dir: Path | None = None,
        paises_conocidos: frozenset[str] | None = None,
    ) -> None:
        self._cliente = cliente
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )
        self._paises_conocidos = paises_conocidos

    def importar(
        self, ids_venue_externos: list[int], dry_run: bool = False
    ) -> ResumenImportacionEstadios:
        """`dry_run=True` (`DATA-012B` §4): consulta la API y resuelve el
        matching igual que una ejecución real, pero no escribe
        `estadios.csv`.
        """
        escritor = CsvUpsertWriter(
            self._data_dir / _ARCHIVO, COLUMNAS, clave_negocio="id_estadio"
        )
        existentes = escritor.leer_existentes()

        filas: list[dict[str, str]] = []
        completos = 0
        condicionales = 0
        incompletos = 0
        advertencias_pais: list[str] = []

        for id_venue in ids_venue_externos:
            try:
                payload = self._cliente.get("/venues", {"id": id_venue})
            except ApiFootballError as exc:
                logger.error("No se pudo consultar /venues?id=%s: %s", id_venue, exc)
                incompletos += 1
                continue

            respuesta = payload.get("response", [])
            if not respuesta:
                logger.warning(
                    "'/venues?id=%s' no devolvió ningún estadio -- se omite, nunca se inventa.",
                    id_venue,
                )
                continue

            fila = self._mapear(respuesta[0])
            resultado = evaluar_calidad(fila, CAMPOS_OBLIGATORIOS, CAMPOS_CONDICIONALES)

            if resultado.calidad is CalidadRegistro.INCOMPLETO:
                incompletos += 1
                logger.error(
                    "Estadio externo %s omitido (INCOMPLETO): faltan %s",
                    id_venue,
                    resultado.campos_obligatorios_faltantes,
                )
                continue

            if self._paises_conocidos is not None and fila["pais"] not in self._paises_conocidos:
                mensaje = f"Estadio '{fila['nombre']}': país '{fila['pais']}' no está entre las selecciones ya importadas"
                advertencias_pais.append(mensaje)
                logger.warning(mensaje)

            coincidencia = encontrar_coincidencia(fila["nombre"], fila["pais"], existentes)
            if coincidencia is not None and coincidencia != fila["id_estadio"]:
                logger.info(
                    "Estadio '%s' coincide por nombre/país con el registro existente '%s' -- "
                    "se actualiza esa clave, no se crea una nueva.",
                    fila["nombre"],
                    coincidencia,
                )
                fila["id_estadio"] = coincidencia

            if resultado.calidad is CalidadRegistro.CONDICIONAL:
                condicionales += 1
            else:
                completos += 1
            filas.append(fila)

        escritura = escritor.upsert(filas, simular=dry_run)

        return ResumenImportacionEstadios(
            escritura=escritura,
            completos=completos,
            condicionales=condicionales,
            incompletos=incompletos,
            advertencias_pais=tuple(advertencias_pais),
        )

    @staticmethod
    def _mapear(venue: dict) -> dict[str, str]:
        id_externo = venue.get("id")
        capacidad = venue.get("capacity")
        return {
            "id_estadio": f"{_PREFIJO_ID}-{id_externo}" if id_externo is not None else "",
            "nombre": (venue.get("name") or "").strip(),
            "ciudad": (venue.get("city") or "").strip(),
            "pais": (venue.get("country") or "").strip(),
            "capacidad": str(capacidad) if isinstance(capacidad, int) else "",
            "tipo_superficie": (venue.get("surface") or "").strip(),
            # CONDICIONAL (docs/44 §3.6) -- confirmado ausente, nunca inventado
            "altitud_metros": "",
            "techado": "",
        }
