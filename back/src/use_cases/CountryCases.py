from src.entities.User import User
from src.gateways.CountryAPI import CountryAPI
from typing import Union

def getCountryByCCA3UseCase(country_api: CountryAPI, cca3:str) -> Union[User,str]:
    """
    Gets a country by cca3 in the provided repository.

    Parameters:
        repository (Repository): The repository to get the country.
        cca3 (str): The cca3 to get.

    Returns:
        Union[User,str]: Returns a error message or a list of countries.
    """
    # check if cca3 is valid
    if len(cca3) != 3:
        return 'cca3 must have 3 characters'
    
    # get the country
    return country_api.getCountryByCCA3(cca3)