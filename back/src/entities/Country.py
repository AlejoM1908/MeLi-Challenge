from dataclasses import dataclass

@dataclass
class Country:
    cca3: str
    capital: str
    region: str
    subregion: str
    population: int
    names: dict[str,str]
    languages: dict[str,str]
    currencies: dict[str,tuple[str,str]]
    timezones: list[str]

    def __str__(self) -> str:
        return f'{self.names["common"]} ({self.cca3})'
    
    def asDict(self) -> dict:
        return {
            'cca3': self.cca3,
            'capital': self.capital,
            'region': self.region,
            'subregion': self.subregion,
            'population': self.population,
            'names': self.names,
            'languages': self.languages,
            'currencies': self.currencies,
            'timezones': self.timezones
        }
