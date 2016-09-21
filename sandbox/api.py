from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('data', type=str, help='Todo task.')

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
    	args = parser.parse_args(strict=True)
        todos[todo_id] = args['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/todo/<int:todo_id>', endpoint='todo_ep')

if __name__ == '__main__':
    app.run(debug=True)