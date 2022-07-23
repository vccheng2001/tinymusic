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

keymap = {'A2': "A4",
	  'Bb2': "A#4",
	  'B2': "B4",
	  'C3': "c4",
	  'Db3': "c#4",
	  'D3': "d4",
	  'Eb3': "d#4",
	  'E3': "e4",
	  'F3': "f4",
	  'Gb3': "f#4",
	  'G3': "g4",
	  'Ab3': "g#4",
      'A3': "a4",
	  'Bb3': "a#4",
	  'B3': "b4",
      'C4': "c'4",
      'Db4':"c#'4",
	  'D4': "d'4",
      'Eb4': "d#'4",
      'E4': "e'4",
      'F4': "f'4",
      'Gb4': "f#'4",
      'G4': "g'4",
      'Ab4': "g#'4",
      'A4': "a'4",
      'Bb4': "a#'4",
      'B4': "b'4",
      'C5': "c''4",
 }

# Render index page
@app.route("/")
def index():
    return render_template("index.html")

# Notes are in TinyNotation format:
# https://web.mit.edu/music21/doc/usersGuide/usersGuide_16_tinyNotation.html
def process_notes(notes):
    notes = notes[:16]
    notestring = ''
    for i in range(len(notes)):
        notestring += keymap[notes[i]]
        notestring += ' '
        if (i+1) % 4 == 0:
            notestring += '| '
        
    print('final notestring:', notestring)
    return notestring
# Predict
@app.route("/api/predict", methods=["POST"])
def predict():
    body = request.get_json()
    timesignature = body['timesignature']
    tempo = body['tempo']
    notestring = process_notes(body['notes'])
    
    # Get model
    print('Fetching model and version......')
    model = replicate.models.get("andreasjansson/music-inpainting-bert")
    version = model.versions.get(
        "58bdc2073c9c07abcc4200fe808e15b1a555dbb1390e70f5daa6b3d81bd11fb1"
    )

    prediction = replicate.predictions.create(
        version=version,
        input={
            "notes": notestring,
            "chords": "Em | Em | ? | ? ",
            "time_signature": timesignature,
            "tempo": tempo, 
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
