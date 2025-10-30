# 🏠 Local Setup Guide - AI Search Engine

## Quick Start (After Cloning from GitHub)

### Step 1: Clone Repository
```powershell
git clone https://github.com/m-pilli/AI-search-engine.git
cd AI-search-engine
```

### Step 2: Start Backend

**Option A: Using Docker (Recommended)**
```powershell
# Start MongoDB, Redis, and Backend
docker-compose up -d

# Check if backend is running
docker ps
```

**Option B: Manual Python Setup**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

### Step 3: Start Frontend
```powershell
# Open new PowerShell window
cd frontend
npm install
npm start
```

### Step 4: Access Your Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

---

## Environment Variables (Optional)

If you need to customize settings, create `backend/.env`:
```
MONGODB_URI=mongodb://localhost:27017/search_engine
REDIS_URL=redis://localhost:6379/0
EMBEDDING_MODEL=all-MiniLM-L6-v2
SECRET_KEY=your-secret-key
PORT=5000
```

---

## Add Sample Data

To populate the database with sample documents:
```powershell
# Make sure backend is running first
cd backend
python add_sample_docs.py

# Or use the batch script
cd ..
.\load-sample-data.bat
```

---

## Troubleshooting

### Backend won't start?
- Check if MongoDB and Redis are running: `docker ps`
- Check ports 5000, 27017, 6379 are available
- View logs: `docker-compose logs backend`

### Frontend shows "Network Error"?
- Make sure backend is running on http://localhost:5000
- Check browser console for CORS errors
- Verify `REACT_APP_API_URL` is not set (defaults to localhost)

### Search returns no results?
- Add sample documents: `python backend/add_sample_docs.py`
- Rebuild search index: POST to http://localhost:5000/api/documents/rebuild-index

---

## Stop Everything

```powershell
# Stop Docker containers
docker-compose down

# Stop frontend (press Ctrl+C in frontend terminal)
```

---

## That's It! ✅

Your AI Search Engine should be running locally:
- ✅ Frontend at http://localhost:3000
- ✅ Backend at http://localhost:5000
- ✅ All services connected and working!

