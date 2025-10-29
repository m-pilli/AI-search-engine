# AI Search Engine - Quick Start Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.9+ (for local development)
- MongoDB (for local development)

### Option 1: Docker Compose (Recommended)

1. **Clone and Setup**
```bash
git clone <repository-url>
cd ai-search-engine
cp env.prod.example .env
# Edit .env with your configuration
```

2. **Deploy**
```bash
chmod +x deploy.sh
./deploy.sh compose
```

3. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Health Check: http://localhost:5000/api/health

### Option 2: Local Development

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

3. **Database Setup**
```bash
# Start MongoDB locally
mongod
```

### Option 3: Kubernetes

1. **Prerequisites**
- Kubernetes cluster
- kubectl configured
- Docker registry access

2. **Deploy**
```bash
./deploy.sh k8s
```

## 📊 Performance Testing

### Load Testing with Apache Bench
```bash
# Test search endpoint
ab -n 1000 -c 10 "http://localhost:5000/api/search?q=machine%20learning"

# Test health endpoint
ab -n 1000 -c 50 "http://localhost:5000/api/health"
```

### Load Testing with Artillery
```bash
npm install -g artillery
artillery quick --count 100 --num 10 http://localhost:5000/api/search?q=test
```

## 🔧 Configuration

### Environment Variables
- `MONGODB_URI`: MongoDB connection string
- `REDIS_URL`: Redis connection string
- `EMBEDDING_MODEL`: Sentence transformer model name
- `CACHE_TTL`: Cache time-to-live in seconds
- `SECRET_KEY`: Flask secret key

### Search Configuration
- `alpha`: Semantic vs keyword weight (0.0-1.0)
- `limit`: Maximum number of results
- `searchType`: hybrid, semantic, or keyword

## 📈 Monitoring

### Health Checks
- Basic: `/api/health`
- Detailed: `/api/health/detailed`
- Readiness: `/api/health/ready`
- Liveness: `/api/health/live`

### Metrics
- Response time: <200ms target
- Throughput: 1000+ QPS
- Memory usage: <2GB per instance
- CPU usage: <80% utilization

## 🛠️ Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MongoDB is running
   - Verify connection string
   - Check network connectivity

2. **High Memory Usage**
   - Reduce embedding cache size
   - Optimize FAISS index
   - Scale horizontally

3. **Slow Search Performance**
   - Check FAISS index status
   - Monitor CPU usage
   - Optimize query parameters

### Logs
```bash
# Docker Compose logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Kubernetes logs
kubectl logs -f deployment/backend -n ai-search-engine
kubectl logs -f deployment/frontend -n ai-search-engine
```

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
./deploy.sh compose
```

### Database Maintenance
```bash
# Rebuild search index
curl -X POST http://localhost:5000/api/documents/rebuild-index

# Check database stats
curl http://localhost:5000/api/search/stats
```

### Scaling
```bash
# Scale backend
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Scale with Kubernetes
kubectl scale deployment backend --replicas=5 -n ai-search-engine
```

## 📚 Additional Resources

- [API Documentation](docs/api.md)
- [Architecture Overview](docs/architecture.md)
- [Performance Tuning](docs/performance.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

