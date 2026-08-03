"""Doble de prueba de `ApiFootballClientProtocol`, compartido por los tests
de los tres importadores -- nunca golpea la red, nunca requiere una
credencial real.
"""

from __future__ import annotations

from typing import Any

from app.ingestion.api_football_client import ApiFootballError


class FakeApiFootballClient:
    """Devuelve una respuesta pre-configurada por `(endpoint, tupla de
    parámetros ordenada)`. Lanza `ApiFootballError` si se consulta una
    combinación no configurada, para que un test que olvidó registrar una
    respuesta falle de forma explícita en lugar de devolver `None` en
    silencio.
    """

    def __init__(self, respuestas: dict[tuple[str, tuple[tuple[str, Any], ...]], dict]) -> None:
        self._respuestas = respuestas
        self.llamadas: list[tuple[str, dict[str, Any]]] = []

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        params = params or {}
        self.llamadas.append((endpoint, params))
        clave = (endpoint, tuple(sorted(params.items())))
        if clave not in self._respuestas:
            raise ApiFootballError(f"FakeApiFootballClient: sin respuesta configurada para {clave}")
        return self._respuestas[clave]
