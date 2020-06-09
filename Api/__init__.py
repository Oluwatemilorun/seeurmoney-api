from flask import Flask
from Api.v1 import bp as v1_bp
from Api.config import DevConfig



def create_app(config_class=DevConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(v1_bp)

    return app

