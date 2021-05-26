from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "lkmoomoerIUmmf9B5bp"
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)


CommentForm = model_form(Comment, base_class=FlaskForm, db_session=db.session)


@app.before_first_request
def initMe():
    db.create_all()

    comment = Comment(text="Kahvia tekis mieli", name="Joonas")
    db.session.add(comment)

    comment = Comment(
        text="Suomen kesä on lyhyt ja vähäluminen", name="Reino Realisti")
    db.session.add(comment)

    db.session.commit()


@app.route("/")
def index():
    comments = Comment.query.all()
    return render_template("index.html", comments=comments)


@app.route("/msg")
def msgPage():
    flash("This is a flash message!")
    return redirect("/")


if __name__ == "__main__":
    app.run()
