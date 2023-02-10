from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from ..utils import db
from flask_jwt_extended import jwt_required, get_jwt_identity


# Whatever we pass in as the first arguement is what the name of the route would be
order_namespace = Namespace("orders", description="namespace for order")


order_model = order_namespace.model(
    # This is the schema (Serializer)
    'Order', {
        'id': fields.Integer(description='An ID'),
        'quantity': fields.Integer(description='The quantity of the order'),
        'size': fields.String(description='Size of order', required=True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description='The status of our order', required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        'flavour': fields.String(description='The flavour of the pizza', required=True)
    }
)

order_status_model = order_namespace.model(
    # Order Status Schema (Serializer)
    'OrderStatus', {
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
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
         Place an order
        """

        # get current user from the jwt identity
        username = get_jwt_identity()

        # query the user in database
        current_user = User.query.filter_by(username=username).first()

        # Recieve the payload from the frontend
        data = order_namespace.payload

        new_order = Order(
            size=data['size'],
            quantity=data['quantity'],
            order_status=data['order_status'],
            flavour=data['flavour']
        )

        new_order.user = current_user

        new_order.save()

        return new_order, HTTPStatus.CREATED


@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self, order_id):
        """
        Retrieving an order by id
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def put(self, order_id):
        """
        Update an order by id
        """
        order_to_update = Order.get_by_id(order_id)

        data = order_namespace.payload

        order_to_update.quantity = data['quantity']
        order_to_update.size = data['size']
        order_to_update.order_status = data['order_status']
        order_to_update.flavour = data['flavour']

        order_to_update.update()

        return order_to_update, HTTPStatus.CREATED

    @jwt_required()
    def delete(self, order_id):
        """
        Delete an order by id
        """
        order_to_delete = Order.get_by_id(order_id)

        order_to_delete.delete()

        return {"message": "Deleted sucessfully"}, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self, user_id, order_id):
        """
        Get a user specific order
        """

        # Get user by id
        user = User.get_by_id(user_id)

        # Query order by id and filter it by the user
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()

        # Return order

        return order, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/orders')
class UserOrder(Resource):
    @jwt_required()
    @order_namespace.marshal_list_with(order_model)
    def get(self, user_id):
        """
        Get all orders made by user
        """

        # Get the user
        user = User.get_by_id(user_id)
        # Get all orders by the user
        orders = user.orders

        return orders, HTTPStatus.OK


@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_model)
    def patch(self, order_id):
        """
        Update an order status
        """
        data = order_namespace.payload

        order_to_update = Order.get_by_id(order_id)

        order_to_update.order_status = data['order_status']

        order_to_update.update()

        return order_to_update, HTTPStatus.OK
