from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from parser import AcademicPaperSummary  # Pydantic model from earlier
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

parser = PydanticOutputParser(pydantic_object=AcademicPaperSummary)

llm = ChatOpenAI(model="gpt-4", temperature=0)

template = PromptTemplate(
    input_variables=["context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
    template="""
You are an AI academic research assistant. Analyze the provided academic content
and extract structured metadata as follows:

{format_instructions}

Context:
{context}
"""
)

rag_chain = LLMChain(
    llm=llm,
    prompt=template,
    output_parser=parser
)
