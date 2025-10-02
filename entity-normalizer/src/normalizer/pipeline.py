# src/normalizer/pipeline.py
from .entity_types.journals import JournalNormalizer
from .entity_types.organizations import OrganizationNormalizer
from .entity_types.countries import CountryNormalizer
from .entity_types.funders import FunderNormalizer
from .entity_types.topics import TopicNormalizer

class NormalizationPipeline:
    def __init__(self):
        self.journals = JournalNormalizer()
        self.orgs = OrganizationNormalizer()
        self.countries = CountryNormalizer()
        self.funders = FunderNormalizer()
        self.topics = TopicNormalizer()

    def normalize(self, entity_type: str, text: str, ctx: dict | None = None):
        n = getattr(self, {
            "journal":"journals","journals":"journals",
            "organization":"orgs","org":"orgs","organizations":"orgs",
            "country":"countries","countries":"countries",
            "funder":"funders","funders":"funders",
            "topic":"topics","topics":"topics",
        }[entity_type])
        return n.normalize(text, ctx or {})
