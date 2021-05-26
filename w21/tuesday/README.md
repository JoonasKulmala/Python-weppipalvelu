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

Flask and HTML templating.

## Exercises

All files are contained within subdirectories here: [Assignments](https://github.com/JoonasKulmala/Python-weppipalvelu/tree/main/w21/tuesday/Assignments).

### pw2.1 Muuttuja muottiin

A variable needs to be rendered in HTML. Let's declare a variable in flask app and make that happen.

In the flask application `app.py`, simply declare variable *greeting* and instruct HTML file what to render.

```
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def base():
    greeting = "Hello there!"
    return render_template("base.html", name=greeting, greeting=greeting)


app.run()
```

Next up instruct `base.html` where to render the variable - note the line `<p>{{ greeting }}</p>`

 ```
  <!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name=viewport content "width=device-width; initial-scale=1" <title>
  {% block title %}

  {% block headline %}

  {% endblock headline %}

  {% endblock title %}
  </title>
  <style>
  </style>
</head>

<body>
  <article>
    {% block content %}
    <p>{{ greeting }}</p>
    {% endblock content %}
  </article>
</body>

</html>
 ```

 Now run the application and open browser:

    $ python3 app.py

![screenshot](Assignments/pw2.1/Resources/pw2.1_browser.png)

### pw2.2 Tuplamuuttuja

Templating HTML files. No point creating each HTML from the scratch when we can just use the base boilerplate over and over again.

Let's add some functionality to `app.py` by having endpoints **/foo** and **/bar** redirect to corresponding HTML files

```
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def base():
    return render_template("base.html")


@app.route("/foo")
def foo():
    return render_template("foo.html")


@app.route("/bar")
def bar():
    return render_template("bar.html")


app.run()
```

Empty template HTML `base.html` where content rendering has been assigned

```
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name=viewport content "width=device-width; initial-scale=1" <title>
  {% block title %}

  {% block headline %}

  {% endblock headline %}

  {% endblock title %}
  </title>
  <style>
  </style>
</head>

<body>
  <article>
    {% block content %}

    {% endblock content %}
  </article>
</body>

</html>
```

Next up `foo.html` and `bar.html` files which **extend** `base.html`

```
{% extends "base.html" %}

{% block title %}
foo
{% endblock title %}

{% block content %}
<h3>/foo should display this paragraph</h3>
{% endblock content %}
```
![foo](Assignments/pw2.2/Resources/foo_browser.png)

```
{% extends "base.html" %}

{% block title %}
bar
{% endblock title %}

{% block content %}
<h3>/bar should display this paragraph</h3>
{% endblock content %}
```
![bar](Assignments/pw2.2/Resources/bar_html.png)

### pw2.3 Toista tätä, toista tätä

Let's render a list of colours in an array.

```
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
```

Using the same `base.html` template as previously, let's create extending file `colours.html`

```
{% extends "base.html" %}


{% block title %}
<h1> List of {{ name }}</h1>
{% endblock title %}

{% block content %}
{% block body %}
{% for colour in colours %}
<p>{{ colour }}</p>
{% endfor %}
{% endblock body %}
{% endblock content %}
```

![colours](Assignments/pw2.3/Resources/colours_browser.png)

## Sources

Tero Karvinen - [Python Web Service From Idea to Production #pw2](https://terokarvinen.com/2021/python-web-service-from-idea-to-production/#pw2-muotit-ja-lomakkeet)

## Edit history