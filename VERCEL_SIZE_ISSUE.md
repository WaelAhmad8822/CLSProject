# Vercel 250 MB Size Limit Issue

## Problem
Your serverless function exceeds Vercel's 250 MB unzipped size limit. This is because:
- **scikit-learn** (~50-80 MB)
- **numpy** (~30-50 MB) 
- **pandas** (~40-60 MB)
- **scipy** (~50-80 MB)
- **Flask + dependencies** (~10-20 MB)

**Total: ~180-290 MB** (exceeds the 250 MB limit)

## Solutions

### Option 1: Use Vercel Pro Plan (Recommended)
Vercel Pro plan has a **1 GB limit** for serverless functions, which should be enough.

### Option 2: Alternative Platforms (Better for ML Models)

#### A. Railway.app
- **No size limits** for serverless functions
- Easy Flask deployment
- Free tier available
- Better suited for ML workloads

**Deploy to Railway:**
1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`

#### B. Render.com
- **No hard size limits**
- Free tier available
- Good for Python/Flask apps

**Deploy to Render:**
1. Connect your GitHub repo
2. Create new "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`

#### C. Fly.io
- **No size limits**
- Free tier available
- Great for containerized apps

#### D. Google Cloud Run / AWS Lambda
- Pay-as-you-go
- Higher limits
- More complex setup

### Option 3: Optimize Dependencies (May Not Be Enough)

Try using even lighter versions (but may break compatibility):

```txt
Flask==3.0.0
joblib==1.3.2
pandas==2.0.3
scikit-learn==1.3.2
numpy==1.24.3
scipy==1.11.4
```

**Warning:** Older versions may not be compatible with your model if it was trained with newer versions.

### Option 4: Split Architecture

1. **Host model separately** on a service that supports large files
2. **Use Vercel** only for the API gateway
3. **Call external service** for predictions

This adds complexity but keeps you on Vercel.

## Recommendation

**For ML models with large dependencies, I recommend:**

1. **Railway.app** - Easiest migration, no size limits, free tier
2. **Render.com** - Simple deployment, good free tier
3. **Vercel Pro** - If you want to stay on Vercel ($20/month)

## Quick Migration to Railway

1. Create `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

2. Update `app.py` to work with Railway (it already should)

3. Deploy:
```bash
railway login
railway init
railway up
```

Would you like me to help you migrate to Railway or another platform?

