from abc import ABC, abstractmethod
from src.entities.User import User, Role
from src.entities.Risk import Risk, Provider
from enum import Enum
from typing import Union

class Classification(Enum):
    VERY_LOW = 'VERY_LOW'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERY_HIGH = 'VERY_HIGH'

class Repository(ABC):
    @abstractmethod
    def createUser(self, email: str, password: str, name: str) -> Union[bool,str]:
        pass

    @abstractmethod
    def getUserById(self, id: int) -> Union[User,str]:
        pass

    @abstractmethod
    def getUserByEmail(self, email: str) -> Union[User,str]:
        pass

    @abstractmethod
    def getUsersByRole(self, role: str) -> Union[list[User],str]:
        pass

    @abstractmethod
    def getAllUsers(self) -> Union[list[User],str]:
        pass

    @abstractmethod
    def updateUserData(self, user: User) -> Union[bool,str]:
        pass

    @abstractmethod
    def updateUserPassword(self, user: User) -> Union[bool,str]:
        pass

    @abstractmethod
    def deleteUser(self, id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def validateUser(self, user: User) -> Union[bool,str]:
        pass

    @abstractmethod
    def linkRoleToUser(self, user_id: int, role_id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def unlinkRoleToUser(self, user_id: int, role_id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def createRole(self, name: str) -> Union[bool,str]:
        pass

    @abstractmethod
    def getRoleById(self, id: int) -> Union[Role,str]:
        pass

    @abstractmethod
    def updateRole(self, role:Role) -> Union[bool,str]:
        pass

    @abstractmethod
    def deleteRole(self, id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def createProvider(self, name: str, description: str, country:str) -> Union[bool,str]:
        pass

    @abstractmethod
    def getProviderById(self, id: int) -> Union[str,str]:
        pass

    @abstractmethod
    def getProviderByName(self, name: str) -> Union[str,str]:
        pass

    @abstractmethod
    def getAllProviders(self) -> Union[list[Provider],str]:
        pass

    @abstractmethod
    def updateProvider(self, Provider) -> Union[bool,str]:
        pass

    @abstractmethod
    def deleteProvider(self, id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def createRisk(self, provider_id:int, name: str, description: str, probability: Classification, impact: Classification) -> Union[bool,str]:
        pass

    @abstractmethod
    def getRiskById(self, id: int) -> Union[Risk,str]:
        pass

    @abstractmethod
    def getRisksByString(self, string: str) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getRisksByProbability(self, probability: Classification) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getRisksByImpact(self, impact: Classification) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getRisksByUser(self, user: User) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getRisksByProvider(self, provider: Provider) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getRisksByCountry(self, country: str) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getAllRisks(self) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def getAllRisksWithUser(self) -> Union[list[Risk],str]:
        pass

    @abstractmethod
    def updateRisk(self, Risk) -> Union[bool,str]:
        pass

    @abstractmethod
    def deleteRisk(self, id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def relateRiskToUser(self, risk_id: int, user_id: int) -> Union[bool,str]:
        pass

    @abstractmethod
    def unrelateRiskToUser(self, risk_id: int, user_id: int) -> Union[bool,str]:
        pass
