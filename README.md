# Flask-Employee-API [![Python Version](https://img.shields.io/badge/python-3.6.1-brightgreen.svg?)](https://www.python.org/downloads/)

Simple API for Employees to keep track of job tasks with user authorization.

## Getting started

Clone:

```sh
HTTPS: https://github.com/endormi/flask-employee-api.git SSH: git@github.com:endormi/flask-employee-api.git
```

Install requirements:

```sh
pip install -r requirements.txt
```

My `config.py` file is inside .gitignore, so you have to create a `config` file manually.

Example:

```python
import os

class DevConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:\\users\\user\\employee.db"
    DEBUG = True
    SECRET_KEY = 'Your_Secret_Key'
```

Test the `API` with [Postman](https://www.getpostman.com/) or something similar.

Run:

```
python api.py
```

## Admin credentials

Test account:

```sh
login: test

password: test
```

> Use this code if you have a totally new db and need to create an user or just want to make a new admin

```python
@app.route('/employee', methods=['POST'])
def create_employee():

    employee_data = request.get_json()

    pw_hash = generate_password_hash(employee_data['password'], method='sha256')

    new_employee = Employee(public_id=str(uuid.uuid1()), name=employee_data['name'], job_title=employee_data['job_title'], password=pw_hash, admin=True)

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'New employee added'})
```

### Employees

Login with test account that has admin rights:

```sh
http://127.0.0.1:5000/login GET method
```

> In postman (or a similar service) go to authorization, choose basic authorization and for username type test and for password test.

This should give you a token which expires within an hour.

Now go to headers and add key with the name `x-access-token` and add your token to the value section.

Check all of the employees:

> Doesn't work if you're not an admin.

```
http://127.0.0.1:5000/employee
```

Here you should see a list of employees with `public id's`, that `public id` is used to remove, promote etc. employees.

Example:

> Visible for anyone.

```sh
http://127.0.0.1:5000/employee/1ab439cc-ec09-11e9-8090-4cedfb3cafc4
```

Creating an employee:

Go to body, click on raw and choose `JSON`.

> Doesn't work if you're not an admin.

```sh
http://127.0.0.1:5000/employee POST method
```

Example employee:

```js
{"name": "john doe", "job_title": "doeing", "password": "123"}
```

Promoting an employee:

> Doesn't work if you're not an admin.

```sh
http://127.0.0.1:5000/employee/<public_id> PUT method
```

Removing an employee:

> Doesn't work if you're not an admin.

```sh
http://127.0.0.1:5000/employee/<public_id> DELETE method
```

### Task lists

> These are employee specific and not visible to admin users.

Checking tasks:

```sh
http://127.0.0.1:5000/job_tasks GET method
```

Creating a task:

Go to body, click on raw and choose `JSON`.

```sh
http://127.0.0.1:5000/job_tasks POST method
```

Example task:

```js
{"task": "do things"}
```

With the given `ID` check only one task:

```sh
http://127.0.0.1:5000/job_tasks/<id> GET method
```

Finishing a task:

```sh
http://127.0.0.1:5000/job_tasks/<id> PUT method
```

Removing a task:

```sh
http://127.0.0.1:5000/job_tasks/<id> DELETE method
```
