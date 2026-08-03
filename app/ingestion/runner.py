"""Runner oficial de ingestión (`DATA-012B` §3) -- único punto de entrada de
línea de comandos soportado para ejecutar `SeleccionesImporter`,
`EstadiosImporter` y `JugadoresImporter` contra la API real de API-Football.
Reemplaza cualquier script temporal: `DATA-012A` (primera ejecución real)
debe usar este runner, no un script ad-hoc.

## Uso

    python -m app.ingestion.runner --paises Argentina España --dry-run
    python -m app.ingestion.runner --paises Argentina --entidad selecciones
    python -m app.ingestion.runner --paises Argentina --data-dir ruta/a/copia-de-trabajo

`--data-dir` permite apuntar a una copia de trabajo en lugar de
`data/processed/selecciones-nacionales/` real -- es el mecanismo que
`DATA-012A` necesita para validar antes de escribir sobre datos reales
(hallazgo de esa preparación), sin que este módulo tenga que saber nada sobre
esa decisión operativa.

## Descubrimiento de IDs externos

`EstadiosImporter`/`JugadoresImporter` requieren `venue.id`/`team.id` de
API-Football, que `SeleccionesImporter` no expone (solo produce
`id_seleccion`, la clave interna). Este runner resuelve esos IDs con la misma
llamada `GET /teams?country={pais}` que ya usa `SeleccionesImporter` --
`_descubrir_seleccion_nacional` no reimplementa ninguna regla de calidad ni
de mapeo de columnas de ningún CSV, solo lee los IDs externos y deriva
`id_seleccion` con la misma utilidad compartida
(`app/ingestion/valores.py::normalizar_codigo_iso3`) que ya usa
`SeleccionesImporter`. No es un importador nuevo -- no escribe ningún CSV por
sí mismo, delega siempre en los tres importadores ya existentes.
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from app.config.settings import API_FOOTBALL_KEY
from app.ingestion.api_football_client import (
    ApiFootballClient,
    ApiFootballClientProtocol,
    ApiFootballError,
)
from app.ingestion.csv_upsert_writer import ResumenEscritura
from app.ingestion.estadios_importer import EstadiosImporter
from app.ingestion.jugadores_importer import JugadoresImporter
from app.ingestion.selecciones_importer import SeleccionesImporter
from app.ingestion.valores import normalizar_codigo_iso3

logger = logging.getLogger(__name__)

ENTIDADES_DISPONIBLES = ("selecciones", "estadios", "jugadores")


@dataclass(frozen=True)
class SeleccionNacionalDescubierta:
    id_seleccion: str
    team_id_externo: int
    venue_id_externo: int | None


def _descubrir_seleccion_nacional(
    cliente: ApiFootballClientProtocol, pais: str
) -> SeleccionNacionalDescubierta | None:
    """`None` si `/teams?country={pais}` no devuelve ningún equipo nacional,
    o si el equipo nacional encontrado no tiene un `code`/`id` utilizable --
    nunca se inventa un ID externo para poder continuar.
    """
    try:
        payload = cliente.get("/teams", {"country": pais})
    except ApiFootballError as exc:
        logger.error("No se pudo consultar /teams para '%s': %s", pais, exc)
        return None

    for entrada in payload.get("response", []):
        equipo = entrada.get("team") or {}
        if equipo.get("national") is not True:
            continue

        id_seleccion = normalizar_codigo_iso3(equipo.get("code"))
        team_id = equipo.get("id")
        if id_seleccion is None or team_id is None:
            logger.warning(
                "Equipo nacional de '%s' sin 'code' de 3 letras o sin 'id' -- "
                "no se puede resolver para Estadios/Jugadores.",
                pais,
            )
            return None

        venue = entrada.get("venue") or {}
        return SeleccionNacionalDescubierta(
            id_seleccion=id_seleccion,
            team_id_externo=team_id,
            venue_id_externo=venue.get("id"),
        )

    logger.warning("'/teams?country=%s' no devolvió ningún equipo nacional.", pais)
    return None


def _sumar(a: ResumenEscritura, b: ResumenEscritura) -> ResumenEscritura:
    return ResumenEscritura(
        creados=a.creados + b.creados,
        actualizados=a.actualizados + b.actualizados,
        conservados=a.conservados + b.conservados,
        omitidos=a.omitidos + b.omitidos,
        advertencias=a.advertencias + b.advertencias,
        errores=a.errores + b.errores,
    )


def ejecutar(
    paises: list[str],
    entidades: list[str],
    cliente: ApiFootballClientProtocol,
    dry_run: bool = False,
    data_dir: Path | None = None,
    temporada: int | None = None,
    pausa_jugadores_segundos: float | None = None,
) -> dict[str, ResumenEscritura]:
    """Orquesta los tres importadores ya existentes en el orden de capas de
    `docs/43` §3 (Selecciones/Estadios en Capa 0, Jugadores en Capa 1) -- no
    implementa ninguna entidad nueva, solo decide con qué parámetros llamar a
    cada importador.

    `pausa_jugadores_segundos`: `None` (default) deja que `JugadoresImporter`
    use su propia pausa por defecto (`_PAUSA_ENTRE_LLAMADAS_SEGUNDOS`, límite
    por minuto descubierto en `DATA-012A`) -- las pruebas pasan `0` para no
    ralentizar la suite con dobles de prueba que nunca golpean la red real.
    """
    temporada = temporada or date.today().year
    resultados: dict[str, ResumenEscritura] = {}

    if "selecciones" in entidades:
        resumen = SeleccionesImporter(cliente, data_dir=data_dir).importar(paises, dry_run=dry_run)
        resultados["selecciones"] = resumen.escritura

    descubiertas: list[SeleccionNacionalDescubierta] = []
    if "estadios" in entidades or "jugadores" in entidades:
        for pais in paises:
            descubierta = _descubrir_seleccion_nacional(cliente, pais)
            if descubierta is not None:
                descubiertas.append(descubierta)

    if "estadios" in entidades:
        ids_venue = [
            d.venue_id_externo for d in descubiertas if d.venue_id_externo is not None
        ]
        resumen = EstadiosImporter(cliente, data_dir=data_dir).importar(ids_venue, dry_run=dry_run)
        resultados["estadios"] = resumen.escritura

    if "jugadores" in entidades:
        kwargs_pausa = (
            {} if pausa_jugadores_segundos is None else {"pausa_segundos": pausa_jugadores_segundos}
        )
        acumulado = ResumenEscritura()
        for descubierta in descubiertas:
            resumen = JugadoresImporter(cliente, data_dir=data_dir, **kwargs_pausa).importar(
                team_id_externo=descubierta.team_id_externo,
                id_seleccion=descubierta.id_seleccion,
                temporada=temporada,
                dry_run=dry_run,
            )
            acumulado = _sumar(acumulado, resumen.escritura)
        resultados["jugadores"] = acumulado

    return resultados


def _imprimir_resumen(entidad: str, resumen: ResumenEscritura) -> None:
    print(f"\n=== {entidad.capitalize()} ===")
    print(f"Creadas: {resumen.creados}")
    print(f"Actualizadas: {resumen.actualizados}")
    print(f"Conservadas: {resumen.conservados}")
    print(f"Omitidas: {resumen.omitidos}")
    print(f"Errores: {len(resumen.errores)}")
    for advertencia in resumen.advertencias:
        logger.warning(advertencia)
    for error in resumen.errores:
        logger.error(error)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m app.ingestion.runner",
        description=(
            "Runner oficial de ingestión (DATA-012B) -- ejecuta Selecciones/"
            "Estadios/Jugadores contra API-Football."
        ),
    )
    parser.add_argument(
        "--paises", nargs="+", required=True, help="Países a consultar, ej. Argentina España."
    )
    parser.add_argument(
        "--entidad",
        nargs="+",
        choices=ENTIDADES_DISPONIBLES,
        default=list(ENTIDADES_DISPONIBLES),
        help="Entidades a ejecutar (default: las tres).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula la ejecución -- calcula el resumen pero no escribe ningún archivo.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help=(
            "Directorio destino de los CSV (default: data/processed/selecciones-nacionales/ "
            "real). Usar una copia de trabajo para validar antes de escribir sobre datos reales."
        ),
    )
    parser.add_argument(
        "--temporada",
        type=int,
        default=None,
        help="Temporada/season para /players (default: año actual).",
    )
    parser.add_argument(
        "--pausa-jugadores",
        type=float,
        default=None,
        help=(
            "Segundos de pausa antes de cada llamada a /players (default: la de "
            "JugadoresImporter, ver DATA-012A -- límite por minuto de API-Football)."
        ),
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    cliente = ApiFootballClient(API_FOOTBALL_KEY)
    try:
        resultados = ejecutar(
            paises=args.paises,
            entidades=args.entidad,
            cliente=cliente,
            dry_run=args.dry_run,
            data_dir=args.data_dir,
            temporada=args.temporada,
            pausa_jugadores_segundos=args.pausa_jugadores,
        )
    finally:
        cliente.close()

    if args.dry_run:
        print("\n*** DRY RUN -- ningún archivo fue escrito ***")
    for entidad, resumen in resultados.items():
        _imprimir_resumen(entidad, resumen)


if __name__ == "__main__":
    main()
