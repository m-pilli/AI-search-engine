#!/usr/bin/env python3
"""
Add focused, detailed documents to demonstrate the AI Search Engine's capabilities
"""

import requests
import json
from datetime import datetime

def add_document(title, content, category, difficulty, tags):
    """Add a document to the search engine"""
    doc = {
        "title": title,
        "content": content,
        "category": category,
        "difficulty": difficulty,
        "tags": tags,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    try:
        response = requests.post("http://localhost:5000/api/documents", json=doc)
        if response.status_code in [200, 201]:
            print(f"✅ Added: {title}")
            return True
        else:
            print(f"❌ Failed to add {title}: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error adding {title}: {e}")
        return False

def main():
    print("Adding focused documents to demonstrate AI Search capabilities...")
    
    documents = [
        {
            "title": "Machine Learning Fundamentals: Complete Guide",
            "content": """
# Machine Learning Fundamentals: Complete Guide

## What is Machine Learning?

Machine Learning (ML) is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every task. Unlike traditional programming where we write explicit instructions, ML algorithms build mathematical models based on training data to make predictions or decisions.

## Types of Machine Learning

### 1. Supervised Learning
Supervised learning uses labeled training data to learn a mapping function from inputs to outputs. The algorithm learns from examples where both input and desired output are provided.

**Common Algorithms:**
- Linear Regression: Predicts continuous values using linear relationships
- Logistic Regression: Classifies data into categories using logistic function
- Decision Trees: Makes decisions through a tree-like model of decisions
- Random Forest: Ensemble method combining multiple decision trees
- Support Vector Machines (SVM): Finds optimal boundary between classes
- Neural Networks: Inspired by biological neural networks, capable of learning complex patterns

**Applications:**
- Email spam detection
- Medical diagnosis
- Stock price prediction
- Image classification
- Sentiment analysis

### 2. Unsupervised Learning
Unsupervised learning finds hidden patterns in data without labeled examples. The algorithm explores data structure without knowing the correct answers.

**Common Algorithms:**
- K-Means Clustering: Groups data into k clusters based on similarity
- Hierarchical Clustering: Creates tree of clusters
- Principal Component Analysis (PCA): Reduces dimensionality while preserving variance
- DBSCAN: Density-based clustering algorithm
- Gaussian Mixture Models: Probabilistic clustering

**Applications:**
- Customer segmentation
- Anomaly detection
- Data compression
- Market basket analysis
- Gene sequencing

### 3. Reinforcement Learning
Reinforcement learning learns through interaction with an environment, receiving rewards or penalties for actions.

**Key Concepts:**
- Agent: The learner or decision maker
- Environment: The world the agent interacts with
- State: Current situation of the environment
- Action: Choice made by the agent
- Reward: Feedback from the environment
- Policy: Strategy used by agent to determine actions

**Applications:**
- Game playing (AlphaGo, Chess engines)
- Autonomous vehicles
- Robotics
- Trading algorithms
- Resource management

## Machine Learning Workflow

### 1. Data Collection and Preparation
- Data Sources: Databases, APIs, web scraping, sensors
- Data Cleaning: Handling missing values, outliers, duplicates
- Data Transformation: Normalization, encoding categorical variables
- Feature Engineering: Creating new features from existing data

### 2. Model Selection and Training
- Algorithm Selection: Based on problem type, data size, interpretability needs
- Hyperparameter Tuning: Optimizing model parameters
- Cross-Validation: Ensuring model generalizes well
- Training Process: Feeding data to algorithm to learn patterns

### 3. Model Evaluation
- Metrics for Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Metrics for Regression: Mean Absolute Error, Mean Squared Error, R-squared
- Validation: Testing on unseen data
- Overfitting Detection: Model performs well on training but poorly on test data

### 4. Model Deployment and Monitoring
- Production Deployment: Making model available for real-world use
- Performance Monitoring: Tracking model performance over time
- Model Updates: Retraining with new data
- A/B Testing: Comparing different model versions

## Advanced Topics

### Deep Learning
Deep learning uses neural networks with multiple layers to learn complex patterns. It has revolutionized fields like computer vision and natural language processing.

**Architectures:**
- Convolutional Neural Networks (CNNs): Excellent for image processing
- Recurrent Neural Networks (RNNs): Good for sequential data
- Long Short-Term Memory (LSTM): Handles long-term dependencies
- Transformer Networks: State-of-the-art for NLP tasks
- Generative Adversarial Networks (GANs): Generate new data samples

### Natural Language Processing (NLP)
NLP enables computers to understand, interpret, and generate human language.

**Techniques:**
- Tokenization: Breaking text into words or subwords
- Part-of-Speech Tagging: Identifying grammatical roles
- Named Entity Recognition: Finding people, places, organizations
- Sentiment Analysis: Determining emotional tone
- Machine Translation: Converting between languages
- Text Summarization: Creating concise summaries
- Question Answering: Answering questions from text

### Computer Vision
Computer vision enables machines to interpret and understand visual information.

**Applications:**
- Image Classification: Categorizing images
- Object Detection: Finding and locating objects
- Facial Recognition: Identifying people
- Medical Imaging: Analyzing X-rays, MRIs
- Autonomous Vehicles: Understanding road scenes
- Augmented Reality: Overlaying digital information

## Machine Learning in Production

### MLOps (Machine Learning Operations)
MLOps is the practice of deploying and maintaining ML models in production environments.

**Key Components:**
- Version Control: Tracking code, data, and model versions
- Continuous Integration: Automated testing and validation
- Continuous Deployment: Automated model deployment
- Monitoring: Tracking model performance and data drift
- Governance: Ensuring compliance and ethical use

### Model Serving
Different approaches to serve ML models in production:

**Batch Processing**: Processing large datasets offline
**Real-time Inference**: Immediate predictions for individual requests
**Edge Computing**: Running models on devices closer to users
**Model Streaming**: Continuous processing of data streams

### Scalability Considerations
- Distributed Training: Training models across multiple machines
- Model Optimization: Reducing model size and inference time
- Caching: Storing frequently accessed predictions
- Load Balancing: Distributing requests across multiple servers

## Ethical Considerations

### Bias and Fairness
- Algorithmic Bias: Models may perpetuate existing biases
- Fairness Metrics: Measuring and ensuring equitable outcomes
- Bias Detection: Identifying and mitigating bias in models
- Diverse Datasets: Ensuring representative training data

### Privacy and Security
- Data Privacy: Protecting sensitive information
- Differential Privacy: Adding noise to preserve privacy
- Federated Learning: Training without sharing raw data
- Adversarial Attacks: Protecting against malicious inputs

### Transparency and Explainability
- Interpretable Models: Using inherently understandable algorithms
- Explainable AI: Techniques to understand model decisions
- Model Documentation: Clear documentation of model behavior
- Audit Trails: Tracking model decisions and changes

## Future Trends

### Emerging Technologies
- Quantum Machine Learning: Using quantum computers for ML
- Neuromorphic Computing: Hardware inspired by brain structure
- Edge AI: Running AI on mobile and IoT devices
- AutoML: Automating the ML pipeline
- Few-shot Learning: Learning from very few examples

### Industry Applications
- Healthcare: Drug discovery, medical imaging, personalized treatment
- Finance: Fraud detection, algorithmic trading, risk assessment
- Transportation: Autonomous vehicles, traffic optimization
- Education: Personalized learning, automated grading
- Entertainment: Recommendation systems, content generation

## Conclusion

Machine Learning is transforming industries and creating new possibilities for solving complex problems. As the field continues to evolve, it's essential to understand both the technical aspects and the broader implications of ML systems. Success in ML requires not just technical skills, but also domain expertise, ethical considerations, and practical experience with real-world deployment challenges.

The future of machine learning lies in making these powerful tools more accessible, interpretable, and beneficial to society while addressing the challenges of bias, privacy, and scalability that come with widespread adoption.
            """,
            "category": "AI/ML",
            "difficulty": "intermediate",
            "tags": ["machine learning", "AI", "algorithms", "deep learning", "NLP", "computer vision", "MLOps"]
        },
        
        {
            "title": "Python Programming: Advanced Concepts and Best Practices",
            "content": """
# Python Programming: Advanced Concepts and Best Practices

## Introduction to Advanced Python

Python has evolved from a simple scripting language to a powerful platform for building enterprise-grade applications. This comprehensive guide covers advanced Python concepts, design patterns, and best practices for creating scalable, maintainable software systems.

## Object-Oriented Programming in Python

### Advanced Class Concepts

#### Metaclasses
Metaclasses are the "classes of classes" that define how classes are created. They provide powerful ways to customize class creation.

#### Descriptors
Descriptors allow you to customize attribute access and provide powerful ways to implement properties, methods, and attribute validation.

### Design Patterns in Python

#### Factory Pattern
The Factory pattern provides an interface for creating objects without specifying their exact class.

#### Observer Pattern
The Observer pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.

## Asynchronous Programming

### Async/Await Fundamentals
Asynchronous programming allows you to write concurrent code that can handle many operations simultaneously.

### Advanced Async Patterns

#### Async Context Managers
#### Async Generators

## Performance Optimization

### Profiling and Benchmarking
### Memory Optimization
### Caching Strategies

## Testing and Quality Assurance

### Advanced Testing Patterns
### Property-Based Testing

## Web Development with Python

### FastAPI Advanced Features
### Dependency Injection
### Background Tasks
### Middleware and CORS

## Data Processing and Analysis

### Advanced Pandas Operations
### Data Cleaning and Preprocessing
### Feature Engineering
### Aggregation and Pivoting

## Conclusion

Advanced Python programming involves mastering not just the language syntax, but also understanding design patterns, performance optimization, testing strategies, and modern development practices. The key to building scalable applications lies in writing clean, maintainable code that follows established patterns and best practices.

As Python continues to evolve, staying updated with new features, libraries, and methodologies is crucial for building robust, efficient, and maintainable software systems. The combination of Python's simplicity and its powerful ecosystem makes it an excellent choice for everything from simple scripts to complex enterprise applications.
            """,
            "category": "Programming",
            "difficulty": "advanced",
            "tags": ["python", "programming", "OOP", "async", "performance", "testing", "web development"]
        },
        
        {
            "title": "AI Search Engine: Architecture and Implementation",
            "content": """
# AI Search Engine: Architecture and Implementation

## Introduction to AI-Powered Search

Modern search engines have evolved far beyond simple keyword matching. AI-powered search engines combine multiple technologies to understand user intent, provide relevant results, and continuously improve through machine learning.

## Core Search Technologies

### 1. Semantic Search (Vector Search)
Semantic search uses AI to understand the meaning and context of queries and documents, not just keywords.

**Key Components:**
- Embedding Models: Convert text to numerical vectors that capture semantic meaning
- Vector Databases: Store and efficiently search through high-dimensional vectors
- Similarity Metrics: Measure semantic similarity between vectors (cosine similarity, dot product)
- Dimensionality Reduction: Reduce vector dimensions while preserving semantic information

**Popular Embedding Models:**
- Sentence-BERT: Optimized for sentence-level embeddings
- Universal Sentence Encoder: Google's multilingual embedding model
- OpenAI Embeddings: GPT-based text embeddings
- Word2Vec: Word-level embeddings
- FastText: Subword-level embeddings

**Vector Database Solutions:**
- FAISS (Facebook AI Similarity Search): High-performance similarity search
- Pinecone: Managed vector database service
- Weaviate: Open-source vector database
- Elasticsearch with vector search: Traditional search with vector capabilities
- Chroma: Open-source embedding database

### 2. Keyword Search (Traditional Search)
Traditional keyword-based search remains important for exact matches and specific terms.

**Algorithms:**
- TF-IDF (Term Frequency-Inverse Document Frequency): Weights terms by frequency and rarity
- BM25 (Best Matching 25): Improved version of TF-IDF with better normalization
- Boolean Search: AND, OR, NOT operations
- Phrase Search: Exact phrase matching
- Fuzzy Search: Handles typos and variations

**Implementation:**
- Inverted Index: Maps terms to documents containing them
- Tokenization: Breaking text into searchable terms
- Stemming/Lemmatization: Reducing words to root forms
- Stop Word Removal: Removing common words that don't add meaning

### 3. Hybrid Search Architecture
Combining semantic and keyword search provides the best of both worlds.

**Hybrid Ranking Formula:**
```
Final Score = α × Semantic Score + (1-α) × Keyword Score
```
Where α is a tunable parameter (0-1) that controls the balance between semantic and keyword search.

**Benefits:**
- Semantic understanding for conceptual queries
- Exact matching for specific terms
- Improved recall and precision
- Better handling of synonyms and related concepts
- Robust performance across different query types

## Advanced Search Features

### 1. Query Understanding and Processing
- Query Classification: Categorizing queries by intent (informational, navigational, transactional)
- Query Expansion: Adding related terms to improve recall
- Query Rewriting: Modifying queries for better results
- Intent Detection: Understanding what the user really wants
- Entity Recognition: Identifying people, places, organizations in queries

### 2. Personalization and Context
- User Profiling: Learning user preferences and behavior
- Contextual Search: Using current context (location, time, device)
- Collaborative Filtering: Using similar users' behavior
- Session-based Search: Maintaining context within search sessions
- Adaptive Learning: Improving results based on user feedback

### 3. Real-time Search and Updates
- Incremental Indexing: Adding new documents without full rebuild
- Real-time Updates: Immediate availability of new content
- Change Detection: Identifying modified or deleted documents
- Event-driven Architecture: Processing updates as they happen
- Stream Processing: Handling continuous data streams

## Performance Optimization

### 1. Caching Strategies
- Query Result Caching: Storing frequent query results
- Embedding Caching: Caching computed embeddings
- CDN Integration: Distributing cached content globally
- Redis/Memcached: In-memory caching for fast access
- Cache Invalidation: Keeping cached data fresh

### 2. Scalability and Distribution
- Horizontal Scaling: Adding more servers to handle load
- Load Balancing: Distributing requests across servers
- Database Sharding: Splitting data across multiple databases
- Microservices Architecture: Breaking search into independent services
- Container Orchestration: Managing containers with Kubernetes

### 3. Search Performance Metrics
- Response Time: Time to return search results
- Throughput: Queries processed per second
- Index Size: Storage requirements for search index
- Memory Usage: RAM requirements for search operations
- CPU Utilization: Processing power needed for search

## Machine Learning Integration

### 1. Learning to Rank (LTR)
Learning to Rank uses machine learning to improve search result ranking.

**Approaches:**
- Pointwise: Learning relevance scores for individual documents
- Pairwise: Learning relative preferences between document pairs
- Listwise: Optimizing entire ranked lists

**Features:**
- Query Features: Query length, type, complexity
- Document Features: Content quality, freshness, authority
- User Features: Past behavior, preferences, demographics
- Interaction Features: Click-through rates, dwell time, bounce rate

### 2. Neural Information Retrieval
Using neural networks to improve search relevance.

**Architectures:**
- Dense Retrieval: Using dense vector representations
- Sparse Retrieval: Combining dense and sparse representations
- Cross-Encoders: Jointly encoding queries and documents
- Bi-Encoders: Separately encoding queries and documents

### 3. Continuous Learning and Improvement
- A/B Testing: Comparing different search algorithms
- Online Learning: Updating models with new data
- Feedback Loops: Using user interactions to improve results
- Performance Monitoring: Tracking search quality metrics
- Automated Retraining: Updating models based on performance

## Implementation Architecture

### 1. Microservices Design
- Search Service: Core search functionality
- Indexing Service: Document processing and indexing
- Embedding Service: Text-to-vector conversion
- Ranking Service: Result ranking and scoring
- Analytics Service: Search analytics and monitoring

### 2. Data Pipeline
- Data Ingestion: Collecting documents from various sources
- Data Processing: Cleaning and normalizing content
- Feature Extraction: Extracting searchable features
- Index Building: Creating searchable indexes
- Quality Assurance: Validating data quality

### 3. API Design
- RESTful APIs: Standard HTTP-based interfaces
- GraphQL: Flexible query language for APIs
- Real-time APIs: WebSocket connections for live updates
- Batch APIs: Processing multiple requests efficiently
- Rate Limiting: Controlling API usage

## Deployment and Operations

### 1. Infrastructure Requirements
- Compute Resources: CPU and memory for search operations
- Storage: Disk space for indexes and data
- Network: Bandwidth for serving search requests
- Monitoring: Observability and alerting systems
- Backup: Data protection and disaster recovery

### 2. DevOps and CI/CD
- Automated Testing: Unit, integration, and performance tests
- Continuous Integration: Automated build and test processes
- Continuous Deployment: Automated deployment to production
- Infrastructure as Code: Managing infrastructure with code
- Monitoring and Alerting: Real-time system monitoring

### 3. Security Considerations
- Authentication: Verifying user identity
- Authorization: Controlling access to search features
- Data Encryption: Protecting data in transit and at rest
- Privacy Protection: Complying with privacy regulations
- Rate Limiting: Preventing abuse and DoS attacks

## Future Trends and Innovations

### 1. Multimodal Search
- Text + Image Search: Searching with both text and images
- Video Search: Finding relevant video content
- Audio Search: Searching within audio content
- Cross-modal Retrieval: Finding content across different modalities

### 2. Conversational Search
- Natural Language Queries: Understanding complex, conversational queries
- Multi-turn Search: Handling follow-up questions
- Context Awareness: Maintaining context across multiple queries
- Voice Search: Speech-to-text and voice-based search

### 3. Edge Computing and Mobile Search
- On-device Search: Running search locally on devices
- Offline Search: Searching without internet connection
- Mobile Optimization: Optimizing for mobile devices
- Low-latency Search: Minimizing search response time

## Conclusion

Building an AI-powered search engine requires combining multiple technologies, from traditional information retrieval to modern machine learning and AI. The key to success lies in understanding user needs, implementing robust architectures, and continuously improving through data-driven insights.

The future of search is moving toward more intelligent, personalized, and multimodal systems that can understand context, intent, and user preferences. As AI technology continues to advance, search engines will become even more sophisticated, providing users with increasingly relevant and useful results.

Successful search engine implementation requires careful consideration of performance, scalability, user experience, and business requirements. By following best practices and staying updated with the latest technologies, developers can build search systems that provide exceptional value to users and organizations.
            """,
            "category": "AI/ML",
            "difficulty": "advanced",
            "tags": ["search engine", "AI", "semantic search", "vector database", "machine learning", "architecture"]
        }
    ]
    
    success_count = 0
    for doc in documents:
        if add_document(**doc):
            success_count += 1
    
    print(f"\n✅ Successfully added {success_count} comprehensive documents!")
    print("These documents contain detailed, technical content that will demonstrate")
    print("the AI Search Engine's ability to find relevant information from complex documents.")

if __name__ == "__main__":
    main()
