"""
Vercel serverless function entry point for Flask app
This file handles all routes and serves as the main API handler
"""
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
from functools import lru_cache

app = Flask(__name__)

@lru_cache(maxsize=1)
def load_model():
    """Load the model with caching to avoid reloading on every request"""
    # In Vercel, files are in the same directory structure
    model_path = os.path.join(os.path.dirname(__file__), '..', 'gbr_pipeline.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return joblib.load(model_path)

# Load model at module level (cached)
GBR_pipeline = load_model()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running successfully", "status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        data = pd.DataFrame(json_data)
        
        new_data_transformed = GBR_pipeline.named_steps['preprocessor'].transform(data)
        prediction = GBR_pipeline.named_steps['regressor'].predict(new_data_transformed)
        
        return jsonify({'Prediction': prediction.tolist()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Export Flask app for Vercel
# Vercel will automatically detect and use the 'app' variable

