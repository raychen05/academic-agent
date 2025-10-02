import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file) -> str:
    """Extract raw text from a PDF file."""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)

def extract_structured_sections(raw_text: str) -> dict:
    """Extract title, abstract, and full text from raw text."""
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    full_text = "\n".join(lines)

    # Heuristic: title is first non-empty line (can be improved)
    title = lines[0] if lines else ""

    # Heuristic: extract abstract section
    abstract = ""
    abstract_match = re.search(r'(?i)(abstract)\s*[:\-]?\s*(.*?)(?=\n[A-Z][^\n]{0,80}\n)', full_text, re.DOTALL)
    if abstract_match:
        abstract = abstract_match.group(2).strip()

    return {
        "title": title,
        "abstract": abstract,
        "full_text": full_text
    }
