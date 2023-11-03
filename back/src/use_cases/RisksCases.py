from src.entities.Risk import Risk
from src.entities.Repositories import Repository
from typing import Union

def _selectBetterRisk(risk1:Risk, risk2:Risk) -> Risk:
    """
    Select the risk with the higher amount of values.

    Parameters:
        risk1 (Risk): The first risk.
        risk2 (Risk): The second risk.

    Returns:
        Risk: Returns the risk with the higher amount of values.
    """
    if len(risk1.asDict()) > len(risk2.asDict()):
        return risk1
    
    return risk2

def _joinRisksLists(placeholder:list[Risk], new:list[Risk]) -> list[Risk]:
    """
    Joins two lists of risks.

    Parameters:
        placeholder (list[Risk]): The placeholder list.
        new (list[Risk]): The new list.

    Returns:
        list[Risk]: Returns a list of Risks.
    """
    # Check if the new list is valid
    if not isinstance(new, list) or len(new) < 1:
        return []
    
    # Return the inner join of the two lists
    return [_selectBetterRisk(risk, new[new.index(risk)]) for risk in placeholder if risk in new]

def createRiskUseCase(repository:Repository, provider_id:int, name:str, description:str, probability:str, impact:str, email:str) -> Union[bool,str]:
    """
    Creates a new risk in the provided repository.

    Parameters:
        repository (Repository): The repository to create the risk.
        provider_id (int): The provider id to create.
        name (str): The name to create.
        description (str): The description to create.
        probability (str): The probability to create.
        impact (str): The impact to create.
        email (str): The user email from the JWT.

    Returns:
        Union[bool,str]: Returns a error message or a true if risk is created.
    """
    # check if name is valid
    if len(name) < 10:
        return 'Name must have at least 10 character'

    # check if description is valid
    if len(description) < 10:
        return 'Description must have at least 10 character'

    # check if probability is valid
    if probability not in ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']:
        return 'Probability must be in VERY_LOW, LOW, MEDIUM, HIGH or VERY_HIGH'

    # check if impact is valid
    if impact not in ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']:
        return 'Impact must be in VERY_LOW, LOW, MEDIUM, HIGH or VERY_HIGH'

    # check if provider is valid
    stored_provider = repository.getProviderById(provider_id)
    if isinstance(stored_provider, str):
        return stored_provider

    # Get the user creating the risk
    user = repository.getUserByEmail(email)
    if isinstance(user, str):
        return user
    

    operation = repository.createRisk(provider_id, name, description, probability, impact)

    if isinstance(operation, str):
        return operation
    
    # Create a link between the user and the risk
    return repository.relateRiskToUser(operation, user.id)

def updateRiskUseCase(repository:Repository, risk_id:int, new_parameters:dict) -> Union[bool,str]:
    """
    Updates a risk in the provided repository.

    Parameters:
        repository (Repository): The repository to update the risk.
        risk_id (int): The risk id to update.
        name (str): The name to update.
        description (str): The description to update.
        probability (str): The probability to update.
        impact (str): The impact to update.

    Returns:
        Union[bool,str]: Returns a error message or a true if risk is updated.
    """
    # check if the new parameters are valid
    if len(new_parameters) < 1:
        return 'No parameters to update provided'
    
    if not all(key in ['name', 'description', 'probability', 'impact', 'provider_id'] for key in new_parameters):
        return 'Parameters must be in name, description, probability, impact or provider_id'
    
    # check if risk is valid
    stored_risk = repository.getRiskById(risk_id)
    if isinstance(stored_risk, str):
        return stored_risk
    
    # check if name is valid
    if 'name' in new_parameters:
        if len(new_parameters['name']) < 10:
            return 'Name must have at least 10 characters'
        
        stored_risk.name = new_parameters['name']

    # check if description is valid
    if 'description' in new_parameters:
        if len(new_parameters['description']) < 10:
            return 'Description must have at least 10 characters'
        
        stored_risk.description = new_parameters['description']

    # check if probability is valid
    if 'probability' in new_parameters:
        if new_parameters['probability'] not in ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']:
            return 'Probability must be in VERY_LOW, LOW, MEDIUM, HIGH or VERY_HIGH'
        
        stored_risk.probability = new_parameters['probability']

    # check if impact is valid
    if 'impact' in new_parameters:
        if new_parameters['impact'] not in ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']:
            return 'Impact must be in VERY_LOW, LOW, MEDIUM, HIGH or VERY_HIGH'
        
        stored_risk.impact = new_parameters['impact']

    # check if provider is valid
    if 'provider_id' in new_parameters:
        stored_provider = repository.getProviderById(new_parameters['provider_id'])
        if isinstance(stored_provider, str):
            return stored_provider
        
        stored_risk.provider_id = new_parameters['provider_id']

    # update the risk
    return repository.updateRisk(stored_risk)

def deleteRiskUseCase(repository:Repository, risk_id:int) -> Union[bool,str]:
    """
    Deletes a risk in the provided repository.

    Parameters:
        repository (Repository): The repository to delete the risk.
        risk_id (int): The risk id to delete.

    Returns:
        Union[bool,str]: Returns a error message or a true if risk is deleted.
    """
    # check if risk is valid
    stored_risk = repository.getRiskById(risk_id)
    if isinstance(stored_risk, str):
        return stored_risk

    return repository.deleteRisk(risk_id)

def getFilteredRisksUseCase(repository:Repository, filters:dict) -> Union[list[Risk], str]:
    """
    Gets all risks in the provided repository.

    Parameters:
        repository (Repository): The repository to get the risks.
        filters (dict): The filters to apply.

    Returns:
        Union[list[Risk],str]: Returns a error message or a list of Risks if risks are found.
    """
    # check if filters are valid
    for key in filters:
        if key not in ['id','provider_id', 'user_id', 'string', 'probability', 'impact', 'country']:
            return 'Filter must be in provider_id, user_id, string, probability, impact or country'
        
    results = repository.getAllRisks()
    if isinstance(results, str):
        return results

    # check if id is valid
    if 'id' in filters:
        return repository.getRiskById(filters['id'])

    # check if provider_id is valid
    if 'provider_id' in filters:
        stored_provider = repository.getProviderById(filters['provider_id'])
        if isinstance(stored_provider, str):
            return stored_provider
        
        results = _joinRisksLists(results, repository.getRisksByProvider(stored_provider))

    # check if user_id is valid
    if 'user_id' in filters:
        stored_user = repository.getUserById(filters['user_id'])
        if isinstance(stored_user, str):
            return stored_user
        
        results = _joinRisksLists(results, repository.getRisksByUser(stored_user))

    # check if string is valid
    if 'string' in filters:
        if len(filters['string']) < 1:
            return 'String must have at least 1 character'
        
        results = _joinRisksLists(results, repository.getRisksByString(filters['string']))

    # check if probability is valid
    if 'probability' in filters:
        if filters['probability'] not in ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']:
            return 'Probability must be in VERY_LOW, LOW, MEDIUM, HIGH or VERY_HIGH'
        
        results = _joinRisksLists(results, repository.getRisksByProbability(filters['probability']))

    # check if impact is valid
    if 'impact' in filters:
        if filters['impact'] not in ['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']:
            return 'Impact must be in VERY_LOW, LOW, MEDIUM, HIGH or VERY_HIGH'
        
        results = _joinRisksLists(results, repository.getRisksByImpact(filters['impact']))

    # check if country is valid
    if 'country' in filters:
        if len(filters['country']) != 3:
            return 'Country must have 3 characters'
        
        results = _joinRisksLists(results, repository.getRisksByCountry(filters['country']))

    return results