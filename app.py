import uuid

import jwt
from flask import Flask, request, jsonify, make_response

from models import department  # call model file
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from models import user
from models.user import User

app = Flask(__name__)
CORS(app)
from config import config
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'flaskappconfig'

department = department.Department()
user = user.User()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            # data = jwt.decode(token, config['app']['SECRET_KEY'])
            print(token)
            data = jwt.decode(token, config['app']['SECRET_KEY'])
            current_user = user.find({"public_id": data['public_id']})
            print("token validation rule")
            print(current_user)
            # current_user = User.query \
            #     .filter_by(public_id=data['public_id']) \
            #     .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


# department routes
@app.route('/department/', methods=['GET'])
@token_required
def get_departments(current_user):
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


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            jsonify({'error': 'Invalid Credentials Provided. Login Required!'}),
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )
    user_ = user.find_first({"email": auth.get('email')})
    if not user_:
        # returns 401 if user does not exist
        return make_response(
            jsonify({'error': 'Invalid Credentials Provided! User does not exist!'}),
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )
    print("user_password")
    print(user_)
    if check_password_hash(user_['password'], auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user_['public_id'],
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, config['app']['SECRET_KEY'])
        print(token)
        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        jsonify({'error': 'Invalid Credentials Provided! Wrong Password Provided!'}),
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    _user_ = user.find({"email": email})
    print(_user_)
    if not _user_:
        # database ORM object
        db_user = {
            "public_id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "password": generate_password_hash(password)
        }
        user.create(db_user)

        return make_response(jsonify({'success': 'Successfully registered.'}), 201)
    else:
        # returns 202 if user already exists
        return make_response(jsonify({'error': 'User already exists. Please Log in.'}), 202)


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    # querying the database
    # for all the entries in it
    # users = User.query.all()

    users = user.find_all(current_user)
    # converting the query objects
    # to list of jsons
    output = []
    print("result")
    print(users)
    for user__ in users:
        # appending the user data json
        # to the response list
        output.append({
            'public_id': user__["public_id"],
            'name': user__["name"],
            'email': user__["email"]
        })

    return jsonify({'users': output})


if __name__ == '__main__':
    app.run(debug=True)
