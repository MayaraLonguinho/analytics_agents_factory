"""Skill Architecture - INDEX

## Overview
Reusable skill library with 30+ skills organized by domain and execution type.

## Architecture Principles
1. **Reusable Components**: Skills are composable and reusable across agents
2. **No Direct Execution**: Skills are invoked through SkillRegistry only
3. **Declarative Interface**: SkillContract defines inputs, outputs, dependencies
4. **Multiple Execution Types**: native (Python), llm (Language Model), mcp (Model Context Protocol), composite (multi-skill)
5. **Type Safety**: Input/output validation against schema
6. **Brain Integration**: Skills reference Brain knowledge when needed

## Skill Categories

### Discovery (2 skills)
- discover_intent: Extract intent from natural language
- question_generation: Generate discovery questions

### Dataset Skills (4 skills)
- profile_csv_dataset: Comprehensive dataset analysis
- detect_data_types: Infer column data types
- analyze_data_quality: Assess quality metrics
- (more in dataset subtree)

### Analytics Skills (3 skills)
- generate_eda_report: Exploratory data analysis
- detect_correlations: Find column correlations
- generate_visualizations: Create charts and visualizations

### Data Engineering (4 skills)
- extract_csv_source: Load CSV files
- transform_data: Apply transformations
- validate_data_schema: Schema validation
- (load skill in d_load/)

### Development (backend, frontend, database, infrastructure)
- design_api_structure: Design REST APIs
- (more development skills)

### Quality & Certification (3 skills)
- generate_test_cases: Create test specifications
- validate_deliverables: Verify requirements
- certify_project: Create certification certificate

## File Structure
```
d_skills/
  ├── skill_contract.py          # SkillContract & ISkill interface
  ├── registry.py                # SkillRegistry for discovery
  ├── declarations/
  │   └── skills.yaml            # All skill declarations
  ├── a_discovery/
  │   ├── intent_discovery.py
  │   └── question_generator.py
  ├── b_dataset/
  │   ├── b_profiling/
  │   │   └── profiler.py
  │   ├── c_schema_detection/
  │   │   └── type_detector.py
  │   └── d_quality_analysis/
  │       └── quality_analyzer.py
  ├── c_analytics/
  │   ├── a_eda/
  │   ├── b_metrics/
  │   ├── c_visualization/
  │   └── d_statistical_analysis/
  ├── d_data_engineering/
  │   ├── a_extract/
  │   ├── b_transform/
  │   ├── c_validate/
  │   └── d_load/
  ├── e_development/
  │   ├── a_backend/
  │   ├── b_frontend/
  │   ├── c_database/
  │   └── d_infrastructure/
  └── f_quality/
      ├── a_testing/
      ├── b_validation/
      └── c_certification/
```

## Key Contracts

### SkillContract
```python
@dataclass
class SkillContract:
    skill_id: str
    name: str
    execution_type: SkillExecutionType  # native, llm, mcp, composite
    input_schema: List[ParameterDefinition]
    output_schema: List[ParameterDefinition]
    dependencies: List[str]              # Other skill IDs
    compatible_agents: List[str]         # Agent IDs that can use it
    required_brain_context: List[str]    # Knowledge/rules needed
```

### ParameterDefinition
```python
@dataclass
class ParameterDefinition:
    name: str
    data_type: str                       # string, integer, float, etc
    required: bool
    default_value: Optional[Any]
    constraints: Dict[str, Any]          # min, max, pattern, enum
```

## Execution Types

### NATIVE (Python)
- Direct Python implementation
- Examples: profile_csv_dataset, extract_csv_source, analyze_data_quality
- No external tools needed

### LLM (Language Model)
- Uses Brain and LLM for reasoning
- Examples: design_api_structure, generate_test_cases, question_generation
- Requires LLM provider (configured in b_ai_engine/b_llm_gateway)

### MCP (Model Context Protocol)
- Invokes external MCP servers
- Examples: specialized analytics, external APIs, domain experts
- Requires MCP server registration

### COMPOSITE (Multi-Skill)
- Chains multiple skills together
- Example: eda_analysis = profile + detect_correlations + generate_visualizations
- Orchestrated by SkillRegistry

## Integration Points

### With Agents
- Agents only invoke skills via SkillRegistry
- Skills input/output validated against contracts
- Agent provides required context

### With Brain
- Skills query Brain for patterns and rules
- Knowledge from a_platform.c_brain/declarations/
- Rules enforce quality constraints

### With Orchestrator
- Orchestrator coordinates agents
- Agents coordinate skills
- Skills execute actual work

## Skill Execution Protocol
1. Agent calls SkillRegistry.execute_skill(skill_id, input_data)
2. Registry validates input against SkillContract.input_schema
3. Registry instantiates skill implementation
4. Skill.execute(input_data) runs
5. Registry validates output against SkillContract.output_schema
6. Result returned to agent

## Next Steps
1. Implement core skill classes in each category
2. Create native Python skills first (dataset, analytics, data_engineering)
3. Create LLM skills with Brain integration (discovery, development)
4. Create MCP skill framework
5. Create composite skill orchestrator
6. Integrate with SkillRegistry
7. Connect to agents via allowed_skills
"""
