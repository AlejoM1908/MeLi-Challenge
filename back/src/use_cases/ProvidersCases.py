from src.entities.Provider import Provider
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
    return repository.createProvider(name, description, country_cca3)

def updateProviderUseCase(repository:Repository, country_api:CountryAPI, id:int, new_parameters:dict[str,str]) -> Union[bool,str]:
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
    # check new parameters
    if not new_parameters:
        return 'No parameters to update provided'
    
    # check if required parameters are provided
    if 'name' not in new_parameters and 'description' not in new_parameters and 'country' not in new_parameters:
        return 'No valid parameters to update provided'

    # check if provider exists
    stored_provider = repository.getProviderById(id)
    if isinstance(stored_provider, str):
        return stored_provider
    
    if 'name' in new_parameters: 
        if len(new_parameters['name']) < 5:
            return 'Name must have at least 5 characters'
        
        # check if provider name is already registered
        query = repository.getProviderByName(new_parameters['name'])
        if isinstance(query, Provider):
            return 'The provider name is already registered'
        
        stored_provider.name = new_parameters['name']
    
    if 'description' in new_parameters: 
        if len(new_parameters['description']) < 5:
            return 'Description must have at least 5 characters'
        
        stored_provider.description = new_parameters['description']
    
    if 'country' in new_parameters: 
        if len(new_parameters['country']) != 3:
            return 'Country Code must have 3 characters'
        
        # check if country is valid
        country = country_api.getCountryByCCA3(new_parameters['country'])
        if isinstance(country, str):
            return country
        
        stored_provider.country = new_parameters['country']
    
    return repository.updateProvider(stored_provider)

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
    return repository.deleteProvider(id)

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
    return repository.getProviderById(id)

def getProviderByNameUseCase(repository:Repository, name:str) -> Union[Provider,str]:
    """
    Gets a provider by name in the provided repository.

    Parameters:
        repository (Repository): The repository to get the provider.
        name (str): The name to get.

    Returns:
        Union[Provider,str]: Returns a error message or a provider.
    """
    # get provider
    return repository.getProviderByName(name)

def getProvidersUseCase(repository:Repository) -> Union[list[Provider],str]:
    """
    Gets all providers in the provided repository.

    Parameters:
        repository (Repository): The repository to get the providers.

    Returns:
        Union[list[Provider],str]: Returns a error message or a list of providers.
    """
    # get providers
    return repository.getAllProviders()