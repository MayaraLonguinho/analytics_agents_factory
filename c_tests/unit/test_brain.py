import pytest
import time
import shutil
import os
from a_platform.c_brain.e_memory.memory_manager import MemoryManager
from a_platform.c_brain.f_registry.knowledge_registry import KnowledgeRegistry
from a_platform.c_brain.f_registry.rule_registry import RuleRegistry
from a_platform.c_brain.f_registry.pattern_registry import PatternRegistry
from a_platform.c_brain.g_graph.obsidian.graph_builder import ObsidianGraphBuilder

def test_memory_manager():
    mm = MemoryManager()
    mm.store_session_history("s1", {"action": "login"})
    hist = mm.get_session_history("s1")
    assert len(hist) == 1
    assert "timestamp" in hist[0]
    
    mm.store_architectural_decision("p1", {"desc": "use python"})
    decisions = mm.get_architectural_decisions("p1")
    assert len(decisions) == 1
    
    mm.store_execution_memory("e1", {"status": "running"})
    exec_mem = mm.get_execution_memory("e1")
    assert exec_mem["status"] == "running"

def test_knowledge_registry_performance():
    kr = KnowledgeRegistry()
    for i in range(1000):
        kr.register(f"k{i}", {"domain": "finance", "tags": [f"tag{i%10}"]})
    
    start_time = time.time()
    results = kr.search_by_domain("finance")
    end_time = time.time()
    
    assert len(results) == 1000
    assert (end_time - start_time) < 0.05  # Less than 50ms

def test_rule_registry():
    rr = RuleRegistry()
    rr.register("r1", {"tags": ["security"]})
    assert rr.get("r1")["severity"] == "info"
    
    results = rr.search_by_tags(["security"])
    assert len(results) == 1

def test_pattern_registry():
    pr = PatternRegistry()
    pr.register("p1", {"domain": "frontend"})
    assert len(pr.search_by_domain("frontend")) == 1

def test_graph_builder():
    output_dir = "/tmp/test_obsidian_graph"
    builder = ObsidianGraphBuilder(output_dir)
    
    nodes = [
        {"id": "BrainCore", "content": "Core system", "links": ["Memory", "Rules"]},
        {"id": "Memory", "content": "Memory system", "links": []}
    ]
    
    builder.build_graph(nodes)
    
    assert os.path.exists(os.path.join(output_dir, "BrainCore.md"))
    with open(os.path.join(output_dir, "BrainCore.md"), "r") as f:
        content = f.read()
        assert "[[Memory]]" in content
        
    shutil.rmtree(output_dir)
