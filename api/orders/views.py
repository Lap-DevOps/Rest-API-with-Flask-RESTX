from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from api.models.order import Order
from api.models.user import User

order_namespace = Namespace('orders', description='Orders related operations')

order_model = order_namespace.model(
    "Order", {
        "id": fields.Integer(reaquired=True, description="id"),
        "size": fields.String(reaquired=True, description="size",
                              enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"]),
        "order_status": fields.String(reaquired=True, description="order_status",
                                      enum=["PENDING", "IN_TRANSIT", "DELIVERED", "CANCELLED"]),
        "flavor": fields.String(reaquired=True, description="flavor"),
        "customer": fields.String(reaquired=True, description="customer"),

    }
)


@order_namespace.route('/')
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)
    def get(self):
        """ Get all orders """
        orders = Order.query.all()

        return orders, HTTPStatus.OK

    @jwt_required
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    def post(self):
        """ Place new order """
        username = get_jwt_identity()
        current_user = User.query.get(username=username)

        data = order_namespace.payload
        new_order = Order(
            size=data.get('size'),
            quantity=data.get('quantity'),
            flavor=data.get('flavor'),
        )

        new_order.user = current_user

        new_order.save()
        return new_order, HTTPStatus.CREATED


@order_namespace.route('/<int:order_id>/')
class OrderGetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    def get(self, order_id):
        """ Get an order by id """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    def put(self, order_id):
        """ Update an order by id """
        return {'message': 'update order'}

    def delete(self, order_id):
        """ Delete an order by id """
        return {'message': 'delete order'}


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>/')
class GetSpecificOrderByUser(Resource):
    def get(self, user_id, order_id):
        """ Get user's specific order by id """
        return {'message': 'get order'}


@order_namespace.route('/user/<int:user_id>/orders/')
class UserOdersList(Resource):
    def get(self, user_id):
        """ Get all user's orders """
        return {'message': 'get orders'}


@order_namespace.route('/order/status/<int:order_id>/')
class UpdateOrderStatus(Resource):
    def patch(self, order_id):
        """ Update an order status """
        return {'message': 'update order status'}
