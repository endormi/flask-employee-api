from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))
    done = db.Column(db.Boolean)
    employee_id = db.Column(db.Integer)


if __name__ == '__main__':
    app.run()
