"""Pruebas de `EstadiosImporter` -- fixture basada en el objeto real de "Old
Trafford" verificado con evidencia directa en `DATA-010A` §3.18.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.ingestion.estadios_importer import COLUMNAS, EstadiosImporter
from tests.ingestion.fakes import FakeApiFootballClient

_RESPUESTA_OLD_TRAFFORD = {
    "get": "venues",
    "errors": [],
    "response": [
        {
            "id": 556,
            "name": "Old Trafford",
            "address": "Sir Matt Busby Way",
            "city": "Manchester",
            "country": "England",
            "capacity": 76212,
            "surface": "grass",
            "image": "https://media.api-sports.io/football/venues/556.png",
        }
    ],
}


def _leer(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def test_importa_un_estadio_valido_como_completo(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient({("/venues", (("id", 556),)): _RESPUESTA_OLD_TRAFFORD})
    importer = EstadiosImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar([556])

    assert resumen.escritura.creados == 1
    # nombre/ciudad/pais/capacidad/tipo_superficie: los 5 OBLIGATORIO con fuente -> COMPLETO
    # (altitud_metros/techado son CONDICIONAL, pero el registro solo se marca
    # CONDICIONAL si falta uno de ESOS dos campos, lo cual siempre ocurre hoy)
    assert resumen.condicionales == 1
    assert resumen.incompletos == 0

    filas = _leer(tmp_path / "estadios.csv")
    assert filas[0]["id_estadio"] == "EST-556"
    assert filas[0]["nombre"] == "Old Trafford"
    assert filas[0]["capacidad"] == "76212"
    assert filas[0]["altitud_metros"] == ""  # CONDICIONAL -- nunca inventado
    assert filas[0]["techado"] == ""


def test_estadio_sin_capacidad_queda_incompleto(tmp_path: Path) -> None:
    respuesta = {
        "get": "venues",
        "errors": [],
        "response": [
            {
                "id": 999,
                "name": "Estadio Sin Datos",
                "city": "Ciudad",
                "country": "País",
                "capacity": None,
                "surface": "grass",
            }
        ],
    }
    cliente = FakeApiFootballClient({("/venues", (("id", 999),)): respuesta})
    importer = EstadiosImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar([999])

    assert resumen.incompletos == 1
    assert resumen.escritura.creados == 0


def test_advertencia_de_pais_no_bloquea_la_importacion(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient({("/venues", (("id", 556),)): _RESPUESTA_OLD_TRAFFORD})
    importer = EstadiosImporter(cliente, data_dir=tmp_path, paises_conocidos=frozenset({"Argentina"}))

    resumen = importer.importar([556])

    assert resumen.escritura.creados == 1  # se importa igual
    assert len(resumen.advertencias_pais) == 1
    assert "England" in resumen.advertencias_pais[0]


def test_ejecutar_dos_veces_no_duplica(tmp_path: Path) -> None:
    cliente = FakeApiFootballClient({("/venues", (("id", 556),)): _RESPUESTA_OLD_TRAFFORD})
    importer = EstadiosImporter(cliente, data_dir=tmp_path)

    importer.importar([556])
    resumen_segunda_vez = importer.importar([556])

    assert resumen_segunda_vez.escritura.creados == 0
    assert resumen_segunda_vez.escritura.actualizados == 0
    assert resumen_segunda_vez.escritura.conservados == 1
    assert len(_leer(tmp_path / "estadios.csv")) == 1


def test_matching_por_nombre_y_pais_reutiliza_la_clave_existente_sin_duplicar(
    tmp_path: Path,
) -> None:
    """Caso 4 (DATA-012B): un estadio ya curado manualmente con clave
    secuencial (`EST-000001`) no debe duplicarse cuando la API lo devuelve
    con un `id_estadio` derivado distinto (`EST-556`) -- debe reconocerse por
    `(nombre, país)` normalizados y actualizar la fila ya existente.
    """
    ruta = tmp_path / "estadios.csv"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor_csv = csv.DictWriter(archivo, fieldnames=list(COLUMNAS))
        escritor_csv.writeheader()
        escritor_csv.writerow(
            {
                "id_estadio": "EST-000001",
                "nombre": "old trafford",  # variación de caso -- debe normalizar igual
                "ciudad": "Manchester",
                "pais": "England",
                "capacidad": "76212",
                "tipo_superficie": "grass",
                "altitud_metros": "",
                "techado": "",
            }
        )

    cliente = FakeApiFootballClient({("/venues", (("id", 556),)): _RESPUESTA_OLD_TRAFFORD})
    importer = EstadiosImporter(cliente, data_dir=tmp_path)

    resumen = importer.importar([556])

    filas = _leer(ruta)
    assert len(filas) == 1  # no se duplicó
    assert filas[0]["id_estadio"] == "EST-000001"  # se conservó la clave curada manualmente
    assert resumen.escritura.creados == 0
