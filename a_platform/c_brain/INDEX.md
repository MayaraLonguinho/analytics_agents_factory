# Central Brain — Analytics AI Factory

## Purpose

The Brain is the unified cognitive and knowledge repository for the Analytics AI Factory.

It consolidates all knowledge, rules, patterns, and context needed to:
- Guide project discovery and planning
- Support agent decision-making
- Enforce architecture and coding standards
- Track execution and learning
- Maintain platform and project-specific context

## Structure

```
c_brain/
├── knowledge/          # Domain and platform knowledge
│   ├── platform/       # Platform knowledge (AAF architecture, lifecycle)
│   ├── architecture/   # Architecture patterns and principles
│   ├── analytics/      # Analytics domain knowledge
│   ├── data_engineering/ # Data engineering domain knowledge
│   └── domains/        # Domain-specific knowledge
│
├── rules/              # Decision and validation rules
│   ├── architecture/   # Architecture rules
│   ├── coding/         # Coding standards
│   ├── testing/        # Testing rules
│   ├── documentation/  # Documentation rules
│   └── security/       # Security rules
│
├── patterns/           # Design and implementation patterns
│   ├── etl/            # ETL patterns
│   ├── api/            # API patterns
│   ├── frontend/       # Frontend patterns
│   ├── database/       # Database patterns
│   └── infrastructure/ # Infrastructure patterns
│
├── context/            # Context management
│   ├── platform_context.yaml  # Platform-wide context
│   └── project_context.yaml   # Project-specific context
│
├── memory/             # Memory systems (short-term, long-term, execution)
│   ├── short_term/     # Session and request memory
│   ├── long_term/      # Persistent knowledge storage
│   ├── architecture/   # Architecture decisions
│   └── execution/      # Execution history and state
│
├── registry/           # Graph and registry builders
│   ├── brain_loader.py          # Load and initialize Brain
│   ├── graph_builder.py         # Build knowledge graph
│   ├── knowledge_registry.py    # Knowledge registry
│   ├── rule_registry.py         # Rule registry
│   └── pattern_registry.py      # Pattern registry
│
└── declarations/       # Declarative Brain representations
    ├── knowledge.yaml  # Knowledge graph declaration
    ├── rules.yaml      # Rules declaration
    ├── patterns.yaml   # Patterns declaration
    └── domains.yaml    # Domain definitions
```

## Key Concepts

### Platform Context
Knowledge about how the Analytics AI Factory platform operates:
- Architecture and lifecycle
- Component responsibilities
- Integration patterns
- Configuration and settings

### Project Context
Knowledge specific to a project being created:
- Domain and objectives
- Architecture decisions
- Technology preferences
- Generated artifacts

### Relationships

The Brain models relationships between entities:

```
knowledge → domain       # Knowledge belongs to a domain
domain → rule           # Domain has applicable rules
domain → pattern        # Domain uses patterns
agent → skill           # Agent can execute skills
skill → mcp             # Skill uses MCPs
project → domain        # Project belongs to a domain
project → architecture  # Project follows architecture
project → decision      # Project has decisions
```

## Declarative Representation

Each element (knowledge, rule, pattern, domain) is declared with:

```yaml
id: unique_identifier
type: knowledge|rule|pattern|domain|skill|mcp
name: Human-readable name
description: What this element represents
tags: [tag1, tag2]
relationships:
  - type: references|uses|implements|extends
    target: target_id
source: where_defined (file, module, external)
version: semantic_version
dependencies: [dep1_id, dep2_id]
```

## Compatibility

The declarative representation is designed to be:
- **Obsidian/Graphify compatible**: Can be visualized as knowledge graphs
- **IDE agent consumable**: Accessible via natural language
- **Runtime executable**: Converted to executable structures
- **Version-controllable**: YAML-based declarations

## Consumable By

- **Discovery**: Knowledge about project requirements and patterns
- **Planner**: Rules and patterns for execution planning
- **Agents**: Skills, rules, and context for agent decision-making
- **Factory**: Patterns and rules for artifact generation
- **Runtime**: Knowledge about configurations and execution
- **Validation**: Rules for quality and correctness checking
- **Quality**: Standards and best practices
- **Learning**: Feedback and knowledge updates

## Notes

The Brain does NOT contain:
- Agent operational logic
- Project-specific code generation
- ETL or data processing implementations

The Brain ONLY contains:
- Declarative knowledge and rules
- Design patterns and best practices
- Context and memory management
- Navigation and discovery mechanisms
