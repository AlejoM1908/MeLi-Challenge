from os.path import join, dirname
from dotenv import dotenv_values

src_dir:str = dirname(__file__)
root_dir:str = dirname(src_dir)

config = dotenv_values(join(root_dir, '.env'))

SECRET_KEY = config['SECRET_KEY']