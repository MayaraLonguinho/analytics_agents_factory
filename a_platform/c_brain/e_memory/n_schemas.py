from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from enum import Enum

class MemoryType(str, Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    CONVERSATION = "conversation"
    EXECUTION = "execution"
    SKILL = "skill"
    ARCHITECTURE = "architecture"

class DataType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    OBJECT = "object"

class EntryStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

class MessageEntry(BaseModel):
    role: str
    content: str
    timestamp: Optional[Any] = None

class ExecutionEntry(BaseModel):
    execution_id: Any
    agent_name: str
    skill_name: str
    state: Dict[str, Any]

class SkillResult(BaseModel):
    skill: str
    result: Any

class ArchitectureDecision(BaseModel):
    project_id: str
    decision: Dict[str, Any]

class ArchitectureEntry(BaseModel):
    project_id: str
    architecture: Dict[str, Any]
    version: str

class MemoryConfig(BaseModel):
    max_entries: Optional[int] = None
    default_ttl: Optional[float] = None
    max_size_mb: Optional[int] = None

class MemoryQuery(BaseModel):
    query_string: str
    tags: Optional[List[str]] = None

class MemoryStatistics(BaseModel):
    entries_count: int = 0
    total_size_mb: float = 0.0

class MemoryEntry(BaseModel):
    key: str
    value: Any
    ttl: Optional[float] = None
    created_at: Optional[Any] = None
