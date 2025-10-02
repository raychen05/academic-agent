# src/cli/normalize.py
import sys, csv, json
from normalizer.pipeline import NormalizationPipeline

if __name__ == "__main__":
    pipe = NormalizationPipeline()
    rdr = csv.DictReader(sys.stdin)
    wtr = csv.DictWriter(sys.stdout, fieldnames=["entity_type","input","id","name","score"])
    wtr.writeheader()
    for row in rdr:
        out = pipe.normalize(row["entity_type"], row["input"], json.loads(row.get("context","{}")))
        wtr.writerow({"entity_type": row["entity_type"], "input": row["input"],
                      "id": out.get("id"), "name": out.get("name"), "score": out.get("score", 0.0)})


### Example usage:
# cat inputs.csv | python -m src.cli.normalize > outputs.csv