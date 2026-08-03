"""`SeleccionesImporter` -- construye `selecciones.csv` a partir de
`GET /teams` de API-Football (`docs/43-Pipeline-de-Ingesta.md` §6.2).

## Brecha de evidencia heredada, no resuelta aquí

`docs/43` §6.2 y `docs/44` (que solo clasificó los 7 archivos exigidos
explícitamente por su brief, sin incluir `selecciones.csv`) ya marcaron el
shape de respuesta de `/teams` como **"pendiente de confirmación en la
primera implementación"** -- ni `FII-003` ni `DATA-010A` leyeron esa respuesta
campo a campo contra la documentación oficial (a diferencia de `/players`,
`/venues`, `/fixtures`, que sí se verificaron con evidencia directa). Esta
misión (`DATA-012`) es esa primera implementación, pero **no tuvo una
credencial real de API-Football disponible** para ejecutar la llamada y
cerrar la brecha con evidencia -- se construye este módulo contra el shape
público y ampliamente estable de `/teams` (`{"team": {id, name, code,
country, founded, national, logo}, "venue": {...}}`), documentado aquí
explícitamente como una **suposición no verificada en esta sesión**, no como
un hecho confirmado. El mapeo es deliberadamente defensivo (`dict.get(...)`,
nunca acceso directo `["clave"]`) precisamente por esta incertidumbre: un
campo ausente se traduce en `INCOMPLETO`/`CONDICIONAL`, nunca en una
excepción no controlada ni en un valor inventado.

## Clasificación aplicada (extensión de `docs/44` §2 a `selecciones.csv`)

`docs/44` no clasificó `selecciones.csv` porque su propio brief (`GOV-003`)
no lo exigió -- este módulo aplica la misma regla ya definida en `docs/44` §2
a los 8 campos de `docs/33` §4.1, sin reabrir esa misión:

| Campo | Clasificación | Razón |
|---|---|---|
| `nombre_pais` | OBLIGATORIO | Fuente confirmada (`FII-003` §3.3) |
| `nombre_federacion`, `confederacion`, `ranking_fifa_actual`, `ranking_fifa_fecha` | CONDICIONAL | `docs/33` los declara obligatorios; sin fuente confirmada hoy (`FII-003` §3.3) -- quedan vacíos, nunca inventados |
| `seleccionador_actual` | OPCIONAL, no implementado en esta versión | Fuente existe (`GET /coachs`, `docs/43` §6.2) pero requiere una llamada adicional por selección -- decisión deliberada de alcance mínimo para `DATA-012`, documentada en el cierre de la misión, no una omisión silenciosa |
| `activa` | DERIVADO | `True` si la selección aparece en la respuesta de `/teams` para el país consultado -- no existe un campo booleano directo confirmado |

## Corrección real (`DATA-012A`, primera ejecución contra la API real)

`national=True` **no identifica de forma única** a la selección absoluta
masculina -- confirmado con evidencia directa contra la API real (no
anticipado por ninguna misión anterior, incluida la "suposición no
verificada" de arriba): `/teams?country=Spain` devuelve, además de `{"name":
"Spain", "code": "ESP", "national": true}`, al menos `{"name": "Spain W",
"code": null, "national": true}` (selección femenina) y otra entrada
adicional con `national: true` cuyo `code` (`"SPA"`) sí cumplía el formato de
3 letras -- sin filtrar, esta última se importaba como una segunda selección
espuria. `_es_seleccion_absoluta_masculina` restringe el filtro a la única
entrada cuyo `team.name` coincide exactamente (sin distinguir mayúsculas) con
el país consultado -- la selección femenina/juvenil/futsal nunca coincide con
ese nombre, quedan excluidas sin necesidad de conocer de antemano cada
variante posible.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from app.ingestion.api_football_client import ApiFootballClientProtocol, ApiFootballError
from app.ingestion.calidad import CalidadRegistro, evaluar_calidad
from app.ingestion.csv_upsert_writer import CsvUpsertWriter, ResumenEscritura
from app.ingestion.valores import normalizar_codigo_iso3

logger = logging.getLogger(__name__)

COLUMNAS = (
    "id_seleccion",
    "nombre_pais",
    "nombre_federacion",
    "confederacion",
    "ranking_fifa_actual",
    "ranking_fifa_fecha",
    "seleccionador_actual",
    "activa",
)
CAMPOS_OBLIGATORIOS = ("id_seleccion", "nombre_pais")
CAMPOS_CONDICIONALES = (
    "nombre_federacion",
    "confederacion",
    "ranking_fifa_actual",
    "ranking_fifa_fecha",
)
_ARCHIVO = "selecciones.csv"


def _es_seleccion_absoluta_masculina(equipo: dict, pais: str) -> bool:
    """`national=True` no basta -- un país puede tener varias entradas con
    ese valor (selección femenina, categorías juveniles, futsal; ver
    docstring del módulo, hallazgo de `DATA-012A`). Este importador cubre
    únicamente la selección absoluta masculina, identificada porque su
    `team.name` coincide exactamente (sin distinguir mayúsculas) con el país
    consultado -- las demás variantes nunca coinciden con ese nombre.
    """
    nombre = (equipo.get("name") or "").strip().casefold()
    return equipo.get("national") is True and nombre == pais.strip().casefold()


@dataclass(frozen=True)
class ResumenImportacionSelecciones:
    escritura: ResumenEscritura
    completos: int = 0
    condicionales: int = 0
    incompletos: int = 0
    filas_incompletas: tuple[str, ...] = field(default_factory=tuple)


class SeleccionesImporter:
    """Importa selecciones nacionales, un país a la vez, vía
    `GET /teams?country={pais}`.
    """

    def __init__(self, cliente: ApiFootballClientProtocol, data_dir: Path | None = None) -> None:
        self._cliente = cliente
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def importar(self, paises: list[str], dry_run: bool = False) -> ResumenImportacionSelecciones:
        """Un país sin ningún equipo con `national=True` en la respuesta no
        produce ninguna fila -- nunca se inventa una selección para un país
        sin cobertura confirmada en la fuente.

        `dry_run=True` (`DATA-012B` §4): consulta la API igual, pero no
        escribe `selecciones.csv` -- delega en `CsvUpsertWriter.upsert(...,
        simular=True)`.
        """
        filas: list[dict[str, str]] = []
        completos = 0
        condicionales = 0
        incompletos = 0
        filas_incompletas: list[str] = []

        for pais in paises:
            try:
                payload = self._cliente.get("/teams", {"country": pais})
            except ApiFootballError as exc:
                logger.error("No se pudo consultar /teams para '%s': %s", pais, exc)
                incompletos += 1
                filas_incompletas.append(pais)
                continue

            equipos_nacionales = [
                entrada
                for entrada in payload.get("response", [])
                if _es_seleccion_absoluta_masculina((entrada.get("team") or {}), pais)
            ]
            if not equipos_nacionales:
                logger.warning(
                    "'/teams?country=%s' no devolvió ningún equipo nacional -- se omite, "
                    "nunca se inventa una selección.",
                    pais,
                )
                continue

            for entrada in equipos_nacionales:
                fila = self._mapear(entrada)
                resultado = evaluar_calidad(fila, CAMPOS_OBLIGATORIOS, CAMPOS_CONDICIONALES)
                if resultado.calidad is CalidadRegistro.INCOMPLETO:
                    incompletos += 1
                    filas_incompletas.append(pais)
                    logger.error(
                        "Selección de '%s' omitida (INCOMPLETO): faltan %s",
                        pais,
                        resultado.campos_obligatorios_faltantes,
                    )
                    continue
                if resultado.calidad is CalidadRegistro.CONDICIONAL:
                    condicionales += 1
                else:
                    completos += 1
                filas.append(fila)

        escritura = CsvUpsertWriter(
            self._data_dir / _ARCHIVO, COLUMNAS, clave_negocio="id_seleccion"
        ).upsert(filas, simular=dry_run)

        return ResumenImportacionSelecciones(
            escritura=escritura,
            completos=completos,
            condicionales=condicionales,
            incompletos=incompletos,
            filas_incompletas=tuple(filas_incompletas),
        )

    @staticmethod
    def _mapear(entrada: dict) -> dict[str, str]:
        equipo = entrada.get("team") or {}

        id_seleccion = normalizar_codigo_iso3(equipo.get("code"))
        nombre_pais = (equipo.get("name") or equipo.get("country") or "").strip()

        return {
            "id_seleccion": id_seleccion or "",
            "nombre_pais": nombre_pais,
            # CONDICIONAL (docs/44 §2, extendido) -- sin fuente confirmada, nunca inventados
            "nombre_federacion": "",
            "confederacion": "",
            "ranking_fifa_actual": "",
            "ranking_fifa_fecha": "",
            # OPCIONAL, no implementado en esta versión (ver docstring del módulo)
            "seleccionador_actual": "",
            # DERIVADO: aparece en /teams para el país consultado => activa
            "activa": "true",
        }
