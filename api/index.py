"""
Vercel serverless function entry point for Flask app
This file handles all routes and serves as the main API handler
"""
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
import urllib.request
import tempfile
from functools import lru_cache

app = Flask(__name__)

# Get model URL from environment variable or use default
MODEL_URL = os.environ.get('MODEL_URL', '')

@lru_cache(maxsize=1)
def load_model():
    """Load the model from URL with caching to avoid reloading on every request"""
    if not MODEL_URL:
        raise ValueError(
            "MODEL_URL environment variable not set. "
            "Please set it to the URL where your model file is hosted "
            "(e.g., GitHub raw URL, S3, or Vercel Blob Storage)"
        )
    
    # Download model to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp_file:
        try:
            print(f"Downloading model from {MODEL_URL}...")
            urllib.request.urlretrieve(MODEL_URL, tmp_file.name)
            print("Model downloaded successfully, loading...")
            model = joblib.load(tmp_file.name)
            print("Model loaded successfully")
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {MODEL_URL}: {str(e)}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file.name)
            except:
                pass

# Load model lazily on first request
GBR_pipeline = None

def get_model():
    """Get the model, loading it if necessary"""
    global GBR_pipeline
    if GBR_pipeline is None:
        GBR_pipeline = load_model()
    return GBR_pipeline

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API is running successfully", "status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get model (loads on first request)
        pipeline = get_model()
        
        data = pd.DataFrame(json_data)
        
        new_data_transformed = pipeline.named_steps['preprocessor'].transform(data)
        prediction = pipeline.named_steps['regressor'].predict(new_data_transformed)
        
        return jsonify({'Prediction': prediction.tolist()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Export Flask app for Vercel
# Vercel will automatically detect and use the 'app' variable

