"""Representación oficial del `PredictionContext`.

Ver docs/30-Contrato-Oficial-del-Prediction-Context.md — este módulo traduce,
bloque por bloque, ese contrato a código. Ninguna sección, campo o regla se
inventa aquí: cada modelo cita la sección exacta de `docs/30` de la que
proviene.

BUILD-004: única definición oficial del `PredictionContext` en todo el
proyecto (validación obligatoria: "existe una única definición oficial").
Ningún cálculo, ninguna consulta, ninguna lógica de negocio — únicamente
estructura de datos tipada.

## Elección de tecnología: Pydantic, no `dataclasses`

El brief permite ambas. Se elige Pydantic (`BaseModel`) porque los cinco
requisitos explícitos del brief —mutable, serializable, tipado, fácil de
persistir, fácil de auditar— son, literalmente, capacidades ya incorporadas
en Pydantic sin código adicional:

- **Mutable**: un `BaseModel` de Pydantic permite asignación de atributos
  igual que un `dataclass` (ninguno de los dos se marca `frozen` aquí).
- **Serializable / fácil de persistir y auditar**: `.model_dump()` /
  `.model_dump_json()` producen, sin escribir ninguna función propia, la
  representación anidada completa del objeto — exactamente lo que
  `docs/26`, sección 7 (registro de ejecución) y la futura auditoría
  necesitarán para inspeccionar un `PredictionContext` completo.
- **Tipado**: Pydantic valida los tipos declarados en tiempo de ejecución,
  no solo en tiempo de análisis estático — una garantía adicional que
  `dataclasses` no ofrece por sí solo.

Pydantic ya es una dependencia aprobada del stack (`docs/34`, sección 8) y
se usa, en `app/schemas`, para los contratos externos de la API — pero este
módulo vive deliberadamente en `app/runtime`, no en `app/schemas`: el
`PredictionContext` es el objeto **interno** de ejecución (docs/29, docs/30),
nunca el contrato externo de la API, aunque ambos usen la misma tecnología
de validación.

## Qué NO hace este módulo

No implementa ningún método (ni siquiera uno para "agregar una sección" o
"validar que no se sobrescriba una sección ya escrita") — la regla Append
Only (`docs/30`, sección 2/5) es una responsabilidad de **quién usa** este
objeto (el futuro Runtime), no del contrato de datos en sí. Añadir esa
lógica aquí excedería "no implementar lógica del modelo" (restricciones de
BUILD-004).
"""

from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EstadoEjecucion(str, Enum):
    """Estados de ejecución ya definidos en docs/29-Arquitectura-del-Runtime.md,
    sección 6 — no se redefinen, solo se tipan.
    """

    COMPLETA = "Completa"
    COMPLETA_SIN_VALOR_ESPERADO = "Completa sin Valor Esperado"
    DETENIDA_ANTES_DEL_ENGINE = "Detenida antes del Engine"
    DETENIDA_DURANTE_EL_ENGINE = "Detenida durante el Engine"


class _ContextModel(BaseModel):
    """Base común de todos los bloques -- únicamente configuración, sin
    métodos ni lógica.
    """

    model_config = ConfigDict(validate_assignment=True)


# ---------------------------------------------------------------------------
# 4.1 `metadata`
# ---------------------------------------------------------------------------


class MetadataBlock(_ContextModel):
    """docs/30, sección 4.1. Escrito por el Runtime al crear el Context."""

    version_modelo: str
    timestamp_creacion: datetime
    timestamp_cierre: datetime | None = None
    estado_ejecucion: EstadoEjecucion | None = None
    id_prediccion: str | None = None  # asignado al persistir, no al crear (docs/25 §6)


# ---------------------------------------------------------------------------
# 4.2 `match`
# ---------------------------------------------------------------------------


class MatchBlock(_ContextModel):
    """docs/30, sección 4.2 — equivalente exacto a "Identificación"
    (docs/26/docs/29). Escrito por el Runtime al crear el Context.
    """

    id_partido: str
    seleccion_local: str
    seleccion_visitante: str
    competicion: str
    torneo: str
    fecha: date
    hora_local: time | None = None
    estadio: str | None = None
    arbitro: str | None = None


# ---------------------------------------------------------------------------
# 4.3 `variables`
# ---------------------------------------------------------------------------


class ValorVariable(_ContextModel):
    """Valor de una Variable Oficial, con su disponibilidad explícita —
    nunca se entrega un valor inventado (docs/15/docs/16).
    """

    valor: float | None = None
    disponible: bool = True
    muestra_reducida: bool = False


class VariablesPorEquipo(_ContextModel):
    """Variables de rendimiento (Variable001-004, 006-008): se construyen
    una vez por equipo (docs/30, sección 4.3).
    """

    local: ValorVariable
    visitante: ValorVariable


class VariablesBlock(_ContextModel):
    """docs/30, sección 4.3. Escrito una única vez por `VariablePreparation`.

    Variable005 (Compatibilidad Táctica) y Variable011 (Estado Psicológico)
    no aparecen aquí -- formalmente diferidas en V1 (`MR-004`).
    """

    forma_reciente: VariablesPorEquipo  # Variable001
    rendimiento_torneo: VariablesPorEquipo  # Variable002
    potencial_ofensivo: VariablesPorEquipo  # Variable003
    solidez_defensiva: VariablesPorEquipo  # Variable004
    disponibilidad_plantilla: VariablesPorEquipo  # Variable006
    fatiga: VariablesPorEquipo  # Variable007
    calidad_plantilla: VariablesPorEquipo  # Variable008
    localia: ValorVariable  # Variable009 -- propia del partido, no por equipo
    historial_directo: ValorVariable  # Variable010 -- propia del partido


# ---------------------------------------------------------------------------
# 4.4 `engine` (una subsección por motor)
# ---------------------------------------------------------------------------


class MarcadorProbabilidad(_ContextModel):
    """Un marcador y su probabilidad -- reutilizado por `engine03` (matriz
    completa y Top 4) y por el bloque `prediction` (sección 4.5), para no
    duplicar la misma estructura dos veces.
    """

    marcador: str  # ej. "2-1"
    probabilidad: float


class Engine01Salida(_ContextModel):
    """Salida de engine/01-Offensive-Strength.md (docs/30, sección 4.4)."""

    fuerza_ofensiva: float
    nivel_confianza_calculo: float
    variables_utilizadas: list[str] = Field(default_factory=list)
    variables_descartadas: list[str] = Field(default_factory=list)
    calidad_datos: str


class Engine02Salida(_ContextModel):
    """Salida de engine/02-Defensive-Strength.md (docs/30, sección 4.4)."""

    fuerza_defensiva: float
    nivel_confianza_calculo: float
    variables_utilizadas: list[str] = Field(default_factory=list)
    variables_descartadas: list[str] = Field(default_factory=list)
    calidad_datos: str


class DistribucionGoles(_ContextModel):
    """Distribución marginal de goles por equipo (docs/30, sección 4.4) --
    distinta de la matriz conjunta de marcadores (`probabilidad_marcador`).
    """

    local: dict[str, float] = Field(default_factory=dict)
    visitante: dict[str, float] = Field(default_factory=dict)


class Engine03Salida(_ContextModel):
    """Salida de engine/03-Poisson.md (docs/30, sección 4.4)."""

    goles_esperados_local: float
    goles_esperados_visitante: float
    distribucion_goles: DistribucionGoles
    probabilidad_marcador: list[MarcadorProbabilidad] = Field(default_factory=list)
    top_marcadores: list[MarcadorProbabilidad] = Field(default_factory=list)
    probabilidad_local: float
    probabilidad_empate: float
    probabilidad_visitante: float


class Engine04Salida(_ContextModel):
    """Salida de engine/04-Chaos-Index.md (docs/30, sección 4.4)."""

    indice_caos: float
    nivel_caos: str
    factores_aumentan: list[str] = Field(default_factory=list)
    factores_reducen: list[str] = Field(default_factory=list)
    justificacion: str


class Engine05Salida(_ContextModel):
    """Salida de engine/05-Confidence.md (docs/30, sección 4.4)."""

    indice_confianza: float
    nivel_confianza: str
    factores_positivos: list[str] = Field(default_factory=list)
    factores_negativos: list[str] = Field(default_factory=list)
    justificacion: str


class Engine06Salida(_ContextModel):
    """Salida de engine/06-Expected-Value.md -- una entrada por mercado
    evaluado (docs/30, sección 4.4: "uno por mercado evaluado").
    """

    mercado: str
    valor_esperado: float
    probabilidad_modelo: float
    probabilidad_implicita: float
    diferencia_porcentual: float
    nivel_confianza: float
    indice_caos_asociado: float
    recomendacion: str


class EngineBlock(_ContextModel):
    """docs/30, sección 4.4. Cada subsección la agrega el motor
    correspondiente, en el orden por capas ya fijado (docs/29, sección 4) --
    nunca un motor escribe en la subsección de otro (docs/30, sección 5).
    """

    engine01: Engine01Salida | None = None
    engine02: Engine02Salida | None = None
    engine03: Engine03Salida | None = None
    engine04: Engine04Salida | None = None
    engine05: Engine05Salida | None = None
    engine06: list[Engine06Salida] | None = None  # condicional, Fase 4


# ---------------------------------------------------------------------------
# 4.5 `prediction`
# ---------------------------------------------------------------------------


class Probabilidades(_ContextModel):
    local: float
    empate: float
    visitante: float


class PredictionBlock(_ContextModel):
    """docs/30, sección 4.5 -- subconjunto curado hacia el `PredictionReport`.
    Se completa progresivamente, en el mismo orden por capas que `engine`
    (nunca de una sola vez al final).
    """

    probabilidades: Probabilidades | None = None
    top_marcadores: list[MarcadorProbabilidad] = Field(default_factory=list)
    variables_influyentes: list[str] = Field(default_factory=list)
    confianza: float | None = None
    indice_caos: float | None = None
    valor_esperado: float | str | None = None  # o "no disponible — sin cuotas registradas"


# ---------------------------------------------------------------------------
# 4.6 `market` (condicional)
# ---------------------------------------------------------------------------


class MarketBlock(_ContextModel):
    """docs/30, sección 4.6 -- bloque condicional y deliberadamente mínimo:
    el Contrato de Datos de Mercado completo sigue sin diseñarse (`INC-05`).
    Hoy contiene únicamente la referencia ya documentada: las cuotas leídas
    directamente por `EngineRunner` (excepción heredada, no resuelta aquí).
    """

    cuotas: list[dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# 4.7 `bankroll` (condicional)
# ---------------------------------------------------------------------------


class BankrollBlock(_ContextModel):
    """docs/30, sección 4.7 -- solo si el usuario solicita gestión de
    bankroll (fuera del núcleo, `CLAUDE.md`). Contenido: la propuesta de
    distribución de capital (`.claude/agents/bankroll-manager.md`, "Salida").
    """

    propuesta_distribucion: str | dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# 4.8 `errors`
# ---------------------------------------------------------------------------


class ErrorEntry(_ContextModel):
    """Una entrada del registro append-only de anomalías (docs/30, sección
    4.8) -- la misma información que `docs/26`, sección 7 (registro de
    ejecución), ahora también disponible como sección consultable del
    propio `PredictionContext`.
    """

    evento: str
    componente_emisor: str
    capa_fase: str
    timestamp: datetime
    detalle: str | None = None


# ---------------------------------------------------------------------------
# 4.9 `audit` y 4.10 `learning` -- ausentes en el objeto en memoria
# ---------------------------------------------------------------------------


class AuditBlock(_ContextModel):
    """docs/30, sección 4.9. **Nunca existe en el objeto en memoria de una
    ejecución** (docs/30, sección 3, "Nota central de diseño") -- se agrega,
    después, al registro ya persistido, cross-referenciado por
    `id_prediccion`. Se declara aquí únicamente para completar el contrato
    de los diez bloques; el Runtime nunca la instancia.
    """

    resultado_ref: str
    metricas: dict[str, float] = Field(default_factory=dict)
    fecha_auditoria: datetime


class LearningBlock(_ContextModel):
    """docs/30, sección 4.10. Misma advertencia que `AuditBlock`: ausente en
    el objeto en memoria, se agrega al registro persistido después de
    `audit` (Fase 9, `docs/06`).
    """

    diagnostico: str | None = None
    patrones_detectados: list[str] = Field(default_factory=list)
    resultado_calibracion: dict[str, Any] | None = None
    estado_propuesta: str | None = None  # "pendiente" | "aprobada" | "rechazada"


# ---------------------------------------------------------------------------
# PredictionContext -- el objeto completo (docs/30, sección 4)
# ---------------------------------------------------------------------------


class PredictionContext(_ContextModel):
    """Único objeto compartido entre Runtime, Preparation, Engine y
    Persistence (docs/30, sección 1). Los diez bloques exactos de
    `docs/30`, sección 4 -- ninguno adicional, ninguno omitido.

    `audit` y `learning` se declaran como campos opcionales del contrato
    completo, pero **nunca deben tener valor en el objeto en memoria de una
    ejecución** -- solo existen en el registro ya persistido (docs/30,
    sección 3). Este módulo no impone esa regla en tiempo de ejecución
    (sería lógica, fuera de alcance de BUILD-004); queda documentada aquí
    para que el futuro Runtime la respete.
    """

    metadata: MetadataBlock
    match: MatchBlock
    variables: VariablesBlock | None = None
    engine: EngineBlock = Field(default_factory=EngineBlock)
    prediction: PredictionBlock | None = None
    market: MarketBlock | None = None
    bankroll: BankrollBlock | None = None
    errors: list[ErrorEntry] = Field(default_factory=list)
    audit: AuditBlock | None = None
    learning: LearningBlock | None = None
