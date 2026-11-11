# Cómo contribuir a EcoRun

¡Gracias por ayudar! Estas son las reglas para que EcoRun siga siendo confiable.

## Qué tipo de cambios buscamos

- **Actualizar modelos y precios** cuando Anthropic publique nuevos. Cita la fuente oficial (claude.dev, platform.claude.com, code.claude.com o anthropic.com) y actualiza la fecha de "Última verificación" en `skills/ecorun/references/precios.md`.
- **Mejorar el ruteo** con evidencia: describe la tarea, el modelo que EcoRun eligió, el que debió elegir y por qué (idealmente con costos de `/usage`).
- **Nuevos subagentes** solo para trabajo donde un error es fácil de detectar (buscar, leer, extraer, clasificar). Las decisiones y ediciones se quedan en el modelo principal.
- **Traducciones** del README.

## Reglas de estilo de la skill

- Mantén `SKILL.md` por debajo de ~500 líneas; el detalle va en `references/`.
- Explica el porqué de cada regla en vez de usar solo MAYÚSCULAS.
- Nombra los modelos por familia (Haiku, Sonnet, Opus, Fable) en las reglas; deja las versiones exactas para `references/precios.md`.
- La regla de oro no cambia: si hay duda entre ahorrar y mantener calidad, gana la calidad.

## Antes de abrir un pull request

```bash
python3 scripts/validate.py
python3 scripts/build.py
npx @anthropic-ai/claude-code plugin validate .
```

1. Si cambiaste la skill o los subagentes, sube la versión en `.claude-plugin/plugin.json` y `.claude-plugin/marketplace.json` (las dos deben coincidir; `validate.py` lo revisa).
2. Agrega una entrada en `CHANGELOG.md`.
3. Si el cambio afecta el comportamiento, agrega o actualiza un caso en `skills/ecorun/evals/`.
4. Vuelve a generar `dist/ecorun.zip` con `scripts/build.py` y súbelo en el mismo PR.

## Reportar problemas

Abre un issue con: entorno (claude.ai, Cowork, Claude Code o API), modelo de la sesión, lo que pediste, lo que hizo EcoRun y lo que esperabas.
