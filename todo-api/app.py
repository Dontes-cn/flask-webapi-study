#!flask/bin/python
from flask import Flask,jsonify,abort,make_response,request,url_for,Response
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse, marshal_with
from flask_sqlalchemy import SQLAlchemy

import uuid
import mysql_connect
from models import *


app = Flask(__name__)
app.config.from_object(mysql_connect)
api = Api(app)
auth = HTTPBasicAuth()
with app.app_context():
    db.init_app(app)


tasks = [
    {
        'id':1,
        'title':'yesyesyes',
        'done':False
        },
    {
        'id':2,
        'title':'nonono',
        'done':True
        }
    ]


class Batch11API(Resource):
    def get(self, id):
        batch11_item = Batch11.query.filter(Batch11.posid == id).first()
        batch11_item = batch11_item.to_dict()
        return batch11_item

    def post(self):
        batch11_item_last = Batch11.query.order_by(Batch11.posid.desc()).first()
        posid = batch11_item_last.posid + 1
        province = request.json['province']
        city = request.json['city']
        batch11_item = Batch11(posid=posid,province=province,city=city)
        db.session.add(batch11_item)
        db.session.flush()
        db.session.commit()
        return batch11_item.to_dict()
api.add_resource(Batch11API, '/batch11', endpoint = 'batch11')


class UserAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(UserAPI, '/users/<int:id>', endpoint = 'user')

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return tasks

    def post(self):
        if not request.json or not 'title' in request.json:
            abort(400)
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'done':False
            }
        tasks.append(task)
        return task,201

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = filter(lambda t: t['id'] == id, tasks)
        task = list(task)
        if not task:
            abort(404)
        return task[0]

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(TaskListAPI, '/todo/api/v2.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/v2.0/task/<int:id>', endpoint = 'task')



@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python3'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthoried accss'}), 403)


@app.route('/todo/api/v1.0/tasks',methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id,tasks)
    task = list(task)
    if not task:
        abort(404)
    return jsonify({'task':task[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}), 404)


@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'done':False
        }
    tasks.append(task)
    return jsonify({'task': task}),201


@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id,tasks)
    task = list(task)
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['title'] = request.json.get('title',task[0]['title'])
    return jsonify({'task':task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id,tasks)
    task = list(task)
    if not task:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result':True})


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id=task['id'],_external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True)