"""Paquete preparation -- Capa de Preparacion de Variables.

Materializa, sin redefinirla, la capa ya especificada en
docs/15-Capa-de-Preparacion-de-Variables.md.

Responsabilidad (docs/35, seccion 4): transformar datos ya recuperados por
app/persistence en las Variables Oficiales (docs/16-Contrato-Oficial-de-Variables.md).
Nunca calcula probabilidades, fuerzas, caos ni valor esperado -- esa es la
responsabilidad exclusiva de app/engine.

BUILD-006: implementada `VariablePreparation` (preparation.py), que satisface
`VariablePreparationProtocol` (BUILD-005). Construye el bloque
`context.variables` con las 9 Variables Oficiales activas en V1
(Variable001-004, 006-010), todas marcadas como pendientes de cálculo
("PENDIENTE": `valor=None`, `disponible=False`) -- ningún valor se calcula ni
se inventa todavía. Variable005 y Variable011 permanecen diferidas
(`MR-004`), sin campo en `PredictionContext` (ver nota de alcance en
preparation.py sobre la discrepancia detectada frente al brief de esta
misión, documentada y no resuelta modificando arquitectura previa).

BUILD-017: `VariablePreparation` pasa de estructural a funcional. Antes de
calcular nada, se verificó que 7 de las 9 variables activas no tienen
método de cálculo autorizado en ningún documento (`docs/03`: "Método:
Pendiente", o pesos sin calibrar en `models/offensive-strength.md`/
`defensive-strength.md`) -- hallazgo reportado y resuelto por decisión
explícita del usuario: implementar solo lo que tiene método autorizado y es
compatible con el esquema ya existente. **Variable010 (Historial Directo)**
queda calculada con dato real (`docs/16`: "diferencia neta de victorias"),
leyendo `CsvPreparationRepository` (`app/persistence/preparation_repository.py`,
BUILD-017, nueva implementación real de `PreparationRepositoryProtocol` --
su interfaz se redefine con los tres métodos que esta misión realmente
necesita, reemplazando el `obtener_datos_partido` nunca invocado de
`BUILD-006`). **Variable009 (Localía)** tiene método derivable sin inventar
nada, pero permanece `disponible=False`: `ValorVariable.valor` está tipado
`float | None`, incompatible con el ENUM de texto que exige Variable009 --
mismo "Hallazgo #3" ya documentado sin resolver desde `BUILD-012`
(`engine03.py`), que solo se resolvería modificando `PredictionContext`,
fuera de alcance de esta misión. Variable001/002/006/007/008 permanecen
`disponible=False` por ausencia de método autorizado; Variable003/004, por
depender de pesos explícitamente sin calibrar. Variable005/011 siguen
diferidas, sin cambios.

BUILD-018: implementa Variable003 (Potencial Ofensivo) con dato real,
siguiendo exclusivamente `models/offensive-strength.md` §17-27 (`MODEL-009`
-- única autoridad matemática, ninguna fórmula ni interpretación propia).
Agrega `app/preparation/potencial_ofensivo_repository.py`
(`CsvPotencialOfensivoRepository`/`PotencialOfensivoRepositoryProtocol`) --
vive en `app/preparation/`, no en `app/persistence/`, porque el brief de
esta misión prohíbe explícitamente modificar `Persistence`. `Variable
Preparation.__init__` gana un segundo colaborador opcional
(`potencial_ofensivo_repository`, con valor por defecto) sin alterar la
firma pública `preparar(context)` ni el primer parámetro -- compatible sin
cambios con `BUILD-006`/`BUILD-009`/`BUILD-010`/`BUILD-011`; `Engine01` sigue
leyendo `context.variables.potencial_ofensivo` exactamente igual. Cualquier
fallo al calcular Variable003 se captura internamente, se registra en
`context.errors` y se traduce en `disponible=False` -- nunca detiene el
resto de `VariablePreparation` (restricción explícita del brief, más
estricta que el manejo de errores de `BUILD-016`/`BUILD-017`).

BUILD-019/BUILD-021/BUILD-020: implementan, respectivamente, Variable004
(Solidez Defensiva, `models/defensive-strength.md` §13-21, `MODEL-010`),
Variable002 (Rendimiento en el Torneo, `models/rendimiento-torneo.md`,
`MODEL-012`) y Variable001 (Forma Reciente, `models/forma-reciente.md`,
`MODEL-011`) -- ningún símbolo nuevo de estas tres misiones se exporta
públicamente desde este paquete: `BUILD-019`/`BUILD-020` restringen sus
modificaciones únicamente a `app/preparation/preparation.py` (las clases
`_SolidezDefensivaRepository*`/`_FormaRecienteRepository*` son privadas de
ese módulo), y `BUILD-021` extiende `app/persistence/preparation_
repository.py`, no este paquete. Con esta secuencia, 4 de las 9 Variables
Oficiales activas (001, 002, 003, 004) además de Variable010 tienen cálculo
real -- quedan pendientes 006, 007, 008 (sin método autorizado) y 009
(bloqueo de esquema, ver `preparation.py`).

BUILD-022: implementa el componente "Profundidad" de Variable008 (Calidad
de Plantilla, `models/profundidad-plantilla.md`, `MODEL-013`) -- mismo
alcance de archivo restringido que `BUILD-019`/`BUILD-020`: toda la lectura
de datos nueva (`_ProfundidadPlantillaRepository` y afines, todas privadas)
vive dentro de `preparation.py`, ningún símbolo nuevo se exporta desde este
paquete. "Valor de mercado"/"Experiencia" (las otras dos señales de
Variable008) no se implementan -- fuera de alcance ya fijado por `MR-004`.
Con esta misión, 5 de las 9 Variables Oficiales activas (001, 002, 003, 004,
008-Profundidad) además de Variable010 tienen cálculo real -- quedan
pendientes 006, 007 (sin método autorizado) y 009 (bloqueo de esquema).

BUILD-023: implementa Variable007 (Fatiga) en su alcance reducido V1 --
Escasez de Descanso + Viajes (`models/fatiga.md`, `MODEL-014`) -- mismo
alcance de archivo restringido que `BUILD-019`/`020`/`022`: toda la lectura
de datos nueva (`_FatigaRepository` y afines, todas privadas) vive dentro de
`preparation.py`, ningún símbolo nuevo se exporta desde este paquete.
"Minutos jugados" no se implementa -- `MODEL-014` §11 concluye que no existe
fuente de datos para esa señal con el esquema actual (declarado
explícitamente no implementable, no un simple diferimiento de alcance).
Con esta misión, 6 de las 9 Variables Oficiales activas (001, 002, 003, 004,
007-alcance reducido, 008-Profundidad) además de Variable010 tienen cálculo
real -- queda pendiente 006 (sin método autorizado) y 009 (bloqueo de
esquema).

BUILD-024: implementa Variable006 (Disponibilidad de Plantilla) en su
alcance reducido V1 -- solo "Lesiones" (`models/disponibilidad.md`,
`MODEL-015`) -- mismo alcance de archivo restringido que `BUILD-019`/`020`/
`022`/`023`: toda la lectura de datos nueva (`_DisponibilidadRepository` y
afines, todas privadas) vive dentro de `preparation.py`, ningún símbolo
nuevo se exporta desde este paquete. "Suspensiones"/"Rotaciones" no se
implementan -- `MODEL-015` §10 concluye que ninguna tiene fuente de datos
suficiente con el esquema actual (declaradas explícitamente no
implementables, no un simple diferimiento de alcance). Con esta misión, las
8 Variables Oficiales activas con método derivable tienen cálculo real
(001, 002, 003, 004, 006-alcance reducido, 007-alcance reducido,
008-Profundidad) además de Variable010 -- 8 de 9. Solo queda Variable009
(bloqueo de esquema, no de método ni de dato).
"""

from app.preparation.preparation import PreparationRepositoryProtocol, VariablePreparation
from app.preparation.potencial_ofensivo_repository import (
    CsvPotencialOfensivoRepository,
    DatosPotencialOfensivoInconsistentes,
    MetricaPartido,
    MetricasOfensivas,
    PotencialOfensivoRepositoryProtocol,
)

__all__ = [
    "CsvPotencialOfensivoRepository",
    "DatosPotencialOfensivoInconsistentes",
    "MetricaPartido",
    "MetricasOfensivas",
    "PotencialOfensivoRepositoryProtocol",
    "PreparationRepositoryProtocol",
    "VariablePreparation",
]
