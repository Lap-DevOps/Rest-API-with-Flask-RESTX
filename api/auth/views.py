from flask_restx import Namespace, Resource

auth_namespace = Namespace('auth', description='authentication related operations')


@auth_namespace.route('/signup/')
class Signup(Resource):
    def post(self):
        """Create a new user account"""
        return {'message': 'signup'}

@auth_namespace.route('/login/')
class Login(Resource):
    def post(self):
        """Login a user"""
        return {'message': 'login'}