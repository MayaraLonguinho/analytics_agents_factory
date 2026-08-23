from typing import Dict, Any
from a_platform.a_core.b_domain.project_request import ProjectRequest

class GraphBuilder:
    """
    Constrói a abstração de Grafo representando a arquitetura real e dinâmica.
    Compatível conceitualmente com Obsidian e Graphify.
    """
    def __init__(self):
        pass
        
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
            if key != "status":
                node_id = f"req_{key}"
                nodes.append({"id": node_id, "type": "Requirement", "label": value})
                edges.append({"source": request.project_id, "target": node_id, "relation": "HAS_CONSTRAINT"})
                
        return {
            "nodes": nodes,
            "edges": edges
        }
