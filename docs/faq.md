# Preguntas frecuentes

### ¿EcoRun cambia el modelo por mí?
No el de tu conversación principal: ninguna skill puede hacerlo. En claude.ai y Cowork te sugiere en una línea qué modelo usar; tú lo cambias en el selector. En Claude Code sí manda trabajo a subagentes en Haiku de forma automática, que es donde está la mayor parte del ahorro.

### ¿Me va a llenar las respuestas de avisos?
No. Solo escribe la línea de modelo sugerido cuando el modelo ideal es distinto al actual, y solo al empezar una tarea o cuando la tarea cambia de naturaleza.

### No tengo acceso a Fable. ¿Tengo que configurar algo?
No. EcoRun lo detecta: si Fable no está disponible, usa Opus en `high` con verificación.

### ¿Funciona en inglés u otros idiomas?
Sí. La skill está escrita en español, pero Claude responde en el idioma en que le escribas.

### ¿Por qué no usa Haiku para todo, si es lo más barato?
Porque en tareas que requieren juicio un modelo pequeño se equivoca más, y repetir la tarea sale más caro que hacerla bien la primera vez. EcoRun mide el costo por tarea terminada, no por token.

### ¿Cómo sé cuánto estoy ahorrando?
En Claude Code, corre la misma tarea con y sin EcoRun (o con dos modelos usando `/model`) y compara lo que muestra `/usage`. `/tasks` te dice en qué modelo corre cada subagente.

### Instalé el plugin pero los subagentes siguen en el modelo grande.
Revisa que no tengas definida `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` y que tu Claude Code esté actualizado (`claude update`). En versiones anteriores a la v2.1.251, `CLAUDE_CODE_SUBAGENT_MODEL` pasaba por encima del modelo de cada subagente.

### ¿Por qué la plantilla de `Explore` no viene dentro del plugin?
Porque un subagente de plugin no puede reemplazar al `Explore` integrado de Claude Code; solo uno de usuario (`~/.claude/agents/`) o de proyecto (`.claude/agents/`) puede. Por eso se copia aparte.

### Subí el ZIP a claude.ai y da error.
La carpeta dentro del ZIP debe llamarse igual que la skill (`ecorun`). Usa el `dist/ecorun.zip` del repositorio o genéralo con `python3 scripts/build.py`. Verifica también que la ejecución de código esté activada.

### Tengo dos skills parecidas instaladas.
Desactiva o elimina la otra. Si dos skills de selección de modelo se activan a la vez, gastas tokens de más.
