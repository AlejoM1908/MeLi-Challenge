from dataclasses import dataclass
from typing import Optional

@dataclass
class Risk:
    id: int
    provider_id: int
    name: str
    description: str
    probability: str
    impact: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    country: Optional[str] = None
    user_ids: Optional[list[int]] = None

    def __str__(self) -> str:
        return f'{self.id} - {self.name} - Likelihood: {self.probability} - Impact: {self.impact}'
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Risk):
            return False
        
        return self.id == __value.id
    
    def asDict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if value is not None}