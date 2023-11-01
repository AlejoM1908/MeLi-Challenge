from dataclasses import dataclass
from typing import Optional

@dataclass
class Provider:
    id: int
    name: str
    description: str
    country: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __str__(self) -> str:
        return f'{self.id} - {self.name}'
    
    def asDict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'country': self.country,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

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
    user_id: Optional[int] = None

    def __str__(self) -> str:
        return f'{self.id} - {self.name} - Likelihood: {self.probability} - Impact: {self.impact}'
    
    def asDict(self) -> dict:
        return {
            'id': self.id,
            'provider_id': self.provider_id,
            'name': self.name,
            'description': self.description,
            'probability': self.probability,
            'impact': self.impact,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_id': self.user_id
        }