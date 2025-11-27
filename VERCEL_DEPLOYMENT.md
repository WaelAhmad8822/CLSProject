# Vercel Deployment Guide

## Files Structure
```
Final/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── app.py                # Flask app (for local testing)
├── gbr_pipeline.pkl      # Trained model file
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── .vercelignore        # Files to ignore during deployment
```

## Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy to Vercel
From your project directory:
```bash
vercel
```

For production deployment:
```bash
vercel --prod
```

### 4. Important Notes

- **Model File Size**: Vercel has a 50MB limit for serverless functions. If `gbr_pipeline.pkl` is larger, you may need to:
  - Use Vercel's Blob Storage
  - Or use a different hosting solution for large models

- **API Endpoints**:
  - `GET /` - Health check endpoint
  - `POST /predict` - Prediction endpoint

- **Testing Locally**:
  ```bash
  vercel dev
  ```

### 5. Environment Variables
If you need any environment variables, add them via:
- Vercel Dashboard → Your Project → Settings → Environment Variables
- Or via CLI: `vercel env add VARIABLE_NAME`

### 6. Troubleshooting

- **Import Errors**: Make sure all dependencies are in `requirements.txt`
- **Model Not Found**: Ensure `gbr_pipeline.pkl` is in the root directory
- **Timeout Issues**: Vercel has a 10s timeout for Hobby plan, 60s for Pro

## API Usage

### Health Check
```bash
curl https://your-project.vercel.app/
```

### Prediction
```bash
curl -X POST https://your-project.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": [value1], "feature2": [value2], ...}'
```

