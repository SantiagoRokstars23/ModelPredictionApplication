# Runtime Oficial del Modelo Santiago

**Archivo:** `docs/26-Runtime-del-Modelo.md`

**Misión:** DEV-001 — Runtime Oficial del Modelo Santiago

**Versión:** 1.0.0

**Estado:** Especificación de ejecución — independiente del lenguaje, sin implementar código

---

# Objetivo

Describir **cómo** se ejecutará el Modelo Santiago cuando exista una implementación en código — el recorrido completo de una solicitud, de entrada a informe final — sin elegir lenguaje, sin diseñar clases, sin tocar el **qué** (arquitectura, variables, motores, algoritmo), ya definido en `docs/06`, `docs/14`, `docs/15`, `docs/16`, `docs/17` y `docs/25`.

**Corrección de una discrepancia detectada antes de escribir:** el brief de esta misión ilustra la ejecución del Engine como una secuencia estrictamente lineal (`engine/01 → 02 → 03 → 04 → 05 → 06`). La arquitectura ya establecida y verificada tres veces (`docs/06`, "Diagrama de dependencias del Engine"; `docs/17`; `docs/25`, sección 5) no es lineal: `engine/01` y `engine/02` se ejecutan en paralelo (Capa 1), igual que `engine/04` y `engine/05` (Capa 3). Este documento usa el orden por capas ya establecido, no el lineal del ejemplo — reproducir el lineal habría introducido una contradicción nueva con `docs/06`/`docs/25`, exactamente lo que la validación 5 de esta misión exige evitar.

---

# 1. Punto de entrada

Ya definido, campo por campo, en `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`, sección 1 — no se repite. Resumen de referencia: selección local, selección visitante, competición, torneo, fecha (obligatorios); hora local, mercado solicitado, gestión de bankroll (opcionales). El Runtime es quien recibe este punto de entrada y lo entrega al Orchestrator (`docs/06`, Fase 1).

---

# 2. Construcción del Contexto del Partido

El Runtime consulta la Base de Conocimiento **una única vez por predicción**, en el orden ya definido en `docs/14-Prediction-Pipeline.md`, Etapa 2 (los 10 archivos de `data/processed/selecciones-nacionales/`, en orden). No se repite ese orden aquí.

En esta fase el Runtime **no calcula probabilidades ni ejecuta ningún motor** — coordina dos pasos ya especificados en otros documentos, sin fusionarlos ni redefinirlos:

1. Recuperación de datos de negocio (`docs/14`, Etapa 2).
2. Preparación de Variables Oficiales por la Capa de Preparación de Variables (`docs/15`), devolviendo las 12 variables ya validadas y normalizadas (`docs/16`), 10 activas y 2 formalmente diferidas tras `MR-004`.

El resultado de esta fase es el **Objeto de Contexto** (sección 3) — el Runtime nunca vuelve a tocar la Base de Conocimiento después de construirlo, salvo la única excepción ya documentada (`engine/06` y `cuotas.csv`, `INC-05`, resuelta en principio, pendiente de implementación completa).

---

# 3. Objeto de Contexto

*(Aporte nuevo de esta misión — ningún documento anterior formaliza un único objeto que viaje durante toda la ejecución.)*

El Objeto de Contexto es la única estructura que el Runtime pasa entre fases. Es de **solo-anexado (append-only)**: cada motor puede leer todo lo que ya contiene, pero solo puede agregar una sección nueva con su propia salida — nunca modifica ni elimina lo que otro motor ya escribió. Este es el mecanismo concreto que garantiza, en tiempo de ejecución, el principio de no acceso directo a la Base de Conocimiento (`docs/15`).

| Sección | Contenido | Quién la escribe | Quién puede leerla |
|---|---|---|---|
| Identificación | Selecciones, competición, torneo, fecha, estadio, árbitro (si asignados) | Runtime, al construir el contexto (sección 2) | Todos los motores |
| Variables Oficiales | Las 12 variables (`docs/16`), cada una con su valor o su marca explícita de "no disponible" | Capa de Preparación de Variables (`docs/15`) | Todos los motores, según `docs/17` |
| Metadatos de preparación | Versión del Modelo Santiago, timestamp de construcción del contexto | Runtime | Persistencia (sección 6), Logs (sección 7) |
| Resultados parciales | Fuerza Ofensiva/Defensiva, Goles Esperados, Probabilidades, Top de marcadores, Índice de Caos, Índice de Confianza, Valor Esperado | Cada motor agrega la suya, en el orden de la sección 4 | Los motores de capas posteriores; el Runtime, al consolidar el informe (sección 5) |

Una vez que el Objeto de Contexto existe, **ningún motor consulta `data/processed/` de nuevo** — cada uno lee únicamente lo que ya está en el objeto (variables oficiales y/o resultados parciales de motores anteriores).

---

# 4. Ejecución del Engine

El Runtime ejecuta el Engine por capas, no de forma estrictamente lineal (ver corrección al inicio de este documento), siguiendo exactamente el orden ya definido en `docs/06`/`docs/17`/`docs/25`:

```
Objeto de Contexto (Identificación + Variables Oficiales)
        │
        ▼
Capa 1 (en paralelo):
   engine/01-Offensive-Strength.md  ──► agrega: Fuerza Ofensiva
   engine/02-Defensive-Strength.md  ──► agrega: Fuerza Defensiva
        │
        ▼
Capa 2:
   engine/03-Poisson.md (+ Variable009 Localía, directa del contexto)
        ──► agrega: Goles Esperados, Probabilidades, Top de marcadores
        │
        ▼
Capa 3 (en paralelo):
   engine/04-Chaos-Index.md         ──► agrega: Índice de Caos
   engine/05-Confidence.md (+ Variable010 Historial Directo, directa)
        ──► agrega: Índice de Confianza
        │
        ▼
Capa 4:
   engine/06-Expected-Value.md      ──► agrega: Valor Esperado
        ⚠ excepción documentada: además de leer el Objeto de Contexto,
          consulta cuotas.csv directamente (INC-05, resuelta en principio,
          no en implementación completa — ver docs/16, "Reglas generales")
        │
        ▼
Objeto de Contexto completo (todas las secciones de la tabla de la sección 3 llenas)
```

Cada motor, sin excepción salvo la ya anotada: recibe el objeto, agrega su sección, nunca elimina lo que ya existía, nunca vuelve a consultar la Base de Conocimiento.

---

# 5. Construcción del Informe Final

El Runtime consolida el Objeto de Contexto completo (sección 4) en el contrato de salida ya definido — no se redefine el formato aquí, conforme a la restricción explícita de esta misión. Referencias: `docs/14-Prediction-Pipeline.md`, Etapa 2 ("Información que debe devolver al usuario"), y `docs/25-Trazado-de-Ejecucion-del-Prediction-Pipeline.md`, sección 6 (objeto de respuesta completo, incluidos los dos campos ya marcados como no disponibles en V1: `jugadores_destacados`, `mercados_detectados`).

La única responsabilidad del Runtime en este paso es **transformar** el Objeto de Contexto (estructura interna de ejecución) en el objeto de respuesta (contrato externo hacia el usuario) — son estructuras distintas por diseño: el Objeto de Contexto expone detalles internos (metadatos de preparación, estado de cada variable) que el objeto de respuesta no necesita mostrar al usuario.

---

# 6. Persistencia

Ya especificado en `docs/14-Prediction-Pipeline.md` (Etapas 3-4). El Runtime dispara cada registro exactamente en el momento ya definido — no se redefine el "qué" ni el "cuándo", solo se confirma la responsabilidad de cada uno desde la perspectiva de ejecución:

| Registro | El Runtime lo dispara cuando... | Responsabilidad |
|---|---|---|
| `data/predictions/` | El informe final (sección 5) está construido, siempre antes del inicio del partido | Evidencia inmutable de qué predijo el modelo y con qué versión |
| `data/results/` | El partido finaliza y existe un resultado oficial verificable | Verdad de referencia para la Auditoría — el Runtime no la calcula, solo la registra |
| `data/audit/` | Existen tanto la predicción como el resultado para el mismo partido | Métricas históricas de rendimiento — nunca se calcula antes de que ambos registros existan |

---

# 7. Registro de ejecución (Logs)

*(Aporte nuevo de esta misión — ningún documento anterior especifica qué debe registrar el Runtime sobre su propia ejecución, a diferencia de qué predicción produce.)*

Eventos mínimos que el Runtime debe registrar en cada ejecución, independientemente del formato de log elegido en la implementación:

| Evento | Cuándo | Propósito |
|---|---|---|
| Inicio de ejecución | Al recibir el punto de entrada (sección 1) | Trazabilidad — cuándo empezó a procesarse la solicitud |
| Versión del modelo utilizada | Al construir el Objeto de Contexto | Requisito ya vigente (`data/predictions/README.md`) — el log es donde se origina ese dato |
| Variables utilizadas y su estado | Al completar la Capa de Preparación de Variables | Permite auditar, después, exactamente qué variables participaron y cuáles se marcaron no disponibles |
| Motores ejecutados y su orden real | Después de cada capa (sección 4) | Verifica en producción que el orden por capas se respetó |
| Duración de cada fase | Al cerrar cada capa y al finalizar | Insumo de rendimiento, no de predicción — nunca se usa como variable del modelo |
| Errores detectados | En el momento exacto en que ocurren (sección 8) | Nunca se descartan silenciosamente — todo error queda en el registro aunque el flujo continúe |

Ningún evento de este registro se convierte en una Variable Oficial ni afecta el cálculo — es una capa de observabilidad, paralela y subordinada a la ejecución, nunca parte de ella.

---

# 8. Manejo de errores

Ya especificado, situación por situación, en `docs/06-Flujo-Operacional.md`, tabla "Manejo de errores" — no se redefine. Se confirma aquí, para las 5 situaciones que el brief de esta misión señala explícitamente, que ya tienen regla vigente y cuál es:

| Situación | Regla ya vigente (`docs/06`) |
|---|---|
| Faltan datos | Si son críticos (variable obligatoria): detener antes de ejecutar el Engine. Si son secundarios: continuar, marcar como no disponible |
| Información inconsistente | Se rechaza el valor puntual, nunca se corrige automáticamente (`docs/05-Base-de-Conocimiento.md`) |
| Un motor no puede ejecutarse | Las capas siguientes tampoco se ejecutan — el fallo se propaga hacia adelante, nunca se sustituye por un valor estimado |
| No existen cuotas | Se omite la Fase 4 (Valor Esperado) explícitamente; nunca se estima |
| El partido ya fue predicho | No se genera una segunda predicción silenciosamente; se informa la existente |

La única responsabilidad nueva del Runtime frente a estas reglas ya vigentes es registrarlas en el log de ejecución (sección 7) en el momento en que ocurren — el comportamiento en sí no cambia.

---

# 9. Principios del Runtime

Instancia operativa de los principios ya fijados en `docs/21-Constitucion-del-Modelo-Santiago.md`, Artículo 2 — no se redefinen, se muestra cómo se manifiestan concretamente en la ejecución:

| Principio | Cómo se manifiesta en el Runtime |
|---|---|
| **Desacoplamiento** | El Objeto de Contexto (sección 3) es el único canal entre la Base de Conocimiento y los motores — ningún motor conoce el origen físico de un dato |
| **Reproducibilidad** | El mismo Objeto de Contexto, ejecutado de nuevo, debe producir el mismo informe final — el Runtime no introduce aleatoriedad no documentada |
| **Trazabilidad** | Todo lo que el informe final afirma puede reconstruirse desde el Objeto de Contexto y el log de ejecución (secciones 3 y 7) |
| **Determinismo** | El orden de ejecución por capas (sección 4) es fijo — el Runtime nunca decide dinámicamente en qué orden ejecutar un motor |
| **Independencia del lenguaje** | Ninguna sección de este documento asume un lenguaje, un paradigma (orientado a objetos, funcional, etc.) ni una tecnología de almacenamiento concreta — el Objeto de Contexto es una estructura lógica, no una clase |
| **Separación de responsabilidades** | El Runtime coordina; nunca calcula (eso es `engine/`), nunca decide qué dato usar (eso es la Capa de Preparación), nunca aprueba cambios (eso es el Arquitecto Estadístico Humano) |

---

# Validaciones obligatorias

- **¿El Runtime puede implementarse en cualquier lenguaje?** Sí — ninguna sección usa terminología específica de un paradigma o tecnología; el Objeto de Contexto se describe como estructura lógica (secciones/campos), no como una clase o tipo de un lenguaje concreto.
- **¿Ningún motor consulta directamente la Base de Conocimiento?** Confirmado, con la única excepción ya documentada y heredada de `INC-05` (`engine/06`/cuotas) — no se oculta, se repite explícitamente en la sección 4.
- **¿El Runtime respeta el Prediction Pipeline?** Sí — las secciones 1, 2, 5 y 6 son, explícitamente, una capa de ejecución sobre `docs/14`/`docs/25`, sin redefinir su contenido.
- **¿La arquitectura permanece completamente desacoplada?** Sí, salvo la misma excepción ya conocida — este documento no introduce ningún acoplamiento nuevo.
- **¿Existe contradicción con `docs/06`, `docs/25` o `docs/99`?** No — se corrigió explícitamente, antes de escribir, la única discrepancia detectada (el orden lineal del ejemplo del brief frente al orden por capas ya establecido), para que este documento sea consistente con los tres.

---

# Cierre obligatorio

**1. ¿Qué responsabilidad tiene el Runtime?**
Coordinar la ejecución de principio a fin — construir el Objeto de Contexto, invocar el Engine en el orden correcto, consolidar el informe final, disparar la persistencia y registrar su propia ejecución. Nunca calcula, nunca decide sobre datos, nunca aprueba cambios.

**2. ¿Qué componentes coordina?**
La Base de Conocimiento (a través de la Capa de Preparación de Variables), los 6 motores del Engine, y los tres registros de persistencia (`predictions/`, `results/`, `audit/`).

**3. ¿Qué información recibe?**
El punto de entrada de la sección 1 — selecciones, competición, torneo, fecha, y opcionalmente hora, mercado y bankroll.

**4. ¿Qué información entrega?**
El informe final consolidado (sección 5), ya especificado en `docs/25`, y el registro de ejecución (sección 7) como subproducto de observabilidad.

**5. ¿Qué componentes nunca deben conocer la Base de Conocimiento?**
Los 6 motores del Engine, sin excepción de diseño — la única excepción hoy (`engine/06`/cuotas) es una deuda documentada, no una regla del Runtime.

**6. ¿Qué ventajas aporta este diseño?**
Formaliza, por primera vez, un único objeto (el Objeto de Contexto) que hace cumplible en tiempo de ejecución un principio que hasta ahora solo existía como regla documental (`docs/15`) — y dota al proyecto de una capa de observabilidad (logs) que no existía en ningún documento anterior.

**7. ¿Qué permitirá implementar después?**
Cualquier lenguaje o tecnología puede implementar el Runtime siguiendo esta especificación sin necesidad de volver a diseñar el flujo — el trabajo de implementación se reduce a elegir estructuras de datos concretas para el Objeto de Contexto y conectar los 6 motores ya especificados.

**8. ¿Qué parte queda pendiente antes de comenzar a escribir código?**
Las mismas tres que ya identificó `docs/25`: las fórmulas matemáticas de `models/` (ninguna tiene Versión 2.0 todavía), el Contrato de Datos de Mercado completo (cierra `INC-05`), y una decisión de stack tecnológico — que este documento deliberadamente no toma, por diseño.

**9. ¿Qué misión recomendarías después?**
La misma recomendada por `IMP-001` y `MAP-001`: la primera investigación matemática real en `models/`, empezando por `models/poisson.md`. Es la única pieza que, si sigue pendiente, bloquea que el Runtime aquí diseñado calcule algo real en lugar de solo coordinar estructuras vacías.

**10. ¿Puede considerarse que el Modelo Santiago está listo para iniciar la implementación de la V0.1?**
El diseño de ejecución sí está listo — este documento cierra la última pieza puramente arquitectónica (cómo se ejecuta, no solo qué existe). Pero **no todavía en sentido estricto**: sin al menos una fórmula matemática real en `models/`, cualquier código escrito hoy coordinaría un Objeto de Contexto correctamente estructurado que no podría producir un número real. La arquitectura está lista; el contenido matemático que la hace calculable, no.

---

# Fuera de alcance de esta misión

- No se implementa código.
- No se diseñan clases, tipos ni estructuras de un lenguaje concreto.
- No se elige lenguaje ni tecnología.
- No se modifica el Engine, variables, algoritmos, pesos, fórmulas, `learning/` ni el Pipeline ya definido.
- No se redefine el formato del informe final — ya documentado en `docs/14`/`docs/25`.

---

Fin del documento.
