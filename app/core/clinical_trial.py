from itertools import zip_longest

from app.core.config import settings
from app.models.clinical_trial import ClinicalTrialResult, ClinicalTrialResults


class ClinicalTrialRetriever:
    def __init__(self) -> None:
        self.chroma_collection = settings.chroma_collection

    def __call__(self, query: str, n_results: int = 5) -> ClinicalTrialResults:
        """
        Retrieve clinical trial results for a given query using the default number of results.
        """
        return self.retrieve(query, n_results)

    def retrieve(self, query: str, n_results: int = 5) -> ClinicalTrialResults:
        """
        Retrieve clinical trial results for a given query and number of results.
        """
        results = self.chroma_collection.query(
            query_texts=[query],
            n_results=n_results,
        )
        return self._format_results(results)

    def _format_results(self, results: dict) -> ClinicalTrialResults:
        def flatten(key: str) -> list:
            value = results.get(key, [[]])
            if value and isinstance(value[0], list):
                return value[0]
            ids_len = len(results.get("ids", [[]])[0]) if results.get("ids") else 0
            return [None] * ids_len

        ids = flatten("ids")
        documents = flatten("documents")
        metadatas = flatten("metadatas")
        distances = flatten("distances")
        uris = flatten("uris")

        trials = [
            ClinicalTrialResult(
                id=str(id_) if id_ is not None else "",
                document=doc if doc is not None else "",
                metadata=meta if meta is not None else {},
                distance=dist,
                uri=uri,
            )
            for id_, doc, meta, dist, uri in zip_longest(
                ids, documents, metadatas, distances, uris, fillvalue=None
            )
        ]
        return ClinicalTrialResults(results=trials)
