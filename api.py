from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import datetime
import jwt
import uuid


app = Flask(__name__)

# Config from config.py file
app.config.from_object('config.DevConfig')

db = SQLAlchemy(app)


class Employee(db.Model):
    admin = db.Column(db.Boolean)
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(24))
    job_title = db.Column(db.String(24))
    password = db.Column(db.String(50))


class Job_tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))
    done = db.Column(db.Boolean)
    employee_id = db.Column(db.Integer)


@app.route('/login')
def login():
    """
    Login authorization,
    Has three intances where if not authorized, 401 error occurs (not authenticated)
    If authorized it creates a token with an expiration date of 1 hour
    """
    __auth__ = request.authorization

    employee = Employee.query.filter_by(name=__auth__.username).first()

    if not __auth__ or not __auth__.username or not __auth__.password:
        return make_response('Not authenticated!', 401)

    if not employee:
        return make_response('Not authenticated!', 401)

    if check_password_hash(employee.password, __auth__.password):
        employee_token = jwt.encode({'exp': datetime.datetime.now() + datetime.timedelta(hours=1), 'public_id': employee.public_id}, app.config['SECRET_KEY'])

        return jsonify({'Employee token': employee_token.decode('UTF-8')})

    return make_response('Not authenticated!', 401)


def req_token(i):
    @wraps(i)
    def decoy(*args, **kwargs):
        employee_token = None

        if 'x-access-token' in request.headers:
            employee_token = request.headers['x-access-token']

        if not employee_token:
            return jsonify({'message': 'Missing token'}), 401

        try:
            jwtoken = jwt.decode(employee_token, app.config['SECRET_KEY'])
            current_employee = Employee.query.filter_by(public_id=jwtoken['public_id']).first()
        except:
            return make_response('Not authenticated! Invalid Token!', 401)

        return i(current_employee, *args, **kwargs)

    return decoy


@app.route('/employee', methods=['GET'])
@req_token
def get_employees(current_employee):
    """
    Get all employees
    """
    if not current_employee.admin:
        return jsonify({'message': 'No no, you cannot do that'})

    employees = Employee.query.all()

    output = []

    for employee in employees:

        empl_data = {}

        empl_data['admin'] = employee.admin
        empl_data['public_id'] = employee.public_id
        empl_data['name'] = employee.name
        empl_data['job_title'] = employee.job_title
        empl_data['password'] = employee.password

        output.append(empl_data)

    return jsonify({'Employee list': output})


@app.route('/employee/<public_id>', methods=['GET'])
@req_token
def get_employee(current_employee, public_id):
    """
    Get an employee based on public_id,
    if public_id doesn't match with an employee, returns an error message
    """
    if not current_employee.admin:
        return jsonify({'message': 'No no, you cannot do that'})

    employee = Employee.query.filter_by(public_id=public_id).first()

    if not employee:
        return jsonify({'message': 'No employee found'})

    empl_data = {}

    empl_data['admin'] = employee.admin
    empl_data['public_id'] = employee.public_id
    empl_data['name'] = employee.name
    empl_data['job_title'] = employee.job_title
    empl_data['password'] = employee.password

    return jsonify({'Employee': empl_data})


@app.route('/employee/<public_id>', methods=['PUT'])
@req_token
def promote_employee(current_employee, public_id):
    """
    Promote new employee,
    if public_id doesn't match with an employee, returns an error message
    """
    if not current_employee.admin:
        return jsonify({'message': 'No no, you cannot do that'})

    employee = Employee.query.filter_by(public_id=public_id).first()

    if not employee:
        return jsonify({'message': 'No employee found'})

    employee.admin = True
    db.session.commit()

    return jsonify({'message': 'Employee has been promoted'})


@app.route('/employee', methods=['POST'])
@req_token
def create_employee(current_employee):
    """
    Create a new employee
    """
    if not current_employee.admin:
        return jsonify({'message': 'No no, you cannot do that'})

    employee_data = request.get_json()

    pw_hash = generate_password_hash(employee_data['password'], method='sha256')

    new_employee = Employee(public_id=str(uuid.uuid1()), name=employee_data['name'], job_title=employee_data['job_title'], password=pw_hash, admin=False)

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'New employee added'})


@app.route('/employee/<public_id>', methods=['DELETE'])
@req_token
def remove_employee(current_employee, public_id):
    """
    Remove employee,
    if public_id doesn't match with an employee, returns an error message
    """
    if not current_employee.admin:
        return jsonify({'message': 'No no, you cannot do that'})

    employee = Employee.query.filter_by(public_id=public_id).first()

    if not employee:
        return jsonify({'message': 'No employee found'})

    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee has been removed'})


if __name__ == '__main__':
    app.run()
