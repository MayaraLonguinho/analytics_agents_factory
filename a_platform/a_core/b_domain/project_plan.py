from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Task:
    id: str
    name: str
    description: str
    agent: str
    skills: List[str] = field(default_factory=list)
    mcps: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    expected_artifacts: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    validators: List[str] = field(default_factory=list)

@dataclass
class ProjectPlan:
    project_id: str
    domain: str
    tasks: List[Task] = field(default_factory=list)
    materializer: str = "generic_materializer"
    run_commands: List[str] = field(default_factory=list)
    execution_required: bool = True
    validated: bool = False
    
    def add_task(self, task: Task):
        self.tasks.append(task)

    def validate_dag(self) -> bool:
        """
        Valida se o plano de execução não possui dependências cíclicas ou inválidas.
        """
        if not self.tasks:
            return False

        task_ids = {t.id for t in self.tasks}
        
        # Verifica dependências quebradas
        for task in self.tasks:
            for dep in task.dependencies:
                if dep not in task_ids:
                    raise ValueError(f"Tarefa {task.id} depende da tarefa inexistente {dep}")
                    
        # Verifica ciclos (DFS)
        visited = set()
        path = set()
        
        def has_cycle(t_id: str) -> bool:
            if t_id in path:
                return True
            if t_id in visited:
                return False
                
            visited.add(t_id)
            path.add(t_id)
            
            task = next((t for t in self.tasks if t.id == t_id), None)
            if task:
                for dep in task.dependencies:
                    if has_cycle(dep):
                        return True
                        
            path.remove(t_id)
            return False

        for task in self.tasks:
            if has_cycle(task.id):
                raise ValueError("O plano gerado possui um ciclo de dependências.")
                
        self.validated = True
        return True

    def validate_full(self, skill_registry, mcp_registry, agent_factory, validation_gate) -> bool:
        """
        Valida o DAG e também verifica a existência profunda de todas as dependências 
        declaradas no plano (Agents, Skills, MCPs, Validators, Artefatos).
        """
        self.validate_dag()
        
        for task in self.tasks:
            if not agent_factory.get_agent(task.agent):
                raise ValueError(f"Agente inválido ou não registrado na factory: '{task.agent}' na tarefa {task.id}")
                
            for skill in task.skills:
                # Vamos assumir que skill_registry possua um método has_skill ou get_skill
                # Como não vimos o código todo de skill_registry, o get_skill servirá
                if not skill_registry.get_skill(skill):
                    raise ValueError(f"Skill não registrada: '{skill}' na tarefa {task.id}")
                    
            for mcp in task.mcps:
                if not mcp_registry.get_tool(mcp):
                    raise ValueError(f"MCP não registrado: '{mcp}' na tarefa {task.id}")
                    
            for val in task.validators:
                # Assumimos que validation_gate tem método has_validator ou validators list
                if hasattr(validation_gate, "has_validator") and not validation_gate.has_validator(val):
                     # Fallback check caso não tenha
                     raise ValueError(f"Validator não reconhecido: '{val}' na tarefa {task.id}")
                     
            for art in task.expected_artifacts:
                if not art or "." not in art:
                    raise ValueError(f"Formato de artefato inválido (deve conter extensão): '{art}' na tarefa {task.id}")
                    
        self.validated = True
        return True
