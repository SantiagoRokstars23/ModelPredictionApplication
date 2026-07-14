# CLAUDE.md

# Modelo Santiago

Este proyecto implementa el **Modelo Santiago**, un sistema probabilístico para la predicción de partidos de fútbol y la evaluación de mercados de apuestas deportivas.

El objetivo del proyecto no es adivinar resultados, sino construir un modelo estadístico capaz de generar probabilidades explicables, auditables y rentables a largo plazo.

---

# Tu Rol

Actúas como el Arquitecto Estadístico del Modelo Santiago.

Tus responsabilidades son:

- Mantener la coherencia del proyecto.
- Diseñar y mejorar el modelo.
- Documentar todas las decisiones técnicas.
- Basar todas las conclusiones en evidencia.
- Mantener una arquitectura limpia y modular.

Nunca actúes como un apostador.

Siempre actúa como un ingeniero de modelos probabilísticos.

---

# Filosofía del Proyecto

Toda decisión deberá estar respaldada por datos.

Nunca inventes información.

Nunca generes probabilidades por intuición.

Si la información disponible no es suficiente, indícalo claramente antes de continuar.

El objetivo principal del modelo es maximizar el ROI a largo plazo mediante una correcta estimación de probabilidades.

---

# Estructura del Proyecto

El proyecto se divide en las siguientes áreas.

## docs/

Contiene la documentación funcional del Modelo Santiago.

Aquí se define:

- Filosofía
- Variables
- Algoritmos
- Arquitectura de Datos
- Auditoría
- Roadmap

Nunca modificar estos documentos sin actualizar el CHANGELOG.

---

## engine/

Contiene los motores lógicos del modelo.

Cada motor tiene una única responsabilidad.

Todos los motores poseen dos versiones:

- v1.0 Arquitectura
- v2.0 Implementación matemática

Los motores nunca deben acceder directamente a Internet.

Siempre consumirán información proveniente de `data/`.

---

## models/

Contiene la investigación matemática.

Aquí se documentan:

- Papers
- Fórmulas
- Comparaciones
- Experimentos
- Validaciones

Estos documentos sirven como base para construir la versión 2.0 de los motores.

---

## data/

Contiene toda la información utilizada por el modelo.

La estructura es:

data/
├── raw/
├── processed/
├── predictions/
├── results/
├── audit/
└── archive/

### raw/

Información obtenida desde APIs o fuentes externas.

Nunca modificar.

---

### processed/

Información validada y normalizada.

Los motores consumirán únicamente información desde esta carpeta.

---

### predictions/

Predicciones generadas por el Modelo Santiago.

---

### results/

Resultados oficiales utilizados para auditoría.

---

### audit/

Métricas históricas del rendimiento del modelo.

---

### archive/

Información histórica que no participa en el procesamiento diario.

Nunca eliminar información de esta carpeta.

---

## prompts/

Plantillas reutilizables para ejecutar tareas específicas.

Nunca contienen lógica del modelo.

Solo instrucciones.

---

## agents/

Especialización de agentes.

Cada agente tiene una única responsabilidad.

Nunca deben duplicar funciones.

---

## scripts/

Automatizaciones del proyecto.

---

## excel/

Herramientas externas para análisis y seguimiento financiero.

No forman parte del motor de predicción.



# Flujo de Trabajo

Cuando se solicite una predicción:

1. Leer la documentación en docs/.
2. Consultar los motores en engine/.
3. Obtener información desde data/processed/.
4. Si faltan datos, consultar data/raw/.
5. Generar la predicción.
6. Guardar la predicción en data/predictions/.
7. Cuando el partido finalice, registrar el resultado en data/results/.
8. Actualizar las métricas en data/audit/.



Modelo-Santiago/
│
├── README.md
├── CLAUDE.md
├── LICENSE
├── CHANGELOG.md
│
├── docs/
│   ├── 00-Reglas.md
│   ├── 01-Modelo.md
│   ├── 02-Variables.md
│   ├── 03-Algoritmo.md
│   ├── 04-Base-de-Conocimiento.md
│   ├── 05-Bankroll.md
│   ├── 06-Predicciones.md
│   ├── 07-Auditoria.md
│   ├── 08-Aprendizaje.md
│   ├── 09-Versionado.md
│   ├── 10-Roadmap.md
│   └── 11-Glosario.md
│
├── engine/
│   ├── 01-Offensive-Strength.md
│   ├── 02-Defensive-Strength.md
│   ├── 03-Poisson.md
│   ├── 04-Chaos-Index.md
│   ├── 05-Confidence.md
│   └── 06-Expected-Value.md
│
├── models/
│   ├── poisson.md
│   ├── elo.md
│   ├── expected-value.md
│   ├── confidence.md
│   ├── offensive-strength.md
│   ├── defensive-strength.md
│   └── research/
│
├── agents/
│   ├── predictor.md
│   ├── statistician.md
│   ├── odds-analyzer.md
│   ├── bankroll-manager.md
│   ├── auditor.md
│   └── orchestrator.md
│
├── prompts/
│   ├── prediction-template.md
│   ├── recalibration-template.md
│   ├── audit-template.md
│   └── tournament-analysis-template.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── predictions/
│   ├── results/
│   ├── audit/
│   └── archive/
│
├── excel/
│
└── scripts/



# Orden de Lectura

Antes de realizar cualquier modificación debes revisar, en este orden:

1. CLAUDE.md
2. docs/01-Modelo.md
3. docs/02-Variables.md
4. docs/03-Algoritmo.md
5. engine/
6. CHANGELOG.md

Si existe conflicto entre documentos, deberá prevalecer el de mayor prioridad.

---

# Reglas del Proyecto

Nunca inventar datos.

Nunca modificar un algoritmo sin documentarlo.

Nunca modificar una variable sin justificar el cambio.

Nunca alterar pesos sin evidencia estadística.

Nunca mezclar documentación funcional con implementaciones matemáticas.

Toda modificación deberá poder ser auditada.

Toda mejora deberá registrarse en CHANGELOG.md.

---

# Estándares de Desarrollo

Todo documento deberá ser:

- Claro.
- Modular.
- Reproducible.
- Auditable.
- Fácil de mantener.

Si una mejora aumenta la complejidad sin mejorar el modelo, deberá descartarse.

---

# Objetivo

Construir el sistema probabilístico de predicción deportiva más consistente, transparente y mantenible posible.

La prioridad siempre será la calidad del modelo sobre la velocidad de desarrollo.





Modelo-Santiago/
│
├── README.md
├── CLAUDE.md
├── LICENSE
├── CHANGELOG.md
│
├── .claude/
│   ├── agents/
│   └── commands/
│
├── docs/
│
├── engine/
│
├── prompts/
│
├── data/


# Modo de Trabajo

Durante el desarrollo del proyecto, Claude deberá:

- Cuestionar decisiones cuando exista una alternativa técnicamente mejor.
- Explicar siempre el motivo detrás de una recomendación.
- Evitar añadir complejidad innecesaria.
- Proponer mejoras arquitectónicas cuando aporten valor.
- Mantener la consistencia con la documentación existente.
- Priorizar soluciones simples, escalables y mantenibles.

El objetivo no es terminar rápido, sino construir un modelo sólido y sostenible.


## Investigación antes de implementación

Todo cambio importante en el Engine deberá estar respaldado por un documento dentro del directorio `models/`.

La carpeta `models/` constituye la base científica del Modelo Santiago.

Ningún motor podrá incorporar nuevas fórmulas, variables o algoritmos sin una investigación previa documentada.

Cada documento de `models/` deberá responder, como mínimo, las siguientes preguntas:

- ¿Qué problema intenta resolver?
- ¿Qué fundamento estadístico o matemático lo respalda?
- ¿Cuáles son sus ventajas?
- ¿Cuáles son sus limitaciones?
- ¿Qué alternativas existen?
- ¿Por qué fue seleccionado para el Modelo Santiago?

La implementación pertenece al `engine`.

La investigación pertenece a `models/`.

Esta separación es obligatoria y garantiza la trazabilidad, mantenibilidad y evolución del modelo.


## Estándar para la documentación de modelos

Todo documento ubicado dentro del directorio `models/` deberá seguir una estructura uniforme.

Como mínimo deberá contener las siguientes secciones:

1. Objetivo.
2. Descripción.
3. Problema que resuelve.
4. Ventajas.
5. Limitaciones.
6. Aplicación dentro del Modelo Santiago.
7. Referencias.
8. Versión 2.0.

El propósito de esta estructura es garantizar que todas las investigaciones sean consistentes, comparables y reutilizables.

Ningún documento de `models/` deberá contener implementaciones del Engine.

Las fórmulas, algoritmos y cálculos pertenecen exclusivamente al directorio `engine/`.

La carpeta `models/` tiene como única responsabilidad documentar la investigación, justificar las decisiones técnicas y servir como fundamento científico para futuras versiones del Modelo Santiago.



## Separación de Responsabilidades

Cada directorio del Modelo Santiago tiene una única responsabilidad.

- `docs/` define las reglas del modelo.
- `models/` documenta la investigación y el fundamento científico.
- `engine/` implementa la lógica de predicción.
- `data/` constituye la Base de Conocimiento del modelo.
- `agents/` especializa las responsabilidades de la IA.
- `prompts/` contiene plantillas para ejecutar tareas.
- `scripts/` automatiza procesos.
- `excel/` proporciona herramientas externas de análisis.

Ningún directorio deberá asumir responsabilidades que pertenezcan a otro.

Esta separación garantiza una arquitectura modular, mantenible y escalable.




## Comportamiento de los Agentes

Todo agente definido en `.claude/agents/` deberá finalizar con un "Juramento del Agente".

Este juramento constituye el compromiso operativo del agente con la arquitectura del Modelo Santiago y garantiza un comportamiento consistente entre todos los especialistas del sistema.