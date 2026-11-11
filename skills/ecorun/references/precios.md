# Precios y características (precios de lista de la API)

Última verificación: 10 nov 2026.

Fuente: claude.dev, "Which Claude model should you build with?" (9 nov 2026). Revisar si hay modelos más nuevos.

| | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 | Fable 5.2 |
|---|---|---|---|---|
| Pensado para | Alto volumen, costo bajo | Tareas acotadas, rápido | Trabajo diario complejo | Trabajo técnico más ambicioso y abierto |
| Latencia | La más rápida | Rápida | Moderada | Moderada |
| Entrada / salida (USD por millón de tokens) | 0,10 / 0,50 hasta 100K de prompt; 0,50 / 2,50 por encima | 2 / 10 | 4 / 20 | 8 / 40 |
| Lectura de caché (USD por millón) | 0,01 hasta 100K; 0,05 por encima | 0,10 | 0,20 | 0,20 |
| Contexto / salida máx. | 1M / 128K | 1M / 128K | 1M / 128K | 1M / 128K |
| Effort por defecto (API) | medium | high (medium en Claude Code) | medium | high (medium en Claude Code) |
| Modo rápido | No | No | Sí | Sí |

## Proporciones que deciden casi todo
- Opus 5.5 cuesta el doble que Sonnet 5.5 por token, y Fable 5.2 el doble que Opus 5.5.
- En corridas largas con mucho caché, Fable y Opus cobran igual la lectura de caché; la diferencia queda en entrada sin caché y salida.
- Haiku 5.5 rinde más con prompts cortos (≤100K): ahí cuesta una veinteava parte de la entrada de Sonnet. Con prompts largos, comparar costo por tarea terminada contra Sonnet, no el precio de lista.

## Datos de referencia sobre effort (Opus 5.5, SWE-bench Pro)
- `medium`: ~2,5 puntos menos que `high` por ~70 % del costo.
- `low`: ~8 puntos menos por ~1/3 del costo.
- `xhigh`: ~1,4 puntos más por 2,5 veces el costo de `high`.
- En FrontierCode 2.0, Fable 5.2 en `high` empató con Opus 5.5 en `max` por cerca de la mitad del costo por tarea: antes de subir Opus por encima de `high`, probar Fable.

## Costo del contexto
Una lectura de caché por turno en Opus 5.5 cuesta ~0,03 USD con 150K tokens de contexto y ~0,004 USD con 20K. Mantener el contexto del modelo grande corto ahorra en cada turno.
