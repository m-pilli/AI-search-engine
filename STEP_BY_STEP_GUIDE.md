# 🚀 Step-by-Step Execution Guide for Windows

## Prerequisites Check

Before we start, let's check what you have:
- ✅ Windows 10/11
- ✅ Python 3.13 installed
- ✅ Project files in `C:\Users\Mahathi\Desktop\Search`

## Method 1: Docker Desktop (RECOMMENDED - Easiest)

### Step 1: Install Docker Desktop

1. **Download Docker Desktop**
   - Go to: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Wait for download to complete (~500MB)

2. **Install Docker Desktop**
   - Run the installer (Docker Desktop Installer.exe)
   - Follow the installation wizard
   - Accept the terms and conditions
   - Click "Install"
   - **IMPORTANT**: Restart your computer when prompted

3. **Verify Docker Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

### Step 2: Start Docker Desktop

1. Open Docker Desktop from Start Menu
2. Wait for Docker to start (you'll see a whale icon in system tray)
3. Docker is ready when the icon stops animating

### Step 3: Navigate to Project Directory

```powershell
cd C:\Users\Mahathi\Desktop\Search
```

### Step 4: Start the Application

```powershell
# Start all services
docker-compose up --build
```

This will:
- ✅ Build the backend container
- ✅ Build the frontend container
- ✅ Start MongoDB database
- ✅ Start Redis cache
- ✅ Start Nginx proxy

**Wait 2-3 minutes** for everything to start.

### Step 5: Load Sample Data

Open a NEW terminal window and run:

```powershell
cd C:\Users\Mahathi\Desktop\Search
docker-compose exec backend python load_sample_data.py
```

### Step 6: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api/health

### Step 7: Test the Search

1. Open http://localhost:3000
2. Type a search query: "machine learning"
3. Click Search
4. View results!

---

## Method 2: Local Python Setup (Alternative)

If you can't install Docker, follow these steps:

### Step 1: Install MongoDB

1. Download MongoDB Community Server:
   - Go to: https://www.mongodb.com/try/download/community
   - Select Windows, MSI package
   - Download and install

2. Start MongoDB:
   ```powershell
   # MongoDB should start automatically as a service
   # Or manually start it:
   "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="C:\data\db"
   ```

### Step 2: Install Python Dependencies

```powershell
cd C:\Users\Mahathi\Desktop\Search\backend

# Upgrade pip first
python -m pip install --upgrade pip

# Install packages one by one
pip install Flask==2.3.3
pip install pymongo==4.5.0
pip install python-dotenv==1.0.0
pip install flask-cors==4.0.0

# For the ML packages, we need pre-built wheels
pip install --only-binary :all: numpy
pip install --only-binary :all: scikit-learn
pip install --only-binary :all: sentence-transformers
```

### Step 3: Start the Backend

```powershell
cd C:\Users\Mahathi\Desktop\Search\backend
python app.py
```

Keep this terminal open!

### Step 4: Start the Frontend

Open a NEW terminal:

```powershell
cd C:\Users\Mahathi\Desktop\Search\frontend

# Install Node.js first if you don't have it
# Download from: https://nodejs.org/

# Install dependencies
npm install

# Start the frontend
npm start
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000/api/health

---

## Quick Test Commands

### Test Backend API
```powershell
# Test health check
curl http://localhost:5000/api/health

# Test search (after loading data)
curl "http://localhost:5000/api/search?q=machine%20learning"
```

### Check Docker Status
```powershell
# See running containers
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Stop everything
docker-compose down
```

---

## Troubleshooting

### Issue: "Docker is not running"
**Solution**: 
1. Open Docker Desktop from Start Menu
2. Wait for it to fully start
3. Look for whale icon in system tray

### Issue: "Port already in use"
**Solution**:
```powershell
# Find what's using the port
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue: "Cannot connect to MongoDB"
**Solution**:
```powershell
# Check if MongoDB is running
docker-compose ps

# Restart MongoDB
docker-compose restart mongodb
```

### Issue: Python packages won't install
**Solution**:
1. Install Visual Studio Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. OR use Docker method instead (recommended)

---

## What to Expect

### When Everything Works:

1. **Docker Compose Output**: You'll see logs from all services
2. **Frontend**: Beautiful search interface at http://localhost:3000
3. **Backend**: API responding at http://localhost:5000
4. **Search**: Type queries and get instant results with scores

### First Search:
- Query: "machine learning"
- Results: 5-10 relevant documents
- Response time: <200ms
- Scores: Semantic, Keyword, and Hybrid scores displayed

---

## Next Steps After Setup

1. **Explore the UI**
   - Try different search queries
   - Adjust the alpha parameter (semantic vs keyword)
   - Change search type (hybrid, semantic, keyword)

2. **Add Your Own Documents**
   - Use the API to add documents
   - Or modify `load_sample_data.py` with your data

3. **Check Performance**
   - View statistics at http://localhost:3000/stats
   - Monitor response times
   - Check search quality

4. **Customize**
   - Modify the frontend styling
   - Adjust search parameters
   - Add more features

---

## Getting Help

If you encounter issues:

1. **Check logs**:
   ```powershell
   docker-compose logs -f
   ```

2. **Verify services are running**:
   ```powershell
   docker-compose ps
   ```

3. **Restart everything**:
   ```powershell
   docker-compose down
   docker-compose up --build
   ```

4. **Check the documentation**:
   - `README.md` - Project overview
   - `docs/api.md` - API documentation
   - `docs/architecture.md` - System architecture

---

## Success Checklist

- [ ] Docker Desktop installed and running
- [ ] Project directory: `C:\Users\Mahathi\Desktop\Search`
- [ ] `docker-compose up` running successfully
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend API responding at http://localhost:5000/api/health
- [ ] Sample data loaded
- [ ] Search working with results

Once all checkboxes are complete, you're ready to use and showcase your AI Search Engine! 🎉

