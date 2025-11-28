# Fixing Vercel "No module named 'flask'" Error

## Problem
Vercel is not installing dependencies from `requirements.txt`, causing `ModuleNotFoundError: No module named 'flask'`.

## Solutions to Try

### Solution 1: Ensure requirements.txt is in Root
Make sure `requirements.txt` is in the **root directory** of your repository (same level as `vercel.json`).

### Solution 2: Check Build Logs
In Vercel Dashboard:
1. Go to your project → Deployments
2. Click on the failed deployment
3. Check the "Build Logs" tab
4. Look for messages like:
   - "Installing required dependencies from requirements.txt..."
   - Any pip install errors
   - Size limit errors

### Solution 3: Verify File Structure
Your repo should have:
```
/
├── api/
│   └── index.py
├── requirements.txt  ← Must be here
├── vercel.json
└── runtime.txt (optional)
```

### Solution 4: Force Rebuild
1. In Vercel Dashboard → Settings → General
2. Clear build cache
3. Redeploy

### Solution 5: Check if Build is Completing
The error suggests the build might be failing silently. Check:
- Build logs for any errors
- If you see "Build Completed" but then get import errors, dependencies aren't being installed

### Solution 6: Alternative - Use Build Command
If automatic detection isn't working, you might need to add an explicit build step, but Vercel Python should handle this automatically.

## Most Likely Cause
Given the previous 250MB size limit errors, the build is probably **failing before dependencies are installed**. The dependencies (scikit-learn, numpy, pandas, scipy) are too large for Vercel's free tier.

## Recommended Action
**Consider migrating to Railway or Render** which don't have these size limits and are better suited for ML applications.

