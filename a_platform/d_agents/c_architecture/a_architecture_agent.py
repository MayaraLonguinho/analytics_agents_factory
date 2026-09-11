import json
import asyncio
from typing import Dict, Any, List
from a_platform.a_core.b_domain.g_project_request import ProjectRequest
from a_platform.g_llm_gateway.e_gateway import LLMGateway

class ArchitectureAgent:
    """Agent responsible for determining the technological stack based on context."""
    
    def __init__(self, gateway: LLMGateway):
        self.gateway = gateway

    def generate_architecture(self, request: ProjectRequest) -> bool:
        """Synchronous wrapper for the LLM decision."""
        return asyncio.run(self._generate_architecture_async(request))
        
    async def _generate_architecture_async(self, request: ProjectRequest) -> bool:
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
            "required": ["rationale"]
        }
        
        prompt = f"""
        You are an expert Architecture Agent. Your task is to determine the best technology stack based on the provided inputs.
        DO NOT invent technologies. Respect the user preferences, rules, and patterns.
        CRITICAL RULE: For data_engineering or analytics, DO NOT assume frontend, backend, or authentication unless explicitly demanded in discovery_data. Omit them if not requested.

        Project Type: {request.project_type}
        Business Context: {request.business_context}
        Domain: {request.domain}
        
        Discovery Data: {json.dumps(request.discovery_data)}
        Dataset Profile: {json.dumps(request.dataset_profile)}
        
        Brain Context: {json.dumps(request.brain_context)}
        
        Return the structured JSON containing the selected technologies and a brief rationale.
        """
        
        response = await self.gateway.structured_output(prompt=prompt, schema=schema)
        
        if not response or not getattr(response, "content", None):
            return False
            
        if isinstance(response.content, dict):
            content = response.content
        else:
            try:
                content = json.loads(response.content)
            except:
                return False
                
        request.architecture_decision = {k: v for k, v in content.items() if v}
        
        tech_fields = [k for k in request.architecture_decision if k != "rationale"]
        if not tech_fields:
            return False
            
        return True
