import logging
from a_platform.g_agents.a_base.a_base_agent import BaseAgent
from a_platform.j_llm_gateway.d_gateway import LLMGateway
from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
from a_platform.g_agents.a_base.a_base_agent import BaseAgent
from a_platform.e_skills.h_registry.a_skill_registry import SkillRegistry
from a_platform.g_agents.e_data.a_data_agent import DataAgent
from a_platform.g_agents.f_database.a_database_agent import DatabaseAgent
from a_platform.g_agents.g_analytics.a_analytics_agent import AnalyticsAgent
from a_platform.g_agents.h_testing.a_testing_agent import TestingAgent
from a_platform.g_agents.i_documentation.a_documentation_agent import DocumentationAgent
from a_platform.g_agents.j_backend.a_backend_agent import BackendAgent
from a_platform.g_agents.k_frontend.a_frontend_agent import FrontendAgent
from a_platform.g_agents.l_chatbot.a_chatbot_agent import ChatbotAgent
from a_platform.g_agents.m_infrastructure.a_infrastructure_agent import InfrastructureAgent

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
            if "dataagent" in name_lower or "data_agent" in name_lower or "data_engineer" in name_lower:
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
