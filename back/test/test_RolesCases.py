import sys
import os

current_dir = os.path.dirname(os.path.realpath(__name__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from test.mockRepository import MockRepository
from src.use_cases.RolesCases import *

class TestGetRolesUseCase:
    def test_no_roles(self):
        # Arrange
        repository = MockRepository(empty=True)

        # Act
        result = getRolesUseCase(repository)

        # Assert
        assert result == []

    def test_roles(self):
        # Arrange
        repository = MockRepository()

        # Act
        result = getRolesUseCase(repository)

        # Assert
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].name == 'test'

class TestGetRoleByIdUseCase:
    def test_invalid_id(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = getRoleByIdUseCase(repository, -1)

        # Assert
        assert result == 'Invalid id'

    def test_role_not_found(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = getRoleByIdUseCase(repository, 2)

        # Assert
        assert result == 'Error obtaining rol'

    def test_valid_id(self):
        # Arrange
        repository = MockRepository()

        # Act
        result = getRoleByIdUseCase(repository, 1)

        # Assert
        assert result.id == 1
        assert result.name == 'test'

class TestGetRoleByNameUseCase:
    def test_invalid_name(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = getRoleByNameUseCase(repository, '')

        # Assert
        assert result == 'Name must have at least 1 character'

    def test_role_not_found(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = getRoleByNameUseCase(repository, 'test')

        # Assert
        assert result == 'Error obtaining rol'

    def test_valid_name(self):
        # Arrange
        repository = MockRepository()

        # Act
        result = getRoleByNameUseCase(repository, 'test')

        # Assert
        assert result.id == 1
        assert result.name == 'test'

class TestUpdateRoleUseCase:
    def test_invalid_id(self):
        # Arrange
        repository = MockRepository(fail=[True])
        new_parameters = {
            'name': 'test'
        }

        # Act
        result = updateRoleUseCase(repository, -1, new_parameters)

        # Assert
        assert result == 'Invalid id'

    def test_no_parameters(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = updateRoleUseCase(repository, 1, {})

        # Assert
        assert result == 'No parameters to update provided'

    def no_name_in_parameters(self):
        # Arrange
        repository = MockRepository(fail=[True])
        new_parameters = {
            'description': 'test'
        }

        # Act
        result = updateRoleUseCase(repository, 1, new_parameters)

        # Assert
        assert result == 'No parameters to update provided'

    def test_role_not_found(self):
        # Arrange
        repository = MockRepository(fail=[True])
        new_parameters = {
            'name': 'test'
        }

        # Act
        result = updateRoleUseCase(repository, 2, new_parameters)

        # Assert
        assert result == 'Error obtaining rol'

    def test_invalid_name(self):
        # Arrange
        repository = MockRepository()
        new_parameters = {
            'name': ''
        }

        # Act
        result = updateRoleUseCase(repository, 1, new_parameters)

        # Assert
        assert result == 'Name must have at least 1 character'

    def test_valid_role(self):
        # Arrange
        repository = MockRepository(fail=[False, True])
        new_parameters = {
            'name': 'test'
        }

        # Act
        result = updateRoleUseCase(repository, 1, new_parameters)

        # Assert
        assert result == True

class TestDeleteRoleUseCase:
    def test_invalid_id(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = deleteRoleUseCase(repository, -1)

        # Assert
        assert result == 'Invalid id'

    def test_avoid_deleting_admin_role(self):
        # Arrange
        repository = MockRepository()

        # Act
        result = deleteRoleUseCase(repository, 1)

        # Assert
        assert result == 'You cannot delete the main role'

    def test_role_not_found(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = deleteRoleUseCase(repository, 2)

        # Assert
        assert result == 'Role id does not exists'

    def test_valid_role(self):
        # Arrange
        repository = MockRepository()

        # Act
        result = deleteRoleUseCase(repository, 2)

        # Assert
        assert result == True

class TestCreateRoleUseCase:
    def test_invalid_name(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = createRoleUseCase(repository, '')

        # Assert
        assert result == 'Name must have at least 1 character'

    def test_role_already_registered(self):
        # Arrange
        repository = MockRepository()

        # Act
        result = createRoleUseCase(repository, 'test')

        # Assert
        assert result == 'Role already exists'

    def test_valid_role(self):
        # Arrange
        repository = MockRepository(fail=[True])

        # Act
        result = createRoleUseCase(repository, 'test')

        # Assert
        assert result == True