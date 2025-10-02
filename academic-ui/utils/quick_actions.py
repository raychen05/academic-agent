from utils.llm_helpers import call_llm
from utils.citation_utils import  get_cited_paper_ids, get_citing_paper_ids
#from utils.semantic_search import retrieve_mock



def retrieve_mock(query, k=5):
    # Predefined mock paper data (simulate the 'papers' list)
    mock_papers = [
        {"title": "Paper 1", "abstract": "Abstract 1"},
        {"title": "Paper 2", "abstract": "Abstract 2"},
        {"title": "Paper 3", "abstract": "Abstract 3"},
        {"title": "Paper 4", "abstract": "Abstract 4"},
        {"title": "Paper 5", "abstract": "Abstract 5"},
        {"title": "Paper 6", "abstract": "Abstract 6"},
    ]
    
    # Return the first `k` papers (simulate a search result)
    return mock_papers[:k]

def ask_ai_to_explain(paper_metadata):
    prompt = f"""
You are an expert academic tutor. Read the following paper abstract and explain its main idea to a graduate student in 3–5 sentences.

Title: {paper_metadata['title']}
Abstract: {paper_metadata['abstract']}
"""
    return call_llm(prompt)


def summarize_paper_en(paper_metadata):
    prompt = f"""
Summarize this academic paper in plain English for a high school student. Avoid jargon.

Title: {paper_metadata['title']}
Abstract: {paper_metadata['abstract']}
"""
    return call_llm(prompt)


def compare_two_papers(paper1, paper2):
    prompt = f"""
    Compare the following two academic papers based on their titles and abstracts. Identify both commonalities and differences in the following aspects:

    1. Research topic or problem area
    2. Methodologies or techniques used
    3. Application domains or datasets
    4. Novel contributions or focus
    5. Any notable differences in experimental approach or scope

    Paper 1:
    Title: {paper1['title']}
    Abstract: {paper1['abstract']}

    Paper 2:
    Title: {paper2['title']}
    Abstract: {paper2['abstract']}

    Provide a structured comparison under each point.
    """

    return call_llm(prompt)


def follow_citation_path_ids(paper_metadata):
    cited_ids = get_cited_paper_ids(paper_metadata['id'])  # external API
    citing_ids = get_citing_paper_ids(paper_metadata['id'])
    return {
        "cited_by": citing_ids[:5],
        "references": cited_ids[:5]
    }

def ask_ai_with_context(paper_metadata):
    related_texts = retrieve_mock(paper_metadata["title"])
    context = "\n".join([doc['text'] for doc in related_texts])
    prompt = f"""
Use the following context to help explain the paper:

Context:
{context}

Paper Title: {paper_metadata['title']}
Paper Abstract: {paper_metadata['abstract']}

Explain this paper in simple language, highlighting its novelty.
"""
    return call_llm(prompt)


def follow_citation_path(paper_metadata):
    prompt = f"""
   Given a paper titled "{paper_metadata['title']}" - "WOS:{paper_metadata['id']}",  and its citing papers, extract and summarize:

- Top 5 research topics among citing papers
- Leading institutions and authors who cited it
- Novel insights or methods introduced by citing papers
- Overall impact trend over time
- Are citations supportive, neutral, or critical?

    """

    return call_llm(prompt)


''' 
- How has the paper influenced specific fields or domains?
- Any emerging trends or shifts in research focus?
- How has the paper's influence evolved over time?
- What are the most common methods or keywords in citing papers?
- How do the citing papers compare in terms of citation patterns?
'''