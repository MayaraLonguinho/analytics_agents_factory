import os
import logging
from typing import Dict, Any

from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.c_brain.f_graph.a_graph_backend import ObsidianBackend

logger = logging.getLogger(__name__)

class GraphBuilder:
    """
    Constrói a abstração de Grafo representando a arquitetura real e dinâmica.
    Exporta apenas para Obsidian (Markdown).
    """
    def __init__(self, brain=None):
        self.brain = brain
        # Os artefatos operacionais ficam no runtime
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "j_runtime", "c_artifacts", "graph")
        os.makedirs(base_dir, exist_ok=True)
        self.obsidian_backend = ObsidianBackend(base_dir)
        self.base_dir = base_dir
        
    def build_graph(self, context: ExecutionContext) -> Dict[str, Any]:
        nodes = []
        edges = []
        
        # O objetivo é desenhar nomes limpos como IDs
        
        # 1. Project
        proj_name = context.project_type or f"Project {context.project_id[:4]}"
        nodes.append({"id": proj_name, "type": "Project", "label": proj_name})
        
        # 2. Domain
        dom_name = context.domain or "Generic Domain"
        nodes.append({"id": dom_name, "type": "Domain", "label": dom_name})
        edges.append({"source": proj_name, "target": dom_name, "relation": "BELONGS_TO"})
        
        # Se houver regras do domínio no Brain, podemos linkar
        if self.brain:
            try:
                # Add brain core reference
                nodes.append({"id": "Brain", "type": "System", "label": "Brain"})
                edges.append({"source": dom_name, "target": "Brain", "relation": "MANAGED_BY"})
                
                # Add basic patterns from Brain for this domain
                patterns = self.brain.pattern_registry.search_by_domain(dom_name.lower())
                for p in patterns:
                    pat_name = p.get("pattern", "Unknown Pattern")
                    if pat_name:
                        nodes.append({"id": pat_name, "type": "Pattern", "label": pat_name})
                        edges.append({"source": dom_name, "target": pat_name, "relation": "HAS_PATTERN"})
            except Exception:
                pass

        # 3. Dataset/Source
        ds_name = "CSV" # Default assumption from example if not explicitly typed, normally extracted from dataset_profile
        if context.dataset_profile and context.dataset_profile.get("file_name"):
            ds_name = context.dataset_profile.get("file_name").split(".")[-1].upper()
            if not ds_name: ds_name = "Raw Data"
            
        nodes.append({"id": ds_name, "type": "Dataset", "label": ds_name})
        edges.append({"source": proj_name, "target": ds_name, "relation": "USES_SOURCE"})
        
        # 4. Decisions
        for dec in context.decisions:
            dec_id = dec.id
            nodes.append({"id": dec_id, "type": "Decision", "label": dec.decision})
            edges.append({"source": proj_name, "target": dec_id, "relation": "HAS_DECISION"})

        # Extract details from project plan if available
        if context.project_plan and context.project_plan.tasks:
            prev_node = ds_name
            for task in context.project_plan.tasks:
                
                # Agent
                agent_name = task.assigned_agent or "GenericAgent"
                if not any(n["id"] == agent_name for n in nodes):
                    nodes.append({"id": agent_name, "type": "Agent", "label": agent_name})
                edges.append({"source": prev_node, "target": agent_name, "relation": "PROCESSED_BY"})
                
                # Skills
                for skill in task.required_skills:
                    if not any(n["id"] == skill for n in nodes):
                        nodes.append({"id": skill, "type": "Skill", "label": skill})
                    edges.append({"source": agent_name, "target": skill, "relation": "USES_SKILL"})
                    
                # 6. Capability (Task acts as Capability requirement here)
                cap_id = f"capability_{task.task_id}"
                if not any(n["id"] == cap_id for n in nodes):
                    nodes.append({"id": cap_id, "type": "Capability", "label": cap_id})
                edges.append({"source": agent_name, "target": cap_id, "relation": "REQUIRES_CAPABILITY"})
                    
                prev_node = agent_name # Chain agents

        graph_data = {
            "nodes": nodes,
            "edges": edges
        }
        
        # Exporta grafos usando o backend
        self.obsidian_backend.export_graph(context.project_id, graph_data)
        
        return graph_data
