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
"""

from app.preparation.preparation import PreparationRepositoryProtocol, VariablePreparation

__all__ = ["PreparationRepositoryProtocol", "VariablePreparation"]
