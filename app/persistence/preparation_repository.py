"""`CsvPreparationRepository` -- lectura real de la Base de Conocimiento para
`VariablePreparation` (`app/preparation/preparation.py`, BUILD-017).

Referencias revisadas antes de escribir este módulo: `docs/00-Project-
Tracker.md`, `docs/03-Variables.md`, `docs/16-Contrato-Oficial-de-Variables.md`,
`docs/17-Matriz-de-Consumo-de-Variables.md`, `docs/30-Contrato-Oficial-del-
Prediction-Context.md` §4.3, `docs/35-Arquitectura-Oficial-del-Proyecto-
Python.md` (matriz de dependencias), `app/preparation/preparation.py`
(BUILD-006 -- declara `PreparationRepositoryProtocol`, sin implementación
real hasta ahora), `app/persistence/mu_gol_provider.py` (BUILD-016 -- mismo
patrón de lectura transicional de CSV, ya aceptado en este proyecto).

BUILD-017: primera implementación real del repositorio que `BUILD-006` ya
anticipaba ("se declara aquí, sin implementación real, para que una misión
futura... tenga un punto de inyección ya definido"). A diferencia de
`HistoricalMuGolProvider` (invocado dentro del camino crítico de `Engine03`),
este repositorio se invoca desde `app/preparation`, que `docs/35` ya declara
explícitamente como dependiente de `app/persistence` -- sin ninguna tensión
arquitectónica que documentar (a diferencia de `mu_gol_provider.py`).

BUILD-021: agrega `resolver_id_torneo`/`partidos_del_torneo`, necesarios
para Variable002 (`models/rendimiento-torneo.md`, `MODEL-012`) -- a
diferencia de Variable003/004/010 (que resuelven una *competición* completa,
o un par de selecciones), Variable002 necesita el `id_torneo` **específico**
del partido a predecir, nunca usado directamente por ninguna misión
anterior. El brief de `BUILD-021` autoriza explícitamente "Uso del
CsvPreparationRepository" (a diferencia de `BUILD-019`, que restringía las
modificaciones únicamente a `preparation.py`) -- por eso esta extensión vive
aquí, no duplicada dentro de `preparation.py`.

## Por qué CSV directo, no SQLAlchemy (mismo razonamiento que BUILD-016)

La Base de Conocimiento de Selecciones Nacionales vive hoy en
`data/processed/selecciones-nacionales/*.csv` -- no existe ninguna carga
real hacia PostgreSQL (`app/models` define las tablas, pero ninguna misión
las ha poblado). Crear una `Session`/`Engine` propios está explícitamente
prohibido por el brief de `BUILD-017` ("No puede: crear Engines SQLAlchemy;
crear Sessions; abrir conexiones propias") -- y usar `BaseRepository` no
aportaría nada hoy, porque no hay filas en la base de datos. Se lee CSV
directamente, mismo carácter transicional ya documentado y aceptado en
`mu_gol_provider.py` -- una futura migración hacia repositorios SQLAlchemy
reales sería consistente con esta misma interfaz (`PreparationRepositoryProtocol`,
en `app/preparation/preparation.py`), sin cambiarla.

## Qué NO hace este módulo

No calcula ninguna Variable Oficial -- solo expone datos ya existentes de
`data/processed/`, tal como los declara `docs/15` ("los motores... nunca
conocen si los datos provienen de CSV" -- principio heredado aquí también
para `VariablePreparation`, que consume esta interfaz sin conocer que hay
CSV detrás). No accede a `data/raw/`. No ejecuta motores, no calibra nada,
no infiere ni interpola datos faltantes -- una fila no encontrada siempre
se traduce en `None`, nunca en un valor inventado.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

_ARCHIVO_SELECCIONES = "selecciones.csv"
_ARCHIVO_ESTADIOS = "estadios.csv"
_ARCHIVO_PARTIDOS = "partidos.csv"
_ARCHIVO_TORNEOS = "torneos.csv"


class DatosBaseConocimientoInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado en silencio como "sin evidencia" (`None`/lista vacía). Mismo
    principio que `DatosHistoricosInconsistentes` (`mu_gol_provider.py`,
    BUILD-016).
    """


@dataclass(frozen=True)
class SeleccionInfo:
    """Subconjunto de `selecciones.csv` -- solo los campos que
    `VariablePreparation` necesita hoy (Localía, Historial Directo).
    """

    id_seleccion: str
    nombre_pais: str


@dataclass(frozen=True)
class EstadioInfo:
    """Subconjunto de `estadios.csv` -- solo el país, necesario para
    resolver Localía.
    """

    id_estadio: str
    pais: str


@dataclass(frozen=True)
class ResultadoHistorico:
    """Una fila de `partidos.csv` ya finalizada (goles válidos), tal como
    la necesita el cálculo de Historial Directo (Variable010).
    """

    id_seleccion_local: str
    id_seleccion_visitante: str
    goles_local: int
    goles_visitante: int


@dataclass(frozen=True)
class PartidoTorneo:
    """Una fila de `partidos.csv` ya finalizada (goles válidos), con fecha
    e identificador propio -- lo que necesita Variable002 (`models/
    rendimiento-torneo.md` §5-6, `MODEL-012`, `BUILD-021`) para filtrar los
    partidos ya jugados de un `id_torneo` específico y excluir el partido
    que se está prediciendo.
    """

    id_partido: str
    fecha: date
    id_seleccion_local: str
    id_seleccion_visitante: str
    goles_local: int
    goles_visitante: int


class CsvPreparationRepository:
    """Implementación real de `PreparationRepositoryProtocol`
    (`app/preparation/preparation.py`). Lee `selecciones.csv`,
    `estadios.csv` y `partidos.csv` de `data/processed/selecciones-
    nacionales/` -- nunca `data/raw/`, nunca una fuente externa.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_seleccion(self, identificador: str) -> SeleccionInfo | None:
        """Busca por `id_seleccion` o `nombre_pais` (indistintamente, ver
        `docs/25` §1: "id_seleccion o nombre, resuelto contra
        selecciones.csv") -- nunca inventa una selección no encontrada.
        """
        objetivo = identificador.strip().lower()
        for fila in self._leer_csv(_ARCHIVO_SELECCIONES):
            try:
                id_seleccion = fila["id_seleccion"]
                nombre_pais = fila["nombre_pais"]
            except KeyError as exc:
                raise DatosBaseConocimientoInconsistentes(
                    f"'{_ARCHIVO_SELECCIONES}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_seleccion.strip().lower() == objetivo or nombre_pais.strip().lower() == objetivo:
                return SeleccionInfo(id_seleccion=id_seleccion, nombre_pais=nombre_pais)
        return None

    def obtener_estadio(self, identificador: str) -> EstadioInfo | None:
        """Busca por `id_estadio` o `nombre` -- nunca inventa un estadio no
        encontrado.
        """
        objetivo = identificador.strip().lower()
        for fila in self._leer_csv(_ARCHIVO_ESTADIOS):
            try:
                id_estadio = fila["id_estadio"]
                nombre = fila["nombre"]
                pais = fila["pais"]
            except KeyError as exc:
                raise DatosBaseConocimientoInconsistentes(
                    f"'{_ARCHIVO_ESTADIOS}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_estadio.strip().lower() == objetivo or nombre.strip().lower() == objetivo:
                return EstadioInfo(id_estadio=id_estadio, pais=pais)
        return None

    def historial_enfrentamientos(
        self, id_seleccion_a: str, id_seleccion_b: str
    ) -> list[ResultadoHistorico]:
        """Todos los partidos ya finalizados (goles válidos, no negativos)
        entre las dos selecciones, en cualquier orden local/visitante --
        base de `Historial Directo` (Variable010, `docs/16`: "diferencia
        neta de victorias"). Lista vacía si no hay historial -- nunca un
        resultado inventado.
        """
        objetivo = {id_seleccion_a, id_seleccion_b}
        resultados: list[ResultadoHistorico] = []
        for fila in self._leer_csv(_ARCHIVO_PARTIDOS):
            try:
                local = fila["id_seleccion_local"]
                visitante = fila["id_seleccion_visitante"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise DatosBaseConocimientoInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS}' no tiene la columna esperada: {exc}."
                ) from exc

            if {local, visitante} != objetivo:
                continue

            goles = self._parsear_goles(goles_local_raw, goles_visitante_raw)
            if goles is None:
                continue  # partido no finalizado o dato corrupto -- se descarta, no se inventa

            resultados.append(
                ResultadoHistorico(
                    id_seleccion_local=local,
                    id_seleccion_visitante=visitante,
                    goles_local=goles[0],
                    goles_visitante=goles[1],
                )
            )
        return resultados

    def resolver_id_torneo(self, torneo: str) -> str | None:
        """Busca por `id_torneo` o `edicion` (`torneos.csv` no tiene columna
        `nombre` propia, a diferencia de `selecciones.csv`/`competiciones.csv`
        -- mismo patrón de robustez de búsqueda dual, adaptado a las columnas
        realmente existentes). Nunca inventa un torneo no encontrado.
        """
        objetivo = torneo.strip().lower()
        for fila in self._leer_csv(_ARCHIVO_TORNEOS):
            try:
                id_torneo = fila["id_torneo"]
                edicion = fila["edicion"]
            except KeyError as exc:
                raise DatosBaseConocimientoInconsistentes(
                    f"'{_ARCHIVO_TORNEOS}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_torneo.strip().lower() == objetivo or edicion.strip().lower() == objetivo:
                return id_torneo
        return None

    def partidos_del_torneo(self, id_torneo: str) -> list[PartidoTorneo]:
        """Todos los partidos ya finalizados (goles válidos, fecha
        parseable) de un `id_torneo` específico -- base de Variable002
        (`models/rendimiento-torneo.md` §5-6). Lista vacía si el torneo no
        tiene partidos válidos -- nunca inventa uno.
        """
        resultados: list[PartidoTorneo] = []
        for fila in self._leer_csv(_ARCHIVO_PARTIDOS):
            try:
                fila_id_torneo = fila["id_torneo"]
                id_partido = fila["id_partido"]
                local = fila["id_seleccion_local"]
                visitante = fila["id_seleccion_visitante"]
                fecha_raw = fila["fecha"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise DatosBaseConocimientoInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS}' no tiene la columna esperada: {exc}."
                ) from exc

            if fila_id_torneo != id_torneo:
                continue

            goles = self._parsear_goles(goles_local_raw, goles_visitante_raw)
            if goles is None:
                continue  # partido no finalizado o dato corrupto -- se descarta, no se inventa

            fecha = self._parsear_fecha(fecha_raw)
            if fecha is None:
                continue

            resultados.append(
                PartidoTorneo(
                    id_partido=id_partido,
                    fecha=fecha,
                    id_seleccion_local=local,
                    id_seleccion_visitante=visitante,
                    goles_local=goles[0],
                    goles_visitante=goles[1],
                )
            )
        return resultados

    # -- Lectura de CSV (data/processed/ únicamente, nunca data/raw/) -------

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise DatosBaseConocimientoInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc

    @staticmethod
    def _parsear_goles(goles_local_raw: str, goles_visitante_raw: str) -> tuple[int, int] | None:
        try:
            goles_local = int(goles_local_raw)
            goles_visitante = int(goles_visitante_raw)
        except (TypeError, ValueError):
            return None
        if goles_local < 0 or goles_visitante < 0:
            return None
        return goles_local, goles_visitante

    @staticmethod
    def _parsear_fecha(fecha_raw: str) -> date | None:
        try:
            return date.fromisoformat(str(fecha_raw).strip())
        except (TypeError, ValueError):
            return None
