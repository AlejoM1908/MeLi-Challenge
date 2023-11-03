from flask import Flask
from src.routes import bp
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import dotenv_values
import json

config = dotenv_values(".flaskenv")

def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_pyfile("settings.py")
    app.register_blueprint(bp)

    # Load the swagger file
    with open('src/static/swagger.json', 'r') as f:
        swagger_file = json.load(f)

    # add base url to swagger file
    swagger_file['basePath'] = f'{config["FLASK_RUN_HOST"]}:{config["FLASK_RUN_PORT"]}'

    # save the swagger file
    with open('src/static/swagger.json', 'w') as f:
        json.dump(swagger_file, f)

    # Swagger config
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Risk Manager"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return app