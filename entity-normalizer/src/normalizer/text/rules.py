from .normalize import basic_clean

ALIAS_MAP = {
  # fast path exacts; extend with CSV loader
  "mit": "Massachusetts Institute of Technology",
  "uc berkeley": "University of California, Berkeley",
  "pnas": "Proceedings of the National Academy of Sciences of the United States of America",
  "nih": "National Institutes of Health",
  "nsf": "National Science Foundation",
  "uk": "United Kingdom",
}

def alias_expand(s: str) -> str | None:
    key = basic_clean(s)
    return ALIAS_MAP.get(key)
