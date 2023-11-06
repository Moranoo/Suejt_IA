import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import spacy

app = Flask(__name__)
CORS(app)

# Chargez le modèle Spacy une fois
nlp = spacy.load('en_core_web_lg')

# Fonction pour traiter le commentaire


def treat_comment(comment):
    spacy_comment = nlp(
        comment, disable=["parser", "tagger", "ner", "textcat"])
    treated_tokens = [
        token.text for token in spacy_comment if token.is_alpha and not token.is_stop]
    return " ".join(treated_tokens)


# Charger le modèle et le vectorisateur une seule fois
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Endpoint pour la prédiction


@app.route("/api/predict", methods=["POST"])
@cross_origin()
def predict():
    data = request.json
    text = data.get("comment", "")
    treated_text = treat_comment(text)
    format_vector = vectorizer.transform([treated_text])
    prediction = model.predict(format_vector)
    return jsonify({"prediction": prediction.tolist()})


if __name__ == "__main__":
    app.run(debug=True)
