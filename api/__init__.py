from flask import Flask
from flask_restx import Api

from api.auth.views import auth_namespace
from api.orders.views import order_namespace
from api.config.config import config_dict



def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(
        app=app,
        title = "Flask REST API with Flask-RESTX",
    version = "1.0",
    description = "Simple REST API with Flask-RESTX",
    doc = "/docs",
    )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(order_namespace, path="/orders")

    return app
