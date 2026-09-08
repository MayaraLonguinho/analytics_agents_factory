import json
import asyncio
from typing import Dict, Any, List
from a_core.b_domain.project import DiscoveryResult
from a_core.b_domain.architecture import ArchitectureDecision
from a_platform.g_llm_gateway.gateway import LLMGateway

class ArchitectureAgent:
    """Agent responsible for determining the technological stack based on context."""
    
    def __init__(self, gateway: LLMGateway):
        self.gateway = gateway

    def decide_sync(self, discovery: DiscoveryResult, dataset_profile: Dict[str, Any], rules: List[Any], patterns: List[Any]) -> ArchitectureDecision:
        """Synchronous wrapper for the LLM decision."""
        return asyncio.run(self.decide(discovery, dataset_profile, rules, patterns))
        
    async def decide(self, discovery: DiscoveryResult, dataset_profile: Dict[str, Any], rules: List[Any], patterns: List[Any]) -> ArchitectureDecision:
        """Determines the architecture stack based on inputs using the LLM Gateway."""
        
        schema = {
            "type": "object",
            "properties": {
                "frontend": {"type": "string"},
                "backend": {"type": "string"},
                "database": {"type": "string"},
                "data_pipeline": {"type": "string"},
                "infrastructure": {"type": "string"},
                "authentication": {"type": "string"},
                "testing": {"type": "string"},
                "documentation": {"type": "string"},
                "rationale": {"type": "string"}
            },
            "required": ["frontend", "backend", "database", "data_pipeline", "infrastructure", "authentication", "testing", "documentation", "rationale"]
        }
        
        prompt = f"""
        You are an expert Architecture Agent. Your task is to determine the best technology stack based on the provided inputs.
        DO NOT invent technologies. Respect the user preferences, rules, and patterns.

        Project Objective: {discovery.project_objective}
        Domain: {discovery.domain}
        
        User Answers: {json.dumps(discovery.decisions)}
        Dataset Profile: {json.dumps(dataset_profile)}
        
        Applicable Rules: {rules}
        Applicable Patterns: {patterns}
        
        Return the structured JSON containing the selected technologies and a brief rationale.
        """
        
        # Use default provider/model or a robust one for reasoning
        # For tests, we might use openai gpt-4o or claude-3-5-sonnet if available in gateway. 
        # But we'll rely on gateway's default.
        response = await self.gateway.structured_output(prompt=prompt, schema=schema)
        
        if isinstance(response.content, dict):
            content = response.content
        else:
            try:
                content = json.loads(response.content)
            except:
                content = {}
                
        return ArchitectureDecision(
            frontend=content.get("frontend", discovery.decisions.get("frontend", "React")),
            backend=content.get("backend", discovery.decisions.get("backend", "FastAPI")),
            database=content.get("database", discovery.decisions.get("database", "PostgreSQL")),
            data_pipeline=content.get("data_pipeline", discovery.decisions.get("etl", "None")),
            infrastructure=content.get("infrastructure", discovery.decisions.get("infrastructure", "Docker")),
            authentication=content.get("authentication", discovery.decisions.get("authentication", "JWT")),
            testing=content.get("testing", discovery.decisions.get("testing", "pytest")),
            documentation=content.get("documentation", discovery.decisions.get("documentation", "README")),
            rationale=content.get("rationale", "Derived from defaults due to parsing failure.")
        )
