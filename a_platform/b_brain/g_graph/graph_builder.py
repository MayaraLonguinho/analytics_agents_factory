import os
import logging
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.b_brain.g_graph.backend import ObsidianBackend, GraphifyBackend

logger = logging.getLogger(__name__)

class GraphBuilder:
    """
    Constrói a abstração de Grafo representando a arquitetura real e dinâmica.
    Exporta para Obsidian (Markdown) e Graphify (JSON) através dos backends.
    """
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.obsidian_backend = ObsidianBackend(os.path.join(base_dir, "obsidian"))
        self.graphify_backend = GraphifyBackend(os.path.join(base_dir, "graphify"))
        
    def build_graph(self, request: ProjectRequest) -> Dict[str, Any]:
        nodes = []
        edges = []
        
        # 1. Project Node
        nodes.append({"id": request.project_id, "type": "Project", "label": request.domain or "Generic"})
        
        # 2. Dataset Nodes
        if request.dataset_profile:
            ds_id = f"dataset_{request.project_id}"
            nodes.append({"id": ds_id, "type": "Dataset", "label": request.dataset_profile.get("file_name", "Raw Data")})
            edges.append({"source": request.project_id, "target": ds_id, "relation": "CONSUMES"})
            
            # Extract features from dataset profile for the graph
            for col, stats in request.dataset_profile.get("columns", {}).items():
                col_id = f"col_{col}"
                nodes.append({"id": col_id, "type": "Feature", "label": col, "dtype": stats["type"]})
                edges.append({"source": ds_id, "target": col_id, "relation": "CONTAINS"})
                
        # 3. Discovery Constraints
        for key, value in request.discovery_data.items():
            if key != "status" and key != "history" and value:
                node_id = f"req_{key}"
                nodes.append({"id": node_id, "type": "Requirement", "label": str(value)[:50]})
                edges.append({"source": request.project_id, "target": node_id, "relation": "HAS_CONSTRAINT"})
                
        # 4. Architecture Node (if available)
        if request.architecture_decision:
            arch_id = f"arch_{request.project_id}"
            pattern = request.architecture_decision.get("architecture_pattern", "Unknown")
            nodes.append({"id": arch_id, "type": "Architecture", "label": pattern})
            edges.append({"source": request.project_id, "target": arch_id, "relation": "USES_ARCHITECTURE"})
            
        # 5. Project Plan Nodes (Tasks, Agents, Artifacts)
        if request.project_plan and request.project_plan.tasks:
            for task in request.project_plan.tasks:
                task_id = f"task_{task.id}"
                nodes.append({"id": task_id, "type": "Task", "label": task.name})
                edges.append({"source": request.project_id, "target": task_id, "relation": "HAS_TASK"})
                
                if task.agent:
                    agent_id = f"agent_{task.agent}"
                    # Avoid duplicate agent nodes
                    if not any(n["id"] == agent_id for n in nodes):
                        nodes.append({"id": agent_id, "type": "Agent", "label": task.agent})
                    edges.append({"source": task_id, "target": agent_id, "relation": "ASSIGNED_TO"})
                    
                for dep in task.dependencies:
                    dep_id = f"task_{dep}"
                    edges.append({"source": task_id, "target": dep_id, "relation": "DEPENDS_ON"})
                    
                for artifact in task.expected_artifacts:
                    art_id = f"artifact_{artifact}"
                    if not any(n["id"] == art_id for n in nodes):
                        nodes.append({"id": art_id, "type": "Artifact", "label": artifact})
                    edges.append({"source": task_id, "target": art_id, "relation": "PRODUCES"})

        graph_data = {
            "nodes": nodes,
            "edges": edges
        }
        
        # Exporta grafos usando os backends
        self.obsidian_backend.export_graph(request.project_id, graph_data)
        self.graphify_backend.export_graph(request.project_id, graph_data)
        
        return graph_data
