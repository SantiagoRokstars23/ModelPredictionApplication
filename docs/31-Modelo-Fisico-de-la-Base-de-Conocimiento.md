# Modelo Físico Oficial de la Base de Conocimiento del Modelo Santiago

**Archivo:** `docs/31-Modelo-Fisico-de-la-Base-de-Conocimiento.md`

**Misión:** DATA-003 — Modelo Físico Oficial de la Base de Conocimiento del Modelo Santiago

**Versión:** 1.0.0

**Estado:** Especificación oficial — modelo conceptual de datos (sin implementación)

---

# Objetivo

`docs/05-Base-de-Conocimiento.md` ya define **el flujo** de los datos (Recolección → Validación → Normalización → Almacenamiento) y **la estructura de directorios** (`raw/`, `processed/`, `predictions/`, `results/`, `audit/`, `archive/`). `data/processed/selecciones-nacionales/README.md` ya define, campo por campo, **el esquema físico** de 11 entidades concretas. Ninguno de los dos documentos responde todavía una pregunta intermedia: **¿qué grandes dominios de conocimiento existen dentro del sistema, y cómo se relacionan conceptualmente entre sí?**

Ese es el vacío que cierra esta misión — el **Modelo Físico Oficial**, entendido en el sentido en que lo usa el brief (qué conjuntos de información existen y cómo se relacionan conceptualmente), no en el sentido de un modelo físico de base de datos relacional (tablas, claves, índices). Este documento se ubica, en nivel de abstracción, **entre** `docs/05` (el flujo y las reglas) y `data/processed/selecciones-nacionales/README.md` (el esquema campo por campo) — y sirve, además, para fijar con precisión el límite entre la Base de Conocimiento y la maquinaria de ejecución ya especificada en `docs/26`/`docs/29`/`docs/30`.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué NO repite este documento |
|---|---|---|
| `docs/05-Base-de-Conocimiento.md` | Flujo de datos, estructura de directorios, responsabilidad de cada uno, Principio de Justificación de Datos | Ninguna regla nueva de flujo o validación — se referencian tal cual |
| `docs/06-Flujo-Operacional.md` | Fases del flujo operacional e integración con `data/` | No se redefine ninguna fase |
| `docs/14-Prediction-Pipeline.md` | Orden exacto de lectura de los 11 archivos, actualización de la Base de Conocimiento al finalizar el partido | Se reutiliza como evidencia del orden de dependencia entre dominios (sección 4), sin repetir la tabla completa |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | Que la Base de Conocimiento nunca entrega datos directamente a los motores | Se reafirma como regla de frontera (sección 7), sin repetir su diseño interno |
| `docs/16-Contrato-Oficial-de-Variables.md` | Tipo, unidad, rango de las 12 Variables Oficiales | Ninguna variable se redefine — se referencia como el contrato que consume, no que compite con este documento |
| `docs/25`/`docs/26`/`docs/29`/`docs/30` | Objeto de entrada, Runtime, sus componentes, y la estructura completa del `PredictionContext` | Nada de esto se repite — se usa para trazar, en la sección 7, la frontera exacta entre lo permanente (este documento) y lo transitorio (`docs/30`) |
| `docs/27-Auditoria-de-Variables-Pendientes.md`, `docs/28-Catalogo-de-Variables-Derivadas.md` | Qué datos existen hoy, cuáles faltan, y el catálogo completo de cantidades derivadas | Se referencian como evidencia de que cada dominio aquí definido ya fue auditado dato por dato; no se repite ninguna de sus dos tablas |
| `docs/99-Mapa-Maestro.md` | Vista de alto nivel de todo el proyecto | Este documento profundiza específicamente en `data/`, que `docs/99` solo resume en una fila de su mapa de directorios |
| `data/processed/selecciones-nacionales/README.md` | Esquema campo por campo de las 11 entidades | No se repite ningún campo — se agrupan las entidades en dominios conceptuales de mayor nivel |

Ninguna inconsistencia detectada durante este análisis se corrige aquí — se documenta en "Observaciones", al final.

---

# 1. Propósito

La Base de Conocimiento (`data/`) es la **memoria permanente** del Modelo Santiago: el único conjunto de información que el sistema reconoce como verdadero y disponible para generar predicciones (`docs/05`, "Principio Fundamental"). Representa dos cosas conceptualmente distintas, ambas bajo el mismo directorio:

1. **Conocimiento del mundo** — lo que el modelo sabe sobre selecciones, jugadores, partidos, competiciones y mercado (`raw/`, `processed/`).
2. **Conocimiento sobre sí mismo** — lo que el modelo ha predicho, lo que realmente ocurrió, y qué tan bien predijo (`predictions/`, `results/`, `audit/`).

Ambas categorías son igual de permanentes e igual de auditables — ninguna es más "real" que la otra dentro del sistema.

---

# 2. Principios

| Principio | Qué significa para la Base de Conocimiento |
|---|---|
| **Única fuente de verdad** | Ningún dato usado por el Engine puede existir fuera de `data/processed/`; ningún componente mantiene su propia copia paralela de un dato ya presente aquí (`docs/05`, "Principio Fundamental") |
| **Inmutabilidad** | `data/raw/` nunca se modifica una vez recolectado; `data/results/` y `data/audit/` nunca se modifican una vez escritos; `data/archive/` nunca se elimina (`docs/05`, `docs/14`, "Información que nunca debe sobrescribirse") |
| **Trazabilidad** | Todo dato debe poder rastrearse hasta su fuente original y su fecha de captura (`docs/05`, "Calidad de Datos"; Constitución Art. 8) |
| **Reproducibilidad** | Con el mismo estado de la Base de Conocimiento en un instante dado, cualquier predicción debe poder reconstruirse de forma idéntica (Constitución Art. 2.3) |
| **Separación entre conocimiento histórico y ejecución** | La Base de Conocimiento es permanente y existe independientemente de que haya una predicción en curso; el `PredictionContext` (`docs/30`) es transitorio y existe solo durante una ejecución — desarrollado en la sección 7 |
| **Versionado** | Ningún dato se sobrescribe silenciosamente; toda corrección relevante queda registrada, y la Base de Conocimiento en sí puede evolucionar de tecnología sin afectar al Engine (`docs/05`, "Versionado"/"Evolución"; `docs/15` §9) |

---

# 3. Dominios de Información

La lista de ejemplo del brief agrupa varias entidades físicas bajo una misma etiqueta (ej. "Estadísticas" cubriría hoy tanto `estadisticas_partido.csv` como, implícitamente, `lesiones.csv`). Este documento prefiere **un dominio por responsabilidad única** (mismo principio que `CLAUDE.md`: "Toda entidad deberá tener una única responsabilidad"), lo que produce 13 dominios en lugar de 11 — extensión explícitamente permitida por el brief ("sin asumir que esta sea la lista final").

| # | Dominio | Entidad(es) física(s) hoy | Responsabilidad única |
|---|---|---|---|
| 1 | **Equipos** | `selecciones.csv` | Identidad y fuerza declarada de cada selección nacional |
| 2 | **Jugadores** | `jugadores.csv` | Identidad y atributos individuales de cada futbolista |
| 3 | **Convocatorias** | `convocatorias.csv` | Qué jugadores representan a un equipo en un torneo concreto |
| 4 | **Partidos** | `partidos.csv` | El enfrentamiento en sí: quién, cuándo, dónde, con qué resultado — entidad central del sistema |
| 5 | **Estadísticas de Partido** | `estadisticas_partido.csv` | Rendimiento numérico de cada equipo dentro de un partido ya jugado |
| 6 | **Lesiones** | `lesiones.csv` | Disponibilidad real de cada jugador en el tiempo |
| 7 | **Competiciones y Torneos** | `competiciones.csv`, `torneos.csv` | El marco organizativo bajo el que se juega un partido, en dos niveles: la competición (permanente) y su edición concreta (torneo) |
| 8 | **Infraestructura y Oficiales** | `estadios.csv`, `arbitros.csv` | El entorno físico y humano no perteneciente a ningún equipo |
| 9 | **Cuotas (Datos de Mercado)** | `cuotas.csv` | El precio de mercado de un resultado, de naturaleza distinta al rendimiento deportivo (`docs/16`, "Reglas generales") |
| 10 | **Predicciones** | `data/predictions/` | Lo que el modelo predijo, con qué versión, antes de que el partido ocurriera |
| 11 | **Resultados** | `data/results/` | Lo que realmente ocurrió, verificado externamente |
| 12 | **Auditoría** | `data/audit/` | Qué tan bien predijo el modelo, agregando Predicciones y Resultados |
| 13 | **Aprendizaje (Learning)** | Sin directorio propio en `data/` hoy — ver nota | Qué debería cambiar, con evidencia, a partir de la Auditoría acumulada |

**Nota sobre el dominio 13:** a diferencia de los otros doce, "Aprendizaje" no tiene hoy un directorio de datos propio (`data/learning/` no existe). `learning/` (fuera de `data/`) es el módulo que **procesa** los dominios 10-12 para producir diagnósticos y, como máximo, una propuesta documentada (`learning/weight-adjustment.md`) — nunca escribe en `data/` (`learning/README.md`, "Límites de responsabilidad"). Este documento no resuelve dónde debería persistirse esa propuesta si en el futuro se decide que necesita su propio registro histórico — se deja como pregunta abierta en "Observaciones", por no existir hoy evidencia de que haga falta un directorio nuevo (`CLAUDE.md`: "Ningún dato podrá incorporarse únicamente por si acaso").

**`raw/` y `archive/` no son dominios de información — son estados del ciclo de vida** (sección 6), no categorías de conocimiento. Cualquiera de los 13 dominios anteriores puede tener una porción de sus datos en estado "recién recolectado" (`raw/`) o "histórico inactivo" (`archive/`) sin que eso cambie a qué dominio pertenece.

---

# 4. Relaciones Conceptuales

Solo relaciones — sin SQL, sin ERD, sin claves.

```
Equipo
  │
  ├─ Convoca ──► Jugador (vía Convocatoria, para un Torneo concreto)
  │                  │
  │                  └─ Sufre ──► Lesión
  │
  └─ Participa en ──► Partido
                         │
                         ├─ Produce ──► Estadísticas de Partido
                         │
                         ├─ Se juega en ──► Estadio
                         │
                         ├─ Es dirigido por ──► Árbitro
                         │
                         ├─ Pertenece a ──► Torneo ──► Pertenece a ──► Competición
                         │
                         ├─ Tiene ──► Cuotas (si el mercado las ofrece)
                         │
                         └─ Origina ──► Predicción
                                            │
                                            ├─ Se compara con ──► Resultado (cuando el partido finaliza)
                                            │                         │
                                            │                         ▼
                                            └────────────────► Auditoría
                                                                    │
                                                                    ▼
                                                              Aprendizaje
                                                          (propuesta documentada,
                                                           nunca aplicación automática)
```

**Relaciones adicionales, no jerárquicas:**

- Un **Jugador** pertenece, en cada momento, a un único **Equipo** activo (`data/processed/selecciones-nacionales/README.md`, restricción de `jugadores.csv`).
- Una **Lesión** se origina, opcionalmente, en un **Partido** concreto (`id_partido_origen`), pero pertenece siempre a un **Jugador**, nunca directamente a un Equipo.
- Un **Torneo** pertenece siempre a exactamente una **Competición**; una Competición puede tener muchas ediciones (Torneos) a lo largo del tiempo.
- Las **Cuotas** se relacionan únicamente con el **Partido** — nunca con un Equipo o Jugador de forma independiente, porque el mercado apuesta sobre el resultado del enfrentamiento, no sobre una entidad aislada.

---

# 5. Responsabilidades

| Dominio | Responsabilidad | Nunca hace |
|---|---|---|
| Equipos | Identidad y fuerza declarada de una selección | Registrar historial de partidos (eso es Partidos) |
| Jugadores | Identidad y atributos de un futbolista | Registrar convocatoria a un torneo específico (eso es Convocatorias) |
| Convocatorias | Vincular Jugador ↔ Equipo ↔ Torneo | Registrar minutos jugados o estadísticas individuales (diferido, `MS-001`) |
| Partidos | El enfrentamiento en sí (quién, cuándo, resultado) | Calcular ninguna variable ni estadística derivada |
| Estadísticas de Partido | Rendimiento numérico ya jugado | Registrar el resultado del partido (eso es Partidos) |
| Lesiones | Disponibilidad real de un jugador en el tiempo | Calcular Disponibilidad de Plantilla (Variable006) — eso es `VariablePreparation`, no este dominio |
| Competiciones y Torneos | Marco organizativo permanente (Competición) y su edición concreta (Torneo) | Registrar partidos individuales (eso es Partidos) |
| Infraestructura y Oficiales | Entorno físico/humano no perteneciente a un equipo | Modificar el resultado de un partido |
| Cuotas | Precio de mercado del resultado | Ser tratada como una Variable Oficial (`docs/16`, "Reglas generales") |
| Predicciones | Registro inmutable de qué predijo el modelo, antes del partido | Modificarse una vez registrada, ni siquiera para corregir un error |
| Resultados | Verdad oficial externa de lo ocurrido | Ser calculada por el modelo — siempre proviene de una fuente externa verificada |
| Auditoría | Comparación cuantitativa Predicción vs. Resultado | Modificar predicciones o resultados históricos |
| Aprendizaje | Diagnóstico y propuesta documentada de mejora, con evidencia | Aplicar un cambio de peso, variable o algoritmo por sí mismo |

---

# 6. Ciclo de Vida de los Datos

```
Fuente externa (API, sitio oficial, entrada manual verificada)
        │
        ▼
data/raw/           — copia original, nunca modificada
        │
        ▼
Validación (integridad, formato, fecha, duplicados, nulos, consistencia)
        │
        ▼
Normalización (formato uniforme: fechas YYYY-MM-DD, porcentajes 0-100, identificador único por equipo)
        │
        ▼
data/processed/     — único origen autorizado para el Engine (los 13 dominios de la sección 3, dominios 1-9)
        │
        ▼
Engine (vía VariablePreparation, docs/15) ──► Predicción
        │
        ▼
data/predictions/   — registrado siempre antes del inicio del partido, inmutable
        │
        ▼
(el partido se juega)
        │
        ▼
data/results/       — resultado oficial, crudo, verificado externamente
        │
        ▼
partidos.csv actualizado (estado_partido = finalizado, goles_local/visitante completados)
estadisticas_partido.csv actualizado (si hay estadísticas finales disponibles)
        │
        ▼
data/audit/         — solo cuando existen Predicción y Resultado para el mismo partido
        │
        ▼
Aprendizaje (learning/) — diagnóstico y, como máximo, una propuesta documentada
        │
        ▼
(en cualquier punto posterior, para cualquier dominio)
data/archive/       — cuando el dato deja de participar en el procesamiento activo
                       (ej. cierre de una temporada, una versión de esquema superada),
                       nunca se elimina
```

**Aclaración sobre `data/archive/` (no explícita hasta ahora en ningún documento):** ningún dato está obligado a pasar por `archive/` — a diferencia de las demás transiciones de este ciclo (que son obligatorias para todo dato), `archive/` es un destino **opcional y diferido en el tiempo**, alcanzado únicamente cuando una decisión explícita (ej. cierre de un torneo, migración de esquema) determina que un dato ya no participa del procesamiento diario. Puede alcanzarse desde `data/raw/` (una captura superada por una más reciente) o desde `data/processed/` (una temporada ya cerrada) — nunca desde `data/predictions/`, `data/results/` o `data/audit/`, que permanecen activos indefinidamente por ser, en sí mismos, el historial permanente del modelo (`docs/05`: "nunca eliminar información de esta carpeta").

---

# 7. Separación entre Datos Históricos y Datos de Ejecución

Esta sección responde directamente la validación obligatoria más importante de esta misión: dónde termina la Base de Conocimiento y dónde empieza el Runtime.

| Estructura | Naturaleza | Duración | Dónde vive |
|---|---|---|---|
| **Base de Conocimiento** (`data/`, los 13 dominios de la sección 3) | Permanente, histórica | Indefinida — nunca se destruye | `data/raw/`, `data/processed/`, `data/predictions/`, `data/results/`, `data/audit/`, `data/archive/` |
| **Prediction Context** (`docs/30`) | Transitoria, de ejecución | Una sola predicción — se destruye tras la Persistencia (`docs/30` §3) | En memoria, nunca en `data/` |
| **Runtime** (`docs/26`/`docs/29`) | Maquinaria de coordinación, no almacena conocimiento por sí misma | Una sola ejecución | No persiste nada — delega toda persistencia en el componente `Persistence` (`docs/29` §2) |

La relación entre las tres es de **lectura y escritura acotada, nunca de mezcla**:

- El Runtime **lee** de la Base de Conocimiento (dominios 1-9, vía `VariablePreparation`) para construir el `PredictionContext`.
- El Runtime **nunca** almacena el `PredictionContext` completo en `data/` — solo su proyección curada (`PredictionReport`, `docs/30` §4.5) se escribe en el dominio **Predicciones** (`data/predictions/`).
- El dominio **Resultados** (`data/results/`) se **escribe desde fuera** del Runtime — es un dato externo verificado, no una salida de ejecución (`docs/06`, Fase 7).
- El dominio **Auditoría** se construye comparando dos dominios de la Base de Conocimiento ya existentes (Predicciones, Resultados) — nunca reabriendo el `PredictionContext` original, que para ese momento ya fue destruido (`docs/30` §3, nota central de diseño).

**Consecuencia directa:** la Base de Conocimiento puede evolucionar (cambiar de CSV a PostgreSQL, agregar un dominio nuevo, capturar un dato antes pendiente) sin que el Runtime necesite cambiar — el Runtime nunca conoce la forma física de ningún dominio, solo consume lo que `VariablePreparation` ya le entrega preparado (mismo principio de `docs/15` §9, aplicado aquí a nivel de todo el modelo de dominios, no solo a las Variables Oficiales).

---

# 8. Compatibilidad

| Documento | Verificación |
|---|---|
| `docs/16-Contrato-Oficial-de-Variables.md` | Ninguna Variable Oficial se redefine; los dominios 1-9 son, colectivamente, la fuente física de las 12 variables — la correspondencia exacta variable↔dominio ya está fijada en `docs/14` Etapa 2 y no se repite aquí |
| `docs/26`/`docs/29` (Runtime) | El Runtime sigue sin conocer la forma física de ningún dominio; este documento no introduce ningún acceso nuevo del Runtime a `data/` fuera de `VariablePreparation` y `Persistence`, ya definidos |
| `docs/30` (Prediction Context) | Confirmado en la sección 7: el `PredictionContext` nunca es parte de la Base de Conocimiento; solo su proyección (`PredictionReport`) ingresa al dominio Predicciones |
| `docs/14-Prediction-Pipeline.md` | El orden de lectura de los 11 archivos (Etapa 2) es exactamente el recorrido de los dominios 1-9 en el mismo orden de dependencia mostrado en la sección 4 de este documento |
| **Architecture Freeze** (`docs/23`, Parte 6) | Sin cambios — sigue en **4 de 7** criterios (`docs/00-Project-Tracker.md`). Este documento no resuelve `INC-05` (Criterio 5): el dominio Cuotas sigue siendo, hoy, consumido directamente por `engine/06` sin pasar por `VariablePreparation`, exactamente como ya lo hereda el bloque `market` de `docs/30` |

---

# Validaciones obligatorias

- **¿Todos los dominios actuales del proyecto quedan representados?** Sí — los 13 dominios de la sección 3 cubren exhaustivamente las 11 entidades físicas de `data/processed/selecciones-nacionales/` más `data/predictions/`, `data/results/`, `data/audit/` y el proceso de `learning/` (sin directorio propio, nota explícita en el dominio 13). `data/raw/` y `data/archive/` quedan representados como estados del ciclo de vida (sección 6), no como dominios adicionales — evita contarlos dos veces.
- **¿Existe duplicación conceptual entre dominios?** No. El caso que podría parecer duplicación — `data/results/` (Resultados) frente a `partidos.goles_local`/`goles_visitante` (dentro de Partidos) — es, en realidad, el mismo patrón raw/processed ya aplicado al resto del sistema: `data/results/` es el dato crudo y externo; los campos de `partidos.csv` son su versión validada y normalizada, actualizada solo después (`docs/14`, Etapa 4). Del mismo modo, `xGA` (Solidez Defensiva) no se almacena por separado — se deriva de `xg` del rival vía self-join (`docs/28`), evitando la duplicación que existiría si se guardara dos veces el mismo dato físico.
- **¿El Prediction Context permanece separado de la Base de Conocimiento?** Confirmado explícitamente en la sección 7 — nunca se persiste como objeto completo; solo su proyección curada entra al dominio Predicciones.
- **¿La Base de Conocimiento puede evolucionar sin afectar al Runtime?** Sí — mismo argumento ya fijado en `docs/05` ("Evolución") y `docs/15` §9, reafirmado aquí a nivel de los 13 dominios: cualquier cambio de tecnología física ocurre dentro de la Base de Conocimiento; el Runtime solo conoce el contrato ya preparado (Variables Oficiales, `docs/16`), nunca la forma física de un dominio.

---

# Cierre obligatorio

**1. ¿Qué problema arquitectónico resuelve este documento?**
La ausencia de un mapa conceptual intermedio entre el flujo genérico de `docs/05` y el esquema campo-por-campo de `data/processed/selecciones-nacionales/README.md`. Sin él, entender "qué dominios existen y cómo se relacionan" requería reconstruir esa imagen leyendo 11 tablas de campos por separado.

**2. ¿Qué dominios quedan oficialmente definidos?**
Trece: Equipos, Jugadores, Convocatorias, Partidos, Estadísticas de Partido, Lesiones, Competiciones y Torneos, Infraestructura y Oficiales, Cuotas, Predicciones, Resultados, Auditoría y Aprendizaje (este último sin directorio propio hoy, ver dominio 13).

**3. ¿Qué relaciones conceptuales aparecen?**
Las de la sección 4: Equipo participa en Partido y convoca Jugadores; Partido produce Estadísticas, se juega en un Estadio con un Árbitro, pertenece a un Torneo que pertenece a una Competición, y opcionalmente tiene Cuotas; Partido origina una Predicción que, al compararse con el Resultado, produce Auditoría, que alimenta Aprendizaje.

**4. ¿Qué responsabilidades quedan claramente separadas?**
Las trece de la sección 5 — en particular, que ningún dominio de conocimiento del mundo (1-9) calcula variables ni predicciones, y que ningún dominio de historial del modelo (10-13) se genera sin depender del anterior en la cadena (Auditoría nunca antes de Predicción+Resultado; Aprendizaje nunca antes de Auditoría).

**5. ¿Qué documentos deberán referenciar este modelo?**
`docs/99-Mapa-Maestro.md` (en su próxima actualización del mapa de directorios), cualquier futura misión `MS-`/`DATA-` que capture un dato nuevo (para ubicarlo en el dominio correcto antes de crear un CSV nuevo), y una eventual futura misión de diseño relacional (que partiría de este documento, no de cero).

**6. ¿Qué beneficios aporta para la futura implementación?**
Un implementador puede identificar, antes de diseñar cualquier tabla, a qué dominio pertenece un dato nuevo y qué relaciones conceptuales debe respetar — reduce el riesgo de crear una entidad que duplique la responsabilidad de otra ya existente (mismo riesgo que este documento verificó no estar hoy presente, sección de Validaciones).

**7. ¿Qué parte continúa pendiente?**
Tres cosas, ninguna nueva respecto a lo ya identificado por `docs/27`/`docs/28`: (a) los datos de categoría D todavía sin capturar (Grandes oportunidades, Rotaciones, Clima, entre otros); (b) el Contrato de Datos de Mercado completo para el dominio Cuotas (`INC-05`); (c) una decisión, todavía no tomada, sobre si el dominio Aprendizaje necesita en el futuro su propio espacio de persistencia dentro de `data/` (sección 3, dominio 13).

**8. ¿Qué misión recomendarías después?**
En el eje de datos: una misión de captura que resuelva los elementos de categoría D ya priorizados por `docs/27` (empezando por "Grandes oportunidades", el más barato). En el eje de arquitectura de ejecución: la primera fórmula matemática real en `models/poisson.md`, que sigue siendo, transversalmente, el bloqueante compartido de toda la serie `DEV-`/`MODEL-`.

**9. ¿El núcleo de datos puede considerarse estabilizado?**
A nivel de **dominios y relaciones conceptuales**, sí — los 13 dominios cubren la totalidad de lo que el proyecto reconoce hoy como información, sin huecos ni duplicaciones detectadas. A nivel de **contenido real**, no — 9 de las 11 entidades físicas siguen siendo solo encabezados sin datos poblados (`data/processed/selecciones-nacionales/README.md`, "Estado de los archivos"), y `data/predictions/`, `data/results/`, `data/audit/`, `data/raw/` y `data/archive/` siguen siendo marcadores de posición.

**10. ¿Qué falta para comenzar el diseño relacional?**
Una decisión de stack tecnológico (todavía no tomada por ninguna misión de la serie `DEV-`, por diseño) y, preferiblemente, que los dominios de categoría D más críticos (`docs/27`) ya tengan definida su fuente real — diseñar claves y relaciones físicas sobre un dominio cuyo dato de origen todavía no existe arriesga tener que rediseñarlas después. Ninguna de las dos condiciones es responsabilidad de esta misión.

---

# Observaciones

*(Hallazgos detectados durante el análisis, registrados sin corregirse — conforme al Manual Operativo, `docs/22`, sección 7.)*

1. **Inconsistencia editorial no catalogada hasta ahora en `docs/05-Base-de-Conocimiento.md`:** el encabezado interno del documento dice `# Arquitectura de Datos` y `**Archivo:** docs/04-Arquitectura-de-Datos.md` — un nombre y una ruta que corresponden a una posición anterior a alguna de las renumeraciones ya registradas en `docs/00-Project-Tracker.md` (MS-004/MS-005), nunca actualizada tras el desplazamiento a su posición actual (`docs/05`). Verificado con búsqueda directa: no aparece referenciada en ningún otro documento del proyecto. No se corrige aquí (fuera de alcance de esta misión) — se recomienda una futura misión editorial que la alinee, en el mismo lote que ya tiene pendiente `GR-003` (`data/README.md`).
2. **El dominio 13 (Aprendizaje) carece de una decisión explícita sobre persistencia propia.** `learning/README.md` es categórico en que el módulo nunca escribe en `data/`, pero no aclara qué ocurre con el historial de propuestas ya evaluadas por el Arquitecto Estadístico Humano (aprobadas o rechazadas) — hoy solo `learning/version-history.md` y `CHANGELOG.md` lo registran, ninguno de los dos dentro de `data/`. No se propone una solución (evitaría inventar un dato "por si acaso"); se deja como pregunta abierta para una futura misión de diseño de datos.

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Que agrupar "Competiciones y Torneos" en un único dominio (en lugar de dos separados) y "Infraestructura y Oficiales" (Estadios + Árbitros) es la granularidad correcta. Es una decisión razonada por responsabilidad compartida (ambos pares son marcos de contexto del partido, no protagonistas del enfrentamiento), pero una implementación futura podría preferir separarlos en cuatro dominios en lugar de dos.
- **¿Qué parte de este entregable podría estar equivocada?** La afirmación de que `data/archive/` nunca recibe datos de `data/predictions/`/`results/`/`audit/` se basa en que esos tres directorios se describen como historial permanente en `docs/05`/`data/README.md`, pero ningún documento dice explícitamente que estén *excluidos* de archivarse algún día (ej. predicciones de hace una década). Se interpretó la ausencia de mención como "permanecen activos indefinidamente", no como "nunca podrán archivarse" — una futura misión podría matizarlo.
- **¿Qué información me habría hecho falta para tener más certeza?** Un ejemplo real de un dato que ya haya transitado a `data/archive/` (hoy el directorio solo tiene un `README.md`) habría permitido confirmar si la aclaración de la sección 6 sobre cuándo se activa ese destino es precisa o si faltan casos no anticipados.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que, cuando exista contenido real en `data/predictions/`/`results/`/`audit/`, el patrón raw/processed aplicado a Resultados (sección de Validaciones) efectivamente evite la duplicación anticipada y no aparezcan campos que terminen guardándose dos veces.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí, ya señalada en las Observaciones: el dominio Aprendizaje podría, en una lectura alternativa, no ser un dominio "de datos" en absoluto (por no tener hoy persistencia propia) sino solo un proceso — se decidió mantenerlo como dominio número 13, con la nota explícita, porque el brief lo pide por nombre y porque documentar la ausencia de persistencia es más útil que omitir el dominio por completo.

---

# Fuera de alcance de esta misión

- No se diseñan tablas, SQL, PostgreSQL, índices, claves primarias ni foráneas.
- No se implementa código ni JPA.
- No se modifican las Variables Oficiales, fórmulas, motores ni el Runtime ya definido.
- No se corrige la inconsistencia editorial de `docs/05` detectada en "Observaciones".
- No se decide dónde persistir el historial de propuestas de `learning/` — queda como pregunta abierta.

---

Fin del documento.
