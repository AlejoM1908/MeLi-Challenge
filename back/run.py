from src import create_app
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = create_app()

if __name__ == "__main__":
    print(os.environ.get('FLASK_APP'), os.environ.get('FLASK_RUN_PORT'), os.environ.get('FLASK_RUN_HOST'))
    app.run()