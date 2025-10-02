import re
from typing import List, Optional

class NameNormalizer:
    def __init__(self, stopwords: Optional[List[str]] = None):
        self.synonym_map = {
            "univ": "university",
            "inst": "institute",
            "dept": "department",
            "tech": "technology",
            "sci": "science",
            "natl": "national",
            "ctr": "center",
            "lab": "laboratory",
        }

        self.stopwords = set(stopwords or [])

        # Precompile regex
        self.special_char_pattern = re.compile(r"[^a-z0-9\s]")  # keep alphanumeric and spaces
        self.multiple_spaces_pattern = re.compile(r"\s+")

    def normalize(self, text: str) -> str:
        # 1. Lowercase
        text = text.lower()

        # 2. Remove special characters
        text = self.special_char_pattern.sub(" ", text)

        # 3. Replace multiple spaces with one
        text = self.multiple_spaces_pattern.sub(" ", text).strip()

        # 4. Tokenize
        tokens = text.split()

        # 5. Replace synonyms
        tokens = [self.synonym_map.get(token, token) for token in tokens]

        # 6. Remove stopwords if enabled
        if self.stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]

        # 7. Return normalized string
        return " ".join(tokens)