from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed, Unauthorized

# Initial app setup


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    # Updates the values from the config_dict
    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    api = Api(app)

    # Migrate helps make changes to the db without having to delete the db
    migrate = Migrate(app, db)

    # Configuring Api Route
    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace)

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 405

    @api.errorhandler(Unauthorized)
    def unauthorized(error):
        return {"error": "Unauthorized"}, 401

    @app.shell_context_processor
    # This create the application context and the app instance will be imported into the shell.
    def make_shell_context():
        return {
            'db': db,
            'user': User,
            'order': Order
        }

    return app
