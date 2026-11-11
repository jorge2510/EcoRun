---
name: ecorun
description: EcoRun elige el modelo de Claude (Haiku, Sonnet, Opus o Fable) y el nivel de effort adecuados para cada tarea, para ahorrar tokens sin bajar la calidad del resultado. Úsala SIEMPRE al empezar una tarea sustancial (código, documentos, informes, análisis de datos, extracción, automatizaciones, investigación), cuando el usuario diga "qué modelo uso", "ahorrar tokens", "gastar menos", "optimizar costo", "cambiar de modelo", "effort", "subagentes", o cuando configure Claude Code, agentes o llamadas a la API. También en inglés ("which model should I use", "save tokens", "reduce cost", "model routing"). Úsala también cuando una tarea larga cambie de naturaleza a mitad de camino (por ejemplo, de diseñar a solo formatear).
---

# EcoRun

Objetivo: gastar el mínimo de tokens que todavía dé el mismo resultado. Si hay duda entre ahorrar y mantener calidad, gana la calidad.

Basado en la guía oficial de Anthropic "Which Claude model should you build with?" (claude.dev, 9 nov 2026) y en la documentación de Claude Code sobre subagentes. Responde siempre en el idioma del usuario; las plantillas de abajo están en español solo como ejemplo.

## Disponibilidad de Fable (automática)

Nunca le pidas al usuario que configure o declare si tiene acceso a Fable. Decídelo así:

1. Si la sesión actual corre en Fable → está disponible.
2. Si en esta conversación (o en la memoria) el usuario dijo que no tiene Fable, o un intento de usar `fable` falló → no está disponible.
3. En Claude Code, cuando una tarea pida Fable: lanza el subagente con `model: fable`. Si falla porque el modelo no está disponible, repite en ese mismo turno con `opus` y effort `high`, y sigue sin preguntar.
4. En chat o Cowork, donde solo recomiendas, escribe la recomendación con su respaldo incluido, para que sirva tenga o no acceso:
   `Modelo sugerido: Fable · medium (si no lo tienes, Opus · high) — refactor grande.`

Sin Fable, todo lo que abajo diga "Fable" pasa a "Opus en `high`, luego `xhigh`, con verificación obligatoria" (ver Escalera de calidad).

## Paso 0 — Saber dónde estás

Ninguna skill puede cambiar el modelo de la conversación principal: eso lo hace el usuario (selector de modelo en la app, `/model` en Claude Code). Lo que sí se puede es recomendar a tiempo y, donde hay subagentes, mandar el trabajo a un modelo más barato.

- **claude.ai, apps y Cowork:** recomienda. Si el modelo ideal es distinto al actual, escribe UNA línea al inicio de la respuesta y sigue trabajando con el modelo actual (no te detengas a esperar):
  `Modelo sugerido: Sonnet · medium — tarea acotada con verificación fácil.`
  Si el modelo actual ya es el correcto, no digas nada: esa línea también cuesta tokens. Repite la recomendación solo cuando la tarea cambie de naturaleza, no en cada mensaje. En Cowork, si puedes lanzar subagentes y elegir su modelo, delega como en Claude Code; si no, quédate con la recomendación.
- **Claude Code:** aquí sí enrutas de verdad. Para trabajo de Haiku o Sonnet (leer, buscar, extraer, tareas acotadas) delega a un subagente con el modelo adecuado: usa uno de los subagentes de EcoRun (`eco-explorer`, `eco-log-reader`, `eco-extractor`, todos en Haiku) o pasa el parámetro `model` al lanzar cualquier subagente; ese parámetro tiene prioridad sobre el modelo de la sesión. La conversación principal se queda en su modelo; si conviene cambiarla, recomienda en una línea `/model <alias>` y `/effort <nivel>`. Detalles en `references/claude-code.md`.
- **API o apps que llaman a la API:** elige el `model` por código según el tipo de paso, no le pidas a un modelo que decida qué modelo usar. Ver `references/claude-code.md` (sección API).

## Paso 1 — Clasificar la tarea

Hazte tres preguntas, en este orden:

1. **¿Requiere juicio, diseño o decisiones estructurales?** (diseñar una solución, elegir una arquitectura, redactar conclusiones, depurar algo cuya causa no es obvia) → Opus como mínimo.
2. **¿Está bien acotada y hay especificación clara?** (corregir un bug ya identificado, agregar una función según especificación, aplicar una plantilla conocida) → Sonnet. Ojo: una migración o una optimización de rendimiento pueden tener especificación clara y aun así ser difíciles; esas van en Opus.
3. **¿Es repetitiva, de alto volumen, y un error se detecta fácil?** (clasificar, etiquetar, extraer campos, leer logs, buscar archivos, resumir) → Haiku.

Si no estás seguro → Opus · `medium`. Es el punto de partida que recomienda Anthropic.

## Tabla de ruteo

| Tarea | Modelo inicial | Effort inicial |
|---|---|---|
| No sé todavía / tarea mixta | Opus | medium |
| Ingeniería y depuración del día a día, features de varios pasos | Opus | medium → high |
| Diseño técnico, criterios de diseño, interpretar datos o mediciones, conclusiones | Opus | medium → high |
| Visión y computer use (planos, capturas, fotos, renders, formularios en pantalla) | Opus | medium |
| Documentos, slides y hojas de cálculo cotidianos | Sonnet | high (medium en Claude Code) |
| Documento armado desde mucho material fuente, o modelo financiero complejo | Opus | medium |
| Código bien acotado: bug identificado, iterar una feature, trabajo contra spec | Sonnet | medium → high |
| Tareas de agente repetidas (revisar, investigar, redactar con formato fijo) | Sonnet | medium |
| Chat rápido, preguntas cortas | Sonnet (Haiku si es trivial) | low o medium |
| Clasificación, ruteo, etiquetado, extracción de datos en volumen | Haiku | medium |
| Subagentes que buscan archivos, leen logs o resumen | Haiku o Sonnet | default |
| Refactor o migración grande, planificar arquitectura, liderar muchos subagentes | Fable | medium → high |
| Investigación profunda, análisis científico o cuantitativo difícil | Fable | medium → high |
| Opus en `high` se quedó corto, o corrida larga sin supervisión | Fable | medium |

Ejemplos:
- Pasar datos de 40 facturas PDF a una hoja de cálculo → Haiku (Sonnet si los documentos son manuscritos o de mala calidad).
- Cambiar una columna en un script que ya funciona → Sonnet.
- Informe con datos ya medidos y plantilla definida → Sonnet para el formato; Opus para el análisis y las conclusiones.
- Diseñar una solución técnica desde cero con requisitos ambiguos → Opus (Fable si es muy abierta y hay acceso).
- Reestructurar una app completa o migrar su arquitectura → Fable; sin Fable, Opus en `high`.

## Escalera de calidad (cuando el resultado no alcanza)

Sigue este orden; no saltes directo al modelo más caro:

1. **Dale una forma de verificarse:** un test, un build, un script que compruebe el resultado, un cálculo de control independiente. Suele ser más barato que subir effort.
2. **Sube el effort un nivel.**
3. **Sube al siguiente modelo, empezando con un effort MENOR** al que usabas en el pequeño.

Pasado `high`, un nivel más de effort puede costar lo mismo que un modelo más grande: prueba el modelo siguiente en `medium` antes de ir a `xhigh` o `max`. Subir effort no le da al modelo conocimiento que no tiene; para eso hay que subir de modelo.

Truco cuando la verificación es automática: corre todo en effort bajo y repite solo los fallos en alto. En la prueba publicada por Anthropic (Opus 5.5, SWE-bench Pro) eso dio ~97 % de éxito a ~0,17 USD por tarea, contra 95,3 % a 0,29 USD con todo en `high`.

## Reglas para no perder calidad

- Los modelos pequeños solo hacen trabajo donde un error es barato de detectar (buscar, leer, extraer, clasificar). Las ediciones de código, los cálculos de diseño y las decisiones se quedan en el modelo principal.
- Precio por token alto ≠ costo por tarea alto. Un modelo mejor que acierta a la primera puede salir más barato que uno pequeño que necesita tres intentos.
- Las tareas más difíciles concentran la mayor parte del gasto: ahí es donde conviene comparar, no en las fáciles.
- Nunca bajes de modelo solo porque la tarea "parece corta". Lo que cuenta es cuánto juicio requiere.

## Ahorro sin cambiar de modelo

- **Contexto magro:** cada turno reenvía todo el contexto, y cuanto más grande el modelo, más importa. No pegues archivos enteros si basta un fragmento; no releas lo que ya está en contexto.
- **Delegar lectura pesada:** que un subagente barato lea logs, PDFs largos o carpetas y devuelva un resumen; el modelo grande toma las decisiones.
- **Respuestas del tamaño justo:** no repitas el documento completo para un cambio pequeño; no añadas resúmenes que nadie pidió.

## Cambiar de modelo a mitad de trabajo

- Cambia en una pausa natural (al terminar una fase), no en medio de un razonamiento.
- El caché pertenece al modelo que lo escribió: el primer turno en el modelo nuevo paga escribir todo el contexto otra vez. Antes de cambiar, haz `/compact` en Claude Code o abre una sesión nueva con un plan corto escrito.
- Bajar de nivel pierde el razonamiento previo (un modelo nunca lee los bloques de pensamiento de uno superior). Pasar de Fable a cualquier otro también lo pierde. Deja por escrito las decisiones importantes antes de cambiar.

## Mantenimiento

Los nombres y precios cambian. Si ves un modelo más nuevo que los de esta skill en el selector o en la documentación, avisa en una línea que la tabla puede estar desactualizada y aplica el mismo criterio a la familia correspondiente (Haiku, Sonnet, Opus, Fable). Precios de referencia en `references/precios.md`.
