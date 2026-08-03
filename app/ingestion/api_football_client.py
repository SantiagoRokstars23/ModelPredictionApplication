"""`ApiFootballClient` -- cliente HTTP mínimo hacia la API v3 de API-Football.

Referencias revisadas antes de escribir: `docs/42-Verificacion-Manual-API-
Football.md` §3.5 (autenticación real, verificada con evidencia directa contra
la documentación oficial: header `x-apisports-key`, base URL
`https://v3.football.api-sports.io`), §3.7 (límites del plan Free: 100
requests/día, sin restricción adicional confirmada más allá de la profundidad
de temporadas).

## Qué NO hace este módulo

No implementa reintentos con backoff, caché ni control de tasa (rate
limiting) más allá de exponer los encabezados de respuesta -- `docs/43`
§10 documenta esas políticas como parte de la implementación real de un
importador, no de este cliente mínimo; una misión futura puede envolver este
cliente con esa lógica sin modificarlo. No decide qué endpoints llamar --
eso es responsabilidad de cada importador (`selecciones_importer.py`,
`estadios_importer.py`, `jugadores_importer.py`). No se ejecutó contra la API
real durante `DATA-012` -- sin credencial disponible en esa sesión; toda
prueba de este módulo usa `httpx.MockTransport` (`tests/ingestion/`), nunca
la red real.
"""

from __future__ import annotations

from typing import Any, Protocol

import httpx

_BASE_URL = "https://v3.football.api-sports.io"
_HEADER_API_KEY = "x-apisports-key"


class ApiFootballError(RuntimeError):
    """Fallo real de comunicación con API-Football -- credencial ausente,
    error de red, HTTP distinto de 200, o el propio payload reporta errores
    en su campo `errors` (`docs/42` §3.5: `errors: []` en una respuesta
    exitosa). Nunca se traduce en un valor inventado -- el llamador decide
    qué hacer con el fallo (`docs/38` §5: "si el dato aún no ha sido
    confirmado... no se incorpora").
    """


class ApiFootballClientProtocol(Protocol):
    """Contrato estructural mínimo que necesita cada importador -- permite
    inyectar un doble de prueba sin depender de `httpx` en los tests de los
    importadores (mismo patrón de `Protocol` ya usado en
    `app/persistence/mu_gol_provider.py`).
    """

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]: ...


class ApiFootballClient:
    """Implementación real de `ApiFootballClientProtocol` sobre `httpx`."""

    def __init__(
        self,
        api_key: str,
        http_client: httpx.Client | None = None,
        timeout: float = 15.0,
    ) -> None:
        if not api_key:
            raise ApiFootballError(
                "API_FOOTBALL_KEY vacía -- configurar la variable de entorno antes de "
                "instanciar ApiFootballClient (ver .env.example). Nunca se intenta una "
                "llamada sin autenticar."
            )
        self._api_key = api_key
        self._client = http_client or httpx.Client(base_url=_BASE_URL, timeout=timeout)

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Ejecuta un `GET` autenticado. Devuelve el payload completo
        (`get`, `parameters`, `errors`, `results`, `paging`, `response`) tal
        como lo documenta `docs/42` §3 -- el llamador extrae `response`
        explícitamente, este método no lo hace por él para no ocultar
        `errors`/`paging` a quien sí los necesite.
        """
        try:
            respuesta = self._client.get(
                endpoint, params=params or {}, headers={_HEADER_API_KEY: self._api_key}
            )
        except httpx.HTTPError as exc:
            raise ApiFootballError(f"Fallo de red consultando '{endpoint}': {exc}") from exc

        if respuesta.status_code != 200:
            raise ApiFootballError(
                f"'{endpoint}' devolvió HTTP {respuesta.status_code}: {respuesta.text[:300]}"
            )

        payload = respuesta.json()
        errores = payload.get("errors")
        if errores:
            raise ApiFootballError(f"'{endpoint}' devolvió errores en el payload: {errores}")
        return payload

    def close(self) -> None:
        self._client.close()
