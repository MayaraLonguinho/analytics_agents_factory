import logging
from a_platform.c_agents.base_agent import BaseAgent
from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.e_mcp.mcp_executor import MCPExecutor
from a_platform.d_skills.skill_registry import SkillRegistry

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
            self._cache[agent_name] = BaseAgent(
                name=agent_name,
                gateway=self.gateway,
                mcp=self.mcp,
                skills=self.skills
            )
        return self._cache[agent_name]
