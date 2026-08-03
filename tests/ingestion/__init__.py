"""Pruebas de `app/ingestion` (`DATA-012`) -- ninguna toca la red real ni
`data/processed/selecciones-nacionales/` real: `ApiFootballClient` se prueba
con `httpx.MockTransport`, los importadores con un doble de prueba de
`ApiFootballClientProtocol`, y toda escritura de CSV usa `tmp_path`.
"""
