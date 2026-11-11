#!/usr/bin/env python3
"""Valida la skill, los subagentes y los manifiestos de EcoRun.

Uso: python3 scripts/validate.py
Sale con código 1 si encuentra errores.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ecorun"
VALID_MODELS = {"haiku", "sonnet", "opus", "fable", "inherit"}
VALID_EFFORT = {"low", "medium", "high", "xhigh", "max"}
errors, warnings = [], []


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: falta el frontmatter al inicio")
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)}: frontmatter sin cierre")
        return {}, text
    data = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip().strip('"')
    return data, text[end + 4:]


# 1. Skill
fm, body = frontmatter(SKILL / "SKILL.md")
if fm.get("name") != "ecorun":
    errors.append("SKILL.md: name debe ser 'ecorun' (igual a la carpeta)")
desc = fm.get("description", "")
if not desc:
    errors.append("SKILL.md: falta description")
elif len(desc) > 1024:
    errors.append(f"SKILL.md: description tiene {len(desc)} caracteres (máx. 1024)")
lines = body.count("\n")
if lines > 500:
    warnings.append(f"SKILL.md: {lines} líneas (se recomienda < 500)")
for ref in re.findall(r"`(references/[^`]+\.md)`", body):
    if not (SKILL / ref).exists():
        errors.append(f"SKILL.md: referencia rota {ref}")

# 2. Subagentes
agent_files = sorted((ROOT / "agents").glob("*.md")) + sorted((ROOT / "templates" / "agents").glob("*.md"))
names = set()
for f in agent_files:
    a, _ = frontmatter(f)
    rel = f.relative_to(ROOT)
    for key in ("name", "description"):
        if not a.get(key):
            errors.append(f"{rel}: falta {key}")
    if ":" in a.get("name", ""):
        errors.append(f"{rel}: name no puede contener ':'")
    if a.get("model") and a["model"] not in VALID_MODELS and not a["model"].startswith("claude-"):
        errors.append(f"{rel}: model inválido '{a['model']}'")
    if a.get("effort") and a["effort"] not in VALID_EFFORT:
        errors.append(f"{rel}: effort inválido '{a['effort']}'")
    if f.parent.name == "agents" and f.parent.parent == ROOT:
        if a.get("name") in names:
            errors.append(f"{rel}: name duplicado '{a['name']}'")
        names.add(a.get("name"))
        if a.get("model") not in {"haiku", "sonnet"}:
            warnings.append(f"{rel}: los subagentes de EcoRun deberían usar haiku o sonnet")

# 3. Manifiestos
try:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as e:
    errors.append(f"Manifiesto inválido: {e}")
else:
    if plugin.get("name") != "ecorun":
        errors.append("plugin.json: name debe ser 'ecorun'")
    entry = next((p for p in market.get("plugins", []) if p.get("name") == "ecorun"), None)
    if not entry:
        errors.append("marketplace.json: falta la entrada 'ecorun'")
    elif entry.get("version") != plugin.get("version"):
        errors.append(f"Versiones distintas: plugin.json {plugin.get('version')} vs marketplace.json {entry.get('version')}")
    if not isinstance(market.get("owner"), dict) or not market["owner"].get("name"):
        errors.append("marketplace.json: owner debe ser un objeto con name")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"[{plugin.get('version')}]" not in changelog:
        errors.append(f"CHANGELOG.md: no tiene entrada para la versión {plugin.get('version')}")

# 4. Evals
evals = SKILL / "evals"
for case in sorted(p for p in evals.iterdir() if p.is_dir() and p.name != "results") if evals.exists() else []:
    rel = case.relative_to(ROOT)
    if not (case / "prompt.md").exists():
        errors.append(f"{rel}: falta prompt.md")
    if not (case / "case.yaml").exists():
        errors.append(f"{rel}: falta case.yaml")
    elif f"name: {case.name}" not in (case / "case.yaml").read_text(encoding="utf-8"):
        errors.append(f"{rel}/case.yaml: name debe ser '{case.name}'")
    if not list((case / "graders").glob("*.md")):
        errors.append(f"{rel}: necesita al menos un archivo en graders/")

for w in warnings:
    print(f"ADVERTENCIA  {w}")
for e in errors:
    print(f"ERROR        {e}")
print(f"\n{len(errors)} errores, {len(warnings)} advertencias")
sys.exit(1 if errors else 0)
