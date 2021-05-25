from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    colours = ["black", "white", "yellow", "red", "red"]
    return render_template("base.html", name="Colours", colours=colours)


app.run()
