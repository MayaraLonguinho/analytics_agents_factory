import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GraphBackend(ABC):
    @abstractmethod
    def export_graph(self, project_id: str, graph_data: Dict[str, Any]) -> None:
        pass

class ObsidianBackend(GraphBackend):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def export_graph(self, project_id: str, graph_data: Dict[str, Any]) -> None:
        project_obsidian_dir = os.path.join(self.output_dir, project_id)
        os.makedirs(project_obsidian_dir, exist_ok=True)
        
        # Cria arquivos markdown para os nós
        for node in graph_data.get("nodes", []):
            node_id = node.get("id")
            node_type = node.get("type", "Unknown")
            node_label = node.get("label", "")
            
            # Identifica arestas ligadas a este nó para wikilinks
            links = []
            for edge in graph_data.get("edges", []):
                if edge["source"] == node_id:
                    links.append(f"[[{edge['target']}]] ({edge['relation']})")
                    
            content = f"---\ntype: {node_type}\nproject: {project_id}\n---\n\n"
            content += f"# {node_label}\n\n"
            if links:
                content += "## Links\n" + "\n".join(f"- {l}" for l in links)
                
            file_path = os.path.join(project_obsidian_dir, f"{node_id}.md")
            try:
                with open(file_path, "w") as f:
                    f.write(content)
            except Exception as e:
                logger.error(f"[ObsidianBackend] Falha ao gravar {file_path}: {e}")
        
        logger.info(f"[ObsidianBackend] Grafo exportado para Obsidian em {project_obsidian_dir}")

class GraphifyBackend(GraphBackend):
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def export_graph(self, project_id: str, graph_data: Dict[str, Any]) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, f"{project_id}_graphify.json")
        
        try:
            with open(file_path, "w") as f:
                json.dump(graph_data, f, indent=2)
            logger.info(f"[GraphifyBackend] Grafo exportado para Graphify em {file_path}")
        except Exception as e:
            logger.error(f"[GraphifyBackend] Falha ao gravar {file_path}: {e}")
