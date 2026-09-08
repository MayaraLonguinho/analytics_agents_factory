import sys
import os

# Ensure the package is in PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.i_domains.domain_registry import DomainRegistry

def test_business_context_independence():
    registry = DomainRegistry()
    
    # Test 1: Finance Context with Analytics Domain
    try:
        domain = registry.normalize_domain("analytics")
        config = registry.get_domain_config(domain)
        print("Test 1 (Finance + Analytics): OK")
    except Exception as e:
        print(f"Test 1 Failed: {e}")
        
    # Test 2: Sales Context with Data Engineering Domain
    try:
        domain2 = registry.normalize_domain("data_engineering")
        config2 = registry.get_domain_config(domain2)
        print("Test 2 (Sales + Data Eng): OK")
    except Exception as e:
        print(f"Test 2 Failed: {e}")

    # Test 3: LLM accidentally sets domain to "finance"
    try:
        domain3 = registry.normalize_domain("finance")
        config3 = registry.get_domain_config(domain3)
        print("Test 3 Failed: Should not allow finance as domain")
    except Exception as e:
        print(f"Test 3 (Invalid domain rejected): OK - {e}")

if __name__ == '__main__':
    test_business_context_independence()
