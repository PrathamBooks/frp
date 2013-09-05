from flask import Flask, render_template

import settings

app = Flask(__name__)
app.config.from_object(settings)

__VERSION__ = "0.1"

@app.route("/")
def hello():
    name = "Noufal Ibrahim"
    return render_template("index.html", name = name)

if __name__ == "__main__":
    app.run()
