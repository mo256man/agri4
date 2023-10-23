from flask import Flask, render_template, request
from myEphem import Ephem
import json
import random
from time import sleep
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index_vkey.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
