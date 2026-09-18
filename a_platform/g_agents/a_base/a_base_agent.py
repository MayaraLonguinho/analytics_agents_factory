import logging
import json
import re
from typing import Dict, Any, List

from a_platform.i_llm_gateway.e_gateway import LLMGateway
from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
from a_platform.e_skills.g_registry.a_skill_registry import SkillRegistry
from a_platform.b_contracts import ProjectTask as ProjectTask
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import Artifact

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, gateway: LLMGateway, mcp: MCPExecutor, skills: SkillRegistry):
        self.name = name
        self.gateway = gateway
        self.mcp = mcp
        self.skills = skills

    def execute_task(self, task: ProjectTask, request: ExecutionContext) -> List[Artifact]:
        logger.info(f"[{self.name}] Iniciando task: {task.name}")
        artifacts = []
        
        # 1. Preparar contexto base (Brain + Plan)
        base_context = {
            "domain": request.discovery_data.get("domain", "analytics"),
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
        for skill_name in task.required_skills:
            if skill_name in CORE_SKILL_CONTRACTS:
                contract = CORE_SKILL_CONTRACTS[skill_name]
                
                # Se faltar algum input vital, poderíamos invocar o LLM para preencher. 
                # Para manter estabilidade, geramos via LLM uma extração dos inputs se necessário.
                missing = [p.name for p in contract.input_schema if p.required and p.name not in base_context]
                if missing:
                    logger.warning(f"[{self.name}] Faltam inputs para a skill {skill_name}: {missing}. LLM tentará inferir.")
                    system_prompt = f"Gere um JSON preenchendo os seguintes campos: {missing} baseando-se no contexto."
                    prompt = f"Task: {task.description}\nArch: {json.dumps(base_context['architecture'])}"
                    import asyncio
                    resp = asyncio.run(self.gateway.generate(prompt, system_prompt=system_prompt))
                    if resp.content:
                        try:
                            text = resp.content
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
                import uuid
                artifacts.append(Artifact(
                    identity=str(uuid.uuid4()),
                    name=art_name,
                    path=art_name,
                    type="skill_output",
                    content=content,
                    metadata={"generator": "skill", "skill_name": skill_name},
                    producer=self.name
                ))
                logger.info(f"[{self.name}] Skill {skill_name} gerou artefato {art_name}")
            else:
                logger.warning(f"[{self.name}] Falha na skill {skill_name}: {res.get('error')}")

        # 2.5 Invocar MCPs requeridos
        for mcp_name in getattr(task, "required_mcps", []):
            try:
                # Aqui o Agente aciona MCP real
                mcp_res = self.mcp.execute(mcp_name, payload=base_context)
                if mcp_res.get("status") not in ("ok", "PASSED"):
                    raise ValueError(f"MCP {mcp_name} falhou: {mcp_res}")
                logger.info(f"[{self.name}] MCP {mcp_name} executado com sucesso.")
            except Exception as e:
                logger.error(f"[{self.name}] Falha fatal no MCP {mcp_name}: {e}")
                raise RuntimeError(f"Falha na dependência MCP: {mcp_name}") from e

        # 3. Invocar LLM para gerar código complementar (se houver expected_artifacts que não foram gerados)
        generated_files = [a.name for a in artifacts]
        missing_artifacts = [ea for ea in getattr(task, "expected_artifacts", []) if ea not in generated_files]
        
        for art in missing_artifacts:
            prompt = f"Gere código final para {task.name} no contexto de {base_context['architecture'].get('architecture_pattern')}\nDeve produzir o arquivo: {art}"
            import asyncio
            llm_resp = asyncio.run(self.gateway.generate(prompt, system_prompt=f"Você é o {self.name}", model_preference="openai"))
            if llm_resp.content:
                content = llm_resp.content
                import uuid
                artifacts.append(Artifact(
                    identity=str(uuid.uuid4()),
                    name=art,
                    path=art,
                    type="source_code",
                    content=content,
                    metadata={"generator": "llm", "agent_name": self.name},
                    producer=self.name
                ))
            else:
                logger.error(f"[{self.name}] Erro no LLM para {art}")

        logger.info(f"[{self.name}] ProjectTask {task.name} concluída. {len(artifacts)} artefatos gerados.")
        return artifacts
