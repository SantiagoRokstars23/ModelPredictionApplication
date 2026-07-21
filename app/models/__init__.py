"""Paquete models -- entidades ORM de SQLAlchemy.

Distinto del directorio raiz `models/` (investigacion matematica --
models/poisson.md, models/parameter-calibration.md, etc. -- que permanece
sin cambios). Ver docs/35-Arquitectura-Oficial-del-Proyecto-Python.md,
"Aclaracion de nomenclatura".

Responsabilidad (docs/35, seccion 4): declarar la forma de las 14 tablas
fisicas ya disenadas en docs/33-Modelo-Fisico-PostgreSQL.md como clases
SQLAlchemy. Nunca contiene logica de negocio ni de calculo -- es una hoja
dentro de la matriz de dependencias (docs/35, seccion 5).

BUILD-002: las 14 entidades quedan implementadas (una por modulo, ver cada
archivo). Se re-exportan aqui para que `Base.metadata` conozca las 14 tablas
en cuanto se importe este paquete (necesario para que Alembic, en una mision
futura, pueda generar la primera revision con `--autogenerate`) y para que
las referencias de `relationship()` basadas en nombre de clase (strings)
puedan resolverse sin importar cada modulo por separado.

No se implementa `Propuesta de Aprendizaje` -- docs/33, seccion 4.15, la
marca explicitamente como "no oficial todavia, sin persistencia confirmada".
"""

from app.models.arbitro import Arbitro
from app.models.auditoria import Auditoria
from app.models.base import Base
from app.models.competicion import Competicion
from app.models.convocatoria import Convocatoria
from app.models.cuota import Cuota
from app.models.estadio import Estadio
from app.models.estadistica_partido import EstadisticaPartido
from app.models.jugador import Jugador
from app.models.lesion import Lesion
from app.models.partido import Partido
from app.models.prediccion import Prediccion
from app.models.resultado import Resultado
from app.models.seleccion import Seleccion
from app.models.torneo import Torneo

__all__ = [
    "Arbitro",
    "Auditoria",
    "Base",
    "Competicion",
    "Convocatoria",
    "Cuota",
    "Estadio",
    "EstadisticaPartido",
    "Jugador",
    "Lesion",
    "Partido",
    "Prediccion",
    "Resultado",
    "Seleccion",
    "Torneo",
]
