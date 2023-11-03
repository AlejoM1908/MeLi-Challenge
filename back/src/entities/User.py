from dataclasses import dataclass
from typing import Optional
from src.entities.Role import Role

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
        return {key:value for key, value in self.__dict__.items() if value is not None and key not in ['password', 'hashed_password', 'salt']}