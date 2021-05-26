from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def base():
    return render_template("base.html")


@app.route("/colours")
def colours():
    colours = ["black", "white", "yellow", "red", "red"]
    return render_template("colours.html", name="Colours", colours=colours)


@app.route("/foo")
def foo():
    return render_template("foo.html")


@app.route("/maths")
def maths():
    number = 1
    return render_template("maths.html", number=number)


@app.route("/form", methods=["GET", "POST"])
def form():
    return render_template("form.html")


app.run()
