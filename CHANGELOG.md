# Changelog

Todos los cambios importantes de EcoRun se registran aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [versionado semántico](https://semver.org/lang/es/).

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
