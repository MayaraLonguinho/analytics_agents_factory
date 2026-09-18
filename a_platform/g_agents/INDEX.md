"""Agent Architecture - INDEX

## Overview
Consolidated agent architecture with 15 specialized agents for Analytics AI Factory.

## Architecture Principles
1. **Separation of Concerns**: Each agent handles a single responsibility
2. **No Direct LLM Access**: Agents ONLY coordinate Skills
3. **Skill Coordination**: Agents delegate execution to Skills via SkillRegistry
4. **Brain Integration**: Agents reference Brain for rules, knowledge, patterns
5. **Contract-Based Interface**: AgentContract defines obligations and interface
6. **YAML Declarations**: All agents defined in declarations/agents.yaml

## Agent Tiers

### Tier 1: Orchestration
- **orchestrator**: Main lifecycle orchestrator (REQUESTED → DELIVERING)

### Tier 2: Strategy
- **discovery_agent**: Requirements elicitation and clarification
- **architecture_agent**: Technical design
- **planner_agent**: Project execution planning

### Tier 3: Implementation
- **data_agent**: Dataset extraction, profiling, preparation
- **database_agent**: Database schema design
- **backend_agent**: Backend services development
- **frontend_agent**: UI/Frontend development
- **analytics_agent**: Data analysis and insights
- **infrastructure_agent**: Deployment infrastructure

### Tier 4: Quality & Delivery
- **testing_agent**: Test planning and execution
- **documentation_agent**: Project documentation
- **execution_agent**: Code generation and materialization
- **validation_agent**: Deliverable verification
- **certification_agent**: Project sign-off and certification

## File Structure
```
c_agents/
  ├── agent_contract.py          # AgentContract & IAgent interface
  ├── registry.py                # AgentRegistry for discovery
  ├── declarations/
  │   └── agents.yaml            # All agent declarations
  ├── a_orchestrator/
  │   ├── __init__.py
  │   └── orchestrator.py        # OrchestratorAgent implementation
  ├── b_discovery/
  │   └── discovery_agent.py
  ├── c_architecture/
  │   └── architecture_agent.py
  ├── d_planner/
  │   └── planner_agent.py
  └── ... (other agent implementations)
```

## Key Contracts

### AgentContract
```python
@dataclass
class AgentContract:
    agent_id: str
    name: str
    responsibility: str
    input_schema: Dict[str, Any]      # Input contract
    output_schema: Dict[str, Any]     # Output contract
    allowed_skills: List[str]         # Constraint: only these skills
    applicable_rules: List[str]       # Brain rules to enforce
    required_context: List[str]       # Context types needed
```

### Agent Execution Flow
1. Agent receives input
2. Validate input against contract schema
3. Identify required skills from allowed_skills
4. Invoke SkillRegistry to execute skills
5. Collect skill outputs
6. Return output according to output_schema

## Integration Points

### With Brain
- Reference applicable_rules during execution
- Query for knowledge and patterns to guide decisions
- Enforce Brain rules as constraints

### With Skills
- Skill execution via SkillRegistry
- Pass input to skill, validate output
- Chain skills if needed (depends_on relationships)

### With Orchestrator
- Orchestrator delegates to specific agents
- Agents report back with results
- Orchestrator coordinates across agents

## Next Steps
1. Implement core agent classes
2. Create agent implementations for Tier 1-2 (orchestrator, discovery, architecture)
3. Create agent implementations for Tier 3 (data, backend, analytics)
4. Create agent implementations for Tier 4 (validation, certification)
5. Create SkillExecutor for agent-skill coordination
6. Integrate with orchestrator
"""
