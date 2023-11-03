from src.entities.Role import Role
from src.entities.Repositories import Repository
from typing import Union

def getRolesUseCase(repository:Repository) -> Union[list[Role],str]:
    """
    Gets all roles in the provided repository.

    Parameters:
        repository (Repository): The repository to get the roles.

    Returns:
        Union[list[Role],str]: Returns a error message or a list of roles.
    """
    # Get the roles
    roles = repository.getAllRoles()

    if isinstance(roles, str):
        return roles
    
    return roles

def getRoleByIdUseCase(repository:Repository, role_id:int) -> Union[Role,str]:
    """
    Gets a role by id in the provided repository.

    Parameters:
        repository (Repository): The repository to get the role.
        role_id (int): The id to get.

    Returns:
        Union[Role,str]: Returns a error message or a role.
    """
    # check if id is valid
    if role_id < 1:
        return 'Invalid id'

    # check if role exists
    role = repository.getRoleById(role_id)

    if isinstance(role, str):
        return role
    
    return role

def getRoleByNameUseCase(repository:Repository, name:str) -> Union[Role,str]:
    """
    Gets a role by name in the provided repository.

    Parameters:
        repository (Repository): The repository to get the role.
        name (str): The name to get.

    Returns:
        Union[Role,str]: Returns a error message or a role.
    """
    # check if name is valid
    if len(name) < 1:
        return 'Name must have at least 1 character'

    # Get the role
    role = repository.getRoleByName(name)

    if isinstance(role, str):
        return role
    
    return role

def updateRoleUseCase(repository: Repository, role_id:int, new_parameters:dict[str,str]) -> Union[Role,str]:
    """
    Updates a role in the provided repository.

    Parameters:
        repository (Repository): The repository to update the role.
        role_id (int): The id of the role to update.
        new_parameters (dict[str,str]): The new parameters to update.

    Returns:
        Union[Role,str]: Returns a error message or a role.
    """
    # check if id is valid
    if role_id < 1:
        return 'Invalid id'
    
    # validate new parameters
    if len(new_parameters) < 1:
        return 'No parameters to update provided'
    
    if 'name' not in new_parameters:
        return 'No valid parameters to update provided'
    
    # check if role exists
    role = repository.getRoleById(role_id)
    if isinstance(role, str):
        return role
    
    # check if name is valid
    if 'name' in new_parameters:
        if len(new_parameters['name']) < 1:
            return 'Name must have at least 1 character'
        
        # check if role exists
        query_role = repository.getRoleByName(new_parameters['name'])
        if isinstance(query_role, Role):
            return 'Role already exists'
        
        role.name = new_parameters['name']

    # update the role
    role = repository.updateRole(role)

def deleteRoleUseCase(repository: Repository, role_id:int) -> Union[Role,str]:
    """
    Deletes a role in the provided repository.

    Parameters:
        repository (Repository): The repository to delete the role.
        role_id (int): The id of the role to delete.

    Returns:
        Union[Role,str]: Returns a error message or a role.
    """
    # Avoid deleting the main role
    if role_id == 1:
        return 'You cannot delete the main role'

    # check if role exists
    role = repository.getRoleById(role_id)
    if not isinstance(role, Role):
        return 'Role id does not exists'

    # delete the role
    return repository.deleteRole(role_id)

def createRoleUseCase(repository: Repository, name:str) -> Union[Role,str]:
    """
    Creates a role in the provided repository.

    Parameters:
        repository (Repository): The repository to create the role.
        name (str): The name of the role to create.

    Returns:
        Union[Role,str]: Returns a error message or a role.
    """
    # check if name is valid
    if len(name) < 1:
        return 'Name must have at least 1 character'
    
    # check if role exists
    role = repository.getRoleByName(name)
    if isinstance(role, Role):
        return 'Role already exists'

    # create the role
    role = repository.createRole(name)

    if isinstance(role, str):
        return role
    
    return role