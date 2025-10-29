# AI Search Engine - Performance Tuning Guide

## Overview

This guide provides comprehensive performance tuning strategies for the AI Search Engine to achieve optimal performance across different workloads and scale requirements.

## Performance Targets

### Latency Targets
- **Search Response Time**: <200ms (P95), <100ms (P50)
- **Document Addition**: <500ms
- **Index Rebuild**: <30 seconds for 10K documents
- **Health Checks**: <50ms

### Throughput Targets
- **Search Queries**: 1000+ QPS
- **Document Updates**: 100+ QPS
- **Concurrent Users**: 10,000+

### Resource Utilization
- **CPU Usage**: <80% average
- **Memory Usage**: <2GB per instance
- **Disk I/O**: <1000 IOPS
- **Network**: <100Mbps per instance

## Backend Optimization

### 1. Flask Application Tuning

#### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4  # 2 * CPU cores + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120
keepalive = 5
preload_app = True
```

#### Flask Configuration
```python
# Optimize Flask settings
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=False,
    JSON_SORT_KEYS=False,
    SEND_FILE_MAX_AGE_DEFAULT=31536000,  # 1 year
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10MB
)
```

### 2. Database Optimization

#### MongoDB Configuration
```javascript
// mongod.conf
storage:
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2
      journalCompressor: snappy
      directoryForIndexes: true
    collectionConfig:
      blockCompressor: snappy
    indexConfig:
      prefixCompression: true

operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp
```

#### MongoDB Indexes
```javascript
// Create optimized indexes
db.documents.createIndex({ "title": "text", "content": "text" })
db.documents.createIndex({ "metadata.category": 1 })
db.documents.createIndex({ "created_at": -1 })
db.documents.createIndex({ "updated_at": -1 })

// Compound indexes for common queries
db.documents.createIndex({ 
  "metadata.category": 1, 
  "created_at": -1 
})
```

#### Connection Pooling
```python
# Optimize MongoDB connections
from pymongo import MongoClient
from pymongo.pool import Pool

client = MongoClient(
    mongodb_uri,
    maxPoolSize=50,
    minPoolSize=10,
    maxIdleTimeMS=30000,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=20000
)
```

### 3. Redis Cache Optimization

#### Redis Configuration
```conf
# redis.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
tcp-keepalive 300
timeout 0
```

#### Cache Strategy
```python
# Optimize cache TTL values
CACHE_CONFIG = {
    'search_results': 1800,      # 30 minutes
    'embeddings': 86400,         # 24 hours
    'popular_queries': 3600,     # 1 hour
    'search_stats': 300,         # 5 minutes
    'document_metadata': 7200,   # 2 hours
}
```

### 4. FAISS Vector Database Optimization

#### Index Configuration
```python
# Optimize FAISS index
import faiss

# Use more efficient index types
dimension = 384  # all-MiniLM-L6-v2 dimension

# For production with large datasets
index = faiss.IndexIVFFlat(
    faiss.IndexFlatL2(dimension),
    dimension,
    nlist=1000  # Number of clusters
)

# For smaller datasets
index = faiss.IndexFlatIP(dimension)  # Inner product
```

#### Batch Operations
```python
# Process embeddings in batches
def add_embeddings_batch(embeddings, batch_size=1000):
    for i in range(0, len(embeddings), batch_size):
        batch = embeddings[i:i + batch_size]
        index.add(batch)
```

### 5. AI Model Optimization

#### Model Loading
```python
# Cache model in memory
import torch
from sentence_transformers import SentenceTransformer

# Load model once and reuse
model = SentenceTransformer('all-MiniLM-L6-v2')
model.eval()  # Set to evaluation mode

# Use GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
```

#### Batch Processing
```python
# Process multiple texts at once
def encode_batch(texts, batch_size=32):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
    return embeddings
```

## Frontend Optimization

### 1. React Performance

#### Component Optimization
```typescript
// Use React.memo for expensive components
const SearchResults = React.memo(({ results }) => {
  return (
    <div>
      {results.map(result => (
        <DocumentCard key={result.id} document={result} />
      ))}
    </div>
  );
});

// Use useMemo for expensive calculations
const filteredResults = useMemo(() => {
  return results.filter(result => result.score > minScore);
}, [results, minScore]);
```

#### Bundle Optimization
```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
};
```

### 2. API Optimization

#### Request Debouncing
```typescript
// Debounce search requests
const useDebounce = (value: string, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};
```

#### Caching Strategy
```typescript
// Implement client-side caching
const useSearchCache = () => {
  const cache = useRef(new Map());

  const getCachedResult = (query: string) => {
    return cache.current.get(query);
  };

  const setCachedResult = (query: string, result: any) => {
    cache.current.set(query, {
      data: result,
      timestamp: Date.now(),
    });
  };

  return { getCachedResult, setCachedResult };
};
```

## Infrastructure Optimization

### 1. Docker Optimization

#### Multi-stage Build
```dockerfile
# Backend Dockerfile optimization
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim as runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

# Use non-root user
RUN useradd -m -u 1000 appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
```

#### Resource Limits
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### 2. Kubernetes Optimization

#### Resource Management
```yaml
# k8s/backend.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: backend
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 60
          periodSeconds: 30
```

#### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 3. Nginx Optimization

#### Load Balancing
```nginx
# nginx.conf
upstream backend {
    least_conn;
    server backend_1:5000 max_fails=3 fail_timeout=30s;
    server backend_2:5000 max_fails=3 fail_timeout=30s;
    keepalive 64;
}

server {
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Connection pooling
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Monitoring and Profiling

### 1. Application Monitoring

#### Performance Metrics
```python
# Custom metrics collection
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
SEARCH_REQUESTS = Counter('search_requests_total', 'Total search requests')
SEARCH_DURATION = Histogram('search_duration_seconds', 'Search request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')

# Use in application
@SEARCH_DURATION.time()
def search_documents(query):
    SEARCH_REQUESTS.inc()
    # Search logic here
```

#### Profiling
```python
# Use cProfile for performance profiling
import cProfile
import pstats

def profile_search():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your search code here
    search_documents("test query")
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### 2. Database Monitoring

#### MongoDB Profiling
```javascript
// Enable profiling for slow operations
db.setProfilingLevel(2, { slowms: 100 })

// Analyze slow queries
db.system.profile.find().sort({ ts: -1 }).limit(5).pretty()
```

#### Redis Monitoring
```bash
# Monitor Redis performance
redis-cli --latency-history
redis-cli info stats
redis-cli monitor
```

## Load Testing

### 1. Apache Bench Testing
```bash
# Basic load test
ab -n 1000 -c 10 "http://localhost:5000/api/search?q=machine%20learning"

# Advanced load test with headers
ab -n 1000 -c 10 -H "Content-Type: application/json" \
   "http://localhost:5000/api/search?q=machine%20learning&limit=10"
```

### 2. Artillery Testing
```yaml
# artillery.yml
config:
  target: 'http://localhost:5000'
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 50
    - duration: 60
      arrivalRate: 100

scenarios:
  - name: "Search API"
    weight: 100
    flow:
      - get:
          url: "/api/search"
          qs:
            q: "{{ $randomString() }}"
            limit: 10
```

### 3. Custom Load Testing
```python
# Python load testing script
import asyncio
import aiohttp
import time

async def search_request(session, query):
    async with session.get(f'/api/search?q={query}') as response:
        return await response.json()

async def load_test():
    queries = ['machine learning', 'artificial intelligence', 'data science']
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1000):
            query = queries[i % len(queries)]
            tasks.append(search_request(session, query))
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f"Completed 1000 requests in {end_time - start_time:.2f} seconds")

asyncio.run(load_test())
```

## Troubleshooting Performance Issues

### 1. High Response Times

#### Check Points:
- Database query performance
- Cache hit rates
- Network latency
- CPU usage
- Memory usage

#### Solutions:
```python
# Add query timing
import time

def search_with_timing(query):
    start_time = time.time()
    
    # Check cache first
    cached_result = cache.get(f"search:{query}")
    if cached_result:
        return cached_result
    
    # Perform search
    result = perform_search(query)
    
    # Cache result
    cache.set(f"search:{query}", result, ttl=1800)
    
    # Log timing
    duration = time.time() - start_time
    logger.info(f"Search completed in {duration:.3f}s")
    
    return result
```

### 2. High Memory Usage

#### Check Points:
- Memory leaks in application
- Large data structures
- Inefficient caching
- Database connection leaks

#### Solutions:
```python
# Monitor memory usage
import psutil
import gc

def monitor_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    
    if memory_info.rss > 2 * 1024 * 1024 * 1024:  # 2GB
        logger.warning("High memory usage detected")
        gc.collect()  # Force garbage collection
```

### 3. Database Performance Issues

#### Check Points:
- Slow queries
- Missing indexes
- Connection pool exhaustion
- Lock contention

#### Solutions:
```python
# Optimize database queries
def get_documents_optimized(filters):
    # Use projection to limit fields
    projection = {
        'title': 1,
        'content': 1,
        'metadata': 1,
        'created_at': 1
    }
    
    # Use proper indexes
    cursor = db.documents.find(filters, projection)
    cursor.sort([('created_at', -1)])
    cursor.limit(100)
    
    return list(cursor)
```

## Best Practices Summary

### 1. Application Level
- Use connection pooling
- Implement proper caching strategies
- Optimize database queries
- Use batch operations
- Monitor performance metrics

### 2. Infrastructure Level
- Use appropriate resource limits
- Implement horizontal scaling
- Use load balancing
- Monitor system resources
- Implement health checks

### 3. Development Level
- Profile code regularly
- Use efficient algorithms
- Implement proper error handling
- Write performance tests
- Monitor in production

### 4. Operational Level
- Set up monitoring and alerting
- Implement log aggregation
- Use performance dashboards
- Regular performance reviews
- Capacity planning

