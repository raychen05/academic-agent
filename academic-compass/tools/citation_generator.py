from typing import Dict

class CitationGenerator:
    def __init__(self):
        pass

    def generate_bibtex(self, metadata: Dict) -> str:
        """
        Generate a BibTeX entry for an article.
        """
        entry = "@article{{\n".format()
        entry += f"  author = {{{' and '.join(metadata.get('authors', []))}}},\n"
        entry += f"  title = {{{metadata.get('title', '')}}},\n"
        entry += f"  journal = {{{metadata.get('journal', '')}}},\n"
        entry += f"  year = {{{metadata.get('year', '')}}},\n"

        if metadata.get("volume"):
            entry += f"  volume = {{{metadata['volume']}}},\n"
        if metadata.get("number"):
            entry += f"  number = {{{metadata['number']}}},\n"
        if metadata.get("pages"):
            entry += f"  pages = {{{metadata['pages']}}},\n"
        if metadata.get("doi"):
            entry += f"  doi = {{{metadata['doi']}}},\n"

        entry = entry.rstrip(",\n") + "\n}\n"
        return entry

    def generate_apa(self, metadata: Dict) -> str:
        """
        Generate an APA-style citation.
        """
        authors = metadata.get("authors", [])
        authors_str = ", ".join(authors)
        title = metadata.get("title", "")
        journal = metadata.get("journal", "")
        year = metadata.get("year", "")
        volume = metadata.get("volume", "")
        pages = metadata.get("pages", "")

        citation = f"{authors_str} ({year}). {title}. {journal}"
        if volume:
            citation += f", {volume}"
        if pages:
            citation += f", {pages}"
        citation += "."

        return citation

    def generate_mla(self, metadata: Dict) -> str:
        """
        Generate an MLA-style citation.
        """
        authors = metadata.get("authors", [])
        authors_str = ", and ".join(authors)
        title = metadata.get("title", "")
        journal = metadata.get("journal", "")
        year = metadata.get("year", "")
        volume = metadata.get("volume", "")
        number = metadata.get("number", "")
        pages = metadata.get("pages", "")

        citation = f"{authors_str}. \"{title}.\" {journal}"
        if volume:
            citation += f", vol. {volume}"
        if number:
            citation += f", no. {number}"
        if year:
            citation += f", {year}"
        if pages:
            citation += f", pp. {pages}"
        citation += "."

        return citation
    

    def fetch_metadata_from_doi(self, doi: str) -> dict:
        """
        Use Crossref API to get basic metadata for a given DOI.
        """
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"DOI lookup failed with status {response.status_code}")

        data = response.json()
        item = data["message"]

        authors = []
        for author in item.get("author", []):
            name_parts = []
            if "given" in author:
                name_parts.append(author["given"])
            if "family" in author:
                name_parts.append(author["family"])
            authors.append(" ".join(name_parts))

        metadata = {
            "authors": authors,
            "title": item.get("title", [""])[0],
            "journal": item.get("container-title", [""])[0],
            "year": item.get("published-print", {}).get("date-parts", [[None]])[0][0] or "",
            "volume": item.get("volume", ""),
            "number": item.get("issue", ""),
            "pages": item.get("page", ""),
            "doi": doi
        }
