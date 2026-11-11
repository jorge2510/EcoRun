<p align="center">
  <img src="docs/icon-256.png" alt="EcoRun" width="120">
</p>

<h1 align="center">EcoRun</h1>

<p align="center">
  <b>Nuestro mejor aliado para crear proyectos optimizando nuestros tokens.</b><br>
  Una skill y plugin para Claude que elige el modelo y el nivel de effort adecuados para cada tarea,<br>
  para gastar menos tokens sin bajar la calidad del resultado.
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licencia MIT" src="https://img.shields.io/badge/licencia-MIT-green"></a>
  <img alt="Versión" src="https://img.shields.io/badge/versión-1.0.0-blue">
  <img alt="Claude.ai, Cowork y Claude Code" src="https://img.shields.io/badge/funciona%20en-Claude.ai%20%7C%20Cowork%20%7C%20Claude%20Code-orange">
</p>

<p align="center"><a href="README.en.md">English version</a></p>

---

## ¿Qué problema resuelve?

Usar siempre el modelo más grande es cómodo, pero caro: una buena parte de las tareas (buscar archivos, leer logs, extraer datos de PDFs, aplicar una plantilla) la resuelve igual de bien un modelo más pequeño y rápido. Y al revés: bajar de modelo en una tarea difícil sale más caro, porque hay que repetirla.

EcoRun aplica la guía oficial de Anthropic para elegir modelo ([Which Claude model should you build with?](https://claude.dev/blog/which-claude-model-should-you-build-with/)) en cada tarea, de forma automática:

| Tipo de tarea | Modelo |
|---|---|
| Buscar, leer logs, extraer, clasificar (errores fáciles de detectar) | **Haiku** |
| Tareas acotadas con especificación clara, documentos cotidianos | **Sonnet** |
| Trabajo que requiere juicio, diseño o depuración difícil (punto de partida) | **Opus** |
| Refactors y migraciones grandes, arquitectura, investigación profunda | **Fable** (si tienes acceso; si no, Opus en `high`) |

Además sigue una **escalera de calidad**: antes de subir de modelo, primero le da a Claude una forma de verificar su trabajo y luego sube el effort; solo después cambia de modelo.

## Qué hace en cada entorno

Ninguna skill puede cambiar el modelo de tu conversación principal; eso lo eliges tú. Lo que EcoRun sí hace:

| Entorno | Qué pasa |
|---|---|
| **Claude.ai y apps** | Al empezar una tarea, si conviene otro modelo, escribe una línea como `Modelo sugerido: Sonnet · medium — tarea acotada` y sigue trabajando. Si ya estás en el correcto, no dice nada. |
| **Cowork** | Igual que en claude.ai. Si Cowork le permite lanzar subagentes con modelo propio, delega en ellos el trabajo pesado de lectura. |
| **Claude Code** | Enruta de verdad: manda la búsqueda, la lectura de logs y la extracción a subagentes en Haiku. Para la sesión principal te sugiere `/model` y `/effort` cuando conviene. |
| **API** | Te da las reglas para elegir el `model` por código según el tipo de paso. |

**Fable es automático:** no tienes que configurar si tienes acceso. Si EcoRun intenta usar Fable y no está disponible, sigue con Opus en `high` sin preguntarte.

## Instalación

### Claude.ai y Cowork (skill)

1. Descarga [`dist/ecorun.zip`](dist/ecorun.zip).
2. Asegúrate de tener activada la ejecución de código y creación de archivos (en la configuración de capacidades de Claude).
3. Ve a **Customize → Skills**, pulsa **+**, elige **Create skill → Upload a skill** y sube el ZIP.
4. Activa la skill en tu lista.

Si estás en un plan Team o Enterprise, tu organización puede tener los menús con otros nombres o necesitar que un administrador habilite las skills. Las skills que activas en tu cuenta también se sincronizan con Claude Code cuando inicias sesión con la misma cuenta.

### Claude Code (plugin, recomendado)

El plugin incluye la skill **y** los subagentes en Haiku, que es donde está la mayor parte del ahorro:

```
/plugin marketplace add jorge2510/EcoRun
/plugin install ecorun@ecorun
```

Opcional pero recomendado: deja también la exploración integrada de Claude Code en Haiku copiando la plantilla de `Explore`:

```bash
mkdir -p ~/.claude/agents
curl -o ~/.claude/agents/Explore.md https://raw.githubusercontent.com/jorge2510/EcoRun/main/templates/agents/Explore.md
```

Requisitos: una versión reciente de Claude Code (`claude update`). No definas `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, porque obliga a todos los subagentes a un solo modelo y anula el enrutamiento.

### Solo la skill en Claude Code

Si prefieres no instalar el plugin, copia la carpeta `skills/ecorun` a `~/.claude/skills/ecorun` (todos tus proyectos) o a `.claude/skills/ecorun` (un proyecto). Funcionará, pero sin los subagentes incluidos.

## Cómo usarla

No necesitas hacer nada especial: la skill se activa sola al empezar una tarea sustancial o cuando hablas de ahorrar tokens, elegir modelo o configurar subagentes. También puedes llamarla directamente:

- En claude.ai: "usa EcoRun para esta tarea" o `/ecorun`.
- En Claude Code: `/ecorun:ecorun`.

Ejemplos de lo que verás:

> **Tú:** Pasa los datos de estas 40 facturas a una hoja de cálculo.
> **Claude:** `Modelo sugerido: Haiku · medium (extracción repetitiva, fácil de revisar).` …y sigue con la tarea.

> **Tú (Claude Code):** Encuentra dónde se valida el token de sesión y arregla el bug de expiración.
> **Claude:** Delega la búsqueda a `ecorun:eco-explorer` (Haiku) y hace la corrección en el modelo principal.

## Qué incluye el repositorio

```
EcoRun/
├── .claude-plugin/
│   ├── plugin.json          # Manifiesto del plugin
│   ├── marketplace.json     # Permite instalarlo con /plugin marketplace add
│   └── icon.png
├── skills/ecorun/
│   ├── SKILL.md             # La skill
│   ├── references/          # Detalle para Claude Code/API y tabla de precios
│   └── evals/               # Casos de prueba
├── agents/                  # Subagentes en Haiku: explorer, log-reader, extractor
├── templates/agents/        # Plantilla de Explore para copiar a ~/.claude/agents
├── dist/ecorun.zip          # Paquete listo para subir a claude.ai
├── scripts/                 # Validación y empaquetado
└── docs/                    # Cómo funciona y preguntas frecuentes
```

## Documentación

- [Cómo funciona EcoRun](docs/como-funciona.md): criterios, escalera de calidad y por qué no se pierde calidad.
- [Preguntas frecuentes](docs/faq.md).
- [Referencia para Claude Code y API](skills/ecorun/references/claude-code.md).
- [Precios y características de los modelos](skills/ecorun/references/precios.md).

## Desarrollo

```bash
python3 scripts/validate.py      # revisa la skill, los subagentes y los manifiestos
python3 scripts/build.py         # genera dist/ecorun.zip
npx @anthropic-ai/claude-code plugin validate .   # validador oficial de plugins
```

Para probar la skill con los casos de `skills/ecorun/evals/` desde Claude Code: `claude plugin eval skills/ecorun`. Son ejecuciones reales y se cobran.

Las contribuciones son bienvenidas; lee [CONTRIBUTING.md](CONTRIBUTING.md).

## Limitaciones

- Ninguna skill puede cambiar el modelo de la conversación principal; EcoRun recomienda y, donde hay subagentes, delega.
- Los nombres de modelos y los precios cambian. La tabla de precios indica su fecha de verificación; si sale un modelo nuevo, EcoRun aplica el mismo criterio por familia (Haiku, Sonnet, Opus, Fable) y avisa que la tabla puede estar desactualizada.
- Las cifras de ahorro citadas vienen de pruebas publicadas por Anthropic. Tu ahorro real depende de tus tareas; mídelo con `/usage` en Claude Code.

## Licencia

[MIT](LICENSE) © 2026 Jorge Cabrera. EcoRun es un proyecto independiente y no está afiliado a Anthropic.
