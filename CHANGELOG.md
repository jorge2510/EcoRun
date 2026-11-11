# Changelog

Todos los cambios importantes de EcoRun se registran aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [1.2.0] — 2026-11-10

### Cambiado
- Licencia: de MIT a **MIT + Commons Clause**. EcoRun sigue siendo gratis para usar, modificar y compartir, pero venderla (sola o dentro de un producto o servicio de pago) requiere autorización escrita del autor. Las versiones anteriores siguen bajo MIT.
- `dist/ecorun.zip` ahora incluye el archivo `LICENSE`, para que la licencia viaje con la skill.
- La skill declara su licencia en el campo `license` del frontmatter.

### Corregido
- Se restauró la carpeta `.claude-plugin/` (`plugin.json`, `marketplace.json` e icono), que faltaba en el repositorio: `/plugin marketplace add jorge2510/EcoRun` vuelve a funcionar.
- Se restauró la integración continua (`.github/workflows/validate.yml`), que corre `validate.py` y `build.py` en cada push y pull request.

## [1.1.0] — 2026-11-10

### Cambiado
- **Compuerta** en claude.ai, Cowork y la sesión principal de Claude Code: EcoRun clasifica la tarea antes de ejecutarla y, si conviene otro modelo, manda un mensaje corto con la sugerencia y espera la elección del usuario, en vez de hacer la tarea y recomendar al final.
- EcoRun corre antes de cualquier otra skill, herramienta, búsqueda o lectura de archivos.

### Añadido
- Reglas para no frenar de más: no frena si la respuesta sería más corta que el aviso, no repite la pregunta para la misma tarea y respeta "no me preguntes". Frena siempre si el modelo actual se queda corto.
- Casos de prueba `compuerta-frena-tarea-sustancial` y `compuerta-no-frena-pregunta-corta`.

## [1.0.0] — 2026-11-10

### Añadido
- Skill `ecorun`: elige modelo (Haiku, Sonnet, Opus, Fable) y effort por tipo de tarea, con escalera de calidad y reglas para no perder calidad.
- Detección automática de Fable: si no está disponible, sigue con Opus en `high` sin pedir configuración.
- Plugin de Claude Code con tres subagentes en Haiku: `eco-explorer`, `eco-log-reader` y `eco-extractor`.
- Marketplace para instalar con `/plugin marketplace add jorge2510/EcoRun`.
- Plantilla de `Explore` en Haiku para `~/.claude/agents/`.
- Referencias de Claude Code/API y tabla de precios (verificada el 10 nov 2026).
- Casos de prueba en `skills/ecorun/evals/`, scripts de validación y empaquetado, e integración continua con GitHub Actions.
- README en español e inglés.
