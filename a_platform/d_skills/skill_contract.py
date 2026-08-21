from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from pydantic import BaseModel

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def input_schema(self) -> Type[BaseModel]:
        pass
        
    @property
    @abstractmethod
    def output_schema(self) -> Type[BaseModel]:
        pass
        
    @abstractmethod
    async def execute(self, input_data: BaseModel) -> BaseModel:
        pass
