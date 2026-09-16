from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class MCPDefinition:
    id: str
    name: str
    version: str = "1.0.0"
    capabilities: List[str] = field(default_factory=list)
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    execution_mode: str = "local"
    description: str = ""


class MCPRegistry:
    """Single source of truth for all available MCPs."""

    def __init__(self, manifest_path: Optional[str | Path] = None):
        self.manifest_path = Path(manifest_path) if manifest_path else Path(__file__).with_name("d_mcp_manifest.yaml")
        self.mcps: Dict[str, MCPDefinition] = {}
        self.by_capability: Dict[str, List[str]] = {}
        self._load_manifest()

    def _load_manifest(self) -> None:
        if not self.manifest_path.exists():
            return

        with self.manifest_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        for item in data.get("mcps", []):
            definition = MCPDefinition(
                id=item["id"],
                name=item["name"],
                version=item.get("version", "1.0.0"),
                capabilities=item.get("capabilities", []),
                input_schema=item.get("input_schema", {}),
                output_schema=item.get("output_schema", {}),
                permissions=item.get("permissions", []),
                configuration=item.get("configuration", {}),
                execution_mode=item.get("execution_mode", "local"),
                description=item.get("description", ""),
            )
            self.mcps[definition.id] = definition
            for capability in definition.capabilities:
                self.by_capability.setdefault(capability, []).append(definition.id)

    def register_mcp(self, definition: MCPDefinition) -> None:
        self.mcps[definition.id] = definition
        for capability in definition.capabilities:
            self.by_capability.setdefault(capability, []).append(definition.id)

    def get_mcp(self, mcp_id: str) -> Optional[MCPDefinition]:
        return self.mcps.get(mcp_id)

    def list_mcps(self) -> List[MCPDefinition]:
        return list(self.mcps.values())

    def list_capability(self, capability: str) -> List[MCPDefinition]:
        ids = self.by_capability.get(capability, [])
        return [self.mcps[mcp_id] for mcp_id in ids if mcp_id in self.mcps]

    def to_dict(self) -> Dict[str, Any]:
        return {mcp_id: {
            "id": mcp.id,
            "name": mcp.name,
            "version": mcp.version,
            "capabilities": mcp.capabilities,
            "permissions": mcp.permissions,
            "execution_mode": mcp.execution_mode,
        } for mcp_id, mcp in self.mcps.items()}
