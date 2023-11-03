from src.entities.Repositories import Repository
from src.entities.User import User
from src.entities.Role import Role
from src.entities.Risk import Risk
from src.entities.Provider import Provider
from datetime import datetime, timezone
import bcrypt

class MockRepository(Repository):
    pass

    def __init__(self, fail: bool = None, empty: bool = False):
        self.fail = fail if fail is not None else []
        self.empty = empty

        salt = bcrypt.gensalt(12)
        self.mock_user = User(
            id= 1, 
            email= 'test@test.com',
            password= 'test',
            name= 'test',
            roles= [
                Role(id= 1, name= 'test')
            ],
            created_at= datetime.now(tz= timezone.utc),
            updated_at= datetime.now(tz= timezone.utc),
            salt= salt,
            hashed_password= bcrypt.hashpw('test'.encode('utf-8'), salt),
        )

        self.mock_Risk = Risk(
            id= 1,
            provider_id= 1,
            name= 'test',
            description= 'test',
            probability= 'VERY_LOW',
            impact= 'VERY_HIGH',
            created_at= datetime.now(tz= timezone.utc),
            updated_at= datetime.now(tz= timezone.utc),
            user_ids= [1]
        )

        self.mock_Provider = Provider(
            id= 1,
            name= 'test',
            description= 'test',
            country= 'col',
            created_at= datetime.now(tz= timezone.utc),
            updated_at= datetime.now(tz= timezone.utc)
        )

    def _evaluateFail(self) -> bool:
        # pop head of fail list or if empty return false
        if len(self.fail) == 0:
            return False
        else:
            return self.fail.pop(0)

    def createUser(self, email: str, password: str, name: str) -> bool | str:
        return True if not self._evaluateFail() else 'Error al crear usuario'
    
    def getUserById(self, id: int) -> User | str:
        return self.mock_user if not self._evaluateFail() else 'Error obtaining user'
    
    def getUserById(self, id: int) -> User | str:
        return self.mock_user if not self._evaluateFail() else 'Error obtaining user'
    
    def getUserWithRoles(self, id: int) -> User | str:
        return self.mock_user if not self._evaluateFail() else 'Error obtaining user'
    
    def getUserByEmail(self, email: str) -> User | str:
        return self.mock_user if not self._evaluateFail() else 'Error obtaining user'
    
    def getUsersByRole(self, role: str) -> list[User] | str:
        return [self.mock_user] if not self._evaluateFail() else 'Error obtaining users'
    
    def getAllUsers(self) -> list[User] | str:
        return [self.mock_user] if not self._evaluateFail() else 'Error obtaining users'
    
    def updateUserData(self, user: User) -> bool | str:
        return True if not self._evaluateFail() else 'Error updating user'
    
    def updateUserPassword(self, user: User) -> bool | str:
        return True if not self._evaluateFail() else 'Error updating user'
    
    def deleteUser(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error deleting user'
    
    def validateUser(self, user: User) -> bool | str:
        return True if not self._evaluateFail() else 'The user cannot be validated'
    
    def linkRoleToUser(self, user_id: int, role_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error asigning role to user'
    
    def unlinkRoleToUser(self, user_id: int, role_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error removing role to user'
    
    def getAllRoles(self) -> list[Role] | str:
        if self._evaluateFail():
            return 'Error obtaining roles'
        elif self.empty:
            return []
        else:
            return [self.mock_user.roles[0]]
    
    def createRole(self, name: str) -> bool | str:
        return True if not self._evaluateFail() else 'Error creating rol'
    
    def getRoleById(self, id: int) -> Role | str:
        return self.mock_user.roles[0] if not self._evaluateFail() else 'Error obtaining rol'
    
    def getRoleByName(self, name: str) -> Role | str:
        return self.mock_user.roles[0] if not self._evaluateFail() else 'Error obtaining rol'
    
    def updateRole(self, role: Role) -> bool | str:
        return True if not self._evaluateFail() else 'Error updating rol'
    
    def deleteRole(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error deleting role'
    
    def createProvider(self, name: str, description: str, country: str) -> bool | str:
        return True if not self._evaluateFail() else 'Error creating provider'
    
    def getProviderById(self, id: int) -> Provider | str:
        return self.mock_Provider if not self._evaluateFail() else 'the user couldn\'t be retrieved'
    
    def getProviderByName(self, name: str) -> Provider | str:
        return self.mock_Provider if not self._evaluateFail() else 'the user couldn\'t be retrieved'
    
    def getAllProviders(self) -> list[Provider] | str:
        return [self.mock_Provider] if not self._evaluateFail() else 'the users couldn\'t be retrieved'
    
    def updateProvider(self, provider: Provider) -> bool | str:
        return True if not self._evaluateFail() else 'Error updating provider'
    
    def deleteProvider(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al eliminar proveedor'
    
    def createRisk(self, provider_id: int, name: str, description: str, probability: str, impact: str, user_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error creating risk'
    
    def getRiskById(self, id: int) -> Risk | str:
        return self.mock_Risk if not self._evaluateFail() else 'Error obtaining risk'
    
    def getRisksByString(self, string: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getRisksByProbability(self, probability: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getRisksByImpact(self, impact: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getRisksByUser(self, user_id: int) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getRisksByProvider(self, provider_id: int) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getRisksByCountry(self, country: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getAllRisks(self) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def getAllRisksWithUser(self) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error obtaining risks'
    
    def updateRisk(self, risk: Risk) -> bool | str:
        return True if not self._evaluateFail() else 'Error updating risk'
    
    def deleteRisk(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error deleting risk'
    
    def relateRiskToUser(self, risk_id: int, user_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error relating risk with user'
    
    def unrelateRiskToUser(self, risk_id: int, user_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error unrelating risk with user'