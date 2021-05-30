from flask import Flask, render_template, flash, redirect, session, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, validators, SubmitField
# from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///joonas"  # ???
app.secret_key = "ojiemieCh3eeMee4vahX"
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)  # String -> Comment


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)


CommentForm = model_form(Comment, base_class=FlaskForm, db_session=db.session)


class UserForm(FlaskForm):
    email = StringField("email", validators=[validators.Email()])
    password = PasswordField("password", validators=[
                             validators.InputRequired()])


class RegisterForm(UserForm):
    key = StringField("registration_key", validators=[
                      validators.InputRequired()])


# Define constant for redirecting to /login
# LOGIN = redirect("/login")

def loginRequired():
    if not currentUser():
        flash("Only registered users can leave comments. Please login to your account.")
        abort(403)


@app.before_first_request
def initDb():
    db.create_all()

    comment = Comment(comment="Comment 1 <asks a question>")
    db.session.add(comment)

    comment = Comment(comment="Comment 2 <answer the question>")
    db.session.add(comment)

    comment = Comment(comment="Comment 3 <makes a bad joke>")
    db.session.add(comment)

    user = User(email="user@example.com")
    user.setPassword("mxitpkxw")
    db.session.add(user)

    db.session.commit()


@app.route("/edit/<int:id>", methods=["GET", "POST"])
# def deleteComment():
#    return render_template("/base.html")
@app.route("/new", methods=["GET", "POST"])
def newComment(id=None):
    loginRequired()

    if id:
        comment = Comment.query.get_or_404(id)
    else:
        comment = Comment()

    form = CommentForm(obj=comment)

    if form.validate_on_submit():
        form.populate_obj(comment)

        db.session.add(comment)
        db.session.commit()

        flash("New comment posted!")
        return redirect("/")

    return render_template("new.html", form=form)


@app.route("/delete/<int:id>")
def deleteComment(id):
    loginRequired()
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("Deleted")
    return redirect("/")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/")
def index():
    comments = Comment.query.all()
    return render_template("index.html", comments=comments)


@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")


@app.errorhandler(403)
def custom403(e):
    # LOGIN
    return redirect("/login")


def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None
    return User.query.get(uid)


app.jinja_env.globals["currentUser"] = currentUser


# def loginRequired():
#   if not currentUser():
#      abort(403)


@app.route("/login", methods=["GET", "POST"])
def loginView():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid login")
            print("No such user")
            return redirect("/login")
        if not user.checkPassword(password):
            flash("Invalid login")
            print("bad password")
            return redirect("/login")
        flash("Logged in. Welcome")
        session["uid"] = user.id
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logoutView():
    session["uid"] = None
    flash("Logged out")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def registerView():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.key.data != "joonas":
            flash("Bad registration key.")
            return redirect("/register")
        user = User()
        user.email = form.email.data
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User created")
        return redirect("/login")
    return render_template("register.html", form=form, button="Login")


if __name__ == "__main__":
    app.run()
