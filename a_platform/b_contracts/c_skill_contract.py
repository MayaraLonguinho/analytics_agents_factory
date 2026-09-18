from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class SkillExecutionType(str, Enum):
    NATIVE = "native"
    LLM = "llm"

class ParameterDefinition(BaseModel):
    name: str
    data_type: str
    required: bool = True
    constraints: Dict[str, Any] = Field(default_factory=dict)

class SkillContract(BaseModel):
    model_config = {"extra": "allow"}
    skill_id: str = "default_skill"
    name: str = "Default Skill"
    description: str = "Default description"
    execution_type: SkillExecutionType = SkillExecutionType.NATIVE
    version: str = "1.0.0"
    input_schema: List[ParameterDefinition] = Field(default_factory=list)
    output_schema: List[ParameterDefinition] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    compatible_agents: List[str] = Field(default_factory=list)
    required_mcps: List[str] = Field(default_factory=list)
    required_brain_context: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source: str = ""
    category: str = ""
    author: str = ""
    documentation_url: str = ""

    def validate_input(self, context: Dict[str, Any]) -> None:
        """
        Valida o contexto de entrada contra o input_schema da Skill.
        Falha explicitamente se context não for dict ou se algum parâmetro obrigatório
        declarado em input_schema estiver ausente ou for None.
        """
        if not isinstance(context, dict):
            raise ValueError(
                f"[{self.skill_id}] Contexto de entrada inválido: esperado dict, obtido {type(context).__name__}."
            )

        missing = []
        for param in self.input_schema:
            if param.required and (param.name not in context or context[param.name] is None):
                missing.append(param.name)

        if missing:
            raise ValueError(
                f"[{self.skill_id}] Parâmetros obrigatórios de entrada ausentes: {missing}."
            )

    def validate_output(self, result: Dict[str, Any]) -> None:
        """
        Valida o resultado da execução contra o output_schema da Skill.
        Garante que o resultado seja um dicionário não vazio e, caso output_schema
        declare parâmetros obrigatórios, verifica se todos estão presentes.
        """
        if not isinstance(result, dict):
            raise ValueError(
                f"[{self.skill_id}] Resultado de saída inválido: esperado dict, obtido {type(result).__name__}."
            )

        if not result:
            raise ValueError(
                f"[{self.skill_id}] Resultado da execução da Skill está vazio."
            )

        missing = []
        for param in self.output_schema:
            if param.required and (param.name not in result or result[param.name] is None):
                missing.append(param.name)

        if missing:
            raise ValueError(
                f"[{self.skill_id}] Parâmetros obrigatórios de saída ausentes: {missing}."
            )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Contrato de execução base assíncrono."""
        self.validate_input(context)
        raise NotImplementedError(f"[{self.skill_id}] Método execute() não implementado.")

BaseSkill = SkillContract
CORE_SKILL_CONTRACTS = {}
