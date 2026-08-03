"""Pruebas de `ApiFootballClient` -- todas usan `httpx.MockTransport`, nunca
la red real (sin credencial disponible durante `DATA-012`).
"""

from __future__ import annotations

import httpx
import pytest

from app.ingestion.api_football_client import ApiFootballClient, ApiFootballError


def _client_con_transporte(handler) -> ApiFootballClient:
    transporte = httpx.MockTransport(handler)
    http_client = httpx.Client(base_url="https://v3.football.api-sports.io", transport=transporte)
    return ApiFootballClient(api_key="clave-de-prueba", http_client=http_client)


def test_get_envia_header_de_autenticacion_y_devuelve_el_payload() -> None:
    capturado: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        capturado["x-apisports-key"] = request.headers.get("x-apisports-key", "")
        return httpx.Response(200, json={"get": "venues", "errors": [], "response": [{"id": 556}]})

    cliente = _client_con_transporte(handler)
    payload = cliente.get("/venues", {"id": 556})

    assert capturado["x-apisports-key"] == "clave-de-prueba"
    assert payload["response"] == [{"id": 556}]


def test_api_key_vacia_falla_antes_de_cualquier_llamada() -> None:
    with pytest.raises(ApiFootballError, match="API_FOOTBALL_KEY"):
        ApiFootballClient(api_key="")


def test_http_distinto_de_200_lanza_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text="Too Many Requests")

    cliente = _client_con_transporte(handler)
    with pytest.raises(ApiFootballError, match="429"):
        cliente.get("/venues", {"id": 556})


def test_payload_con_errores_lanza_error_aunque_el_http_sea_200() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"get": "venues", "errors": {"id": "invalid"}, "response": []})

    cliente = _client_con_transporte(handler)
    with pytest.raises(ApiFootballError, match="errores"):
        cliente.get("/venues", {"id": "no-es-un-id"})


def test_fallo_de_red_se_traduce_en_apifootballerror() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("DNS no resuelve", request=request)

    cliente = _client_con_transporte(handler)
    with pytest.raises(ApiFootballError, match="Fallo de red"):
        cliente.get("/venues", {"id": 556})
