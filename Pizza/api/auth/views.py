from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_namespace = Namespace("auth", description="namespace for authentication")

"""
Namespace in restx are just like Blueprint in smorest

Resource are like MethodView
"""

signup_model = auth_namespace.model(
    # This is a Schema (Serializer) for the signup model
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password'),
    }
)


user_model = auth_namespace.model(
    # This is a Schema (Serializer) for the user model
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password_hash': fields.String(required=True, description='A password'),
        'is_active': fields.Boolean(description="This shows that the user is active or not"),
        'is_staff': fields.Boolean(description="This shows that the user is a staff or not"),
    }
)

login_model = auth_namespace.model(
    # This is a Schema (Serializer) for the login model
    'Login', {
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password'),
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    """
    This is the signup route
    """
    @auth_namespace.expect(signup_model)  # Takes in the expected schema
    @auth_namespace.marshal_with(user_model)  # Return the result's schema
    def post(self):
        """
        Sign up a user
        """
        data = request.get_json()  # Get user data

        # Save the data to the user Model
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
        )
        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    """
    This is the login route
    """
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login a user and generate JWT token
        """
        data = request.get_json()  # Get user data

        email = data.get('email')
        password = data.get('password')

        # Query the user from the database using the email
        user = User.query.filter_by(email=email).first()

        # Check if User exist and if password is correct
        if (user is not None) and check_password_hash(user.password_hash, password):
            # Create access token
            access_token = create_access_token(identity=user.username)
            # Create refresh token
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return response, HTTPStatus.CREATED
