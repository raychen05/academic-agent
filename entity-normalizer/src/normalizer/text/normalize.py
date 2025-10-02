import re, unicodedata

_PUNCT = re.compile(r"[^\w\s]")
_WS = re.compile(r"\s+")

def nfkd_ascii(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()

def basic_clean(s: str) -> str:
    s = nfkd_ascii(s.lower())
    s = _PUNCT.sub(" ", s)
    s = _WS.sub(" ", s).strip()
    return s

NOISE_ORG = ("department of","school of","faculty of","lab","laboratory","college of")
def strip_org_noise(s: str) -> str:
    t = s
    for n in NOISE_ORG:
        t = t.replace(n, " ")
    return _WS.sub(" ", t).strip()
