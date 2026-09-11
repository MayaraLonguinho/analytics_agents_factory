class Questionnaire:
    def get_questions_for_domain(self, business_context: str) -> list[str]:
        if business_context == "finance":
            return ["What is the currency?", "How often is data updated?"]
        return ["What is the primary data source?"]
