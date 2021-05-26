from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def base():
	greeting="Hello there!"
	return render_template("base.html", name=greeting, greeting=greeting)

app.run()
