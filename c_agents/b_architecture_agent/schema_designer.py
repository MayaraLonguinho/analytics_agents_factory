class SchemaDesigner:
    def design_star_schema(self, domain: str) -> dict:
        if domain == "finance":
            return {"fact": "fact_transactions", "dimensions": ["dim_account", "dim_date"]}
        return {"fact": "fact_events", "dimensions": ["dim_user", "dim_time"]}
