from flask import jsonify, make_response
from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal, inputs
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'testy':
		return 'flask'
	return None

@auth.error_handler
def unauthorized():
	# return 403 instead of 401 to prevent browsers from displaying the default
	# auth dialog
	return make_response(jsonify({'message': 'Unauthorized access'}), 403)

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
				'birthdate':  fields.DateTime(dt_format='iso8601'),
				'zip_code':   fields.Integer,
				'uri':        fields.Url('user')
}

def try_parsing_date(text):
	valid_date_formats = [
							'%Y-%m-%d', '%Y-%m-%dT%H:%M:%S'
					]
	for fmt in valid_date_formats:
		try:
			return datetime.strptime(text, fmt)
		except ValueError:
			pass
	raise ValueError('no valid date format found')

def return_user_or_abort(user_id):
	user = [user for user in USERS if user['user_id'] == user_id]
	if len(user) == 0:
		abort(404, message="User {user_id} doesn't exist...".format(user_id=user_id))
	else:
		return user[0]



class User(Resource):
	decorators = [auth.login_required]

	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('first_name', type=str, required=True, help='User\'s first name.')
		self.parser.add_argument('last_name', type=str, required=True, help='User\'s last name.')
		self.parser.add_argument('birthdate', type=lambda x: try_parsing_date(x), help='User\'s birthdate.')		
		self.parser.add_argument('zip_code', type=int, help='User\'s zip code.')
		super(User, self).__init__()

	def get(self, user_id):
		user = return_user_or_abort(user_id)
		return {'user': marshal(user, user_fields)}


	def put(self, user_id):		
		user = return_user_or_abort(user_id)
		print user
		args = self.parser.parse_args(strict=True)
		for k, v in args.items():
			if v is not None:
				user[k] = v
		return {'user': marshal(user, user_fields)}#, 201

	def delete(self, user_id):
		user = return_user_or_abort(user_id)        
		USERS.remove(user)
		return {'result': True}#, 204


class UserList(Resource):
	decorators = [auth.login_required]

	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('first_name', type=str, required=True, help='User\'s first name.')
		self.parser.add_argument('last_name', type=str, required=True, help='User\'s last name.')
		self.parser.add_argument('birthdate', type=lambda x: try_parsing_date(x), help='User\'s birthdate.')		
		self.parser.add_argument('zip_code', type=int, help='User\'s zip code.')
		super(UserList, self).__init__()

	def get(self):
		return {'users': [marshal(user, user_fields) for user in USERS]}

	def post(self):
		args = self.parser.parse_args()

		# Check if USERS list is empty:
		if len(USERS) > 0:
			user_id = USERS[-1]['user_id'] + 1
		else:
			user_id = 1

		user = {
			'user_id': user_id,
			'first_name': args.first_name,
			'last_name': args.last_name,
			'birthdate': args.birthdate,
			'zip_code': args.zip_code
		}
		USERS.append(user)
		return {'user': marshal(user, user_fields)}, 201