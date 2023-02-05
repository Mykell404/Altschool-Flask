import os
from flask import Flask, jsonify
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.user import blp as UserBlueprint
from datetime import timedelta
from blocklist import BLOCKLIST


# Todo: create a init file for resources

def create_app(db_url=None):

    # configure your app
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "micheal"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    db.init_app(app)

    api = Api(app)
    jwt = JWTManager(app)

    # This decorator sets the callback function used to check if a JWT has been revoked.
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    # This decorator sets the callback function for returning a custom response when an expired JWT is encountered.
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The Token has Expired", "error": "Expired token"}), 401

    # This decorator sets the callback function that will be used if an invalid JWT attempts to access a protected endpoint.
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return ({"description": "Signature verification failed", "error": "invalid token"}), 401

    # This decorator sets the callback function used to return a custom response when no JWT is present.
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Request does not contain an access token",
                "error": "authorization_required"
            }), 401
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
