# Flask-Employee-API

Simple API for Employees to keep track of job tasks with user authorization.

```sh
pip install -r requirements.txt
```

My `config.py` file is inside .gitignore, so you have to create `config` file manually.

Example:

```python
import os

class DevConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:\\users\\endormi\\employee.db"
    DEBUG = True
    SECRET_KEY = ''
```
