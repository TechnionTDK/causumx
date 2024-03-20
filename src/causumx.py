class CauSumX:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def get_explanation(self, query, size_constraint):
        # Mock explanation data
        explanation = {
            "summary": "Mock explanation for the query on dataset " + self.dataset_name,
            "details": [
                {"cause": "Factor A", "effect": "10% increase"},
                {"cause": "Factor B", "effect": "5% decrease"},
            ],
            "query": query,
            "size_constraint": size_constraint
        }
        return explanation
