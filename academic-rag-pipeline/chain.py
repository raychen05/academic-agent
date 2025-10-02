from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from parser import parser

llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = PromptTemplate(
    template="""
You are a research assistant. Extract the following structured fields from the academic paper:

- Title, Year, Authors, Affiliations
- Research Objective
- Method
- Key Results
- Datasets
- Models or Tools
- Contributions / Novelty
- Comparison to Prior Work
- Evaluation Metrics
- Limitations
- Application Domain
- Paper Type
- Code/Data Link
- Citation Count
- Keywords
- Related Papers
- Lay Summary

Return as JSON with this format:
{format_instructions}

--- Paper Start ---
Title: {paper_title}
Abstract: {paper_abstract}
--- Paper End ---
""",
    input_variables=["paper_title", "paper_abstract"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)
