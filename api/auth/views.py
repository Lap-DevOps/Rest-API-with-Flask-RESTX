from http import HTTPStatus

from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from api.models.user import User

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

login_model = auth_namespace.model(
    "Login",
    {
        "email": fields.String(reaquired=True, description="Email"),
        "password": fields.String(reaquired=True, description="Password"),
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
    @auth_namespace.expect(login_model)
    def post(self):
        """Login a user"""

        data = auth_namespace.payload
        user = User.query.filter_by(email=data.get('email')).first_or_404()
        if user:
            if check_password_hash(user.password_hash, data.get('password')):
                access_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)
                response = {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
                return response, HTTPStatus.OK
        return {'message': 'login'}


@auth_namespace.route('/refresh/')
class Refresh(Resource):
    @jwt_required(refresh=True)
    @auth_namespace.doc(description='Refresh token')
    def post(self):
        """Refresh token"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}, HTTPStatus.OK