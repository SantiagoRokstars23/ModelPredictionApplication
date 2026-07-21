# Arquitectura Oficial del Proyecto Python del Modelo Santiago

**Archivo:** `docs/35-Arquitectura-Oficial-del-Proyecto-Python.md`

**Misión:** DEV-004 — Arquitectura Oficial del Proyecto Python del Modelo Santiago

**Versión:** 1.0.0

**Estado:** Especificación oficial — arquitectura de proyecto (sin implementación, sin carpetas creadas)

---

# Objetivo

`ARCH-000` congeló **con qué** se construye el Modelo Santiago (Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Docker). `DEV-001` a `DEV-003` y `DATA-003` a `DATA-005` definieron **qué** existe (el Runtime, sus siete componentes, el `PredictionContext`, el modelo de datos físico). Ninguno de los siete documentos anteriores responde una pregunta distinta: **¿en qué paquetes concretos del proyecto Python vivirá cada una de esas piezas, y quién puede depender de quién?**

Ese es el vacío que cierra esta misión — la última pieza puramente arquitectónica antes de que exista la primera línea de código real.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué aporta este documento |
|---|---|---|
| `docs/34-Decision-Oficial-del-Stack-Tecnologico.md` | Qué tecnologías se usan | En qué paquete concreto se usa cada una |
| `docs/26`/`docs/29` | El Runtime y sus siete componentes (`PredictionRequest` → ... → `Persistence`) | El paquete Python exacto donde vive cada componente |
| `docs/30` | La estructura interna del `PredictionContext` | Confirma que sigue siendo el único objeto compartido entre paquetes (sección 6) |
| `docs/31`/`docs/32`/`docs/33` | Los 13 dominios, las 15 entidades, las 14 tablas físicas | El paquete que las materializa como modelos SQLAlchemy (`app/models/`) |

Ninguna decisión de estos siete documentos se modifica — este documento únicamente les da una dirección de archivo.

---

# 1. Objetivo del proyecto Python

## Qué implementará exactamente

El código ejecutable que materializa, sin redefinirla, la arquitectura ya diseñada: el Runtime y sus siete componentes (`docs/29`), los seis motores del Engine una vez tengan Versión 2.0 en `models/`, la Capa de Preparación de Variables (`docs/15`), el modelo físico de datos (`docs/33`) y una API que exponga todo esto a un cliente.

## Qué responsabilidades tendrá

- **Ejecutar**: correr el Runtime y el Engine sobre datos reales.
- **Persistir**: escribir y leer contra PostgreSQL.
- **Exponer**: dar acceso a una API HTTP (FastAPI) para solicitar predicciones.

## Qué responsabilidades seguirán perteneciendo a la documentación

Todo lo que ya vive en `docs/`, `engine/` (las especificaciones `.md`, no el código) y `models/` sigue siendo la única fuente de verdad conceptual — el código nunca decide una fórmula, una variable o una regla de negocio nueva; solo ejecuta lo que esos documentos ya aprobaron. Esta es la misma separación que `CLAUDE.md` ya fija para "engine/" (especificación) frente a lo que un futuro "engine ejecutable" haría — este documento la extiende, por primera vez, a un proyecto de código real.

---

## Aclaración de nomenclatura (para evitar una confusión real)

Esta arquitectura introduce dos paquetes cuyo nombre coincide, a propósito, con dos directorios ya existentes en la raíz del repositorio — deben distinguirse sin ambigüedad:

| Nombre compartido | Directorio raíz (ya existente, documentación) | Paquete nuevo (código) |
|---|---|---|
| `engine` | `engine/01-Offensive-Strength.md` a `engine/06-Expected-Value.md` — especificación de cada motor | `app/engine/` — implementación en Python de esas mismas especificaciones |
| `models` | `models/offensive-strength.md` a `models/parameter-calibration.md` — investigación matemática | `app/models/` — **no tiene relación con la investigación matemática**; son las clases SQLAlchemy que representan las 14 tablas físicas de `docs/33` |

Ningún directorio raíz se renombra, se mueve ni se duplica — coexisten, con responsabilidades explícitamente distintas.

---

# 2. Arquitectura General

```
Cliente
   │
   ▼
FastAPI (app/api)                    ── recibe la solicitud HTTP, la valida contra app/schemas
   │
   ▼
Runtime (app/runtime)                ── construye PredictionContext, coordina todo lo siguiente
   │
   ▼
Preparación (app/preparation)        ── transforma datos de app/persistence en Variables Oficiales
   │
   ▼
Engine (app/engine)                  ── ejecuta los 6 motores, por capas (docs/29 §4)
   │
   ▼
Assembler (dentro de app/runtime)    ── transforma el PredictionContext completo en PredictionReport
   │
   ▼
Persistencia (app/persistence)       ── escribe el PredictionReport en la Base de Datos
   │
   ▼
Base de Datos (PostgreSQL, app/models describe su forma)
   │
   ▼
Respuesta (de vuelta por FastAPI, serializada con app/schemas)
```

---

# 3. Estructura Oficial del Proyecto

*(Diseño conceptual — ningún directorio se crea en esta misión.)*

```
(raíz del repositorio — ya existente, sin cambios)
├── docs/            (gobierna — sin cambios)
├── engine/          (especificación de cada motor — sin cambios, ver "Aclaración de nomenclatura")
├── models/          (investigación matemática — sin cambios, ver "Aclaración de nomenclatura")
├── data/            (Base de Conocimiento origen — raw/processed/predictions/results/audit/archive)
├── prompts/, .claude/agents/, CLAUDE.md, README.md, CHANGELOG.md, LICENSE (sin cambios)
│
├── app/                     ← código de la implementación (nuevo, conceptual)
│   ├── api/                 (FastAPI: routers y endpoints)
│   ├── runtime/             (Runtime + sus 7 componentes, docs/29)
│   ├── engine/              (los 6 motores, en código — implementa engine/*.md)
│   ├── preparation/         (Capa de Preparación de Variables, docs/15)
│   ├── persistence/         (acceso a datos: repositorios, sesión de SQLAlchemy)
│   ├── models/              (ORM SQLAlchemy — las 14 tablas de docs/33)
│   ├── schemas/             (Pydantic — contratos de entrada/salida de la API)
│   ├── services/            (Statistician/Auditor/Bankroll Manager — fases fuera del núcleo del Runtime)
│   └── config/              (configuración: conexión a BD, versión del modelo, settings)
│
├── tests/                   ← pytest (conceptual)
├── migrations/              ← Alembic (conceptual)
└── scripts/                 (ya previsto en CLAUDE.md — importación/seed de CSV a PostgreSQL viviría aquí)
```

## Justificación de cada módulo nuevo

| Módulo | Por qué existe |
|---|---|
| `app/api/` | Es el único punto de contacto con el mundo exterior — FastAPI ya fue elegido (`docs/34`) precisamente por su integración nativa con Pydantic (`app/schemas`) y su documentación automática |
| `app/runtime/` | Materializa, sin redefinirlos, los siete componentes ya diseñados en `docs/29` — es el único paquete que conoce el orden de ejecución completo |
| `app/engine/` | Aísla la lógica matemática pura (los 6 motores) de cualquier detalle de infraestructura — es, por diseño, el paquete más protegido de toda la arquitectura (sección 6) |
| `app/preparation/` | Materializa la Capa de Preparación de Variables (`docs/15`) — el único paquete, junto con `app/persistence`, autorizado a conocer el origen físico de un dato |
| `app/persistence/` | Aísla el acceso a datos (SQLAlchemy, sesiones, consultas) del resto del sistema — ningún otro paquete conoce SQL |
| `app/models/` | Representa, uno a uno, las 14 tablas físicas ya diseñadas en `docs/33` — nunca contiene lógica de negocio, solo estructura de datos |
| `app/schemas/` | Separa deliberadamente el contrato **externo** (lo que la API expone) del contrato **interno de almacenamiento** (`app/models`) — el mismo principio de desacoplamiento que `docs/15` ya aplicó entre Base de Conocimiento y Variables Oficiales, ahora aplicado entre base de datos y API |
| `app/services/` | Aloja las responsabilidades de los agentes que existen fuera del núcleo lineal del Runtime — validación previa (Statistician), auditoría posterior (Auditor), gestión de bankroll opcional (Bankroll Manager) — ver tabla de la sección 6 |
| `app/config/` | Centraliza configuración (cadena de conexión, versión del modelo) — nunca contiene lógica de negocio ni de cálculo |
| `tests/` | pytest, ya oficializado en `docs/34` §9 — refleja la estructura de `app/` |
| `migrations/` | Alembic, ya oficializado en `docs/34` §6 — cada tabla de `docs/33` es una migración candidata, en el orden de dependencia ya fijado (`docs/32` §6) |
| `scripts/` | Ya previsto por `CLAUDE.md` desde el diseño original del repositorio, nunca creado hasta ahora — aquí viviría, en el futuro, el script de importación que carga los CSV de `data/processed/` a PostgreSQL |

---

# 4. Responsabilidades

| Paquete | Responsabilidad | Puede depender de | Nunca hace |
|---|---|---|---|
| `app/api` | Recibir la solicitud HTTP, validarla contra `app/schemas`, invocar `app/runtime`, devolver la respuesta | `app/schemas`, `app/runtime`, `app/config` | Calcular una probabilidad; conocer SQLAlchemy o PostgreSQL directamente |
| `app/runtime` | Construir el `PredictionContext`, coordinar `app/preparation` → `app/engine` → Assembler → `app/persistence`, en ese orden | `app/preparation`, `app/engine`, `app/persistence`, `app/config` | Ejecutar SQL; conocer FastAPI |
| `app/engine` | Ejecutar la lógica matemática de los 6 motores (una vez tengan Versión 2.0 en `models/`) | Únicamente el `PredictionContext` (o su representación en memoria) — ninguna otra dependencia interna de `app/` | Conocer FastAPI, SQLAlchemy, PostgreSQL, ni ningún otro paquete de `app/` |
| `app/preparation` | Transformar datos ya recuperados por `app/persistence` en las 12 Variables Oficiales (`docs/16`) | `app/persistence` (para leer), `app/models` (para conocer la forma de los datos que lee) | Calcular probabilidades, fuerzas, caos o valor esperado |
| `app/persistence` | Ejecutar consultas y escrituras contra PostgreSQL, usando `app/models` | `app/models`, `app/config` | Ejecutar lógica matemática o de negocio |
| `app/models` | Declarar la forma de las 14 tablas físicas (`docs/33`) como clases SQLAlchemy | Nada dentro de `app/` (es una hoja) | Contener lógica de negocio o de cálculo |
| `app/schemas` | Declarar los contratos Pydantic de entrada/salida de la API | Nada dentro de `app/` (es una hoja, independiente de `app/models`) | Conocer SQLAlchemy |
| `app/services` | Validación previa, auditoría posterior, gestión de bankroll opcional (sección 6) | `app/persistence`, `app/runtime` (para invocarlo, en el caso del Auditor) | Formar parte del camino crítico del Runtime — se ejecutan antes o después, nunca dentro |
| `app/config` | Configuración transversal (conexión, versión) | Nada | Contener lógica de negocio |

---

# 5. Dependencias

Matriz conceptual de dependencia, estrictamente unidireccional — **nunca al revés**:

```
app/api
   │
   ▼
app/runtime
   │
   ▼
app/preparation
   │
   ▼
app/engine
   │
   ▼
(Assembler, dentro de app/runtime)
   │
   ▼
app/persistence
   │
   ▼
app/models  →  Base de Datos (PostgreSQL)
```

`app/schemas` y `app/config` son dependencias transversales ("hojas"): cualquier paquete puede depender de ellos, pero ellos no dependen de ningún otro paquete de `app/`. `app/services` depende de `app/persistence` y, cuando corresponde, invoca a `app/runtime` desde **fuera** de su camino crítico (nunca al revés — el Runtime nunca depende de `app/services`).

---

# 6. Reglas arquitectónicas

| Regla | Por qué |
|---|---|
| **`app/engine` nunca conoce FastAPI** | El Engine es lógica matemática pura — acoplarlo a un framework web lo haría imposible de probar de forma aislada (`tests/`) y violaría el desacoplamiento ya exigido por `docs/15` |
| **`app/engine` nunca conoce PostgreSQL ni SQLAlchemy** | Mismo principio que ya rige el Engine documental: "los motores nunca deben conocer si los datos provienen de CSV" (`docs/15` §8) — en código, se traduce en que ni siquiera importan el paquete de acceso a datos |
| **`app/runtime` nunca conoce SQL** | Delega toda persistencia en `app/persistence` — el Runtime coordina, nunca ejecuta una consulta directamente (mismo principio que `docs/26` §9: "el Runtime coordina; nunca calcula") |
| **`app/api` nunca calcula probabilidades** | Delega el cálculo completo a `app/runtime` — la API es, exclusivamente, una capa de transporte |
| **`app/persistence` nunca ejecuta lógica matemática** | Es una capa de acceso a datos pura — cualquier cálculo que apareciera allí sería una duplicación de responsabilidad ya prohibida por `docs/15`/`docs/17` |
| **`PredictionContext` sigue siendo el único objeto compartido** | `docs/30` no se modifica — `app/preparation`, `app/engine` y el resto de `app/runtime` siguen comunicándose exclusivamente a través de sus secciones ya definidas (`metadata`, `match`, `variables`, `engine`, `prediction`, etc.), nunca mediante variables globales ni acoplamiento directo entre paquetes |
| **`app/schemas` nunca conoce `app/models`** | Mantiene el contrato externo (API) desacoplado del contrato interno de almacenamiento — un cambio de esquema de base de datos no debería, por sí solo, romper el contrato ya publicado de la API |

## Mapeo de los agentes documentales (`.claude/agents/`) al código

*(Aporte de esta misión, no pedido explícitamente por el brief, pero necesario para que `app/services` tenga una responsabilidad exacta y verificable.)*

| Agente (`.claude/agents/`) | Dónde vive en el código |
|---|---|
| Orchestrator | `app/api` (recibe la solicitud) + el coordinador de más alto nivel dentro de `app/runtime` |
| Statistician | `app/services` (validación de suficiencia, Fase 2 de `docs/06`) — se ejecuta **antes** de que `app/runtime` invoque `app/preparation` |
| Predictor | `app/runtime` en sí mismo — es la encarnación en código de este agente |
| Odds Analyzer | Parte de la Capa 4 condicional dentro de `app/engine`/`app/runtime` (`docs/29` §4) — no es un paquete separado |
| Bankroll Manager | `app/services` — opcional, fuera del núcleo, igual que en `docs/06` |
| Auditor | `app/services` — Fase 8, se ejecuta después, sobre datos ya persistidos |

---

# 7. Flujo de ejecución

1. El cliente envía una solicitud HTTP a `app/api`.
2. `app/api` valida la solicitud contra el esquema `PredictionRequest` de `app/schemas` — si es inválida, responde de inmediato sin invocar nada más.
3. `app/api` invoca a `app/runtime`, entregándole el `PredictionRequest` ya validado.
4. `app/runtime` construye el `PredictionContext` (bloques `metadata` y `match`, `docs/30` §4.1-4.2).
5. `app/runtime` invoca `app/services` (Statistician) para confirmar suficiencia de datos — si falla, el flujo se detiene aquí, antes de tocar `app/preparation`.
6. `app/runtime` invoca `app/preparation`, que lee de `app/persistence` y agrega el bloque `variables` al `PredictionContext`.
7. `app/runtime` invoca `app/engine` por capas (Capa 1: Offensive/Defensive Strength en paralelo; Capa 2: Poisson; Capa 3: Chaos/Confidence en paralelo; Capa 4: Expected Value, condicional) — cada motor agrega su propia subsección del bloque `engine`.
8. El Assembler (dentro de `app/runtime`) lee el `PredictionContext` completo y construye el `PredictionReport`.
9. `app/runtime` invoca `app/persistence` para escribir el `PredictionReport` en PostgreSQL (tabla `predicciones`, `docs/33` §4.12).
10. `app/runtime` devuelve el `PredictionReport` a `app/api`.
11. `app/api` lo serializa con el esquema `PredictionReport` de `app/schemas` y responde al cliente.
12. *(Más adelante, fuera de este ciclo)* `app/services` (Auditor) compara la predicción persistida contra el resultado oficial, una vez disponible, y escribe en la tabla `auditorias`.

---

# 8. Estrategia de crecimiento

| Qué se agrega | Dónde se agrega | Qué NO cambia |
|---|---|---|
| Un motor nuevo (ej. `engine/07-Bankroll-Engine.md`, ya previsto como futuro) | Un módulo nuevo dentro de `app/engine/`, registrado en la secuencia de capas de `app/runtime` | Ningún otro paquete — `app/api`, `app/persistence`, `app/schemas` no se enteran de que existe un motor nuevo |
| Una Variable Oficial nueva (Variable013 en adelante, `docs/16` §9) | `app/preparation`, después de que `docs/03`/`docs/16` la documenten primero (`CLAUDE.md`: "Investigación antes de implementación") | `app/engine` no cambia salvo el motor específico que la consuma |
| Un endpoint nuevo (ej. consultar el estado de una predicción ya registrada) | Un router nuevo dentro de `app/api`, con su propio esquema en `app/schemas` | `app/runtime`, `app/engine`, `app/persistence` — un endpoint de solo lectura no toca el camino de escritura |
| Un modelo matemático nuevo o una recalibración (`models/`, `MODEL-` futuro) | Primero `models/` (investigación), después el módulo correspondiente de `app/engine` | La arquitectura de paquetes en sí — solo cambia el contenido interno de un módulo ya existente |

Ninguno de los cuatro casos exige reorganizar un paquete existente — es, precisamente, la propiedad que valida esta arquitectura (ver "Validaciones obligatorias").

---

# 9. Compatibilidad

| Documento | Verificación |
|---|---|
| `docs/26`/`docs/29` (Runtime) | Los siete componentes tienen, cada uno, un lugar exacto dentro de `app/runtime` (Assembler) o en paquetes dedicados (`app/preparation`, `app/persistence`) — ninguno queda sin dirección |
| `docs/30` (`PredictionContext`) | Sigue siendo el único objeto compartido (sección 6) — ningún paquete nuevo introduce un canal de comunicación alternativo |
| `docs/31`/`docs/32`/`docs/33` (Base de Conocimiento) | Las 14 tablas físicas se materializan exactamente en `app/models`, sin alterar ninguna columna, tipo o relación ya diseñada |
| `docs/34` (Stack Oficial) | FastAPI → `app/api`; SQLAlchemy/Alembic → `app/models`/`app/persistence`/`migrations/`; Pydantic → `app/schemas`; NumPy/Pandas/SciPy → `app/engine`; pytest → `tests/` — cada tecnología ya congelada tiene un paquete de destino inequívoco |

---

# Restricciones (confirmación de cumplimiento)

Este documento no escribe código, no crea carpetas reales, y no modifica el Engine, las Variables Oficiales, las fórmulas matemáticas, el Runtime ni el `PredictionContext` ya definidos — únicamente les asigna una ubicación conceptual dentro de un proyecto Python todavía no iniciado.

---

# Validaciones obligatorias

- **¿Todos los componentes actuales tienen un lugar dentro del proyecto?** Sí — los siete componentes de `docs/29`, los seis motores del Engine, las 14 tablas de `docs/33` y las cinco tecnologías principales de `docs/34` quedan, cada uno, asignados a un paquete exacto (secciones 3-4, 9).
- **¿No existen dependencias circulares?** Confirmado — la matriz de la sección 5 es estrictamente unidireccional (`api → runtime → preparation → engine → persistence → models`), con `schemas`/`config` como hojas sin dependencias internas y `services` operando fuera del camino crítico, nunca dentro de él.
- **¿El Engine permanece completamente desacoplado?** Sí — `app/engine` no depende, ni puede depender, de `app/api`, `app/persistence`, `app/models` ni `app/schemas` (sección 6); su única entrada es el `PredictionContext`.
- **¿La arquitectura soporta crecimiento futuro sin reorganizar el proyecto?** Sí — los cuatro casos de crecimiento de la sección 8 se resuelven agregando contenido a un paquete ya existente, nunca creando una nueva capa o reordenando la matriz de dependencias.

---

# Cierre obligatorio

**1. ¿Qué problema arquitectónico resuelve este documento?**
La ausencia de una asignación concreta, paquete por paquete, de cada pieza ya diseñada por `ARCH-000`/`DEV-001-003`/`DATA-003-005` — sin ella, la primera línea de código real habría tenido que inventar su propia organización, con riesgo de acoplar el Engine a FastAPI o a SQLAlchemy desde el primer commit.

**2. ¿Cómo quedará organizado el proyecto Python?**
En un paquete `app/` con nueve subpaquetes de responsabilidad única (`api`, `runtime`, `engine`, `preparation`, `persistence`, `models`, `schemas`, `services`, `config`), más `tests/`, `migrations/` y `scripts/` a su mismo nivel — todos coexistiendo con la estructura documental ya existente (`docs/`, `engine/`, `models/`, `data/`), sin reemplazarla (sección 3).

**3. ¿Qué componente será el punto de entrada de toda la aplicación?**
`app/api` — el único paquete que recibe una solicitud del mundo exterior.

**4. ¿Qué componente coordinará la ejecución?**
`app/runtime` — construye el `PredictionContext`, invoca `app/preparation`, `app/engine` y, mediante el Assembler, `app/persistence`, en ese orden fijo.

**5. ¿Qué componente contendrá exclusivamente la lógica matemática?**
`app/engine` — el único paquete de todo el proyecto sin ninguna dependencia interna de infraestructura (sección 6).

**6. ¿Qué ventajas ofrece esta organización?**
Permite probar el Engine de forma completamente aislada (sin base de datos ni servidor HTTP); permite cambiar de framework web o de motor de base de datos sin tocar la lógica matemática; y hace explícita, en la propia estructura de carpetas, la misma separación de responsabilidades que `CLAUDE.md` ya exige a nivel documental.

**7. ¿Qué documentos pasan a ser la referencia oficial para iniciar la implementación?**
Los siete ya analizados (`docs/26`, `29`, `30`, `31`, `32`, `33`, `34`) más este mismo documento (`docs/35`), que es quien les da, por primera vez, una dirección de archivo concreta.

**8. ¿Qué misión recomendarías inmediatamente después?**
La misma prioridad ya heredada de `MODEL-007`/`MODEL-008`: una misión de captura de datos reales (`docs/27`), condición para que `app/engine` tenga algo calibrado que ejecutar. En el eje de arquitectura, esta misión cierra la cadena — no queda ninguna pieza puramente conceptual pendiente de diseño.

**9. ¿El proyecto queda listo para comenzar la construcción de la V1?**
En el eje arquitectónico, sí — por primera vez, existe una respuesta completa a "qué construir, con qué, y dónde vive cada pieza". En el eje matemático, no todavía: sigue pendiente, como en cada cierre anterior, al menos una fórmula con Versión 2.0 calibrada en `models/`, sin la cual `app/engine` existiría como estructura vacía sin ningún cálculo real que ejecutar.

**10. ¿Qué porcentaje estimas que representa este hito dentro del desarrollo total del Modelo Santiago?**
Cualitativamente: cierra el **100% del diseño arquitectónico de ejecución** (Runtime, datos, stack, organización de código) — la fase de diseño que comenzó en `docs/06` y se extendió por `DEV-`/`DATA-`/`ARCH-`. No representa ningún porcentaje del **desarrollo de código** (0%, nada implementado todavía) ni del **contenido matemático calibrado** (0%, sin cambios respecto a `MODEL-008`). Es, en términos del propio `docs/99-Mapa-Maestro.md`, el cierre definitivo de la etapa "Arquitectura" y la habilitación formal de la etapa "Implementación V0.1" — sin que esta misión, por sí sola, haya avanzado esa segunda etapa ni un solo paso.

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Que el proyecto Python coexiste, como nuevos directorios de nivel raíz (`app/`, `tests/`, `migrations/`), dentro de este mismo repositorio, en lugar de vivir en un repositorio separado. El brief no lo especifica explícitamente; se eligió esta lectura por ser la más consistente con la estructura ya declarada en `CLAUDE.md`/`README.md` (que ya prevé `scripts/` y `excel/` como hermanos de `docs/`/`engine/`/`models/`/`data/`), pero una decisión futura podría preferir separar el código en un repositorio propio.
- **¿Qué parte de este entregable podría estar equivocada?** La asignación de "Odds Analyzer" como parte de la Capa 4 de `app/engine`/`app/runtime` en lugar de un servicio propio en `app/services` es una decisión de diseño razonable pero no la única — podría, alternativamente, tratarse como un servicio que decide *si* invocar `engine/06`, dejando que `app/engine` solo contenga el cálculo puro.
- **¿Qué información me habría hecho falta para tener más certeza?** Sin ningún endpoint real definido todavía (qué operaciones expondrá exactamente `app/api` más allá de "solicitar una predicción"), la estructura interna de `app/api` (routers concretos) sigue siendo una extrapolación razonable, no una certeza verificada contra un documento previo.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que, al escribir el primer módulo real de `app/engine`, efectivamente no necesite importar nada de `app/persistence`/`app/models`/`app/api` — es la validación más importante de toda esta arquitectura y hoy es solo una regla declarada, no verificada con código real.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí, ya señaladas arriba (repositorio separado, Odds Analyzer como servicio) — ambas se documentan como decisiones tomadas, no como hechos incuestionables.

---

# Fuera de alcance de esta misión

- No se escribe código.
- No se crean carpetas reales.
- No se modifica el Engine, las Variables Oficiales, las fórmulas matemáticas, el Runtime ni el `PredictionContext` ya definidos.
- No se inicia la implementación de la V1.
- No se decide si el proyecto Python vive en este mismo repositorio o en uno separado — se asume la primera opción, declarada explícitamente en la Autocrítica, no verificada con una misión `GOV-` dedicada.

---

Fin del documento.
