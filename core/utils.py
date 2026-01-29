# core/utils.py
import json
from pathlib import Path

def load_config(path_or_file):
    p = Path(path_or_file)
    if p.is_file():
        with open(p) as f:
            return json.load(f)
    raise FileNotFoundError(f"Config not found: {p}")

def ensure_dirs(p):
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)


