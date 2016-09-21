from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('data', type=str, help='Todo task.')

todos = {}

resource_fields = {
    'task':   fields.String,
    'uri':    fields.Url('todo_ep')
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='1', task='Remember the milk')

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
    	args = parser.parse_args(strict=True)
        todos[todo_id] = args['data']
        return {todo_id: todos[todo_id]}


api.add_resource(Todo, '/todo/<int:todo_id>', endpoint='todo')
api.add_resource(TodoSimple, '/todo/<int:todo_id>', endpoint='todo_ep')


if __name__ == '__main__':
    app.run(debug=True)