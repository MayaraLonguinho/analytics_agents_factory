from typing import Any, Dict, List
import os

class ObsidianGraphBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def build_graph(self, nodes: List[Dict[str, Any]]) -> None:
        """
        Builds markdown files with Obsidian wikilinks [[...]]
        nodes: [{"id": "NodeA", "content": "...", "links": ["NodeB", "NodeC"]}]
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            
        for node in nodes:
            file_path = os.path.join(self.output_dir, f"{node['id']}.md")
            with open(file_path, "w") as f:
                f.write(f"# {node['id']}\n\n")
                f.write(node.get("content", "") + "\n\n")
                
                links = node.get("links", [])
                if links:
                    f.write("## Related\n")
                    for link in links:
                        f.write(f"- [[{link}]]\n")
