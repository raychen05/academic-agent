# tests/test_experiment_aggregator.py
import pytest
from tools.experiment_aggregator import ExperimentAggregator

def test_list_experiments():
    agg = ExperimentAggregator()
    exps = agg.list_experiments("Genomics")
    assert any("Genomics" in exp["dataset"] for exp in exps)

def test_aggregate_summary():
    agg = ExperimentAggregator()
    summary = agg.aggregate_summary("Genomics")
    assert summary["num_experiments"] >= 1
    assert "methods" in summary and isinstance(summary["methods"], list)