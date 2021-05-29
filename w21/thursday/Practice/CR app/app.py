from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = "Eere3Wie5amei3wae5Ey"
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


DrinkForm = model_form(Drink, base_class=FlaskForm, db_session=db.session)


@app.before_first_request
def initDb():
    db.create_all()

    drink = Drink(name="Coffee")
    db.session.add(drink)

    db.session.commit()


@app.route("/new", methods=["GET", "POST"])
def newDrink():
    form = DrinkForm()

    if form.validate_on_submit():
        drink = Drink()
        form.populate_obj(drink)

        db.session.add(drink)
        db.session.commit()

        print("New drink added to database")
        # flash("Added")
        # redirect("/")

    return render_template("new.html", form=form)


@app.route("/")
def index():
    drinks = Drink.query.all()
    return render_template("index.html", drinks=drinks)


if __name__ == "__main__":
    app.run()
