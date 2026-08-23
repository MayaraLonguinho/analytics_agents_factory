import logging
from typing import Dict, Any, List

from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.e_mcp.mcp_executor import MCPExecutor
from a_platform.d_skills.skill_registry import SkillRegistry
from a_platform.a_core.b_domain.project_plan import Task
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, gateway: LLMGateway, mcp: MCPExecutor, skills: SkillRegistry):
        self.name = name
        self.gateway = gateway
        self.mcp = mcp
        self.skills = skills

    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Iniciando task: {task.name}")
        artifacts = []
        
        # 1. Preparar contexto (Brain + Plan)
        context = {
            "domain": request.discovery_data.get("domain", "generic"),
            "architecture": request.architecture_decision,
            "task_description": task.description
        }
        
        # 2. Chamar Skills requeridas
        for skill_name in task.skills:
            res = self.skills.run_skill(skill_name, context)
            if res.get("success"):
                art_name = res.get("artifact", "unknown.txt")
                content = res.get("content", "")
                artifacts.append(Artifact(name=art_name, content=content, type="skill_output", metadata={"generator": "skill", "skill_name": skill_name}))
                logger.info(f"[{self.name}] Skill {skill_name} gerou artefato {art_name}")
            else:
                logger.warning(f"[{self.name}] Falha na skill {skill_name}: {res.get('error')}")

        # 3. Invocar LLM para complementar lógica se necessário
        prompt = f"Gere código base para {task.name} no contexto de {context['architecture'].get('architecture_pattern')}"
        llm_resp = self.gateway.generate_text(prompt, system_prompt=f"Você é o {self.name}", model_preference="openai")
        if llm_resp.get("success"):
            art_name = f"{self.name}_output.py"
            content = llm_resp.get("text")
            artifacts.append(Artifact(name=art_name, content=content, type="source_code", metadata={"generator": "llm", "agent_name": self.name}))
        else:
            logger.error(f"[{self.name}] Erro no LLM: {llm_resp.get('error')}")
            # Se LLM falhar, nós decidimos falhar ou retornar os artefatos que temos?
            # Neste caso, vamos apenas logar, a Factory decide.

        logger.info(f"[{self.name}] Task {task.name} concluída. {len(artifacts)} artefatos gerados.")
        return artifacts
