# src/normalizer/utils_text.py
import re, unicodedata

PUNCT_RE = re.compile(r"[^\w\s]")
WS_RE = re.compile(r"\s+")

def norm_unicode(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()

def normalize_text(s: str) -> str:
    s = norm_unicode(s.lower())
    s = PUNCT_RE.sub(" ", s)
    s = WS_RE.sub(" ", s).strip()
    return s
