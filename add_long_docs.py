import requests

API_URL = "http://localhost:5000/api/documents/batch"

# Longer, more realistic documents
long_documents = [
    {
        "title": "Complete Guide to Machine Learning",
        "content": """Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data without being explicitly programmed. 

INTRODUCTION:
Machine learning has revolutionized how we approach problem-solving in computer science. Instead of programming explicit rules, we train algorithms on data to discover patterns and make predictions.

TYPES OF MACHINE LEARNING:

1. Supervised Learning:
In supervised learning, algorithms learn from labeled training data. The algorithm learns to map inputs to outputs based on example input-output pairs. Common algorithms include:
- Linear Regression: For predicting continuous values
- Logistic Regression: For classification problems
- Decision Trees: For both classification and regression
- Random Forests: Ensemble method using multiple decision trees
- Support Vector Machines: For classification with optimal hyperplanes
- Neural Networks: Inspired by biological neural networks

2. Unsupervised Learning:
Unsupervised learning works with unlabeled data to discover hidden patterns. The algorithm tries to learn the underlying structure of the data. Key techniques include:
- Clustering (K-means, DBSCAN, Hierarchical)
- Dimensionality Reduction (PCA, t-SNE, UMAP)
- Anomaly Detection
- Association Rule Learning

3. Reinforcement Learning:
An agent learns to make decisions by interacting with an environment to maximize cumulative reward. Applications include game playing, robotics, and autonomous systems.

APPLICATIONS:
Machine learning powers modern applications across industries:
- Healthcare: Disease diagnosis, drug discovery, personalized medicine
- Finance: Fraud detection, algorithmic trading, credit scoring
- E-commerce: Recommendation systems, demand forecasting, customer segmentation
- Transportation: Autonomous vehicles, route optimization, traffic prediction
- Natural Language Processing: Chatbots, translation, sentiment analysis
- Computer Vision: Image recognition, object detection, facial recognition

FUTURE DIRECTIONS:
The field continues to evolve with new architectures, techniques, and applications being developed constantly. Key areas of research include transfer learning, few-shot learning, explainable AI, and federated learning.""",
        "metadata": {
            "category": "AI/ML",
            "difficulty": "comprehensive",
            "word_count": 2500,
            "tags": ["machine learning", "AI", "comprehensive guide"]
        }
    },
    {
        "title": "Python Programming: From Basics to Advanced",
        "content": """Python is a high-level, interpreted programming language created by Guido van Rossum in 1991. It emphasizes code readability and simplicity, making it an excellent choice for beginners and experts alike.

CHAPTER 1: PYTHON BASICS

Python Philosophy:
Python follows the "Zen of Python" principles:
- Beautiful is better than ugly
- Explicit is better than implicit
- Simple is better than complex
- Readability counts

Basic Syntax:
Python uses indentation to define code blocks, unlike languages that use curly braces. Variables are dynamically typed, meaning you don't need to declare their type explicitly.

Data Types:
- Numbers: int, float, complex
- Strings: Immutable sequences of characters
- Lists: Mutable ordered sequences
- Tuples: Immutable ordered sequences
- Dictionaries: Key-value pairs
- Sets: Unordered collections of unique elements

CHAPTER 2: CONTROL FLOW

Conditional Statements:
Python uses if, elif, and else for conditional logic. The syntax is clean and readable.

Loops:
- For loops: Iterate over sequences
- While loops: Execute while condition is true
- List comprehensions: Concise way to create lists

CHAPTER 3: FUNCTIONS AND MODULES

Functions:
Functions are defined using the def keyword. Python supports:
- Default arguments
- Keyword arguments
- Variable-length arguments (*args, **kwargs)
- Lambda functions for short anonymous functions
- Decorators for modifying function behavior

Modules and Packages:
Python's module system allows code organization and reuse. The standard library is extensive, covering file I/O, system operations, networking, and more.

CHAPTER 4: OBJECT-ORIENTED PROGRAMMING

Classes and Objects:
Python supports OOP with classes, inheritance, encapsulation, and polymorphism. Special methods (dunder methods) allow customization of built-in behavior.

CHAPTER 5: ADVANCED TOPICS

Generators and Iterators:
Efficient memory usage for large datasets using lazy evaluation.

Context Managers:
The 'with' statement for resource management and cleanup.

Asynchronous Programming:
async/await for concurrent programming and I/O operations.

POPULAR FRAMEWORKS:
- Django: Full-featured web framework
- Flask: Lightweight web framework
- FastAPI: Modern API framework
- Pandas: Data analysis and manipulation
- NumPy: Numerical computing
- TensorFlow/PyTorch: Deep learning
- Scikit-learn: Machine learning

BEST PRACTICES:
- Follow PEP 8 style guide
- Write docstrings for documentation
- Use virtual environments
- Write unit tests
- Use version control (Git)
- Handle exceptions properly
- Use type hints for better code clarity

Python's versatility and ease of use have made it the language of choice for data science, web development, automation, and artificial intelligence.""",
        "metadata": {
            "category": "Programming",
            "difficulty": "all-levels",
            "word_count": 3200,
            "tags": ["python", "programming", "tutorial", "comprehensive"]
        }
    }
]

# Add the longer documents
try:
    print("Adding longer sample documents...")
    response = requests.post(API_URL, json={"documents": long_documents}, timeout=30)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Successfully added {result['total_added']} longer documents!")
        for doc in result['added_documents']:
            print(f"  - {doc['title']} ({len(doc['content'])} characters)")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

