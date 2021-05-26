from flask import Flask, render_template, redirect, flash
app = Flask(__name__)


@app.route("/foo")
def sooMsg():
    flash("Foo says hello!!")
    return redirect("/")


@ap.route(/"bar")
def barMsg():
    flash("Bar wishes you well!")
    return redirect("/")


if __name__ == "__main__":
    app.run()
