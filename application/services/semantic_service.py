class SemanticService:

    def __init__(self, semantic_repository):
        self.semantic_repository = semantic_repository

    def get_status(self):
        return self.semantic_repository.get_graph_status()

    def get_risk(self, code: str):
        return self.semantic_repository.find_risk(code)

    def get_critical_risks(self):
        return (
            self.semantic_repository
            .find_critical_risks()
        )
