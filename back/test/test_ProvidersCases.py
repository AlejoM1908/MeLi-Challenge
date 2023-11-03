import sys
import os

current_dir = os.path.dirname(os.path.realpath(__name__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from test.mockRepository import MockRepository
from src.gateways.CountryAPI import CountryAPI
from src.use_cases.ProvidersCases import *
from dotenv import dotenv_values

config = dotenv_values(".env")

class TestCreateProviderUseCase:
    def test_invalid_name(self):
        # Arrange
        name = ''
        description = 'test'
        country_cca3 = 'col'

        # Act
        result = createProviderUseCase(MockRepository(), CountryAPI(config['COUNTRY_API_URL']), name, description, country_cca3)

        # Assert
        assert result == 'Name must have at least 5 characters'

    def test_invalid_description(self):
        # Arrange
        name = 'test provider'
        description = ''
        country_cca3 = 'col'

        # Act
        result = createProviderUseCase(MockRepository(), CountryAPI(config['COUNTRY_API_URL']), name, description, country_cca3)

        # Assert
        assert result == 'Description must have at least 5 characters'

    def test_invalid_country(self):
        # Arrange
        name = 'test provider'
        description = 'test description'
        country_cca3 = 'test'

        # Act
        result = createProviderUseCase(MockRepository(), CountryAPI(config['COUNTRY_API_URL']), name, description, country_cca3)

        # Assert
        assert result == 'Country Code not found'

    def test_existant_provider(self):
        # Arrange
        name = 'test provider'
        description = 'test description'
        country_cca3 = 'col'

        # Act
        result = createProviderUseCase(MockRepository(), CountryAPI(config['COUNTRY_API_URL']), name, description, country_cca3)

        # Assert
        assert result == 'Provider already registered'

    def test_valid_provider(self):
        # Arrange
        name = 'test provider'
        description = 'test description'
        country_cca3 = 'col'

        # Act
        result = createProviderUseCase(MockRepository(fail=[True]), CountryAPI(config['COUNTRY_API_URL']), name, description, country_cca3)

        # Assert
        assert result == True

class TestUpdateProviderUseCase:
    def test_invalid_name(self):
        # Arrange
        id = 1
        new_parameters = {
            'name': '',
            'description': 'test description',
            'country': 'col'
        }

        # Act
        result = updateProviderUseCase(MockRepository(), CountryAPI(config['COUNTRY_API_URL']), id, new_parameters)

        # Assert
        assert result == 'Name must have at least 5 characters'

    def test_invalid_description(self):
        # Arrange
        id = 1
        new_parameters = {
            'name': 'test provider',
            'description': '',
            'country': 'col'
        }

        # Act
        result = updateProviderUseCase(MockRepository(fail=[False,True]), CountryAPI(config['COUNTRY_API_URL']), id, new_parameters)

        # Assert
        assert result == 'Description must have at least 5 characters'

    def test_invalid_country(self):
        # Arrange
        id = 1
        new_parameters = {
            'name': 'test provider',
            'description': 'test description',
            'country': 'test'
        }

        # Act
        result = updateProviderUseCase(MockRepository(fail=[False, True]), CountryAPI(config['COUNTRY_API_URL']), id, new_parameters)

        # Assert
        assert result == 'Country Code must have 3 characters'

    def test_existant_provider(self):
        # Arrange
        id = 1
        new_parameters = {
            'name': 'test provider',
            'description': 'test description',
            'country': 'col'
        }

        # Act
        result = updateProviderUseCase(MockRepository(), CountryAPI(config['COUNTRY_API_URL']), id, new_parameters)

        # Assert
        assert result == 'The provider name is already registered'

    def test_valid_provider(self):
        # Arrange
        id = 1
        new_parameters = {
            'name': 'test provider',
            'description': 'test description',
            'country': 'col'
        }

        # Act
        result = updateProviderUseCase(MockRepository(fail=[False, True]), CountryAPI(config['COUNTRY_API_URL']), id, new_parameters)

        # Assert
        assert result == True

class TestDeleteProviderUseCase:
    def test_invalid_id(self):
        # Arrange
        id = 0

        # Act
        result = deleteProviderUseCase(MockRepository(fail=[True]), id)

        # Assert
        assert result == 'the user couldn\'t be retrieved'

    def test_valid_id(self):
        # Arrange
        id = 1

        # Act
        result = deleteProviderUseCase(MockRepository(), id)

        # Assert
        assert result == True