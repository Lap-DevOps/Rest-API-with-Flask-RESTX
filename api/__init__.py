from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from werkzeug.exceptions import NotFound, MethodNotAllowed

from api.auth.views import auth_namespace
from api.config.config import config_dict
from api.models.order import Order  # noqa
from api.models.user import User  # noqa
from api.orders.views import order_namespace
from api.utils import db


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    jwt = JWTManager(app)

    authorizations = {
        "Bearer Auth": {
            'type': "apiKey",
            'in': 'header',
            'name': "Authorization",
            'description': "Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    api = Api(
        app=app,
        title="Flask REST API with Flask-RESTX",
        version="1.0",
        description="Simple REST API with Flask-RESTX",
        doc="/docs",
        authorizations=authorizations,
        security="Bearer Auth"
    )
    db.init_app(app)
    migrate = Migrate(app, db)


    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 405

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(order_namespace, path="/orders")

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order,
        }

    return app
