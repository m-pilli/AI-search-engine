# 🚀 Quick Steps: Deploy to GitHub + Vercel

## ✅ Step 1: Commit to Git (Do this first!)

All files are ready! Just run:

```powershell
git commit -m "Initial commit: AI Search Engine - Full Stack Application"
```

## ✅ Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `ai-search-engine` (or any name)
3. **Leave everything unchecked** (no README, .gitignore, license)
4. Click **"Create repository"**

## ✅ Step 3: Push to GitHub

After creating the repo, GitHub will show you commands. Run these in PowerShell:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**⚠️ If asked for password:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your GitHub password)
  - How to get token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
  - Name: `vercel-deploy`
  - Select scope: ✅ `repo` (full control of private repositories)
  - Click "Generate token"
  - **Copy the token** and use it as password

## ✅ Step 4: Deploy Frontend to Vercel

1. Go to: https://vercel.com
2. Click **"Sign up"** → **"Continue with GitHub"**
3. Click **"Add New..."** → **"Project"**
4. Find your repository and click **"Import"**

### Vercel Settings:

- **Framework Preset**: `Create React App` (auto-detected)
- **Root Directory**: Click **"Edit"** → Type `frontend`
- **Build Command**: `npm run build` (auto)
- **Output Directory**: `build` (auto)
- **Install Command**: `npm install` (auto)

### Environment Variables:

Click **"Environment Variables"** and add:

```
REACT_APP_API_URL = http://localhost:5000/api
```

(You'll update this after backend deployment)

5. Click **"Deploy"** ✨

**Your frontend will be live at:** `https://your-repo-name.vercel.app`

---

## 📝 Next Steps (After Vercel Deployment)

To deploy the backend:
1. See [DEPLOYMENT.md](./DEPLOYMENT.md) for backend hosting options (Render/Railway)
2. Update `REACT_APP_API_URL` in Vercel after backend is deployed

---

## 🎉 Done!

Your project is now:
- ✅ On GitHub (version controlled)
- ✅ Frontend on Vercel (live URL)

**Share your Vercel URL:** `https://your-repo-name.vercel.app`

---

## 🔗 Useful Links

- **GitHub**: https://github.com/YOUR_USERNAME/YOUR_REPO
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Full Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)

