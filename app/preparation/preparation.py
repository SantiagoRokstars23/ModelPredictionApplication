"""`VariablePreparation` -- construye el bloque `context.variables`.

Ver docs/15-Capa-de-Preparacion-de-Variables.md (responsabilidad conceptual),
docs/16-Contrato-Oficial-de-Variables.md (las 12 Variables Oficiales),
docs/17-Matriz-de-Consumo-de-Variables.md (qué motor consume cada una),
docs/29-Arquitectura-del-Runtime.md (interfaz `VariablePreparationProtocol`,
BUILD-005), docs/30-Contrato-Oficial-del-Prediction-Context.md, sección 4.3
(forma exacta del bloque `variables`).

BUILD-006: primera pieza funcional del flujo. Implementa el protocolo ya
definido por BUILD-005 (`VariablePreparationProtocol.preparar`) -- no
modifica el Runtime, `PredictionContext` ni ningún otro componente ya
implementado. No calcula ningún valor: cada Variable Oficial se entrega
únicamente con su estructura, marcada como no disponible ("PENDIENTE"),
nunca con un valor inventado (`CLAUDE.md`: "Nunca inventar datos").

## Observación de la misión (discrepancia entre el brief y la arquitectura
## ya vigente -- documentada, no resuelta; decisión explícita del usuario)

El brief de BUILD-006 pide preparar "las 12 Variables Oficiales, no más, no
menos". Sin embargo, `docs/03-Variables.md`, `docs/17-Matriz-de-Consumo-de-Variables.md`
y `docs/30-Contrato-Oficial-del-Prediction-Context.md` (sección 4.3) ya
establecen, de forma consistente entre sí, que Variable005 (Compatibilidad
Táctica) y Variable011 (Estado Psicológico) están **formalmente diferidas**
desde `MR-004` -- sin fuente de datos real en la Base de Conocimiento, sin
consumidor asignado, y explícitamente ausentes del bloque `variables` de
`docs/30`. El `PredictionContext` ya implementado en BUILD-004
(`VariablesBlock`) tiene, en consecuencia, nueve campos, no doce -- y esta
misma misión prohíbe modificar `PredictionContext`. Por decisión explícita
del usuario (no una resolución unilateral de esta sesión), esta
implementación prepara únicamente las **nueve Variables Oficiales activas
en V1** (Variable001, 002, 003, 004, 006, 007, 008, 009, 010), dejando
Variable005 y Variable011 diferidas conforme a `MR-004`, sin tocar ningún
documento de arquitectura ya existente.
"""

from __future__ import annotations

from typing import Any, Protocol

from app.runtime.prediction_context import (
    PredictionContext,
    ValorVariable,
    VariablesBlock,
    VariablesPorEquipo,
)


class PreparationRepositoryProtocol(Protocol):
    """Interfaz de lectura desde Persistence -- ningún repositorio
    específico existe todavía (`app/persistence` solo tiene `BaseRepository`
    genérico, BUILD-003). Se declara aquí, sin implementación real, para que
    una misión futura (la que efectivamente calcule un valor) tenga un
    punto de inyección ya definido -- "utilizar únicamente interfaces o
    stubs" (brief de BUILD-006).
    """

    def obtener_datos_partido(self, id_partido: str) -> Any:
        """Debe devolver los datos de negocio necesarios para construir las
        Variables Oficiales de un partido. No se invoca en esta misión (ver
        nota en `VariablePreparation.preparar`).
        """
        ...


class VariablePreparation:
    """Implementación de `VariablePreparationProtocol` (`app/runtime/runtime.py`,
    BUILD-005). Construye `context.variables` con las 9 Variables Oficiales
    activas en V1, todas marcadas como pendientes de cálculo -- nunca
    calcula, nunca consulta SQL, nunca decide suficiencia de datos (esa es
    responsabilidad del Statistician, fuera de esta clase, `docs/15` §1).
    """

    def __init__(self, repository: PreparationRepositoryProtocol | None = None) -> None:
        # Aceptado para habilitar la inyección de un repositorio real en una
        # misión futura. No se invoca en `preparar()`: ningún dato leído
        # cambiaría el resultado de esta misión, porque ninguna variable se
        # calcula todavía (ver nota de alcance, encabezado del módulo).
        self._repository = repository

    def preparar(self, context: PredictionContext) -> None:
        """Agrega el bloque `variables` al `context` (docs/30, sección 4.3).

        Cada Variable Oficial se entrega únicamente con su estructura --
        `valor=None`, `disponible=False` ("PENDIENTE") -- nunca con un valor
        inventado. Las variables de rendimiento (Variable001-004, 006-008)
        se preparan una vez por equipo (local y visitante, `docs/30` §4.3);
        Localía (Variable009) e Historial Directo (Variable010) son propias
        del enfrentamiento, un único valor por partido.
        """
        context.variables = VariablesBlock(
            forma_reciente=self._pendiente_por_equipo(),  # Variable001
            rendimiento_torneo=self._pendiente_por_equipo(),  # Variable002
            potencial_ofensivo=self._pendiente_por_equipo(),  # Variable003
            solidez_defensiva=self._pendiente_por_equipo(),  # Variable004
            disponibilidad_plantilla=self._pendiente_por_equipo(),  # Variable006
            fatiga=self._pendiente_por_equipo(),  # Variable007
            calidad_plantilla=self._pendiente_por_equipo(),  # Variable008
            localia=self._pendiente(),  # Variable009
            historial_directo=self._pendiente(),  # Variable010
        )

    def _pendiente(self) -> ValorVariable:
        """Una Variable Oficial sin calcular -- estructura únicamente."""
        return ValorVariable(valor=None, disponible=False, muestra_reducida=False)

    def _pendiente_por_equipo(self) -> VariablesPorEquipo:
        """La misma estructura pendiente, una vez por equipo (local y
        visitante) -- ver docs/30, sección 4.3.
        """
        return VariablesPorEquipo(local=self._pendiente(), visitante=self._pendiente())
