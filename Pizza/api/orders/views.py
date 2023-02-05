from flask_restx import Namespace, Resource


# Whatever we pass in as the first arguement is what the name of the route would be
order_namespace = Namespace("order", description="namespace for order")


@order_namespace.route('/')
class HelloOrder(Resource):
    def get(self):
        return {"message": "Nice to meet you"}
