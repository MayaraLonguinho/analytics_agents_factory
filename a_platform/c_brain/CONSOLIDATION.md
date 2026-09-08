# Central Brain — Consolidation & Architecture

## Overview

The Analytics AI Factory now has a unified, centralized Brain (at `c_brain/`) that consolidates all knowledge, rules, patterns, and context from the previous distributed implementations (`c_brain/` and `b_ai_engine/a_brain/`).

## Consolidation Strategy

### Removed Conflicts

The new centralized Brain eliminates competing implementations:

- **Deprecated**: `c_brain/` (older, simpler Brain implementation)
- **Deprecated**: `b_ai_engine/a_brain/` (larger, documentation-focused Brain)
- **Active**: `c_brain/` (canonical, unified Brain)

### Knowledge Reuse

All valuable knowledge has been consolidated:

- Architecture principles (Clean Architecture, SOLID)
- Domain templates (Analytics, Personal Finance, CRM, Generic Webapp)
- ETL and data engineering patterns
- Rules for coding, testing, security, documentation
- API, frontend, database, and infrastructure patterns

## Structure

### Declarative Definitions

Brain elements are declared in YAML for:

- **Knowledge** (`declarations/knowledge.yaml`): Concepts, domains, platform understanding
- **Rules** (`declarations/rules.yaml`): Validation, coding standards, security policies
- **Patterns** (`declarations/patterns.yaml`): Design and implementation patterns
- **Domains** (`declarations/domains.yaml`): Project domains with architecture defaults and applicable rules/patterns

### Modular Organization

```
c_brain/
├── declarations/          # YAML-based declarative definitions
│   ├── knowledge.yaml     # All knowledge elements
│   ├── rules.yaml         # All rules
│   ├── patterns.yaml      # All patterns
│   └── domains.yaml       # All domains and skill mappings
│
├── context/               # Context management (platform and project)
│   ├── platform_context.yaml  # How AAF operates
│   └── project_context.yaml   # Template for project-specific context
│
├── registry/              # Graph and registry builders
│   ├── brain_loader.py          # Load YAML declarations
│   ├── graph_builder.py         # Build knowledge graph
│   ├── knowledge_registry.py    # Query and access interface
│   ├── rule_registry.py         # Rule management
│   └── pattern_registry.py      # Pattern management
│
├── knowledge/             # Knowledge artifacts (optional, for future expansion)
├── rules/                 # Rule artifacts (optional, for future expansion)
├── patterns/              # Pattern artifacts (optional, for future expansion)
└── memory/                # Memory systems (short-term, long-term, architecture, execution)
```

## How It Works

### 1. Loading (BrainLoader)

```python
from a_platform.c_brain.registry import BrainLoader

loader = BrainLoader()
brain_state = loader.load()  # Load all YAML declarations
```

The loader:
- Reads YAML from `declarations/`
- Creates BrainElement objects (Knowledge, Rule, Pattern, Domain)
- Builds unified BrainState

### 2. Graph Building (KnowledgeGraphBuilder)

```python
from a_platform.c_brain.registry import KnowledgeGraphBuilder

graph = KnowledgeGraphBuilder(brain_state).build()
```

The graph builder:
- Converts elements to graph nodes
- Builds edges from relationships
- Creates adjacency lists for traversal
- Enables path finding and related element discovery

### 3. Querying (BrainRegistry)

```python
from a_platform.c_brain.registry import BrainRegistry

registry = BrainRegistry()

# Access knowledge, rules, patterns, domains
domain = registry.get_domain("analytics")
rules = registry.get_rules_for_domain("analytics")
patterns = registry.recommend_patterns("analytics")
architecture = registry.recommend_architecture("analytics")
```

## Relationships

The Brain models these relationship types:

- **knowledge → domain**: Knowledge belongs to a domain
- **domain → rule**: Domain has applicable rules
- **domain → pattern**: Domain uses patterns
- **agent → skill**: Agent can execute skills
- **skill → mcp**: Skill uses MCPs
- **project → domain**: Project belongs to domain
- **project → architecture**: Project follows architecture
- **project → decision**: Project has decisions

## Contexts

### Platform Context

Knowledge about how the Analytics AI Factory operates:

- Architecture and lifecycle stages
- Component responsibilities
- Integration protocols
- Configuration and settings

Located at: `c_brain/context/platform_context.yaml`

### Project Context

Knowledge specific to a project being created:

- Discovery results and requirements
- Architecture decisions
- Technology stack
- Generated artifacts
- Quality metrics
- Execution state

Located at: `c_brain/context/project_context.yaml` (template)

## Declarative Representation

Each Brain element (knowledge, rule, pattern, domain) has:

```yaml
id: unique_identifier
type: knowledge|rule|pattern|domain|skill|mcp
name: Human-readable name
description: What this element represents
tags: [tag1, tag2]
source: where_defined (file, module)
version: semantic_version
dependencies: [dep1_id, dep2_id]
relationships:
  - type: references|uses|implements|extends|part_of|produces|documents
    target: target_id
```

## Consumable By

The Brain is designed to be consumed by all platform components:

- **Discovery**: Knows what to ask and analyze
- **Planner**: Selects patterns and validates against rules
- **Agents**: Execute skills based on Brain guidance
- **Factory**: Applies patterns to generate artifacts
- **Runtime**: Knows configurations and execution model
- **Validation**: Checks against rules and patterns
- **Quality**: Applies standards and best practices
- **Learning**: Captures and updates knowledge

## Obsidian/Graphify Compatibility

The Brain can be exported to Obsidian-compatible format:

```python
registry.export_to_obsidian(Path("brain_graph"))
```

This creates:
- `INDEX.md` - Navigation index
- One `.md` file per node - With relationships and metadata
- Graph visualization-ready structure

## API Examples

### Get Domain Information

```python
registry = BrainRegistry()
domain = registry.get_domain("analytics")
architecture = registry.recommend_architecture("analytics")
rules = registry.get_rules_for_domain("analytics")
patterns = registry.get_patterns_for_domain("analytics")
```

### Find Related Knowledge

```python
related = registry.get_related_knowledge("etl_patterns")
path = registry.find_path("analytics_domain", "etl_patterns")
```

### Query Builder

```python
results = (registry.query()
    .where_type("rule")
    .where_tag("security")
    .execute())
```

### Export Brain State

```python
state = registry.to_dict()  # Export as JSON
registry.export_to_obsidian(Path("brain_graph"))
```

## Integration with Orchestrator

The Brain is automatically initialized in the orchestrator:

```python
from a_core.c_orchestration.orchestrator import PlatformOrchestrator

orchestrator = PlatformOrchestrator()
# orchestrator.brain is a BrainRegistry instance

# Get domain rules during planning
rules = orchestrator.brain.get_rules_for_domain(domain_id)

# Recommend patterns for project
patterns = orchestrator.brain.recommend_patterns(domain_id)

# Get architecture defaults
architecture = orchestrator.brain.get_domain_architecture(domain_id)
```

## No Agent Operational Logic

The Brain contains:
- ✅ Knowledge and rules
- ✅ Patterns and best practices
- ✅ Domain information
- ✅ Context and memory management
- ❌ Agent operational logic (this stays in d_agents/)
- ❌ Skill implementations (skills stay in agents)

## Extensibility

To add new knowledge, rules, or patterns:

1. Update the appropriate YAML file in `declarations/`
2. Reload the Brain: `loader = BrainLoader(); loader.load()`
3. Query using the registry API

Example adding a new rule:

```yaml
# In declarations/rules.yaml
- id: my_new_rule
  type: rule
  name: My New Rule
  description: Rule description
  tags: [category]
  applies_to: [domain1, domain2]
  severity: high
```

## Performance

- **Loading**: YAML files loaded once on initialization
- **Caching**: Optional JSON cache for repeated loads
- **Queries**: O(1) direct access, O(n) for searches
- **Graph operations**: Efficient adjacency lists

## Migration from Old Brains

Existing code using `c_brain/` or `b_ai_engine/a_brain/` should:

1. Replace imports with: `from a_platform.c_brain.registry import BrainRegistry`
2. Create registry: `registry = BrainRegistry()`
3. Use query API instead of direct file access
4. Update any agent decision logic to use registry recommendations

## Notes

- The new Brain is immediately consumable by all platform components
- YAML declarations are version-controlled and auditable
- Graph structure enables Obsidian visualization
- Registry API provides consistent access across components
- No tests in this block (per requirements)
- Old Brain implementations should be removed to avoid confusion
