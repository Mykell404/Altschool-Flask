from flask_restx import Namespace, Resource

auth_namespace = Namespace("auth", description="namespace for authentication")

"""
Namespace in restx are just like Blueprint in smorest

Resource are like MethodView
"""


@auth_namespace.route('/')
class HelloAuth(Resource):
    def get(self):
        return {"message": "Nice to meet you"}
