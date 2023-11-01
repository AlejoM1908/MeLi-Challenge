from src.entities.Risk import Provider
from src.entities.Repositories import Repository
from src.gateways.CountryAPI import CountryAPI
from typing import Union

def createProviderUseCase(repository:Repository, country_api:CountryAPI, name:str, description:str, country_cca3:str) -> Union[bool,str]:
    """
    Creates a new provider in the provided repository.

    Parameters:
        repository (Repository): The repository to create the provider.
        name (str): The name to create.
        description (str): The description to create.
        country_cca3 (str): The country to create.

    Returns:
        Union[bool,str]: Returns a error message or a true if provider is created.
    """
    # check if name is valid
    if len(name) < 5:
        return 'Name must have at least 5 characters'

    # check if description is valid
    if len(description) < 5:
        return 'Description must have at least 5 characters'

    # check if country is valid
    country = country_api.getCountryByCCA3(country_cca3)
    if isinstance(country, str):
        return country
    
    # check if provider is already registered
    stored_provider = repository.getProviderByName(name)
    if isinstance(stored_provider, Provider):
        return 'Provider already registered'
    
    # create provider
    operation = repository.createProvider(name, description, country_cca3)

    if isinstance(operation, str):
        return operation
    
    return True

def updateProviderUseCase(repository:Repository, country_api:CountryAPI, id:int, name:str, description:str, country_cca3:str) -> Union[bool,str]:
    """
    Updates a provider in the provided repository.

    Parameters:
        repository (Repository): The repository to update the provider.
        id (int): The id to update.
        name (str): The name to update.
        description (str): The description to update.
        country_cca3 (str): The country to update.

    Returns:
        Union[bool,str]: Returns a error message or a true if provider is updated.
    """
    # check if name is valid
    if len(name) < 1:
        return 'Name must have at least 1 character'

    # check if description is valid
    if len(description) < 1:
        return 'Description must have at least 1 character'

    # check if country is valid
    country = country_api.getCountryByCCA3(country_cca3)
    if isinstance(country, str):
        return country
    
    # check if provider is already registered
    stored_provider = repository.getProviderById(id)
    if isinstance(stored_provider, str):
        return stored_provider
    
    # update provider
    stored_provider.name = name
    stored_provider.description = description
    stored_provider.country = country_cca3
    operation = repository.updateProvider(stored_provider)

    if isinstance(operation, str):
        return operation
    
    return True

def deleteProviderUseCase(repository:Repository, id:int) -> Union[bool,str]:
    """
    Deletes a provider in the provided repository.

    Parameters:
        repository (Repository): The repository to delete the provider.
        id (int): The id to delete.

    Returns:
        Union[bool,str]: Returns a error message or a true if provider is deleted.
    """
    # check if provider is already registered
    stored_provider = repository.getProviderById(id)
    if isinstance(stored_provider, str):
        return stored_provider
    
    # delete provider
    operation = repository.deleteProvider(id)

    if isinstance(operation, str):
        return operation
    
    return True

def getProviderByIdUseCase(repository:Repository, id:int) -> Union[Provider,str]:
    """
    Gets a provider by id in the provided repository.

    Parameters:
        repository (Repository): The repository to get the provider.
        id (int): The id to get.

    Returns:
        Union[Provider,str]: Returns a error message or a provider.
    """
    # get provider
    provider = repository.getProviderById(id)

    if isinstance(provider, str):
        return provider
    
    return provider

def getProvidersUseCase(repository:Repository) -> Union[list[Provider],str]:
    """
    Gets all providers in the provided repository.

    Parameters:
        repository (Repository): The repository to get the providers.

    Returns:
        Union[list[Provider],str]: Returns a error message or a list of providers.
    """
    # get providers
    providers = repository.getAllProviders()

    if isinstance(providers, str):
        return providers
    
    return providers