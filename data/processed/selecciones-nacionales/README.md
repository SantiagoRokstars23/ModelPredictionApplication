# Módulo: Selecciones Nacionales

**Directorio:** `data/processed/selecciones-nacionales/`

**Versión:** 1.0.0

**Estado:** Activo (esquema aprobado, sin datos reales todavía)

---

# Objetivo

Este módulo constituye la primera implementación de la Base de Conocimiento (`docs/04-Base-de-Conocimiento.md`) para el dominio de selecciones nacionales de fútbol.

Define 11 entidades, cada una en su propio archivo CSV, siguiendo el esquema aprobado en la Misión 001.

---

# Decisiones arquitectónicas aplicadas

1. **Principio de Justificación de Datos**: cada campo de cada entidad está justificado explícitamente en este documento (ver tablas por entidad), conforme a `docs/04-Base-de-Conocimiento.md`.
2. **Ubicación**: se mantiene `data/processed/selecciones-nacionales/`.
3. **`campeon_id_seleccion` eliminado** de `torneos`: es un dato derivado (se obtiene consultando el partido con `fase = final` en `partidos.csv`), nunca se almacena para evitar duplicación.
4. **Sin estadísticas individuales de jugador** en esta misión (goles, asistencias, minutos jugados por jugador y partido). Queda explícitamente diferido a una misión futura.
5. **`id_torneo` nunca nulo**: se define la competición `Amistosos Internacionales` y un torneo contenedor por año calendario para partidos amistosos (ver sección dedicada más abajo).

---

# Convención: Amistosos Internacionales

Los partidos amistosos no pertenecen a un torneo con fase de grupos ni eliminatorias, pero **todo partido debe tener un `id_torneo` válido** para preservar la integridad referencial del modelo (regla aplicada en esta misión: evitar `id_torneo` nulo).

Se resuelve de la siguiente forma:

- Se crea **una única competición permanente** en `competiciones.csv`: `Amistosos Internacionales` (tipo `amistoso`, organizada por FIFA). No es periódica (`periodicidad_anios` queda vacío) porque no sigue un ciclo fijo.
- Se crea **un torneo contenedor por año calendario** en `torneos.csv` (ej. `TOR-2026-AMISTOSOS`, `fecha_inicio: 2026-01-01`, `fecha_fin: 2026-12-31`). Todo amistoso jugado ese año se asocia a ese `id_torneo`.
- La sede no es única (los amistosos se juegan en estadios distintos), por lo que `paises_organizadores` para estos torneos contenedor queda como `N/A (sede variable, ver partidos.id_estadio)`.
- `numero_selecciones_participantes` queda vacío para estos torneos, ya que no existe un conjunto fijo de participantes.

**Regla operativa:** al registrar el primer amistoso de un nuevo año calendario, se debe crear primero la fila correspondiente en `torneos.csv` (`TOR-<año>-AMISTOSOS`) antes de insertar el partido. Esta misión ya crea la fila para el año en curso (2026) como ejemplo del patrón.

**Nota de granularidad:** se eligió agrupar por año calendario (no por ventana FIFA de fecha internacional) por simplicidad, siguiendo la regla del proyecto de no incrementar la complejidad sin evidencia de que mejora el modelo (`CLAUDE.md`). Si en el futuro se demuestra que la granularidad por ventana FIFA aporta valor predictivo, se documentará como mejora en `models/` antes de modificar este esquema.

---

# Estado de los archivos

Todos los CSV de este módulo contienen únicamente la fila de encabezado, salvo `competiciones.csv` y `torneos.csv`, que incluyen la fila de referencia de "Amistosos Internacionales" descrita arriba (dato de catálogo/esquema, no dato observacional de un partido concreto). No se ha incorporado ningún dato real de partidos, jugadores ni estadísticas — cumpliendo la regla "nunca inventar datos" mientras no exista una fuente verificada.

---

# Entidades

## 1. `selecciones.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_seleccion` | STRING(3) | PK | Integridad referencial: identificador único usado por todas las entidades relacionadas |
| `nombre_pais` | STRING | | Identificación legible del equipo en reportes de predicción (`docs/06-predicciones.md`) |
| `nombre_federacion` | STRING | | Trazabilidad de la fuente oficial (`docs/04-Base-de-Conocimiento.md`: "toda fuente deberá ser identificable y verificable") |
| `confederacion` | ENUM | | Contextualiza viajes intercontinentales (Factores Externos, `docs/02-Variables.md`) y agrupación de clasificatorias |
| `ranking_fifa_actual` | INTEGER | | Proxy de fuerza general, usado como prior en `engine/03-Poisson.md` y `engine/05-Confidence.md` |
| `ranking_fifa_fecha` | DATE | | Vigencia del dato (`docs/04-Base-de-Conocimiento.md`: "Calidad de Datos → fecha de actualización") |
| `seleccionador_actual` | STRING | | Insumo cualitativo de Compatibilidad Táctica (Variable 005, `docs/02-Variables.md`) |
| `activa` | BOOLEAN | | Integridad del modelo: excluye federaciones inactivas de la predicción |

**Relaciones:** referenciada por `jugadores`, `convocatorias`, `partidos`, `estadisticas_partido`.
**Restricciones:** `id_seleccion` único, 3 letras mayúsculas; `ranking_fifa_actual` > 0; `ranking_fifa_fecha` no futura.

---

## 2. `jugadores.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_jugador` | STRING | PK | Integridad referencial (`convocatorias`, `lesiones`) |
| `nombre_completo` | STRING | | Trazabilidad |
| `nombre_conocido` | STRING | | Legibilidad en reportes |
| `fecha_nacimiento` | DATE | | Proxy de Fatiga/Calidad de Plantilla (edad, Variable 007/008) |
| `posicion_principal` | ENUM | | Insumo de Compatibilidad Táctica (Variable 005) |
| `pie_habil` | ENUM | | Insumo secundario de Compatibilidad Táctica |
| `altura_cm` | INTEGER | | Insumo de perfil físico en Compatibilidad Táctica (ej. juego aéreo) |
| `id_seleccion` | STRING | FK → `selecciones` | Integridad referencial; insumo de Disponibilidad de Plantilla |
| `club_actual` | STRING | | Contexto de carga competitiva, insumo de Fatiga (Variable 007) |
| `activo_seleccion` | BOOLEAN | | Integridad: evita convocatorias inválidas |

**Restricciones:** `id_jugador` único e inmutable; `fecha_nacimiento` no futura; un jugador solo puede tener una `id_seleccion` activa a la vez.

---

## 3. `convocatorias.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_convocatoria` | STRING | PK | Integridad referencial/trazabilidad |
| `id_torneo` | STRING | FK → `torneos` | Reconstruye Disponibilidad de Plantilla (Variable 006) por torneo |
| `id_seleccion` | STRING | FK → `selecciones` | Idem |
| `id_jugador` | STRING | FK → `jugadores` | Idem |
| `dorsal` | INTEGER | | Trazabilidad/identificación oficial |
| `posicion_convocatoria` | ENUM | | Refina Compatibilidad Táctica para el torneo específico |
| `fecha_convocatoria` | DATE | | Vigencia del dato; insumo de Estado Psicológico (tensión por convocatoria tardía) |
| `estado_convocatoria` | ENUM | | Insumo directo de Disponibilidad de Plantilla (bajas antes/durante el torneo) |

**Restricciones:** único (`id_torneo`, `id_seleccion`, `id_jugador`); único (`id_torneo`, `id_seleccion`, `dorsal`).

---

## 4. `partidos.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_partido` | STRING | PK | Integridad referencial: entidad central del sistema |
| `id_torneo` | STRING | FK → `torneos` (nunca nulo) | Insumo de Rendimiento en el Torneo (Variable 002) y de Índice de Caos |
| `id_seleccion_local` | STRING | FK → `selecciones` | Insumo de Localía (Variable 009) |
| `id_seleccion_visitante` | STRING | FK → `selecciones` | Idem |
| `id_estadio` | STRING | FK → `estadios` | Insumo de Factores Externos (altitud, clima) |
| `id_arbitro` | STRING | FK → `arbitros` | Insumo de Factores Externos (Variable 012) |
| `fecha` | DATE | | Insumo de Forma Reciente (Variable 001) y Fatiga (descanso entre partidos) |
| `hora_local` | STRING | | Insumo secundario de Factores Externos (calor/humedad según franja horaria) |
| `fase` | ENUM | | Insumo de Índice de Caos (`engine/04-Chaos-Index.md`) y Estado Psicológico |
| `jornada` | INTEGER | | Contextualiza Rendimiento en el Torneo |
| `goles_local` | INTEGER | | Resultado oficial, base de `docs/07-Auditoria.md` |
| `goles_visitante` | INTEGER | | Idem |
| `estado_partido` | ENUM | | Filtra partidos válidos para el cálculo de variables |
| `asistencia` | INTEGER | | Insumo secundario de Estado Psicológico/presión ambiental |

**Campo excluido:** `resultado_final`/`ganador` — se deriva de `goles_local` vs. `goles_visitante`.
**Restricciones:** `id_seleccion_local` ≠ `id_seleccion_visitante`; goles solo se completan si `estado_partido = finalizado`; `jornada` obligatorio solo si `fase = fase_grupos`; `id_torneo` es **obligatorio siempre** (ver convención de Amistosos Internacionales).

---

## 5. `estadisticas_partido.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_estadistica_partido` | STRING | PK | Integridad referencial |
| `id_partido` | STRING | FK → `partidos` | Relación obligatoria |
| `id_seleccion` | STRING | FK → `selecciones` | Idem |
| `xg` | DECIMAL | | Insumo directo de Potencial Ofensivo (Variable 003) y `engine/01-Offensive-Strength.md` |
| `posesion_pct` | DECIMAL | | Insumo de Compatibilidad Táctica (Variable 005) |
| `disparos_totales` | INTEGER | | Insumo directo de Potencial Ofensivo (Variable 003) |
| `disparos_al_arco` | INTEGER | | Idem |
| `corners` | INTEGER | | Proxy secundario de dominio ofensivo |
| `faltas_cometidas` | INTEGER | | Insumo de Índice de Caos (indisciplina como imprevisibilidad) |
| `tarjetas_amarillas` | INTEGER | | Idem, y base para futura Disponibilidad de Plantilla por acumulación |
| `tarjetas_rojas` | INTEGER | | Idem |
| `pases_completados` | INTEGER | | Insumo de Compatibilidad Táctica (estilo de posesión/juego directo) |
| `precision_pases_pct` | DECIMAL | | Idem |

**Campo excluido:** `xga` — es idéntico al `xg` del rival en el mismo `id_partido`; se obtiene con un self-join, nunca se duplica.
**Restricciones:** único (`id_partido`, `id_seleccion`); `posesion_pct` 0-100; `disparos_al_arco` ≤ `disparos_totales`.

---

## 6. `lesiones.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_lesion` | STRING | PK | Integridad referencial |
| `id_jugador` | STRING | FK → `jugadores` | Insumo de Disponibilidad de Plantilla (Variable 006) |
| `tipo_lesion` | STRING | | Calibra el impacto real en Disponibilidad |
| `gravedad` | ENUM | | Idem |
| `fecha_inicio` | DATE | | Permite calcular disponibilidad exacta por partido/convocatoria |
| `fecha_estimada_retorno` | DATE | | Idem |
| `fecha_retorno_real` | DATE | | Idem |
| `id_partido_origen` | STRING | FK → `partidos` (opcional) | Trazabilidad del origen de la lesión |
| `estado` | ENUM | | Filtra lesiones activas vs. resueltas |
| `fuente` | STRING | | Regla "nunca inventar datos": la fuente debe ser verificable |

**Campo excluido:** `id_seleccion` — se deriva de `jugadores.id_jugador`.
**Restricciones:** `fecha_estimada_retorno` ≥ `fecha_inicio`; `fecha_retorno_real` solo si `estado = recuperado`; `fuente` obligatoria.

---

## 7. `cuotas.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_cuota` | STRING | PK | Integridad referencial |
| `id_partido` | STRING | FK → `partidos` | Relación obligatoria |
| `casa_apuestas` | STRING | | Trazabilidad de la fuente |
| `mercado` | ENUM | | Define qué probabilidad de mercado se compara en `engine/06-Expected-Value.md` |
| `seleccion_o_resultado` | STRING | | Idem |
| `cuota_decimal` | DECIMAL | | Insumo directo de `engine/06-Expected-Value.md` |
| `fecha_captura` | DATE+hora | | Las cuotas varían en el tiempo; se necesita la vigente al momento de la predicción |
| `estado_cuota` | ENUM | | Filtra cuotas abiertas de las cerradas/suspendidas |

**Campo excluido:** `probabilidad_implicita` — se calcula en `engine/06-Expected-Value.md`, no es un dato bruto.
**Restricciones:** `cuota_decimal` > 1.00; unicidad real = (`id_partido`, `casa_apuestas`, `mercado`, `seleccion_o_resultado`, `fecha_captura`).

---

## 8. `arbitros.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_arbitro` | STRING | PK | Integridad referencial |
| `nombre_completo` | STRING | | Trazabilidad |
| `nacionalidad` | STRING | | Contexto de Factores Externos (sesgo potencial, solo con evidencia) |
| `confederacion_arbitral` | ENUM | | Calibra la fiabilidad del dato (exigencia distinta por panel) |
| `categoria` | ENUM | | Idem |
| `activo` | BOOLEAN | | Filtra árbitros vigentes |

**Restricciones:** `nombre_completo` obligatorio; `categoria = fifa_internacional` requerido en torneos FIFA/confederación.

---

## 9. `estadios.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_estadio` | STRING | PK | Integridad referencial |
| `nombre` | STRING | | Trazabilidad/contexto |
| `ciudad` | STRING | | Idem |
| `pais` | STRING | | Idem |
| `capacidad` | INTEGER | | Proxy de Estado Psicológico/presión ambiental |
| `tipo_superficie` | ENUM | | Insumo de Factores Externos (Variable 012: estado del campo) |
| `altitud_metros` | INTEGER | | Insumo directo de Factores Externos (Variable 012: altitud) |
| `techado` | BOOLEAN | | Insumo de Factores Externos (anula la variable clima si es techado) |

**Restricciones:** `capacidad` > 0; `altitud_metros` puede ser negativo.

---

## 10. `competiciones.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_competicion` | STRING | PK | Integridad referencial |
| `nombre` | STRING | | Trazabilidad/legibilidad |
| `confederacion_organizadora` | ENUM | | Contextualiza el nivel de exigencia esperado |
| `tipo` | ENUM | | Insumo directo de Índice de Caos y de la ponderación por tipo de partido (`docs/01-modelo.md`, Niveles A-D) |
| `periodicidad_anios` | INTEGER | | Contextualiza relevancia competitiva (vacío si `tipo = amistoso`) |
| `activa` | BOOLEAN | | Filtra competiciones vigentes |

**Datos de catálogo incluidos en esta misión:** fila `Amistosos Internacionales` (ver convención dedicada).

---

## 11. `torneos.csv`

| Campo | Tipo | Clave | Justificación |
|---|---|---|---|
| `id_torneo` | STRING | PK | Integridad referencial (obligatorio en `partidos`, nunca nulo) |
| `id_competicion` | STRING | FK → `competiciones` | Relación obligatoria |
| `edicion` | STRING | | Trazabilidad/legibilidad temporal |
| `paises_organizadores` | STRING | | Insumo de Factores Externos (sede única vs. multisede afecta Localía, Variable 009) |
| `fecha_inicio` | DATE | | Delimita la ventana temporal de Rendimiento en el Torneo (Variable 002) |
| `fecha_fin` | DATE | | Idem |
| `formato` | STRING | | Contextualiza Índice de Caos (grupos + eliminación directa vs. liga) |
| `numero_selecciones_participantes` | INTEGER | | Contextualiza el nivel competitivo (vacío si `tipo` de la competición es `amistoso`) |

**Campo eliminado (decisión de esta misión):** `campeon_id_seleccion` — dato derivado de `partidos` (fila con `fase = final`), nunca almacenado.
**Restricciones:** `fecha_fin` ≥ `fecha_inicio`.
**Datos de catálogo incluidos en esta misión:** fila `TOR-2026-AMISTOSOS` (ver convención dedicada).

---

# Próximos pasos (fuera de esta misión)

- Misión futura: estadísticas individuales de jugador por partido (goles, asistencias, minutos jugados, tarjetas), explícitamente diferida por decisión de esta misión.
- Incorporación de datos reales validados desde `data/raw/` siguiendo el flujo de `docs/04-Base-de-Conocimiento.md`.
