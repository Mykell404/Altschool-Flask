from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict

# Initial app setup


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    # Updates the values from the given object
    app.config.from_object(config)

    api = Api(app)

    # Configuring Api Route
    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace)

    return app
