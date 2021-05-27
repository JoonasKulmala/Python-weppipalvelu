from flask import Flask, render_template, redirect, flash
app = Flask(__name__)

app.secret_key = b"jXef7J2hirwCA8DW9CxIdHm88wJhvY"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/foo")
def fooMsg():
    flash("Foo says hello!")
    return redirect("/")


@app.route("/bar")
def barMsg():
    flash("Bar wishes you well!")
    return redirect("/")


if __name__ == "__main__":
    app.run()
