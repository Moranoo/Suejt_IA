import pandas as pd
import numpy as np
import pickle
import spacy

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def treat_comment(comment):
  nlp = spacy.load('en_core_web_lg')
  spacy_comment = nlp(comment, disable=["parser", "tagger", "ner", "textcat"])
  treated_tokens = []
  i = 0
  for w in spacy_comment:
    if w.is_alpha and not w.is_stop:
      i += 1
      print(f"Token {i}: {w.text}")
      treated_tokens.append(w.text)
  return " ".join(treated_tokens)

with open('Fmodel.pkl', 'rb') as f:
    model = pickle.load(f)

with open('XVect.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route("/api/predict")
@cross_origin()
def predict():
  text = 'je fais un test'
  model = pickle.load(open("Fmodel.pkl", "rb"))
  vectorizer = pickle.load(open("XVect.pkl", "rb"))
  formatVector = vectorizer.tranform([treat_comment(text)])
  prediction = model.predict(formatVector)
  print(prediction)
  return jsonify(prediction)


if __name__ == "__main__":
    app.run(debug=True)
