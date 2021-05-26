# w21 tuesday | Joonas Kulmala

- [w21 tuesday | Joonas Kulmala](#w21-tuesday--joonas-kulmala)
  - [Exercise goals & enviroment](#exercise-goals--enviroment)
  - [Exercises](#exercises)
    - [pw2.1 Muuttuja muottiin](#pw21-muuttuja-muottiin)
    - [pw2.2 Tuplamuuttuja](#pw22-tuplamuuttuja)
    - [pw2.3 Toista tätä, toista tätä](#pw23-toista-tätä-toista-tätä)
  - [Sources](#sources)
  - [Edit history](#edit-history)

## Exercise goals & enviroment

| Tool   | Version |
| ------ | ------- |
| Python | 3.8.5   |
| Flask  | 2.0.1   |

Flask and HTML templates.

## Exercises

Exercises are contained within subdirectories; [here](https://github.com/JoonasKulmala/Python-weppipalvelu/tree/main/w21/tuesday/Assignments).

### pw2.1 Muuttuja muottiin

`app.py`

    from flask import Flask, render_template
    app = Flask(__name__)

@app.route("/")
def base():
	return render_template("base.html")

@app.route("/colour")
def colours():
	colour = "blue"
	return render_template("colour.html", name=colour, colour=colour)

app.run()

### pw2.2 Tuplamuuttuja

### pw2.3 Toista tätä, toista tätä

## Sources

## Edit history