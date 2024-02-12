from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from api.models.order import Order
from api.models.user import User
from api.utils import db

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

order_status_model = order_namespace.model(
    "OrderStatus", {
        "order_status": fields.String(reaquired=True, description="Order_status",
                                      enum=["PENDING", "IN_TRANSIT", "DELIVERED", "CANCELLED"]),
    }
)


@order_namespace.route('/')
class OrderGetCreate(Resource):
    # @jwt_required()
    @order_namespace.marshal_list_with(order_model)
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
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self, order_id):
        """ Get an order by id """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    @jwt_required()
    @order_namespace.marshal_with(order_model)
    @order_namespace.expect(order_model)
    def put(self, order_id):
        """ Update an order by id """

        order_to_update = Order.get_by_id(order_id)
        data = order_namespace.payload
        order_to_update.quantity = data.get["quantity"]
        order_to_update.size = data.get["size"]
        order_to_update.flavour = data.get["flavour"]
        db.session.commit()
        return order_to_update, HTTPStatus.OK

    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def delete(self, order_id):
        """ Delete an order by id """

        order_to_delete = Order.get_by_id(order_id)
        order_to_delete.delete()
        return order_to_delete, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/order/<int:order_id>/')
class GetSpecificOrderByUser(Resource):
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self, user_id, order_id):
        """ Get user's specific order by id """

        user = User.get_user_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
        return order, HTTPStatus.OK


@order_namespace.route('/user/<int:user_id>/orders/')
class UserOrdersList(Resource):
    @jwt_required()
    @order_namespace.marshal_list_with(order_model)
    def get(self, user_id):
        """ Get all user's orders """
        user = User.get_user_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK


@order_namespace.route('/order/status/<int:order_id>/')
class UpdateOrderStatus(Resource):
    @jwt_required()
    @order_namespace.expect(order_status_model)
    def patch(self, order_id):
        """ Update an order status """
        data = order_namespace.payload
        order_to_update = Order.get_by_id(order_id)
        order_to_update.order_status = data.get("order_status")
        db.session.commit()
        return order_to_update, HTTPStatus.OK
