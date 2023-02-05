from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace

# Initial app setup


def create_app():
    app = Flask(__name__)

    api = Api(app)

    # Configuring Api Route
    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace)

    return app
