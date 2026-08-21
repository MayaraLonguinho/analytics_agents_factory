class Questionnaire:
    def get_questions_for_domain(self, domain: str) -> list[str]:
        if domain == "finance":
            return ["What is the currency?", "How often is data updated?"]
        return ["What is the primary data source?"]
