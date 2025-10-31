# 🚀 Backend Deployment Guide - Render.com

## Why Deploy Backend Separately?

- **Vercel** = Frontend hosting (React apps) ✅ Already deployed
- **Render/Railway** = Backend hosting (Docker/Python) ⚠️ Needs deployment

---

## Step 1: Deploy Backend to Render.com (FREE)

### 1.1 Sign Up
- Go to: https://render.com
- Click "Sign Up" → Use GitHub account (same as Vercel)

### 1.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `m-pilli/AI-search-engine`
3. Click **"Connect"**

### 1.3 Configure Backend
- **Name**: `ai-search-backend`
- **Root Directory**: `backend`
- **Environment**: **Docker**
- **Dockerfile Path**: `backend/Dockerfile`
- **Instance Type**: **Free** (512MB RAM - upgrade if needed)

### 1.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

```
MONGODB_URI = mongodb://localhost:27017/search_engine
REDIS_URL = redis://localhost:6379/0
EMBEDDING_MODEL = all-MiniLM-L6-v2
SECRET_KEY = your-secret-key-change-this
PORT = 5000
CORS_ORIGINS = https://ai-search-engine-frontend-ktasoc3u0-m-pillis-projects.vercel.app
```

**Note:** For production, you'll need:
- **MongoDB Atlas** (free tier) - https://www.mongodb.com/cloud/atlas
- **Upstash Redis** (free tier) - https://upstash.com

### 1.5 Deploy!
- Click **"Create Web Service"**
- Wait 5-10 minutes for first build
- Get your backend URL: `https://ai-search-backend.onrender.com`

---

## Step 2: Update Frontend API URL

### 2.1 Update Vercel Environment Variable
1. Go to: https://vercel.com/dashboard
2. Your project → **Settings** → **Environment Variables**
3. Edit `REACT_APP_API_URL`:
   - **Value**: `https://ai-search-backend.onrender.com/api`
   - **Save**

### 2.2 Redeploy Frontend
- Go to **Deployments** tab
- Click **"..."** → **"Redeploy"**
- Wait for completion

---

## Step 3: Update CORS in Backend

If CORS errors occur, update `backend/app.py`:

```python
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://ai-search-engine-frontend-ktasoc3u0-m-pillis-projects.vercel.app")
CORS(app, origins=[CORS_ORIGINS], supports_credentials=True)
```

Then push to GitHub (Render auto-redeploys).

---

## Alternative: Railway.app

If Render doesn't work:

1. Go to: https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. Select your repository
4. **Add Service** → **Dockerfile**
5. Set **Root Directory** to `backend`
6. Add same environment variables
7. Deploy!

---

## Current Status

✅ **Frontend**: Deployed on Vercel  
⚠️ **Backend**: Still running locally (needs deployment)  
🔧 **Solution**: Deploy backend to Render/Railway

---

## After Deployment

Your complete stack will be:
- **Frontend**: https://ai-search-engine-frontend-ktasoc3u0-m-pillis-projects.vercel.app/
- **Backend**: https://ai-search-backend.onrender.com/api
- **Full Integration**: Frontend → Backend → Working! 🎉

