from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = b"dppoi96cc.eeoe98"  # pwgen -1 20
db = SQLAlchemy(app)


class WeatherForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    weather = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, default="No comment")


CommentForm = model_form(
    WeatherForecast, base_class=FlaskForm, db_session=db.session)


@app.before_first_request
def initMe():
    db.create_all()

    weather = WeatherForecast(
        day="Monday", weather="Cloudy")
    db.session.add(weather)

    weather = WeatherForecast(
        day="Tuesday", weather="Rain", comment="Bring an umbrella")
    db.session.add(weather)

    weather = WeatherForecast(
        day="Wednesday", weather="Monsoon", comment="Better know how to swim")
    db.session.add(weather)

    db.session.commit()


@app.route("/new", methods=["GET", "POST"])
def addForm():
    form = CommentForm()
    print(request.form)
    return render_template("new.html", form=form)


@app.route("/")
def index():
    weathers = WeatherForecast.query.all()
    return render_template("index.html", weathers=weathers)


if __name__ == "__main__":
    app.run()
