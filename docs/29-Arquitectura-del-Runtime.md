# Arquitectura de Implementación del Runtime

**Archivo:** `docs/29-Arquitectura-del-Runtime.md`

**Misión:** DEV-002 — Arquitectura de Implementación del Runtime

**Versión:** 1.0.0

**Estado:** Especificación arquitectónica de implementación — independiente del lenguaje, sin implementar código

---

# Objetivo

`docs/26-Runtime-del-Modelo.md` (DEV-001) especifica **qué hace** el Runtime: construye el Objeto de Contexto, invoca el Engine por capas, consolida el informe y dispara la persistencia. Ese documento no se redefine aquí — se da un paso más cerca de la implementación: **nombrar y delimitar los componentes internos** que materializarán esa especificación cuando exista código real, sin elegir lenguaje, sin diseñar clases y sin tocar fórmulas, variables o algoritmos.

Este documento responde una pregunta que `docs/26` deja intencionalmente a nivel de flujo: *si mañana alguien escribe código siguiendo esta arquitectura, ¿en cuántas piezas se divide el Runtime, qué nombre tiene cada una, y quién es responsable de qué?*

## Qué responsabilidad tiene el Runtime

Coordinar la ejecución completa de una predicción, de principio a fin: recibir la solicitud, construir el contexto, invocar el Engine en el orden correcto, consolidar el informe, y disparar la persistencia. Es la misma responsabilidad ya fijada en `docs/26`, sección 9 ("Separación de responsabilidades") — este documento no la amplía, solo la reparte entre componentes con nombre propio.

## Qué NO hace el Runtime

- No calcula probabilidades, fuerzas, caos, confianza ni valor esperado — eso es `engine/`.
- No decide qué dato de negocio alimenta qué variable — eso es la Capa de Preparación de Variables (`docs/15`).
- No valida si hay datos suficientes para intentar una predicción — eso es el Statistician (`docs/06`, Fase 2), que actúa antes de que el Runtime construya el contexto.
- No aprueba cambios de peso, variable o algoritmo — eso pertenece, en exclusiva, al Arquitecto Estadístico Humano (`docs/21`, Artículo 5).
- No elige tecnología, lenguaje ni estructura de almacenamiento — eso queda fuera de alcance de toda la serie `DEV-`, por diseño.

---

# 1. Relación con los documentos ya existentes (léase antes de continuar)

Este documento no repite ni redefine:

| Documento | Qué ya define | Qué aporta este documento |
|---|---|---|
| `docs/06-Flujo-Operacional.md` | Fases 0-10, diagrama de dependencias del Engine por capas, manejo de errores | Ninguna fase nueva — solo nombra los componentes que ejecutan la Fase 3 internamente |
| `docs/14-Prediction-Pipeline.md` | Orden de archivos, contrato de salida, registro y actualización de la Base de Conocimiento | Ninguna etapa nueva — los componentes aquí definidos son quienes ejecutan esas etapas |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | Responsabilidad, entrada, salida y validaciones de la Capa de Preparación de Variables | Le asigna el nombre de componente `VariablePreparation` dentro de esta arquitectura, sin alterar ninguna de sus reglas |
| `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md` | Objeto de entrada, traza numérica, objeto de respuesta completo | Nombra esos dos objetos (`PredictionRequest`, `PredictionReport`) como componentes de la arquitectura de implementación |
| `docs/26-Runtime-del-Modelo.md` | El Runtime, el Objeto de Contexto (append-only), la ejecución por capas, los logs, el manejo de errores | Descompone el Runtime en componentes con nombre propio y define, por primera vez, quién escribe y quién lee cada sección del Objeto de Contexto |

**Regla de equivalencia (para que no se lea como una redefinición):** `PredictionContext` de este documento **es** el Objeto de Contexto de `docs/26`, sección 3 — mismo objeto, mismas reglas de solo-anexado, ahora con un nombre estable de cara a la implementación. Ninguna sección de `docs/26` queda contradicha.

---

# 2. Componentes

```
PredictionRequest
        │
        ▼
PredictionContext
        │
        ▼
VariablePreparation
        │
        ▼
EngineRunner
        │
        ▼
PredictionAssembler
        │
        ▼
PredictionReport
        │
        ▼
Persistence
```

Cada flecha representa una transformación, nunca una llamada arbitraria: cada componente recibe exactamente lo que el anterior produjo, y no conoce nada del componente que lo sucede.

| Componente | Qué es | Equivalente ya especificado |
|---|---|---|
| `PredictionRequest` | El objeto de entrada de una predicción | `docs/25`, sección 1 |
| `PredictionContext` | El objeto central que viaja por toda la ejecución, de solo-anexado | `docs/26`, sección 3 (Objeto de Contexto) |
| `VariablePreparation` | El componente que transforma la Base de Conocimiento en las 12 Variables Oficiales | `docs/15` (Capa de Preparación de Variables) |
| `EngineRunner` | El componente que invoca los 6 motores del Engine en el orden por capas ya fijado | `docs/06` (diagrama de dependencias), `docs/17`, `docs/26` sección 4 — nunca antes tuvo nombre propio, separado del Runtime genérico |
| `PredictionAssembler` | El componente que transforma el `PredictionContext` completo en el contrato de salida | `docs/26`, sección 5 (Construcción del Informe Final) |
| `PredictionReport` | El objeto de respuesta final, entregado al usuario y registrado | `docs/25`, sección 6 |
| `Persistence` | El componente que escribe en `data/predictions/`, `data/results/` y `data/audit/` | `docs/26`, sección 6; `docs/14`, Etapas 3-4 |

`EngineRunner` y `PredictionAssembler` son los dos únicos aportes genuinamente nuevos de esta misión: `docs/26` ya describía "ejecutar el Engine" y "construir el informe" como pasos del Runtime, pero nunca los aisló como componentes con responsabilidad y frontera propias. El resto de la tabla da nombre estable a objetos que ya existían.

---

# 3. `PredictionContext`

Mismo objeto que `docs/26`, sección 3, con la misma regla de solo-anexado (append-only): cada componente puede leer todo lo ya escrito, pero solo puede agregar la sección que le pertenece — nunca modifica ni elimina lo que otro componente ya escribió.

Lo que este documento aporta, y que `docs/26` no detallaba, es la **frontera de escritura por componente** — quién exactamente puede agregar cada sección:

| Sección | Contenido | Quién la escribe | Quién la lee |
|---|---|---|---|
| Identificación | Selecciones, competición, torneo, fecha, estadio, árbitro (si asignados) | El propio Runtime, al recibir el `PredictionRequest` | Todos los componentes posteriores |
| Metadatos de preparación | Versión del Modelo Santiago, timestamp de construcción | El propio Runtime | `PredictionAssembler`, `Persistence` |
| Variables Oficiales | Las 12 variables (`docs/16`), cada una con su valor o su marca de "no disponible" | `VariablePreparation`, una única vez | `EngineRunner` (cada motor, según `docs/17`) |
| Resultados parciales | Fuerza Ofensiva/Defensiva, Goles Esperados, Probabilidades, Top de marcadores, Índice de Caos, Índice de Confianza, Valor Esperado | `EngineRunner`, una sección por motor, en el orden de la sección 4 | Motores de capas posteriores (dentro de `EngineRunner`); `PredictionAssembler` |
| Estado de ejecución | Ver sección 6 de este documento (Completa / Completa sin Valor Esperado / Detenida) | El propio Runtime, al cerrar cada capa | `PredictionAssembler`, `Persistence`, log de ejecución |

**Ningún componente distinto del que aparece en la columna "Quién la escribe" puede escribir en esa sección.** `PredictionAssembler`, en particular, nunca escribe en el `PredictionContext` — solo lo lee para producir el `PredictionReport`, que es un objeto distinto (ver sección 8).

---

# 4. Orden de ejecución

**Corrección aplicada antes de escribir, por la misma razón que en `docs/26`:** el orden de ejemplo de esta misión lista los motores como si `Engine01` y `Engine02` se ejecutaran uno después del otro. La arquitectura ya establecida y verificada en `docs/06`, `docs/17` y `docs/26` los ejecuta **en paralelo** (Capa 1), igual que `Engine04` y `Engine05` (Capa 3, que el propio orden de esta misión sí agrupa correctamente con "+"). Se usa aquí el orden por capas, no el lineal, para no introducir una contradicción nueva con los tres documentos ya vigentes.

```
PredictionRequest
        │
        ▼
Runtime construye PredictionContext (Identificación + Metadatos)
        │
        ▼
VariablePreparation ──► agrega: Variables Oficiales
        │
        ▼
EngineRunner
        │
        ├─ Capa 1 (en paralelo): Engine01 + Engine02 ──► Fuerza Ofensiva / Fuerza Defensiva
        │
        ▼
        Capa 2: Engine03 (+ Variable009 Localía, directa) ──► Goles Esperados, Probabilidades, Top marcadores
        │
        ▼
        Capa 3 (en paralelo): Engine04 + Engine05 (+ Variable010 Historial Directo, directa en Engine05)
                              ──► Índice de Caos / Índice de Confianza
        │
        ▼
        Capa 4: Engine06 (si hay cuotas) ──► Valor Esperado
                ⚠ excepción documentada: además de leer PredictionContext,
                  consulta cuotas.csv directamente (INC-05, ver sección 5 de este documento)
        │
        ▼
PredictionContext completo (todas las secciones de la sección 3 llenas o marcadas)
        │
        ▼
PredictionAssembler ──► construye PredictionReport
        │
        ▼
Persistence ──► data/predictions/
        │
        ▼
(el partido se juega — tiempo después)
        │
        ▼
Persistence ──► data/results/ ──► data/audit/
```

Este orden es exactamente el mismo que `docs/26`, sección 4 — la única diferencia es que aquí cada paso queda asignado a un componente con nombre (`EngineRunner` para toda la ejecución del Engine, `PredictionAssembler` para el paso final, `Persistence` para los tres registros), en vez de atribuirse genéricamente al "Runtime".

---

# 5. Responsabilidades

| Componente | Hace | Nunca hace |
|---|---|---|
| Runtime | Recibe `PredictionRequest`; construye la Identificación y los Metadatos del `PredictionContext`; invoca `VariablePreparation`, `EngineRunner`, `PredictionAssembler` y `Persistence`, en ese orden; registra el log de ejecución (`docs/26`, sección 7) | Calcular, decidir suficiencia de datos, aprobar cambios de peso |
| `PredictionRequest` | Representa la solicitud validada (selecciones, competición, torneo, fecha, y opcionalmente hora, mercado, bankroll — `docs/25`, sección 1) | Contener lógica de cálculo; ser mutado tras su creación |
| `PredictionContext` | Transportar, de forma append-only, todo lo que se conoce de una predicción en curso | Ser modificado por un componente distinto al dueño de cada sección (sección 3); persistirse tal cual (se transforma primero en `PredictionReport`) |
| `VariablePreparation` | Transformar la Base de Conocimiento en las 12 Variables Oficiales, validadas y normalizadas (`docs/15`) | Calcular probabilidades, fuerzas, caos o valor esperado; decidir si vale la pena predecir con datos parciales (`docs/15`, sección 1) |
| `EngineRunner` | Invocar `engine/01` a `engine/06` en el orden por capas de la sección 4; agregar cada resultado parcial al `PredictionContext`; detectar y propagar el fallo de un motor (sección 6) | Leer `data/processed/` directamente (excepción documentada: `engine/06`/cuotas, heredada de `INC-05`); decidir dinámicamente un orden distinto al ya fijado |
| `PredictionAssembler` | Leer el `PredictionContext` completo y transformarlo en el contrato de salida (`PredictionReport`) | Escribir en el `PredictionContext`; calcular ningún valor nuevo — solo transforma lo que ya existe |
| `PredictionReport` | El contrato de salida hacia el usuario y hacia `Persistence` (`docs/25`, sección 6) | Exponer detalles internos de ejecución (metadatos de preparación, estado interno de cada variable) que no forman parte del contrato externo |
| `Persistence` | Escribir en `data/predictions/` (al cerrar el `PredictionReport`), `data/results/` (cuando exista resultado oficial) y `data/audit/` (cuando existan ambos) | Calcular métricas de auditoría por sí misma (eso es el Auditor, `docs/06`, Fase 8); modificar un registro ya escrito (inmutabilidad, `docs/14`) |

Esta tabla es la versión "por componente" de la tabla ya existente "Responsabilidades por módulo" de `docs/06` — no la reemplaza (esa tabla sigue siendo la referencia a nivel de fases y agentes); esta es su equivalente al nivel de implementación del Runtime.

---

# 6. Manejo de errores

Ya especificado, situación por situación, en `docs/06-Flujo-Operacional.md` (tabla "Manejo de errores") y confirmado en `docs/26`, sección 8 — no se redefine ninguna regla aquí. Lo que aporta esta sección es **a qué componente le corresponde cada paso** del ciclo que pide el brief de esta misión:

```
Un motor falla dentro de EngineRunner
        │
        ▼
EngineRunner detecta el fallo y no agrega la sección de resultado parcial correspondiente
        │
        ▼
Runtime registra el evento en el log de ejecución (docs/26, sección 7) —
        nunca se descarta silenciosamente
        │
        ▼
¿Puede continuar? (regla ya vigente en docs/06, tabla "Manejo de errores")
        │
        ├─ No (el motor fallido alimenta a capas posteriores) ──► EngineRunner detiene
        │                                                          las capas siguientes;
        │                                                          el fallo se propaga
        │                                                          hacia adelante, nunca
        │                                                          se sustituye por un
        │                                                          valor estimado
        │
        └─ Sí (excepción ya documentada: ausencia de cuotas para Engine06,
              Fase 4 condicional — no es un fallo, es una omisión esperada)
              ──► EngineRunner continúa sin esa sección
        │
        ▼
Runtime marca el Estado de ejecución final en PredictionContext (ver tabla siguiente)
```

**Estados de ejecución posibles** (aporte nuevo de esta misión — ni `docs/06` ni `docs/26` categorizaban explícitamente el resultado final de una ejecución, solo el manejo de cada error puntual):

| Estado | Cuándo ocurre | Qué recibe el usuario |
|---|---|---|
| Completa | Las 4 capas del Engine se ejecutaron y existen cuotas para Valor Esperado | `PredictionReport` con los 9 campos de `docs/25`, sección 6, todos con valor |
| Completa sin Valor Esperado | Las Capas 1-3 se ejecutaron; no existían cuotas registradas (Fase 4 omitida, `docs/06`) | `PredictionReport` con `valor_esperado: "no disponible — sin cuotas registradas"`, el resto completo |
| Detenida antes del Engine | `VariablePreparation` no pudo construir una variable obligatoria (Nivel A, `docs/16`/`docs/17`) | Ningún `PredictionReport` — el Orchestrator informa al usuario qué falta y por qué, antes de invocar `EngineRunner` |
| Detenida durante el Engine | Un motor de una capa intermedia falló y las capas siguientes no pudieron ejecutarse | Ningún `PredictionReport` completo; el fallo y la capa exacta quedan en el log de ejecución para su diagnóstico |

Este estado no es una Variable Oficial ni afecta ningún cálculo — es, igual que el log de ejecución de `docs/26`, una capa de observabilidad paralela y subordinada a la ejecución.

---

# 7. Persistencia

Ya especificado en `docs/14`, Etapas 3-4, y en `docs/26`, sección 6 — se confirma aquí, sin redefinir el "qué" ni el "cuándo", qué dispara cada registro:

| Registro | Lo dispara... | Cuándo |
|---|---|---|
| `data/predictions/` | `Persistence`, invocado por el Runtime inmediatamente después de que `PredictionAssembler` entrega el `PredictionReport` | Siempre antes del inicio del partido, nunca después (`docs/14`, Etapa 3) |
| `data/results/` | `Persistence`, cuando existe un resultado oficial verificable | Un proceso externo al ciclo de una predicción individual (`docs/06`, Fase 7) — no lo calcula el Runtime, solo lo registra |
| `data/audit/` | `Persistence`, cuando existen tanto la predicción como el resultado para el mismo partido | Nunca antes de que ambos registros existan (`docs/06`, Fase 8) |

**Sobre `PredictionRequest` — resolución explícita de una ambigüedad del brief:** este documento decide, por justificación de datos (`CLAUDE.md`, "Principio de Justificación de Datos"), que el `PredictionRequest` **no se persiste como un registro independiente**. Ya queda capturado dos veces por mecanismos ya existentes: (1) transitoriamente, en el evento "Inicio de ejecución" del log (`docs/26`, sección 7); (2) permanentemente, como parte del campo `partido` del `PredictionReport` ya registrado en `data/predictions/` (`docs/25`, sección 6). Crear un cuarto registro solo para la solicitud cruda duplicaría un dato ya trazable desde el `PredictionReport`, violando "Una única fuente de verdad para cada dato" (`CLAUDE.md`).

---

# 8. Reporte

El `PredictionAssembler` es el único componente responsable de transformar el `PredictionContext` completo (o el estado alcanzado antes de una detención, sección 6) en el `PredictionReport` — el contrato de salida ya definido en `docs/25`, sección 6, y `docs/14`, Etapa 2. Este documento no redefine ese formato (fuera de alcance explícito de esta misión); solo fija el flujo:

```
PredictionContext completo
        │
        ▼
PredictionAssembler lee (nunca escribe):
   - Identificación                  ──► campo "partido"
   - Resultados parciales (Engine03) ──► "probabilidades", "top_marcadores"
   - Resultados parciales (Engine04) ──► "indice_caos"
   - Resultados parciales (Engine05) ──► "confianza"
   - Resultados parciales (Engine06, si existe) ──► "valor_esperado"
   - Variables Oficiales que efectivamente participaron ──► "variables_influyentes"
   - Metadatos de preparación        ──► "version_modelo"
        │
        ▼
PredictionAssembler genera id_prediccion (id_partido + timestamp)
        │
        ▼
PredictionReport (objeto de respuesta completo, docs/25 sección 6)
```

`PredictionAssembler` **transforma, nunca calcula**: cada campo del `PredictionReport` ya existe, en alguna forma, dentro del `PredictionContext` — la única responsabilidad de este componente es dar forma de contrato de salida a información que el Engine ya produjo. Esta es la misma distinción que `docs/26`, sección 5, ya establecía entre "estructura interna de ejecución" y "contrato externo hacia el usuario" — aquí queda, además, asignada a un componente concreto.

---

# 9. Compatibilidad

Verificación explícita, documento por documento, de que ninguna sección anterior contradice lo ya especificado:

| Documento | Verificación |
|---|---|
| `docs/06-Flujo-Operacional.md` | El orden por capas de la sección 4 es idéntico al "Diagrama de dependencias del Engine"; el manejo de errores de la sección 6 no introduce ninguna regla nueva, solo asigna las ya vigentes a `EngineRunner`/Runtime |
| `docs/14-Prediction-Pipeline.md` | La Etapa 2 (motores que ejecuta, información que devuelve) se preserva sin cambios en las secciones 4 y 8; la Etapa 3 (registro) se preserva sin cambios en la sección 7 |
| `docs/15-Capa-de-Preparacion-de-Variables.md` | `VariablePreparation` conserva exactamente las mismas responsabilidades, entradas, salidas y validaciones — solo recibe un nombre de componente |
| `docs/17-Matriz-de-Consumo-de-Variables.md` | El consumo de variables por motor (incluida la excepción de `engine/06`/cuotas) se hereda sin alteración dentro de `EngineRunner` |
| `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md` | `PredictionRequest` y `PredictionReport` son, campo por campo, los mismos objetos ya definidos en las secciones 1 y 6 de ese documento |
| `docs/26-Runtime-del-Modelo.md` | `PredictionContext` es el mismo Objeto de Contexto, con la misma regla append-only; el log de ejecución y el manejo de errores no se redefinen, solo se les asigna un componente emisor |
| `engine/01` a `engine/06` | Ninguno se modifica; `EngineRunner` los invoca exactamente en el orden y con las entradas ya declaradas en cada uno |
| `models/` (los 6 documentos) | Ninguna fórmula se toca; esta arquitectura sigue sin poder calcular un número real hasta que exista Versión 2.0 de cada motor (misma conclusión que `docs/26`, pregunta 8 del cierre) |

No se detecta ninguna contradicción nueva.

---

# Validaciones obligatorias

- **¿Algún componente rompe el desacoplamiento?** No, con la misma única excepción ya conocida y heredada: `EngineRunner`, al invocar `engine/06`, además de leer `PredictionContext` consulta `cuotas.csv` directamente (`INC-05`, resuelta en principio en `MR-004`, pendiente de implementación completa). Ningún otro componente accede a `data/processed/` — solo `VariablePreparation` (que es, precisamente, la pieza diseñada para hacerlo) y, para persistir, `Persistence`.
- **¿`PredictionContext` es suficiente para ejecutar todo el modelo?** Sí — contiene, en un único objeto append-only, todo lo que cualquier componente posterior necesita leer (Identificación, Variables Oficiales, Resultados parciales, Metadatos, Estado de ejecución). Ningún componente de la sección 2 necesita una fuente de información adicional fuera de `PredictionContext`, salvo la excepción ya señalada de `EngineRunner`/cuotas.
- **¿El Runtime puede implementarse exactamente como está diseñado?** Sí, en cualquier lenguaje: ninguna sección de este documento asume una tecnología, un paradigma ni una estructura de datos concreta — cada componente se describe por su responsabilidad y su frontera de lectura/escritura, no por una clase o un tipo.

---

# Cierre obligatorio

**1. ¿Qué responsabilidad tiene el Runtime?**
La misma ya fijada en `docs/26`: coordinar de principio a fin — construir el contexto, invocar el Engine, consolidar el informe, disparar la persistencia. Este documento no la cambia, solo la reparte entre siete componentes con nombre propio.

**2. ¿Qué objeto es el corazón del sistema?**
`PredictionContext` — el mismo Objeto de Contexto de `docs/26`, ahora con una frontera de escritura explícita por sección (sección 3 de este documento).

**3. ¿Qué componente coordina la ejecución?**
El Runtime construye el contexto inicial e invoca, en orden, a `VariablePreparation`, `EngineRunner`, `PredictionAssembler` y `Persistence`. Dentro de la ejecución del Engine específicamente, `EngineRunner` es quien coordina el orden por capas de los 6 motores — es el aporte de nombre más significativo de esta misión, porque `docs/26` nunca lo aisló como pieza propia.

**4. ¿Qué componente construye el reporte?**
`PredictionAssembler` — lee el `PredictionContext` completo (o su estado al detenerse) y lo transforma en `PredictionReport`, sin calcular ningún valor nuevo (sección 8).

**5. ¿Qué componente persiste la información?**
`Persistence` — el único componente que escribe en `data/predictions/`, `data/results/` y `data/audit/`, en los tres momentos ya fijados por `docs/14` y `docs/26` (sección 7 de este documento).

**6. ¿Qué riesgos arquitectónicos detectaste?**
Ninguno nuevo respecto a los ya inventariados por `MR-001`/`AR-001`/`AR-002`. Se reafirma el único riesgo estructural relevante para esta misión: `EngineRunner`, al heredar la excepción de `engine/06`/cuotas (`INC-05`), es el único componente de los siete cuya frontera de desacoplamiento no es absoluta — un riesgo ya documentado, no uno nuevo introducido aquí. Un riesgo menor, propio de esta misión: si en el futuro se implementa código nombrando estos siete componentes literalmente (`PredictionRequest`, `PredictionContext`, etc.) como clases o módulos, deberá mantenerse la disciplina de que `PredictionAssembler` nunca escriba en `PredictionContext` — la tabla de la sección 3 es la única fuente de verdad sobre quién escribe qué, y una implementación descuidada podría romper esa regla sin que ningún documento lo detecte automáticamente (es una regla de disciplina de implementación, no verificable desde la documentación).

**7. ¿Qué faltaría para comenzar la implementación en código?**
Las mismas tres piezas ya identificadas por `docs/25`/`docs/26`: (a) al menos una fórmula matemática real en `models/` con Versión 2.0 (ninguna la tiene todavía); (b) el Contrato de Datos de Mercado completo, que cerraría la excepción de `EngineRunner`/cuotas en implementación (`INC-05`); (c) una decisión de stack tecnológico, que esta serie `DEV-` no toma por diseño.

**8. ¿Puede iniciarse la V0.1 después de este documento?**
No todavía, en sentido estricto — misma conclusión que `docs/26`. Esta misión cierra un nivel adicional de diseño (los componentes internos del Runtime, con nombre y frontera), pero no resuelve lo que ya bloqueaba a `docs/26`: sin una fórmula matemática real, cualquier código escrito hoy sobre estos siete componentes coordinaría correctamente una ejecución que no puede producir un número real todavía.

---

# Autocrítica

*(Sección exigida por `docs/22-Manual-Operativo-del-Arquitecto-IA.md`, sección 8, para toda misión de arquitectura.)*

- **¿Qué supuestos hice sin poder verificarlos completamente?** Que los nombres en inglés del brief (`PredictionRequest`, `PredictionContext`, etc.) se referían exactamente a los objetos ya especificados en español por `docs/25`/`docs/26`, y no a conceptos nuevos y distintos. Se verificó comparando campo por campo (secciones 1 y 3 de este documento) antes de asumir la equivalencia, pero la correspondencia exacta solo podrá confirmarse del todo cuando exista una implementación real.
- **¿Qué parte de este entregable podría estar equivocada?** La decisión de no persistir `PredictionRequest` como registro independiente (sección 7) es una interpretación razonable del principio de justificación de datos, pero el brief lo listaba explícitamente junto a predicción/auditoría/resultado como si mereciera persistencia propia — una lectura alternativa válida sería que sí debería registrarse de forma independiente por razones de auditoría de solicitudes (ej. detectar solicitudes repetidas antes de que lleguen al Runtime). Se documenta la decisión tomada y su justificación explícitamente para que sea revisable.
- **¿Qué información me habría hecho falta para tener más certeza?** Un ejemplo de implementación real (aunque sea en pseudocódigo, fuera del alcance de esta misión) habría permitido confirmar si la frontera de escritura de `PredictionContext` (sección 3) es suficientemente precisa para evitar ambigüedad en tiempo de código.
- **¿Qué validaría antes de que esto se implemente o se tome como definitivo?** Que la primera implementación de código real (cuando exista) efectivamente respete la tabla de "quién escribe qué" de la sección 3 sin que ningún componente necesite acceso de escritura fuera de su sección asignada.
- **¿Existe una interpretación razonable distinta a la que elegí?** Sí, ya señalada arriba sobre la persistencia de `PredictionRequest`. También es razonable considerar `EngineRunner` como parte del propio Runtime en lugar de un componente separado (la línea entre "el Runtime invoca al Engine" y "un componente aparte invoca al Engine" es, en última instancia, una decisión de nomenclatura); se eligió separarlo porque el brief lista explícitamente `EngineRunner` como un eslabón propio de la cadena de componentes.

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se diseñan clases, tipos ni estructuras de un lenguaje concreto.
- No se elige lenguaje ni tecnología.
- No se modifica el Engine, variables, algoritmos, pesos, fórmulas, `learning/`, el Pipeline ni el Runtime ya definido en `docs/26`.
- No se redefine el formato del informe final — ya documentado en `docs/14`/`docs/25`.
- No se resuelve `INC-05` (Contrato de Datos de Mercado) — se hereda como excepción documentada, igual que en `docs/26`.

---

Fin del documento.
