from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from sandbox.resources.api import User
from sandbox.resources.api import UserList

api.add_resource(User, '/users/<int:user_id>', endpoint='user')
api.add_resource(UserList, '/users', '/users/', endpoint='users')