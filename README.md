# Flask-Employee-API

Simple API for Employees to keep track of job tasks with user authorization.

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
    SECRET_KEY = ''
```

Test the `API` with [Postman](https://www.getpostman.com/) or something similar.

Run:

```
python api.py
```

### Employees

Login with test account that has admin rights:

```sh
http://127.0.0.1:5000/login GET method

In postman (or a similar service) go to authorization, choose basic authorization and for username type test and for password test
```

This should give you a token which expires within an hour.

Now go to headers and add key with the name `x-access-token` and add your token to the value section.

Check all of the employees:

> Doesn't work if you're not an admin.

```
http://127.0.0.1:5000/employee
```

Here you should see a list of employees with `public id's`, that `public id` is used to remove, promote etc. employees.

Example:

```sh
http://127.0.0.1:5000/employee/3e36267f-5a9c-4a02-9397-1f2fbee52ce1
```

Creating an employee:

Go to body, click on raw and choose `JSON`.

> Doesn't work if you're not an admin.

```sh
http://127.0.0.1:5000/employee POST method

Example
{"name": "john doe", "job_title": "doeing", "password": "123"}
```

Promoting an employee:

> Doesn't work if you're not an admin.

```sh
http://127.0.0.1:5000/employee/(public_id) PUT method
```

Removing an employee:

> Doesn't work if you're not an admin.

```sh
http://127.0.0.1:5000/employee/(public_id) DELETE method
```

### Task lists

Checking tasks "employee specific":

```sh
http://127.0.0.1:5000/job_tasks GET method
```

Creating a task "employee specific":

Go to body, click on raw and choose `JSON`.

```sh
http://127.0.0.1:5000/job_tasks POST method

Example:
{"task": "do things"}
```

With the given `ID` check only one task:

```sh
http://127.0.0.1:5000/job_tasks/1 GET method
```

Finishing a task "employee specific":

```sh
http://127.0.0.1:5000/job_tasks/1 PUT method
```

Removing a task "employee specific":

```sh
http://127.0.0.1:5000/job_tasks/1 DELETE method
```
