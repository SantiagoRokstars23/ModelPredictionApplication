"""Pruebas de `JugadoresImporter` -- fixtures basadas en los objetos reales
de Neymar (`/players`, `DATA-010A` §3.20) y de la plantilla del Manchester
United (`/players/squads`, `DATA-010A` §3.16).
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.ingestion.jugadores_importer import JugadoresImporter
from tests.ingestion.fakes import FakeApiFootballClient

_RESPUESTA_SQUAD = {
    "get": "players/squads",
    "errors": [],
    "response": [
        {
            "team": {"id": 33, "name": "Manchester United"},
            "players": [
                {"id": 276, "name": "Neymar", "age": 28, "number": 10, "position": "Attacker"},
            ],
        }
    ],
}

_RESPUESTA_PERFIL_NEYMAR = {
    "get": "players",
    "errors": [],
    "response": [
        {
            "player": {
                "id": 276,
                "name": "Neymar",
                "firstname": "Neymar",
                "lastname": "da Silva Santos Junior",
                "age": 28,
                "birth": {"date": "1992-02-05", "place": "Mogi das Cruzes", "country": "Brazil"},
                "nationality": "Brazil",
                "height": "175 cm",
                "weight": "68 kg",
                "injured": False,
            },
            "statistics": [{"team": {"id": 33, "name": "Manchester United"}}],
        }
    ],
}


def _leer(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def _cliente_completo() -> FakeApiFootballClient:
    return FakeApiFootballClient(
        {
            ("/players/squads", (("team", 33),)): _RESPUESTA_SQUAD,
            ("/players", (("id", 276), ("season", 2024))): _RESPUESTA_PERFIL_NEYMAR,
        }
    )


def test_importa_un_jugador_completo(tmp_path: Path) -> None:
    importer = JugadoresImporter(_cliente_completo(), data_dir=tmp_path, pausa_segundos=0)

    resumen = importer.importar(team_id_externo=33, id_seleccion="ARG", temporada=2024)

    assert resumen.escritura.creados == 1
    assert resumen.incompletos == 0
    # pie_habil no tiene fuente -> CONDICIONAL, nunca COMPLETO con las fuentes actuales
    assert resumen.condicionales == 1

    filas = _leer(tmp_path / "jugadores.csv")
    assert filas[0]["id_jugador"] == "JUG-276"
    assert filas[0]["nombre_completo"] == "Neymar da Silva Santos Junior"
    assert filas[0]["fecha_nacimiento"] == "1992-02-05"
    assert filas[0]["posicion_principal"] == "Attacker"
    assert filas[0]["altura_cm"] == "175"
    assert filas[0]["pie_habil"] == ""  # NO DISPONIBLE -- nunca inventado
    assert filas[0]["id_seleccion"] == "ARG"
    assert filas[0]["club_actual"] == "Manchester United"
    assert filas[0]["activo_seleccion"] == "true"


def test_perfil_no_disponible_no_detiene_el_resto_de_la_plantilla(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient(
        {("/players/squads", (("team", 33),)): _RESPUESTA_SQUAD}
        # sin respuesta configurada para /players -> FakeApiFootballClient lanza ApiFootballError,
        # que _obtener_perfil debe capturar y tratar como perfil vacío
    )
    importer = JugadoresImporter(cliente, data_dir=tmp_path, pausa_segundos=0)

    resumen = importer.importar(team_id_externo=33, id_seleccion="ARG", temporada=2024)

    # sin perfil, faltan nombre_completo/fecha_nacimiento (OBLIGATORIO) -> INCOMPLETO, no una excepción
    assert resumen.incompletos == 1
    assert resumen.escritura.creados == 0


def test_id_seleccion_vacio_lanza_error_explicito(tmp_path: Path) -> None:
    import pytest

    importer = JugadoresImporter(_cliente_completo(), data_dir=tmp_path, pausa_segundos=0)
    with pytest.raises(ValueError, match="id_seleccion"):
        importer.importar(team_id_externo=33, id_seleccion="  ", temporada=2024)


def test_ejecutar_dos_veces_no_duplica(tmp_path: Path) -> None:
    importer = JugadoresImporter(_cliente_completo(), data_dir=tmp_path, pausa_segundos=0)

    importer.importar(team_id_externo=33, id_seleccion="ARG", temporada=2024)
    resumen_segunda_vez = importer.importar(team_id_externo=33, id_seleccion="ARG", temporada=2024)

    assert resumen_segunda_vez.escritura.creados == 0
    assert resumen_segunda_vez.escritura.actualizados == 0
    assert len(_leer(tmp_path / "jugadores.csv")) == 1
