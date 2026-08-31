from dataclasses import dataclass, field
from typing import List, Dict, Any
from abc import ABC, abstractmethod

@dataclass
class SkillContract:
    name: str
    description: str
    required_inputs: List[str]
    expected_outputs: List[str]
    
    def validate_inputs(self, context: Dict[str, Any]) -> bool:
        """
        Verifica se todos os required_inputs estão presentes no context fornecido pelo Agent.
        """
        missing = [req for req in self.required_inputs if req not in context]
        if missing:
            raise ValueError(f"Skill '{self.name}' falhou na validação de contrato. Faltam os inputs: {missing}")
        return True

class BaseSkill(ABC):
    def __init__(self, contract: SkillContract):
        self.contract = contract

    def validate_input(self, context: Dict[str, Any]) -> bool:
        return self.contract.validate_inputs(context)
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a skill com o contexto validado."""
        pass

    def validate_output(self, result: Dict[str, Any]) -> bool:
        missing = [req for req in self.contract.expected_outputs if req not in result]
        if missing:
            raise ValueError(f"Skill '{self.contract.name}' falhou na validação de output. Faltam os retornos: {missing}")
        return True

# Registro estático dos contratos das skills base da plataforma
CORE_SKILL_CONTRACTS = {
    "sql_generation": SkillContract(
        name="sql_generation",
        description="Gera esquemas DDL SQL baseados no dataset ou modelo.",
        required_inputs=["database_technology", "schema_definition"],
        expected_outputs=["schema.sql"]
    ),
    "api_design": SkillContract(
        name="api_design",
        description="Desenha a especificação OpenAPI.",
        required_inputs=["domain", "architecture"],
        expected_outputs=["swagger.yaml"]
    ),
    "dataset_profiling": SkillContract(
        name="dataset_profiling",
        description="Realiza o profiling descritivo do dataset.",
        required_inputs=["dataset_path"],
        expected_outputs=["dataset_profile.json"]
    ),
    "etl_scripting": SkillContract(
        name="etl_scripting",
        description="Gera scripts de extração, transformação e carga.",
        required_inputs=["data_processing_tool", "dataset_path", "target_table"],
        expected_outputs=["etl.py"]
    ),
    "basic_coding": SkillContract(
        name="basic_coding",
        description="Gera um script padrão Python hello world.",
        required_inputs=["script_name"],
        expected_outputs=[]
    )
}
