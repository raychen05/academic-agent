from pydantic import BaseModel, Field
from typing import List, Optional
from langchain.output_parsers import PydanticOutputParser

class AcademicPaperSummary(BaseModel):
    title: str
    year: Optional[str]
    authors: List[str]
    affiliations: List[str]
    objective: str
    method: str
    results: str
    datasets: List[str]
    models_or_tools: List[str]
    contributions: str
    comparison_to_prior_work: str
    evaluation_metrics: List[str]
    limitations: str
    application_domain: str
    paper_type: str
    code_or_data_link: Optional[str]
    citation_count: Optional[int]
    keywords: List[str]
    related_papers: List[str]
    lay_summary: str

parser = PydanticOutputParser(pydantic_object=AcademicPaperSummary)
