from flask import Flask, request, render_template, jsonify
import joblib
import os

# Load model and vectorizer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))

# Initialize Flask
app = Flask(__name__)

# Home route - display form
@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        text = request.form.get('text')  # Get text from form
        vect_text = vectorizer.transform([text])
        prediction = model.predict(vect_text)[0]
    return render_template('index.html', prediction=prediction)

# API route - for programmatic use
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    vect_text = vectorizer.transform([text])
    prediction = model.predict(vect_text)[0]
    return jsonify({"prediction": int(prediction)})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sets this
    app.run(host="0.0.0.0", port=port)

