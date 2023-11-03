from src.entities.Repositories import Repository
from src.entities.User import User
from typing import Union
from datetime import datetime, timedelta, timezone
import jwt
import re

def loginUseCase(repository: Repository, email:str, password:str) -> Union[str, bool]:
    """
    Validates the user credentials in the provided repository and returns a JWT token if valid.
    
    Parameters:
        repository (Repository): The repository to validate the user credentials.
        email (str): The email to validate.
        password (str): The password to validate.

    Returns:
        Union[str, bool]: Returns a error message or a true if user is valid.
    """
    # check if email is valid
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return 'Invalid email format'
    
    stored_user = repository.getUserByEmail(email)
    if not isinstance(stored_user, User):
        return 'User not found'
    
    validate = repository.validateUser(User(id= 0, email= email, password= password))
    if isinstance(validate, str):
        return validate
    
    return True

def registerUseCase(repository: Repository, email:str, password:str, name:str) -> Union[str, bool]:
    """
    Registers a new user in the provided repository.
    
    Parameters:
        repository (Repository): The repository to register the user.
        email (str): The email to register.
        password (str): The password to register.
        name (str): The name to register.

    Returns:
        Union[str, bool]: Returns a error message or a true if user is registered.
    """
    # check if email is valid
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return 'Invalid email format'
    
    # check if email is already registered
    stored_user = repository.getUserByEmail(email)
    if isinstance(stored_user, User):
        return 'User already registered'
    
    # check if password is valid
    if len(password) < 8:
        return 'Password must have at least 8 characters'
    
    # check if name is valid
    if len(name) < 3:
        return 'Name must have at least 3 characters'
    
    # register user
    operation = repository.createUser(email, password, name)

    if isinstance(operation, str):
        return operation
    
    operation = repository.linkRoleToUser(operation, 1)
    if isinstance(operation, str):
        return operation
    
    return True

def generateJWTPairUseCase(secrets: dict[str,str], payload: dict[str, str | int], *, expiracy_in_minutes: int = 30, expiracy_in_days: int = 1) -> Union[str, tuple[str,str]]:
    """
    Generates a JWT token and a refresh token based on the provided secrets and payload.
    
    Positional Parameters:
        secrets (dict[str,str]): The secrets to generate the tokens, must have the keys 'jwt' and 'refresh'.
        payload (dict[str, str | int]): The payload to generate the tokens.

    Keyword Arguments:
        expiracy_in_minutes (int): The expiracy in minutes of the JWT token. Defaults to 30 minutes.
        expiracy_in_days (int): The expiracy in days of the refresh token. Defaults to 1 day.

    Returns:
        Union[str, tuple[str,str]]: Returns a error message or a tuple with the JWT token and the refresh token.
    """
    if not secrets or not payload:
        return 'Provided invalid parameters'
    
    if not 'jwt' in secrets or not 'refresh' in secrets:
        return 'Provided invalid secrets'
    
    jwt_payload = payload.copy()
    jwt_payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(minutes=expiracy_in_minutes)

    refresh_payload = payload.copy()
    refresh_payload['exp'] = datetime.now(tz=timezone.utc) + timedelta(days=expiracy_in_days)
    refresh_payload['exp'] = int(refresh_payload['exp'].timestamp())

    try:
        jwt_token = jwt.encode(jwt_payload, secrets['jwt'], algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, secrets['refresh'], algorithm='HS256')

        return (jwt_token, refresh_token)
    except Exception as e:
        
        return 'Error while generating tokens'

def refreshUseCase(secrets: dict[str,str], refresh_token: str) -> Union[str, tuple[str,str]]:
    """
    Refreshes the JWT token based on the provided refresh token and secret reusing the payload.

    Parameters:
        secrets (dict[str,str]): The secrets to generate the tokens, must have the keys 'jwt' and 'refresh'.
        refresh_token (str): The refresh token to validate.

    Returns:
        Union[str, tuple[str,str]]: Returns a error message or a tuple with the new JWT token and the refresh token.
    """
    if not secrets or not refresh_token:
        return 'Provided invalid parameters'

    if not 'jwt' in secrets or not 'refresh' in secrets:
        return 'Provided invalid secrets'

    # Validate refresh token
    payload = verifyTokenUseCase(secrets['refresh'], refresh_token)

    if isinstance(payload, str):
        return payload
    
    # Generate new tokens if valid
    return generateJWTPairUseCase(secrets, payload)

def verifyTokenUseCase(secret:str, token:str) -> Union[str, dict[str,str]]:
    """
    Verifies if the provided token is valid.

    Parameters:
        secret (str): The secret to validate the token.
        token (str): The token to validate.

    Returns:
        Union[str, dict[str,str]]: Returns a error message or the token payload if valid.
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'], leeway=10)
    except Exception as e:
        return 'Invalid token'
    
    return payload