"""
Task Decomposer - Lógica de decomposição de objetivos em tarefas
"""

import re
import hashlib
from typing import List, Optional
from .k_interfaces import ITaskDecomposer
from .i_schemas import Task, TaskType, TaskPriority, PlanningContext


class TaskDecomposer(ITaskDecomposer):
    """Implementação de decomposição de objetivos em tarefas."""

    def __init__(self):
        """Inicializa o decompositor de tarefas."""
        self.task_counter = 0

    async def decompose(self, objective: str, context: Optional[PlanningContext] = None) -> List[Task]:
        """
        Decompõe um objetivo em tarefas atômicas.
        """
        tasks = []

        # Identificar tipo de objetivo e aplicar estratégia de decomposição
        if self._is_data_analysis_objective(objective):
            tasks = await self._decompose_data_analysis(objective, context)
        elif self._is_report_generation_objective(objective):
            tasks = await self._decompose_report_generation(objective, context)
        elif self._is_data_processing_objective(objective):
            tasks = await self._decompose_data_processing(objective, context)
        else:
            tasks = await self._decompose_generic(objective, context)

        # Identificar dependências
        tasks = await self.identify_dependencies(tasks)

        # Eliminar duplicatas
        tasks = await self.eliminate_duplicates(tasks)

        return tasks

    async def identify_dependencies(self, tasks: List[Task]) -> List[Task]:
        """
        Identifica dependências entre tarefas baseado em tipos e descrições.
        """
        # Mapear tarefas por tipo
        task_by_type = {}
        for task in tasks:
            if task.task_type not in task_by_type:
                task_by_type[task.task_type] = []
            task_by_type[task.task_type].append(task)

        # Data collection deve vir antes de processing
        if TaskType.DATA_COLLECTION in task_by_type and TaskType.DATA_PROCESSING in task_by_type:
            for processing_task in task_by_type[TaskType.DATA_PROCESSING]:
                for collection_task in task_by_type[TaskType.DATA_COLLECTION]:
                    processing_task.add_dependency(collection_task.id)

        # Data processing deve vir antes de analysis
        if TaskType.DATA_PROCESSING in task_by_type and TaskType.ANALYSIS in task_by_type:
            for analysis_task in task_by_type[TaskType.ANALYSIS]:
                for processing_task in task_by_type[TaskType.DATA_PROCESSING]:
                    analysis_task.add_dependency(processing_task.id)

        # Analysis deve vir antes de reporting
        if TaskType.ANALYSIS in task_by_type and TaskType.REPORTING in task_by_type:
            for reporting_task in task_by_type[TaskType.REPORTING]:
                for analysis_task in task_by_type[TaskType.ANALYSIS]:
                    reporting_task.add_dependency(analysis_task.id)

        return tasks

    async def eliminate_duplicates(self, tasks: List[Task]) -> List[Task]:
        """
        Elimina tarefas duplicadas baseado em similaridade de descrição.
        """
        seen_hashes = {}
        unique_tasks = []

        for task in tasks:
            # Gerar hash da descrição (normalizada)
            normalized_desc = task.description.lower().strip()
            desc_hash = hashlib.md5(normalized_desc.encode()).hexdigest()

            if desc_hash not in seen_hashes:
                seen_hashes[desc_hash] = task
                unique_tasks.append(task)
            else:
                # Merge metadados da tarefa duplicada
                existing_task = seen_hashes[desc_hash]
                existing_task.metadata.update(task.metadata)

        return unique_tasks

    def _is_data_analysis_objective(self, objective: str) -> bool:
        """Verifica se o objetivo é de análise de dados."""
        keywords = ["analyze", "analysis", "metrics", "kpi", "statistics"]
        return any(keyword in objective.lower() for keyword in keywords)

    def _is_report_generation_objective(self, objective: str) -> bool:
        """Verifica se o objetivo é de geração de relatório."""
        keywords = ["report", "generate report", "dashboard", "visualization"]
        return any(keyword in objective.lower() for keyword in keywords)

    def _is_data_processing_objective(self, objective: str) -> bool:
        """Verifica se o objetivo é de processamento de dados."""
        keywords = ["process", "transform", "clean", "filter", "aggregate"]
        return any(keyword in objective.lower() for keyword in keywords)

    async def _decompose_data_analysis(self, objective: str, context: Optional[PlanningContext]) -> List[Task]:
        """Decompõe objetivo de análise de dados."""
        tasks = []

        # Task 1: Coletar dados
        tasks.append(Task(
            id=self._generate_task_id("collect_data"),
            description="Collect required data for analysis",
            task_type=TaskType.DATA_COLLECTION,
            priority=TaskPriority.HIGH,
            responsible_agent="data_agent"
        ))

        # Task 2: Validar dados
        tasks.append(Task(
            id=self._generate_task_id("validate_data"),
            description="Validate data quality and completeness",
            task_type=TaskType.VALIDATION,
            priority=TaskPriority.HIGH,
            responsible_agent="data_agent"
        ))

        # Task 3: Processar dados
        tasks.append(Task(
            id=self._generate_task_id("process_data"),
            description="Process and transform data for analysis",
            task_type=TaskType.DATA_PROCESSING,
            priority=TaskPriority.MEDIUM,
            responsible_agent="analytics_agent"
        ))

        # Task 4: Realizar análise
        tasks.append(Task(
            id=self._generate_task_id("perform_analysis"),
            description="Perform data analysis and calculations",
            task_type=TaskType.ANALYSIS,
            priority=TaskPriority.HIGH,
            responsible_agent="analytics_agent"
        ))

        # Task 5: Validar resultados
        tasks.append(Task(
            id=self._generate_task_id("validate_results"),
            description="Validate analysis results",
            task_type=TaskType.VALIDATION,
            priority=TaskPriority.MEDIUM,
            responsible_agent="analytics_agent"
        ))

        return tasks

    async def _decompose_report_generation(self, objective: str, context: Optional[PlanningContext]) -> List[Task]:
        """Decompõe objetivo de geração de relatório."""
        tasks = []

        # Task 1: Coletar dados
        tasks.append(Task(
            id=self._generate_task_id("collect_report_data"),
            description="Collect data for report generation",
            task_type=TaskType.DATA_COLLECTION,
            priority=TaskPriority.HIGH,
            responsible_agent="data_agent"
        ))

        # Task 2: Analisar dados
        tasks.append(Task(
            id=self._generate_task_id("analyze_report_data"),
            description="Analyze data for report",
            task_type=TaskType.ANALYSIS,
            priority=TaskPriority.HIGH,
            responsible_agent="analytics_agent"
        ))

        # Task 3: Gerar relatório
        tasks.append(Task(
            id=self._generate_task_id("generate_report"),
            description="Generate report with visualizations",
            task_type=TaskType.REPORTING,
            priority=TaskPriority.HIGH,
            responsible_agent="reporting_agent"
        ))

        # Task 4: Validar relatório
        tasks.append(Task(
            id=self._generate_task_id("validate_report"),
            description="Validate report accuracy and completeness",
            task_type=TaskType.VALIDATION,
            priority=TaskPriority.MEDIUM,
            responsible_agent="reporting_agent"
        ))

        return tasks

    async def _decompose_data_processing(self, objective: str, context: Optional[PlanningContext]) -> List[Task]:
        """Decompõe objetivo de processamento de dados."""
        tasks = []

        # Task 1: Ler dados
        tasks.append(Task(
            id=self._generate_task_id("read_data"),
            description="Read input data",
            task_type=TaskType.DATA_COLLECTION,
            priority=TaskPriority.HIGH,
            responsible_agent="data_agent"
        ))

        # Task 2: Limpar dados
        tasks.append(Task(
            id=self._generate_task_id("clean_data"),
            description="Clean and normalize data",
            task_type=TaskType.DATA_PROCESSING,
            priority=TaskPriority.HIGH,
            responsible_agent="data_agent"
        ))

        # Task 3: Transformar dados
        tasks.append(Task(
            id=self._generate_task_id("transform_data"),
            description="Transform data according to requirements",
            task_type=TaskType.DATA_PROCESSING,
            priority=TaskPriority.MEDIUM,
            responsible_agent="data_agent"
        ))

        # Task 4: Salvar dados
        tasks.append(Task(
            id=self._generate_task_id("save_data"),
            description="Save processed data",
            task_type=TaskType.DATA_PROCESSING,
            priority=TaskPriority.HIGH,
            responsible_agent="data_agent"
        ))

        return tasks

    async def _decompose_generic(self, objective: str, context: Optional[PlanningContext]) -> List[Task]:
        """Decompõe objetivo genérico."""
        tasks = []

        # Task única para objetivo genérico
        tasks.append(Task(
            id=self._generate_task_id("execute_task"),
            description=objective,
            task_type=TaskType.CUSTOM,
            priority=TaskPriority.MEDIUM,
            responsible_agent="general_agent"
        ))

        return tasks

    def _generate_task_id(self, prefix: str) -> str:
        """Gera um ID único para tarefa."""
        self.task_counter += 1
        return f"{prefix}_{self.task_counter}"
