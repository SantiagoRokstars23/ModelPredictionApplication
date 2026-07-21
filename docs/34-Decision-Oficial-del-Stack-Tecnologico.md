# Decisión Oficial del Stack Tecnológico del Modelo Santiago

**Archivo:** `docs/34-Decision-Oficial-del-Stack-Tecnologico.md`

**Misión:** ARCH-000 — Decisión Oficial del Stack Tecnológico del Modelo Santiago (primera misión de una nueva serie, `ARCH-`, dedicada a decisiones de arquitectura tecnológica congeladas)

**Versión:** 1.0.0

**Estado:** Especificación oficial — decisión de stack congelada (sin implementación)

---

# Objetivo

Toda la arquitectura del Modelo Santiago (`docs/06`, `docs/25`, `docs/26`, `docs/29`, `docs/30`, `docs/31`, `docs/32`, `docs/33`) fue diseñada, deliberadamente, sin comprometerse con ningún lenguaje ni tecnología — `docs/26`/`docs/29`/`docs/30` lo afirman explícitamente ("no elige lenguaje ni tecnología... fuera de alcance de toda la serie `DEV-`"). Esa neutralidad ya cumplió su propósito: permitió diseñar el Runtime, el `PredictionContext` y el modelo de datos sin atarlos prematuramente a una decisión no evaluada.

Esta misión hace exactamente lo contrario, y de forma deliberada: **congela** una decisión de stack única y oficial, obligatoria para toda implementación futura. No es una ampliación de `docs/26`/`docs/29`/`docs/30` — es el punto de transición que ellos mismos dejaron pendiente.

---

# 0. Relación con los documentos ya existentes (sin duplicar)

| Documento | Qué ya define | Qué aporta esta misión |
|---|---|---|
| `CLAUDE.md` | Gobierna el proyecto; no menciona ninguna tecnología concreta | Ninguna contradicción — `CLAUDE.md` sigue gobernando por encima de esta decisión (Constitución, Art. 3) |
| `docs/21-Constitucion-del-Modelo-Santiago.md` | Art. 10 ("condiciones mínimas para iniciar implementación"); Art. 12 ("puede cambiar de tecnología... siempre que permanezca compatible") | Esta misión es el acto explícito de evolución tecnológica que el Art. 12 exige que sea deliberado, no implícito |
| `docs/26`/`docs/29`/`docs/30` | Runtime, componentes y `PredictionContext`, todos explícitamente independientes de lenguaje | Se confirma, en la sección de Validaciones, que el stack aquí elegido puede implementarlos sin modificar ninguno de los tres |
| `docs/33-Modelo-Fisico-PostgreSQL.md` | Modelo físico PostgreSQL, redactado asumiendo de facto Java/Spring Boot/Hibernate/JPA/Flyway/Liquibase (ya señalado allí mismo como hallazgo sin resolver) | Esta misión **resuelve esa ambigüedad a favor de Python** — y, al hacerlo, deja la sección 9 de `docs/33` desactualizada; ver "Observaciones", hallazgo 1 |
| `docs/12-Roadmap.md` | Proyecta la evolución v1 Excel → **v2 Python** → v3 Machine Learning → v4 Dashboard → v5 Automatización completa | Es la única evidencia documental real, preexistente a esta misión, de una intención tecnológica — la decisión de esta misión es consistente con ella, no la contradice |

---

# 1. Objetivo del stack

## Por qué existe

Para que exista, por primera vez, una decisión tecnológica única y verificable que toda implementación futura deba usar sin volver a discutirla — cerrando la neutralidad deliberada de `docs/26`/`docs/29`/`docs/30`, y resolviendo formalmente la ambigüedad que `docs/33` había dejado abierta (asumió Java/Spring Boot sin mandato, y lo señaló explícitamente como hallazgo pendiente).

## Qué problemas pretende resolver

- Evita que cada futura misión de implementación tenga que inventar o negociar su propio stack.
- Da continuidad a la única evidencia real ya documentada del proyecto (`docs/12-Roadmap.md`: v2 = Python), en lugar de partir de cero o de una suposición no verificada.
- Fija un punto de no retorno técnico razonado — no arbitrario ni impuesto sin justificación (Constitución, Art. 2.1, "Objetividad").

## Qué principios respeta

| Principio | Cómo se respeta |
|---|---|
| Objetividad / Evidencia antes que opinión (Constitución Art. 2.1/2.5) | Cada tecnología se justifica contra el dominio real del proyecto (cálculo estadístico, contrato de datos explícito), no por preferencia |
| Separación de responsabilidades (Art. 2.6) | Esta misión decide **con qué** se construye; no toca **qué** se construye (Runtime, Engine, Variables, `models/`) |
| Desarrollo incremental (Art. 2.7) | Se elige el stack mínimo suficiente para V1, dejando explícita su capacidad de crecer hacia V2/V3 (sección de Validaciones) sin migrar de tecnología |
| Evolución (Art. 12) | El cambio de "sin tecnología" a "stack congelado" es, precisamente, el tipo de decisión deliberada que este artículo exige — nunca implícita |

---

# 2. Lenguaje principal: Python

**Decisión:** Python como lenguaje oficial de implementación del Modelo Santiago V1.

## Justificación

1. **Es la única evidencia documental real ya existente en el proyecto.** `docs/12-Roadmap.md` proyecta explícitamente "v2: Python" desde antes de esta misión — se elige continuidad con lo ya documentado, no una decisión sin precedente.
2. **El dominio del proyecto es, por naturaleza, estadístico/científico.** `models/` ya investiga fórmulas de Poisson, entropía de Shannon, distribuciones de probabilidad — el ecosistema científico de Python (sección 7) es el estándar de facto para exactamente ese tipo de cálculo, con librerías maduras y validadas por la comunidad, en lugar de reimplementar manualmente lo que ya existe y está probado.
3. **Encaja con el patrón de contrato explícito ya establecido por el proyecto** (`docs/16`, `docs/30`): el tipado gradual de Python moderno, combinado con Pydantic (sección 8) y MyPy (sección 10), permite expresar esos contratos como código verificable, no solo como documentación.

## Comparación breve (sin convertirla en un benchmark)

| Lenguaje | Fortaleza reconocida | Por qué no se elige para el Modelo Santiago |
|---|---|---|
| **Java** | Tipado estricto, ecosistema empresarial maduro (y, de hecho, lo que `docs/33` había asumido sin mandato) | Ecosistema científico/estadístico comparativamente más débil y verboso que Python para el tipo de investigación que `models/` ya desarrolla; further, su adopción aquí nunca fue una decisión formal — esta misión la reemplaza explícitamente (ver Observaciones) |
| **C#** | Ecosistema (.NET) maduro y con buen tipado | Menor adopción en el dominio estadístico/deportivo que el stack científico de Python; acoplamiento cultural más fuerte a un ecosistema (.NET/Windows) que no aporta ventaja aquí |
| **Node.js (JavaScript/TypeScript)** | Excelente para I/O concurrente y APIs web ligeras | Ecosistema numérico/científico inmaduro frente a NumPy/SciPy — obligaría a reimplementar o enlazar con librerías externas para el núcleo matemático del Engine |
| **Go** | Rendimiento y concurrencia sobresalientes | Ecosistema científico/estadístico prácticamente inexistente comparado con Python — candidato razonable para un futuro servicio de muy alta concurrencia (`docs/12`, v4/v5), no para la investigación y el cálculo central de V1/V2 |

Python no se elige por ser "el mejor" en abstracto — se elige por ser el único ya implícito en la evidencia documental del proyecto y el que mejor encaja con su dominio de cálculo real.

---

# 3. Base de datos: PostgreSQL

**Decisión:** PostgreSQL, ya diseñado a nivel físico en `docs/33-Modelo-Fisico-PostgreSQL.md` (DATA-005) — esta misión formaliza su elección al nivel de stack oficial, sin rediseñar ninguna tabla, tipo o restricción ya definida allí.

| Criterio | Por qué PostgreSQL lo cumple |
|---|---|
| **Consistencia** | ACID completo y transacciones estrictas — imprescindible para que ninguna predicción quede parcialmente escrita (`docs/14`: "nunca se sobrescribe"; `docs/30`: append-only) |
| **Relaciones** | Motor relacional maduro, exactamente lo que exige el modelo de 14 tablas y sus relaciones 1:N/1:1/N:M ya diseñadas (`docs/32`/`docs/33`) |
| **Consultas analíticas** | Soporte robusto de agregaciones, funciones de ventana y CTEs recursivas — necesarias para las métricas de cartera (ROI, Yield, Drawdown) que `docs/33` ya identificó como series calculadas sobre muchas filas de `auditorias`, no como columnas de una sola |
| **Escalabilidad** | Particionado nativo, índices avanzados (`GIN` sobre `JSONB`, ya recomendado en `docs/33` §6) y una trayectoria de crecimiento sin necesidad de cambiar de motor en V2/V3 |

---

# 4. Framework: FastAPI

**Decisión:** FastAPI como framework oficial de la capa de servicio (API que expone el Runtime, `docs/29`).

- **Simplicidad:** sintaxis mínima basada en *type hints* nativos de Python, reduce código repetitivo frente a frameworks más pesados (ej. Django, pensado para aplicaciones con interfaz web completa, innecesaria aquí).
- **Documentación automática:** genera especificación OpenAPI/Swagger directamente de los tipos ya declarados — beneficio inmediato para un proyecto que ya exige contrato explícito en cada capa (`docs/16`, `docs/30`).
- **Integración con Pydantic:** FastAPI usa Pydantic de forma nativa para validar entrada y salida — encaja exactamente con `PredictionRequest` y `PredictionReport` (`docs/25`/`docs/29`), que pueden modelarse literalmente como esquemas Pydantic validados en cada solicitud, sin una capa de validación adicional.

---

# 5. ORM: SQLAlchemy 2.x

**Decisión:** SQLAlchemy 2.x como capa de acceso a datos oficial.

**Justificación:** es el ORM/*toolkit* de acceso a datos más maduro y ampliamente adoptado del ecosistema Python. Su estilo 2.x (`Mapped`/`mapped_column`, tipado explícito) es coherente con la exigencia de tipado estático de la sección 10 (MyPy), y soporta de forma directa los tipos ya definidos en `docs/33` sin fricción: `UUID` nativo de PostgreSQL, `JSONB`, `TIMESTAMP` con zona horaria.

**Reconciliación explícita con `docs/33`:** aunque ese documento fue redactado en términos de JPA/Hibernate (Java), su diseño físico (tablas, tipos conceptuales, claves, índices) es agnóstico del ORM elegido — SQLAlchemy puede implementar exactamente el mismo modelo de 14 tablas sin ningún cambio de fondo. Solo la sección 9 de `docs/33` ("Compatibilidad", redactada en términos de Spring Data JPA/Hibernate) queda desactualizada por esta decisión — no el modelo físico en sí (ver "Observaciones", hallazgo 1).

---

# 6. Migraciones: Alembic

**Decisión:** Alembic como herramienta oficial de migraciones — el equivalente, dentro del ecosistema SQLAlchemy, de lo que `docs/33` §9 ya preveía con Flyway/Liquibase para un ecosistema Java. El orden de migración sigue siendo exactamente el mismo grafo de dependencias acíclico ya fijado en `docs/32` §6: `competiciones` → `torneos` → (`selecciones`, `estadios`, `arbitros`) → `jugadores` → `partidos` → (`convocatorias`, `estadisticas_partido`, `lesiones`, `cuotas`, `predicciones`, `resultados`) → `auditorias`. Cada tabla de `docs/33` §4 sigue siendo una migración candidata individual — el cambio de herramienta no altera ese orden.

---

# 7. Librerías científicas: NumPy, Pandas, SciPy

| Librería | Rol dentro del Modelo Santiago |
|---|---|
| **NumPy** | Álgebra vectorizada de bajo nivel — sustento de la matriz de probabilidades conjuntas que `engine/03-Poisson.md`/`models/poisson.md` ya anticipan (`docs/25` §5, "matriz de marcadores") |
| **Pandas** | Manipulación tabular — encaja directamente con la forma actual de la Base de Conocimiento (`data/processed/`, CSV) y con las transformaciones ya descritas conceptualmente por la Capa de Preparación de Variables (`docs/15`: leer, validar, normalizar, construir) |
| **SciPy** | Funciones estadísticas y distribuciones de probabilidad ya implementadas y validadas (`scipy.stats.poisson`, funciones de distribución acumulada) — evita reimplementar manualmente la Distribución de Poisson que `models/poisson.md` ya fundamenta matemáticamente, reduciendo el riesgo de introducir un error de implementación sobre una fórmula ya investigada |

---

# 8. Validación: Pydantic

**Decisión:** Pydantic como capa oficial de validación de datos, transversal a toda la aplicación — no solo dentro de FastAPI (sección 4). Modela `PredictionRequest` y `PredictionReport` (`docs/25`, `docs/29`) como esquemas validados en tiempo de ejecución, y puede representar el Contrato Oficial de Variables (`docs/16`: tipo, unidad, rango, nulabilidad) como un esquema verificable por código, en lugar de solo documentado en prosa.

---

# 9. Testing: pytest

**Decisión:** pytest como framework oficial de pruebas.

**Alcance:**

- Pruebas unitarias de cada motor (`engine/01` a `06`), una vez cada uno tenga su Versión 2.0 respaldada en `models/`.
- Pruebas de integración del Runtime y sus componentes (`docs/26`/`docs/29`), verificando el orden por capas y la frontera de escritura del `PredictionContext` (`docs/30` §3).
- Pruebas de regresión de la Capa de Preparación de Variables (`docs/15`) contra el Contrato Oficial de Variables (`docs/16`): que cada variable se entregue con el tipo, rango y nulabilidad ya contratados.

**Fuera del alcance de esta decisión:** pruebas de carga/rendimiento — no existe todavía evidencia de un volumen de datos que las justifique (`CLAUDE.md`: no anticipar sin evidencia).

---

# 10. Calidad de código: Ruff, MyPy

| Herramienta | Elección | Justificación |
|---|---|---|
| **Ruff** | Adoptada, para *linting* y formateo | Escrito en Rust, sustancialmente más rápido que las alternativas dispersas (`flake8` + `isort` + `pyupgrade`); desde sus versiones recientes incluye también un formateador compatible con el estilo de Black — permite cubrir *lint* y formato con una única herramienta |
| **Black** | **No se adopta como herramienta separada** | `ruff format` ya cubre el mismo estilo de formateo que Black, sin necesitar mantener dos herramientas con responsabilidad solapada — reduce la superficie de configuración (`CLAUDE.md`, Modo de Trabajo: "evitar añadir complejidad innecesaria") |
| **MyPy** | Adoptado, para tipado estático | Exige que el código declare tipos explícitos — coherente con la filosofía de "contrato explícito" que ya domina toda la documentación del proyecto (`docs/16`, `docs/30`); sin tipado estático verificado en CI, esa misma filosofía se perdería exactamente en la capa donde más importa: el código real |

---

# 11. Gestión del proyecto: uv, `pyproject.toml`

**Decisión:** `uv` como gestor de entornos y dependencias oficial (sobre `pip` puro).

**Justificación:** `uv` resuelve e instala dependencias sustancialmente más rápido que `pip` (implementado en Rust), incluye gestión de entornos virtuales integrada, y usa `pyproject.toml` como única fuente de verdad — evita necesitar `pip` + `venv` + una herramienta adicional de resolución de dependencias por separado. Se reconoce que `pip` tiene más años de adopción y es más universalmente conocido, pero no aporta ninguna ventaja que `uv` no iguale o supere, y el proyecto no tiene todavía código heredado que dependa específicamente de `pip` — no existe costo de migración que pagar por elegir la opción más simple desde el principio.

**`pyproject.toml`:** archivo único de metadatos del proyecto, dependencias, y configuración de Ruff/MyPy/pytest — reduce la dispersión de archivos de configuración (`setup.py`, `setup.cfg`, `.flake8`, etc., ya en desuso en el ecosistema moderno de Python).

**Estructura de dependencias (conceptual, sin crear el archivo real — fuera de alcance):**

- **Dependencias de producción:** FastAPI, SQLAlchemy, Alembic, Pydantic, NumPy, Pandas, SciPy, y un *driver* de PostgreSQL — necesario para que SQLAlchemy pueda conversar con el motor elegido (sección 3), no mencionado explícitamente en el brief pero indispensable para que el stack funcione. Se recomienda `psycopg` (versión 3), sucesor activamente mantenido de `psycopg2`, con soporte nativo asíncrono si en el futuro FastAPI lo requiere.
- **Dependencias de desarrollo:** pytest, Ruff, MyPy — separadas de las de producción, patrón estándar de `pyproject.toml` (grupo de dependencias opcional/de desarrollo).

---

# 12. Contenedores: Docker

**Decisión:** Docker como tecnología oficial de contenerización.

**Componentes que se dockerizan:**

- La aplicación Python/FastAPI (una imagen de servicio).
- PostgreSQL (imagen oficial, para desarrollo y pruebas locales — si en producción se usa un servicio gestionado en lugar de un contenedor propio es una decisión de infraestructura futura, fuera de esta misión).
- Opcionalmente, un contenedor de migraciones (Alembic) ejecutado como paso previo al arranque del servicio.

Docker Compose se menciona como la herramienta natural de orquestación de estos componentes en entornos de desarrollo local — ningún `Dockerfile` ni `docker-compose.yml` se escribe en esta misión (fuera de alcance explícito).

---

# 13. Versiones mínimas

**Advertencia de honestidad epistémica, antes de fijar cifras:** el conocimiento de este Arquitecto IA tiene un corte temporal (enero 2026), mientras que la fecha real del proyecto es julio 2026. No se afirma con certeza cuál es la versión estable más reciente de cada herramienta en este momento exacto — fijar esa cifra sin poder verificarla violaría "Nunca inventar información" (`CLAUDE.md`). En su lugar, se fija un **piso mínimo verificable y ya estable a la fecha de corte del conocimiento**, con la instrucción explícita de preferir, al momento real de implementación, la versión estable más reciente disponible que no esté próxima a su fin de soporte (End of Life).

| Tecnología | Versión mínima congelada | Justificación |
|---|---|---|
| **Python** | 3.12 | Estable y con soporte de seguridad activo a la fecha de corte de este documento; se instruye preferir la versión estable más reciente disponible al implementar (previsiblemente 3.13 o posterior, dado el ciclo anual de releases de Python) — nunca una versión próxima a su EOL |
| **PostgreSQL** | 16 | Estable, con soporte activo, sin restricción sobre `JSONB`, índices parciales o CTEs recursivas (todas ya usadas en `docs/33`); se instruye preferir la versión estable más reciente al implementar, especialmente relevante si se busca soporte nativo de generación UUIDv7 (`docs/33` §8), función que versiones más recientes del motor tienden a incorporar primero |
| **Docker Engine** | 24.x | Versión estable con soporte activo a la fecha de corte; se instruye igual preferir la versión estable más reciente al implementar |

**Ninguna versión aquí listada debe interpretarse como un techo** — son pisos mínimos, no versiones objetivo fijas. Verificar la vigencia real de cada una al iniciar la implementación es responsabilidad explícita de esa futura misión, no de esta.

---

# 14. Fuera de alcance de esta misión

- No se implementa código.
- No se crea la estructura de carpetas de un proyecto Python (`src/`, `pyproject.toml` real, etc.).
- No se modifica el Runtime, el Engine, las Variables Oficiales, los modelos matemáticos de `models/`, el `PredictionContext` ni la Base de Conocimiento.
- No se escribe ningún `Dockerfile`, `docker-compose.yml`, migración de Alembic, ni esquema Pydantic real.
- No se corrige la sección 9 de `docs/33-Modelo-Fisico-PostgreSQL.md` (Java/Spring/JPA/Hibernate) — se documenta como hallazgo pendiente, no se edita en esta misión.

---

# Restricciones (confirmación de cumplimiento)

Esta misión no modifica el Runtime, el Engine, las Variables Oficiales, los modelos matemáticos, el `PredictionContext` ni la Base de Conocimiento. No implementa código ni genera estructura de carpetas — únicamente oficializa una decisión de stack ya evaluada.

---

# Validaciones obligatorias

- **¿El stack soporta toda la arquitectura actual?** Sí — Python/FastAPI puede implementar el Runtime y sus siete componentes (`docs/29`) sin modificar ninguno; SQLAlchemy puede materializar exactamente las 14 tablas de `docs/33`; Pydantic puede expresar el `PredictionContext` (`docs/30`) y el Contrato de Variables (`docs/16`) como esquemas verificables.
- **¿No contradice ningún documento existente?** **Con una única excepción, declarada explícitamente, no ocultada:** la sección 9 de `docs/33-Modelo-Fisico-PostgreSQL.md` fue redactada asumiendo Java/Spring Data JPA/Hibernate/Flyway/Liquibase — esta decisión oficial la reemplaza por Python/SQLAlchemy/Alembic. El **modelo físico en sí** (tablas, tipos, claves, índices) no queda contradicho —es agnóstico de ORM/lenguaje, como el propio `docs/33` ya declaraba en sus tipos conceptuales—, pero su sección de compatibilidad sí queda desactualizada. Ver "Observaciones", hallazgo 1, y la recomendación de misión siguiente.
- **¿Permite implementar exactamente el Runtime ya diseñado?** Sí — ninguna decisión de esta misión exige rediseñar `PredictionRequest`, `PredictionContext`, `VariablePreparation`, `EngineRunner`, `PredictionAssembler`, `PredictionReport` ni `Persistence` (`docs/29` §2).
- **¿Soporta el crecimiento hacia V2?** Sí — `docs/12-Roadmap.md` ya proyecta "v2: Python", y el ecosistema científico elegido (NumPy/Pandas/SciPy) es también la base natural de "v3: Machine Learning" (ej. `scikit-learn`, que se integra en el mismo ecosistema sin cambiar de lenguaje ni de base de datos).

---

# Cierre obligatorio

**1. ¿Por qué este stack fue elegido?**
Porque es la única evidencia documental real y preexistente del proyecto (`docs/12`: v2 = Python), porque su ecosistema científico encaja directamente con el dominio de investigación estadística ya desarrollado en `models/`, y porque cada pieza individual (FastAPI, SQLAlchemy, Pydantic, pytest, Ruff, MyPy, uv) se justifica por continuidad de filosofía con el resto del proyecto (contrato explícito, simplicidad, evitar complejidad sin evidencia).

**2. ¿Qué alternativas fueron descartadas y por qué?**
Java, C#, Node.js y Go como lenguaje principal (sección 2, tabla comparativa) — ninguno ofrece el mismo ecosistema científico maduro sin reimplementación o dependencias externas; Black como formateador independiente (`ruff format` ya cubre el mismo rol); `pip` puro como gestor de dependencias (`uv` lo iguala o supera sin costo de migración).

**3. ¿Qué ventajas aporta para el Modelo Santiago?**
Cierra, por primera vez, la ambigüedad tecnológica que `docs/26`/`docs/29`/`docs/30` dejaron deliberadamente abierta; da continuidad real al roadmap ya documentado; y resuelve, en una única decisión oficial, la inconsistencia que `docs/33` había introducido sin mandato.

**4. ¿Qué componentes utilizarán cada tecnología?**
FastAPI expone el Runtime como servicio; SQLAlchemy + Alembic implementan las 14 tablas de `docs/33`; Pydantic valida `PredictionRequest`/`PredictionReport` y el Contrato de Variables; NumPy/Pandas/SciPy ejecutan el cálculo real de `engine/01-06` una vez tengan Versión 2.0; pytest valida todo lo anterior; Ruff/MyPy garantizan calidad de código; Docker empaqueta la aplicación y PostgreSQL para desarrollo.

**5. ¿Qué tecnologías quedan explícitamente fuera del proyecto?**
Java, Spring Boot, Hibernate, JPA, Flyway, Liquibase (el stack que `docs/33` había asumido sin mandato); Black como herramienta de formateo independiente; `pip` puro como gestor principal de dependencias; cualquier motor de base de datos distinto de PostgreSQL.

**6. ¿Qué decisiones tecnológicas quedan completamente congeladas?**
Las trece de las secciones 2 a 13: lenguaje (Python), base de datos (PostgreSQL), framework (FastAPI), ORM (SQLAlchemy 2.x), migraciones (Alembic), librerías científicas (NumPy/Pandas/SciPy), validación (Pydantic), testing (pytest), calidad de código (Ruff, MyPy), gestión de proyecto (`uv`, `pyproject.toml`), contenedores (Docker), y los pisos mínimos de versión de la sección 13.

**7. ¿Qué documento deberá utilizar este stack como referencia?**
Toda futura misión `DEV-`/`DATA-`/`IMP-` que implemente código real, y en particular una futura reconciliación de `docs/33` §9, que deberá reescribirse en términos de SQLAlchemy/Alembic en lugar de JPA/Hibernate/Flyway/Liquibase.

**8. ¿Qué misión recomendarías inmediatamente después?**
Dos, en este orden de prioridad: (a) una misión de reconciliación editorial de `docs/33` §9 (Compatibilidad), para alinearla con esta decisión oficial — se recomienda como la más urgente, por ser la única contradicción activa detectada por esta misión (Constitución, Art. 7: toda contradicción debe documentarse y resolverse, nunca quedar abierta silenciosamente); (b) la primera fórmula matemática real en `models/poisson.md`, que sigue siendo, transversalmente, el bloqueante compartido de toda la serie `DEV-`/`MODEL-` para que este stack tenga algo real que calcular.

**9. ¿El proyecto queda oficialmente listo para iniciar implementación?**
En el eje tecnológico, sí — es la primera vez que el proyecto tiene una decisión de stack completa y sin ambigüedad. En el eje matemático, no todavía — sigue pendiente, como en cada cierre anterior de la serie `DEV-`/`DATA-`, al menos una fórmula real en `models/` con Versión 2.0.

**10. ¿Consideras que termina aquí la fase de diseño y comienza formalmente la fase de construcción?**
No completamente todavía, pero se acerca más que en cualquier misión anterior. La fase de diseño arquitectónico (qué existe, cómo se relaciona, con qué se construye) queda, con esta misión, prácticamente cerrada. Lo que impide declarar el cierre formal de la fase de diseño y el inicio de la de construcción son las mismas dos condiciones ya identificadas: (a) la contradicción activa de `docs/33` §9 todavía sin reconciliar (Constitución, Art. 10: "ausencia de contradicciones documentadas de gravedad Crítica" como condición para iniciar implementación de código — esta sí es de gravedad relevante, por tocar directamente la tecnología recién congelada); (b) la ausencia total, todavía, de una fórmula matemática con Versión 2.0 en `models/`. Ninguna de las dos es un defecto de esta misión — son, precisamente, las dos tareas que deberían ejecutarse antes de escribir la primera línea de código real.

---

# Observaciones

*(Hallazgos detectados durante el análisis, registrados con el mismo rigor que el objetivo principal — Manual Operativo, `docs/22`, sección 7.)*

1. **Contradicción activa y de alta relevancia: `docs/33-Modelo-Fisico-PostgreSQL.md` §9 ("Compatibilidad") asume Java + Spring Data JPA + Hibernate + Flyway/Liquibase, mientras que esta misión oficializa Python + SQLAlchemy + Alembic.** No es una inconsistencia menor: esa sección justifica decisiones de nombrado de columnas (`snake_case` compatible con `SpringPhysicalNamingStrategy`) y de generación de identificadores (`@GeneratedValue` de Hibernate 6) en términos específicos del ecosistema Java, ninguno de los cuales aplica a SQLAlchemy. **El modelo físico en sí —las 14 tablas, sus tipos conceptuales, claves e índices— no queda afectado**, porque `docs/33` ya lo diseñó de forma agnóstica al ORM (tipos conceptuales, no anotaciones de código). Se recomienda explícitamente, y con prioridad alta (ver Cierre, pregunta 8), una misión de reconciliación editorial dedicada a reescribir únicamente la sección 9 de `docs/33` en términos de SQLAlchemy 2.x/Alembic. **Esto sí cambia la prioridad del roadmap vigente:** se recomienda ejecutarla antes que la siguiente investigación matemática de `models/`, por ser aislada, de bajo riesgo, y porque deja de crecer cuanto antes se corrija (mismo patrón ya aplicado por el proyecto a `INC-18` en `AR-001`).
2. **La serie `ARCH-` es nueva.** A diferencia de `DEV-` (diseño de ejecución) y `DATA-` (modelo de datos), esta serie está dedicada específicamente a decisiones de arquitectura *tecnológica* congeladas — se distingue de ambas para que una futura consulta a `docs/00-Project-Tracker.md` no confunda "cómo se ejecuta el modelo" (`DEV-`) o "cómo se modelan los datos" (`DATA-`) con "con qué tecnología concreta se construye" (`ARCH-`).

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Las versiones mínimas de la sección 13 se fijan con una advertencia explícita de incertidumbre por el corte de conocimiento de este Arquitecto IA (enero 2026) frente a la fecha real del proyecto (julio 2026) — es un supuesto declarado, no oculto, pero sigue siendo un supuesto: la versión estable real disponible hoy podría ser distinta de la asumida.
- **¿Qué parte de este entregable podría estar equivocada?** La decisión de no adoptar Black como herramienta separada de Ruff asume que `ruff format` es, en la práctica, suficientemente maduro y estable para el estilo que el equipo de implementación finalmente prefiera — es una decisión razonable hoy, pero una implementación futura podría encontrar un caso de formato donde Black y `ruff format` difieran de forma relevante.
- **¿Qué información me habría hecho falta para tener más certeza?** Una estimación real de volumen de datos y de concurrencia esperada habría permitido justificar con más precisión decisiones como UUID vs. `BIGSERIAL` (ya tomada en `docs/33`, reafirmada aquí implícitamente) o la necesidad real de async en FastAPI/SQLAlchemy — hoy esa estimación no existe en ningún documento del proyecto.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que, al iniciar la implementación real, las versiones mínimas de la sección 13 sigan siendo razonables (no EOL) en ese momento — es, explícitamente, responsabilidad de esa futura misión, no de esta.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí — se podría haber interpretado que `docs/33` ya "decidía" Java de forma vinculante y que esta misión necesitaría un proceso de reconciliación formal antes de reemplazarlo. Se optó por tratar la asunción de `docs/33` como lo que ella misma declaró ser (un hallazgo pendiente sin mandato oficial, no una decisión firme), lo que permite a esta misión resolverla directamente en lugar de bloquearse esperando una reconciliación previa — pero se documenta la contradicción con total transparencia (Observaciones, hallazgo 1) en lugar de asumir silenciosamente que nunca existió.

---

Fin del documento.
