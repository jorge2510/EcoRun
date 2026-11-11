# Enrutamiento real en Claude Code y en la API

## Claude Code

### Qué cambia solo y qué no
- **Cambia solo:** los subagentes. Uno definido con `model: haiku` corre en Haiku cada vez que se le delega trabajo. Además, al lanzar cualquier subagente se puede pasar el parámetro `model` (`haiku`, `sonnet`, `opus`, `fable` o un ID completo) y opcionalmente `effort`.
- **No cambia solo:** la conversación principal. Solo cambia con `/model`, `--model` o la configuración. EcoRun lo recomienda en una línea cuando conviene.
- **Fable sin acceso:** si un subagente con `model: fable` falla porque el modelo no está disponible, relanzar con `model: opus` y effort `high` en el mismo turno, sin preguntar.

### Orden en que Claude Code decide el modelo de un subagente
1. El parámetro `model` de esa invocación.
2. El campo `model` del archivo del subagente (`inherit` = modelo de la conversación principal).
3. La variable `CLAUDE_CODE_SUBAGENT_MODEL`, si está definida.
4. El modelo de la conversación principal.

Si un alias es de la misma familia que la conversación principal (por ejemplo `opus` con la sesión en Opus), el subagente usa exactamente el modelo de la sesión.

### Subagentes que trae EcoRun (plugin)
Todos en Haiku, solo lectura salvo lo indicado:
- `ecorun:eco-explorer` — busca archivos, símbolos y patrones; devuelve rutas y líneas.
- `ecorun:eco-log-reader` — lee salidas de tests y logs; reporta cada fallo.
- `ecorun:eco-extractor` — extrae campos de PDFs, imágenes o tablas a JSON, marcando lo dudoso.

### Exploración barata (opcional, recomendado)
El subagente integrado `Explore` usa el modelo de la sesión (o Opus si la sesión está en Fable). Un subagente de usuario o de proyecto llamado `Explore` lo reemplaza; uno de plugin no puede. Para dejar la exploración en Haiku, copia `templates/agents/Explore.md` del repositorio a `~/.claude/agents/` (todos tus proyectos) o a `.claude/agents/` (un proyecto).

### Comandos útiles
- `/model` cambia el modelo de la sesión.
- `/effort` cambia el nivel de esfuerzo; `/effort status` muestra el actual.
- `/tasks` muestra en qué modelo corre cada subagente.
- `/usage` muestra el gasto: úsalo para comparar dos modelos en la misma tarea.
- `/compact` antes de cambiar de modelo, para que el primer turno del modelo nuevo no pague todo el historial.

### Variables de entorno
- `CLAUDE_CODE_SUBAGENT_MODEL`: modelo por defecto para subagentes que no fijan uno. Desde Claude Code v2.1.251 ya no pasa por encima del `model` de cada subagente ni del parámetro por invocación; en versiones anteriores sí, así que actualiza (`claude update`) o no la definas.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`: NO la actives con EcoRun. Obliga a todos los subagentes a un solo modelo e ignora el enrutamiento.
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`: fija a qué modelo apunta el alias `haiku`.
- Los alias dependen del proveedor: en la API de Anthropic apuntan a la última versión de cada familia; en Bedrock, Google Cloud, Foundry o Claude Platform on AWS pueden apuntar a versiones anteriores. Revisa la documentación de configuración de modelos de Claude Code.

### Sobre `opusplan`
Planifica con Opus y ejecuta con Sonnet, o sea, las ediciones de código quedan en Sonnet. Eso va al revés de la regla de EcoRun (ediciones en el modelo principal). Mídelo en tus tareas antes de usarlo por defecto.

### Cuándo NO usar equipos de subagentes
Para una cadena de pasos dependientes o trabajo que cabe en una sola ventana de contexto, planificar y fusionar cuesta más de lo que ahorra. Los equipos (un líder grande + muchos trabajadores baratos) rinden en trabajo más grande que un contexto: en una prueba de Anthropic, Opus 5.5 liderando trabajadores Sonnet 5.5 costó un tercio menos que Opus solo, con resultado similar.

## API

- Elige `model` por código según el tipo de paso (una tabla tipo → modelo). No le pidas a un modelo que decida qué modelo usar.
- Construye cada petición para el modelo más estricto del sistema, así un paso puede subir o bajar de nivel sin tocar código:
  - historial solo de anexado (no editar mensajes previos; Fable rechaza con error 400 si cambia algo antes de uno de sus bloques de pensamiento),
  - `tool_choice: auto` con herramientas `strict: true` (`any`/`tool` dan error 400 en Sonnet 5.5, Opus 5.5 y Fable 5.2),
  - leer los bloques de contenido por `type` (la respuesta puede empezar con un bloque de pensamiento).
- Opus y Fable siempre piensan: pedir thinking apagado da error.
- Haiku 5.5: no usar `temperature`/`top_p`/`top_k` distintos del valor por defecto, reemplazar `budget_tokens` por effort y terminar `messages` con un turno de usuario.
- Herramienta advisor (beta): ejecutor barato + asesor fuerte. Solo compensa si el ejecutor consulta seguido en trabajo mayormente rutinario. Mide la tasa de consulta antes de adoptarla; en las pruebas publicadas ninguna combinación superó claramente al ejecutor solo.

## Medir antes de fijar una regla
1. Toma tareas reales y define un chequeo de resultado para cada una.
2. Corre cada modelo candidato en 2–3 niveles de effort, cada uno en su propia sesión.
3. Registra el costo por tarea terminada (campo `usage`) y grafica puntaje contra gasto.
4. Quédate con una combinación de modelos solo si supera a todos los puntos de modelo único.
