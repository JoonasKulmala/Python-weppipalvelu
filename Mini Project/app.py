from flask import Flask, render_template, flash, redirect, session, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import StringField, PasswordField, validators, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Postgres database, comment out to use in-memory database
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///your_database_name"
app.secret_key = "phi7ThothioLeopa0pai"  # pwgen -1 20
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    postId = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False, default="user")
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)


PostForm = model_form(Post, base_class=FlaskForm, db_session=db.session)

CommentForm = model_form(Comment, base_class=FlaskForm, db_session=db.session)


class UserForm(FlaskForm):
    email = StringField("email", validators=[validators.Email()])
    password = PasswordField("password", validators=[
                             validators.InputRequired()])


class RegisterForm(UserForm):
    key = StringField("registration_key", validators=[
                      validators.InputRequired()])


# Test data, do not deploy in production. Always use secure passwords.
@app.before_first_request
def initDb():
    db.create_all()

    post = Post(post="How cold is it in space?")
    db.session.add(post)

    post = Post(post="Hey people, take a look at my new car!")
    db.session.add(post)

    comment = Comment(
        comment="Better put on some layers if you're moonwalking.", postId=1)
    db.session.add(comment)

    comment = Comment(
        comment="What model year is your car? It looks brand new :)", postId=2)
    db.session.add(comment)

    user = User(email="admin@example.com", role="admin")
    user.setPassword("password")
    db.session.add(user)

    user = User(email="user@example.com", role="user")
    user.setPassword("password")
    db.session.add(user)

    db.session.commit()


def loginRequired():
    if not currentUser():
        flash("Only registered users can post new threads. Please login to your account.")
        abort(403)


@app.route("/<int:id>", methods=["GET", "POST"])
def thread(id):
    posts = Post.query.filter_by(id=id)
    return render_template("thread.html", posts=posts)


# Update, Create new Post
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def newPost(id=None):
    loginRequired()
    if id:
        post = Post.query.get_or_404(id)
    else:
        post = Post()
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        flash("New thread created!")
        return redirect("/")

    return render_template("new.html", form=form)


# DELETE Post
@app.route("/delete/<int:id>")
def deletePost(id):
    loginRequired()
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.")
    return redirect("/")


# Incomplete: User profile page
@app.route("/profile")
def profile():
    return render_template("profile.html")


# Main page
@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


# Error handling
@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")


# Error handling
@app.errorhandler(403)
def custom403(e):
    return redirect("/login")


# User login session
def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None
    return User.query.get(uid)


app.jinja_env.globals["currentUser"] = currentUser


# Authenticate login
@app.route("/login", methods=["GET", "POST"])
def loginView():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid login.")
            return redirect("/login")
        if not user.checkPassword(password):
            flash("Invalid login.")
            return redirect("/login")
        flash("Login successful!")
        session["uid"] = user.id
        return redirect("/")

    return render_template("login.html", form=form)


# User logout
@app.route("/logout")
def logoutView():
    session["uid"] = None
    flash("Logged out")
    return redirect("/")


# Authenticate registration
@app.route("/register", methods=["GET", "POST"])
def registerView():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        if email and User.query.filter_by(email=email).first():
            flash('Email address already registered for an account.')
            return redirect("/register")
        if form.key.data != "your_key_name":  # Use secure name for registration key
            flash("Bad registration key.")
            return redirect("/register")
        user = User()
        user.email = form.email.data
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("New account created!")
        return redirect("/login")

    return render_template("register.html", form=form, button="Login")


# Remove from production deployment build
if __name__ == "__main__":
    app.run()
