from src.entities.Repositories import Repository
from src.entities.User import User, Role
from src.entities.Risk import Risk, Provider
from datetime import datetime, timezone
import bcrypt

class MockRepository(Repository):
    pass

    def __init__(self, fail: bool = None):
        self.fail = fail if fail is not None else []

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
            user_id= 1
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
        return self.mock_user if not self._evaluateFail() else 'Error al obtener usuario'
    
    def getUserById(self, id: int) -> User | str:
        return self.mock_user if not self._evaluateFail() else 'Error al obtener usuario'
    
    def getUserByEmail(self, email: str) -> User | str:
        return self.mock_user if not self._evaluateFail() else 'Error al obtener usuario'
    
    def getUsersByRole(self, role: str) -> list[User] | str:
        return [self.mock_user] if not self._evaluateFail() else 'Error al obtener usuarios'
    
    def getAllUsers(self) -> list[User] | str:
        return [self.mock_user] if not self._evaluateFail() else 'Error al obtener usuarios'
    
    def updateUserData(self, user: User) -> bool | str:
        return True if not self._evaluateFail() else 'Error al actualizar usuario'
    
    def updateUserPassword(self, user: User) -> bool | str:
        return True if not self._evaluateFail() else 'Error al actualizar usuario'
    
    def deleteUser(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al eliminar usuario'
    
    def validateUser(self, user: User) -> bool | str:
        return True if not self._evaluateFail() else 'Error al validar usuario'
    
    def linkRoleToUser(self, user_id: int, role_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al asignar rol'
    
    def unlinkRoleToUser(self, user_id: int, role_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al desasignar rol'
    
    def createRole(self, name: str) -> bool | str:
        return True if not self._evaluateFail() else 'Error al crear rol'
    
    def getRoleById(self, id: int) -> Role | str:
        return self.mock_user.roles[0] if not self._evaluateFail() else 'Error al obtener rol'
    
    def updateRole(self, role: Role) -> bool | str:
        return True if not self._evaluateFail() else 'Error al actualizar rol'
    
    def deleteRole(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al eliminar rol'
    
    def createProvider(self, name: str, description: str, country: str) -> bool | str:
        return True if not self._evaluateFail() else 'Error al crear proveedor'
    
    def getProviderById(self, id: int) -> Provider | str:
        return self.mock_Provider if not self._evaluateFail() else 'Error al obtener proveedor'
    
    def getProviderByName(self, name: str) -> Provider | str:
        return self.mock_Provider if not self._evaluateFail() else 'Error al obtener proveedor'
    
    def getAllProviders(self) -> list[Provider] | str:
        return [self.mock_Provider] if not self._evaluateFail() else 'Error al obtener proveedores'
    
    def updateProvider(self, provider: Provider) -> bool | str:
        return True if not self._evaluateFail() else 'Error al actualizar proveedor'
    
    def deleteProvider(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al eliminar proveedor'
    
    def createRisk(self, provider_id: int, name: str, description: str, probability: str, impact: str, user_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al crear riesgo'
    
    def getRiskById(self, id: int) -> Risk | str:
        return self.mock_Risk if not self._evaluateFail() else 'Error al obtener riesgo'
    
    def getRisksByString(self, string: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getRisksByProbability(self, probability: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getRisksByImpact(self, impact: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getRisksByUser(self, user_id: int) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getRisksByProvider(self, provider_id: int) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getRisksByCountry(self, country: str) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getAllRisks(self) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def getAllRisksWithUser(self) -> list[Risk] | str:
        return [self.mock_Risk] if not self._evaluateFail() else 'Error al obtener riesgos'
    
    def updateRisk(self, risk: Risk) -> bool | str:
        return True if not self._evaluateFail() else 'Error al actualizar riesgo'
    
    def deleteRisk(self, id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al eliminar riesgo'
    
    def relateRiskToUser(self, risk_id: int, user_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al relacionar riesgo con usuario'
    
    def unrelateRiskToUser(self, risk_id: int, user_id: int) -> bool | str:
        return True if not self._evaluateFail() else 'Error al desrelacionar riesgo con usuario'