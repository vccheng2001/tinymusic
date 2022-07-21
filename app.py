import json
import replicate
from flask import (
    Flask,
    jsonify,
    render_template,
    send_from_directory,
    request,
)
import random 
app = Flask(__name__)

# Render index page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
