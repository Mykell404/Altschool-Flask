from flask_restx import Namespace, Resource


# Whatever we pass in as the first arguement is what the name of the route would be
order_namespace = Namespace("orders", description="namespace for order")


@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    def get(self):
        """
          Get all orders
        """
        pass

    def post(self):
        """
         Place an order
        """
        pass


@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):
    def get(self, order_id):
        """
        Retrieving an order by id
        """
        pass

    def put(self, order_id):
        """
        Update an order by id
        """
        pass

    def delete(self, order_id):
        """
        Delete an order by id
        """
        pass


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    def get(self, user_id, order_id):
        """
        Get a user specific order
        """
        pass


@order_namespace.route('/user/<int:user_id>/orders')
class UserOrder(Resource):
    def get(self, user_id):
        """
        Get all orders made by user
        """
        pass


@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    def patch(self, order_id):
        """
        Update an order status
        """
        pass
