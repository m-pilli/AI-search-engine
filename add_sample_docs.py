import requests
import json

# API endpoint
API_URL = "http://localhost:5000/api/documents/batch"

# Sample documents about various tech topics
documents = [
    {
        "title": "Introduction to Machine Learning",
        "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data without being explicitly programmed. It involves training models on datasets to make predictions or decisions. Common types include supervised learning, unsupervised learning, and reinforcement learning. Popular algorithms include linear regression, decision trees, neural networks, and support vector machines. Applications range from image recognition to natural language processing.",
        "metadata": {
            "category": "AI/ML",
            "difficulty": "beginner",
            "tags": ["machine learning", "AI", "algorithms", "data science"]
        }
    },
    {
        "title": "Deep Learning and Neural Networks",
        "content": "Deep learning is a branch of machine learning based on artificial neural networks. It uses multiple layers of neurons to progressively extract higher-level features from raw input. Convolutional Neural Networks (CNNs) are used for image processing, while Recurrent Neural Networks (RNNs) excel at sequence data. Transformers have revolutionized natural language processing. Deep learning powers applications like computer vision, speech recognition, and autonomous vehicles.",
        "metadata": {
            "category": "AI/ML",
            "difficulty": "advanced",
            "tags": ["deep learning", "neural networks", "AI", "CNN", "RNN"]
        }
    },
    {
        "title": "Python Programming for Beginners",
        "content": "Python is a versatile programming language known for its readability and simplicity. It features dynamic typing, extensive standard library, and strong community support. Key features include list comprehensions, decorators, and generators. Popular frameworks include Django for web development, Flask for APIs, and Pandas for data analysis. Python is widely used in data science, web development, automation, and artificial intelligence applications.",
        "metadata": {
            "category": "Programming",
            "difficulty": "beginner",
            "tags": ["python", "programming", "coding", "beginner"]
        }
    },
    {
        "title": "Web Development with React",
        "content": "React is a JavaScript library for building user interfaces, particularly web applications. It uses a component-based architecture and virtual DOM for efficient rendering. React applications are built using JSX, a syntax extension that allows HTML-like code in JavaScript. Key concepts include components, props, state, hooks, and lifecycle methods. React is often used with Redux for state management and React Router for navigation in single-page applications.",
        "metadata": {
            "category": "Web Development",
            "difficulty": "intermediate",
            "tags": ["react", "javascript", "frontend", "web development"]
        }
    },
    {
        "title": "Database Design and SQL",
        "content": "Database design involves creating an efficient and logical structure for storing data. Key principles include normalization to reduce redundancy, proper indexing for performance, and establishing relationships between tables. SQL (Structured Query Language) is used to interact with relational databases. Common operations include SELECT for queries, JOIN for combining tables, and CREATE for defining schema. Popular databases include PostgreSQL, MySQL, and SQLite.",
        "metadata": {
            "category": "Database",
            "difficulty": "intermediate",
            "tags": ["database", "SQL", "design", "data"]
        }
    },
    {
        "title": "Cloud Computing with AWS",
        "content": "Cloud computing provides on-demand access to computing resources over the internet. Amazon Web Services (AWS) offers Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS). Key services include EC2 for compute, S3 for storage, RDS for databases, and Lambda for serverless computing. Benefits include scalability, cost-effectiveness, and global availability. DevOps practices enable continuous integration and deployment.",
        "metadata": {
            "category": "Cloud Computing",
            "difficulty": "intermediate",
            "tags": ["cloud", "AWS", "devops", "infrastructure"]
        }
    },
    {
        "title": "Artificial Intelligence and Ethics",
        "content": "Artificial Intelligence raises important ethical considerations including bias in algorithms, privacy concerns, job displacement, and autonomous decision-making. Responsible AI development requires transparency, fairness, accountability, and respect for human rights. Issues include algorithmic bias in hiring and lending, surveillance concerns, and the impact on employment. Organizations must implement ethical guidelines and diverse teams to ensure AI benefits society equitably.",
        "metadata": {
            "category": "AI Ethics",
            "difficulty": "advanced",
            "tags": ["AI", "ethics", "bias", "responsibility"]
        }
    },
    {
        "title": "Data Science and Analytics",
        "content": "Data science combines statistics, programming, and domain expertise to extract insights from data. The process includes data collection, cleaning, exploratory analysis, modeling, and visualization. Key tools include Python libraries like Pandas, NumPy, and Scikit-learn, along with visualization tools like Matplotlib and Seaborn. Data scientists use statistical methods, machine learning, and domain knowledge to solve business problems and make data-driven decisions.",
        "metadata": {
            "category": "Data Science",
            "difficulty": "intermediate",
            "tags": ["data science", "analytics", "statistics", "python"]
        }
    }
]

# Send batch request
try:
    print("Adding sample documents...")
    response = requests.post(API_URL, json={"documents": documents}, timeout=30)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Successfully added {result['total_added']} documents!")
        print("\nDocuments added:")
        for doc in result['added_documents']:
            print(f"  - {doc['title']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")

