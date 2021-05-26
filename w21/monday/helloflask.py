from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/python")
def hellopython():
    return "Python is cool!"


@app.route("/base")
def base():
    return render_template("base.html")


app.run()
