import logging
import re
from typing import Dict, Any
from a_platform.b_contracts import BaseSkill
from a_platform.j_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class ReadmeGenerationSkill(BaseSkill):
    def __init__(self, **data: Any):
        super().__init__(
            skill_id="readme-generation",
            name="README Generation Skill",
            input_schema=[],
            **data
        )
        self.llm = LLMGateway()

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        description = context.get("task_description", "Geração do README do projeto")
        plan = context.get("project_plan", {})
        arch = context.get("architecture", {})

        system_prompt = (
            "Você é um Technical Writer sênior. Gere o README.md do projeto estruturado em: "
            "1. Objetivo, 2. Fonte de Dados, 3. Fluxo de Dados (diagrama textual), "
            "4. Estrutura do Projeto, 5. Dependências, 6. Comando Exato para Execução, 7. Resultado Esperado. "
            "Responda SOMENTE com o conteúdo Markdown, sem bloco ```markdown envolvendo o documento todo."
        )
        user_prompt = f"Descrição: {description}\nArquitetura: {arch}\nPlano: {plan}\nContexto: {context}"
        resp = await self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        content = resp.content or ""
        content = re.sub(r'^```[\w]*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'```$', '', content, flags=re.MULTILINE).strip()

        result = {"README.md": content}
        self.validate_output(result)
        return result
