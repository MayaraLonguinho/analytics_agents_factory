# Knowledge Registry

## Objetivo

O Knowledge Registry é o mecanismo central responsável por registrar, organizar e fornecer acesso às fontes de conhecimento do Brain. Ele atua como catálogo que permite aos Agents descobrir e acessar conhecimento relevante.

## Funcionalidades

### Registro de Fontes

O Knowledge Registry mantém um registro de todas as fontes de conhecimento disponíveis:

```python
class KnowledgeSource:
    """Representa uma fonte de conhecimento"""
    
    def __init__(self, id: str, type: str, category: str, path: str, metadata: dict):
        self.id = id
        self.type = type  # internal, external, generated
        self.category = category  # architecture, backend, frontend, etc.
        self.path = path  # caminho para o conhecimento
        self.metadata = metadata  # metadados adicionais
        self.registered_at = datetime.utcnow()
        self.last_accessed = None
        self.access_count = 0
```

### Descoberta de Fontes

Agents podem descobrir fontes de conhecimento baseadas em critérios:

```python
def find_sources(
    knowledge_type: str = None,
    category: str = None,
    context: dict = None
) -> List[KnowledgeSource]:
    """
    Encontra fontes de conhecimento relevantes.
    
    Args:
        knowledge_type: Tipo de conhecimento (internal, external, generated)
        category: Categoria específica (architecture, backend, etc.)
        context: Contexto adicional da tarefa
        
    Returns:
        Lista de fontes de conhecimento relevantes
    """
```

### Acesso ao Conhecimento

O Registry fornece acesso padronizado ao conhecimento:

```python
def get_knowledge(source_id: str) -> Any:
    """
    Acessa o conteúdo de uma fonte de conhecimento.
    
    Args:
        source_id: ID da fonte de conhecimento
        
    Returns:
        Conteúdo da fonte de conhecimento
    """
```

### Metadados

Cada fonte possui metadados que facilitam a descoberta:

```python
metadata = {
    "name": "Personal Finance Flow Backend",
    "description": "Padrões de backend do projeto de referência",
    "version": "1.0",
    "language": "python",
    "technologies": ["fastapi", "pydantic", "sqlalchemy"],
    "tags": ["backend", "api", "rest"],
    "quality": "high",
    "last_updated": "2024-01-15",
    "author": "platform",
    "dependencies": [],
    "related_sources": []
}
```

## Estrutura do Registry

### Hierarquia

```
KnowledgeRegistry
├── InternalKnowledge
│   ├── Architecture
│   ├── Patterns
│   ├── Prompts
│   ├── Rules
│   ├── Examples
│   ├── BestPractices
│   ├── DecisionLog
│   ├── ADR
│   ├── PersonalFinanceFlow
│   │   ├── Architecture
│   │   ├── Backend
│   │   ├── Frontend
│   │   ├── Database
│   │   ├── ETL
│   │   ├── Analytics
│   │   ├── BusinessRules
│   │   ├── Patterns
│   │   ├── Prompts
│   │   └── Examples
│   └── ...
├── ExternalKnowledge
│   ├── Anthropic
│   ├── AwesomeAgentSkills
│   ├── GitHubExamples
│   ├── MCPExamples
│   ├── LLMPatterns
│   └── Documentation
└── GeneratedKnowledge
    ├── Reports
    ├── Analyses
    ├── Plans
    ├── Decisions
    ├── Metrics
    ├── Summaries
    ├── Insights
    └── Recommendations
```

### Registro

Cada fonte é registrada com um ID único:

```python
# Exemplo de registro
registry.register(
    id="pff-backend-001",
    type="internal",
    category="backend",
    path="internal_knowledge/personal_finance_flow/backend",
    metadata={
        "name": "Personal Finance Flow Backend",
        "description": "Padrões de backend do projeto de referência",
        "version": "1.0",
        "language": "python",
        "technologies": ["fastapi", "pydantic", "sqlalchemy"]
    }
)
```

## Operações

### Registro

```python
def register(source: KnowledgeSource) -> bool:
    """
    Registra uma nova fonte de conhecimento.
    
    Args:
        source: Fonte de conhecimento a registrar
        
    Returns:
        True se registrado com sucesso
    """
```

### Busca

```python
def search(query: str, filters: dict = None) -> List[KnowledgeSource]:
    """
    Busca fontes de conhecimento.
    
    Args:
        query: Query de busca
        filters: Filtros adicionais
        
    Returns:
        Lista de fontes encontradas
    """
```

### Consulta

```python
def query(criteria: dict) -> List[KnowledgeSource]:
    """
    Consulta fontes baseadas em critérios.
    
    Args:
        criteria: Critérios de consulta
        
    Returns:
        Lista de fontes que atendem aos critérios
    """
```

### Atualização

```python
def update(source_id: str, metadata: dict) -> bool:
    """
    Atualiza metadados de uma fonte.
    
    Args:
        source_id: ID da fonte
        metadata: Novos metadados
        
    Returns:
        True se atualizado com sucesso
    """
```

### Remoção

```python
def unregister(source_id: str) -> bool:
    """
    Remove uma fonte do registro.
    
    Args:
        source_id: ID da fonte
        
    Returns:
        True se removido com sucesso
    """
```

## Integração com Agents

### Backend Agent

```python
class BackendAgent:
    def generate_backend(self, context: dict):
        # Consulta Knowledge Registry
        sources = knowledge_registry.find_sources(
            knowledge_type="internal",
            category="backend",
            context=context
        )
        
        # Acessa conhecimento
        for source in sources:
            knowledge = knowledge_registry.get_knowledge(source.id)
            # Aplica conhecimento
```

### Architecture Agent

```python
class ArchitectureAgent:
    def design_architecture(self, requirements: dict):
        # Consulta Knowledge Registry
        sources = knowledge_registry.find_sources(
            knowledge_type="internal",
            category="architecture",
            context={"project_type": requirements["type"]}
        )
        
        # Acessa conhecimento
        architecture_patterns = knowledge_registry.get_knowledge(
            "architecture-patterns-001"
        )
        
        # Aplica conhecimento
```

### Analytics Agent

```python
class AnalyticsAgent:
    def generate_analytics(self, data: dict):
        # Consulta Knowledge Registry
        sources = knowledge_registry.find_sources(
            knowledge_type="internal",
            category="analytics",
            context={"data_type": data["type"]}
        )
        
        # Consulta conhecimento gerado anteriormente
        generated = knowledge_registry.find_sources(
            knowledge_type="generated",
            category="analyses",
            context={"similar_data": True}
        )
        
        # Aplica conhecimento
```

## Indexação

O Knowledge Registry mantém índices para busca eficiente:

```python
class KnowledgeIndex:
    """Índice para busca eficiente"""
    
    def __init__(self):
        self.by_type = {}  # internal, external, generated
        self.by_category = {}  # architecture, backend, etc.
        self.by_tags = {}  # tags para busca
        self.by_technology = {}  # tecnologias utilizadas
        self.popularity = {}  # ranking por popularidade
```

## Rastreabilidade

O Registry mantém registro de acessos:

```python
class AccessLog:
    """Log de acessos ao conhecimento"""
    
    def __init__(self):
        self.accesses = []
    
    def log_access(self, source_id: str, agent_id: str, context: dict):
        """Registra um acesso"""
        self.accesses.append({
            "timestamp": datetime.utcnow(),
            "source_id": source_id,
            "agent_id": agent_id,
            "context": context
        })
    
    def get_access_history(self, source_id: str) -> List[dict]:
        """Retorna histórico de acessos"""
        return [a for a in self.accesses if a["source_id"] == source_id]
```

## Validação

O Registry valida fontes antes de registrá-las:

```python
def validate_source(source: KnowledgeSource) -> bool:
    """
    Valida uma fonte de conhecimento.
    
    Args:
        source: Fonte a validar
        
    Returns:
        True se válida
    """
    # Verifica se path existe
    if not os.path.exists(source.path):
        return False
    
    # Verifica metadados obrigatórios
    required_fields = ["name", "description", "version"]
    for field in required_fields:
        if field not in source.metadata:
            return False
    
    # Verifica duplicidade
    if source.id in registry.sources:
        return False
    
    return True
```

## Performance

O Knowledge Registry é otimizado para performance:

- **Cache**: Fontes populares são cacheadas
- **Lazy Loading**: Conteúdo é carregado sob demanda
- **Indexação**: Índices para busca rápida
- **Batch Operations**: Operações em lote para eficiência
- **Async**: Operações assíncronas quando apropriado

## Nota Importante

**O Knowledge Registry não implementa RAG, busca semântica ou banco vetorial.** Ele serve apenas como catálogo determinístico baseado em metadados e categorias. A busca é feita por correspondência exata de critérios, não por similaridade semântica.
