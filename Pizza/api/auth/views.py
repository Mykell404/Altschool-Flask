from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace("auth", description="namespace for authentication")

"""
Namespace in restx are just like Blueprint in smorest

Resource are like MethodView
"""

auth_model = auth_namespace.model(
    # This is a Schema (Serializer) for the user model
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password'),
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    """
    This is the signup route
    """
    @auth_namespace.expect
    def post(self):
        """
        Sign up a user
        """
        pass


@auth_namespace.route('/login')
class Login(Resource):
    """
    This is the login route
    """

    def post(self):
        """
        Login a user and generate JWT token
        """
        pass
