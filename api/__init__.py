from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate

from api.auth.views import auth_namespace
from api.config.config import config_dict
from api.models.order import Order  # noqa
from api.models.user import User  # noqa
from api.orders.views import order_namespace
from api.utils import db


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(
        app=app,
        title="Flask REST API with Flask-RESTX",
        version="1.0",
        description="Simple REST API with Flask-RESTX",
        doc="/docs",
    )
    db.init_app(app)
    migrate = Migrate(app, db)

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
