from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
from functools import lru_cache

# Create a Flask app
app = Flask(__name__)

@lru_cache(maxsize=1)
def load_model():
    """Load the model with caching to avoid reloading on every request"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'gbr_pipeline.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return joblib.load(model_path)

# Load model at startup
GBR_pipeline = load_model()

@app.route('/')
def home():
    return "Now Run Successfully......"


# Define an API endpoint for image classification
@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
        data = pd.DataFrame(json_data)

        new_data_transformed = GBR_pipeline.named_steps['preprocessor'].transform(data)

        prediction = GBR_pipeline.named_steps['regressor'].predict(new_data_transformed)

        return jsonify({'Prediction': prediction.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)})



# if __name__ == '__main__':
#     app.run()