"""`CsvPotencialOfensivoRepository` -- lectura real de las métricas de tiro
que exige Variable003 (Potencial Ofensivo), conforme a la especificación
oficial de `models/offensive-strength.md` §17-27 (`MODEL-009`).

Referencias revisadas antes de escribir este módulo: `docs/00-Project-
Tracker.md`, `models/offensive-strength.md` §20-22 (fuente de datos exacta,
fórmula, ventana temporal -- única autoridad matemática de esta misión),
`app/preparation/preparation.py` (BUILD-017 -- consumidor), `app/persistence/
preparation_repository.py` y `mu_gol_provider.py` (mismo patrón de lectura
transicional de CSV ya aceptado en este proyecto).

BUILD-018: el brief restringe las modificaciones a `app/preparation/
preparation.py` y "archivos auxiliares estrictamente necesarios" -- explícita
mente prohíbe modificar `Persistence`. Por eso este módulo vive dentro de
`app/preparation/` (el único paquete que esta misión puede modificar en
profundidad) en lugar de `app/persistence/`, aunque su función (leer CSV) es
idéntica en espíritu a `CsvPreparationRepository`/`HistoricalMuGolProvider`
(`BUILD-016`/`BUILD-017`) -- una futura misión sin esa restricción podría
consolidar ambos en `app/persistence/`, sin cambiar este `Protocol`.

## Qué NO hace este módulo

No calcula `Z`, `Φ` ni `P` -- esa aritmética pertenece a `VariablePreparation`
(`preparation.py`), que es quien implementa la fórmula de `models/offensive-
strength.md` §21. Este módulo únicamente localiza y agrupa datos ya
existentes en `data/processed/`, nunca `data/raw/`. No calcula ninguna otra
Variable Oficial, no ejecuta motores, no accede a `PredictionContext` ni al
Runtime. No aproxima, no interpola, no rellena filas faltantes -- un partido
sin estadística válida simplemente no entra en ninguna lista.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Protocol

_ARCHIVO_ESTADISTICAS = "estadisticas_partido.csv"
_ARCHIVO_PARTIDOS = "partidos.csv"
_ARCHIVO_TORNEOS = "torneos.csv"
_ARCHIVO_COMPETICIONES = "competiciones.csv"


class DatosPotencialOfensivoInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos. Mismo
    principio que `DatosHistoricosInconsistentes`/`DatosBaseConocimiento
    Inconsistentes` (`BUILD-016`/`BUILD-017`). `VariablePreparation` debe
    capturar esta excepción (nunca dejarla propagar sin control, conforme
    al brief de `BUILD-018`: "nunca lanzar excepciones que detengan
    VariablePreparation completo") y marcar `disponible=False`.
    """


@dataclass(frozen=True)
class MetricaPartido:
    """Una fila de `estadisticas_partido.csv` ya validada y unida a la
    fecha de su partido (`models/offensive-strength.md` §20-21) -- exactamente
    las tres métricas oficiales de V1, ninguna más.
    """

    fecha: date
    xg: float
    disparos_totales: float
    disparos_al_arco: float


@dataclass(frozen=True)
class MetricasOfensivas:
    """Resultado de una consulta: hasta `n` partidos más recientes del
    equipo (`x̄_i(equipo)`, `models/offensive-strength.md` §21) y la
    población de la competición en el mismo rango de fechas
    (`μ_i(competición)`/`σ_i(competición)`, misma sección).
    """

    equipo: list[MetricaPartido]
    poblacion_competicion: list[MetricaPartido]


class PotencialOfensivoRepositoryProtocol(Protocol):
    """Interfaz de lectura -- satisfecha por `CsvPotencialOfensivoRepository`."""

    def obtener_metricas_ofensivas(
        self, id_seleccion: str, competicion: str, n: int
    ) -> MetricasOfensivas | None:
        """Debe devolver `None` si la competición no se reconoce, o
        `MetricasOfensivas` con `equipo=[]` si la competición existe pero el
        equipo no tiene partidos válidos -- nunca debe inventar un partido.
        """
        ...

    def listar_selecciones(self, competicion: str) -> list[str]:
        """IMP-001 (`MODEL-018`): lista de `id_seleccion` con al menos una
        fila real en `estadisticas_partido.csv` dentro de esta competición --
        insumo para calcular `Z*_competición` (media histórica del z-score
        estandarizado), nunca para calcular `Z`/`Φ`/`P` (responsabilidad de
        `VariablePreparation`, ver docstring del módulo). Devuelve `[]` si la
        competición no se reconoce -- mismo criterio que `obtener_metricas_
        ofensivas`.
        """
        ...


class CsvPotencialOfensivoRepository:
    """Lee `estadisticas_partido.csv`, `partidos.csv`, `torneos.csv` y
    `competiciones.csv` de `data/processed/selecciones-nacionales/` --
    nunca `data/raw/`, nunca una fuente externa (ranking FIFA, Elo --
    explícitamente descartadas por `models/offensive-strength.md` §20).
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_metricas_ofensivas(
        self, id_seleccion: str, competicion: str, n: int
    ) -> MetricasOfensivas | None:
        id_competicion = self._resolver_id_competicion(competicion)
        if id_competicion is None:
            return None

        ids_torneo = self._torneos_de_competicion(id_competicion)
        if not ids_torneo:
            return None

        fechas_por_partido = self._indice_partidos_validos(ids_torneo)
        if not fechas_por_partido:
            return MetricasOfensivas(equipo=[], poblacion_competicion=[])

        equipo_todas: list[MetricaPartido] = []
        poblacion_todas: list[MetricaPartido] = []

        for fila in self._leer_csv(_ARCHIVO_ESTADISTICAS):
            try:
                id_partido = fila["id_partido"]
                fila_id_seleccion = fila["id_seleccion"]
                xg_raw = fila["xg"]
                disparos_totales_raw = fila["disparos_totales"]
                disparos_al_arco_raw = fila["disparos_al_arco"]
            except KeyError as exc:
                raise DatosPotencialOfensivoInconsistentes(
                    f"'{_ARCHIVO_ESTADISTICAS}' no tiene la columna esperada: {exc}."
                ) from exc

            fecha = fechas_por_partido.get(id_partido)
            if fecha is None:
                continue  # partido fuera de la competición solicitada, o no válido (sección "Fuente de datos")

            metrica = self._parsear_metrica(fecha, xg_raw, disparos_totales_raw, disparos_al_arco_raw)
            if metrica is None:
                continue  # fila con dato no numérico/negativo -- se descarta, no se inventa

            if fila_id_seleccion == id_seleccion:
                equipo_todas.append(metrica)
            poblacion_todas.append(metrica)

        if not equipo_todas:
            return MetricasOfensivas(equipo=[], poblacion_competicion=[])

        equipo_reciente = sorted(equipo_todas, key=lambda m: m.fecha, reverse=True)[:n]
        fecha_min = min(m.fecha for m in equipo_reciente)
        fecha_max = max(m.fecha for m in equipo_reciente)

        # "misma ventana temporal... para que la comparación sea contemporánea"
        # (models/offensive-strength.md §22) -- población acotada al rango de
        # fechas de los propios partidos recientes del equipo.
        poblacion = [m for m in poblacion_todas if fecha_min <= m.fecha <= fecha_max]

        return MetricasOfensivas(equipo=equipo_reciente, poblacion_competicion=poblacion)

    def listar_selecciones(self, competicion: str) -> list[str]:
        id_competicion = self._resolver_id_competicion(competicion)
        if id_competicion is None:
            return []

        ids_torneo = self._torneos_de_competicion(id_competicion)
        if not ids_torneo:
            return []

        fechas_por_partido = self._indice_partidos_validos(ids_torneo)
        if not fechas_por_partido:
            return []

        selecciones: set[str] = set()
        for fila in self._leer_csv(_ARCHIVO_ESTADISTICAS):
            try:
                id_partido = fila["id_partido"]
                id_seleccion = fila["id_seleccion"]
            except KeyError as exc:
                raise DatosPotencialOfensivoInconsistentes(
                    f"'{_ARCHIVO_ESTADISTICAS}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_partido not in fechas_por_partido:
                continue  # partido fuera de la competición solicitada, o no válido
            selecciones.add(id_seleccion)

        return sorted(selecciones)

    # -- Resolución de competición (mismo patrón que mu_gol_provider.py) -----

    def _resolver_id_competicion(self, competicion: str) -> str | None:
        objetivo = competicion.strip().lower()
        for fila in self._leer_csv(_ARCHIVO_COMPETICIONES):
            try:
                nombre = fila["nombre"]
                id_competicion = fila["id_competicion"]
            except KeyError as exc:
                raise DatosPotencialOfensivoInconsistentes(
                    f"'{_ARCHIVO_COMPETICIONES}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_competicion.strip().lower() == objetivo or nombre.strip().lower() == objetivo:
                return id_competicion
        return None

    def _torneos_de_competicion(self, id_competicion: str) -> set[str]:
        ids_torneo: set[str] = set()
        for fila in self._leer_csv(_ARCHIVO_TORNEOS):
            try:
                if fila["id_competicion"] == id_competicion:
                    ids_torneo.add(fila["id_torneo"])
            except KeyError as exc:
                raise DatosPotencialOfensivoInconsistentes(
                    f"'{_ARCHIVO_TORNEOS}' no tiene la columna esperada: {exc}."
                ) from exc
        return ids_torneo

    def _indice_partidos_validos(self, ids_torneo: set[str]) -> dict[str, date]:
        """`id_partido -> fecha`, solo para partidos de `ids_torneo` con
        goles válidos (proxy de "finalizado" ya usado en `CsvPreparation
        Repository`/`HistoricalMuGolProvider`, `estado_partido` no tiene
        ENUM formalizado en ningún documento -- no se asume un valor de
        texto no verificado) y fecha parseable.
        """
        indice: dict[str, date] = {}
        for fila in self._leer_csv(_ARCHIVO_PARTIDOS):
            try:
                id_partido = fila["id_partido"]
                id_torneo = fila["id_torneo"]
                fecha_raw = fila["fecha"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise DatosPotencialOfensivoInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_torneo not in ids_torneo:
                continue
            if not self._goles_validos(goles_local_raw, goles_visitante_raw):
                continue

            fecha = self._parsear_fecha(fecha_raw)
            if fecha is None:
                continue

            indice[id_partido] = fecha
        return indice

    @staticmethod
    def _goles_validos(goles_local_raw: str, goles_visitante_raw: str) -> bool:
        try:
            return int(goles_local_raw) >= 0 and int(goles_visitante_raw) >= 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _parsear_fecha(fecha_raw: Any) -> date | None:
        try:
            return date.fromisoformat(str(fecha_raw).strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _parsear_metrica(
        fecha: date, xg_raw: str, disparos_totales_raw: str, disparos_al_arco_raw: str
    ) -> MetricaPartido | None:
        try:
            xg = float(xg_raw)
            disparos_totales = float(disparos_totales_raw)
            disparos_al_arco = float(disparos_al_arco_raw)
        except (TypeError, ValueError):
            return None
        if xg < 0 or disparos_totales < 0 or disparos_al_arco < 0:
            return None
        return MetricaPartido(
            fecha=fecha, xg=xg, disparos_totales=disparos_totales, disparos_al_arco=disparos_al_arco
        )

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise DatosPotencialOfensivoInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc
