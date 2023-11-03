from dataclasses import dataclass
from typing import Optional

@dataclass
class Role:
    id: int
    name: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __str__(self) -> str:
        return f'{self.id} - {self.name}'
    
    def asDict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if value is not None}