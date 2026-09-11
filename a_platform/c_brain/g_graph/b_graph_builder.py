import os
import logging
from typing import Dict, Any

from a_platform.a_core.b_domain.i_execution_context import ExecutionContext
from a_platform.c_brain.g_graph.a_backend import ObsidianBackend, GraphifyBackend

logger = logging.getLogger(__name__)

class GraphBuilder:
    """
    Constrói a abstração de Grafo representando a arquitetura real e dinâmica.
    Exporta para Obsidian (Markdown) e Graphify (JSON) através dos backends.
    """
    def __init__(self):
        # Os artefatos devem ser gerados como runtime_artifacts, não na raiz
        base_dir = os.path.join(os.getcwd(), "e_generated_projects", "runtime_artifacts")
        os.makedirs(base_dir, exist_ok=True)
        self.obsidian_backend = ObsidianBackend(os.path.join(base_dir, "obsidian"))
        self.graphify_backend = GraphifyBackend(os.path.join(base_dir, "graphify"))
        self.base_dir = base_dir
        
    def build_graph(self, context: ExecutionContext) -> Dict[str, Any]:
        nodes = []
        edges = []
        
        # 7. O grafo deve representar: Project -> Context -> Dataset -> Decision -> Domain -> Capability -> Skill -> Agent -> MCP -> Gate
        
        # 1. Project
        proj_id = f"project_{context.project_id}"
        nodes.append({"id": proj_id, "type": "Project", "label": context.domain or "Generic"})
        
        # 2. Context
        ctx_id = f"context_{context.project_id}"
        nodes.append({"id": ctx_id, "type": "Context", "label": "Project Context"})
        edges.append({"source": proj_id, "target": ctx_id, "relation": "HAS_CONTEXT"})
        
        # 3. Dataset
        ds_id = f"dataset_{context.project_id}"
        dataset_name = context.dataset_profile.get("file_name", "Raw Data") if context.dataset_profile else "No Data"
        nodes.append({"id": ds_id, "type": "Dataset", "label": dataset_name})
        edges.append({"source": ctx_id, "target": ds_id, "relation": "USES_DATASET"})
        
        # 4. Decision (Architecture)
        dec_id = f"decision_{context.project_id}"
        pattern = context.architecture_decision.get("architecture_pattern", "Unknown") if context.architecture_decision else "None"
        nodes.append({"id": dec_id, "type": "Decision", "label": pattern})
        edges.append({"source": ds_id, "target": dec_id, "relation": "DRIVES_DECISION"})
        
        # 5. Domain
        dom_id = f"domain_{context.domain}"
        nodes.append({"id": dom_id, "type": "Domain", "label": context.domain})
        edges.append({"source": dec_id, "target": dom_id, "relation": "BELONGS_TO_DOMAIN"})
        
        # Extract details from project plan if available
        if context.project_plan and context.project_plan.tasks:
            for task in context.project_plan.tasks:
                # 6. Capability (Task acts as Capability requirement here)
                cap_id = f"capability_{task.id}"
                nodes.append({"id": cap_id, "type": "Capability", "label": task.name})
                edges.append({"source": dom_id, "target": cap_id, "relation": "REQUIRES_CAPABILITY"})
                
                # 7. Skill
                for skill in task.skills:
                    skill_id = f"skill_{skill}"
                    if not any(n["id"] == skill_id for n in nodes):
                        nodes.append({"id": skill_id, "type": "Skill", "label": skill})
                    edges.append({"source": cap_id, "target": skill_id, "relation": "USES_SKILL"})
                    
                    # 8. Agent
                    agent_id = f"agent_{task.agent}"
                    if not any(n["id"] == agent_id for n in nodes):
                        nodes.append({"id": agent_id, "type": "Agent", "label": task.agent})
                    edges.append({"source": skill_id, "target": agent_id, "relation": "EXECUTED_BY"})
                    
                    # 9. MCP
                    for mcp in task.mcps:
                        mcp_id = f"mcp_{mcp}"
                        if not any(n["id"] == mcp_id for n in nodes):
                            nodes.append({"id": mcp_id, "type": "MCP", "label": mcp})
                        edges.append({"source": agent_id, "target": mcp_id, "relation": "UTILIZES_MCP"})
                        
                        # 10. Gate (Validators/Expected Artifacts)
                        for artifact in task.expected_artifacts:
                            gate_id = f"gate_{artifact}"
                            if not any(n["id"] == gate_id for n in nodes):
                                nodes.append({"id": gate_id, "type": "Gate", "label": artifact})
                            edges.append({"source": mcp_id, "target": gate_id, "relation": "VALIDATED_BY"})

        graph_data = {
            "nodes": nodes,
            "edges": edges
        }
        
        # Exporta grafos usando os backends
        self.obsidian_backend.export_graph(context.project_id, graph_data)
        self.graphify_backend.export_graph(context.project_id, graph_data)
        
        return graph_data
