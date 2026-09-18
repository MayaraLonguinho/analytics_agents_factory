from pydantic import BaseModel, Field
from typing import List

class MaterializationResult(BaseModel):
    status: str
    evidence: str
    details: str = ""
    errors: List[str] = Field(default_factory=list)
    materialized_paths: List[str] = Field(default_factory=list)
    origin: str = "Materializer"
