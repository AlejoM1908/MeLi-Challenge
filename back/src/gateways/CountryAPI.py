from src.entities.Country import Country
import requests as req
import json

class CountryAPI:
    def __init__(self, url: str) -> None:
        self.url = url
        self.filters = ["cca3", "capital", "region", "subregion", "population", "names", "languages", "currencies", "timezones"]

    def _cleanCountryData(self, country_data: dict) -> Country:
        return Country(
            cca3=country_data['cca3'],
            capital=country_data['capital'][0] if country_data['capital'] else None,
            region=country_data['region'],
            subregion=country_data['subregion'],
            population=country_data['population'],
            names={
                'common': country_data['name']['common'],
                'official': country_data['name']['official']
            },
            languages=country_data['languages'],
            currencies={
                currency: (country_data['currencies'][currency]['name'], country_data['currencies'][currency]['symbol'])
                for currency in country_data['currencies']
            },
            timezones=country_data['timezones']
        )
    
    def _queryAPI(self, path: str) -> json:
        query_url = f'{self.url}/{path}?filter={",".join(self.filters)}'
        return req.get(query_url).json()

    def getAllCountries(self) -> list[Country]:
        countries_data = self._queryAPI('all')

        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
    def getCountryByCCA3(self, cca3: str) -> Country:
        country_data = self._queryAPI(f'alpha/{cca3}')[0]
        return self._cleanCountryData(country_data)
    
    def getCountriesByListOfCCA3(self, cca3_list: list[str]) -> list[Country]:
        countries_data = self._queryAPI(f'alpha?codes={",".join(cca3_list)}')
        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
    def getCountriesByCurrency(self, currency: str) -> list[Country]:
        countries_data = self._queryAPI(f'currency/{currency}')
        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
    def getCountriesByLanguage(self, language: str) -> list[Country]:
        countries_data = self._queryAPI(f'lang/{language}')
        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
    def getCountriesByCapital(self, capital: str) -> list[Country]:
        countries_data = self._queryAPI(f'capital/{capital}')
        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
    def getCountriesByRegion(self, region: str) -> list[Country]:
        countries_data = req.get(f'{self.url}/region/{region}').json()
        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
    def getCountriesBySubregion(self, subregion: str) -> list[Country]:
        countries_data = req.get(f'{self.url}/subregion/{subregion}').json()
        countries = [self._cleanCountryData(country_data) for country_data in countries_data]
        return countries
    
