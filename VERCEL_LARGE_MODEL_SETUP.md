# Vercel Deployment with Large Model File

## Problem
Vercel has a 250 MB unzipped size limit for serverless functions. Your model file and dependencies exceed this limit.

## Solution
The model file is now excluded from the deployment bundle and loaded from an external URL at runtime.

## Setup Steps

### Option 1: GitHub Releases (Recommended for Public Models)

1. **Create a GitHub Release:**
   ```bash
   # Tag your release
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Upload model as release asset:**
   - Go to your GitHub repo → Releases → Create a new release
   - Upload `gbr_pipeline.pkl` as a release asset
   - Copy the direct download URL (e.g., `https://github.com/WaelAhmad8822/CLSProject/releases/download/v1.0.0/gbr_pipeline.pkl`)

3. **Set environment variable in Vercel:**
   ```bash
   vercel env add MODEL_URL
   # Enter the GitHub release URL when prompted
   ```

### Option 2: GitHub Raw URL (If model is in repo)

If your model is committed to the repo:
```bash
# URL format: https://raw.githubusercontent.com/USERNAME/REPO/BRANCH/path/to/file.pkl
vercel env add MODEL_URL
# Enter: https://raw.githubusercontent.com/WaelAhmad8822/CLSProject/main/gbr_pipeline.pkl
```

### Option 3: AWS S3

1. **Upload to S3:**
   ```bash
   aws s3 cp gbr_pipeline.pkl s3://your-bucket-name/models/gbr_pipeline.pkl --acl public-read
   ```

2. **Get public URL:**
   ```
   https://your-bucket-name.s3.amazonaws.com/models/gbr_pipeline.pkl
   ```

3. **Set in Vercel:**
   ```bash
   vercel env add MODEL_URL
   # Enter the S3 URL
   ```

### Option 4: Vercel Blob Storage

1. **Install Vercel Blob:**
   ```bash
   npm install @vercel/blob
   ```

2. **Upload script (create upload_blob.js):**
   ```javascript
   const { put } = require('@vercel/blob');
   const fs = require('fs');
   
   async function upload() {
     const file = fs.readFileSync('gbr_pipeline.pkl');
     const blob = await put('gbr_pipeline.pkl', file, {
       access: 'public',
     });
     console.log('Model URL:', blob.url);
   }
   
   upload();
   ```

3. **Run upload:**
   ```bash
   node upload_blob.js
   ```

4. **Set MODEL_URL in Vercel to the returned URL**

### Option 5: Any Public File Hosting

You can use any service that provides direct download URLs:
- Google Drive (use direct download link)
- Dropbox (use direct download link)
- Any CDN or file hosting service

## Setting Environment Variable in Vercel

### Via CLI:
```bash
vercel env add MODEL_URL production
# Enter your model URL when prompted
```

### Via Dashboard:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add new variable:
   - Name: `MODEL_URL`
   - Value: Your model file URL
   - Environment: Production, Preview, Development (select all)

## Important Notes

- **First Request Will Be Slow**: The model downloads on the first request (cached after that)
- **Model Size**: Make sure your hosting service allows files of your model's size
- **Public Access**: The model URL must be publicly accessible (or use signed URLs with proper auth)
- **Caching**: The model is cached in memory after first load using `@lru_cache`

## Testing Locally

Before deploying, test locally:
```bash
export MODEL_URL="https://your-model-url.com/gbr_pipeline.pkl"
vercel dev
```

## Troubleshooting

- **Model not loading**: Check that MODEL_URL is set correctly
- **Timeout errors**: First request may timeout if model is very large - consider using a faster CDN
- **Memory issues**: If model is too large for serverless function memory, consider using a different platform

