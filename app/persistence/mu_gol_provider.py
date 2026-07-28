"""`HistoricalMuGolProvider` -- proveedor oficial de `μ_gol` (`models/poisson.md`
§6, §17, §21).

Referencias revisadas antes de escribir este módulo: `docs/00-Project-
Tracker.md`, `models/poisson.md` (§6: definición exacta de `μ_gol`),
`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md` (matriz de
dependencias, sección 5-6), `app/engine/engine03.py` (BUILD-012 --
consumidor de este proveedor, define el `Protocol` que este módulo debe
satisfacer estructuralmente), `app/preparation/preparation.py` (BUILD-006
-- mismo patrón de `Protocol` declarado junto a su consumidor, precedente
citado explícitamente por `BUILD-012` para `MuGolProvider`).

BUILD-016: primera implementación real de un colaborador inyectable para
Engine03 (`MuGolProvider`, documentado como sin implementación desde
`BUILD-012`). No modifica `Engine03`, `PredictionContext`, el Runtime, las
Variables Oficiales ni ninguna fórmula matemática -- únicamente agrega este
archivo nuevo.

## Nota sobre `app/persistence/__init__.py` (acceso "contra PostgreSQL")

El docstring del paquete (`app/persistence/__init__.py`, BUILD-003) describe
su responsabilidad como "ejecutar consultas y escrituras contra PostgreSQL
usando `app/models`". Este módulo no usa SQLAlchemy en absoluto -- lee CSV
directamente, mismo carácter transicional ya aceptado en el proyecto para
`cuotas.csv` (`INC-05`, `engine/06`): la Base de Conocimiento vive hoy en
`data/processed/`, no en PostgreSQL poblado. Se documenta aquí, no se
resuelve (fuera de alcance de `BUILD-016`) -- una futura migración de este
proveedor a un repositorio SQLAlchemy real (`partidos`, `torneos`,
`competiciones`, ya modelados desde `BUILD-002`) sería consistente con la
letra exacta de ese docstring, sin cambiar el `Protocol` que este módulo
expone.

## Ubicación -- por qué `app/persistence`, no `app/services`

El brief sugiere `app/services/mu_goal_provider.py` "o la ubicación que
definan como oficial según la arquitectura". `docs/35`, sección 6 (tabla de
responsabilidades), fija una restricción explícita para `app/services`:
"Nunca... formar parte del camino crítico del Runtime -- se ejecutan antes
o después, nunca dentro" (reservado a Statistician/Auditor/Bankroll
Manager). Pero `MuGolProvider` se invoca **dentro** de `Engine03.ejecutar()`,
en plena Capa 2 -- exactamente el camino crítico que `app/services` tiene
prohibido integrar. `docs/35` sí asigna a `app/persistence` "toda la lógica
de acceso a datos" (sección 4) -- y calcular `μ_gol` es, precisamente, leer
y agregar datos ya existentes de la Base de Conocimiento, no lógica de
negocio del Engine. Se elige `app/persistence/mu_gol_provider.py` (no
`repositories/`, porque no opera sobre SQLAlchemy/`BaseRepository` como los
futuros repositorios de esa carpeta, sino directamente sobre los CSV de
`data/processed/`, mientras no exista una tabla `partidos` poblada).

## Protocol declarado de forma independiente -- no importado desde `app.engine`

`app/engine/engine03.py` ya declara su propio `MuGolProvider(Protocol)`.
Este módulo **no lo importa** -- `docs/35` §5 fija una matriz de
dependencias estrictamente unidireccional
(`api → runtime → preparation → engine → persistence → models`):
`app/persistence` no puede depender de `app/engine` (iría en sentido
contrario). `Protocol` de Python se satisface **estructuralmente** (duck
typing): `HistoricalMuGolProvider`, con su método `obtener_mu_gol(self,
competicion: str) -> float | None`, ya es compatible con el `MuGolProvider`
de `engine03.py` sin heredar de él ni importarlo -- quien componga la
aplicación (una futura misión de *wiring*, `app/api` o un arnés de pruebas)
simplemente instancia `HistoricalMuGolProvider` y lo inyecta en `Engine03`.

## Algoritmo (`models/poisson.md` §6, literal, sin ampliar)

`μ_gol` = promedio histórico de goles por equipo por partido, en la
competición solicitada. Cálculo:

1. Resolver `id_competicion` a partir del identificador de competición
   recibido -- acepta tanto `id_competicion` como `nombre` (`competiciones.csv`,
   mismo contrato dual ya usado por `CsvPotencialOfensivoRepository`/
   `_SolidezDefensivaRepository`, unificado aquí por `FIX-001`).
2. Resolver el conjunto de `id_torneo` (ediciones) que pertenecen a esa
   competición (`torneos.csv`, columna `id_competicion`).
3. Filtrar `partidos.csv` a las filas cuyo `id_torneo` pertenezca a ese
   conjunto y cuyos `goles_local`/`goles_visitante` sean enteros válidos,
   no negativos.
4. `μ_gol = (Σ goles_local + Σ goles_visitante) / (2 · n_partidos)` --
   promedio simple, sin ponderar, sin media móvil, sin separar local de
   visitante (todo eso queda explícitamente fuera de alcance de esta
   misión, ver "Fuera de alcance" del brief).
5. Si `n_partidos < MINIMO_PARTIDOS_HISTORICOS`, se considera evidencia
   insuficiente -- devuelve `None` (nunca un valor inventado).

## Manejo de errores -- nunca un placeholder silencioso

- **Partidos insuficientes** (cero, o por debajo de `MINIMO_PARTIDOS_
  HISTORICOS`): devuelve `None` -- el mismo contrato que `MuGolProvider`
  (`engine03.py`) ya espera; Engine03 ya interpreta `None` como "sin dato",
  registra `ErrorEntry` y se detiene (`MuGolNoDisponible`, sin cambios).
- **Competición no reconocida** (sin fila en `competiciones.csv`): mismo
  tratamiento, `None` -- no es distinguible, para quien llama, de "no hay
  historial suficiente".
- **Datos estructuralmente inconsistentes** (columna esperada ausente,
  archivo CSV corrupto/no legible): se levanta `DatosHistoricosInconsistentes`
  -- un fallo real, no una ausencia de evidencia, y por lo tanto no debe
  disfrazarse de `None`. Como este proveedor nunca escribe en
  `PredictionContext` (fuera de su responsabilidad, ver docstring de la
  clase), la excepción se propaga; si se invoca desde dentro de
  `Engine03.ejecutar()`, `EngineRunner._ejecutar_capa` ya la captura y la
  registra en `context.errors` (mismo mecanismo ya vigente desde
  `BUILD-007`, sin necesidad de que este módulo conozca `PredictionContext`).
- **Filas individuales inconsistentes** (`goles_local`/`goles_visitante` no
  numérico o negativo en una fila puntual): se descartan silenciosamente
  **solo esa fila**, no todo el cálculo -- un único dato corrupto no debe
  invalidar el resto del historial válido; si el resultado neto no alcanza
  `MINIMO_PARTIDOS_HISTORICOS`, se aplica la misma regla de "insuficiente".

## Qué NO hace este módulo (alcance explícito del brief)

No ejecuta ningún motor. No accede a `PredictionContext` ni al Runtime en
absoluto -- ninguna importación de `app.runtime` ni `app.engine`. No
calcula probabilidades, `λ`, ni ninguna otra salida del Engine. No calibra
nada, no aplica medias móviles, no pondera por tiempo, no separa local de
visitante, no calcula Expected Goals ni usa aprendizaje automático -- todo
explícitamente fuera de alcance del brief de `BUILD-016`. Nunca lee
`data/raw/`.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Protocol

MINIMO_PARTIDOS_HISTORICOS = 10
"""Placeholder documentado (TODO) -- ningún documento (`models/poisson.md`,
`models/parameter-calibration.md`) propone un tamaño mínimo de muestra para
`μ_gol`. Valor estructural, no calibrado: suficientemente mayor que 1 para
evitar que un único partido determine el promedio de toda una competición,
sin pretensión de significancia estadística real. Requiere calibración real
(`models/parameter-calibration.md` §7) en cuanto exista evidencia suficiente
en `data/results/`.
"""

_ARCHIVO_PARTIDOS = "partidos.csv"
_ARCHIVO_TORNEOS = "torneos.csv"
_ARCHIVO_COMPETICIONES = "competiciones.csv"


class MuGolProviderProtocol(Protocol):
    """Contrato estructural -- ver "Protocol declarado de forma
    independiente" en el docstring del módulo. Misma firma que
    `app.engine.engine03.MuGolProvider`, sin importarlo.
    """

    def obtener_mu_gol(self, competicion: str) -> float | None:
        """Debe devolver el promedio histórico de goles por equipo por
        partido para `competicion`, o `None` si no hay evidencia
        suficiente -- nunca debe inventar un valor.
        """
        ...


class DatosHistoricosInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado como "sin evidencia suficiente" (`None`). Ver "Manejo de
    errores" en el docstring del módulo.
    """


class HistoricalMuGolProvider:
    """Calcula `μ_gol` a partir del historial real de partidos en
    `data/processed/selecciones-nacionales/` (`models/poisson.md` §6).
    Nunca accede a `data/raw/`, nunca ejecuta motores, nunca modifica
    `PredictionContext` -- únicamente lee CSV y devuelve un `float | None`.
    """

    def __init__(
        self,
        data_dir: Path | None = None,
        minimo_partidos: int = MINIMO_PARTIDOS_HISTORICOS,
    ) -> None:
        """`data_dir` es inyectable (por defecto,
        `data/processed/selecciones-nacionales/` resuelto de forma
        absoluta desde la ubicación de este archivo, no desde el
        directorio de trabajo actual) -- permite apuntar a un directorio de
        prueba sin modificar el repositorio real.
        """
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )
        self._minimo_partidos = minimo_partidos

    def obtener_mu_gol(self, competicion: str) -> float | None:
        id_competicion = self._resolver_id_competicion(competicion)
        if id_competicion is None:
            return None

        ids_torneo = self._torneos_de_competicion(id_competicion)
        if not ids_torneo:
            return None

        partidos_validos = self._partidos_validos(ids_torneo)
        if len(partidos_validos) < self._minimo_partidos:
            return None

        total_goles = sum(goles_local + goles_visitante for goles_local, goles_visitante in partidos_validos)
        return total_goles / (2 * len(partidos_validos))

    # -- Lectura de CSV (data/processed/ únicamente, nunca data/raw/) -------

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise DatosHistoricosInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc

    def _resolver_id_competicion(self, competicion: str) -> str | None:
        """Acepta `id_competicion` o `nombre` (`FIX-001`) -- antes solo
        aceptaba `nombre`, inconsistente con `CsvPotencialOfensivoRepository`/
        `_SolidezDefensivaRepository` (Variable003/004), que ya resolvían
        ambos. Detectado por ejecución real en `ENGINE-001`: pasar
        `context.match.competicion="COMP-000004"` hacía fallar `Engine03`
        (`μ_gol` no resuelto) mientras Variable003/004 sí calculaban
        correctamente con ese mismo valor. Ningún cambio de algoritmo --
        `μ_gol` sigue siendo el promedio simple ya definido en
        `models/poisson.md` §6, sin ponderar ni recalibrar.
        """
        filas = self._leer_csv(_ARCHIVO_COMPETICIONES)
        objetivo = competicion.strip().lower()
        for fila in filas:
            try:
                nombre = fila["nombre"]
                id_competicion = fila["id_competicion"]
            except KeyError as exc:
                raise DatosHistoricosInconsistentes(
                    f"'{_ARCHIVO_COMPETICIONES}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_competicion.strip().lower() == objetivo or nombre.strip().lower() == objetivo:
                return id_competicion
        return None

    def _torneos_de_competicion(self, id_competicion: str) -> set[str]:
        filas = self._leer_csv(_ARCHIVO_TORNEOS)
        ids_torneo: set[str] = set()
        for fila in filas:
            try:
                if fila["id_competicion"] == id_competicion:
                    ids_torneo.add(fila["id_torneo"])
            except KeyError as exc:
                raise DatosHistoricosInconsistentes(
                    f"'{_ARCHIVO_TORNEOS}' no tiene la columna esperada: {exc}."
                ) from exc
        return ids_torneo

    def _partidos_validos(self, ids_torneo: set[str]) -> list[tuple[int, int]]:
        filas = self._leer_csv(_ARCHIVO_PARTIDOS)
        partidos_validos: list[tuple[int, int]] = []
        for fila in filas:
            try:
                id_torneo = fila["id_torneo"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise DatosHistoricosInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_torneo not in ids_torneo:
                continue

            goles = self._parsear_goles(goles_local_raw, goles_visitante_raw)
            if goles is not None:
                partidos_validos.append(goles)

        return partidos_validos

    @staticmethod
    def _parsear_goles(goles_local_raw: str, goles_visitante_raw: str) -> tuple[int, int] | None:
        """Descarta -- solo esa fila, ver "Manejo de errores" -- si los
        goles no son enteros no negativos (partido no finalizado, celda
        vacía, valor corrupto). Nunca inventa un valor para completar una
        fila incompleta.
        """
        try:
            goles_local = int(goles_local_raw)
            goles_visitante = int(goles_visitante_raw)
        except (TypeError, ValueError):
            return None
        if goles_local < 0 or goles_visitante < 0:
            return None
        return goles_local, goles_visitante


class StaticMuGolProvider:
    """Proveedor fijo -- **únicamente para pruebas**, nunca para un cálculo
    real (brief de `BUILD-016`: "opcionalmente... únicamente para
    pruebas"). No lee ningún archivo, no aplica ninguna lógica -- devuelve
    siempre el mismo valor inyectado en el constructor. No debe usarse en
    ninguna composición de producción del Runtime.
    """

    def __init__(self, valor_fijo: float | None) -> None:
        self._valor_fijo = valor_fijo

    def obtener_mu_gol(self, competicion: str) -> float | None:
        return self._valor_fijo
