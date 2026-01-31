from flask import Flask, request, render_template, jsonify
import joblib
import os

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Heroku provides PORT
    app.run(host="0.0.0.0", port=port)

