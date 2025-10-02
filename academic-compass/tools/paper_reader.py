# tools/paper_reader.py - skeleton for context

# Extract sections, explain terms, QA
# Use PDF parsers like PyMuPDF + plug into OpenAI for deeper Q&A


# tools/paper_reader.py
import fitz  # PyMuPDF
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class PaperReader:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def parse_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Splits a PDF into sections by page for simplicity.
        You could improve this with real section headers, regex, or layout analysis.
        """
        doc = fitz.open(pdf_path)
        sections = []
        for page_num, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                sections.append({
                    "page": page_num + 1,
                    "content": text
                })
        return sections

    def extract_terms(self, sections: List[Dict], glossary: List[str]) -> Dict[str, List[str]]:
        """
        Simple terminology matching: finds which glossary terms appear in each section.
        """
        matches = {}
        for term in glossary:
            term_lower = term.lower()
            found_in = []
            for section in sections:
                if term_lower in section["content"].lower():
                    found_in.append(f"Page {section['page']}")
            if found_in:
                matches[term] = found_in
        return matches

    def answer_question(self, question: str, sections: List[Dict]) -> str:
        """
        Basic retrieval-based Q&A:
        - Embed question
        - Embed sections
        - Rank by cosine similarity
        - Return the most relevant section text as the answer
        """
        question_embedding = self.model.encode([question], normalize_embeddings=True)
        section_texts = [s["content"] for s in sections]
        section_embeddings = self.model.encode(section_texts, normalize_embeddings=True)

        import numpy as np
        scores = np.dot(section_embeddings, question_embedding.T).flatten()
        best_idx = np.argmax(scores)

        return f"Most relevant section (Page {sections[best_idx]['page']}):\n\n{sections[best_idx]['content'][:500]}..."