from ols_client import EBIClient


class Annotator:
    def __init__(self):
        self.ebi_client = EBIClient()

    def run(self, text):
        """get SNOMED annotations for term"""
        return self.ebi_client.search(query=text, params={"ontology": "snomed"})
