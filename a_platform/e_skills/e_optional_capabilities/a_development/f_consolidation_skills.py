import logging
import re
import asyncio
from typing import Dict, Any
from a_platform.a_core.a_contracts.b_skill_contract import BaseSkill, SkillContract, CORE_SKILL_CONTRACTS
from a_platform.g_llm_gateway.e_gateway import LLMGateway

logger = logging.getLogger(__name__)

class LLMGeneratedSkill(BaseSkill):
    """Implementação real baseada em LLM para habilidades sob demanda."""
    def __init__(self, skill_id: str, extension: str, role_prompt: str):
        super().__init__()
        self.skill_id = skill_id
        self.extension = extension
        self.role_prompt = role_prompt
        self.llm = LLMGateway()

    def get_contract(self) -> SkillContract:
        return CORE_SKILL_CONTRACTS[self.skill_id]

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        contract = self.get_contract()
        description = input_data.get("task_description", contract.description)
        project_plan = input_data.get("project_plan", {})
        
        system_prompt = (
            f"Você é um engenheiro sênior. O seu papel é: {self.role_prompt}\n"
            f"Responda SOMENTE com o código/texto final do artefato. "
            f"Não inclua texto ao redor. Não use formatação markdown como ``` no início ou no fim, "
            f"apenas retorne o conteúdo puro."
        )

        user_prompt = f"Gere o conteúdo completo para a habilidade '{contract.name}'.\nDescrição: {description}\nContexto: {input_data}\nPlan: {project_plan}"

        llm_response = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        if not llm_response.content:
            error_msg = f"LLM Generation Failed para {self.skill_id}"
            logger.error(f"[{self.__class__.__name__}] {error_msg}")
            raise ValueError(error_msg)
            
        code_text = llm_response.content
        code_text = re.sub(r'^```[\w]*\n', '', code_text, flags=re.MULTILINE)
        code_text = re.sub(r'```$', '', code_text, flags=re.MULTILINE).strip()
        
        artifact_name = f"{self.skill_id}_output.{self.extension}"
        if self.skill_id == "documentation":
            artifact_name = "README.md"
        elif self.skill_id == "docker":
            artifact_name = "docker-compose.yml"
            
        return {
            artifact_name: code_text
        }

class CleaningSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("cleaning", "py", "Engenheiro de Dados focado em limpeza de dataframes Pandas/Spark.")

class DeduplicationSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("deduplication", "py", "Engenheiro de Dados focado em deduplicação e qualidade.")

class CategorizationSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("categorization", "py", "Engenheiro de Analytics focado em agrupar e classificar entidades.")

class AnalyticsSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("analytics", "sql", "Engenheiro de Analytics construindo views e tabelas analíticas complexas.")

class DashboardSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("dashboard", "py", "Desenvolvedor de Frontend focado em Streamlit/Dash.")

class ChatbotSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("chatbot", "py", "AI Engineer desenvolvendo chatbots com LangChain e LLMs.")

class BackendSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("backend", "py", "Engenheiro de Backend desenvolvendo APIs com FastAPI/Flask.")

class FrontendSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("frontend", "jsx", "Desenvolvedor React desenvolvendo componentes e UIs complexas.")

class TestingSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("testing", "py", "Engenheiro de QA criando testes unitários exaustivos com pytest.")

class DocumentationSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("documentation", "md", "Technical Writer criando documentação impecável em Markdown.")

class DockerSkill(LLMGeneratedSkill):
    def __init__(self): super().__init__("docker", "yml", "Engenheiro DevOps criando receitas Docker e docker-compose.yml.")
