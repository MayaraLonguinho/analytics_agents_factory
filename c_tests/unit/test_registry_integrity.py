# pyrefly: ignore [missing-import]
import pytest
import os
import yaml

def test_registry_integrity():
    registry_path = os.path.join(os.getcwd(), "a_platform", "h_domains", "registry.yaml")
    
    with open(registry_path, "r") as f:
        registry = yaml.safe_load(f)
        
    domains = registry.get("domains", {})
    assert "analytics" in domains
    
    # Check if all MCPS in registry exist in mcp_executor
    from a_platform.e_mcp.mcp_executor import MCPExecutor
    executor = MCPExecutor()
    valid_mcps = ["filesystem_mcp", "git_mcp", "docker_mcp", "database_mcp", "browser_mcp"]
    
    for domain, data in domains.items():
        for mcp in data.get("mcps", []):
            assert mcp in valid_mcps, f"MCP {mcp} not valid"
            
    # Check if all skills in registry exist in SkillRegistry
    from a_platform.d_skills.skill_registry import SkillRegistry
    skill_registry = SkillRegistry()
    
    for domain, data in domains.items():
        for skill in data.get("skills", []):
            assert skill in skill_registry.skills, f"Skill {skill} not found in SkillRegistry"
