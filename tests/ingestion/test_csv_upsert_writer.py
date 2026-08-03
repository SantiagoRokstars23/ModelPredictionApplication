"""Pruebas de `CsvUpsertWriter` -- foco en el requisito explícito de
`DATA-012`: "Ejecutar dos veces el importador no debe duplicar registros".
Toda escritura ocurre en `tmp_path`, nunca en `data/processed/` real.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from app.ingestion.csv_upsert_writer import CsvUpsertWriter

COLUMNAS = ("id_estadio", "nombre", "ciudad")


def _leer(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def test_primer_upsert_crea_el_archivo_y_todas_las_filas_como_creadas(tmp_path: Path) -> None:
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")

    resumen = escritor.upsert(
        [
            {"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"},
            {"id_estadio": "EST-2", "nombre": "Anfield", "ciudad": "Liverpool"},
        ]
    )

    assert resumen.creados == 2
    assert resumen.actualizados == 0
    filas = _leer(ruta)
    assert len(filas) == 2
    assert {f["id_estadio"] for f in filas} == {"EST-1", "EST-2"}


def test_ejecutar_dos_veces_con_los_mismos_datos_no_duplica(tmp_path: Path) -> None:
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")
    filas = [{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"}]

    escritor.upsert(filas)
    resumen_segunda_pasada = escritor.upsert(filas)

    assert resumen_segunda_pasada.creados == 0
    assert resumen_segunda_pasada.actualizados == 0  # sin cambios reales -- no cuenta como actualización
    assert resumen_segunda_pasada.conservados == 1  # Caso 5 (DATA-012B): segunda ejecución no cambia nada
    assert len(_leer(ruta)) == 1


def test_preserva_valor_existente_cuando_el_nuevo_llega_vacio(tmp_path: Path) -> None:
    """Caso 1 (DATA-012B): CSV = 'Manchester', API = NULL -> se conserva 'Manchester'."""
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")
    escritor.upsert([{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"}])

    resumen = escritor.upsert([{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": ""}])

    assert resumen.conservados == 1
    assert resumen.actualizados == 0
    filas = _leer(ruta)
    assert filas[0]["ciudad"] == "Manchester"  # el valor nuevo vacío nunca sobrescribe uno válido


def test_completa_un_campo_antes_vacio_con_el_valor_nuevo(tmp_path: Path) -> None:
    """Caso 2 (DATA-012B): CSV = NULL, API = 'Manchester' -> se adopta 'Manchester'."""
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")
    escritor.upsert([{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": ""}])

    resumen = escritor.upsert([{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"}])

    assert resumen.actualizados == 1
    assert resumen.conservados == 0
    filas = _leer(ruta)
    assert filas[0]["ciudad"] == "Manchester"


def test_dry_run_no_escribe_ningun_archivo(tmp_path: Path) -> None:
    """Caso 3 (DATA-012B): --dry-run no debe escribir ningún archivo."""
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")

    resumen = escritor.upsert(
        [{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"}], simular=True
    )

    assert resumen.creados == 1
    assert not ruta.exists()


def test_segunda_pasada_con_un_valor_distinto_actualiza_sin_duplicar(tmp_path: Path) -> None:
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")
    escritor.upsert([{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"}])

    resumen = escritor.upsert(
        [{"id_estadio": "EST-1", "nombre": "Old Trafford Stadium", "ciudad": "Manchester"}]
    )

    assert resumen.creados == 0
    assert resumen.actualizados == 1
    filas = _leer(ruta)
    assert len(filas) == 1
    assert filas[0]["nombre"] == "Old Trafford Stadium"


def test_upsert_preserva_filas_ya_existentes_de_ejecuciones_anteriores(tmp_path: Path) -> None:
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")
    escritor.upsert([{"id_estadio": "EST-1", "nombre": "Old Trafford", "ciudad": "Manchester"}])

    escritor.upsert([{"id_estadio": "EST-2", "nombre": "Anfield", "ciudad": "Liverpool"}])

    filas = _leer(ruta)
    assert {f["id_estadio"] for f in filas} == {"EST-1", "EST-2"}


def test_fila_con_clave_de_negocio_vacia_se_omite_como_advertencia(tmp_path: Path) -> None:
    ruta = tmp_path / "estadios.csv"
    escritor = CsvUpsertWriter(ruta, COLUMNAS, clave_negocio="id_estadio")

    resumen = escritor.upsert([{"id_estadio": "", "nombre": "Sin ID", "ciudad": "Nowhere"}])

    assert resumen.omitidos == 1
    assert resumen.creados == 0
    assert len(resumen.advertencias) == 1
    assert not ruta.exists() or _leer(ruta) == []


def test_clave_de_negocio_debe_estar_entre_las_columnas_declaradas(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="clave de negocio"):
        CsvUpsertWriter(tmp_path / "x.csv", COLUMNAS, clave_negocio="no_existe")
