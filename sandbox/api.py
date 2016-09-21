from flask import Flask
from flask_restful import Resource, Api, reqparse, abort#, fields, marshal_with

app = Flask(__name__)
api = Api(app)

USERS = {
	'user1': {'first_name': 'bill', 'last_name': 'billiams', 'birthdate': '20160101', 'zip_code': '11111'},
	'user2': {'first_name': 'frank', 'last_name': 'billiams', 'birthdate': '20160101', 'zip_code': '22222'},
	'user3': {'first_name': 'samantha', 'last_name': 'james', 'birthdate': '20160101', 'zip_code': '33333'},
	'user4': {'first_name': 'ted', 'last_name': 'excellent', 'birthdate': '20160101', 'zip_code': '44444'},
	'user5': {'first_name': 'nutflux', 'last_name': 'reader', 'birthdate': '20160101', 'zip_code': '55555'}
}

# resource_fields = {
# 	'first_name':   fields.String,
# 	'last_name':   fields.String,
# 	'birthdate':   fields.Date,
# 	'zip_code':   fields.Integer
# }

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='User\'s first name.')
parser.add_argument('last_name', type=str, help='User\'s last name.')
parser.add_argument('birthdate', type=int, help='User\'s birthdate.')
parser.add_argument('zip_code', type=int, help='User\'s zip code.')


def abort_if_user_doesnt_exist(user_id):
	if user_id not in USERS:
		abort(404, message="User {user_id} doesn't exist...".format(user_id=user_id))

# class UserDao(object):
#     def __init__(self, user_id, user):
#         self.user_id = user_id
#         self.user = user

#         # This field will not be sent in the response
#         self.status = 'active'

class User(Resource):
	# @marshal_with(resource_fields)

	def get(self, user_id):
		abort_if_user_doesnt_exist(user_id)
		return USERS[user_id]


	def put(self, user_id):
		args = parser.parse_args(strict=True)
		first_name = args['first_name']
		last_name = args['last_name']
		birthdate = args['birthdate']
		zip_code = args['zip_code']

		user = {
				'first_name': first_name,
				'last_name': last_name,
				'birthdate': birthdate,
				'zip_code': zip_code
			}
		USERS[user_id] = user
		return user, 201

	def delete(self, user_id):
		abort_if_user_doesnt_exist(user_id)
		del USERS[user_id]
		return '', 204


class UserList(Resource):
	# @marshal_with(resource_fields)

	def get(self):
		return USERS

	def post(self):
		args = parser.parse_args(strict=True)
		first_name = args['first_name']
		last_name = args['last_name']
		birthdate = args['birthdate']
		zip_code = args['zip_code']

		user_id = int(max(USERS.keys()).lstrip('user')) + 1
		user_id = 'user%i' % user_id
		user = {
				'first_name': first_name,
				'last_name': last_name,
				'birthdate': birthdate,
				'zip_code': zip_code
			}
		USERS[user_id] = user
		return USERS[user_id], 201

api.add_resource(User, '/users/<string:user_id>')
api.add_resource(UserList, '/users')


if __name__ == '__main__':
	app.run(debug=True)