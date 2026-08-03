"""Pruebas del runner oficial de ingestión (`app/ingestion/runner.py`,
`DATA-012B` §3). Nunca toca `data/processed/` real -- siempre `tmp_path`, y
nunca golpea la red -- siempre `FakeApiFootballClient`.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.ingestion.runner import (
    SeleccionNacionalDescubierta,
    _descubrir_seleccion_nacional,
    ejecutar,
)
from tests.ingestion.fakes import FakeApiFootballClient

_RESPUESTA_TEAMS_ARGENTINA = {
    "get": "teams",
    "errors": [],
    "response": [
        {
            "team": {
                "id": 26,
                "name": "Argentina",
                "code": "ARG",
                "country": "Argentina",
                "national": True,
            },
            "venue": {"id": 1000, "name": "Estadio Monumental"},
        }
    ],
}

_RESPUESTA_VENUE = {
    "get": "venues",
    "errors": [],
    "response": [
        {
            "id": 1000,
            "name": "Estadio Monumental",
            "city": "Buenos Aires",
            "country": "Argentina",
            "capacity": 83214,
            "surface": "grass",
        }
    ],
}

_RESPUESTA_SQUAD = {
    "get": "players/squads",
    "errors": [],
    "response": [
        {
            "team": {"id": 26, "name": "Argentina"},
            "players": [{"id": 500, "name": "Jugador X", "position": "Attacker"}],
        }
    ],
}

_RESPUESTA_PERFIL = {
    "get": "players",
    "errors": [],
    "response": [
        {
            "player": {
                "id": 500,
                "firstname": "Jugador",
                "lastname": "X",
                "birth": {"date": "1995-01-01"},
                "height": "180 cm",
            },
            "statistics": [{"team": {"id": 26, "name": "Argentina"}}],
        }
    ],
}


def _cliente_completo() -> FakeApiFootballClient:
    return FakeApiFootballClient(
        {
            ("/teams", (("country", "Argentina"),)): _RESPUESTA_TEAMS_ARGENTINA,
            ("/venues", (("id", 1000),)): _RESPUESTA_VENUE,
            ("/players/squads", (("team", 26),)): _RESPUESTA_SQUAD,
            ("/players", (("id", 500), ("season", 2024))): _RESPUESTA_PERFIL,
        }
    )


def _leer(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def test_descubrir_seleccion_nacional_resuelve_ids_externos() -> None:
    cliente = FakeApiFootballClient({("/teams", (("country", "Argentina"),)): _RESPUESTA_TEAMS_ARGENTINA})

    descubierta = _descubrir_seleccion_nacional(cliente, "Argentina")

    assert descubierta == SeleccionNacionalDescubierta(
        id_seleccion="ARG", team_id_externo=26, venue_id_externo=1000
    )


def test_descubrir_seleccion_nacional_sin_equipo_nacional_devuelve_none() -> None:
    cliente = FakeApiFootballClient(
        {("/teams", (("country", "Nadie"),)): {"get": "teams", "errors": [], "response": []}}
    )

    assert _descubrir_seleccion_nacional(cliente, "Nadie") is None


def test_ejecutar_solo_selecciones_no_llama_a_teams_dos_veces_de_mas(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient({("/teams", (("country", "Argentina"),)): _RESPUESTA_TEAMS_ARGENTINA})

    resultados = ejecutar(
        paises=["Argentina"], entidades=["selecciones"], cliente=cliente, data_dir=tmp_path
    )

    assert set(resultados.keys()) == {"selecciones"}
    assert resultados["selecciones"].creados == 1
    assert _leer(tmp_path / "selecciones.csv")[0]["id_seleccion"] == "ARG"
    assert not (tmp_path / "estadios.csv").exists()
    assert not (tmp_path / "jugadores.csv").exists()


def test_ejecutar_las_tres_entidades_orquesta_el_descubrimiento_de_ids(tmp_path: Path) -> None:
    resultados = ejecutar(
        paises=["Argentina"],
        entidades=["selecciones", "estadios", "jugadores"],
        cliente=_cliente_completo(),
        data_dir=tmp_path,
        temporada=2024,
        pausa_jugadores_segundos=0,
    )

    assert resultados["selecciones"].creados == 1
    assert resultados["estadios"].creados == 1
    assert resultados["jugadores"].creados == 1
    assert _leer(tmp_path / "estadios.csv")[0]["id_estadio"] == "EST-1000"
    assert _leer(tmp_path / "jugadores.csv")[0]["id_seleccion"] == "ARG"


def test_dry_run_no_escribe_ningun_archivo(tmp_path: Path) -> None:
    resultados = ejecutar(
        paises=["Argentina"],
        entidades=["selecciones", "estadios", "jugadores"],
        cliente=_cliente_completo(),
        data_dir=tmp_path,
        temporada=2024,
        dry_run=True,
        pausa_jugadores_segundos=0,
    )

    assert resultados["selecciones"].creados == 1
    assert resultados["estadios"].creados == 1
    assert resultados["jugadores"].creados == 1
    assert not (tmp_path / "selecciones.csv").exists()
    assert not (tmp_path / "estadios.csv").exists()
    assert not (tmp_path / "jugadores.csv").exists()


def test_segunda_ejecucion_identica_no_cambia_nada(tmp_path: Path) -> None:
    """Caso 5 (DATA-012B), a nivel de runner: ejecutar dos veces con los
    mismos datos no debe producir ningún cambio real en la segunda pasada.
    """
    ejecutar(
        paises=["Argentina"],
        entidades=["selecciones", "estadios", "jugadores"],
        cliente=_cliente_completo(),
        data_dir=tmp_path,
        temporada=2024,
        pausa_jugadores_segundos=0,
    )

    resultados_segunda_vez = ejecutar(
        paises=["Argentina"],
        entidades=["selecciones", "estadios", "jugadores"],
        cliente=_cliente_completo(),
        data_dir=tmp_path,
        temporada=2024,
        pausa_jugadores_segundos=0,
    )

    for entidad in ("selecciones", "estadios", "jugadores"):
        assert resultados_segunda_vez[entidad].creados == 0
        assert resultados_segunda_vez[entidad].actualizados == 0
        assert resultados_segunda_vez[entidad].conservados == 1
