"""
SkillRegistry — Autoridade de resolução, carregamento sob demanda e execução de Skills.
Implementa Progressive Disclosure e Lazy Loading (carrega apenas a Skill selecionada).
Suporta IDs canônicos (kebab-case) e legados (snake_case) para compatibilidade reversa total.
"""
import logging
import asyncio
import inspect
from typing import Dict, Any, Optional, Type
from a_platform.b_contracts import BaseSkill

logger = logging.getLogger(__name__)

class SkillRegistry:
    """
    Centraliza a resolução e execução das Skills.
    Carrega sob demanda (lazy loading) a classe concreta correspondente.
    """
    def __init__(self):
        self._instances: Dict[str, BaseSkill] = {}
        # Mapeamento dinâmico: skill_id -> (module_path, class_name)
        self._skill_loaders: Dict[str, tuple[str, str]] = {
            # Canonical IDs
            "dataset-profiling": ("a_platform.e_skills.b_dataset.profiling.skill", "DatasetProfilingSkill"),
            "data-ingestion": ("a_platform.e_skills.b_dataset.ingestion.skill", "DataIngestionSkill"),
            "data-cleaning": ("a_platform.e_skills.b_dataset.cleaning.skill", "DataCleaningSkill"),
            "data-transformation": ("a_platform.e_skills.b_dataset.transformation.skill", "DataTransformationSkill"),
            "dataset-validation": ("a_platform.e_skills.b_dataset.validation.skill", "DatasetValidationSkill"),
            "exploratory-data-analysis": ("a_platform.e_skills.c_analytics.exploratory_data_analysis.skill", "ExploratoryDataAnalysisSkill"),
            "statistical-analysis": ("a_platform.e_skills.c_analytics.statistical_analysis.skill", "StatisticalAnalysisSkill"),
            "metrics-analysis": ("a_platform.e_skills.c_analytics.metrics_analysis.skill", "MetricsAnalysisSkill"),
            "data-visualization": ("a_platform.e_skills.c_analytics.data_visualization.skill", "DataVisualizationSkill"),
            "feature-engineering": ("a_platform.e_skills.c_analytics.feature_engineering.skill", "FeatureEngineeringSkill"),
            "feature-selection": ("a_platform.e_skills.c_analytics.feature_selection.skill", "FeatureSelectionSkill"),
            "model-training": ("a_platform.e_skills.c_analytics.model_training.skill", "ModelTrainingSkill"),
            "model-evaluation": ("a_platform.e_skills.c_analytics.model_evaluation.skill", "ModelEvaluationSkill"),
            "prediction": ("a_platform.e_skills.c_analytics.prediction.skill", "PredictionSkill"),
            "etl-pipeline": ("a_platform.e_skills.d_data_engineering.etl_pipeline.skill", "EtlPipelineSkill"),
            "sql-analytics": ("a_platform.e_skills.d_data_engineering.sql_analytics.skill", "SqlAnalyticsSkill"),
            "sql-optimization": ("a_platform.e_skills.d_data_engineering.sql_optimization.skill", "SqlOptimizationSkill"),
            "dimensional-modeling": ("a_platform.e_skills.d_data_engineering.dimensional_modeling.skill", "DimensionalModelingSkill"),
            "analytics-engineering": ("a_platform.e_skills.d_data_engineering.analytics_engineering.skill", "AnalyticsEngineeringSkill"),
            "pipeline-observability": ("a_platform.e_skills.d_data_engineering.pipeline_observability.skill", "PipelineObservabilitySkill"),
            "technical-documentation": ("a_platform.e_skills.e_development.technical_documentation.skill", "TechnicalDocumentationSkill"),
            "readme-generation": ("a_platform.e_skills.e_development.readme_generation.skill", "ReadmeGenerationSkill"),
            "architecture-documentation": ("a_platform.e_skills.e_development.architecture_documentation.skill", "ArchitectureDocumentationSkill"),
            "data-quality": ("a_platform.e_skills.f_quality.data_quality.skill", "DataQualitySkill"),
            "code-quality": ("a_platform.e_skills.f_quality.code_quality.skill", "CodeQualitySkill"),
            "dependency-quality": ("a_platform.e_skills.f_quality.dependency_quality.skill", "DependencyQualitySkill"),
            "discover-intent": ("a_platform.e_skills.a_discovery.intent_discovery.skill", "IntentDiscoverySkill"),

            # Aliases e compatibilidade reversa com o repositório existente
            "dataset_profiling": ("a_platform.e_skills.a_dataset_profiling.c_profiling.a_profiler", "DatasetProfilingSkill"),
            "etl_scripting": ("a_platform.e_skills.b_etl.a_etl_scripting", "EtlScriptingSkill"),
            "sql_generation": ("a_platform.e_skills.d_analytics.a_sql_generation", "SqlGenerationSkill"),
            "basic_coding": ("a_platform.e_skills.g_optional.a_development.b_basic_coding", "BasicCodingSkill"),
            "api_design": ("a_platform.e_skills.g_optional.a_development.a_api_design", "ApiDesignSkill"),
            "cleaning": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "CleaningSkill"),
            "deduplication": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "DeduplicationSkill"),
            "categorization": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "CategorizationSkill"),
            "analytics": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "AnalyticsSkill"),
            "dashboard": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "DashboardSkill"),
            "chatbot": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "ChatbotSkill"),
            "backend": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "BackendSkill"),
            "frontend": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "FrontendSkill"),
            "testing": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "TestingSkill"),
            "documentation": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "DocumentationSkill"),
            "docker": ("a_platform.e_skills.g_optional.a_development.f_consolidation_skills", "DockerSkill"),
        }

    @property
    def skills(self):
        """Propriedade para compatibilidade com acessos diretos legados a self.skills."""
        return self

    def __contains__(self, item: str) -> bool:
        return self._normalize_name(item) in self._skill_loaders

    def __getitem__(self, item: str) -> Optional[BaseSkill]:
        return self.get_skill(item)

    def _normalize_name(self, name: str) -> str:
        if name in self._skill_loaders:
            return name
        kebab = name.replace("_", "-")
        if kebab in self._skill_loaders:
            return kebab
        snake = name.replace("-", "_")
        if snake in self._skill_loaders:
            return snake
        return name

    def get(self, name: str) -> Optional[BaseSkill]:
        """Alias para get_skill."""
        return self.get_skill(name)

    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """Resolve e carrega sob demanda (lazy loading) a Skill solicitada."""
        key = self._normalize_name(name)
        if key in self._instances:
            return self._instances[key]

        if key not in self._skill_loaders:
            logger.warning(f"[SkillRegistry] Skill '{name}' não encontrada no registry.")
            return None

        module_path, class_name = self._skill_loaders[key]
        try:
            import importlib
            mod = importlib.import_module(module_path)
            cls_: Type[BaseSkill] = getattr(mod, class_name)
            instance = cls_()
            self._instances[key] = instance
            self._instances[name] = instance
            logger.info(f"[SkillRegistry] Skill '{key}' carregada sob demanda com sucesso ({class_name}).")
            return instance
        except Exception as e:
            logger.error(f"[SkillRegistry] Falha ao carregar skill '{key}' de {module_path}.{class_name}: {e}")
            return None

    def run_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Invoca a Skill solicitada, validando contratos de input e output."""
        logger.info(f"[SkillRegistry] Invocando skill: {skill_name}")
        skill_impl = self.get_skill(skill_name)
        if skill_impl is None:
            return {"success": False, "error": f"Skill '{skill_name}' desconhecida ou indisponível."}

        try:
            # 1. Valida input
            skill_impl.validate_input(context)

            # 2. Executa
            if inspect.iscoroutinefunction(skill_impl.execute):
                result = asyncio.run(skill_impl.execute(context))
            else:
                result = skill_impl.execute(context)

            # 3. Valida output
            skill_impl.validate_output(result)

            first_artifact = list(result.keys())[0] if result else "unknown"
            content = result.get(first_artifact, "")
            return {"success": True, "artifact": first_artifact, "content": content}

        except ValueError as ve:
            logger.error(f"[SkillRegistry] Erro de contrato na skill '{skill_name}': {ve}")
            return {"success": False, "error": str(ve)}
        except Exception as e:
            logger.error(f"[SkillRegistry] Falha de execução na skill '{skill_name}': {e}")
            return {"success": False, "error": str(e)}
