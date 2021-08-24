"""Server for student lab pairs."""

from flask import Flask, render_template, redirect, request, session

import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
app.jinja_env.undefined = StrictUndefined


##################################################################
# ROUTES #
##################################################################

@app.route("/")
def show_homepage():
    return render_template("index.html")


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)
