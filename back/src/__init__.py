from flask import Flask
from src.routes import bp
from flask_swagger_ui import get_swaggerui_blueprint

def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_pyfile("settings.py")
    app.register_blueprint(bp)

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