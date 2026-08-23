import logging
import json
import re
from typing import Dict, Any, List

from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.e_mcp.mcp_executor import MCPExecutor
from a_platform.d_skills.skill_registry import SkillRegistry
from a_platform.a_core.b_domain.project_plan import Task
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.d_skills.skill_contract import CORE_SKILL_CONTRACTS

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
        
        # 1. Preparar contexto base (Brain + Plan)
        base_context = {
            "domain": request.discovery_data.get("domain", "generic"),
            "architecture": request.architecture_decision,
            "task_description": task.description,
            "dataset_path": request.dataset_path,
            "database_technology": request.architecture_decision.get("database_technology", "PostgreSQL") if request.architecture_decision else "PostgreSQL",
            "data_processing_tool": request.architecture_decision.get("data_processing", "Pandas") if request.architecture_decision else "Pandas",
            "target_table": "main_table",
            "script_name": f"{self.name}_output.py",
            "schema_definition": "CREATE TABLE auto_generated (id INT);"
        }
        
        # 2. Chamar Skills requeridas preenchendo contratos
        for skill_name in task.skills:
            if skill_name in CORE_SKILL_CONTRACTS:
                contract = CORE_SKILL_CONTRACTS[skill_name]
                
                # Se faltar algum input vital, poderíamos invocar o LLM para preencher. 
                # Para manter estabilidade, geramos via LLM uma extração dos inputs se necessário.
                missing = [r for r in contract.required_inputs if r not in base_context]
                if missing:
                    logger.warning(f"[{self.name}] Faltam inputs para a skill {skill_name}: {missing}. LLM tentará inferir.")
                    system_prompt = f"Gere um JSON preenchendo os seguintes campos: {missing} baseando-se no contexto."
                    prompt = f"Task: {task.description}\nArch: {json.dumps(base_context['architecture'])}"
                    resp = self.gateway.generate_text(prompt, system_prompt=system_prompt)
                    if resp.get("success"):
                        try:
                            text = resp.get("text", "")
                            match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
                            if match:
                                text = match.group(1).strip()
                            inferred = json.loads(text)
                            base_context.update(inferred)
                        except:
                            pass
                
            res = self.skills.run_skill(skill_name, base_context)
            if res.get("success"):
                art_name = res.get("artifact", "unknown.txt")
                content = res.get("content", "")
                artifacts.append(Artifact(name=art_name, content=content, type="skill_output", metadata={"generator": "skill", "skill_name": skill_name}))
                logger.info(f"[{self.name}] Skill {skill_name} gerou artefato {art_name}")
            else:
                logger.warning(f"[{self.name}] Falha na skill {skill_name}: {res.get('error')}")

        # 3. Invocar LLM para gerar código complementar (se houver expected_artifacts que não foram gerados)
        generated_files = [a.name for a in artifacts]
        missing_artifacts = [ea for ea in task.expected_artifacts if ea not in generated_files]
        
        for art in missing_artifacts:
            prompt = f"Gere código final para {task.name} no contexto de {base_context['architecture'].get('architecture_pattern')}\nDeve produzir o arquivo: {art}"
            llm_resp = self.gateway.generate_text(prompt, system_prompt=f"Você é o {self.name}", model_preference="openai")
            if llm_resp.get("success"):
                content = llm_resp.get("text")
                artifacts.append(Artifact(name=art, content=content, type="source_code", metadata={"generator": "llm", "agent_name": self.name}))
            else:
                logger.error(f"[{self.name}] Erro no LLM para {art}: {llm_resp.get('error')}")

        logger.info(f"[{self.name}] Task {task.name} concluída. {len(artifacts)} artefatos gerados.")
        return artifacts
