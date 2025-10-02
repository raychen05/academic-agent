from prompt_toolkit import prompt
from services.llm_helpers import call_llm



def summarize_citation_growth(paper_title, growth_data):
    """
    paper_title: str - title of the paper
    growth_data: dict - {
        "annual_citations": {2019: 3, 2020: 8, 2021: 14, 2022: 22, 2023: 40},
        "forecast": {2024: 55, 2025: 73}
    }
    """

    prompt = f"""
You are an expert in bibliometrics and research analytics.
Analyze the citation growth of the paper titled "{paper_title}".

Citation history by year:
{growth_data["annual_citations"]}

Forecast (based on statistical modeling):
{growth_data["forecast"]}

Tasks:
1. Summarize the growth trend (is it accelerating, steady, or declining?).
2. Comment on the likely reasons for this pattern (field trends, novelty, collaborations, etc.).
3. Mention the forecast explicitly and what it suggests for the paper’s influence.

Be concise (max 4 sentences) but informative. Avoid generic statements.
    """
    return call_llm(prompt)