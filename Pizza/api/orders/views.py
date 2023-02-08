from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from http import HTTPStatus
from flask_jwt_extended import jwt_required


# Whatever we pass in as the first arguement is what the name of the route would be
order_namespace = Namespace("orders", description="namespace for order")


order_model = order_namespace.model(
    # This is the schema (Serializer)
    'Order', {
        'id': fields.Integer(description='An ID'),
        'size': fields.String(description='Size of order', required=True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description='The status of our order', required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
    }
)


@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)  # Response
    @jwt_required()
    def get(self):
        """
          Get all orders
        """
        orders = Order.query.all()
        return orders, HTTPStatus.OK

    @order_namespace.expect(order_model)  # Requests
    @jwt_required()
    def post(self):
        """
         Place an order
        """
        data = order_namespace.payload

        return data, HTTPStatus.CREATED


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
