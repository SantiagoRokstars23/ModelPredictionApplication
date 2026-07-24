"""Paquete persistence -- acceso a datos.

Responsabilidad (docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, seccion 4):
ejecutar consultas y escrituras contra PostgreSQL usando app/models. Nunca
ejecuta logica matematica o de negocio -- cualquier calculo que aparezca
aqui duplicaria una responsabilidad ya asignada a app/engine o app/preparation.

BUILD-003: primera version funcional. Expone:

- `get_engine()` (database.py) -- el único Engine de SQLAlchemy de toda la
  aplicación, de creación perezosa, leyendo `DATABASE_URL` desde `app/config`.
- `get_session()` / `SessionLocal` (session.py) -- la única fábrica y el
  único gestor de contexto para obtener una sesión.
- `BaseRepository` (repositories/base_repository.py) -- operaciones CRUD
  genéricas (`add`, `get`, `list`, `delete`, `update`), sin ninguna consulta
  específica de un modelo concreto.

BUILD-008: implementado `RuntimePersistence` (runtime_persistence.py) --
satisface `PersistenceProtocol` (`app/runtime/runtime.py`, BUILD-005),
reutilizando exclusivamente `get_session`/`BaseRepository` ya construidos en
BUILD-003 (ninguna sesión, motor o conexión nueva). Implementa
`persist_prediction` (persistencia real de una `Prediccion`, con la brecha
de resolución de `partido_id` documentada explícitamente en el módulo);
`persist_audit`/`persist_learning` quedan como *placeholders* documentados,
sin lógica de auditoría ni aprendizaje real.

Ningún repositorio específico (`PredictionRepository`, `MatchRepository`,
`SelectionRepository`, etc.), ninguna consulta de negocio, ningún filtro --
explícitamente fuera del alcance de esta serie de misiones. Ningún paquete
de `app/` distinto de éste debe crear un `Engine` o una `Session` por su
cuenta: éste es el único punto oficial de acceso a PostgreSQL (docs/35,
sección 6).

BUILD-016: implementado `HistoricalMuGolProvider` (mu_gol_provider.py) --
primera implementación real de un colaborador inyectable para `Engine03`
(`MuGolProvider`, sin implementación desde `BUILD-012`). Calcula `μ_gol`
(`models/poisson.md` §6) leyendo directamente `partidos.csv`/`torneos.csv`/
`competiciones.csv` de `data/processed/` -- no usa SQLAlchemy, carácter
transicional documentado explícitamente en el propio módulo (mismo
tratamiento ya aceptado para `cuotas.csv`, `INC-05`). Declara su propio
`MuGolProviderProtocol`, sin importar `app.engine` (matriz de dependencias
unidireccional, `docs/35` §5) -- satisface el `MuGolProvider` de
`engine03.py` por compatibilidad estructural (`Protocol`, duck typing), sin
heredar de él. Nunca ejecuta motores, nunca toca `PredictionContext` ni el
Runtime. Incluye `StaticMuGolProvider`, fijo, únicamente para pruebas.

BUILD-017: implementado `CsvPreparationRepository` (preparation_repository.py)
-- primera implementación real de `PreparationRepositoryProtocol`
(`app/preparation/preparation.py`, sin implementación desde `BUILD-006`).
Expone `obtener_seleccion`, `obtener_estadio` y `historial_enfrentamientos`,
leyendo `selecciones.csv`/`estadios.csv`/`partidos.csv` de `data/processed/`
-- mismo carácter transicional (CSV, no SQLAlchemy) ya documentado en
`mu_gol_provider.py`, sin la tensión arquitectónica de ese módulo (`docs/35`
ya declara que `app/preparation` depende de `app/persistence`). Nunca
calcula ninguna Variable Oficial ni accede a `data/raw/`.

BUILD-021: agrega `resolver_id_torneo`/`partidos_del_torneo` a
`CsvPreparationRepository`, necesarios para Variable002 (`models/
rendimiento-torneo.md`, `MODEL-012`) -- primera vez que se resuelve un
`id_torneo` específico (no una competición completa ni un par de
selecciones). Nueva clase `PartidoTorneo` (con `id_partido`/`fecha`, a
diferencia de `ResultadoHistorico`).
"""

from app.persistence.database import get_engine
from app.persistence.mu_gol_provider import (
    DatosHistoricosInconsistentes,
    HistoricalMuGolProvider,
    MuGolProviderProtocol,
    StaticMuGolProvider,
)
from app.persistence.preparation_repository import (
    CsvPreparationRepository,
    DatosBaseConocimientoInconsistentes,
    EstadioInfo,
    PartidoTorneo,
    ResultadoHistorico,
    SeleccionInfo,
)
from app.persistence.repositories.base_repository import BaseRepository
from app.persistence.runtime_persistence import RuntimePersistence
from app.persistence.session import SessionLocal, get_session

__all__ = [
    "BaseRepository",
    "CsvPreparationRepository",
    "DatosBaseConocimientoInconsistentes",
    "DatosHistoricosInconsistentes",
    "EstadioInfo",
    "HistoricalMuGolProvider",
    "MuGolProviderProtocol",
    "PartidoTorneo",
    "ResultadoHistorico",
    "RuntimePersistence",
    "SeleccionInfo",
    "SessionLocal",
    "StaticMuGolProvider",
    "get_engine",
    "get_session",
]
