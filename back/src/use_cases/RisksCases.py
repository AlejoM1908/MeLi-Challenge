from src.entities.Risk import Risk
from src.entities.Repositories import Repository
from src.gateways.CountryAPI import CountryAPI
from typing import Union

def createRiskUseCase(repository:Repository, country_api:CountryAPI, name:str, description:str, probability:str, impact:str, provider_id:int, user_id:int) -> Union[bool,str]:
    """
    Creates a new risk in the provided repository.

    Parameters:
        repository (Repository): The repository to create the risk.
        name (str): The name to create.
        description (str): The description to create.
        probability (str): The probability to create.
        impact (str): The impact to create.
        provider_id (int): The provider id to create.
        user_id (int): The user id to create.

    Returns:
        Union[bool,str]: Returns a error message or a true if risk is created.
    """
    # check if name is valid
    if len(name) < 1:
        return 'Name must have at least 1 character'

    # check if description is valid
    if len(description) < 1:
        return 'Description must have at least 1 character'

    # check if probability is valid
    if probability not in ['LOW', 'MEDIUM', 'HIGH']:
        return 'Probability must be LOW, MEDIUM or HIGH'

    # check if impact is valid
    if impact not in ['LOW', 'MEDIUM', 'HIGH']:
        return 'Impact must be LOW, MEDIUM or HIGH'

    # check if provider is valid
    stored_provider = repository.getProviderById(provider_id)
    if isinstance(stored_provider, str):
        return stored_provider

    # check if user is valid
    stored_user = repository.getUserById(user_id)
    if isinstance(stored_user, str):
        return stored_user

    # no need to check if risk is already registered
    # create risk
    operation = repository.createRisk(provider_id, name, description, probability, impact)

    return operation