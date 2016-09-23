from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal
from datetime import datetime

USERS = [
	{'user_id': 1, 'first_name': 'bill', 'last_name': 'billiams', 'birthdate': datetime(2016, 1, 1), 'zip_code': '11111'},
	{'user_id': 2, 'first_name': 'frank', 'last_name': 'billiams', 'birthdate': datetime(2016, 1, 1), 'zip_code': '22222'},
	{'user_id': 3, 'first_name': 'samantha', 'last_name': 'james', 'birthdate': datetime(2016, 1, 1), 'zip_code': '33333'},
	{'user_id': 4, 'first_name': 'ted', 'last_name': 'excellent', 'birthdate': datetime(2016, 1, 1), 'zip_code': '44444'},
	{'user_id': 5, 'first_name': 'nutflux', 'last_name': 'reader', 'birthdate': datetime(2016, 1, 1), 'zip_code': '55555'}
]

user_fields = {
				'first_name': fields.String,
				'last_name':  fields.String,
				'birthdate':  fields.DateTime,
				'zip_code':   fields.Integer,
				'uri':        fields.Url('user')
}



def return_user_or_abort(user_id):
	user = [user for user in USERS if user['user_id'] == user_id]
	if len(user) == 0:
		abort(404, message="User {user_id} doesn't exist...".format(user_id=user_id))
	else:
		return user[0]



class User(Resource):
	def __init__(self):
		parser = reqparse.RequestParser()
		parser.add_argument('first_name', type=str, required=True, help='User\'s first name.')
		parser.add_argument('last_name', type=str, required=True, help='User\'s last name.')
		parser.add_argument('birthdate', type=int, help='User\'s birthdate.')
		parser.add_argument('zip_code', type=int, help='User\'s zip code.')
		super(User, self).__init__()

	def get(self, user_id):
		user = return_user_or_abort(user_id)
		return {'user': marshal(user, user_fields)}


	def put(self, user_id):
		user = return_user_or_abort(user_id)
		args = self.reqparse.parse_args(strict=True)
		for k, v in args.items():
			if v is not None:
				user[k] = v
		return {'user': marshal(user, user_fields)}, 201

	def delete(self, user_id):
		user = return_user_or_abort(user_id)        
		users.remove(user)
		return {'result': True}, 204


class UserList(Resource):
	def __init__(self):
		parser = reqparse.RequestParser()
		parser.add_argument('first_name', type=str, required=True, help='User\'s first name.')
		parser.add_argument('last_name', type=str, required=True, help='User\'s last name.')
		parser.add_argument('birthdate', type=int, help='User\'s birthdate.')
		parser.add_argument('zip_code', type=int, help='User\'s zip code.')

	def get(self):
		return {'users': [marshal(user, user_fields) for user in USERS]}

	def post(self):
		args = self.reqparse.parse_args()
		user = {
			'user_id': USERS[-1]['user_id'] + 1,
			'first_name': args.first_name,
			'last_name': args.last_name,
			'birthdate': args.birthdate,
			'zip_code': args.zip_code
		}
		USERS.append(user)
		return {'user': marshal(user, user_fields)}, 201