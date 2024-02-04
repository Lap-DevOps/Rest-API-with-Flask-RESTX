from flask_restx import Namespace, Resource, fields
from http import HTTPStatus

from api.models.user import User
from werkzeug.security import generate_password_hash,check_password_hash

auth_namespace = Namespace('auth', description='authentication related operations')

signup_model = auth_namespace.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(reaquired=True, description="Username"),
        "email": fields.String(reaquired=True, description="Email"),
        "password": fields.String(reaquired=True, description="Password"),
    })


user_model = auth_namespace.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(reaquired=True, description="Username"),
        "email": fields.String(reaquired=True, description="Email"),
        'is_active': fields.Boolean(reaquired=True, description="Is active?"),
        'is_stuff': fields.Boolean(reaquired=True, description="Is stuff?")

    }
)


@auth_namespace.route('/signup/')
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """Create a new user account"""
        data = auth_namespace.payload
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'), )
        )
        new_user.save()
        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login/')
class Login(Resource):
    def post(self):
        """Login a user"""
        return {'message': 'login'}
