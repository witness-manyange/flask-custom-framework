from flask import Flask, request, jsonify
from models import department  # call model file
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other

app = Flask(__name__)
CORS(app)

department = department.Department()


# todo routes
@app.route('/department/', methods=['GET'])
def get_departments():
    return jsonify(department.find({})), 200


@app.route('/departments/<string:department_id>/', methods=['GET'])
def get_department(department_id):
    return department.find_by_id(department_id), 200


@app.route('/departments', methods=['POST'])
def add_departments():
    if request.method == "POST":
        print("now printing values received!")
        print(request.form)
        name = request.form['name']
        description = request.form['description']
        response = department.create({'name': name, 'description': description})
        return response, 201


@app.route('/departments/<string:department_id>/', methods=['PUT'])
def update_departments(todo_id):
    if request.method == "PUT":
        name = request.form['name']
        description = request.form['description']
        response = department.update(todo_id, {'name': name, 'description': description})
        return response, 201


@app.route('/departments/<string:department_id>/', methods=['DELETE'])
def delete_departments(department_id):
    if request.method == "DELETE":
        department.delete(department_id)
        return "Record Deleted"


if __name__ == '__main__':
    app.run(debug=True)