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

# Predict
@app.route("/api/predict", methods=["POST"])
def predict():
    body = request.get_json()
    notes = body['notes']
    
    # Get model
    print('Fetching model and version......')
    model = replicate.models.get("andreasjansson/music-inpainting-bert")
    version = model.versions.get(
        "58bdc2073c9c07abcc4200fe808e15b1a555dbb1390e70f5daa6b3d81bd11fb1"
    )

    prediction = replicate.predictions.create(
        version=version,
        input={
            "notes": notes,
            "time_signature": 4,
            "tempo": 100,
            "sample_width": 80,
            "seed": -1
        },
    )
    
    return jsonify({"prediction_id": prediction.id})#, "score": prediction.score})

# Get prediction by its ID
@app.route("/api/predictions/<prediction_id>", methods=["GET"])
def get_prediction(prediction_id):
    prediction = replicate.predictions.get(prediction_id)
    output = None
    
    if prediction.output:
        print('Prediction output', prediction.output)
        import time
        time.sleep(5)
    return jsonify({"output": prediction.output, "status": prediction.status})


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(debug=True)
