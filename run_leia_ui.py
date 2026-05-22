#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_leia_ui.py — Point d'entrée de Leia V19
"""
import sys
import os

# ── Racine du projet ──────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Tous les sous-modules dans sys.path ──────────────────────────────────────
_LEIA_MODULES = [
    "Interface",
    "Cerveau",
    "Coeur",
    "Cognition",
    "Conscience",
    "Initiative",
    "Memory",
    "Parler",
    "Soi_Leia",
    "Connaissance",
]

for _folder in _LEIA_MODULES:
    _path = os.path.join(ROOT, _folder)
    if os.path.isdir(_path) and _path not in sys.path:
        sys.path.insert(0, _path)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Patch chemins global ──────────────────────────────────────────────────────
try:
    import leia_path_patch  # noqa
except Exception:
    pass

# ── Patch injection données de livre dans le payload ─────────────────────────
try:
    import leia_book_patch  # noqa
except Exception as e:
    print(f"[WARN] leia_book_patch non chargé: {e}")

# ── Lancer l'interface ────────────────────────────────────────────────────────
from leia_complete_interface import main

if __name__ == "__main__":
    main()
