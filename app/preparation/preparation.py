"""`VariablePreparation` -- construye el bloque `context.variables` con datos
reales, donde es posible calcularlos sin inventar información.

Ver docs/15-Capa-de-Preparacion-de-Variables.md (responsabilidad conceptual),
docs/16-Contrato-Oficial-de-Variables.md (las 12 Variables Oficiales),
docs/17-Matriz-de-Consumo-de-Variables.md (qué motor consume cada una),
docs/29-Arquitectura-del-Runtime.md (interfaz `VariablePreparationProtocol`,
BUILD-005), docs/30-Contrato-Oficial-del-Prediction-Context.md, sección 4.3
(forma exacta del bloque `variables`), docs/03-Variables.md (estado real de
"Método de cálculo" por variable -- decisivo para BUILD-017), `models/
offensive-strength.md` §6.1 y §17-27 (`MODEL-001`/`MODEL-009` -- única
autoridad matemática de Variable003), `models/defensive-strength.md` §6.2 y
§13-21 (`MODEL-002`/`MODEL-010` -- única autoridad matemática de Variable004),
`models/rendimiento-torneo.md` (`MODEL-012` -- única autoridad matemática de
Variable002, ver "BUILD-021" más abajo), `models/forma-reciente.md`
(`MODEL-011` -- única autoridad matemática de Variable001, ver "BUILD-020"
más abajo), app/persistence/preparation_repository.py (BUILD-017/BUILD-021
-- Variable010/Variable002), app/preparation/potencial_ofensivo_repository.py
(BUILD-018 -- Variable003).

BUILD-017: reemplaza la implementación estructural de BUILD-006 por una
implementación funcional. No modifica `VariablePreparationProtocol.preparar`
(mismo protocolo, BUILD-005), `PredictionContext`, el Runtime, `EngineRunner`
ni ningún motor.

BUILD-018: implementa Variable003 (Potencial Ofensivo) con dato real,
siguiendo **exclusivamente** `models/offensive-strength.md` en su versión
vigente tras `MODEL-009` (§6.1, §17-27) -- ninguna fórmula anterior, ninguna
nota del brief, ninguna interpretación personal. No modifica `Engine01`,
`EngineRunner`, `PredictionContext` ni `Persistence`: la lectura de datos
nueva que esta variable necesita vive en `app/preparation/potencial_
ofensivo_repository.py` (dentro del único paquete que este brief autoriza a
modificar en profundidad), no en `app/persistence/`. `VariablePreparation.
__init__` gana un segundo colaborador opcional
(`potencial_ofensivo_repository`), con un valor por defecto -- la firma
`preparar(context)` y el primer parámetro (`repository`) no cambian,
preservando compatibilidad total con `BUILD-006`/`BUILD-009`/`BUILD-010`/
`BUILD-011` (`Engine01` sigue leyendo `context.variables.potencial_
ofensivo` exactamente igual, sin ninguna modificación).

BUILD-019: implementa Variable004 (Solidez Defensiva) con dato real,
siguiendo **exclusivamente** `models/defensive-strength.md` en su versión
vigente tras `MODEL-010` (§6.2, §13-21) -- ninguna fórmula anterior (no se
reutiliza el mecanismo de Variable003 salvo donde `MODEL-010` lo autoriza
explícitamente, ver `_SolidezDefensivaRepository`), ninguna nota del brief,
ninguna interpretación personal. **Alcance de archivo más estricto que
`BUILD-018`:** el brief de esta misión restringe las modificaciones
únicamente a `app/preparation/preparation.py` (más los imports/exports que
resulten necesarios) -- a diferencia de `BUILD-018`, no autoriza crear
"archivos auxiliares". Por eso toda la lectura de datos nueva que Variable004
necesita (`_SolidezDefensivaRepository` y sus tipos auxiliares, todos
privados de este módulo) vive **dentro de este mismo archivo**, en lugar de
en un archivo propio como `potencial_ofensivo_repository.py` -- duplicando
deliberadamente un pequeño fragmento de lectura de CSV ya existente ahí,
documentado como consecuencia directa de esa restricción de alcance, no como
un descuido. No modifica `Engine02`, `EngineRunner`, `PredictionContext` ni
`Persistence`. `VariablePreparation.__init__` gana un tercer colaborador
opcional (`solidez_defensiva_repository`), con valor por defecto -- la firma
`preparar(context)` y los dos parámetros ya existentes no cambian,
preservando compatibilidad total con `BUILD-006`/`009`/`010`/`011`/`018`
(`Engine02` sigue leyendo `context.variables.solidez_defensiva` exactamente
igual, sin ninguna modificación).

BUILD-020: implementa Variable001 (Forma Reciente) con dato real, siguiendo
**exclusivamente** `models/forma-reciente.md` (`MODEL-011`) -- ninguna
fórmula anterior, ninguna interpretación personal. Nota de secuencia: esta
misión se completa después de `BUILD-021` en este repositorio (`MODEL-011`
ya existía, sin implementar, cuando `BUILD-021` se cerró -- ver tabla
"Hallazgo central" más abajo, fila 001) -- el número de misión sigue la
numeración ya asignada en `docs/00-Project-Tracker.md`, no el orden real de
ejecución. A diferencia de Variable002/003/004 (que restringen la ventana a
un torneo o competición específicos), Variable001 no filtra por competición
ni torneo: cuenta los últimos `N=5` partidos oficiales de la selección en
`partidos.csv`, sin importar su torneo (`models/forma-reciente.md` §8: "sin
distinción de amistosos y competiciones" -- ningún join contra `torneos.csv`/
`competiciones.csv` es necesario, a diferencia de Variable002/003/004). El
brief de esta misión restringe las modificaciones únicamente a
`preparation.py` (mismo alcance de archivo que `BUILD-019`) -- por eso
`_FormaRecienteRepository` y sus tipos auxiliares viven dentro de este mismo
módulo, en lugar de un archivo propio o de una extensión de
`CsvPreparationRepository`. `VariablePreparation.__init__` gana un cuarto
colaborador opcional (`forma_reciente_repository`), con valor por defecto --
la firma `preparar(context)` y los tres parámetros ya existentes no cambian,
preservando compatibilidad total con `BUILD-006`/`009`/`010`/`011`/`018`/
`019`/`021` (`Engine01`/`Engine02` siguen leyendo
`context.variables.forma_reciente` exactamente igual, sin ninguna
modificación). Calcula también, como cálculo interno documentado (`models/
forma-reciente.md` §10), `Estabilidad_Forma` (desviación estándar muestral
de los puntos por partido en la misma ventana) -- **no se publica**:
`ValorVariable` solo admite un `float` por variable, ya ocupado por
`Forma_Reciente`; queda como una función privada, invocada y su resultado
descartado, que demuestra que la fórmula de `MODEL-011` §10 es efectivamente
calculable con los datos ya disponibles, sin exponerla a `Engine04`/
`Engine05` -- eso exige una futura misión de gobernanza que decida su
mecanismo de exposición sin modificar `PredictionContext`, explícitamente
fuera de alcance de esta misión.

BUILD-021: implementa Variable002 (Rendimiento en el Torneo) con dato real,
siguiendo **exclusivamente** `models/rendimiento-torneo.md` en su versión
vigente tras `MODEL-012` -- ninguna fórmula anterior, ninguna interpretación
personal. A diferencia de Variable003/004 (que resuelven una *competición*
completa) y de Variable010 (que resuelve un par de selecciones), Variable002
necesita el `id_torneo` **específico** del partido que se está prediciendo
-- primera vez que `context.match.torneo` se usa directamente. El brief
autoriza explícitamente "Uso del `CsvPreparationRepository`" (a diferencia
de `BUILD-019`) -- por eso `resolver_id_torneo`/`partidos_del_torneo` se
agregan a `app/persistence/preparation_repository.py`, no duplicados dentro
de este archivo. `VariablePreparation.__init__` no gana ningún colaborador
nuevo (reutiliza `self._repository`, ya inyectado desde `BUILD-017`) -- la
firma `preparar(context)` y los tres parámetros ya existentes no cambian,
preservando compatibilidad total con `BUILD-006`/`009`/`010`/`011`/`018`/
`019` (`Engine01`/`Engine02` siguen leyendo `context.variables.rendimiento_
torneo` exactamente igual).

BUILD-022: implementa el componente "Profundidad" de Variable008 (Calidad
de Plantilla) con dato real, siguiendo **exclusivamente** `models/
profundidad-plantilla.md` (`MODEL-013`) -- ninguna fórmula anterior, ninguna
interpretación personal. Único componente activo de Variable008 en V1
(alcance ya fijado por `MR-004`/`docs/24`, confirmado por `MODEL-013`):
"Valor de mercado" y "Experiencia" no se implementan, conforme al "No
implementar" explícito del brief de esta misión. Reutiliza el mecanismo de
z-score/Φ de `MODEL-009`/`MODEL-010` (`_aplicar_formula_potencial_ofensivo`/
`_aplicar_formula_solidez_defensiva`), aplicado a un conteo de convocados
por posición en lugar de una métrica de tiro -- agrupación **dinámica**, sin
ninguna lista predeclarada de posiciones (`MODEL-013` §4/§10: ningún
documento del proyecto formaliza el ENUM de `posicion_principal`, y esta
misión no lo inventa; se agrupa por cualquier valor de texto distinto
observado, recortado de espacios, sin ninguna normalización adicional). A
diferencia de Variable003/004 (población = misma competición, misma ventana
de fechas) y de Variable002 (ventana = partidos ya jugados del torneo),
Variable008 no tiene ventana de `N` partidos en absoluto: la convocatoria es
una fotografía única por `id_torneo` (`MODEL-013` §8) -- la población es el
conjunto de selecciones con convocatoria válida al **mismo torneo
específico** del partido a predecir. **Corrección de consistencia interna
del propio `models/profundidad-plantilla.md`, determinada por su Caso
límite "posición exclusiva de un equipo" (sección 11), no una
interpretación nueva de esta misión:** la sección 6 de ese documento
describe la población en términos generales ("cada selección con al menos
una fila válida... incluye a T"), pero su propia tabla de casos límite solo
tiene sentido si la población de una posición `p` se restringe a las
selecciones que **efectivamente registran** esa posición (sin "rellenar con
cero" las que no la tienen) -- de lo contrario, una posición exclusiva de un
equipo nunca tendría población `<2` mientras el torneo tenga 2+ selecciones
en total, contradiciendo esa fila explícita del documento. Esta misión
implementa la única lectura que reconcilia ambas partes del documento
consigo mismo, mismo tipo de corrección de consistencia ya aplicado por
`BUILD-019`/`MODEL-010` a "Porterías en cero". El brief de esta misión
restringe las modificaciones únicamente a `preparation.py` (mismo alcance de
archivo que `BUILD-019`/`BUILD-020`) -- por eso `_ProfundidadPlantilla
Repository` y sus tipos auxiliares viven dentro de este mismo módulo.
`VariablePreparation.__init__` gana un quinto colaborador opcional
(`profundidad_plantilla_repository`), con valor por defecto -- la firma
`preparar(context)` y los cuatro parámetros ya existentes no cambian,
preservando compatibilidad total con `BUILD-006`/`009`/`010`/`011`/`018`/
`019`/`020`/`021` (`Engine01`/`Engine02` siguen leyendo
`context.variables.calidad_plantilla` exactamente igual, sin ninguna
modificación). `MODEL-013` no define un criterio de "muestra reducida" para
esta variable (sin ventana de `N` que comparar) -- `muestra_reducida` queda
siempre `False`, sin inventar un umbral no solicitado por ningún documento.

BUILD-023: implementa Variable007 (Fatiga) en su alcance reducido V1
(Escasez de Descanso + Viajes), siguiendo **exclusivamente** `models/
fatiga.md` (`MODEL-014`) -- ninguna fórmula anterior, ninguna interpretación
personal. "Minutos jugados" no se implementa: `MODEL-014` §11 ya concluyó
que no existe fuente de datos para esa señal (declarado explícitamente no
implementable, no un simple diferimiento de alcance como el de Variable008).
Reutiliza el mecanismo z-score/Φ (`_aplicar_formula_fatiga_descanso`) para
"Escasez de Descanso", invertido (`100·(1−Φ(z))`, misma técnica de inversión
que `_aplicar_formula_solidez_defensiva`) porque más días de descanso
implica menos fatiga; `Días_descanso` se busca sobre **todo** `partidos.csv`
(cualquier torneo/competición, `MODEL-014` §4, mismo criterio que
Variable001/`BUILD-020`), pero la población de comparación (`μ`/`σ`) se
restringe a las selecciones del torneo específico del partido a predecir
(mismo criterio "mismo torneo" que Variable008/`BUILD-022`). Para "Viajes",
no reutiliza z-score/Φ (`MODEL-014` §4/§7: la señal es categórica, no
continua, con solo tres niveles derivables de `estadios.csv.ciudad`/`pais`)
-- usa en su lugar un mapeo ordinal directo (`50·Categoría_Viaje`), sin
calibrar. Ambos sub-índices se combinan por promedio simple, con
degradación a un solo término si falta uno (mismo patrón de
`_aplicar_formula_rendimiento_torneo`/`BUILD-021`). **Alcance de archivo
restringido, mismo criterio que `BUILD-019`/`020`/`022`:** el brief de esta
misión restringe las modificaciones únicamente a `preparation.py` -- por eso
`_FatigaRepository` y sus tipos auxiliares viven dentro de este mismo
módulo, en lugar de extender `CsvPreparationRepository` (que además no
expone `ciudad` de `estadios.csv`, solo `pais`, insuficiente para la señal
de Viajes). `VariablePreparation.__init__` gana un sexto colaborador
opcional (`fatiga_repository`), con valor por defecto -- la firma
`preparar(context)` y los cinco parámetros ya existentes no cambian,
preservando compatibilidad total con `BUILD-006`/`009`/`010`/`011`/`018`/
`019`/`020`/`021`/`022` (`Engine01`/`Engine02`/`Engine04` siguen leyendo
`context.variables.fatiga` exactamente igual, sin ninguna modificación).
`MODEL-014` no define un criterio de "muestra reducida" para esta variable
(sin ventana de `N` que comparar, mismo caso que Variable008) --
`muestra_reducida` queda siempre `False`, sin inventar un umbral no
solicitado.

BUILD-024: implementa Variable006 (Disponibilidad de Plantilla) en su
alcance reducido V1 (solo "Lesiones"), siguiendo **exclusivamente** `models/
disponibilidad.md` (`MODEL-015`) -- ninguna fórmula anterior, ninguna
interpretación personal. "Suspensiones"/"Rotaciones" no se implementan:
`MODEL-015` §10 ya concluyó que ninguna tiene fuente de datos suficiente hoy
(ENUM de `estado_convocatoria` sin formalizar; sin tabla de alineación por
partido) -- declarado explícitamente no implementable, no un simple
diferimiento de alcance. A diferencia de Variable003/004/007-Descanso/008,
no usa z-score ni Φ: `Disponibilidad_Plantilla = 100·(|Convocados| −
Lesionados_activos)/|Convocados|` es un cociente directo de conteos, ya
acotado `[0,100]` por construcción aritmética (`MODEL-015` §4). Una lesión
cubre la fecha del partido a predecir si `fecha_inicio ≤ context.match.
fecha` y (`fecha_retorno_real`, o si no existe `fecha_estimada_retorno`, o
si ninguna existe se trata como activa indefinidamente, `MODEL-015` §6) es
`≥ context.match.fecha` -- nunca se usa `lesiones.csv.estado` (`MODEL-015`
§4: `TEXT CHECK ENUM` sin valores formalizados en ningún documento, mismo
vacío de gobernanza ya detectado por `MODEL-013`/`BUILD-022` para
`posicion_principal`). La convocatoria se resuelve al torneo específico del
partido a predecir, mismo criterio "mismo torneo" que Variable008/
`BUILD-022`. Ni `jugadores.csv` ni `partidos.csv` son necesarios para esta
señal (`MODEL-015` §4) -- a diferencia de `BUILD-022` (necesita
`jugadores.csv`) y de `BUILD-023` (necesita `partidos.csv`). **Alcance de
archivo restringido, mismo criterio que `BUILD-019`/`020`/`022`/`023`:** el
brief de esta misión restringe las modificaciones únicamente a
`preparation.py` -- por eso `_DisponibilidadRepository` y sus tipos
auxiliares viven dentro de este mismo módulo. `VariablePreparation.__init__`
gana un séptimo colaborador opcional (`disponibilidad_repository`), con
valor por defecto -- la firma `preparar(context)` y los seis parámetros ya
existentes no cambian, preservando compatibilidad total con `BUILD-006`/
`009`/`010`/`011`/`018`/`019`/`020`/`021`/`022`/`023` (`Engine01`/`Engine02`/
`Engine04`/`Engine05` siguen leyendo `context.variables.disponibilidad_
plantilla` exactamente igual, sin ninguna modificación). `MODEL-015` no
define un criterio de "muestra reducida" para esta variable (sin ventana de
`N` que comparar, mismo caso que Variable007/008) -- `muestra_reducida`
queda siempre `False`, sin inventar un umbral no solicitado.

## Fórmula implementada (cita literal de `models/forma-reciente.md` §6)

```
Para cada uno de los últimos N=5 partidos oficiales del equipo:
    puntos_j = 3   si ganó   |   1   si empató   |   0   si perdió

n = número de partidos válidos encontrados (n ≤ N)
Forma_Reciente = 100 · (Σⱼ puntos_j) / (3 · n)
```

Sin ningún join contra `torneos.csv`/`competiciones.csv`: la ventana no se
restringe a una competición específica (§8, "sin distinción de amistosos y
competiciones") -- cualquier fila de `partidos.csv` donde el equipo participe,
con goles y fecha válidos, cuenta igual. Ningún peso libre: proporción
directa, ya acotada `[0,100]` por construcción aritmética (§9), sin `Φ` ni
normalización estadística. Si `n = 0` (cero partidos oficiales válidos),
Variable001 se marca `disponible=False` -- nunca un valor inventado.

Cálculo interno adicional, no publicado (§10): `Estabilidad_Forma` =
desviación estándar muestral de `{puntos_1, ..., puntos_n}`, indefinida
(`None`) si `n < 2` -- se calcula (`_calcular_estabilidad_forma`) para dejar
evidencia de que la fórmula candidata a `Δ_forma`/`C_forma` es efectivamente
computable, pero su resultado se descarta: no existe campo en `ValorVariable`
para publicarla, y exponerla a `Engine04`/`Engine05` requiere una misión de
gobernanza aparte (fuera de alcance de `BUILD-020`).

## Fórmula implementada (cita literal de `models/offensive-strength.md` §21)

```
Para cada métrica i ∈ {xG, disparos_totales, disparos_al_arco}:
    z_i = (x̄_i(equipo) − μ_i(competición)) / σ_i(competición)
Z = Σ vᵢ · zᵢ                      (vᵢ = 1/3 cada una, §21)
P = 100 · Φ(Z / s)                  (s = √(Σvᵢ²) = √(1/3), §21)
```

`x̄_i(equipo)` se calcula sobre los últimos `N = 10` partidos oficiales del
equipo (§22); `μ_i`/`σ_i(competición)` sobre la población de todos los
equipos de la misma competición dentro del mismo rango de fechas que esos
`N` partidos (§22, "misma ventana temporal... para que la comparación sea
contemporánea"). Si una métrica tiene `σ` indefinida o igual a 0, se excluye
del cálculo de `Z` sin renormalizar los pesos restantes -- mismo tratamiento
que una variable opcional ausente en la sección 6.2 de este documento,
citado explícitamente por la sección 24 de la especificación. Si las tres
métricas quedan excluidas, o el equipo no tiene ningún partido válido,
Variable003 se marca `disponible=False` -- nunca un valor inventado.

## Fórmula implementada (cita literal de `models/defensive-strength.md` §15)

```
Para cada métrica i ∈ {xGA, goles_recibidos, remates_permitidos, tasa_sin_porteria_en_cero}:
    z_i = (x̄_i(equipo) − μ_i(competición)) / σ_i(competición)
Z_def = Σ vᵢ' · zᵢ                              (vᵢ' = 1/4 cada una, §15)
P_def = 100 · (1 − Φ(Z_def / s_def))            (s_def = √(Σvᵢ'²) = √(1/4) = 0.5, §15)
```

Mismo mecanismo de ventana/población que Variable003 (`x̄_i(equipo)` sobre
los últimos `N = 10` partidos -- **reutilizado explícitamente**, no una
decisión de esta misión: `models/defensive-strength.md` §16 autoriza
literalmente "la misma ventana de N partidos" que Variable003; `μ_i`/`σ_i
(competición)` sobre la misma población en el mismo rango de fechas). La
cuarta métrica (`tasa_sin_porteria_en_cero`) sustituye a "porterías en cero"
-- corrección de consistencia de signo ya fijada por `MODEL-010` §15, no una
interpretación de esta misión: una fila de `partidos.csv` con al menos un
gol recibido por el equipo cuenta como `1.0` para esta métrica, `0.0` en
caso contrario, de modo que las 4 métricas apuntan uniformemente en la
dirección "más alto = peor defensa" antes de construir `Z_def`. Si una
métrica tiene `σ` indefinida o igual a 0, se excluye sin renormalizar --
idéntico a Variable003. Si las 4 quedan excluidas, o el equipo no tiene
ningún partido válido, Variable004 se marca `disponible=False`.

## Fórmula implementada (cita literal de `models/rendimiento-torneo.md` §6)

```
Puntos_torneo = Σⱼ puntos_j                                      (puntos_j ∈ {0,1,3}, sistema estándar)
Goles_favor   = Σⱼ goles_a_favor_j
Goles_contra  = Σⱼ goles_en_contra_j

Puntos_pct = 100 · Puntos_torneo / (3 · n)                        (definido si n ≥ 1)
Gol_pct    = 100 · Goles_favor / (Goles_favor + Goles_contra)     (definido si Goles_favor+Goles_contra ≥ 1)

Rendimiento_Torneo = (Puntos_pct + Gol_pct) / 2   si ambos están definidos
Rendimiento_Torneo = Puntos_pct                    si solo Puntos_pct está definido
```

`j` recorre los partidos que el equipo **ya jugó** dentro del `id_torneo`
**específico** del partido que se está prediciendo -- nunca la competición
completa (a diferencia de Variable003/004), y nunca partidos futuros o el
propio partido a predecir: se filtra a `fecha < context.match.fecha`, con
exclusión adicional por `id_partido` como salvaguarda (`models/rendimiento-
torneo.md` §2/§8: "todos los partidos ya jugados... dentro del `id_torneo`
específico"). Sin ventana `N` fija -- la propia definición del torneo acota
el conjunto. Ningún peso libre: ambos sub-índices ya están acotados
`[0,100]` por construcción: aritmética directa, no `Φ`. Si `n = 0` (debut
absoluto en el torneo) o ambos sub-índices son indefinidos, Variable002 se
marca `disponible=False` -- excepción ya documentada en `docs/17` (no
detiene el pipeline, `Engine01`/`Engine02` ya tratan Variable001/002 como
opcionales en su propio código, `BUILD-009`/`BUILD-011`).

## Fórmula implementada (cita literal de `models/profundidad-plantilla.md` §6)

```
P(T) = posiciones distintas observadas en la convocatoria del equipo al
       id_torneo específico del partido a predecir (jugadores.csv.
       posicion_principal, vía join con convocatorias.csv)

Para cada posición p ∈ P(T):
    conteo(T, p) = número de convocados de T en la posición p

    Población de p = conteo(T', p) para cada selección T' del mismo torneo
    que también registra al menos un convocado en la posición p (incluye a
    T; ver "Corrección de consistencia interna" en BUILD-022 más arriba)

    Si la población de p tiene menos de 2 selecciones, o σ_p = 0:
        p se excluye del cálculo de Z, sin renormalizar (§11)
    si no:
        z_p = (conteo(T, p) − μ_p) / σ_p

k = número de posiciones no excluidas
Z = Σ (1/k) · z_p                 (peso igualitario, símbolo propio, §6)
s = √(1/k)                        (derivado matemáticamente de los pesos)

Profundidad_Plantilla = 100 · Φ(Z / s)
```

Sin ventana de `N` partidos (§8: la convocatoria es una fotografía única por
torneo). Ningún umbral absoluto de "cuántos convocados por posición
bastan" -- toda la fórmula es relativa a la población del propio torneo,
mismo principio que Variable003/004 (`MODEL-009`/`MODEL-010`). Fila de
`convocatorias.csv` sin `id_jugador` resoluble en `jugadores.csv`, o con
`posicion_principal` vacía, se descarta individualmente (§11) -- nunca
invalida el resto de la convocatoria. Si `k = 0` (todas las posiciones
excluidas) o la selección no tiene ningún convocado clasificable, Variable008
(componente Profundidad) se marca `disponible=False` -- nunca un valor
inventado.

## Fórmula implementada (cita literal de `models/fatiga.md` §6-8)

```
Sea F = context.match.fecha, Tor = context.match.torneo, T el equipo evaluado

Partido_anterior(X) = partido finalizado más reciente de X con fecha < F,
    sobre TODO partidos.csv, sin filtrar por id_torneo (§4)
Días_descanso(X)     = F − fecha(Partido_anterior(X))

Población(Tor) = selecciones con al menos una fila en partidos.csv del
    mismo id_torneo del partido a predecir (incluye a T)

z = (Días_descanso(T) − μ) / σ           (μ, σ sobre Población(Tor) con
                                           Partido_anterior resoluble)
Fatiga_Descanso = 100 · (1 − Φ(z))        (§6 -- invertido: más descanso = menos fatiga)

Categoría_Viaje ∈ {0, 1, 2}               (misma ciudad / mismo país / distinto país,
                                           entre el estadio de Partido_anterior(T)
                                           y context.match.estadio, vía estadios.csv)
Fatiga_Viaje = 50 · Categoría_Viaje        (§7)

Fatiga = (Fatiga_Descanso + Fatiga_Viaje) / 2     si ambas señales disponibles
Fatiga = el término único disponible              si solo una lo está        (§8)
```

Sin ventana de `N` partidos (§10: ambas señales son comparaciones puntuales
contra el partido inmediatamente anterior, no un promedio móvil). Si
`Población(Tor)` tiene menos de 2 selecciones con `Partido_anterior`
resoluble, o `σ = 0`, se excluye `Fatiga_Descanso` (§13). Si `context.match.
estadio` no está asignado, o el estadio de `Partido_anterior(T)` no resuelve
en `estadios.csv`, se excluye `Fatiga_Viaje` (§13). Si `T` no tiene ningún
partido anterior (debut absoluto), o ambas señales quedan excluidas,
Variable007 se marca `disponible=False` -- nunca un valor inventado.
"Minutos jugados" no se implementa -- `MODEL-014` §11 concluye que no existe
fuente de datos para esa señal en el esquema actual.

## Fórmula implementada (cita literal de `models/disponibilidad.md` §6)

```
Sea Tor = context.match.torneo, F = context.match.fecha, T el equipo evaluado

Convocados(T, Tor) = { id_jugador distintos de T en convocatorias.csv
                        para el id_torneo específico del partido a predecir }

Para cada lesión L de un jugador de Convocados(T, Tor):
    fecha_fin_efectiva(L) = fecha_retorno_real(L)          si está presente
                           = fecha_estimada_retorno(L)      si no, y esta sí
                           = indefinida (sin cota)           si ninguna existe

    L cubre F  ⟺  fecha_inicio(L) ≤ F  Y  (fecha_fin_efectiva(L) indefinida
                                            O  F ≤ fecha_fin_efectiva(L))

Lesionados_activos(T, Tor, F) = |{ j ∈ Convocados(T, Tor) :
    al menos una lesión de j cubre F }|

Disponibilidad_Plantilla = 100 · (|Convocados| − Lesionados_activos) / |Convocados|
```

Definida solo si `|Convocados(T, Tor)| > 0` (§11). Sin z-score, sin `Φ`,
sin ningún peso -- cociente directo de conteos, ya acotado `[0,100]` por
construcción aritmética (§9). Nunca se usa `lesiones.csv.estado` (§4: `TEXT
CHECK ENUM` sin valores formalizados en ningún documento del proyecto). Una
lesión sin ninguna fecha de retorno se trata como activa indefinidamente
desde `fecha_inicio` -- nunca se asume una recuperación no registrada (§6).
Si `Convocados(T, Tor)` está vacío, o el torneo no se reconoce, Variable006
se marca `disponible=False` -- nunca un valor inventado. "Suspensiones" y
"Rotaciones" no se implementan -- `MODEL-015` §10 concluye que ninguna
tiene fuente de datos suficiente con el esquema actual.

## Manejo de errores (más estricto que `BUILD-016`/`BUILD-017`)

El brief de esta misión exige explícitamente que ningún fallo al calcular
Variable002/Variable003/Variable004 detenga `VariablePreparation` por
completo -- a diferencia de `CsvPreparationRepository`/`HistoricalMuGol
Provider`, cuyas excepciones (`DatosBaseConocimientoInconsistentes`/
`DatosHistoricosInconsistentes`) estaban pensadas para propagarse hasta
`EngineRunner`. Aquí, cualquier excepción -- incluida `DatosBaseConocimiento
Inconsistentes`/`DatosPotencialOfensivoInconsistentes`/`_DatosSolidezDefensi
vaInconsistentes`/`_DatosProfundidadPlantillaInconsistentes`/
`_DatosFatigaInconsistentes`/`_DatosDisponibilidadInconsistentes` -- se
captura dentro de `_calcular_rendimiento_torneo`/`_calcular_potencial_
ofensivo`/`_calcular_solidez_defensiva`/`_calcular_profundidad_plantilla`/
`_calcular_fatiga`/`_calcular_disponibilidad`, se registra como `ErrorEntry`
en `context.errors` (`docs/30` §4.8) y se traduce en `disponible=False` para
esa variable únicamente; el resto de `VariablePreparation` continúa sin
alteración.

## Hallazgo central de BUILD-017 -- reportado y resuelto por decisión
## explícita del usuario (no unilateralmente); estado actualizado por
## BUILD-018, BUILD-019, BUILD-021, BUILD-023 y BUILD-024

Antes de escribir código (BUILD-017) se verificó, variable por variable, si
existe una fórmula ya investigada y documentada (no inventada aquí) para
transformar datos crudos en el valor 0-100 (o entero con signo, Variable010)
de cada Variable Oficial activa. Resultado (estado original, BUILD-017):

| Variable | Método autorizado | Bloqueo (BUILD-017) | Estado tras BUILD-018/019/021 |
|---|---|---|---|
| 001 (Forma Reciente) | `docs/03`: "Método: Pendiente de definir en Algoritmo.md"; `docs/04-Algoritmo.md`: "La metodología exacta se documentará posteriormente" | Sin método -- ningún documento de `models/` lo cubre | **`MODEL-011` fijó la fórmula (sin pesos libres) -- `BUILD-020` la implementa. Ver "Fórmula implementada" arriba** |
| 002 (Rendimiento en el Torneo) | `docs/03`: "Método: Pendiente" | Igual | **`MODEL-012` fijó la fórmula (sin pesos libres) -- `BUILD-021` la implementa. Ver "Fórmula implementada" arriba** |
| 003 (Potencial Ofensivo) | `models/offensive-strength.md` §6.1 define `P = 100·Φ(Z/s)`, pero `Z = Σvᵢ·zᵢ` exige pesos `vᵢ`/`s` explícitamente sin calibrar ("Nunca alterar pesos sin evidencia estadística", `CLAUDE.md`) | Método existe, calibración fuera de alcance de `BUILD-017` | **`MODEL-009` fijó pesos placeholder justificados (§17-27) -- `BUILD-018` los implementa. Ver "Fórmula implementada" arriba** |
| 004 (Solidez Defensiva) | Mismo patrón (`models/defensive-strength.md`) | Igual | **`MODEL-010` fijó pesos placeholder justificados (§13-21) -- `BUILD-019` los implementa. Ver "Fórmula implementada" arriba** |
| 006 (Disponibilidad de Plantilla) | `docs/03`: "Método: Pendiente" | Sin método | **`MODEL-015` fijó la fórmula del alcance reducido (solo "Lesiones", sin ningún peso ni z-score) -- `BUILD-024` la implementa. Ver "Fórmula implementada" arriba. "Suspensiones"/"Rotaciones" siguen sin método -- declaradas explícitamente no implementables con el esquema actual (`MODEL-015` §10)** |
| 007 (Fatiga) | `docs/03`: "Método: Pendiente" | Sin método | **`MODEL-014` fijó la fórmula del alcance reducido (Escasez de Descanso + Viajes, sin pesos libres salvo el mapeo ordinal de Viajes) -- `BUILD-023` la implementa. Ver "Fórmula implementada" arriba. "Minutos jugados" sigue sin método -- declarado explícitamente no implementable con el esquema actual (`MODEL-014` §11)** |
| 008 (Calidad de Plantilla) | `docs/03`/MR-004: "derivable de convocatorias.csv+jugadores.csv", sin fórmula de qué es "profundidad" numéricamente | Sin método | **`MODEL-013` fijó la fórmula del componente "Profundidad" (sin pesos libres) -- `BUILD-022` la implementa. Ver "Fórmula implementada" arriba. "Valor de mercado"/"Experiencia" siguen sin método (fuera de alcance, `MR-004`)** |
| 009 (Localía) | Derivable sin inventar nada (comparar país del estadio contra país de cada selección) -- **pero** `ValorVariable.valor` (`app/runtime/prediction_context.py`) está tipado `float \\| None`, incompatible con el ENUM de texto que exige Variable009 (`docs/16`: "Condición: local/visitante/neutral") | Bloqueo de esquema, no de método ni de dato -- mismo "Hallazgo #3" ya documentado sin resolver desde `BUILD-012` (`engine03.py`) | Sin cambios -- seguiría exigiendo modificar `PredictionContext`, fuera de alcance de `BUILD-018`/`019`/`021`/`022` (`GR-010`/`docs/36` recomienda una futura `BUILD-` dedicada) |
| 010 (Historial Directo) | `docs/16`: "diferencia neta de victorias" -- conteo directo, sin pesos, valor numérico con signo (compatible con `float \\| None`) | Sin bloqueo -- implementado en `BUILD-017` | Sin cambios |

**Con `BUILD-024`, las 8 Variables Oficiales activas con método derivable
tienen cálculo real (Variable001, 002, 003, 004, 006-alcance reducido,
007-alcance reducido, 008-Profundidad) además de Variable010 -- 8 de 9.**
Solo queda 009 (bloqueo de esquema, no de método ni de dato). Variable006
completa (con "Suspensiones"/"Rotaciones") y Variable007 completa (con
"Minutos jugados") no quedan pendientes por falta de investigación, sino
declaradas explícitamente no implementables con el esquema de datos actual
(`MODEL-015` §10, `MODEL-014` §11).

**Decisión explícita del usuario (BUILD-017):** implementar únicamente lo que
tiene método autorizado y es compatible con el esquema ya existente; las
demás permanecen `disponible=False`, cada una con la razón exacta
documentada en el código (`_pendiente_por_equipo`/`_pendiente`, con
comentario por variable) -- nunca inventar una fórmula ni un valor, conforme
a `CLAUDE.md` ("Investigación antes de implementación", "Nunca inventes
información") y la Constitución (Art. 2, "No autoaprobación"). `BUILD-018`/
`BUILD-019`/`BUILD-021`/`BUILD-020`/`BUILD-022`/`BUILD-023`/`BUILD-024` no
reabren esa decisión -- implementan Variable003/Variable004/Variable002/
Variable001/Variable008 (Profundidad)/Variable007 (alcance reducido)/
Variable006 (alcance reducido) porque, y solo porque, `MODEL-009`/
`MODEL-010`/`MODEL-012`/`MODEL-011`/`MODEL-013`/`MODEL-014`/`MODEL-015` ya
completaron sus especificaciones siguiendo ese mismo criterio.

## Arquitectura -- por qué `CsvPreparationRepository`, no SQLAlchemy directo

El brief prohíbe crear `Engine`/`Session`/conexiones propias -- se inyecta
`PreparationRepositoryProtocol` (ya declarado desde `BUILD-006`, sin
implementación real hasta ahora) y se usa, por defecto,
`CsvPreparationRepository` (`app/persistence/preparation_repository.py`,
BUILD-017), que lee `data/processed/selecciones-nacionales/` directamente
-- nunca `data/raw/`, nunca una `Session` de SQLAlchemy propia. Ver el
docstring de ese módulo para la justificación completa del carácter
transicional (CSV, no PostgreSQL poblado).

## Qué NO hace este módulo

No calcula Fuerza Ofensiva, Fuerza Defensiva, `λ`, probabilidades, Índice de
Caos, Índice de Confianza ni Valor Esperado -- responsabilidad exclusiva de
`app/engine`. No persiste nada. No invoca ningún motor. No consulta APIs
externas. No calibra, no interpola, no imputa datos faltantes -- toda
ausencia se declara explícitamente (`disponible=False`), nunca se sustituye
por un promedio, un valor por defecto ni cero.
"""

from __future__ import annotations

import csv
import math
import statistics
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Protocol

from app.persistence.preparation_repository import (
    CsvPreparationRepository,
    EstadioInfo,
    PartidoTorneo,
    ResultadoHistorico,
    SeleccionInfo,
)
from app.preparation.potencial_ofensivo_repository import (
    CsvPotencialOfensivoRepository,
    MetricasOfensivas,
    PotencialOfensivoRepositoryProtocol,
)
from app.runtime.prediction_context import (
    ErrorEntry,
    PredictionContext,
    ValorVariable,
    VariablesBlock,
    VariablesPorEquipo,
)

# ---------------------------------------------------------------------------
# Parámetros simbólicos -- ver "Hallazgo central" en el docstring del módulo.
# ---------------------------------------------------------------------------

MUESTRA_REDUCIDA_UMBRAL = 5
"""Placeholder documentado (TODO) -- ningún documento fija un mínimo de
partidos de historial directo para considerar la muestra "reducida"
(`ValorVariable.muestra_reducida`, `docs/15` §6). Valor estructural, no
calibrado -- señala, sin pretensión estadística, que menos de 5
enfrentamientos previos es poca evidencia. Requiere calibración real
(`models/parameter-calibration.md` §7).
"""

# -- Variable001 (Forma Reciente) -- constante citada literalmente de
# `models/forma-reciente.md` §8 (MODEL-011). No se elige aquí; esta misión
# (BUILD-020) solo la transcribe a código.

VENTANA_PARTIDOS_FORMA_RECIENTE = 5  # N, §8 -- elegido independientemente de N=10 (Variable003/004)

# -- Variable003 (Potencial Ofensivo) -- constantes citadas literalmente de
# `models/offensive-strength.md` §21-22 (MODEL-009). Ninguna se elige aquí;
# esta misión (BUILD-018) solo las transcribe a código.

VENTANA_PARTIDOS_POTENCIAL_OFENSIVO = 10  # N, §22
PESO_METRICA_POTENCIAL_OFENSIVO = 1 / 3  # vᵢ, §21 -- una por cada una de las 3 métricas
ESCALA_POTENCIAL_OFENSIVO = math.sqrt(3 * PESO_METRICA_POTENCIAL_OFENSIVO**2)  # s = √(Σvᵢ²), §21
_METRICAS_POTENCIAL_OFENSIVO = ("xg", "disparos_totales", "disparos_al_arco")  # §20/§22, exactamente estas 3

# -- Variable004 (Solidez Defensiva) -- constantes citadas literalmente de
# `models/defensive-strength.md` §15-16 (MODEL-010). Ninguna se elige aquí;
# esta misión (BUILD-019) solo las transcribe a código.

VENTANA_PARTIDOS_SOLIDEZ_DEFENSIVA = VENTANA_PARTIDOS_POTENCIAL_OFENSIVO
"""N=10, reutilizado explícitamente de Variable003 -- `models/defensive-
strength.md` §16 autoriza literalmente "la misma ventana de N partidos",
no es una decisión independiente de esta misión (a diferencia de los pesos,
símbolos propios, ver abajo).
"""

PESO_METRICA_SOLIDEZ_DEFENSIVA = 1 / 4  # vᵢ', §15 -- una por cada una de las 4 métricas, símbolos propios
ESCALA_SOLIDEZ_DEFENSIVA = math.sqrt(4 * PESO_METRICA_SOLIDEZ_DEFENSIVA**2)  # s_def = √(Σvᵢ'²) = √(1/4) = 0.5, §15
_METRICAS_SOLIDEZ_DEFENSIVA = ("xga", "goles_recibidos", "remates_permitidos", "concedio_gol")
"""§14/§15 -- "concedio_gol" reemplaza literalmente a "porterías en cero":
corrección de consistencia de signo ya fijada por `MODEL-010` §15 (no una
interpretación de esta misión), necesaria para que las 4 métricas apunten
uniformemente en la dirección "más alto = peor defensa" antes de construir
`Z_def`.
"""

# -- Shrinkage de Variable003/004 -- ecuación oficial aprobada por MODEL-018,
# implementada literalmente por IMP-001. Aplica por igual a Potencial
# Ofensivo y Solidez Defensiva (mismo mecanismo de z-score/Φ en ambas).

K_SHRINKAGE_VARIABLE003_004 = 5
"""`k`, MODEL-018 §11-12 -- constante estructural documentada, **no
calibrada, no configurable** (primera implementación, IMP-001). Representa
el "punto de estabilización": el `N` en el que la evidencia propia del
equipo y la media histórica de la competición pesan exactamente igual
(`w(k)=0.5`). Valor `5` elegido por ser la mitad de `VENTANA_PARTIDOS_
POTENCIAL_OFENSIVO`/`VENTANA_PARTIDOS_SOLIDEZ_DEFENSIVA` (N=10, ventana ya
vigente) -- no una calibración estadística; una futura misión de
calibración podría ajustarlo con más volumen de datos (MODEL-018 §11,
rango sugerido `k∈[5,8]`).
"""


def _peso_shrinkage(n: int, k: float = K_SHRINKAGE_VARIABLE003_004) -> float:
    """`w(N) = N/(N+k)` -- MODEL-018 §12, ecuación oficial (Opción A)."""
    return n / (n + k)


_ARCHIVO_ESTADISTICAS_DEFENSIVAS = "estadisticas_partido.csv"
_ARCHIVO_PARTIDOS_DEFENSIVOS = "partidos.csv"
_ARCHIVO_TORNEOS_DEFENSIVOS = "torneos.csv"
_ARCHIVO_COMPETICIONES_DEFENSIVAS = "competiciones.csv"


class _DatosSolidezDefensivaInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado como ausencia de evidencia. Clase privada de este módulo -- el
    brief de `BUILD-019` restringe las modificaciones únicamente a
    `preparation.py` (a diferencia de `BUILD-018`, que sí autorizaba
    "archivos auxiliares"), así que esta excepción no vive en un módulo
    propio como `DatosPotencialOfensivoInconsistentes`.
    """


@dataclass(frozen=True)
class _MetricaSolidezDefensivaPartido:
    """Una observación equipo-partido, ya en la polaridad "más alto = peor
    desempeño defensivo" (`models/defensive-strength.md` §15).
    """

    fecha: date
    xga: float
    goles_recibidos: float
    remates_permitidos: float
    concedio_gol: float  # 1.0 si el equipo recibió al menos un gol en ese partido, 0.0 en caso contrario


@dataclass(frozen=True)
class _MetricasSolidezDefensiva:
    equipo: list[_MetricaSolidezDefensivaPartido]
    poblacion_competicion: list[_MetricaSolidezDefensivaPartido]


class _SolidezDefensivaRepositoryProtocol(Protocol):
    """Interfaz de lectura -- satisfecha por `_SolidezDefensivaRepository`.
    Privada de este módulo, mismo motivo que `_DatosSolidezDefensivaInconsistentes`.
    """

    def obtener_metricas_defensivas(
        self, id_seleccion: str, competicion: str, n: int
    ) -> _MetricasSolidezDefensiva | None:
        """Debe devolver `None` si la competición no se reconoce, o
        `_MetricasSolidezDefensiva` con `equipo=[]` si la competición existe
        pero el equipo no tiene partidos válidos -- nunca debe inventar un
        partido.
        """
        ...

    def listar_selecciones(self, competicion: str) -> list[str]:
        """IMP-001 (`MODEL-018`): lista de `id_seleccion` con al menos una
        fila real en `estadisticas_partido.csv` dentro de esta competición --
        mismo propósito y mismo criterio que `PotencialOfensivoRepository
        Protocol.listar_selecciones`, para Variable004."""
        ...


class _SolidezDefensivaRepository:
    """Lee `estadisticas_partido.csv`/`partidos.csv`/`torneos.csv`/
    `competiciones.csv` de `data/processed/selecciones-nacionales/` -- nunca
    `data/raw/` -- para construir las 4 métricas de Variable004
    (`models/defensive-strength.md` §14-15, `MODEL-010`).

    A diferencia de `CsvPotencialOfensivoRepository` (`BUILD-018`, vive en su
    propio archivo), esta clase vive **dentro de `preparation.py`**: el
    brief de `BUILD-019` restringe las modificaciones únicamente a este
    archivo. Esto duplica, deliberadamente, un pequeño fragmento de lectura
    de CSV (resolución de competición, parseo de fecha/goles) ya presente en
    `potencial_ofensivo_repository.py` -- documentado aquí como consecuencia
    directa de esa restricción de alcance, no como un descuido de diseño.

    Cada métrica se construye desde la perspectiva del **rival** de cada
    partido -- `xGA`/remates permitidos: *self-join* sobre `id_partido`
    contra la fila del oponente en `estadisticas_partido.csv`; goles
    recibidos: el marcador del oponente en `partidos.csv` -- a diferencia de
    `CsvPotencialOfensivoRepository`, que usa las estadísticas propias del
    equipo.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_metricas_defensivas(
        self, id_seleccion: str, competicion: str, n: int
    ) -> _MetricasSolidezDefensiva | None:
        id_competicion = self._resolver_id_competicion(competicion)
        if id_competicion is None:
            return None

        ids_torneo = self._torneos_de_competicion(id_competicion)
        if not ids_torneo:
            return None

        partidos = self._indice_partidos_validos(ids_torneo)
        if not partidos:
            return _MetricasSolidezDefensiva(equipo=[], poblacion_competicion=[])

        estadisticas = self._indice_estadisticas(set(partidos.keys()))

        equipo_todas: list[_MetricaSolidezDefensivaPartido] = []
        poblacion_todas: list[_MetricaSolidezDefensivaPartido] = []

        for id_partido, (fecha, id_local, id_visitante, goles_local, goles_visitante) in partidos.items():
            for id_equipo, id_rival, goles_recibidos_valor in (
                (id_local, id_visitante, goles_visitante),
                (id_visitante, id_local, goles_local),
            ):
                estadistica_rival = estadisticas.get((id_partido, id_rival))
                if estadistica_rival is None:
                    continue  # estadística incompleta -- se descarta esta observación, no se inventa

                xga, remates_permitidos = estadistica_rival
                metrica = _MetricaSolidezDefensivaPartido(
                    fecha=fecha,
                    xga=xga,
                    goles_recibidos=float(goles_recibidos_valor),
                    remates_permitidos=remates_permitidos,
                    concedio_gol=1.0 if goles_recibidos_valor > 0 else 0.0,
                )

                if id_equipo == id_seleccion:
                    equipo_todas.append(metrica)
                poblacion_todas.append(metrica)

        if not equipo_todas:
            return _MetricasSolidezDefensiva(equipo=[], poblacion_competicion=[])

        equipo_reciente = sorted(equipo_todas, key=lambda m: m.fecha, reverse=True)[:n]
        fecha_min = min(m.fecha for m in equipo_reciente)
        fecha_max = max(m.fecha for m in equipo_reciente)

        # "misma ventana temporal" (models/defensive-strength.md §16, mismo
        # mecanismo ya usado por Variable003, MODEL-009 §22).
        poblacion = [m for m in poblacion_todas if fecha_min <= m.fecha <= fecha_max]

        return _MetricasSolidezDefensiva(equipo=equipo_reciente, poblacion_competicion=poblacion)

    def listar_selecciones(self, competicion: str) -> list[str]:
        id_competicion = self._resolver_id_competicion(competicion)
        if id_competicion is None:
            return []

        ids_torneo = self._torneos_de_competicion(id_competicion)
        if not ids_torneo:
            return []

        partidos = self._indice_partidos_validos(ids_torneo)
        if not partidos:
            return []

        estadisticas = self._indice_estadisticas(set(partidos.keys()))

        selecciones: set[str] = set()
        for id_partido, (_, id_local, id_visitante, _, _) in partidos.items():
            for id_equipo, id_rival in ((id_local, id_visitante), (id_visitante, id_local)):
                if (id_partido, id_rival) in estadisticas:
                    selecciones.add(id_equipo)  # necesita estadística del rival, mismo criterio que obtener_metricas_defensivas

        return sorted(selecciones)

    # -- Resolución de competición (mismo patrón que CsvPotencialOfensivoRepository) --

    def _resolver_id_competicion(self, competicion: str) -> str | None:
        objetivo = competicion.strip().lower()
        for fila in self._leer_csv(_ARCHIVO_COMPETICIONES_DEFENSIVAS):
            try:
                nombre = fila["nombre"]
                id_competicion = fila["id_competicion"]
            except KeyError as exc:
                raise _DatosSolidezDefensivaInconsistentes(
                    f"'{_ARCHIVO_COMPETICIONES_DEFENSIVAS}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_competicion.strip().lower() == objetivo or nombre.strip().lower() == objetivo:
                return id_competicion
        return None

    def _torneos_de_competicion(self, id_competicion: str) -> set[str]:
        ids_torneo: set[str] = set()
        for fila in self._leer_csv(_ARCHIVO_TORNEOS_DEFENSIVOS):
            try:
                if fila["id_competicion"] == id_competicion:
                    ids_torneo.add(fila["id_torneo"])
            except KeyError as exc:
                raise _DatosSolidezDefensivaInconsistentes(
                    f"'{_ARCHIVO_TORNEOS_DEFENSIVOS}' no tiene la columna esperada: {exc}."
                ) from exc
        return ids_torneo

    def _indice_partidos_validos(
        self, ids_torneo: set[str]
    ) -> dict[str, tuple[date, str, str, int, int]]:
        """`id_partido -> (fecha, id_seleccion_local, id_seleccion_visitante,
        goles_local, goles_visitante)`, solo para partidos de `ids_torneo`
        con goles válidos (mismo proxy de "finalizado" ya usado en
        `CsvPotencialOfensivoRepository`) y fecha parseable.
        """
        indice: dict[str, tuple[date, str, str, int, int]] = {}
        for fila in self._leer_csv(_ARCHIVO_PARTIDOS_DEFENSIVOS):
            try:
                id_partido = fila["id_partido"]
                id_torneo = fila["id_torneo"]
                id_local = fila["id_seleccion_local"]
                id_visitante = fila["id_seleccion_visitante"]
                fecha_raw = fila["fecha"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise _DatosSolidezDefensivaInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS_DEFENSIVOS}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_torneo not in ids_torneo:
                continue

            goles = self._parsear_goles(goles_local_raw, goles_visitante_raw)
            if goles is None:
                continue

            fecha = self._parsear_fecha(fecha_raw)
            if fecha is None:
                continue

            indice[id_partido] = (fecha, id_local, id_visitante, goles[0], goles[1])
        return indice

    def _indice_estadisticas(self, ids_partido: set[str]) -> dict[tuple[str, str], tuple[float, float]]:
        """`(id_partido, id_seleccion) -> (xg, disparos_totales)`, restringido
        a los partidos ya validados por `_indice_partidos_validos`.
        """
        indice: dict[tuple[str, str], tuple[float, float]] = {}
        for fila in self._leer_csv(_ARCHIVO_ESTADISTICAS_DEFENSIVAS):
            try:
                id_partido = fila["id_partido"]
                id_seleccion = fila["id_seleccion"]
                xg_raw = fila["xg"]
                disparos_totales_raw = fila["disparos_totales"]
            except KeyError as exc:
                raise _DatosSolidezDefensivaInconsistentes(
                    f"'{_ARCHIVO_ESTADISTICAS_DEFENSIVAS}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_partido not in ids_partido:
                continue

            try:
                xg = float(xg_raw)
                disparos_totales = float(disparos_totales_raw)
            except (TypeError, ValueError):
                continue
            if xg < 0 or disparos_totales < 0:
                continue

            indice[(id_partido, id_seleccion)] = (xg, disparos_totales)
        return indice

    @staticmethod
    def _parsear_goles(goles_local_raw: str, goles_visitante_raw: str) -> tuple[int, int] | None:
        try:
            goles_local = int(goles_local_raw)
            goles_visitante = int(goles_visitante_raw)
        except (TypeError, ValueError):
            return None
        if goles_local < 0 or goles_visitante < 0:
            return None
        return goles_local, goles_visitante

    @staticmethod
    def _parsear_fecha(fecha_raw: object) -> date | None:
        try:
            return date.fromisoformat(str(fecha_raw).strip())
        except (TypeError, ValueError):
            return None

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise _DatosSolidezDefensivaInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc


_ARCHIVO_PARTIDOS_FORMA_RECIENTE = "partidos.csv"


class _DatosFormaRecienteInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado como ausencia de evidencia. Clase privada de este módulo -- mismo
    motivo que `_DatosSolidezDefensivaInconsistentes` (el brief de
    `BUILD-020` restringe las modificaciones únicamente a `preparation.py`,
    mismo alcance que `BUILD-019`).
    """


@dataclass(frozen=True)
class _PartidoFormaReciente:
    """Una observación equipo-partido ya reducida a puntos (`models/forma-
    reciente.md` §6) -- sistema 3-1-0, sin goles ni diferencia de gol
    (explícitamente reservados a Variable002, §4).
    """

    fecha: date
    puntos: float  # 3.0 victoria, 1.0 empate, 0.0 derrota


class _FormaRecienteRepositoryProtocol(Protocol):
    """Interfaz de lectura -- satisfecha por `_FormaRecienteRepository`.
    Privada de este módulo, mismo motivo que `_SolidezDefensivaRepositoryProtocol`.
    """

    def obtener_ultimos_partidos(self, id_seleccion: str, n: int) -> list[_PartidoFormaReciente]:
        """Debe devolver, como máximo, los `n` partidos oficiales más
        recientes del equipo -- cualquier torneo o competición, sin
        distinción (`models/forma-reciente.md` §8) --, ordenados
        cronológicamente ascendente. Lista vacía si el equipo no tiene
        ningún partido válido -- nunca debe inventar uno.
        """
        ...


class _FormaRecienteRepository:
    """Lee `partidos.csv` de `data/processed/selecciones-nacionales/` --
    nunca `data/raw/` -- para construir la ventana de Variable001 (`models/
    forma-reciente.md` §5-8, `MODEL-011`).

    A diferencia de `_SolidezDefensivaRepository`/`CsvPotencialOfensivo
    Repository`, no resuelve ninguna competición ni población de rivales:
    Variable001 no compara al equipo contra nadie (sección 4 de la
    especificación) -- solo necesita sus propios últimos `N` partidos,
    cualquiera sea el torneo. Por eso no lee `torneos.csv` ni
    `competiciones.csv`, a diferencia de los otros tres repositorios de este
    módulo.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_ultimos_partidos(self, id_seleccion: str, n: int) -> list[_PartidoFormaReciente]:
        partidos: list[_PartidoFormaReciente] = []
        for fila in self._leer_csv(_ARCHIVO_PARTIDOS_FORMA_RECIENTE):
            try:
                id_local = fila["id_seleccion_local"]
                id_visitante = fila["id_seleccion_visitante"]
                fecha_raw = fila["fecha"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise _DatosFormaRecienteInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS_FORMA_RECIENTE}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_seleccion not in (id_local, id_visitante):
                continue

            goles = self._parsear_goles(goles_local_raw, goles_visitante_raw)
            if goles is None:
                continue  # fila corrupta -- se descarta, nunca se interpola (§11)

            fecha = self._parsear_fecha(fecha_raw)
            if fecha is None:
                continue  # fila corrupta -- se descarta, nunca se interpola (§11)

            goles_local, goles_visitante = goles
            if id_local == id_seleccion:
                goles_propios, goles_rival = goles_local, goles_visitante
            else:
                goles_propios, goles_rival = goles_visitante, goles_local

            if goles_propios > goles_rival:
                puntos = 3.0
            elif goles_propios == goles_rival:
                puntos = 1.0
            else:
                puntos = 0.0

            partidos.append(_PartidoFormaReciente(fecha=fecha, puntos=puntos))

        recientes = sorted(partidos, key=lambda p: p.fecha, reverse=True)[:n]
        return sorted(recientes, key=lambda p: p.fecha)  # cronológico ascendente, §2

    @staticmethod
    def _parsear_goles(goles_local_raw: str, goles_visitante_raw: str) -> tuple[int, int] | None:
        try:
            goles_local = int(goles_local_raw)
            goles_visitante = int(goles_visitante_raw)
        except (TypeError, ValueError):
            return None
        if goles_local < 0 or goles_visitante < 0:
            return None
        return goles_local, goles_visitante

    @staticmethod
    def _parsear_fecha(fecha_raw: object) -> date | None:
        try:
            return date.fromisoformat(str(fecha_raw).strip())
        except (TypeError, ValueError):
            return None

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise _DatosFormaRecienteInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc


_ARCHIVO_CONVOCATORIAS = "convocatorias.csv"
_ARCHIVO_JUGADORES = "jugadores.csv"


class _DatosProfundidadPlantillaInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado como ausencia de evidencia. Clase privada de este módulo -- mismo
    motivo que `_DatosFormaRecienteInconsistentes` (el brief de `BUILD-022`
    restringe las modificaciones únicamente a `preparation.py`, mismo alcance
    que `BUILD-019`/`BUILD-020`).
    """


class _ProfundidadPlantillaRepositoryProtocol(Protocol):
    """Interfaz de lectura -- satisfecha por `_ProfundidadPlantillaRepository`.
    Privada de este módulo, mismo motivo que `_FormaRecienteRepositoryProtocol`.
    """

    def obtener_conteo_posiciones_torneo(self, id_torneo: str) -> dict[str, dict[str, int]]:
        """`id_seleccion -> {posición: conteo}`, para toda selección con al
        menos un convocado clasificable (jugador resoluble en `jugadores.csv`,
        `posicion_principal` no vacía) en `convocatorias.csv` para ese
        `id_torneo`. Diccionario vacío si no hay ninguna fila válida -- nunca
        debe inventar una selección, posición o conteo. Las posiciones nunca
        provienen de una lista predeclarada (`models/profundidad-plantilla.md`
        §4/§10): son exactamente los valores de texto distintos observados.
        """
        ...


class _ProfundidadPlantillaRepository:
    """Lee `convocatorias.csv`/`jugadores.csv` de `data/processed/
    selecciones-nacionales/` -- nunca `data/raw/` -- para construir el
    conteo de convocados por posición que exige el componente "Profundidad"
    de Variable008 (`models/profundidad-plantilla.md` §5-7, `MODEL-013`).

    A diferencia de `_SolidezDefensivaRepository`/`CsvPotencialOfensivo
    Repository`, no resuelve ninguna competición ni ventana de fechas: la
    convocatoria es una fotografía única por `id_torneo` (§8) -- el propio
    torneo específico del partido a predecir ya acota el conjunto. Nunca
    agrupa manualmente: la clasificación por posición usa exactamente el
    valor de texto de `jugadores.csv.posicion_principal`, recortado de
    espacios, sin ninguna normalización ni mapeo adicional (§4/§10).
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_conteo_posiciones_torneo(self, id_torneo: str) -> dict[str, dict[str, int]]:
        posiciones_por_jugador = self._indice_posiciones_jugador()

        conteos: dict[str, dict[str, int]] = {}
        for fila in self._leer_csv(_ARCHIVO_CONVOCATORIAS):
            try:
                fila_id_torneo = fila["id_torneo"]
                id_seleccion = fila["id_seleccion"]
                id_jugador = fila["id_jugador"]
            except KeyError as exc:
                raise _DatosProfundidadPlantillaInconsistentes(
                    f"'{_ARCHIVO_CONVOCATORIAS}' no tiene la columna esperada: {exc}."
                ) from exc

            if fila_id_torneo != id_torneo:
                continue

            posicion = posiciones_por_jugador.get(id_jugador)
            if posicion is None:
                continue  # jugador no resoluble (FK rota) -- se descarta, §11

            conteo_seleccion = conteos.setdefault(id_seleccion, {})
            conteo_seleccion[posicion] = conteo_seleccion.get(posicion, 0) + 1

        return conteos

    def _indice_posiciones_jugador(self) -> dict[str, str]:
        """`id_jugador -> posicion_principal`, recortada de espacios --
        jugadores con posición vacía o no legible no se incluyen (§11:
        "posición vacía o no parseable" se descarta, nunca se clasifica en un
        grupo inventado).
        """
        indice: dict[str, str] = {}
        for fila in self._leer_csv(_ARCHIVO_JUGADORES):
            try:
                id_jugador = fila["id_jugador"]
                posicion_principal = fila["posicion_principal"]
            except KeyError as exc:
                raise _DatosProfundidadPlantillaInconsistentes(
                    f"'{_ARCHIVO_JUGADORES}' no tiene la columna esperada: {exc}."
                ) from exc

            posicion = posicion_principal.strip() if posicion_principal else ""
            if not posicion:
                continue  # posición vacía -- no clasificable, §11

            indice[id_jugador] = posicion
        return indice

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise _DatosProfundidadPlantillaInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc


_ARCHIVO_PARTIDOS_FATIGA = "partidos.csv"
_ARCHIVO_ESTADIOS_FATIGA = "estadios.csv"


class _DatosFatigaInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado como ausencia de evidencia. Clase privada de este módulo -- mismo
    motivo que `_DatosProfundidadPlantillaInconsistentes` (el brief de
    `BUILD-023` restringe las modificaciones únicamente a `preparation.py`,
    mismo alcance que `BUILD-019`/`020`/`022`).
    """


@dataclass(frozen=True)
class _PartidoAnteriorFatiga:
    """El partido finalizado más reciente de una selección antes de una
    fecha límite, localizado sobre TODO `partidos.csv` -- cualquier torneo o
    competición, nunca restringido al torneo del partido a predecir
    (`models/fatiga.md` §4) -- lo que necesitan ambas señales de Fatiga.
    """

    fecha: date
    id_estadio: str  # cadena vacía si el partido no tiene estadio asignado


@dataclass(frozen=True)
class _MetricasFatiga:
    """`selecciones_torneo`: población de comparación de Escasez de Descanso
    -- toda selección con al menos una fila en `partidos.csv` del `id_torneo`
    específico del partido a predecir (`models/fatiga.md` §6, incluye a T).
    `partido_anterior_por_seleccion`: `id_seleccion -> _PartidoAnteriorFatiga`,
    para toda selección (de cualquier torneo) con un partido anterior
    resoluble -- no solo las del torneo evaluado, para poder reutilizarse
    igual si en el futuro se consulta otro torneo con el mismo caché.
    """

    selecciones_torneo: frozenset[str]
    partido_anterior_por_seleccion: dict[str, _PartidoAnteriorFatiga]


class _FatigaRepositoryProtocol(Protocol):
    """Interfaz de lectura -- satisfecha por `_FatigaRepository`. Privada de
    este módulo, mismo motivo que `_ProfundidadPlantillaRepositoryProtocol`.
    """

    def obtener_metricas_fatiga(self, id_torneo: str, fecha_limite: date) -> _MetricasFatiga:
        """Nunca debe inventar un partido ni una selección -- `frozenset`/
        `dict` vacíos si no hay evidencia.
        """
        ...

    def resolver_ubicacion_estadio(self, identificador: str) -> tuple[str, str] | None:
        """`(ciudad, pais)` -- por `id_estadio` o `nombre` (mismo criterio de
        búsqueda dual que `CsvPreparationRepository.obtener_estadio`). `None`
        si no se encuentra -- nunca inventa un estadio.
        """
        ...


class _FatigaRepository:
    """Lee `partidos.csv`/`estadios.csv` de `data/processed/selecciones-
    nacionales/` -- nunca `data/raw/` -- para construir las dos señales del
    alcance reducido de Variable007 (`models/fatiga.md` §5-7, `MODEL-014`).

    A diferencia de `CsvPreparationRepository.obtener_estadio` (que solo
    expone `pais`, suficiente para Localía), esta clase también necesita
    `ciudad` para clasificar "Viajes" (§7) -- por eso no reutiliza ese
    método, y por eso (junto con la restricción de alcance de archivo de
    `BUILD-023`, igual que `BUILD-019`/`020`/`022`) vive **dentro de
    `preparation.py`**, duplicando deliberadamente un pequeño fragmento de
    lectura de `estadios.csv` ya presente en `app/persistence/preparation_
    repository.py`.

    "Partido anterior" usa el mismo proxy de "finalizado" ya usado en el
    resto de este módulo (goles y fecha parseables) -- nunca compara el
    texto de `estado_partido` directamente, mismo criterio que
    `_SolidezDefensivaRepository`/`_FormaRecienteRepository`/
    `CsvPreparationRepository`.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_metricas_fatiga(self, id_torneo: str, fecha_limite: date) -> _MetricasFatiga:
        selecciones_torneo: set[str] = set()
        mejor_partido: dict[str, _PartidoAnteriorFatiga] = {}

        for fila in self._leer_csv(_ARCHIVO_PARTIDOS_FATIGA):
            try:
                fila_id_torneo = fila["id_torneo"]
                id_local = fila["id_seleccion_local"]
                id_visitante = fila["id_seleccion_visitante"]
                id_estadio_raw = fila["id_estadio"]
                fecha_raw = fila["fecha"]
                goles_local_raw = fila["goles_local"]
                goles_visitante_raw = fila["goles_visitante"]
            except KeyError as exc:
                raise _DatosFatigaInconsistentes(
                    f"'{_ARCHIVO_PARTIDOS_FATIGA}' no tiene la columna esperada: {exc}."
                ) from exc

            # Población de Escasez de Descanso (§6): cualquier fila del
            # torneo específico, sin exigir "finalizado" -- una selección
            # participa en el torneo aunque el partido aún no se haya jugado.
            if fila_id_torneo == id_torneo:
                selecciones_torneo.add(id_local)
                selecciones_torneo.add(id_visitante)

            # "Partido anterior" (§4): sobre TODO partidos.csv, sin filtrar
            # por id_torneo -- solo partidos finalizados (proxy de goles/
            # fecha parseables) estrictamente anteriores a fecha_limite.
            if self._parsear_goles(goles_local_raw, goles_visitante_raw) is None:
                continue
            fecha = self._parsear_fecha(fecha_raw)
            if fecha is None or fecha >= fecha_limite:
                continue

            id_estadio = id_estadio_raw.strip() if id_estadio_raw else ""
            for id_seleccion in (id_local, id_visitante):
                actual = mejor_partido.get(id_seleccion)
                if actual is None or fecha > actual.fecha:
                    mejor_partido[id_seleccion] = _PartidoAnteriorFatiga(fecha=fecha, id_estadio=id_estadio)

        return _MetricasFatiga(
            selecciones_torneo=frozenset(selecciones_torneo),
            partido_anterior_por_seleccion=mejor_partido,
        )

    def resolver_ubicacion_estadio(self, identificador: str) -> tuple[str, str] | None:
        objetivo = identificador.strip().lower()
        for fila in self._leer_csv(_ARCHIVO_ESTADIOS_FATIGA):
            try:
                id_estadio = fila["id_estadio"]
                nombre = fila["nombre"]
                ciudad = fila["ciudad"]
                pais = fila["pais"]
            except KeyError as exc:
                raise _DatosFatigaInconsistentes(
                    f"'{_ARCHIVO_ESTADIOS_FATIGA}' no tiene la columna esperada: {exc}."
                ) from exc
            if id_estadio.strip().lower() == objetivo or nombre.strip().lower() == objetivo:
                return ciudad, pais
        return None

    @staticmethod
    def _parsear_goles(goles_local_raw: str, goles_visitante_raw: str) -> tuple[int, int] | None:
        try:
            goles_local = int(goles_local_raw)
            goles_visitante = int(goles_visitante_raw)
        except (TypeError, ValueError):
            return None
        if goles_local < 0 or goles_visitante < 0:
            return None
        return goles_local, goles_visitante

    @staticmethod
    def _parsear_fecha(fecha_raw: object) -> date | None:
        try:
            return date.fromisoformat(str(fecha_raw).strip())
        except (TypeError, ValueError):
            return None

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise _DatosFatigaInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc


_ARCHIVO_CONVOCATORIAS_DISPONIBILIDAD = "convocatorias.csv"
_ARCHIVO_LESIONES = "lesiones.csv"


class _DatosDisponibilidadInconsistentes(RuntimeError):
    """Los archivos de `data/processed/` no tienen la estructura esperada
    (columna faltante, archivo no legible) -- un fallo real de datos, nunca
    tratado como ausencia de evidencia. Clase privada de este módulo -- mismo
    motivo que `_DatosFatigaInconsistentes` (el brief de `BUILD-024`
    restringe las modificaciones únicamente a `preparation.py`, mismo
    alcance que `BUILD-019`/`020`/`022`/`023`).
    """


@dataclass(frozen=True)
class _VentanaLesion:
    """El rango de fechas en el que una lesión cubre al jugador -- `models/
    disponibilidad.md` §6. `fecha_fin_efectiva=None` significa "sin cota":
    ni `fecha_retorno_real` ni `fecha_estimada_retorno` existen, así que la
    lesión se trata como activa indefinidamente desde `fecha_inicio` --
    nunca se asume una recuperación no registrada.
    """

    fecha_inicio: date
    fecha_fin_efectiva: date | None


@dataclass(frozen=True)
class _MetricasDisponibilidad:
    """`convocados`: jugadores distintos convocados por el equipo evaluado
    al torneo específico del partido a predecir (`convocatorias.csv`).
    `lesiones_por_jugador`: `id_jugador -> [_VentanaLesion, ...]`, ya
    restringido a los convocados de `convocados` -- nunca incluye lesiones
    de jugadores no convocados por este equipo a este torneo.
    """

    convocados: frozenset[str]
    lesiones_por_jugador: dict[str, list[_VentanaLesion]]


class _DisponibilidadRepositoryProtocol(Protocol):
    """Interfaz de lectura -- satisfecha por `_DisponibilidadRepository`.
    Privada de este módulo, mismo motivo que `_FatigaRepositoryProtocol`.
    """

    def obtener_metricas_disponibilidad(self, id_torneo: str, id_seleccion: str) -> _MetricasDisponibilidad:
        """Nunca debe inventar una convocatoria ni una lesión --
        `frozenset`/`dict` vacíos si no hay evidencia.
        """
        ...


class _DisponibilidadRepository:
    """Lee `convocatorias.csv`/`lesiones.csv` de `data/processed/
    selecciones-nacionales/` -- nunca `data/raw/` -- para construir el
    alcance reducido de Variable006 (solo "Lesiones", `models/
    disponibilidad.md` §5-6, `MODEL-015`).

    A diferencia de `_ProfundidadPlantillaRepository` (necesita
    `jugadores.csv` para resolver `posicion_principal`) y de
    `_FatigaRepository` (necesita `partidos.csv`/`estadios.csv`), esta
    clase no necesita ninguno de los dos: `lesiones.csv.id_jugador` ya
    vincula directamente con `convocatorias.csv.id_jugador`, y la fecha del
    partido a predecir ya está disponible en `context.match.fecha`
    (`models/disponibilidad.md` §4). Por la misma restricción de alcance de
    archivo que `BUILD-019`/`020`/`022`/`023`, vive dentro de
    `preparation.py`, en lugar de extender `CsvPreparationRepository`.

    Nunca lee `lesiones.csv.estado` (`TEXT CHECK ENUM` sin valores
    formalizados en ningún documento del proyecto, `models/
    disponibilidad.md` §4) -- la actividad de una lesión se determina
    enteramente por sus tres columnas de fecha.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "selecciones-nacionales"
        )

    def obtener_metricas_disponibilidad(self, id_torneo: str, id_seleccion: str) -> _MetricasDisponibilidad:
        convocados: set[str] = set()
        for fila in self._leer_csv(_ARCHIVO_CONVOCATORIAS_DISPONIBILIDAD):
            try:
                fila_id_torneo = fila["id_torneo"]
                fila_id_seleccion = fila["id_seleccion"]
                id_jugador = fila["id_jugador"]
            except KeyError as exc:
                raise _DatosDisponibilidadInconsistentes(
                    f"'{_ARCHIVO_CONVOCATORIAS_DISPONIBILIDAD}' no tiene la columna esperada: {exc}."
                ) from exc

            if fila_id_torneo == id_torneo and fila_id_seleccion == id_seleccion:
                convocados.add(id_jugador)

        if not convocados:
            return _MetricasDisponibilidad(convocados=frozenset(), lesiones_por_jugador={})

        lesiones_por_jugador: dict[str, list[_VentanaLesion]] = {}
        for fila in self._leer_csv(_ARCHIVO_LESIONES):
            try:
                id_jugador = fila["id_jugador"]
                fecha_inicio_raw = fila["fecha_inicio"]
                fecha_estimada_raw = fila["fecha_estimada_retorno"]
                fecha_real_raw = fila["fecha_retorno_real"]
            except KeyError as exc:
                raise _DatosDisponibilidadInconsistentes(
                    f"'{_ARCHIVO_LESIONES}' no tiene la columna esperada: {exc}."
                ) from exc

            if id_jugador not in convocados:
                continue  # lesión de un jugador no convocado por este equipo a este torneo

            fecha_inicio = self._parsear_fecha(fecha_inicio_raw)
            if fecha_inicio is None:
                continue  # fila corrupta -- se descarta individualmente, §11

            # Precedencia: fecha_retorno_real (dato observado) sobre
            # fecha_estimada_retorno (estimación) -- §6. None si ninguna
            # existe: la lesión se trata como activa sin cota.
            fecha_fin_efectiva = self._parsear_fecha(fecha_real_raw)
            if fecha_fin_efectiva is None:
                fecha_fin_efectiva = self._parsear_fecha(fecha_estimada_raw)

            lesiones_por_jugador.setdefault(id_jugador, []).append(
                _VentanaLesion(fecha_inicio=fecha_inicio, fecha_fin_efectiva=fecha_fin_efectiva)
            )

        return _MetricasDisponibilidad(
            convocados=frozenset(convocados),
            lesiones_por_jugador=lesiones_por_jugador,
        )

    @staticmethod
    def _parsear_fecha(fecha_raw: object) -> date | None:
        try:
            return date.fromisoformat(str(fecha_raw).strip())
        except (TypeError, ValueError):
            return None

    def _leer_csv(self, nombre_archivo: str) -> list[dict[str, str]]:
        ruta = self._data_dir / nombre_archivo
        try:
            with ruta.open(newline="", encoding="utf-8") as archivo:
                return list(csv.DictReader(archivo))
        except OSError as exc:
            raise _DatosDisponibilidadInconsistentes(
                f"No se pudo leer '{ruta}': {exc}. Nunca se sustituye por un valor inventado."
            ) from exc


class PreparationRepositoryProtocol(Protocol):
    """Interfaz de lectura desde la Base de Conocimiento -- satisfecha por
    `CsvPreparationRepository` (`app/persistence/preparation_repository.py`,
    BUILD-017). Reemplaza la interfaz mínima de `BUILD-006`
    (`obtener_datos_partido`, nunca invocada) por los métodos que esta
    implementación realmente necesita. `resolver_id_torneo`/`partidos_del_
    torneo` agregados por `BUILD-021` (Variable002).
    """

    def obtener_seleccion(self, identificador: str) -> SeleccionInfo | None:
        """`id_seleccion` o nombre -- debe devolver `None` si no se
        encuentra, nunca inventar una selección.
        """
        ...

    def obtener_estadio(self, identificador: str) -> EstadioInfo | None:
        """`id_estadio` o nombre -- debe devolver `None` si no se
        encuentra, nunca inventar un estadio.
        """
        ...

    def historial_enfrentamientos(
        self, id_seleccion_a: str, id_seleccion_b: str
    ) -> list[ResultadoHistorico]:
        """Todos los partidos finalizados entre ambas selecciones -- lista
        vacía si no hay historial, nunca un resultado inventado.
        """
        ...

    def resolver_id_torneo(self, torneo: str) -> str | None:
        """`id_torneo` o `edicion` -- debe devolver `None` si no se
        encuentra, nunca inventar un torneo.
        """
        ...

    def partidos_del_torneo(self, id_torneo: str) -> list[PartidoTorneo]:
        """Todos los partidos finalizados de un `id_torneo` específico --
        lista vacía si no hay partidos válidos, nunca uno inventado.
        """
        ...


class VariablePreparation:
    """Implementación de `VariablePreparationProtocol` (`app/runtime/runtime.py`,
    BUILD-005). Construye `context.variables` con las 9 Variables Oficiales
    activas en V1. Variable001 (Forma Reciente, `BUILD-020`), Variable002
    (Rendimiento en el Torneo, `BUILD-021`), Variable003 (Potencial Ofensivo,
    `BUILD-018`), Variable004 (Solidez Defensiva, `BUILD-019`), Variable006
    (Disponibilidad de Plantilla, alcance reducido: solo Lesiones,
    `BUILD-024`), Variable007 (Fatiga, alcance reducido: Escasez de Descanso
    + Viajes, `BUILD-023`), Variable008 (Calidad de Plantilla, componente
    "Profundidad", `BUILD-022`) y Variable010 (Historial Directo,
    `BUILD-017`) se calculan con dato real -- solo Variable009 permanece
    `disponible=False`, por bloqueo de esquema (ver "Hallazgo central",
    docstring del módulo), no de método ni de dato. Nunca calcula fuera de
    lo ya especificado en `models/`, nunca consulta SQL directamente, nunca
    decide suficiencia de datos (esa es responsabilidad del Statistician,
    fuera de esta clase, `docs/15` §1).
    """

    def __init__(
        self,
        repository: PreparationRepositoryProtocol | None = None,
        potencial_ofensivo_repository: PotencialOfensivoRepositoryProtocol | None = None,
        solidez_defensiva_repository: _SolidezDefensivaRepositoryProtocol | None = None,
        forma_reciente_repository: _FormaRecienteRepositoryProtocol | None = None,
        profundidad_plantilla_repository: _ProfundidadPlantillaRepositoryProtocol | None = None,
        fatiga_repository: _FatigaRepositoryProtocol | None = None,
        disponibilidad_repository: _DisponibilidadRepositoryProtocol | None = None,
    ) -> None:
        self._repository = repository or CsvPreparationRepository()
        self._potencial_ofensivo_repository = potencial_ofensivo_repository or CsvPotencialOfensivoRepository()
        self._solidez_defensiva_repository = solidez_defensiva_repository or _SolidezDefensivaRepository()
        self._forma_reciente_repository = forma_reciente_repository or _FormaRecienteRepository()
        self._profundidad_plantilla_repository = (
            profundidad_plantilla_repository or _ProfundidadPlantillaRepository()
        )
        self._fatiga_repository = fatiga_repository or _FatigaRepository()
        self._disponibilidad_repository = disponibilidad_repository or _DisponibilidadRepository()

    def preparar(self, context: PredictionContext) -> None:
        """Agrega el bloque `variables` al `context` (docs/30, sección 4.3).

        Las variables de rendimiento (Variable001-004, 006-008) se preparan
        una vez por equipo (local y visitante, `docs/30` §4.3); Localía
        (Variable009) e Historial Directo (Variable010) son propias del
        enfrentamiento, un único valor por partido.
        """
        match = context.match
        seleccion_local = self._repository.obtener_seleccion(match.seleccion_local)
        seleccion_visitante = self._repository.obtener_seleccion(match.seleccion_visitante)

        context.variables = VariablesBlock(
            forma_reciente=VariablesPorEquipo(
                local=self._calcular_forma_reciente(context, seleccion_local, "local"),
                visitante=self._calcular_forma_reciente(context, seleccion_visitante, "visitante"),
            ),  # Variable001 -- calculado con dato real (models/forma-reciente.md, MODEL-011)
            rendimiento_torneo=VariablesPorEquipo(
                local=self._calcular_rendimiento_torneo(context, seleccion_local, "local"),
                visitante=self._calcular_rendimiento_torneo(context, seleccion_visitante, "visitante"),
            ),  # Variable002 -- calculado con dato real (models/rendimiento-torneo.md, MODEL-012)
            potencial_ofensivo=VariablesPorEquipo(
                local=self._calcular_potencial_ofensivo(context, seleccion_local, "local"),
                visitante=self._calcular_potencial_ofensivo(context, seleccion_visitante, "visitante"),
            ),  # Variable003 -- calculado con dato real (models/offensive-strength.md §17-27, MODEL-009)
            solidez_defensiva=VariablesPorEquipo(
                local=self._calcular_solidez_defensiva(context, seleccion_local, "local"),
                visitante=self._calcular_solidez_defensiva(context, seleccion_visitante, "visitante"),
            ),  # Variable004 -- calculado con dato real (models/defensive-strength.md §13-21, MODEL-010)
            disponibilidad_plantilla=VariablesPorEquipo(
                local=self._calcular_disponibilidad(context, seleccion_local, "local"),
                visitante=self._calcular_disponibilidad(context, seleccion_visitante, "visitante"),
            ),  # Variable006 (alcance reducido: solo Lesiones) -- calculado con dato real (models/disponibilidad.md, MODEL-015)
            fatiga=VariablesPorEquipo(
                local=self._calcular_fatiga(context, seleccion_local, "local"),
                visitante=self._calcular_fatiga(context, seleccion_visitante, "visitante"),
            ),  # Variable007 (alcance reducido: Escasez de Descanso + Viajes) -- calculado con dato real (models/fatiga.md, MODEL-014)
            calidad_plantilla=VariablesPorEquipo(
                local=self._calcular_profundidad_plantilla(context, seleccion_local, "local"),
                visitante=self._calcular_profundidad_plantilla(context, seleccion_visitante, "visitante"),
            ),  # Variable008 (componente Profundidad) -- calculado con dato real (models/profundidad-plantilla.md, MODEL-013)
            localia=self._calcular_localia(context, seleccion_local, seleccion_visitante),  # Variable009 -- FIX-002
            historial_directo=self._calcular_historial_directo(seleccion_local, seleccion_visitante),  # Variable010
        )

    # -- Variable009 (Localía) -- FIX-002, corrige bloqueo de esquema heredado de BUILD-012 --

    def _calcular_localia(
        self,
        context: PredictionContext,
        seleccion_local: SeleccionInfo | None,
        seleccion_visitante: SeleccionInfo | None,
    ) -> ValorVariable:
        """`docs/16`: "Condición: local/visitante/neutral" -- compara el
        país del estadio (`estadios.csv.pais`, ya expuesto por
        `CsvPreparationRepository.obtener_estadio`, documentado desde su
        propia creación como "suficiente para Localía") contra el país de
        cada selección (`selecciones.csv.nombre_pais`). Ninguna fuente
        nueva, ningún dato inventado -- únicamente conecta dos lecturas ya
        existentes que nunca se habían unido por el bloqueo de tipo de
        `ValorVariable.valor` (ya corregido, ver `FIX-002` en
        `app/runtime/prediction_context.py`).

        `disponible=False` (nunca un valor inventado) si falta el estadio
        del partido, si no se encuentra en `estadios.csv`, o si alguna de
        las dos selecciones no se resuelve -- mismo criterio de ausencia de
        evidencia ya usado por el resto de este módulo.
        """
        if not context.match.estadio:
            return self._pendiente()
        estadio = self._repository.obtener_estadio(context.match.estadio)
        if estadio is None:
            return self._pendiente()
        if seleccion_local is None or seleccion_visitante is None:
            return self._pendiente()

        pais_estadio = estadio.pais.strip().lower()
        if pais_estadio == seleccion_local.nombre_pais.strip().lower():
            condicion = "local"
        elif pais_estadio == seleccion_visitante.nombre_pais.strip().lower():
            condicion = "visitante"
        else:
            condicion = "neutral"

        return ValorVariable(valor=condicion, disponible=True)

    # -- Variable001 (Forma Reciente) -- BUILD-020, models/forma-reciente.md --

    def _calcular_forma_reciente(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de `models/
        forma-reciente.md` §6 (única autoridad matemática de esta misión).
        Cualquier fallo se captura aquí mismo -- nunca se deja propagar una
        excepción que detenga el resto de `VariablePreparation` (mismo
        criterio que `BUILD-018`/`BUILD-019`/`BUILD-021`).
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            partidos = self._forma_reciente_repository.obtener_ultimos_partidos(
                seleccion.id_seleccion, VENTANA_PARTIDOS_FORMA_RECIENTE
            )
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener partidos de Forma Reciente",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if not partidos:
            return self._pendiente()  # cero partidos oficiales -- disponible=False (§11), nunca inventado

        # Cálculo interno, no publicado (§10) -- ver docstring del módulo y de
        # `_calcular_estabilidad_forma`: demuestra que la fórmula candidata a
        # Δ_forma/C_forma es computable, sin exponerla a Engine04/Engine05.
        # Resultado descartado intencionalmente -- ValorVariable no tiene
        # dónde publicarlo (ver docstring del módulo, sección BUILD-020).
        self._calcular_estabilidad_forma(partidos)

        resultado = self._aplicar_formula_forma_reciente(partidos)

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Forma Reciente fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            muestra_reducida=len(partidos) < VENTANA_PARTIDOS_FORMA_RECIENTE,
        )

    @staticmethod
    def _aplicar_formula_forma_reciente(partidos: list[_PartidoFormaReciente]) -> float:
        """`models/forma-reciente.md` §6: `Forma_Reciente = 100·(Σ puntos_j)/(3n)`.
        Sin pesos libres -- proporción directa, ya acotada `[0,100]` por
        construcción aritmética (§9). Llamada solo cuando `partidos` no está
        vacío (§11); `n=0` nunca llega a esta función.
        """
        n = len(partidos)
        return 100.0 * sum(partido.puntos for partido in partidos) / (3 * n)

    @staticmethod
    def _calcular_estabilidad_forma(partidos: list[_PartidoFormaReciente]) -> float | None:
        """`models/forma-reciente.md` §10 (`MODEL-011`): desviación estándar
        muestral de los puntos por partido en la misma ventana -- candidata
        directa a `Δ_forma` (`Engine04`)/`C_forma` (`Engine05`), pero sin
        mecanismo de publicación aprobado en `BUILD-020` (`ValorVariable`
        solo admite un `float` por variable, ya ocupado por
        `Forma_Reciente`). Indefinida (`None`) si `n < 2` -- mismo criterio
        que `σ_i(competición)` en `MODEL-009`/`MODEL-010`, nunca se sustituye
        por 0.
        """
        if len(partidos) < 2:
            return None
        return statistics.stdev(partido.puntos for partido in partidos)

    # -- Variable002 (Rendimiento en el Torneo) -- BUILD-021, models/rendimiento-torneo.md --

    def _calcular_rendimiento_torneo(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de
        `models/rendimiento-torneo.md` §6 (única autoridad matemática de
        esta misión). Cualquier fallo se captura aquí mismo -- nunca se deja
        propagar una excepción que detenga el resto de `VariablePreparation`
        (mismo criterio que `BUILD-018`/`BUILD-019`).
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            id_torneo = self._repository.resolver_id_torneo(context.match.torneo)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al resolver el torneo de Rendimiento en el Torneo",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if id_torneo is None:
            return self._pendiente()  # torneo no reconocido -- sin evidencia, no es un error

        try:
            partidos_torneo = self._repository.partidos_del_torneo(id_torneo)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener partidos del torneo",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}), torneo '{id_torneo}': {exc}",
            )
            return self._pendiente()

        # Solo partidos ya jugados -- estrictamente anteriores al partido que
        # se está prediciendo, con exclusión adicional por id_partido como
        # salvaguarda (models/rendimiento-torneo.md §2/§8; nunca se filtra
        # con el propio resultado del partido a predecir, evita fuga de datos).
        partidos_previos = [
            partido
            for partido in partidos_torneo
            if partido.id_partido != context.match.id_partido
            and partido.fecha < context.match.fecha
            and seleccion.id_seleccion in (partido.id_seleccion_local, partido.id_seleccion_visitante)
        ]

        if not partidos_previos:
            return self._pendiente()  # debut absoluto en el torneo -- excepción ya documentada en docs/17

        try:
            resultado = self._aplicar_formula_rendimiento_torneo(partidos_previos, seleccion.id_seleccion)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al calcular Rendimiento en el Torneo",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Rendimiento en el Torneo fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            muestra_reducida=len(partidos_previos) < MUESTRA_REDUCIDA_UMBRAL,
        )

    @staticmethod
    def _aplicar_formula_rendimiento_torneo(partidos_previos: list[PartidoTorneo], id_seleccion: str) -> float:
        """`models/rendimiento-torneo.md` §6: combina `Puntos_pct` (siempre
        definido, ya se validó `n ≥ 1` antes de llamar) con `Gol_pct` (solo
        si hay al menos un gol total en la ventana) -- promedio simple si
        ambos existen, o solo `Puntos_pct` si `Gol_pct` es indefinido. Nunca
        inventa un valor para `Gol_pct`.
        """
        puntos_torneo = 0
        goles_favor = 0
        goles_contra = 0

        for partido in partidos_previos:
            if partido.id_seleccion_local == id_seleccion:
                goles_propios, goles_rival = partido.goles_local, partido.goles_visitante
            else:
                goles_propios, goles_rival = partido.goles_visitante, partido.goles_local

            if goles_propios > goles_rival:
                puntos_torneo += 3
            elif goles_propios == goles_rival:
                puntos_torneo += 1

            goles_favor += goles_propios
            goles_contra += goles_rival

        n = len(partidos_previos)
        puntos_pct = 100.0 * puntos_torneo / (3 * n)

        total_goles = goles_favor + goles_contra
        if total_goles < 1:
            return puntos_pct  # Gol_pct indefinido -- se usa solo Puntos_pct, nunca se inventa

        gol_pct = 100.0 * goles_favor / total_goles
        return (puntos_pct + gol_pct) / 2.0

    # -- Variable003 (Potencial Ofensivo) -- BUILD-018, models/offensive-strength.md §17-27 --

    def _calcular_potencial_ofensivo(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de
        `models/offensive-strength.md` §21 (única autoridad matemática de
        esta misión). Cualquier fallo se captura aquí mismo -- nunca se deja
        propagar una excepción que detenga el resto de `VariablePreparation`
        (brief de `BUILD-018`, sección "Manejo de errores").
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            metricas = self._potencial_ofensivo_repository.obtener_metricas_ofensivas(
                seleccion.id_seleccion, context.match.competicion, VENTANA_PARTIDOS_POTENCIAL_OFENSIVO
            )
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener métricas de Potencial Ofensivo",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if metricas is None or not metricas.equipo:
            return self._pendiente()  # competición no reconocida o sin partidos válidos -- sin evidencia

        try:
            resultado = self._aplicar_formula_potencial_ofensivo(metricas, context.match.competicion)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al calcular Potencial Ofensivo",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if resultado is None:
            return self._pendiente()  # las 3 métricas quedaron excluidas (σ indefinida o 0, §24)

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Potencial Ofensivo fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): P={resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            muestra_reducida=len(metricas.equipo) < VENTANA_PARTIDOS_POTENCIAL_OFENSIVO,
        )

    @staticmethod
    def _z_estandarizado_potencial_ofensivo(metricas: MetricasOfensivas) -> float | None:
        """`models/offensive-strength.md` §21: `Z = Σ vᵢ·zᵢ`, `Z* = Z/s`.
        Una métrica con `σ` indefinida (menos de 2 observaciones en la
        población) o igual a 0 se excluye del cálculo de `Z`, sin
        renormalizar los pesos restantes -- mismo tratamiento que una
        variable opcional ausente en la sección 6.2, citado explícitamente
        por la sección 24. Si las 3 quedan excluidas, devuelve `None`.

        Extraído como paso independiente por IMP-001 (`MODEL-018` §9-10):
        el z-score estandarizado, ya vigente sin cambios, se reutiliza tanto
        para el equipo evaluado como para cada equipo de `_media_z_
        potencial_ofensivo_competicion` -- nunca se toca su fórmula interna.
        """
        z_scores: list[float] = []
        for atributo in _METRICAS_POTENCIAL_OFENSIVO:
            valores_equipo = [getattr(m, atributo) for m in metricas.equipo]
            valores_poblacion = [getattr(m, atributo) for m in metricas.poblacion_competicion]

            if len(valores_poblacion) < 2:
                continue  # σ indefinida -- §24, se excluye esta métrica

            promedio_equipo = statistics.fmean(valores_equipo)
            promedio_competicion = statistics.fmean(valores_poblacion)
            desviacion_competicion = statistics.stdev(valores_poblacion)

            if desviacion_competicion == 0.0:
                continue  # §24, se excluye esta métrica -- nunca se divide por cero

            z_scores.append((promedio_equipo - promedio_competicion) / desviacion_competicion)

        if not z_scores:
            return None

        z = sum(PESO_METRICA_POTENCIAL_OFENSIVO * z_i for z_i in z_scores)
        return z / ESCALA_POTENCIAL_OFENSIVO

    def _media_z_potencial_ofensivo_competicion(self, competicion: str) -> float | None:
        """IMP-001 (`MODEL-018` §9-10): media histórica de `Z*` -- equivalente
        a `Φ⁻¹(P̄_competición/100)` -- calculada sobre todos los equipos con
        estadística real en esta competición (nunca un valor inventado ni
        una constante fija; recalculada a partir de los mismos datos reales
        que ya usa `CsvPotencialOfensivoRepository`). Devuelve `None` si no
        hay ningún equipo con `Z*` calculable -- en ese caso no se aplica
        shrinkage (ver `_aplicar_formula_potencial_ofensivo`), nunca se
        sustituye por un valor supuesto.
        """
        try:
            selecciones = self._potencial_ofensivo_repository.listar_selecciones(competicion)
        except Exception:  # captura amplia intencional -- ver docstring del módulo
            return None

        z_valores: list[float] = []
        for id_seleccion in selecciones:
            try:
                metricas = self._potencial_ofensivo_repository.obtener_metricas_ofensivas(
                    id_seleccion, competicion, VENTANA_PARTIDOS_POTENCIAL_OFENSIVO
                )
            except Exception:  # captura amplia intencional -- ver docstring del módulo
                continue
            if metricas is None or not metricas.equipo:
                continue
            z = self._z_estandarizado_potencial_ofensivo(metricas)
            if z is not None:
                z_valores.append(z)

        if not z_valores:
            return None
        return statistics.fmean(z_valores)

    def _aplicar_formula_potencial_ofensivo(
        self, metricas: MetricasOfensivas, competicion: str
    ) -> float | None:
        """`models/offensive-strength.md` §21, con la etapa de Shrinkage de
        `MODEL-018` insertada por IMP-001 entre el z-score estandarizado y
        `Φ`: `Z*_final = w(N)·Z*_equipo + (1−w(N))·Z*_competición`,
        `w(N)=N/(N+k)` (`K_SHRINKAGE_VARIABLE003_004`). La contracción se
        aplica exclusivamente sobre `Z*` (antes de `Φ`) -- **nunca** sobre el
        percentil `P` ya transformado (`MODEL-018` §9). Si no existe media
        de competición calculable (ningún equipo con `Z*` propio todavía),
        no se aplica shrinkage y se conserva el z-score crudo -- nunca se
        inventa una media.
        """
        z_estrella = self._z_estandarizado_potencial_ofensivo(metricas)
        if z_estrella is None:
            return None

        z_competicion = self._media_z_potencial_ofensivo_competicion(competicion)
        if z_competicion is None:
            z_final = z_estrella
        else:
            w = _peso_shrinkage(len(metricas.equipo))
            z_final = w * z_estrella + (1.0 - w) * z_competicion

        phi = statistics.NormalDist().cdf(z_final)
        return 100.0 * phi

    # -- Variable004 (Solidez Defensiva) -- BUILD-019, models/defensive-strength.md §13-21 --

    def _calcular_solidez_defensiva(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de
        `models/defensive-strength.md` §15 (única autoridad matemática de
        esta misión) -- ninguna fórmula anterior, ninguna reinterpretación.
        Cualquier fallo se captura aquí mismo -- nunca se deja propagar una
        excepción que detenga el resto de `VariablePreparation` (brief de
        `BUILD-019`, restricción explícita, mismo criterio que `BUILD-018`).
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            metricas = self._solidez_defensiva_repository.obtener_metricas_defensivas(
                seleccion.id_seleccion, context.match.competicion, VENTANA_PARTIDOS_SOLIDEZ_DEFENSIVA
            )
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener métricas de Solidez Defensiva",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if metricas is None or not metricas.equipo:
            return self._pendiente()  # competición no reconocida o sin partidos válidos -- sin evidencia

        try:
            resultado = self._aplicar_formula_solidez_defensiva(metricas, context.match.competicion)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al calcular Solidez Defensiva",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if resultado is None:
            return self._pendiente()  # las 4 métricas quedaron excluidas (σ indefinida o 0, §18)

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Solidez Defensiva fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): P_def={resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            muestra_reducida=len(metricas.equipo) < VENTANA_PARTIDOS_SOLIDEZ_DEFENSIVA,
        )

    @staticmethod
    def _z_estandarizado_solidez_defensiva(metricas: _MetricasSolidezDefensiva) -> float | None:
        """`models/defensive-strength.md` §15: `Z_def = Σ vᵢ'·zᵢ`,
        `Z_def* = Z_def/s_def`. Una métrica con `σ` indefinida (menos de 2
        observaciones en la población) o igual a 0 se excluye del cálculo de
        `Z_def`, sin renormalizar los pesos restantes -- idéntico al
        tratamiento de Variable003 (`MODEL-009`/`MODEL-010` §18). Si las 4
        quedan excluidas, devuelve `None`.

        Extraído como paso independiente por IMP-001 (`MODEL-018` §9-10),
        mismo motivo que `_z_estandarizado_potencial_ofensivo`: se reutiliza
        tanto para el equipo evaluado como para cada equipo de `_media_z_
        solidez_defensiva_competicion` -- la inversión `1 − Φ(...)` (nótese,
        respecto a Variable003) se aplica **después** de la contracción, no
        aquí (ver `_aplicar_formula_solidez_defensiva`).
        """
        z_scores: list[float] = []
        for atributo in _METRICAS_SOLIDEZ_DEFENSIVA:
            valores_equipo = [getattr(m, atributo) for m in metricas.equipo]
            valores_poblacion = [getattr(m, atributo) for m in metricas.poblacion_competicion]

            if len(valores_poblacion) < 2:
                continue  # σ indefinida -- §18, se excluye esta métrica

            promedio_equipo = statistics.fmean(valores_equipo)
            promedio_competicion = statistics.fmean(valores_poblacion)
            desviacion_competicion = statistics.stdev(valores_poblacion)

            if desviacion_competicion == 0.0:
                continue  # §18, se excluye esta métrica -- nunca se divide por cero

            z_scores.append((promedio_equipo - promedio_competicion) / desviacion_competicion)

        if not z_scores:
            return None

        z_def = sum(PESO_METRICA_SOLIDEZ_DEFENSIVA * z_i for z_i in z_scores)
        return z_def / ESCALA_SOLIDEZ_DEFENSIVA

    def _media_z_solidez_defensiva_competicion(self, competicion: str) -> float | None:
        """IMP-001 (`MODEL-018` §9-10): media histórica de `Z_def*` sobre
        todos los equipos con estadística real en esta competición -- mismo
        criterio y mismo motivo que `_media_z_potencial_ofensivo_competicion`,
        para Variable004. Devuelve `None` si no hay ningún equipo con
        `Z_def*` calculable -- en ese caso no se aplica shrinkage, nunca se
        sustituye por un valor supuesto.
        """
        try:
            selecciones = self._solidez_defensiva_repository.listar_selecciones(competicion)
        except Exception:  # captura amplia intencional -- ver docstring del módulo
            return None

        z_valores: list[float] = []
        for id_seleccion in selecciones:
            try:
                metricas = self._solidez_defensiva_repository.obtener_metricas_defensivas(
                    id_seleccion, competicion, VENTANA_PARTIDOS_SOLIDEZ_DEFENSIVA
                )
            except Exception:  # captura amplia intencional -- ver docstring del módulo
                continue
            if metricas is None or not metricas.equipo:
                continue
            z = self._z_estandarizado_solidez_defensiva(metricas)
            if z is not None:
                z_valores.append(z)

        if not z_valores:
            return None
        return statistics.fmean(z_valores)

    def _aplicar_formula_solidez_defensiva(
        self, metricas: _MetricasSolidezDefensiva, competicion: str
    ) -> float | None:
        """`models/defensive-strength.md` §15, con la etapa de Shrinkage de
        `MODEL-018` insertada por IMP-001 entre el z-score estandarizado y
        `Φ`: `Z_def*_final = w(N)·Z_def*_equipo + (1−w(N))·Z_def*_competición`,
        `w(N)=N/(N+k)` (`K_SHRINKAGE_VARIABLE003_004`, misma constante que
        Variable003). La contracción se aplica sobre `Z_def*` -- **nunca**
        sobre el percentil `P_def` ya transformado (`MODEL-018` §9); la
        inversión `1 − Φ(...)` (`P_def = 100·(1−Φ(Z_def*_final))`), ya
        vigente sin cambios, se aplica al final, después de contraer. Si no
        existe media de competición calculable, no se aplica shrinkage y se
        conserva el z-score crudo -- nunca se inventa una media.
        """
        z_estrella = self._z_estandarizado_solidez_defensiva(metricas)
        if z_estrella is None:
            return None

        z_competicion = self._media_z_solidez_defensiva_competicion(competicion)
        if z_competicion is None:
            z_final = z_estrella
        else:
            w = _peso_shrinkage(len(metricas.equipo))
            z_final = w * z_estrella + (1.0 - w) * z_competicion

        phi = statistics.NormalDist().cdf(z_final)
        return 100.0 * (1.0 - phi)

    # -- Variable008 (Calidad de Plantilla, componente Profundidad) -- BUILD-022, models/profundidad-plantilla.md --

    def _calcular_profundidad_plantilla(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de `models/
        profundidad-plantilla.md` §6 (única autoridad matemática de esta
        misión) -- único componente activo de Variable008 en V1 ("Valor de
        mercado"/"Experiencia" no se implementan, MODEL-013 "No implementar").
        Cualquier fallo se captura aquí mismo -- nunca se deja propagar una
        excepción que detenga el resto de `VariablePreparation` (mismo
        criterio que `BUILD-018`/`019`/`020`/`021`).
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            id_torneo = self._repository.resolver_id_torneo(context.match.torneo)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al resolver el torneo de Profundidad de Plantilla",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if id_torneo is None:
            return self._pendiente()  # torneo no reconocido -- sin evidencia, no es un error

        try:
            conteos_por_seleccion = self._profundidad_plantilla_repository.obtener_conteo_posiciones_torneo(
                id_torneo
            )
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener la convocatoria de Profundidad de Plantilla",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        conteo_equipo = conteos_por_seleccion.get(seleccion.id_seleccion)
        if not conteo_equipo:
            return self._pendiente()  # convocatoria inexistente o sin jugadores clasificables, §11

        try:
            resultado = self._aplicar_formula_profundidad_plantilla(conteo_equipo, conteos_por_seleccion)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al calcular Profundidad de Plantilla",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if resultado is None:
            return self._pendiente()  # todas las posiciones excluidas (σ indefinida o 0, §11)

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Profundidad de Plantilla fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            # MODEL-013 no define un criterio de muestra reducida para esta
            # variable (§8: sin ventana de N que comparar) -- nunca se inventa
            # uno no solicitado por ningún documento.
            muestra_reducida=False,
        )

    @staticmethod
    def _aplicar_formula_profundidad_plantilla(
        conteo_equipo: dict[str, int], conteos_por_seleccion: dict[str, dict[str, int]]
    ) -> float | None:
        """`models/profundidad-plantilla.md` §6: `Z = Σ(1/k)·z_p`,
        `Profundidad_Plantilla = 100·Φ(Z/s)`, `s = √(1/k)`. La población de
        cada posición `p` se restringe a las selecciones que efectivamente
        registran esa posición (nunca se rellena con cero) -- corrección de
        consistencia interna del propio documento, determinada por su Caso
        límite "posición exclusiva de un equipo" (§11), no una interpretación
        nueva de esta misión (ver docstring del módulo, sección BUILD-022).
        Si la población de una posición tiene menos de 2 selecciones, o
        `σ_p = 0`, esa posición se excluye sin renormalizar -- idéntico al
        tratamiento de Variable003/004. Si todas quedan excluidas, `None`.
        """
        z_scores: list[float] = []
        for posicion, conteo_propio in conteo_equipo.items():
            valores_poblacion = [
                conteos[posicion] for conteos in conteos_por_seleccion.values() if posicion in conteos
            ]

            if len(valores_poblacion) < 2:
                continue  # σ indefinida -- §11, se excluye esta posición

            promedio = statistics.fmean(valores_poblacion)
            desviacion = statistics.stdev(valores_poblacion)

            if desviacion == 0.0:
                continue  # §11, se excluye esta posición -- nunca se divide por cero

            z_scores.append((conteo_propio - promedio) / desviacion)

        if not z_scores:
            return None

        k = len(z_scores)
        z = sum((1.0 / k) * z_i for z_i in z_scores)
        s = math.sqrt(1.0 / k)
        phi = statistics.NormalDist().cdf(z / s)
        return 100.0 * phi

    # -- Variable006 (Disponibilidad de Plantilla, alcance reducido) -- BUILD-024, models/disponibilidad.md --

    def _calcular_disponibilidad(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de `models/
        disponibilidad.md` §6 (única autoridad matemática de esta misión) --
        alcance reducido (solo "Lesiones"); "Suspensiones"/"Rotaciones" no se
        implementan (§10: declaradas explícitamente no implementables con el
        esquema actual). Cualquier fallo se captura aquí mismo -- nunca se
        deja propagar una excepción que detenga el resto de
        `VariablePreparation` (mismo criterio que `BUILD-018`/`019`/`020`/
        `022`/`023`).
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            id_torneo = self._repository.resolver_id_torneo(context.match.torneo)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al resolver el torneo de Disponibilidad de Plantilla",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if id_torneo is None:
            return self._pendiente()  # torneo no reconocido -- sin evidencia, no es un error

        try:
            metricas = self._disponibilidad_repository.obtener_metricas_disponibilidad(
                id_torneo, seleccion.id_seleccion
            )
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener métricas de Disponibilidad de Plantilla",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if not metricas.convocados:
            return self._pendiente()  # sin convocatoria válida al torneo -- §11

        try:
            resultado = self._aplicar_formula_disponibilidad(metricas, context.match.fecha)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al calcular Disponibilidad de Plantilla",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if resultado is None:
            return self._pendiente()  # sin convocados -- §11 (salvaguarda, ya validado arriba)

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Disponibilidad de Plantilla fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            # MODEL-015 no define un criterio de muestra reducida para esta
            # variable (sin ventana de N que comparar, mismo caso que
            # Variable007/008) -- nunca se inventa uno no solicitado.
            muestra_reducida=False,
        )

    @staticmethod
    def _aplicar_formula_disponibilidad(
        metricas: _MetricasDisponibilidad, fecha_partido: date
    ) -> float | None:
        """`models/disponibilidad.md` §6: `Disponibilidad_Plantilla =
        100·(|Convocados| − Lesionados_activos)/|Convocados|` -- cociente
        directo de conteos, sin z-score ni `Φ`. Una lesión cubre
        `fecha_partido` si `fecha_inicio ≤ fecha_partido` y (`fecha_fin_
        efectiva` es indefinida, o `fecha_partido ≤ fecha_fin_efectiva`) --
        un jugador con varias lesiones que cubren la fecha cuenta una sola
        vez (`any(...)`, nunca se descuenta dos veces al mismo convocado).
        Devuelve `None` si `metricas.convocados` está vacío (salvaguarda --
        el llamador ya valida esto antes de invocar esta función).
        """
        total_convocados = len(metricas.convocados)
        if total_convocados == 0:
            return None

        lesionados_activos = 0
        for id_jugador in metricas.convocados:
            ventanas = metricas.lesiones_por_jugador.get(id_jugador)
            if not ventanas:
                continue  # sin lesión registrada -- cuenta como disponible, §11
            if any(
                ventana.fecha_inicio <= fecha_partido
                and (ventana.fecha_fin_efectiva is None or fecha_partido <= ventana.fecha_fin_efectiva)
                for ventana in ventanas
            ):
                lesionados_activos += 1

        return 100.0 * (total_convocados - lesionados_activos) / total_convocados

    # -- Variable007 (Fatiga, alcance reducido) -- BUILD-023, models/fatiga.md --

    def _calcular_fatiga(
        self, context: PredictionContext, seleccion: SeleccionInfo | None, lado: str
    ) -> ValorVariable:
        """Implementa, literalmente y sin ampliar, la fórmula de `models/
        fatiga.md` §6-8 (única autoridad matemática de esta misión) --
        alcance reducido (Escasez de Descanso + Viajes); "Minutos jugados"
        no se implementa (§11: declarado explícitamente no implementable con
        el esquema actual). Cualquier fallo se captura aquí mismo -- nunca se
        deja propagar una excepción que detenga el resto de
        `VariablePreparation` (mismo criterio que `BUILD-018`/`019`/`020`/`022`).
        """
        if seleccion is None:
            return self._pendiente()  # selección no resuelta -- sin evidencia, no es un error

        try:
            id_torneo = self._repository.resolver_id_torneo(context.match.torneo)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al resolver el torneo de Fatiga",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        if id_torneo is None:
            return self._pendiente()  # torneo no reconocido -- sin evidencia, no es un error

        try:
            metricas = self._fatiga_repository.obtener_metricas_fatiga(id_torneo, context.match.fecha)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al obtener métricas de Fatiga",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            return self._pendiente()

        partido_anterior = metricas.partido_anterior_por_seleccion.get(seleccion.id_seleccion)
        if partido_anterior is None:
            return self._pendiente()  # sin partido oficial anterior -- debut absoluto, §13

        try:
            dias_descanso = (context.match.fecha - partido_anterior.fecha).days
            fatiga_descanso = self._aplicar_formula_fatiga_descanso(dias_descanso, context.match.fecha, metricas)
        except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
            self._registrar_error_preparacion(
                context,
                evento="Fallo al calcular Fatiga por descanso",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
            )
            fatiga_descanso = None

        fatiga_viaje = None
        if partido_anterior.id_estadio and context.match.estadio:
            try:
                ubicacion_anterior = self._fatiga_repository.resolver_ubicacion_estadio(partido_anterior.id_estadio)
                ubicacion_destino = self._fatiga_repository.resolver_ubicacion_estadio(context.match.estadio)
            except Exception as exc:  # captura amplia intencional -- ver docstring del módulo
                self._registrar_error_preparacion(
                    context,
                    evento="Fallo al resolver la ubicación de un estadio para Fatiga",
                    detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {exc}",
                )
                ubicacion_anterior = ubicacion_destino = None

            if ubicacion_anterior is not None and ubicacion_destino is not None:
                fatiga_viaje = self._aplicar_formula_fatiga_viaje(ubicacion_anterior, ubicacion_destino)
            # estadio no asignado o no resoluble en estadios.csv -- Fatiga_Viaje
            # no se calcula, §13; nunca se inventa un estadio ni una distancia.

        if fatiga_descanso is None and fatiga_viaje is None:
            return self._pendiente()  # ninguna señal disponible, §13

        if fatiga_descanso is not None and fatiga_viaje is not None:
            resultado = (fatiga_descanso + fatiga_viaje) / 2.0
        elif fatiga_descanso is not None:
            resultado = fatiga_descanso
        else:
            resultado = fatiga_viaje

        if not isinstance(resultado, float) or not (0.0 <= resultado <= 100.0):
            self._registrar_error_preparacion(
                context,
                evento="Fatiga fuera de rango",
                detalle=f"Selección '{seleccion.id_seleccion}' ({lado}): {resultado!r} (esperado [0,100])",
            )
            return self._pendiente()

        return ValorVariable(
            valor=resultado,
            disponible=True,
            # MODEL-014 no define un criterio de muestra reducida para esta
            # variable (sin ventana de N que comparar, mismo caso que
            # Variable008) -- nunca se inventa uno no solicitado.
            muestra_reducida=False,
        )

    @staticmethod
    def _aplicar_formula_fatiga_descanso(
        dias_descanso_equipo: int, fecha_limite: date, metricas: _MetricasFatiga
    ) -> float | None:
        """`models/fatiga.md` §6: `Fatiga_Descanso = 100·(1−Φ(z))`, invertido
        porque más días de descanso implica menos fatiga (misma técnica de
        inversión que `_aplicar_formula_solidez_defensiva`). La población de
        comparación se restringe a las selecciones del torneo específico del
        partido a predecir (`metricas.selecciones_torneo`, §6). Si esa
        población tiene menos de 2 selecciones con partido anterior
        resoluble, o `σ = 0`, devuelve `None` -- §13, se excluye esta señal.
        """
        poblacion_dias = [
            (fecha_limite - partido.fecha).days
            for id_seleccion, partido in metricas.partido_anterior_por_seleccion.items()
            if id_seleccion in metricas.selecciones_torneo
        ]

        if len(poblacion_dias) < 2:
            return None  # σ indefinida -- §13, se excluye esta señal

        media = statistics.fmean(poblacion_dias)
        desviacion = statistics.stdev(poblacion_dias)
        if desviacion == 0.0:
            return None  # §13, se excluye esta señal -- nunca se divide por cero

        z = (dias_descanso_equipo - media) / desviacion
        phi = statistics.NormalDist().cdf(z)
        return 100.0 * (1.0 - phi)

    @staticmethod
    def _aplicar_formula_fatiga_viaje(
        ubicacion_anterior: tuple[str, str], ubicacion_destino: tuple[str, str]
    ) -> float:
        """`models/fatiga.md` §7: `Fatiga_Viaje = 50·Categoría_Viaje`, con
        `Categoría_Viaje ∈ {0,1,2}` (misma ciudad / mismo país-distinta
        ciudad / distinto país) -- mapeo ordinal sin calibrar, no un z-score
        (la señal es categórica, no continua, §4/§7).
        """
        ciudad_anterior, pais_anterior = ubicacion_anterior
        ciudad_destino, pais_destino = ubicacion_destino

        if ciudad_anterior.strip().lower() == ciudad_destino.strip().lower():
            categoria = 0
        elif pais_anterior.strip().lower() == pais_destino.strip().lower():
            categoria = 1
        else:
            categoria = 2

        return 50.0 * categoria

    # -- Variable010 (Historial Directo) -- BUILD-017 -----------------------

    def _calcular_historial_directo(
        self, seleccion_local: SeleccionInfo | None, seleccion_visitante: SeleccionInfo | None
    ) -> ValorVariable:
        """`docs/16`: "diferencia neta de victorias". Cuenta, sobre todo el
        historial de enfrentamientos directos entre ambas selecciones
        (cualquier orden local/visitante histórico), las victorias del
        equipo que hoy es local menos las del equipo que hoy es visitante.
        Empates no suman a ninguno. Sin historial, `disponible=False` --
        nunca se sustituye por 0 (`docs/16`/brief: "nunca reemplazar
        silenciosamente por cero").
        """
        if seleccion_local is None or seleccion_visitante is None:
            return self._pendiente()

        historial = self._repository.historial_enfrentamientos(
            seleccion_local.id_seleccion, seleccion_visitante.id_seleccion
        )
        if not historial:
            return self._pendiente()

        victorias_local_actual = 0
        victorias_visitante_actual = 0
        for resultado in historial:
            if resultado.goles_local == resultado.goles_visitante:
                continue  # empate -- no suma a ninguno
            ganador = (
                resultado.id_seleccion_local
                if resultado.goles_local > resultado.goles_visitante
                else resultado.id_seleccion_visitante
            )
            if ganador == seleccion_local.id_seleccion:
                victorias_local_actual += 1
            elif ganador == seleccion_visitante.id_seleccion:
                victorias_visitante_actual += 1

        diferencia = victorias_local_actual - victorias_visitante_actual
        return ValorVariable(
            valor=float(diferencia),
            disponible=True,
            muestra_reducida=len(historial) < MUESTRA_REDUCIDA_UMBRAL,
        )

    # -- Estructura "pendiente" -- variables sin método autorizado o bloqueadas --

    def _pendiente(self) -> ValorVariable:
        """Una Variable Oficial sin calcular -- estructura únicamente,
        nunca un valor inventado.
        """
        return ValorVariable(valor=None, disponible=False, muestra_reducida=False)

    def _pendiente_por_equipo(self) -> VariablesPorEquipo:
        """La misma estructura pendiente, una vez por equipo (local y
        visitante) -- ver docs/30, sección 4.3.
        """
        return VariablesPorEquipo(local=self._pendiente(), visitante=self._pendiente())

    # -- Errores -- únicamente para Variable002/Variable003/Variable004
    # (brief de BUILD-018/BUILD-019/BUILD-021: "registrar la causa" sin
    # lanzar una excepción que detenga VariablePreparation) ------------------

    @staticmethod
    def _registrar_error_preparacion(context: PredictionContext, evento: str, detalle: str) -> None:
        """Único punto de registro de anomalías de `VariablePreparation`
        (`docs/30` §4.8) -- mismo patrón que `_registrar_error` en
        `Engine01`-`06`, adaptado a esta clase (que no tenía, hasta
        `BUILD-018`, ningún camino de error que necesitara tocar
        `context.errors`).
        """
        context.errors.append(
            ErrorEntry(
                evento=evento,
                componente_emisor="VariablePreparation",
                capa_fase="Fase 3",
                timestamp=datetime.now(timezone.utc),
                detalle=detalle,
            )
        )
