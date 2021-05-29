from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/python")
def python():
    return "Python is cool!"


@app.route("/foo")
def foo():
    return ("Foo is here all alone")


app.run()
