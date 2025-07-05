from app.core.config import settings


class ClinicalTrialRetriever:
    def __init__(self) -> None:
        self.chroma_collection = settings.chroma_collection

    def retrieve(self, query: str, n_results: int = 5) -> list:
        results = self.chroma_collection.query(
            query_texts=[query],
            n_results=n_results,
        )
        return results
