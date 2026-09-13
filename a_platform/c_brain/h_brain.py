import logging
from typing import Dict, Any, List

from .g_registry.a_knowledge_registry import KnowledgeRegistry
from .g_registry.b_pattern_registry import PatternRegistry
from .g_registry.c_rule_registry import RuleRegistry

from a_platform.i_domains.a_domain_registry import DomainRegistry
from a_platform.f_mcp.d_registry.a_registry import MCPRegistry
from a_platform.e_skills.g_registry.j_skill_registry import SkillRegistry
from a_platform.d_agents.n_registry.a_registry import AgentRegistry

logger = logging.getLogger(__name__)

class Brain:
    """
    O Cérebro da plataforma.
    Centraliza o conhecimento core da plataforma (regras fixas) 
    e gerencia o conhecimento de projetos (dinâmico) através de registries formais.
    """
    def __init__(self):
        self.knowledge_registry = KnowledgeRegistry()
        self.rule_registry = RuleRegistry()
        self.pattern_registry = PatternRegistry()
        
        self.domain_registry = DomainRegistry()
        self.mcp_registry = MCPRegistry()
        self.skill_registry = SkillRegistry()
        self.agent_registry = AgentRegistry()
        
        self._initialize_core_knowledge()
        self._initialize_core_rules()
        self._initialize_core_patterns()
        self._initialize_team_standards()
        
        # Project Knowledge (armazenado por contexto da execução atual ou memória passada)
        self.project_knowledge = {}

    def _initialize_team_standards(self):
        roles = {
            "Owner": "Decide regras de negócio e prioridades do produto",
            "Architect": "Decide a stack tecnológica e padrões de arquitetura",
            "Data Engineer": "Responsável por pipelines (ETL/ELT), armazenamento e qualidade de dados",
            "Analytics Engineer": "Responsável por modelagem de dados, transformações (dbt) e métricas de negócio",
            "QA": "Garante a qualidade através de testes automatizados e critérios de aceitação",
            "Reviewer": "Revisa o código, arquitetura e garante a aderência aos padrões da equipe"
        }
        
        rules = {
            "definition_of_ready": "Discovery e Planning devem estar completos com datasets profileados e arquitetura definida.",
            "definition_of_done": "Execution, Tests, Validation, Quality e Certification devem retornar PASS.",
            "decision_rule": "Qualquer mudança arquitetural ou regra nova deve ser registrada como uma Decisão (D-NN) no contexto.",
            "evidence_rule": "Falhas e sucessos operacionais exigem evidências reais do ExecutionResult (ex: exit code).",
            "no_placeholder_rule": "É proibido gerar código com placeholders, comentários de 'TODO' ou lógica vazia.",
            "no_manual_generation_rule": "É proibido pedir para o usuário gerar arquivos manualmente no terminal ou na IDE.",
            "no_invention_rule": "Não inventar regra de negócio. Não inventar colunas. Não inventar resultados.",
            "no_fake_success_rule": "Não declarar sucesso sem evidência (testes, checagens estáticas, execução).",
            "brain_override_rule": "Não permitir que o LLM ignore uma regra do Brain sob NENHUMA circunstância."
        }
        
        for role, desc in roles.items():
            self.rule_registry.register(f"role_{role.lower().replace(' ', '_')}", {
                "rule": f"ROLE {role}: {desc}",
                "tags": ["team_standard", "role"]
            })
            
        for rule_name, desc in rules.items():
            self.rule_registry.register(f"rule_{rule_name}", {
                "rule": f"RULE {rule_name}: {desc}",
                "tags": ["team_standard", "rule"]
            })
    def apply_intelligent_defaults(self, context_request: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica defaults razoáveis para arquitetura e escopo se não especificados."""
        if not context_request.get("architecture"):
            domain = context_request.get("domain", "")
            if domain == "data_engineering":
                context_request["architecture"] = {"architecture_pattern": "Data Lakehouse"}
            elif domain == "analytics":
                context_request["architecture"] = {"architecture_pattern": "Star Schema"}
            else:
                context_request["architecture"] = {"architecture_pattern": "Microservices"}
        return context_request

    def _initialize_core_knowledge(self):
        self.knowledge_registry.register("db_support", {
            "supported_databases": ["PostgreSQL", "MongoDB", "SQLite", "DuckDB", "Snowflake", "BigQuery"],
            "domain": "platform",
            "tags": ["database", "core"]
        })
        self.knowledge_registry.register("lang_support", {
            "supported_languages": ["Python 3.10+", "SQL", "JavaScript", "TypeScript"],
            "domain": "platform",
            "tags": ["language", "core"]
        })
        self.knowledge_registry.register("arch_core", {
            "core_architectures": {
                "monolith": "Ideal para sistemas de pequeno porte e MVPs.",
                "microservices": "Ideal para alta escalabilidade e equipes distribuídas.",
                "data_pipeline": "Ideal para Analytics, ETL/ELT."
            },
            "domain": "platform",
            "tags": ["architecture", "core"]
        })

    def _initialize_core_rules(self):
        self.rule_registry.register("arch_soc", {
            "rule": "Separação de conceitos (SoC).",
            "tags": ["architecture"]
        })
        self.rule_registry.register("arch_cohesion", {
            "rule": "Alta coesão e Baixo acoplamento.",
            "tags": ["architecture"]
        })
        self.rule_registry.register("arch_db_logic", {
            "rule": "Não utilize lógicas de negócio no banco de dados (evite procedures densas).",
            "tags": ["architecture"]
        })
        self.rule_registry.register("sec_crypto", {
            "rule": "Criptografia at-rest para dados sensíveis.",
            "tags": ["security"]
        })
        self.rule_registry.register("sec_privilege", {
            "rule": "Princípio do Menor Privilégio.",
            "tags": ["security"]
        })

    def _initialize_core_patterns(self):
        self.pattern_registry.register("analytics_patterns", {
            "pattern": "Star Schema, ELT, Data Lakehouse",
            "domain": "analytics"
        })

    def generate_context_pack(self, context_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera um Context Pack compacto sob demanda com orçamento configurável.
        """
        context_request = self.apply_intelligent_defaults(context_request)
        
        budget_tokens = context_request.get("max_tokens", 50000)
        # Aproximação conservadora: 1 token = 4 caracteres
        max_chars = budget_tokens * 4
        
        domain = context_request.get("domain", "")
        project_type = context_request.get("project_type", "")
        capabilities = context_request.get("capabilities", [])
        
        # Inicia pack
        pack = {
            "project": {
                "project_type": project_type,
                "business_context": context_request.get("business_context", ""),
                "domain": domain,
            },
            "architecture": context_request.get("architecture", {}),
            "decisions": context_request.get("decisions", []),
            "dataset_profile": context_request.get("dataset_profile", {}),
            "capabilities_requested": capabilities
        }
        
        # Adicionar regras críticas sempre
        pack["team_standards"] = self.get_rules("team_standard")
        
        # Carregamentos sob demanda baseados no contexto
        if context_request.get("fetch_domain_rules"):
            try:
                domain_config = self.domain_registry.get_domain_config(domain)
                pack["domain_rules"] = domain_config
            except Exception:
                pack["domain_rules"] = "Domain not found"
                
        if context_request.get("fetch_platform_stack"):
            platform_kb = self.knowledge_registry.search_by_domain("platform")
            platform_stack = {}
            for kb in platform_kb:
                platform_stack.update({k: v for k, v in kb.items() if k not in ["domain", "tags"]})
            pack["platform_stack"] = platform_stack
            
        if context_request.get("fetch_architecture_rules"):
            pack["architecture_rules"] = self.get_rules("architecture")
            
        if context_request.get("fetch_security_rules"):
            pack["security_rules"] = self.get_rules("security")
            
        if context_request.get("fetch_patterns"):
            domain_lower = (domain or "").lower()
            patterns = self.pattern_registry.search_by_domain(domain_lower)
            if patterns:
                pack["domain_patterns"] = f"Padrões recomendados: {patterns[0].get('pattern')}"

        # Aplicar controle de limite de tamanho de forma ingênua/segura
        import json
        pack_str = json.dumps(pack)
        if len(pack_str) > max_chars:
            logger.warning("Context Pack excede o orçamento de tokens. Realizando poda.")
            pack.pop("platform_stack", None)
            pack.pop("dataset_profile", None)
            
        return pack

    def retrieve_relevant_knowledge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Delega para a nova função mantendo compatibilidade
        return self.generate_context_pack(context)

    def inject_project_context(self, project_id: str, key: str, value: Any):
        """Permite que os agentes alimentem o Brain com decisões do projeto."""
        if project_id not in self.project_knowledge:
            self.project_knowledge[project_id] = {}
        self.project_knowledge[project_id][key] = value

    def get_rules(self, category: str) -> list:
        rules = self.rule_registry.search_by_tags([category])
        return [r.get("rule") for r in rules]
