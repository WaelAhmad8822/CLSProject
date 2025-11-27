# Deploying to PythonAnywhere

1. **Upload project files**
   - Upload `app.py`, `gbr_pipeline.pkl`, and `requirements.txt` into a new PythonAnywhere project directory (e.g. `/home/<user>/mysite/`).

2. **Create a virtual environment**
   ```bash
   mkvirtualenv --python=python3.10 flask-app
   workon flask-app
   pip install -r /home/<user>/mysite/requirements.txt
   ```

3. **Configure the web app**
   - On the PythonAnywhere dashboard, create a new **Flask** web app that points to the same Python version as the virtualenv.
   - Edit the WSGI configuration file so the last lines read:
     ```python
     import sys
     path = '/home/<user>/mysite'
     if path not in sys.path:
         sys.path.append(path)

     from app import application  # Flask instance exposed in app.py
     ```
   - Set the virtualenv path to `/home/<user>/.virtualenvs/flask-app`.

4. **Reload**
   - Click **Reload** on the PythonAnywhere web app page. The `/` route should show the JSON health response, and `/predict` accepts POSTed JSON.

5. **Testing locally**
   ```bash
   python app.py
   curl -X POST http://localhost:5000/predict \
        -H "Content-Type: application/json" \
        -d '[{"feature_a": 1, "feature_b": 2}]'
   ```

