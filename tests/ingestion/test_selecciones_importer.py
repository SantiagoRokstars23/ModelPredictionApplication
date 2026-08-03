"""Pruebas de `SeleccionesImporter` -- fixtures basadas en el shape público
de `/teams` (no verificado línea por línea contra la API real en ninguna
misión, ver docstring de `selecciones_importer.py`). Nunca toca
`data/processed/` real: siempre `tmp_path`.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.ingestion.calidad import CalidadRegistro, evaluar_calidad
from app.ingestion.selecciones_importer import (
    CAMPOS_CONDICIONALES,
    CAMPOS_OBLIGATORIOS,
    SeleccionesImporter,
)
from tests.ingestion.fakes import FakeApiFootballClient

_RESPUESTA_ARGENTINA = {
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
                "logo": "https://media.api-sports.io/football/teams/26.png",
            },
            "venue": {},
        }
    ],
}

_RESPUESTA_SIN_SELECCION_NACIONAL = {
    "get": "teams",
    "errors": [],
    "response": [
        {
            "team": {"id": 555, "name": "Boca Juniors", "code": None, "country": "Argentina", "national": False}
        }
    ],
}


def _leer(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def test_importa_una_seleccion_valida_como_condicional(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient({("/teams", (("country", "Argentina"),)): _RESPUESTA_ARGENTINA})
    importer = SeleccionesImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar(["Argentina"])

    assert resumen.escritura.creados == 1
    assert resumen.incompletos == 0
    # nombre_federacion/confederacion/ranking_fifa_* siguen sin fuente -> CONDICIONAL, no COMPLETO
    assert resumen.condicionales == 1
    assert resumen.completos == 0

    filas = _leer(tmp_path / "selecciones.csv")
    assert len(filas) == 1
    assert filas[0]["id_seleccion"] == "ARG"
    assert filas[0]["nombre_pais"] == "Argentina"
    assert filas[0]["nombre_federacion"] == ""  # CONDICIONAL -- nunca inventado
    assert filas[0]["activa"] == "true"


def test_pais_sin_equipo_nacional_no_produce_ninguna_fila(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient(
        {("/teams", (("country", "Argentina"),)): _RESPUESTA_SIN_SELECCION_NACIONAL}
    )
    importer = SeleccionesImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar(["Argentina"])

    assert resumen.escritura.creados == 0
    assert resumen.incompletos == 0
    assert not (tmp_path / "selecciones.csv").exists() or _leer(tmp_path / "selecciones.csv") == []


def test_codigo_de_equipo_invalido_produce_fila_incompleta(tmp_path: Path) -> None:
    respuesta = {
        "get": "teams",
        "errors": [],
        "response": [
            # "name" == país consultado -- pasa el filtro de selección absoluta
            # masculina (DATA-012A); lo que se prueba aquí es el código inválido.
            {"team": {"id": 1, "name": "X", "code": "ARGENTINA", "national": True}}
        ],
    }
    cliente = FakeApiFootballClient({("/teams", (("country", "X"),)): respuesta})
    importer = SeleccionesImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar(["X"])

    # "ARGENTINA" no tiene 3 letras -> id_seleccion no se puede derivar -> INCOMPLETO
    assert resumen.incompletos == 1
    assert resumen.escritura.creados == 0


def test_pais_con_varios_equipos_nacionales_solo_importa_la_seleccion_absoluta(
    tmp_path: Path,
) -> None:
    """Hallazgo real de `DATA-012A`: `/teams?country=Spain` devolvió, además
    de la selección absoluta ("Spain"/`ESP`), la femenina ("Spain W", sin
    código) ambas con `national=True` -- solo debe importarse la primera.
    """
    respuesta = {
        "get": "teams",
        "errors": [],
        "response": [
            {"team": {"id": 9, "name": "Spain", "code": "ESP", "national": True}},
            {"team": {"id": 1736, "name": "Spain W", "code": None, "national": True}},
        ],
    }
    cliente = FakeApiFootballClient({("/teams", (("country", "Spain"),)): respuesta})
    importer = SeleccionesImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar(["Spain"])

    assert resumen.escritura.creados == 1
    filas = _leer(tmp_path / "selecciones.csv")
    assert len(filas) == 1
    assert filas[0]["id_seleccion"] == "ESP"


def test_ejecutar_dos_veces_no_duplica(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient({("/teams", (("country", "Argentina"),)): _RESPUESTA_ARGENTINA})
    importer = SeleccionesImporter(cliente, data_dir=tmp_path)

    importer.importar(["Argentina"])
    resumen_segunda_vez = importer.importar(["Argentina"])

    assert resumen_segunda_vez.escritura.creados == 0
    assert resumen_segunda_vez.escritura.actualizados == 0
    assert len(_leer(tmp_path / "selecciones.csv")) == 1


def test_evaluar_calidad_directamente_sobre_los_campos_declarados_del_importador() -> None:
    fila_condicional = {
        "id_seleccion": "ARG",
        "nombre_pais": "Argentina",
        "nombre_federacion": "",
        "confederacion": "",
        "ranking_fifa_actual": "",
        "ranking_fifa_fecha": "",
    }
    resultado = evaluar_calidad(fila_condicional, CAMPOS_OBLIGATORIOS, CAMPOS_CONDICIONALES)
    assert resultado.calidad is CalidadRegistro.CONDICIONAL
    assert set(resultado.campos_condicionales_vacios) == set(CAMPOS_CONDICIONALES)
