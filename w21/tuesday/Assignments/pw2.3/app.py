from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def base():
    return render_template("base.html")


@app.route("/colours")
def colours():
    colours = ["black", "white", "yellow", "red", "red"]
    return render_template("colours.html", name="Colours", colours=colours)


app.run()
