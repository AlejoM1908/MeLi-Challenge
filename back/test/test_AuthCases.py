import sys
import os

current_dir = os.path.dirname(os.path.realpath(__name__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from test.mockRepository import MockRepository
from src.use_cases.AuthCases import *
import jwt

class TestLoginUseCase:
    def test_invalid_email(self):
        # Arrange
        email = 'test'
        password = 'test'

        # Act
        result = loginUseCase(MockRepository(), email, password)

        # Assert
        assert result == 'Invalid email format'

    def test_user_not_found(self):
        # Arrange
        email = 'test@test.com'
        password = 'test'

        # Act
        result = loginUseCase(MockRepository(fail=[True]), email, password)

        # Assert
        assert result == 'User not found'

    def test_invalid_password(self):
        # Arrange
        email = 'test@test.com'
        password = 'test'

        # Act
        result = loginUseCase(MockRepository(fail=[False, True]), email, password)

        # Assert
        assert result == 'Error al validar usuario'

    def test_valid_user(self):
        # Arrange
        email = 'test@test.com'
        password = 'test'

        # Act
        result = loginUseCase(MockRepository(), email, password)

        # Assert
        assert result == True

class TestRegisterUseCase:
    def test_invalid_email(self):
        # Arrange
        email = 'test'
        password = 'test'
        name = 'test'

        # Act
        result = registerUseCase(MockRepository(), email, password, name)

        # Assert
        assert result == 'Invalid email format'

    def test_user_already_registered(self):
        # Arrange
        email = 'test@test.com'
        password = 'test'
        name = 'test'

        # Act
        result = registerUseCase(MockRepository(), email, password, name)

        # Assert
        assert result == 'User already registered'

    def test_invalid_password(self):
        # Arrange
        email = 'test@test.com'
        password = 'test'
        name = 'test'

        # Act
        result = registerUseCase(MockRepository(fail=[True]), email, password, name)

        # Assert
        assert result == 'Password must have at least 8 characters'

    def test_invalid_name(self):
        # Arrange
        email = 'test@test.com'
        password = 'testpassword'
        name = 'te'

        # Act
        result = registerUseCase(MockRepository(fail=[True]), email, password, name)

        # Assert
        assert result == 'Name must have at least 3 characters'

    def test_valid_user(self):
        # Arrange
        email = 'test@test.com'
        password = 'testpassword'
        name = 'test'

        # Act
        result = registerUseCase(MockRepository(fail=[True]), email, password, name)

        # Assert
        assert result == True

class TestGenerateJWTPairUseCase:
    def test_missing_parameters(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt",
            "refresh": "secretforrefresh"
        }

        # Act
        result = generateJWTPairUseCase(secrets, None)

        # Assert
        assert result == 'Provided invalid parameters'

    def test_missing_secrets(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt"
        }
        payload = {
            "email": "test@test.com"
        }

        # Act
        result = generateJWTPairUseCase(secrets, payload)

        # Assert
        assert result == 'Provided invalid secrets'

    def test_valid_parameters(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt",
            "refresh": "secretforrefresh"
        }
        payload = {
            "email": "test@test.com"
        }

        # Act
        result = generateJWTPairUseCase(secrets, payload)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)
        assert len(result[0]) > 0
        assert len(result[1]) > 0
        assert result[0] != result[1]
        assert result[0] != secrets["jwt"]
        assert result[1] != secrets["refresh"]
        assert jwt.decode(result[0], secrets["jwt"], algorithms=["HS256"])["email"] == payload["email"]
        assert jwt.decode(result[1], secrets["refresh"], algorithms=["HS256"])["email"] == payload["email"]

class TestVerifyTokenUseCase:
    def test_invalid_token(self):
        # Arrange
        payload = {
            "email": "test@test.com",
            "exp": datetime.now(tz=timezone.utc) - timedelta(minutes=5)
        }
        refresh = jwt.encode(payload, "secretforrefresh", algorithm="HS256")

        # Act
        result = verifyTokenUseCase("secretforrefresh", refresh)

        # Assert
        assert result == 'Invalid token'

    def test_valid_token(self):
        # Arrange
        payload = {
            "email": "test@test.com",
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        }
        refresh = jwt.encode(payload, "secretforrefresh", algorithm="HS256")

        # Act
        result = verifyTokenUseCase("secretforrefresh", refresh)

        # Assert
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result["email"] == payload["email"]

class TestRefreshUseCase:
    def test_invalid_parameters(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt",
            "refresh": "secretforrefresh"
        }
        refresh_token = None

        # Act
        result = refreshUseCase(secrets, refresh_token)

        # Assert
        assert result == 'Provided invalid parameters'

    def test_invalid_secrets(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt"
        }
        payload = {
            "email": "test@test.com",
            "exp": datetime.now(tz=timezone.utc) - timedelta(minutes=5)
        }
        refresh = jwt.encode(payload, "secretforrefresh", algorithm="HS256")

        # Act
        result = refreshUseCase(secrets, refresh)

        # Assert
        assert result == 'Provided invalid secrets'

    def test_invalid_token(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt",
            "refresh": "secretforrefresh"
        }
        payload = {
            "email": "test@test.com",
            "exp": datetime.now(tz=timezone.utc) - timedelta(minutes=5)
        }
        refresh = jwt.encode(payload, secrets["refresh"], algorithm="HS256")

        # Act
        result = refreshUseCase(secrets, refresh)

        # Assert
        assert result == 'Invalid token'

    def test_valid_token(self):
        # Arrange
        secrets = {
            "jwt": "secretforjwt",
            "refresh": "secretforrefresh"
        }
        payload = {
            "email": "test@test.com",
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        }
        refresh = jwt.encode(payload, secrets["refresh"], algorithm="HS256")

        # Act
        result = refreshUseCase(secrets, refresh)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)
        assert len(result[0]) > 0
        assert len(result[1]) > 0
        assert result[0] != result[1]
        assert result[0] != secrets["jwt"]
        assert result[1] != secrets["refresh"]
        assert jwt.decode(result[0], secrets["jwt"], algorithms=["HS256"])["email"] == payload["email"]
        assert jwt.decode(result[1], secrets["refresh"], algorithms=["HS256"])["email"] == payload["email"]