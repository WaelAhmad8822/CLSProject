"""
Vercel serverless function entry point for Flask app
This file handles all routes and serves as the main API handler
"""
import sys
import os

# CRITICAL: Force Python to use installed sklearn, not Vercel's vendored version
# Vercel bundles sklearn in _vendor directory which causes version conflicts
def fix_sklearn_imports():
    """Remove vendored sklearn from sys.modules and sys.path"""
    # Remove _vendor paths from sys.path
    sys.path = [p for p in sys.path if '_vendor' not in p]
    
    # Remove any sklearn modules that might have been imported from vendor
    modules_to_remove = [k for k in sys.modules.keys() if k.startswith('sklearn')]
    for mod in modules_to_remove:
        if '_vendor' in str(sys.modules[mod].__file__ if hasattr(sys.modules[mod], '__file__') else ''):
            del sys.modules[mod]
    
    # Ensure site-packages is first in path
    import site
    site_packages = site.getsitepackages()
    for sp in site_packages:
        if sp not in sys.path:
            sys.path.insert(0, sp)

# Fix imports before anything else
fix_sklearn_imports()

from flask import Flask, request, jsonify
import joblib
import pandas as pd
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
    
    # Re-fix imports before loading model (in case they got messed up)
    fix_sklearn_imports()
    
    # Import sklearn AFTER fixing paths
    import sklearn
    import importlib
    
    # Force reload sklearn.compose._column_transformer to ensure we get the right version
    if 'sklearn.compose._column_transformer' in sys.modules:
        del sys.modules['sklearn.compose._column_transformer']
    if 'sklearn.compose' in sys.modules:
        del sys.modules['sklearn.compose']
    
    # Import fresh from site-packages
    ct_module = importlib.import_module('sklearn.compose._column_transformer')
    
    print(f"Using scikit-learn version: {sklearn.__version__}")
    print(f"sklearn location: {sklearn.__file__}")
    print(f"Column transformer location: {ct_module.__file__}")
    print(f"Has _RemainderColsList: {hasattr(ct_module, '_RemainderColsList')}")
    
    # Verify we have the required attribute
    if not hasattr(ct_module, '_RemainderColsList'):
        raise RuntimeError(
            f"scikit-learn version mismatch! The installed version ({sklearn.__version__}) "
            f"does not have _RemainderColsList attribute. This model requires scikit-learn 1.7.2. "
            f"sklearn path: {sklearn.__file__}"
        )
    
    # Download model to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp_file:
        try:
            print(f"Downloading model from {MODEL_URL}...")
            urllib.request.urlretrieve(MODEL_URL, tmp_file.name)
            print("Model downloaded successfully, loading...")
            
            # Load model - joblib should now use the correct sklearn version
            model = joblib.load(tmp_file.name)
            print("Model loaded successfully")
            return model
        except AttributeError as e:
            error_msg = str(e)
            if '_RemainderColsList' in error_msg:
                raise RuntimeError(
                    f"Failed to load model: Vercel is using vendored sklearn from _vendor directory. "
                    f"Please ensure requirements.txt has scikit-learn==1.7.2 and redeploy. "
                    f"Current sklearn version: {sklearn.__version__}, "
                    f"sklearn path: {sklearn.__file__}. "
                    f"Error: {error_msg}"
                )
            raise
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
    """Health check endpoint"""
    return jsonify({"message": "API is running successfully", "status": "ok"})

@app.route('/check-version', methods=['GET'])
def check_version():
    """Debug endpoint to check sklearn version and paths"""
    try:
        fix_sklearn_imports()
        import sklearn
        import sklearn.compose._column_transformer as ct_module
        
        info = {
            "sklearn_version": sklearn.__version__,
            "sklearn_location": sklearn.__file__,
            "column_transformer_location": ct_module.__file__,
            "has_remainder_cols_list": hasattr(ct_module, '_RemainderColsList'),
            "is_vendored": '_vendor' in sklearn.__file__ if hasattr(sklearn, '__file__') else False,
            "python_version": sys.version,
            "sys_path": sys.path[:5]  # First 5 paths
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

