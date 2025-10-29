# AI Search Engine - API Documentation

## Overview

The AI Search Engine provides a RESTful API for semantic and keyword-based document search. The API supports hybrid ranking that combines AI-powered semantic understanding with traditional keyword matching.

## Base URL

- **Development**: `http://localhost:5000/api`
- **Production**: `https://your-domain.com/api`

## Authentication

Currently, the API does not require authentication. In production, consider implementing API keys or OAuth2.

## Response Format

All API responses are in JSON format with the following structure:

```json
{
  "data": {...},
  "message": "Success message",
  "timestamp": "2023-10-28T21:00:00Z"
}
```

Error responses:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2023-10-28T21:00:00Z"
}
```

## Endpoints

### Search

#### Search Documents
Search for documents using hybrid semantic and keyword search.

**Endpoint**: `GET /search`

**Parameters**:
- `q` (string, required): Search query
- `limit` (integer, optional): Number of results (default: 10, max: 100)
- `alpha` (float, optional): Semantic vs keyword weight (default: 0.7, range: 0.0-1.0)
- `type` (string, optional): Search type - `hybrid`, `semantic`, or `keyword` (default: `hybrid`)

**Example Request**:
```bash
curl "http://localhost:5000/api/search?q=machine%20learning&limit=5&alpha=0.8&type=hybrid"
```

**Example Response**:
```json
{
  "results": [
    {
      "id": "doc_123",
      "title": "Introduction to Machine Learning",
      "content": "Machine learning is a subset of artificial intelligence...",
      "metadata": {
        "category": "AI/ML",
        "tags": ["machine learning", "AI", "algorithms"]
      },
      "score": 0.95,
      "semantic_score": 0.92,
      "keyword_score": 0.88,
      "created_at": "2023-10-28T20:00:00Z",
      "updated_at": "2023-10-28T20:00:00Z"
    }
  ],
  "query": "machine learning",
  "total_results": 1,
  "response_time_ms": 150,
  "alpha": 0.8,
  "search_stats": {
    "semantic_results_count": 5,
    "keyword_results_count": 3,
    "unique_documents": 4
  }
}
```

#### Search Suggestions
Get search suggestions based on partial query.

**Endpoint**: `GET /search/suggestions`

**Parameters**:
- `q` (string, required): Partial query (minimum 2 characters)
- `limit` (integer, optional): Number of suggestions (default: 5, max: 20)

**Example Request**:
```bash
curl "http://localhost:5000/api/search/suggestions?q=mach&limit=5"
```

**Example Response**:
```json
{
  "suggestions": [
    "machine learning",
    "machine learning algorithms",
    "machine learning python",
    "machine learning tutorial",
    "machine learning vs deep learning"
  ]
}
```

#### Search Statistics
Get search engine statistics and performance metrics.

**Endpoint**: `GET /search/stats`

**Example Request**:
```bash
curl "http://localhost:5000/api/search/stats"
```

**Example Response**:
```json
{
  "semantic_search": {
    "total_documents": 1000,
    "model_name": "all-MiniLM-L6-v2",
    "embedding_dimension": 384,
    "index_type": "FAISS_IndexFlatIP"
  },
  "keyword_search": {
    "total_documents": 1000,
    "vocabulary_size": 50000,
    "max_features": 10000,
    "ngram_range": [1, 2]
  },
  "database": {
    "total_documents": 1000,
    "total_content_length": 5000000
  },
  "default_alpha": 0.7
}
```

### Documents

#### List Documents
Get a paginated list of all documents.

**Endpoint**: `GET /documents`

**Parameters**:
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Documents per page (default: 20, max: 100)

**Example Request**:
```bash
curl "http://localhost:5000/api/documents?page=1&per_page=10"
```

**Example Response**:
```json
{
  "documents": [
    {
      "_id": "doc_123",
      "title": "Document Title",
      "content": "Document content...",
      "metadata": {...},
      "created_at": "2023-10-28T20:00:00Z",
      "updated_at": "2023-10-28T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 1000,
    "pages": 100
  }
}
```

#### Get Document
Get a specific document by ID.

**Endpoint**: `GET /documents/{id}`

**Example Request**:
```bash
curl "http://localhost:5000/api/documents/doc_123"
```

**Example Response**:
```json
{
  "_id": "doc_123",
  "title": "Document Title",
  "content": "Full document content...",
  "metadata": {
    "category": "Technology",
    "tags": ["AI", "Machine Learning"]
  },
  "created_at": "2023-10-28T20:00:00Z",
  "updated_at": "2023-10-28T20:00:00Z"
}
```

#### Add Document
Add a new document to the search index.

**Endpoint**: `POST /documents`

**Request Body**:
```json
{
  "title": "Document Title",
  "content": "Document content...",
  "metadata": {
    "category": "Technology",
    "tags": ["AI", "Machine Learning"]
  }
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:5000/api/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Document",
    "content": "This is the content of the new document.",
    "metadata": {
      "category": "Technology",
      "tags": ["AI", "Machine Learning"]
    }
  }'
```

**Example Response**:
```json
{
  "id": "doc_456",
  "title": "New Document",
  "content": "This is the content of the new document.",
  "metadata": {
    "category": "Technology",
    "tags": ["AI", "Machine Learning"]
  },
  "message": "Document added successfully"
}
```

#### Update Document
Update an existing document.

**Endpoint**: `PUT /documents/{id}`

**Request Body**:
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "metadata": {
    "category": "Updated Category"
  }
}
```

**Example Request**:
```bash
curl -X PUT "http://localhost:5000/api/documents/doc_123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Document Title",
    "content": "Updated document content."
  }'
```

**Example Response**:
```json
{
  "message": "Document updated successfully"
}
```

#### Delete Document
Delete a document from the search index.

**Endpoint**: `DELETE /documents/{id}`

**Example Request**:
```bash
curl -X DELETE "http://localhost:5000/api/documents/doc_123"
```

**Example Response**:
```json
{
  "message": "Document deleted successfully"
}
```

#### Batch Add Documents
Add multiple documents at once.

**Endpoint**: `POST /documents/batch`

**Request Body**:
```json
{
  "documents": [
    {
      "title": "Document 1",
      "content": "Content 1...",
      "metadata": {...}
    },
    {
      "title": "Document 2",
      "content": "Content 2...",
      "metadata": {...}
    }
  ]
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:5000/api/documents/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "title": "Batch Document 1",
        "content": "Content of first document.",
        "metadata": {"category": "Tech"}
      },
      {
        "title": "Batch Document 2",
        "content": "Content of second document.",
        "metadata": {"category": "Science"}
      }
    ]
  }'
```

**Example Response**:
```json
{
  "added_documents": [
    {
      "id": "doc_789",
      "title": "Batch Document 1",
      "content": "Content of first document.",
      "metadata": {"category": "Tech"}
    },
    {
      "id": "doc_790",
      "title": "Batch Document 2",
      "content": "Content of second document.",
      "metadata": {"category": "Science"}
    }
  ],
  "total_added": 2,
  "errors": []
}
```

#### Rebuild Search Index
Rebuild the entire search index from all documents.

**Endpoint**: `POST /documents/rebuild-index`

**Example Request**:
```bash
curl -X POST "http://localhost:5000/api/documents/rebuild-index"
```

**Example Response**:
```json
{
  "message": "Search index rebuilt successfully",
  "total_documents": 1000
}
```

### Health

#### Health Check
Basic health check endpoint.

**Endpoint**: `GET /health`

**Example Request**:
```bash
curl "http://localhost:5000/api/health"
```

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": 1698523200,
  "service": "AI Search Engine",
  "version": "1.0.0"
}
```

#### Detailed Health Check
Detailed health check with service status.

**Endpoint**: `GET /health/detailed`

**Example Request**:
```bash
curl "http://localhost:5000/api/health/detailed"
```

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": 1698523200,
  "service": "AI Search Engine",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "type": "MongoDB",
      "connected": true
    },
    "redis": {
      "status": "healthy",
      "type": "Redis",
      "connected": true
    }
  }
}
```

#### Readiness Check
Kubernetes readiness check.

**Endpoint**: `GET /health/ready`

**Example Request**:
```bash
curl "http://localhost:5000/api/health/ready"
```

**Example Response**:
```json
{
  "status": "ready",
  "timestamp": 1698523200
}
```

#### Liveness Check
Kubernetes liveness check.

**Endpoint**: `GET /health/live`

**Example Request**:
```bash
curl "http://localhost:5000/api/health/live"
```

**Example Response**:
```json
{
  "status": "alive",
  "timestamp": 1698523200
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service temporarily unavailable |

## Rate Limiting

- **Search API**: 10 requests per second per IP
- **General API**: 50 requests per second per IP
- **Batch Operations**: 5 requests per minute per IP

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Request limit per time window
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Time when the rate limit resets

## Search Configuration

### Alpha Parameter
The `alpha` parameter controls the balance between semantic and keyword search:

- `alpha = 0.0`: Pure keyword search
- `alpha = 0.5`: Balanced hybrid search
- `alpha = 1.0`: Pure semantic search
- `alpha = 0.7`: Default (semantic-leaning hybrid)

### Search Types
- **hybrid**: Combines semantic and keyword search (recommended)
- **semantic**: AI-powered meaning-based search
- **keyword**: Traditional text matching search

## Performance Considerations

- **Response Time**: Target <200ms for search queries
- **Throughput**: Supports 1000+ queries per second
- **Caching**: Results are cached for 30 minutes
- **Indexing**: Embeddings are cached for 24 hours

## Examples

### Python Client Example
```python
import requests

# Search for documents
response = requests.get(
    "http://localhost:5000/api/search",
    params={
        "q": "machine learning",
        "limit": 5,
        "alpha": 0.8,
        "type": "hybrid"
    }
)

results = response.json()
for result in results["results"]:
    print(f"Title: {result['title']}")
    print(f"Score: {result['score']:.2f}")
    print(f"Content: {result['content'][:100]}...")
    print()
```

### JavaScript Client Example
```javascript
// Search for documents
const searchDocuments = async (query) => {
  const response = await fetch(
    `http://localhost:5000/api/search?q=${encodeURIComponent(query)}&limit=5&alpha=0.8`
  );
  const data = await response.json();
  return data.results;
};

// Usage
searchDocuments("machine learning").then(results => {
  results.forEach(result => {
    console.log(`Title: ${result.title}`);
    console.log(`Score: ${result.score.toFixed(2)}`);
  });
});
```

### cURL Examples
```bash
# Basic search
curl "http://localhost:5000/api/search?q=artificial%20intelligence"

# Advanced search with parameters
curl "http://localhost:5000/api/search?q=machine%20learning&limit=10&alpha=0.9&type=semantic"

# Add a document
curl -X POST "http://localhost:5000/api/documents" \
  -H "Content-Type: application/json" \
  -d '{"title": "AI Research", "content": "Latest AI research findings..."}'

# Get document by ID
curl "http://localhost:5000/api/documents/doc_123"

# Get search statistics
curl "http://localhost:5000/api/search/stats"
```

