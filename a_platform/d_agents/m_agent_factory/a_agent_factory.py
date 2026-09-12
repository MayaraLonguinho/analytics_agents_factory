import logging
from a_platform.d_agents.p_base.a_base_agent import BaseAgent
from a_platform.g_llm_gateway.e_gateway import LLMGateway
from a_platform.f_mcp.e_executor.a_executor import MCPExecutor
from a_platform.e_skills.j_skill_registry import SkillRegistry
from a_platform.d_agents.k_specialized_agents import (
    DataAgent, DatabaseAgent, AnalyticsAgent, TestingAgent, InfrastructureAgent,
    BackendAgent, FrontendAgent, DocumentationAgent, ChatbotAgent
)

logger = logging.getLogger(__name__)

class AgentFactory:
    """
    Fábrica que instancia agentes baseados no nome da task.
    """
    def __init__(self):
        self.gateway = LLMGateway()
        self.mcp = MCPExecutor()
        self.skills = SkillRegistry()
        self._cache = {}

    def get_agent(self, agent_name: str) -> BaseAgent:
        if agent_name not in self._cache:
            logger.info(f"[AgentFactory] Instanciando novo agente: {agent_name}")
            
            agent_class = BaseAgent
            name_lower = agent_name.lower()
            if "data_agent" in name_lower or "data_engineer" in name_lower:
                agent_class = DataAgent
            elif "database" in name_lower:
                agent_class = DatabaseAgent
            elif "analytic" in name_lower:
                agent_class = AnalyticsAgent
            elif "test" in name_lower:
                agent_class = TestingAgent
            elif "infra" in name_lower:
                agent_class = InfrastructureAgent
            elif "backend" in name_lower:
                agent_class = BackendAgent
            elif "frontend" in name_lower:
                agent_class = FrontendAgent
            elif "doc" in name_lower:
                agent_class = DocumentationAgent
            elif "chat" in name_lower:
                agent_class = ChatbotAgent
                
            self._cache[agent_name] = agent_class(
                name=agent_name,
                gateway=self.gateway,
                mcp=self.mcp,
                skills=self.skills
            )
        return self._cache[agent_name]
