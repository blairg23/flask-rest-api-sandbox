from flask import Flask
from flask_restful import Api

app = Flask(__name__, static_url_path="")
api = Api(app)

from sandbox import views

from sandbox.resources.api import User
from sandbox.resources.api import UserList

api.add_resource(User, '/userlist/api/v1.0/users/<int:user_id>', endpoint='user')
api.add_resource(UserList, '/userlist/api/v1.0/users', '/userlist/api/v1.0/users/', endpoint='users')