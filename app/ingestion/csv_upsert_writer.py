"""`CsvUpsertWriter` -- escritura idempotente en un CSV de
`data/processed/selecciones-nacionales/` a partir de una clave de negocio.

Referencia de autoridad: `docs/38-Protocolo-Oficial-Ingesta-Datos.md` §7
("Convención de actualización" -- fila nueva se agrega, corrección de un
valor ya incorporado se corrige sin perder trazabilidad, nunca se elimina una
fila ya escrita) y el requisito explícito de `DATA-012`: "Ejecutar dos veces
el importador no debe duplicar registros".

## Cómo se logra la idempotencia

Cada importador identifica una columna como clave de negocio (`id_seleccion`,
`id_estadio`, `id_jugador`) y la deriva de forma **determinística** a partir
del identificador externo de API-Football (ver cada importador). Con eso, la
misma fila externa produce siempre la misma clave interna -- este escritor
solo necesita, en cada ejecución, leer el CSV existente, indexarlo por esa
clave, y decidir por cada fila nueva si es un alta (`creados`) o una
actualización de una fila ya existente (`actualizados`/`conservados`); nunca
duplica.

`docs/43-Pipeline-de-Ingesta.md` §5 anticipaba una "tabla de correspondencia
de identificadores externos" como componente de soporte separado -- este
escritor no la necesita: al derivar la clave de negocio de forma
determinística, la propia clave *es* la correspondencia, sin infraestructura
adicional (`CLAUDE.md`: "si una mejora aumenta la complejidad sin mejorar el
modelo, deberá descartarse" -- aplicado aquí a favor de la opción más simple).

## Política de Preservación (`DATA-012B` §1)

Hallazgo de la preparación de `DATA-012A`: `selecciones.csv` ya tiene 62
filas curadas manualmente con `nombre_federacion`/`confederacion`/
`ranking_fifa_*` completos; el importador siempre entrega esos campos vacíos
(sin fuente confirmada, `docs/44` §2). Sin una regla de preservación, la
sobrescritura de fila completa habría borrado esos valores reales en la
primera ejecución contra la API real -- exactamente lo que este escritor
existe para impedir (`docs/38` §7).

La regla se aplica **columna por columna**, para cualquier entidad, no solo
Selecciones: si el valor nuevo llega vacío (`app/ingestion/valores.py::es_vacio`)
y el valor ya almacenado no lo está, se conserva el valor ya almacenado. En
cualquier otro caso (el valor nuevo no está vacío, sea igual o distinto al
anterior) se usa el valor nuevo. Nunca ocurre "dato válido → NULL".

Una fila cuya combinación resulta idéntica a la ya almacenada se cuenta como
`conservados` (nada cambió realmente); una fila cuya combinación difiere se
cuenta como `actualizados`. Esto también resuelve, sin lógica adicional, el
caso de "completar un campo antes vacío" (CSV `NULL` + API con valor →
`actualizados`, el valor nuevo se adopta porque no hay nada que preservar).

## Qué NO hace este módulo

No valida los datos -- eso ya ocurrió antes de que una fila llegue aquí
(`app/ingestion/calidad.py`, y la validación propia de cada importador). No
decide qué archivo escribir ni con qué encabezado -- ambos los declara el
importador que lo invoca. No escribe a `data/raw/` bajo ninguna circunstancia.
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path

from app.ingestion.valores import es_vacio

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResumenEscritura:
    creados: int = 0
    actualizados: int = 0
    conservados: int = 0
    omitidos: int = 0
    advertencias: tuple[str, ...] = field(default_factory=tuple)
    errores: tuple[str, ...] = field(default_factory=tuple)


class CsvUpsertWriter:
    """Escribe filas (`dict[str, str]`) en un CSV de
    `data/processed/selecciones-nacionales/`, indexadas por una columna de
    clave de negocio -- nunca duplica, nunca reordena columnas respecto al
    encabezado ya declarado por el importador.
    """

    def __init__(self, ruta_archivo: Path, columnas: tuple[str, ...], clave_negocio: str) -> None:
        if clave_negocio not in columnas:
            raise ValueError(
                f"La clave de negocio '{clave_negocio}' debe ser una de las columnas declaradas: {columnas}"
            )
        self._ruta = ruta_archivo
        self._columnas = columnas
        self._clave = clave_negocio

    def upsert(self, filas: list[dict[str, str]], simular: bool = False) -> ResumenEscritura:
        """Aplica todas las filas de un lote de importación en una sola
        pasada. Una fila cuya clave de negocio está vacía se omite (no puede
        indexarse) -- se registra como advertencia, nunca detiene el resto
        del lote.

        `simular=True` (Dry Run, `DATA-012B` §4): calcula el mismo
        `ResumenEscritura` que produciría la ejecución real -- incluida la
        Política de Preservación -- pero nunca llama a `_escribir`, por lo
        que ningún archivo se crea ni se modifica.
        """
        existentes = self.leer_existentes()
        creados = 0
        actualizados = 0
        conservados = 0
        omitidos = 0
        advertencias: list[str] = []
        errores: list[str] = []

        for fila in filas:
            clave = (fila.get(self._clave) or "").strip()
            if not clave:
                omitidos += 1
                mensaje = f"Fila omitida: '{self._clave}' vacío ({fila})"
                advertencias.append(mensaje)
                logger.warning(mensaje)
                continue

            faltantes = set(self._columnas) - set(fila.keys())
            if faltantes:
                omitidos += 1
                mensaje = f"Fila '{clave}' omitida: columnas no declaradas en el escritor: {faltantes}"
                errores.append(mensaje)
                logger.error(mensaje)
                continue

            if clave in existentes:
                combinada = self._combinar(existentes[clave], fila)
                if combinada != existentes[clave]:
                    actualizados += 1
                    logger.info("Registro '%s' actualizado en '%s'", clave, self._ruta.name)
                else:
                    conservados += 1
                existentes[clave] = combinada
            else:
                creados += 1
                logger.info("Registro '%s' creado en '%s'", clave, self._ruta.name)
                existentes[clave] = fila

        if not simular:
            self._escribir(existentes)
        return ResumenEscritura(
            creados=creados,
            actualizados=actualizados,
            conservados=conservados,
            omitidos=omitidos,
            advertencias=tuple(advertencias),
            errores=tuple(errores),
        )

    def _combinar(self, existente: dict[str, str], nueva: dict[str, str]) -> dict[str, str]:
        """Política de Preservación (`DATA-012B` §1), aplicada columna por
        columna: un valor nuevo vacío nunca sobrescribe un valor existente no
        vacío. Genérica -- no conoce el nombre de ninguna columna en
        particular, funciona igual para cualquier entidad.
        """
        combinada: dict[str, str] = {}
        for columna in self._columnas:
            valor_nuevo = nueva.get(columna, "")
            valor_existente = existente.get(columna, "")
            if es_vacio(valor_nuevo) and not es_vacio(valor_existente):
                combinada[columna] = valor_existente
            else:
                combinada[columna] = valor_nuevo
        return combinada

    def leer_existentes(self) -> dict[str, dict[str, str]]:
        """Público (antes `_leer_existentes`) -- `EstadiosImporter`
        (`DATA-012B` §2) lo necesita para construir su índice de
        emparejamiento por nombre/país *antes* de decidir la clave de
        negocio de cada fila nueva, no solo `upsert()` internamente.
        """
        if not self._ruta.exists():
            return {}
        with self._ruta.open(newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return {
                fila[self._clave]: fila
                for fila in lector
                if fila.get(self._clave)
            }

    def _escribir(self, filas_por_clave: dict[str, dict[str, str]]) -> None:
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        filas_ordenadas = sorted(filas_por_clave.values(), key=lambda f: f[self._clave])
        with self._ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=list(self._columnas))
            escritor.writeheader()
            for fila in filas_ordenadas:
                escritor.writerow({columna: fila.get(columna, "") for columna in self._columnas})
