# src/normalizer/rules/normalize_rules.py
import csv, json
from .token_maps import *
from ..utils_text import normalize_text

def apply_alias_map(name: str, alias_csv: str) -> str | None:
    n = normalize_text(name)
    with open(alias_csv) as f:
        for row in csv.reader(f):
            alias, canonical = row
            if normalize_text(alias) == n:
                return canonical
    return None

def expand_abbrev(tokens: list[str], common_json: str) -> list[str]:
    maps = json.load(open(common_json))
    return [maps.get(t, t) for t in tokens]
