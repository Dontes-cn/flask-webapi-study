#!flask/bin/python
from flask import Flask,jsonify,abort,make_response,request,url_for
from flask_restful import Api, Resource


app = Flask(__name__)
auth = HTTPBasicAuth()


tasks = [
    {
        'id':1,
        'title':'fuck',
        'done':False
        },
    {
        'id':2,
        'title':'your mom',
        'done':True
        }
    ]


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python3'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthoried accss'}), 401)


@app.route('/todo/api/v1.0/tasks',methods=['GET'])
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