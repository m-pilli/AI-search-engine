# 🚀 Deployment Guide: AI Search Engine

This guide will help you deploy your AI Search Engine to GitHub and Vercel.

## 📋 Prerequisites

1. **Git** installed (check with `git --version`)
2. **GitHub account** (create at https://github.com)
3. **Vercel account** (create at https://vercel.com - can sign up with GitHub)

---

## Step 1: Push to GitHub

### 1.1 Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
# Check if git is already initialized
git status

# If not initialized, run:
git init
git branch -M main
```

### 1.2 Create .gitignore (Already Created ✅)

The `.gitignore` file is already created to exclude sensitive files.

### 1.3 Add and Commit Files

```powershell
git add .
git commit -m "Initial commit: AI Search Engine with React frontend and Flask backend"
```

### 1.4 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ai-search-engine` (or any name you like)
3. **DO NOT** initialize with README, .gitignore, or license
4. Click **"Create repository"**

### 1.5 Push to GitHub

```powershell
# Replace YOUR_USERNAME and REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

**If asked for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)
  - Create token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Select scope: `repo`
  - Copy token and use as password

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Connect Vercel to GitHub

1. Go to https://vercel.com/login
2. Click **"Sign up"** and choose **"Continue with GitHub"**
3. Authorize Vercel to access your GitHub account

### 2.2 Import Your Repository

1. Click **"Add New..."** → **"Project"**
2. Find your `ai-search-engine` repository
3. Click **"Import"**

### 2.3 Configure Frontend Project

**Important Settings:**

- **Framework Preset**: `Create React App`
- **Root Directory**: `frontend` (click "Edit" next to Root Directory)
- **Build Command**: `npm run build` (automatically detected)
- **Output Directory**: `build` (automatically detected)
- **Install Command**: `npm install` (automatically detected)

### 2.4 Set Environment Variables

Click **"Environment Variables"** and add:

```
Name: REACT_APP_API_URL
Value: http://localhost:5000/api
```

**⚠️ Note:** For now, this is set to localhost. You'll update this after deploying the backend.

### 2.5 Deploy!

Click **"Deploy"** button and wait 2-3 minutes.

**Your frontend will be live at:** `https://your-project-name.vercel.app`

---

## Step 3: Deploy Backend (Choose One Option)

### Option A: Render.com (Recommended - Free Tier Available)

1. Go to https://render.com and sign up (free account)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-search-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Instance Type**: `Free` (512MB RAM - upgrade if needed for AI models)

5. **Add Environment Variables:**
   ```
   MONGODB_URI=mongodb://localhost:27017/search_engine
   REDIS_URL=redis://localhost:6379/0
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   SECRET_KEY=your-secret-key-here
   PORT=5000
   CORS_ORIGINS=https://your-project-name.vercel.app
   ```

6. Click **"Create Web Service"**

7. **Get your backend URL:** `https://ai-search-backend.onrender.com`

8. **Update Vercel Environment Variable:**
   - Go back to Vercel → Your Project → Settings → Environment Variables
   - Update `REACT_APP_API_URL` to: `https://ai-search-backend.onrender.com/api`
   - Redeploy frontend

### Option B: Railway.app

1. Go to https://railway.app and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Click **"Add Service"** → **"Dockerfile"**
5. Set **Root Directory** to `backend`
6. Add environment variables (same as Render)
7. Deploy!

---

## Step 4: Update Frontend API URL

After your backend is deployed:

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Update `REACT_APP_API_URL` to your backend URL:
   ```
   https://your-backend-url.onrender.com/api
   ```
3. Go to **Deployments** tab
4. Click **"..."** (three dots) on latest deployment → **"Redeploy"**

---

## Step 5: Test Your Deployment

1. **Frontend**: Visit `https://your-project-name.vercel.app`
2. **Backend Health**: Visit `https://your-backend-url.onrender.com/api/health`
3. **Test Search**: Try searching in your deployed frontend!

---

## 🔧 Troubleshooting

### Frontend shows "Network Error"
- Check if backend is running and accessible
- Verify `REACT_APP_API_URL` in Vercel environment variables
- Check browser console for CORS errors

### Backend deployment fails
- Check Render/Railway logs
- Ensure MongoDB and Redis URLs are correct
- Verify Dockerfile is correct

### CORS Errors
- Add your Vercel frontend URL to backend `CORS_ORIGINS` environment variable
- Restart backend service

---

## 📝 Quick Commands Reference

```powershell
# Git commands
git status
git add .
git commit -m "Update: description"
git push

# Local testing
cd frontend && npm start
cd backend && docker-compose up

# Check deployed URLs
# Frontend: Check Vercel dashboard
# Backend: Check Render/Railway dashboard
```

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Frontend on Vercel (fast, globally distributed)
- ✅ Backend on Render/Railway (with Docker support)
- ✅ Your AI Search Engine live on the internet!

**Share your live URL:** `https://your-project-name.vercel.app`

