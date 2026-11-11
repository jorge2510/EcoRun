# Cómo funciona EcoRun

## La idea central

El costo real de una tarea no es el precio por token, sino lo que cuesta **terminarla bien**. Un modelo pequeño es más barato por token, pero si falla y hay que repetir, sale caro. Un modelo grande en una tarea trivial desperdicia dinero. EcoRun busca el modelo más barato que todavía termina la tarea igual de bien.

Regla de oro: **si hay duda entre ahorrar y mantener calidad, gana la calidad.** Por eso el punto de partida es Opus en effort `medium`, como recomienda Anthropic, y EcoRun solo baja cuando la tarea claramente lo permite.

## Las tres preguntas

Para cada tarea, EcoRun se pregunta en orden:

1. **¿Requiere juicio, diseño o decisiones estructurales?** → Opus como mínimo.
2. **¿Está bien acotada y tiene especificación clara?** → Sonnet.
3. **¿Es repetitiva, de alto volumen, y un error se detecta fácil?** → Haiku.

Las tareas más ambiciosas (migraciones grandes, arquitectura, investigación profunda) van a Fable si hay acceso.

## La escalera de calidad

Cuando un resultado no alcanza, EcoRun no salta directo al modelo más caro:

1. **Verificación:** le da a Claude una forma de comprobar su trabajo (un test, un build, un cálculo de control). Es lo más barato.
2. **Effort:** sube un nivel de esfuerzo.
3. **Modelo:** sube al siguiente modelo, empezando con un effort menor.

Pasado `high`, un nivel más de effort puede costar lo mismo que un modelo más grande, así que conviene probar el modelo siguiente en `medium` antes de ir a `xhigh` o `max`.

## Por qué no se pierde calidad

- Los modelos pequeños solo hacen trabajo donde un error salta a la vista: encontrar archivos, leer logs, extraer campos. Las decisiones y las ediciones de código se quedan en el modelo principal.
- Los subagentes de EcoRun están escritos para no adivinar: si no encuentran algo o un dato es dudoso, lo dicen explícitamente.
- Ante la duda, EcoRun elige el modelo más capaz.

## Fable automático

EcoRun no pide configuración. Si la sesión corre en Fable, sabe que lo tienes. En Claude Code intenta usarlo y, si no está disponible, repite con Opus en `high`. En chat y Cowork, la recomendación incluye el respaldo: `Fable · medium (si no lo tienes, Opus · high)`.

## Cambiar de modelo sin desperdiciar

- El caché de contexto pertenece al modelo que lo escribió: al cambiar, el primer turno paga reescribir todo el contexto. Conviene hacer `/compact` o empezar una sesión nueva con un plan corto.
- Bajar de modelo pierde el razonamiento previo. Por eso EcoRun cambia en pausas naturales y deja por escrito las decisiones importantes.

## Ahorro sin cambiar de modelo

- Contexto magro: no pegar archivos enteros si basta un fragmento.
- Delegar lectura pesada a subagentes baratos que devuelven solo un resumen.
- Respuestas del tamaño justo.
