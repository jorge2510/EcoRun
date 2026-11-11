#!/usr/bin/env python3
"""Empaqueta la skill en dist/ecorun.zip para subirla a claude.ai o Cowork.

El ZIP contiene una carpeta 'ecorun/' (debe coincidir con el name de la skill)
con SKILL.md, references/ y el LICENSE del repositorio. Los casos de prueba
(evals/) no se incluyen.

Uso: python3 scripts/build.py
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ecorun"
OUT = ROOT / "dist" / "ecorun.zip"
EXCLUDE = {"evals", "__pycache__", ".DS_Store"}

OUT.parent.mkdir(exist_ok=True)
files = sorted(
    p for p in SKILL.rglob("*")
    if p.is_file() and not any(part in EXCLUDE for part in p.relative_to(SKILL).parts)
)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for p in files:
        info = zipfile.ZipInfo(f"ecorun/{p.relative_to(SKILL).as_posix()}", date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, p.read_bytes())
        print(f"  + ecorun/{p.relative_to(SKILL).as_posix()}")
    info = zipfile.ZipInfo("ecorun/LICENSE", date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, (ROOT / "LICENSE").read_bytes())
    print("  + ecorun/LICENSE")
print(f"Listo: {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
