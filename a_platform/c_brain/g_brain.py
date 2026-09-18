import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GenericRegistry:
    def __init__(self):
        self.data = {}
    
    def register(self, key: str, value: Any):
        self.data[key] = value

    def search_by_tags(self, tags: List[str]) -> List[Any]:
        results = []
        for v in self.data.values():
            if isinstance(v, dict) and "tags" in v:
                if any(t in v["tags"] for t in tags):
                    results.append(v)
        return results

    def search_by_domain(self, domain: str) -> List[Any]:
        results = []
        for v in self.data.values():
            if isinstance(v, dict) and v.get("domain") == domain:
                results.append(v)
        return results

class KnowledgeRegistry(GenericRegistry): pass
class RuleRegistry(GenericRegistry): pass
class PatternRegistry(GenericRegistry): pass

from a_platform.c_brain.d_domains.a_domain_registry import DomainRegistry
from a_platform.f_mcps.d_registry.a_registry import MCPRegistry
from a_platform.e_skills.h_registry.a_skill_registry import SkillRegistry
from a_platform.g_agents.o_registry.a_registry import AgentRegistry

class Brain:
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
        
        self.project_knowledge = {}

    def _initialize_team_standards(self):
        roles = {
            "Owner": "Decide regras de negócio e prioridades",
            "Architect": "Decide a stack tecnológica",
            "Data Engineer": "Responsável por pipelines",
            "Analytics Engineer": "Responsável por modelagem",
            "QA": "Garante a qualidade",
            "Reviewer": "Revisa o código"
        }
        
        rules = {
            "definition_of_ready": "Discovery e Planning completos.",
            "definition_of_done": "Execution, Tests, Validation, Quality e Certification retornam PASS.",
            "decision_rule": "Mudança deve ser D-NN.",
            "evidence_rule": "Não retornar fake success.",
            "no_placeholder_rule": "Proibido placeholders.",
            "no_manual_generation_rule": "Proibido tarefas manuais.",
            "no_invention_rule": "Não inventar colunas ou dados.",
            "no_fake_success_rule": "Não declarar sucesso sem evidência.",
            "brain_override_rule": "O LLM não ignora regras."
        }
        
        for role, desc in roles.items():
            self.rule_registry.register(f"role_{role.lower().replace(" ", "_")}", {
                "rule": f"ROLE {role}: {desc}", "tags": ["team_standard", "role"]
            })
            
        for rule_name, desc in rules.items():
            self.rule_registry.register(f"rule_{rule_name}", {
                "rule": f"RULE {rule_name}: {desc}", "tags": ["team_standard", "rule"]
            })
            
    def apply_intelligent_defaults(self, context_request: Dict[str, Any]) -> Dict[str, Any]:
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
            "supported_databases": ["PostgreSQL", "MongoDB", "SQLite", "Snowflake", "BigQuery"],
            "domain": "platform", "tags": ["database", "core"]
        })
        self.knowledge_registry.register("lang_support", {
            "supported_languages": ["Python 3.10+", "SQL", "JavaScript", "TypeScript"],
            "domain": "platform", "tags": ["language", "core"]
        })
        self.knowledge_registry.register("arch_core", {
            "core_architectures": {
                "monolith": "Ideal para MVPs.",
                "microservices": "Ideal para escalabilidade.",
                "data_pipeline": "Ideal para Analytics."
            },
            "domain": "platform", "tags": ["architecture", "core"]
        })

    def _initialize_core_rules(self):
        self.rule_registry.register("arch_soc", {"rule": "SoC.", "tags": ["architecture"]})
        self.rule_registry.register("arch_cohesion", {"rule": "Alta coesão.", "tags": ["architecture"]})
        self.rule_registry.register("arch_db_logic", {"rule": "Sem lógica densa no banco.", "tags": ["architecture"]})
        self.rule_registry.register("sec_crypto", {"rule": "Criptografia.", "tags": ["security"]})
        self.rule_registry.register("sec_privilege", {"rule": "Menor privilégio.", "tags": ["security"]})

    def _initialize_core_patterns(self):
        self.pattern_registry.register("analytics_patterns", {
            "pattern": "Star Schema, ELT, Data Lakehouse", "domain": "analytics"
        })

    def generate_context_pack(self, context_request: Dict[str, Any]) -> Dict[str, Any]:
        context_request = self.apply_intelligent_defaults(context_request)
        max_chars = context_request.get("max_tokens", 50000) * 4
        
        pack = {
            "project": {
                "project_type": context_request.get("project_type", ""),
                "business_context": context_request.get("business_context", ""),
                "domain": context_request.get("domain", ""),
            },
            "architecture": context_request.get("architecture", {}),
            "decisions": context_request.get("decisions", []),
            "dataset_profile": context_request.get("dataset_profile", {}),
            "capabilities_requested": context_request.get("capabilities", [])
        }
        
        pack["team_standards"] = self.get_rules("team_standard")
        
        import json
        pack_str = json.dumps(pack)
        if len(pack_str) > max_chars:
            pack.pop("dataset_profile", None)
            
        return pack

    def retrieve_relevant_knowledge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return self.generate_context_pack(context)

    def inject_project_context(self, project_id: str, key: str, value: Any):
        if project_id not in self.project_knowledge:
            self.project_knowledge[project_id] = {}
        self.project_knowledge[project_id][key] = value

    def get_rules(self, category: str) -> list:
        rules = self.rule_registry.search_by_tags([category])
        return [r.get("rule") for r in rules]

__all__ = ["Brain"]
