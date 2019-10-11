from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
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


@app.route('/employee', methods=['GET'])
def get_employees():
    employees = Employee.query.all()

    output = []

    for employee in employees:

        empl_data = {}

        empl_data['public_id'] = employee.public_id
        empl_data['name'] = employee.name
        empl_data['public_id'] = employee.public_id
        empl_data['job_title'] = employee.job_title
        empl_data['password'] = employee.password
        empl_data['admin'] = employee.admin

        output.append(empl_data)

    return jsonify({'Employee list': output})


@app.route('/employee/<public_id>', methods=['GET'])
def get_employee():
    return ''


@app.route('/employee', methods=['POST'])
def create_employee():
    employee_data = request.get_json()

    pw_hash = generate_password_hash(employee_data['password'], method='sha256')

    new_employee = Employee(public_id=str(uuid.uuid1()), name=employee_data['name'], job_title=employee_data['job_title'], password=pw_hash, admin=False)

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'New employee added'})


@app.route('/employee/<public_id>', methods=['PUT'])
def promote_employee():
    return ''


@app.route('/employee/<public_id>', methods=['DELETE'])
def remove_employee():
    return ''


if __name__ == '__main__':
    app.run()
