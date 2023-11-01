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
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

@dataclass
class User:
    id: int
    email: str
    hashed_password: Optional[str] = None
    salt: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[list[Role]] = None

    def __str__(self) -> str:
        return f'{self.id} - {self.email}{f" - {self.name}" if self.name is not None else ""}'
    
    def asDict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }