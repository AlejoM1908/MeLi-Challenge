from os.path import join, dirname
from dotenv import dotenv_values
from src.gateways.MySQLRepository import MySQLRepository
from src.gateways.CountryAPI import CountryAPI

src_dir:str = dirname(__file__)
root_dir:str = dirname(src_dir)

config = dotenv_values(join(root_dir, '.env'))

SECRETS = {
    'jwt': config['JWT_SECRET'],
    'refresh': config['REFRESH_SECRET']
}

# Database
REPOSITORY = MySQLRepository({
    'host': config['MYSQL_HOST'],
    'port': int(config['MYSQL_PORT']) if 'MYSQL_PORT' in config else 3306,
    'user': config['MYSQL_USER'],
    'password': config['MYSQL_PASS'],
    'database': config['MYSQL_NAME']
})

# Country API
COUNTRY_API = CountryAPI(config['COUNTRY_API_URL'])