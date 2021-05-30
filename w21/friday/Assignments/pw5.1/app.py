from flask import Flask, render_template, flash, redirect, session, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, validators, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "ojiemieCh3eeMee4vahX"
db = SQLAlchemy(app)


class Plot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plot = db.Column(db.Text(160), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user")
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)


PlotForm = model_form(Plot, base_class=FlaskForm, db_session=db.session)


class UserForm(FlaskForm):
    email = StringField("email", validators=[validators.Email()])
    password = PasswordField("password", validators=[
                             validators.InputRequired()])


class RegisterForm(UserForm):
    key = StringField("registration_key", validators=[
                      validators.InputRequired()])


def loginRequired():
    if not currentUser():
        flash("Only registered users can post their plots. Please login to your account.")
        abort(403)


@app.before_first_request
def initDb():
    db.create_all()

    plot = Plot(plot="An old dragon who lived by the sea becomes a vlogger. He faces monumental obstacles such as not having fingers for typing with a keyboard designed for humans and having a bad reputation as a fire breathing monstrosity.")
    db.session.add(plot)

    plot = Plot(plot="The plot is <writes a long, confusing text about a dog who loses its parents and befriends an unicorn with a dream of becoming the world's greatest painter>.")
    db.session.add(plot)

    plot = Plot(plot="A young girl moves to a small town and meets a young boy who turns out to be a vampire who sparkles in direct sunlight and drives a modest hatchback Volvo.")
    db.session.add(plot)

    user = User(email="admin@example.com", role="admin")
    user.setPassword("password")
    db.session.add(user)

    user = User(email="user@example.com", role="user")
    user.setPassword("password")
    db.session.add(user)

    db.session.commit()


@app.route("/edit/<int:id>", methods=["GET", "POST"])
# Create a method that restricts deleting posts to its author
@app.route("/new", methods=["GET", "POST"])
def newPlot(id=None):
    loginRequired()

    if id:
        plot = Plot.query.get_or_404(id)
    else:
        plot = Plot()

    form = PlotForm(obj=plot)

    if form.validate_on_submit():
        form.populate_obj(plot)

        db.session.add(plot)
        db.session.commit()

        flash("New comment posted!")
        return redirect("/")

    return render_template("new.html", form=form)


@app.route("/delete/<int:id>")
def deletePlot(id):
    loginRequired()
    plot = Plot.query.get_or_404(id)
    db.session.delete(plot)
    db.session.commit()
    flash("Your post has been deleted.")
    return redirect("/")


@app.route("/")
def index():
    plots = Plot.query.all()
    return render_template("index.html", plots=plots)


@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")


@app.errorhandler(403)
def custom403(e):
    return redirect("/login")


def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None
    return User.query.get(uid)


app.jinja_env.globals["currentUser"] = currentUser


@app.route("/login", methods=["GET", "POST"])
def loginView():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid login")
            return redirect("/login")
        if not user.checkPassword(password):
            flash("Invalid login")
            return redirect("/login")
        flash("Logged in, welcome!")
        session["uid"] = user.id
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logoutView():
    session["uid"] = None
    flash("You have been logged out from your account.")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def registerView():
    form = RegisterForm()
    if form.validate_on_submit():
        # Needs to be hidden or validated elsewhere
        if form.key.data != "joonas":
            flash("Bad registration key.")
            return redirect("/register")
        user = User()
        user.email = form.email.data
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your new account has been created.")
        return redirect("/login")
    return render_template("register.html", form=form, button="Login")


if __name__ == "__main__":
    app.run()
