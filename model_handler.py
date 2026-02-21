import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_ml_assets():
    """Loads and returns the model and vectorizer."""
    model_path = os.path.join(BASE_DIR, "model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        raise FileNotFoundError("Model or vectorizer pickle files not found.")
        
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def predict_spam(text, model, vectorizer):
    """Predicts if a given text is spam or ham, returning label and probability."""
    if not text:
        return "Clean", 0.0
    
    vect_text = vectorizer.transform([text])
    prediction = model.predict(vect_text)[0]
    
    # Calculate probability if the model supports it
    probability = 0.0
    if hasattr(model, "predict_proba"):
        prob_array = model.predict_proba(vect_text)[0]
        # Get the probability of the predicted class
        probability = prob_array[1] if prediction == 1 else prob_array[0]
        probability = round(probability * 100, 2)
    
    label = "Spam" if prediction == 1 else "Clean"
    return label, probability