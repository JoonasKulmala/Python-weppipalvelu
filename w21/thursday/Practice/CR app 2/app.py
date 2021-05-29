from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "udgfewh90wt4"
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    email = db.Column(db.email, nullable=False)  # datatype?
    phone = db.Column(db.Integer, nullable=True)


EmployeeForm = model_form(
    Employee, base_class=EmployeeForm, db_session=db.session)
