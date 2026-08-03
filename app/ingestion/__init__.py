"""`app/ingestion` -- Importadores de entidades maestras del Modelo Santiago.

Misión: **DATA-012**, primera implementación de código del Pipeline de Ingesta
diseñado (sin código) en `docs/43-Pipeline-de-Ingesta.md`. Referencias
revisadas antes de escribir: `docs/43` (arquitectura, orden de ejecución por
capas §3), `docs/44-Reconciliacion-del-Esquema.md` (clasificación
OBLIGATORIO/CONDICIONAL/OPCIONAL/DERIVADO/NO DISPONIBLE por campo, `GOV-003`),
`docs/38-Protocolo-Oficial-Ingesta-Datos.md` (reglas de aceptación/rechazo),
`docs/42-Verificacion-Manual-API-Football.md` (endpoints y campos verificados
con evidencia directa), `app/persistence/mu_gol_provider.py` y
`app/persistence/preparation_repository.py` (convenciones de lectura de CSV ya
aceptadas en este proyecto, reutilizadas aquí para la escritura).

## Alcance de DATA-012 (Capa 0 y Capa 1 del grafo de `docs/43` §3)

Implementa únicamente **Selecciones**, **Estadios** y **Jugadores** --
`selecciones_importer.py`, `estadios_importer.py`, `jugadores_importer.py`.
Partidos, Estadísticas de Partido, Convocatorias y Cuotas quedan **fuera de
alcance**, explícitamente prohibidos por el brief de esta misión -- no se
implementan aquí ni en ningún módulo de este paquete.

## Por qué un paquete nuevo, fuera de los nueve ya registrados en `docs/35`

`docs/35-Arquitectura-Oficial-del-Proyecto-Python.md` §3-4 enumera nueve
subpaquetes de `app/` (`api`, `runtime`, `engine`, `preparation`,
`persistence`, `models`, `schemas`, `services`, `config`) y asigna `scripts/`
como destino del *futuro* cargador CSV → PostgreSQL -- pero ninguno de los
nueve corresponde a "traer datos de una fuente externa hacia
`data/processed/`": `app/persistence` está definido explícitamente como
consumidor de datos ya existentes para el Engine (`docs/35` línea 152:
"Ejecutar consultas y escrituras contra PostgreSQL"), en dirección opuesta a
lo que este paquete hace. `docs/43-Pipeline-de-Ingesta.md` §5 ya anticipó que
un componente de este tipo "deberá diseñar[se] dentro de `app/`" sin asignarle
un paquete. Se documenta aquí, explícitamente, como una extensión de la
arquitectura no prevista por `docs/35` -- pendiente de que una futura misión
`GR-`/`AR-` la registre formalmente en ese documento (sincronización
documental, `docs/22` §6: se identifica, no se aplica en esta misión).

## Qué NO hace este paquete

No modifica `app/engine`, ninguna Variable Oficial ni ninguna fórmula del
modelo -- escribe exclusivamente en `data/processed/selecciones-nacionales/`,
nunca en `data/raw/` ni en la base de datos PostgreSQL (que sigue sin
poblarse). No inventa ningún valor: todo campo clasificado `CONDICIONAL` o
`NO DISPONIBLE` (`docs/44`) se deja vacío, nunca estimado ni interpolado.
"""
