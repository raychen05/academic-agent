# tests/test_impact_eval.py
import pytest
from tools.impact_eval import ImpactEvaluator

def test_impact_evaluator_metrics():
    evaluator = ImpactEvaluator()
    result = evaluator.evaluate()

    assert result["h_index"] == 2  # Paper C(25), A(10), B(5), D(2) → h-index = 2
    assert result["total_citations"] == 42
    assert isinstance(result["average_altmetric"], float)
    assert result["average_altmetric"] > 0