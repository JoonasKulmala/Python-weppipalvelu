from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form


app = Flask(__name__)
app.secret_key = "Eere3Wie5amei3wae5Ey"
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)


ContactForm = model_form(Contact, base_class=FlaskForm, db_session=db.session)


@app.before_first_request
def initDb():
    db.create_all()

    contact = Contact(first_name="John", last_name="Doe",
                      email="foo@example.com", phone_number="123456789")
    db.session.add(contact)

    db.session.commit()


@app.route("/<int:id>/delete")
def deleteContact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()

    flash("Contact removed from list.")
    return redirect("/")


@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def newContact(id=None):
    contact = Contact()
    if id:
        contact = Contact.query.get_or_404(id)

    form = ContactForm(obj=contact)

    if form.validate_on_submit():
        form.populate_obj(contact)

        db.session.add(contact)
        db.session.commit()

        flash("New contact added.")
        return redirect("/")

    return render_template("new.html", form=form)


@app.route("/")
def index():
    contacts = Contact.query.all()
    return render_template("index.html", contacts=contacts)


if __name__ == "__main__":
    app.run()
