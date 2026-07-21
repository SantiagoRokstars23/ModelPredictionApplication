"""Paquete repositories -- acceso genérico a las entidades de app/models.

Ver docs/35-Arquitectura-Oficial-del-Proyecto-Python.md, sección 4.

BUILD-003: únicamente `BaseRepository` (operaciones CRUD comunes). Ningún
repositorio específico de una entidad concreta (`PredictionRepository`,
`MatchRepository`, `SelectionRepository`, etc.) -- explícitamente fuera del
alcance de esta misión, junto con cualquier consulta o filtro de negocio.
"""
