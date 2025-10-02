# src/normalizer/entity_types/journals.py
from .base import BaseNormalizer
class JournalNormalizer(BaseNormalizer):
    def __init__(self, catalog_path="data/catalo gs/journals.csv"):
        super().__init__("journals", catalog_path)
