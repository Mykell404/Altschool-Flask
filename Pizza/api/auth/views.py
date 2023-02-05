from flask_restx import Namespace, Resource

auth_namespace = Namespace("auth", description="namespace for authentication")

"""
Namespace in restx are just like Blueprint in smorest

Resource are like MethodView
"""


@auth_namespace.route('/signup')
class SignUp(Resource):
    """
    This is the signup route
    """

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
