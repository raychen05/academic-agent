# paper_quality_estimator.py

from typing import List, Dict, Optional

class PaperQualityEstimator:
    """
    Estimates paper quality and flags retractions or suspicious signals.
    """

    def __init__(self, retraction_list: Optional[List[str]] = None, blacklisted_journals: Optional[List[str]] = None):
        """
        :param retraction_list: List of known retracted DOIs
        :param blacklisted_journals: List of known predatory or blacklisted journals
        """
        self.retraction_list = retraction_list or []
        self.blacklisted_journals = blacklisted_journals or []

    def check_retraction(self, doi: str) -> bool:
        """
        Checks if the paper DOI is in the retraction list.
        """
        return doi.lower() in [d.lower() for d in self.retraction_list]

    def basic_quality_checks(self, paper: Dict) -> Dict:
        """
        Basic checks: low citation count, shady journal, suspicious language.
        """
        warnings = []

        if self.check_retraction(paper.get("doi", "")):
            warnings.append("🚨 This paper is RETRACTED.")

        # Check blacklisted journal
        journal = paper.get("journal", "").lower()
        if any(journal == b.lower() for b in self.blacklisted_journals):
            warnings.append(f"⚠️ Published in blacklisted journal: {paper['journal']}.")

        # Check citation count
        citations = paper.get("citation_count", 0)
        if citations < 5:
            warnings.append("⚠️ Very low citation count — may indicate limited impact or visibility.")

        # Check for suspicious language in abstract
        abstract = paper.get("abstract", "").lower()
        suspicious_phrases = ["fake results", "pseudo", "hoax", "bogus"]
        if any(phrase in abstract for phrase in suspicious_phrases):
            warnings.append("⚠️ Suspicious language found in abstract.")

        return {
            "doi": paper.get("doi"),
            "title": paper.get("title"),
            "quality_warnings": warnings or ["✅ No major issues detected."]
        }

    def analyze_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        Run checks for multiple papers.
        """
        return [self.basic_quality_checks(p) for p in papers]