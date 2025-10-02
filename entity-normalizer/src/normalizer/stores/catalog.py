# src/normalizer/stores/catalog.py
import pandas as pd
from pathlib import Path

class Catalog:
    def __init__(self, path_csv: str, key_cols=("id","name")):
        self.df = pd.read_csv(path_csv)
        self.df["name_norm"] = self.df["name"].str.lower()
        self.names = self.df["name"].tolist()

    def row_by_name(self, name: str) -> dict | None:
        hit = self.df[self.df["name"] == name]
        return None if hit.empty else hit.iloc[0].to_dict()


import pandas as pd

class Catalog2:
    def __init__(self, path: str, name_col="name"):
        self.df = pd.read_csv(path)
        self.df[name_col] = self.df[name_col].astype(str)
        self.name_col = name_col
        self.names = self.df[name_col].tolist()

    def by_name(self, name: str) -> dict | None:
        hit = self.df[self.df[self.name_col] == name]
        return None if hit.empty else hit.iloc[0].to_dict()

    def by_id(self, _id) -> dict | None:
        hit = self.df[self.df["id"] == _id]
        return None if hit.empty else hit.iloc[0].to_dict()
