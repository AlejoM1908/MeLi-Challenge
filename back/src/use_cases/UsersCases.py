from src.entities.User import User
from src.entities.Repositories import Repository
from typing import Union

def getUserByEmailUseCase(repository:Repository, email:str) -> Union[User,str]:
    """
    Gets a user by email in the provided repository.

    Parameters:
        repository (Repository): The repository to get the user.
        email (str): The email to get.

    Returns:
        Union[User,str]: Returns a error message or a list of users.
    """
    # check if email is valid
    if len(email) < 1:
        return 'Email must have at least 1 character'

    # Get the user
    user = repository.getUserByEmail(email)

    if isinstance(user, str):
        return user
    
    return user

def getUserRolesUseCase(repository:Repository, user_id:int) -> Union[User,str]:
    """
    Gets a user with roles by id in the provided repository.

    Parameters:
        repository (Repository): The repository to get the user.
        user_id (int): The id to get.

    Returns:
        Union[User,str]: Returns a error message or a list of users.
    """
    # check if user id is valid
    if user_id < 1:
        return 'User id must be greater than 0'

    # Get the user
    user = repository.getUserWithRoles(user_id)

    if isinstance(user, str):
        return user
    
    return user

def addRoleToUserUseCase(repository:Repository, user_id:int, role_id:int) -> Union[bool,str]:
    """
    Adds a role to a user in the provided repository.

    Parameters:
        repository (Repository): The repository to add the role.
        user_id (int): The id to add the role.
        role_id (int): The id of the role to add.

    Returns:
        Union[bool,str]: Returns a error message or a true if role is added.
    """
    # check if user id is valid
    if user_id < 1:
        return 'User id must be greater than 0'
    
    # check if role id is valid
    if role_id < 1:
        return 'Role id must be greater than 0'

    # check if user exists
    stored_user = repository.getUserById(user_id)
    if isinstance(stored_user, str):
        return 'User not found'
    
    # check if role exists
    stored_role = repository.getRoleById(role_id)
    if isinstance(stored_role, str):
        return 'Role not found'
    
    # add role to user
    return repository.linkRoleToUser(stored_user.id, stored_role.id)

def removeRoleFromUserUseCase(repository:Repository, user_id:int, role_id:int) -> Union[bool,str]:
    """
    Removes a role from a user in the provided repository.

    Parameters:
        repository (Repository): The repository to remove the role.
        user_id (int): The id to remove the role.
        role_id (int): The id of the role to remove.

    Returns:
        Union[bool,str]: Returns a error message or a true if role is removed.
    """
    # check if user id is valid
    if user_id < 1:
        return 'User id must be greater than 0'
    
    # check if role id is valid
    if role_id < 1:
        return 'Role id must be greater than 0'

    # check if user exists
    stored_user = repository.getUserById(user_id)
    if isinstance(stored_user, str):
        return 'User not found'
    
    # check if role exists
    stored_role = repository.getRoleById(role_id)
    if isinstance(stored_role, str):
        return 'Role not found'
    
    # remove role from user
    return repository.unlinkRoleToUser(stored_user.id, stored_role.id)

def addUserToRiskUseCase(repository:Repository, user_id:int, risk_id:int) -> Union[bool,str]:
    """
    Adds a user to a risk in the provided repository.

    Parameters:
        repository (Repository): The repository to add the user.
        user_id (int): The id to add the user.
        risk_id (int): The id of the risk to add.

    Returns:
        Union[bool,str]: Returns a error message or a true if user is added.
    """
    # check if user id is valid
    if user_id < 1:
        return 'User id must be greater than 0'
    
    # check if risk id is valid
    if risk_id < 1:
        return 'Risk id must be greater than 0'

    # check if user exists
    stored_user = repository.getUserById(user_id)
    if isinstance(stored_user, str):
        return 'User not found'
    
    # check if risk exists
    stored_risk = repository.getRiskById(risk_id)
    if isinstance(stored_risk, str):
        return 'Risk not found'
    
    # add risk to user
    return repository.relateRiskToUser(stored_risk.id, stored_user.id)

def removeUserFromRiskUseCase(repository:Repository, user_id:int, risk_id:int) -> Union[bool,str]:
    """
    Removes a user from a risk in the provided repository.

    Parameters:
        repository (Repository): The repository to remove the user.
        user_id (int): The id to remove the user.
        risk_id (int): The id of the risk to remove.

    Returns:
        Union[bool,str]: Returns a error message or a true if user is removed.
    """
    # check if user id is valid
    if user_id < 1:
        return 'User id must be greater than 0'
    
    # check if risk id is valid
    if risk_id < 1:
        return 'Risk id must be greater than 0'

    # check if user exists
    stored_user = repository.getUserById(user_id)
    if isinstance(stored_user, str):
        return 'User not found'
    
    # check if risk exists
    stored_risk = repository.getRiskById(risk_id)
    if isinstance(stored_risk, str):
        return 'Risk not found'
    
    # remove risk from user
    return repository.unrelateRiskToUser(stored_risk.id, stored_user.id)

def updateUserUseCase(repository: Repository, user_id:int, new_parameters:dict[str,str]) -> Union[bool,str]:
    """
    Updates a user in the provided repository.

    Parameters:
        repository (Repository): The repository to update the user.
        user_id (int): The id to update.
        new_parameters (dict[str,str]): The parameters to update.

    Returns:
        Union[bool,str]: Returns a error message or a true if user is updated.
    """
    # check new parameters
    if not new_parameters:
        return 'No parameters to update provided'
    
    # check if required parameters are provided
    if 'name' not in new_parameters and 'email' not in new_parameters and 'password' not in new_parameters:
        return 'No valid parameters to update provided'
    
    # check if user exists
    stored_user = repository.getUserById(user_id)
    if isinstance(stored_user, str):
        return 'User not found'
    
    # check if email is valid
    if 'email' in new_parameters:
        if len(new_parameters['email']) < 1:
            return 'Email must have at least 1 character'
        
        # check if email is already registered
        query_user = repository.getUserByEmail(new_parameters['email'])
        if isinstance(query_user, User):
            return 'Email already registered'
        
        stored_user.email = new_parameters['email']

    # check if name is valid
    if 'name' in new_parameters:
        if len(new_parameters['name']) < 1:
            return 'Name must have at least 1 character'
        
        stored_user.name = new_parameters['name']

    # check if password is valid
    if 'password' in new_parameters:
        if len(new_parameters['password']) < 1:
            return 'Password must have at least 1 character'
        
        stored_user.password = new_parameters['password']

    # update user
    return repository.updateUserData(stored_user)
