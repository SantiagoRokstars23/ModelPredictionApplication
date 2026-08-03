"""`JugadoresImporter` -- construye `jugadores.csv` combinando
`GET /players/squads` (plantilla, posición, dorsal -- `docs/42-Verificacion-
Manual-API-Football.md` §3.16, objeto real del Manchester United leído en su
totalidad) y `GET /players` (perfil: nombre, fecha de nacimiento, altura --
`docs/42` §3.20, objeto real de Neymar leído en su totalidad).

## Por qué dos llamadas, no una

`/players/squads` no incluye fecha de nacimiento, altura ni nombre completo
(objeto confirmado: `id, name, age, number, position, photo` -- 6 campos,
ninguno de perfil completo). `/players` sí los tiene, pero no incluye
`position` de forma confirmada (`docs/43` §6.5: el perfil base de `/players`
leído en `DATA-010A` termina en `photo`, sin `position`; ese campo solo se
confirmó vía `/players/squads`). Combinar ambos endpoints es la única forma
de poblar `posicion_principal` y `fecha_nacimiento` en la misma fila con
evidencia real para cada campo, en lugar de asumir que un único endpoint los
tiene todos.

## Brecha de evidencia no resuelta aquí

La combinación exacta de parámetros `GET /players?id={id}&season={temporada}`
no fue probada contra la API real en ninguna misión anterior (`FII-003`/
`DATA-010A` no ejecutaron esa llamada puntual) -- se documenta como una
suposición razonable basada en el patrón `id`+`season` ya confirmado en otros
endpoints (`/teams`, `/venues`), no como un hecho verificado. El mapeo es
defensivo (`dict.get(...)`) por la misma razón.

## Clasificación aplicada (`docs/44-Reconciliacion-del-Esquema.md` §3.3)

| Campo | Clasificación | Razón |
|---|---|---|
| `nombre_completo`, `fecha_nacimiento`, `posicion_principal`, `id_seleccion` | OBLIGATORIO | Fuente confirmada |
| `nombre_conocido`, `altura_cm`, `club_actual` | OPCIONAL | Fuente confirmada, no bloqueante |
| `pie_habil` | **NO DISPONIBLE** | Confirmado ausente (`DATA-010A` §3.20) -- queda vacío igual que un campo CONDICIONAL, nunca inventado |
| `activo_seleccion` | DERIVADO | `True` porque el jugador proviene de la plantilla actual (`/players/squads`) de la selección consultada |

## Límite por minuto (`DATA-012A`, primera ejecución contra la API real)

Hallazgo no documentado por ninguna misión anterior (`docs/42`/`docs/43` solo
registraban el límite de 100 requests/día del plan Free): API-Football
también aplica un límite **por minuto**. Este importador llama a `/players`
una vez por jugador de la plantilla en secuencia, sin ninguna pausa -- contra
la API real, una plantilla de ~25 jugadores agota ese límite antes de
terminar, y cada llamada rechazada con HTTP 429 deja al jugador
correspondiente `INCOMPLETO` (falta `nombre_completo`/`fecha_nacimiento`),
no por ausencia real de dato. `_PAUSA_ENTRE_LLAMADAS_SEGUNDOS` introduce una
pausa fija y conservadora antes de cada llamada a `/players` -- se trata como
corrección de un error de ejecución (`DATA-012A`, alcance permitido), no
como una política de reintentos/backoff nueva: no hay reintento, solo
espaciado; una implementación de backoff more completa queda, igual que
antes, para una misión futura dedicada (ver `api_football_client.py`).
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from app.ingestion.api_football_client import ApiFootballClientProtocol, ApiFootballError
from app.ingestion.calidad import CalidadRegistro, evaluar_calidad
from app.ingestion.csv_upsert_writer import CsvUpsertWriter, ResumenEscritura

logger = logging.getLogger(__name__)

_PAUSA_ENTRE_LLAMADAS_SEGUNDOS = 6.5

COLUMNAS = (
    "id_jugador",
    "nombre_completo",
    "nombre_conocido",
    "fecha_nacimiento",
    "posicion_principal",
    "pie_habil",
    "altura_cm",
    "id_seleccion",
    "club_actual",
    "activo_seleccion",
)
CAMPOS_OBLIGATORIOS = (
    "id_jugador",
    "nombre_completo",
    "fecha_nacimiento",
    "posicion_principal",
    "id_seleccion",
)
# pie_habil se trata igual que un campo CONDICIONAL para efectos de calidad de
# registro (docs/44 clasifica NO DISPONIBLE en lugar de CONDICIONAL, pero
# ambos comparten la misma consecuencia operativa: queda vacío, no bloquea).
CAMPOS_CONDICIONALES = ("pie_habil",)
_ARCHIVO = "jugadores.csv"
_PREFIJO_ID = "JUG"
_PATRON_ALTURA = re.compile(r"(\d+)")


@dataclass(frozen=True)
class ResumenImportacionJugadores:
    escritura: ResumenEscritura
    completos: int = 0
    condicionales: int = 0
    incompletos: int = 0


class JugadoresImporter:
    """Importa la plantilla actual de una selección. `id_seleccion` debe ser
    una clave ya resuelta (por ejemplo, la producida por
    `SeleccionesImporter`) -- este importador no inventa ni valida la
    existencia de la selección más allá de exigir que no esté vacía; la
    integridad referencial real ocurre al escribir en `jugadores.csv`
    (`docs/38` §6: "FK inexistente" es responsabilidad de quien orquesta el
    orden de ejecución del pipeline, `docs/43` §3 Capa 1).
    """

    def __init__(
        self,
        cliente: ApiFootballClientProtocol,
        data_dir: Path | None = None,
        pausa_segundos: float = _PAUSA_ENTRE_LLAMADAS_SEGUNDOS,
    ) -> None:
        self._cliente = cliente
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )
        self._pausa_segundos = pausa_segundos

    def importar(
        self,
        team_id_externo: int,
        id_seleccion: str,
        temporada: int,
        dry_run: bool = False,
    ) -> ResumenImportacionJugadores:
        """`dry_run=True` (`DATA-012B` §4): consulta la API igual, pero no
        escribe `jugadores.csv`.
        """
        if not id_seleccion.strip():
            raise ValueError("id_seleccion no puede estar vacío -- FK obligatoria de jugadores.csv")

        try:
            payload_squad = self._cliente.get("/players/squads", {"team": team_id_externo})
        except ApiFootballError as exc:
            logger.error("No se pudo consultar /players/squads?team=%s: %s", team_id_externo, exc)
            return ResumenImportacionJugadores(escritura=ResumenEscritura())

        respuesta_squad = payload_squad.get("response", [])
        if not respuesta_squad:
            logger.warning(
                "'/players/squads?team=%s' no devolvió ninguna plantilla -- se omite.",
                team_id_externo,
            )
            return ResumenImportacionJugadores(escritura=ResumenEscritura())

        jugadores_squad = respuesta_squad[0].get("players", [])

        filas: list[dict[str, str]] = []
        completos = 0
        condicionales = 0
        incompletos = 0

        for jugador_squad in jugadores_squad:
            id_externo = jugador_squad.get("id")
            if id_externo is None:
                incompletos += 1
                logger.error("Jugador sin 'id' en /players/squads -- omitido, nunca se inventa un id.")
                continue

            perfil = self._obtener_perfil(id_externo, temporada)
            fila = self._mapear(jugador_squad, perfil, id_seleccion)
            resultado = evaluar_calidad(fila, CAMPOS_OBLIGATORIOS, CAMPOS_CONDICIONALES)

            if resultado.calidad is CalidadRegistro.INCOMPLETO:
                incompletos += 1
                logger.error(
                    "Jugador externo %s omitido (INCOMPLETO): faltan %s",
                    id_externo,
                    resultado.campos_obligatorios_faltantes,
                )
                continue

            if resultado.calidad is CalidadRegistro.CONDICIONAL:
                condicionales += 1
            else:
                completos += 1
            filas.append(fila)

        escritura = CsvUpsertWriter(
            self._data_dir / _ARCHIVO, COLUMNAS, clave_negocio="id_jugador"
        ).upsert(filas, simular=dry_run)

        return ResumenImportacionJugadores(
            escritura=escritura,
            completos=completos,
            condicionales=condicionales,
            incompletos=incompletos,
        )

    def _obtener_perfil(self, id_externo: int, temporada: int) -> dict:
        """Perfil completo de `/players` -- `{}` si la llamada falla o no
        devuelve nada, nunca una excepción que detenga el resto de la
        plantilla (un jugador sin perfil disponible queda INCOMPLETO
        individualmente, el resto de la importación continúa).

        Pausa antes de cada llamada (`self._pausa_segundos`, por defecto
        `_PAUSA_ENTRE_LLAMADAS_SEGUNDOS`, ver docstring del módulo) --
        espaciado fijo, no reintento, para respetar el límite por minuto
        descubierto en `DATA-012A`. Las pruebas la desactivan (`pausa_segundos=0`)
        para no ralentizar la suite con dobles de prueba que nunca golpean la
        red real.
        """
        time.sleep(self._pausa_segundos)
        try:
            payload = self._cliente.get("/players", {"id": id_externo, "season": temporada})
        except ApiFootballError as exc:
            logger.warning("No se pudo consultar /players?id=%s: %s", id_externo, exc)
            return {}
        respuesta = payload.get("response", [])
        return respuesta[0] if respuesta else {}

    @staticmethod
    def _mapear(jugador_squad: dict, perfil: dict, id_seleccion: str) -> dict[str, str]:
        datos_perfil = perfil.get("player") or {}
        estadisticas = perfil.get("statistics") or []
        club_actual = ""
        if estadisticas:
            equipo = (estadisticas[0] or {}).get("team") or {}
            club_actual = (equipo.get("name") or "").strip()

        nombre_completo = " ".join(
            parte
            for parte in (datos_perfil.get("firstname"), datos_perfil.get("lastname"))
            if parte
        ).strip()

        return {
            "id_jugador": f"{_PREFIJO_ID}-{jugador_squad.get('id')}",
            "nombre_completo": nombre_completo,
            "nombre_conocido": (datos_perfil.get("name") or "").strip(),
            "fecha_nacimiento": JugadoresImporter._normalizar_fecha(
                (datos_perfil.get("birth") or {}).get("date")
            ),
            "posicion_principal": (jugador_squad.get("position") or "").strip(),
            # NO DISPONIBLE (docs/44 §3.3) -- confirmado ausente, nunca inventado
            "pie_habil": "",
            "altura_cm": JugadoresImporter._normalizar_altura(datos_perfil.get("height")),
            "id_seleccion": id_seleccion,
            "club_actual": club_actual,
            # DERIVADO -- proviene de la plantilla actual consultada
            "activo_seleccion": "true",
        }

    @staticmethod
    def _normalizar_fecha(fecha_raw: object) -> str:
        if not isinstance(fecha_raw, str):
            return ""
        try:
            return date.fromisoformat(fecha_raw.strip()).isoformat()
        except ValueError:
            logger.warning("Fecha de nacimiento con formato inesperado, descartada: %r", fecha_raw)
            return ""

    @staticmethod
    def _normalizar_altura(altura_raw: object) -> str:
        if not isinstance(altura_raw, str):
            return ""
        coincidencia = _PATRON_ALTURA.search(altura_raw)
        return coincidencia.group(1) if coincidencia else ""
