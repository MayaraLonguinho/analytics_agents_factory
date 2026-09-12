"""
Analytics Orchestrator - Coordenador de Skills de Analytics

Responsável por coordenar todas as Skills de Analytics, incluindo:
- Skills de Data Science
- Skills de Data Profiling
- Skills de Visualização
- Skills de ETL (quando aplicável)

O Orchestrator segue o Agent Decision Flow e consulta o Brain antes da execução.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import importlib
import sys


class AnalyticsOrchestrator:
    """
    Coordenador de Skills de Analytics
    
    Responsabilidades:
    - Localizar Skills registradas
    - Validar entradas
    - Definir ordem de execução
    - Registrar logs
    - Documentar o fluxo executado
    - Consultar o Brain antes da execução
    - Seguir o Agent Decision Flow
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o Analytics Orchestrator
        
        Args:
            config: Dicionário de configuração
        """
        self.config = config or {}
        self.logger = self._setup_logger()
        self.skill_registry = self._load_skill_registry()
        self.execution_log = []
        self.brain_consulted = False
        
    def _setup_logger(self) -> logging.Logger:
        """Configura o logger do Orchestrator"""
        logger = logging.getLogger("AnalyticsOrchestrator")
        logger.setLevel(self.config.get("log_level", logging.INFO))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_skill_registry(self) -> Dict[str, Any]:
        """
        Carrega o registro de Skills disponíveis
        
        Returns:
            Dicionário com Skills registradas
        """
        try:
            # Importar Skills de Data Science
            from a_backend.b_src.i_services.data_science import (
                Describe, Mean, Median, Mode, Variance, StandardDeviation,
                Covariance, Correlation, Percentiles, Distribution,
                MissingValues, UniqueValues, FeatureImportance
            )
            
            # Importar Skills de Profiling
            from a_backend.b_src.i_services.profiling import (
                StatisticsAnalyzer, TypeInference, MissingValuesAnalyzer,
                DuplicateAnalyzer, CardinalityAnalyzer, DistributionAnalyzer,
                FeatureClassifier, OutlierDetector, AnomalyDetector
            )
            
            # Importar Skills de Visualização
            from a_backend.b_src.i_services.visualization import (
                Histogram, ScatterPlot, LinePlot, BarPlot, PieChart,
                BoxPlot, ViolinPlot, Heatmap, PairPlot, CorrelationMatrix,
                ConfusionMatrix, ROCCurve, RegressionPlot, ClusterPlot,
                TrendPlot, SeasonalityPlot, ResidualPlot
            )
            
            # Importar Skills de ETL (quando aplicável)
            from a_backend.b_src.i_services.etl import (
                Extract, Validation, Cleaning, Mapping, Transformation,
                Grouping, Loading
            )
            
            registry = {
                # Data Science Skills
                "describe": Describe,
                "mean": Mean,
                "median": Median,
                "mode": Mode,
                "variance": Variance,
                "std_dev": StandardDeviation,
                "covariance": Covariance,
                "correlation": Correlation,
                "percentiles": Percentiles,
                "distribution": Distribution,
                "missing_values": MissingValues,
                "unique_values": UniqueValues,
                "feature_importance": FeatureImportance,
                
                # Profiling Skills
                "statistics_analyzer": StatisticsAnalyzer,
                "type_inference": TypeInference,
                "missing_values_analyzer": MissingValuesAnalyzer,
                "duplicate_analyzer": DuplicateAnalyzer,
                "cardinality_analyzer": CardinalityAnalyzer,
                "distribution_analyzer": DistributionAnalyzer,
                "feature_classifier": FeatureClassifier,
                "outlier_detector": OutlierDetector,
                "anomaly_detector": AnomalyDetector,
                
                # Visualization Skills
                "histogram": Histogram,
                "scatter_plot": ScatterPlot,
                "line_plot": LinePlot,
                "bar_plot": BarPlot,
                "pie_chart": PieChart,
                "boxplot": BoxPlot,
                "violin_plot": ViolinPlot,
                "heatmap": Heatmap,
                "pair_plot": PairPlot,
                "correlation_matrix": CorrelationMatrix,
                "confusion_matrix": ConfusionMatrix,
                "roc_curve": ROCCurve,
                "regression_plot": RegressionPlot,
                "cluster_plot": ClusterPlot,
                "trend_plot": TrendPlot,
                "seasonality_plot": SeasonalityPlot,
                "residual_plot": ResidualPlot,
                
                # ETL Skills
                "extract": Extract,
                "validation": Validation,
                "cleaning": Cleaning,
                "mapping": Mapping,
                "transformation": Transformation,
                "grouping": Grouping,
                "loading": Loading
            }
            
            self.logger.info(f"Skill Registry carregado com {len(registry)} Skills")
            return registry
            
        except ImportError as e:
            self.logger.error(f"Erro ao importar Skills: {e}")
            return {}
    
    async def consult_brain(self, task: str) -> Dict[str, Any]:
        """
        Consulta o Brain antes da execução
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Dicionário com conhecimento do Brain
        """
        self.logger.info(f"Consultando Brain para tarefa: {task}")
        
        # Simulação de consulta ao Brain
        # Em produção, isso consultaria os arquivos em b_ai_engine/a_brain/
        brain_knowledge = {
            "task": task,
            "suggested_skills": self._suggest_skills(task),
            "execution_order": self._determine_execution_order(task),
            "best_practices": self._get_best_practices(task),
            "timestamp": datetime.now().isoformat()
        }
        
        self.brain_consulted = True
        self.logger.info(f"Brain consultado com sucesso")
        
        return brain_knowledge
    
    def _suggest_skills(self, task: str) -> List[str]:
        """
        Sugere Skills baseadas na tarefa
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Lista de Skills sugeridas
        """
        task_lower = task.lower()
        
        if "profiling" in task_lower or "exploratory" in task_lower:
            return [
                "type_inference", "statistics_analyzer", "missing_values_analyzer",
                "duplicate_analyzer", "cardinality_analyzer", "distribution_analyzer"
            ]
        elif "visualization" in task_lower or "plot" in task_lower:
            return [
                "histogram", "scatter_plot", "line_plot", "bar_plot",
                "heatmap", "correlation_matrix"
            ]
        elif "statistics" in task_lower or "analysis" in task_lower:
            return [
                "describe", "mean", "median", "variance", "std_dev",
                "correlation", "covariance"
            ]
        elif "ml" in task_lower or "feature" in task_lower:
            return [
                "feature_importance", "feature_classifier", "outlier_detector"
            ]
        else:
            return ["describe", "statistics_analyzer"]
    
    def _determine_execution_order(self, task: str) -> List[str]:
        """
        Determina a ordem de execução das Skills
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Lista de Skills em ordem de execução
        """
        task_lower = task.lower()
        
        if "profiling" in task_lower:
            return [
                "type_inference",
                "statistics_analyzer",
                "missing_values_analyzer",
                "duplicate_analyzer",
                "cardinality_analyzer",
                "distribution_analyzer",
                "feature_classifier"
            ]
        elif "visualization" in task_lower:
            return [
                "describe",
                "statistics_analyzer",
                "correlation",
                "histogram",
                "scatter_plot",
                "heatmap"
            ]
        else:
            return self._suggest_skills(task)
    
    def _get_best_practices(self, task: str) -> List[str]:
        """
        Obtém melhores práticas do Brain
        
        Args:
            task: Tarefa a ser executada
            
        Returns:
            Lista de melhores práticas
        """
        return [
            "Validar dados antes da execução",
            "Tratar valores nulos apropriadamente",
            "Documentar cada passo da execução",
            "Verificar resultados após cada Skill",
            "Seguir responsabilidade única de cada Skill"
        ]
    
    def validate_inputs(self, inputs: Dict[str, Any], skill_name: str) -> bool:
        """
        Valida as entradas para uma Skill
        
        Args:
            inputs: Dicionário de entradas
            skill_name: Nome da Skill
            
        Returns:
            True se válido, False caso contrário
        """
        self.logger.info(f"Validando entradas para Skill: {skill_name}")
        
        # Validação básica
        if not inputs:
            self.logger.error("Entradas vazias")
            return False
        
        if "data" not in inputs:
            self.logger.error("Dados não fornecidos")
            return False
        
        # Validação específica por Skill
        if skill_name in ["scatter_plot", "line_plot", "bar_plot", "regression_plot"]:
            if "x_column" not in inputs or "y_column" not in inputs:
                self.logger.error("Colunas x e y não fornecidas")
                return False
        
        if skill_name in ["histogram", "boxplot", "violin_plot"]:
            if "column" not in inputs:
                self.logger.error("Coluna não fornecida")
                return False
        
        self.logger.info(f"Entradas validadas com sucesso para Skill: {skill_name}")
        return True
    
    async def execute_skill(self, skill_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa uma Skill específica
        
        Args:
            skill_name: Nome da Skill
            inputs: Dicionário de entradas
            
        Returns:
            Dicionário com resultado da execução
        """
        start_time = datetime.now()
        
        try:
            # Validar entradas
            if not self.validate_inputs(inputs, skill_name):
                return {
                    "success": False,
                    "error": "Validação de entradas falhou",
                    "skill": skill_name,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Localizar Skill
            if skill_name not in self.skill_registry:
                self.logger.error(f"Skill {skill_name} não encontrada no registro")
                return {
                    "success": False,
                    "error": f"Skill {skill_name} não encontrada",
                    "skill": skill_name,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Instanciar Skill
            skill_class = self.skill_registry[skill_name]
            skill = skill_class()
            
            # Executar Skill
            self.logger.info(f"Executando Skill: {skill_name}")
            result = await skill.execute(inputs)
            
            # Registrar execução
            execution_time = (datetime.now() - start_time).total_seconds()
            log_entry = {
                "skill": skill_name,
                "success": result.get("success", False),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
            self.execution_log.append(log_entry)
            
            self.logger.info(f"Skill {skill_name} executada em {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao executar Skill {skill_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "skill": skill_name,
                "timestamp": datetime.now().isoformat()
            }
    
    async def execute_pipeline(self, task: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa um pipeline completo de Skills
        
        Args:
            task: Tarefa a ser executada
            inputs: Dicionário de entradas
            
        Returns:
            Dicionário com resultado do pipeline
        """
        start_time = datetime.now()
        
        self.logger.info(f"Iniciando pipeline para tarefa: {task}")
        
        # Consultar Brain
        brain_knowledge = await self.consult_brain(task)
        
        # Determinar Skills e ordem
        skills_to_execute = brain_knowledge.get("execution_order", [])
        
        if not skills_to_execute:
            self.logger.warning("Nenhuma Skill sugerida pelo Brain")
            return {
                "success": False,
                "error": "Nenhuma Skill sugerida",
                "timestamp": datetime.now().isoformat()
            }
        
        # Executar Skills em ordem
        results = {}
        for skill_name in skills_to_execute:
            self.logger.info(f"Executando Skill {skill_name} no pipeline")
            result = await self.execute_skill(skill_name, inputs)
            results[skill_name] = result
            
            # Se uma Skill falhar, continuar com as próximas
            if not result.get("success"):
                self.logger.warning(f"Skill {skill_name} falhou, continuando pipeline")
        
        # Documentar fluxo executado
        execution_time = (datetime.now() - start_time).total_seconds()
        pipeline_summary = {
            "task": task,
            "total_skills": len(skills_to_execute),
            "successful_skills": sum(1 for r in results.values() if r.get("success")),
            "failed_skills": sum(1 for r in results.values() if not r.get("success")),
            "execution_time": execution_time,
            "execution_log": self.execution_log,
            "brain_consulted": self.brain_consulted,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"Pipeline concluído em {execution_time:.2f}s")
        
        return {
            "success": True,
            "results": results,
            "summary": pipeline_summary,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """
        Retorna o log de execução
        
        Returns:
            Lista de entradas de log
        """
        return self.execution_log
    
    def clear_execution_log(self) -> None:
        """Limpa o log de execução"""
        self.execution_log = []
        self.logger.info("Log de execução limpo")
    
    def get_skill_registry(self) -> Dict[str, Any]:
        """
        Retorna o registro de Skills
        
        Returns:
            Dicionário com Skills registradas
        """
        return self.skill_registry
