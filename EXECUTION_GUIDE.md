# 🚀 AI Search Engine - Execution Guide

## Prerequisites

Before running the project, ensure you have:

- **Docker & Docker Compose** (Recommended)
- **Python 3.9+** (for local development)
- **Node.js 16+** (for local development)
- **MongoDB** (for local development)

## Quick Start (Docker - Recommended)

### 1. Clone and Setup
```bash
# Navigate to project directory
cd C:\Users\Mahathi\Desktop\Search

# Copy environment configuration
copy env.prod.example .env
# Edit .env with your settings (optional for local development)
```

### 2. Deploy with Docker Compose
```bash
# Make deployment script executable (if on Linux/Mac)
chmod +x deploy.sh

# Deploy the application
./deploy.sh compose
# OR manually:
docker-compose up --build
```

### 3. Load Sample Data
```bash
# Load sample documents for testing
docker-compose exec backend python load_sample_data.py
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

## Local Development Setup

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set MONGODB_URI=mongodb://localhost:27017/search_engine
set FLASK_ENV=development

# Run the application
python app.py
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables
set REACT_APP_API_URL=http://localhost:5000/api

# Run the development server
npm start
```

### 3. Database Setup
```bash
# Start MongoDB (if not using Docker)
mongod

# Load sample data
cd backend
python load_sample_data.py
```

## Testing the Application

### 1. Basic Search Test
```bash
# Test search API
curl "http://localhost:5000/api/search?q=machine%20learning&limit=5"

# Test health check
curl "http://localhost:5000/api/health"
```

### 2. Frontend Testing
1. Open http://localhost:3000
2. Enter a search query (e.g., "machine learning")
3. Adjust search parameters (alpha, limit, search type)
4. View results with relevance scores

### 3. Performance Testing
```bash
# Load test with Apache Bench
ab -n 100 -c 10 "http://localhost:5000/api/search?q=test"

# Test different search types
curl "http://localhost:5000/api/search?q=AI&type=semantic"
curl "http://localhost:5000/api/search?q=AI&type=keyword"
curl "http://localhost:5000/api/search?q=AI&type=hybrid&alpha=0.8"
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   ```bash
   # Check if MongoDB is running
   docker-compose ps
   # OR for local MongoDB
   mongosh
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using the port
   netstat -ano | findstr :5000
   # Kill the process or change ports in docker-compose.yml
   ```

3. **Frontend Can't Connect to Backend**
   ```bash
   # Check backend is running
   curl http://localhost:5000/api/health
   # Update REACT_APP_API_URL in frontend/.env
   ```

4. **Out of Memory Errors**
   ```bash
   # Increase Docker memory limits
   # OR reduce batch sizes in load_sample_data.py
   ```

### Logs and Debugging
```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# View specific service logs
docker-compose logs backend
docker-compose logs mongodb
docker-compose logs redis
```

## Production Deployment

### 1. Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment status
kubectl get pods -n ai-search-engine
kubectl get services -n ai-search-engine
```

### 2. Production Docker Compose
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

## Monitoring and Maintenance

### 1. Health Checks
```bash
# Check all services
curl http://localhost:5000/api/health/detailed

# Check search statistics
curl http://localhost:5000/api/search/stats
```

### 2. Performance Monitoring
```bash
# View system metrics
docker stats

# Check cache performance
docker-compose exec redis redis-cli info stats
```

### 3. Maintenance Tasks
```bash
# Rebuild search index
curl -X POST http://localhost:5000/api/documents/rebuild-index

# Clear cache
docker-compose exec redis redis-cli flushdb
```

## Next Steps

1. **Customize Search**: Modify alpha values and search parameters
2. **Add Documents**: Use the API to add your own documents
3. **Scale Up**: Deploy to cloud with Kubernetes
4. **Monitor**: Set up monitoring and alerting
5. **Optimize**: Tune performance based on your use case

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Test individual components: `curl http://localhost:5000/api/health`
4. Review the documentation in the `docs/` folder

