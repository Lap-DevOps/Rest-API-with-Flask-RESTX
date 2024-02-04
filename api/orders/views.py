from flask_restx import Namespace, Resource

order_namespace = Namespace('orders', description='Orders related operations')


@order_namespace.route('/')
class OrderGetCreate(Resource):
    def get(self):
        """ Get all orders """
        return {'message': 'orders'}

    def post(self):
        """ Place new order """
        return {'message': 'create order'}


@order_namespace.route('/<int:order_id>/')
class OrderGetUpdateDelete(Resource):
    def get(self, order_id):
        """ Get an order by id """
        return {'message': 'get order'}

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
        """ Update order status """
        return {'message': 'update order status'}
