import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)

class SampleDataLoader:
    """Load sample data for testing the search engine."""
    
    def __init__(self):
        self.sample_documents = []
    
    def load_wikipedia_articles(self, topics: List[str], max_articles: int = 50) -> List[Dict[str, Any]]:
        """Load Wikipedia articles as sample documents."""
        documents = []
        
        for topic in topics[:max_articles]:
            try:
                # Get Wikipedia article
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Get full article content
                    content_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{topic.replace(' ', '_')}"
                    content_response = requests.get(content_url, timeout=10)
                    
                    content = ""
                    if content_response.status_code == 200:
                        soup = BeautifulSoup(content_response.text, 'html.parser')
                        # Extract text content
                        for p in soup.find_all('p'):
                            content += p.get_text() + " "
                    
                    document = {
                        'title': data.get('title', topic),
                        'content': content.strip() or data.get('extract', ''),
                        'metadata': {
                            'source': 'wikipedia',
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                            'thumbnail': data.get('thumbnail', {}).get('source', ''),
                            'description': data.get('description', ''),
                            'topic': topic
                        }
                    }
                    
                    documents.append(document)
                    logger.info(f"Loaded Wikipedia article: {topic}")
                    
                time.sleep(1)  # Be respectful to Wikipedia API
                
            except Exception as e:
                logger.error(f"Error loading Wikipedia article for {topic}: {e}")
                continue
        
        return documents
    
    def load_tech_articles(self) -> List[Dict[str, Any]]:
        """Load sample technology articles."""
        tech_articles = [
            {
                'title': 'Introduction to Machine Learning',
                'content': '''
                Machine learning is a subset of artificial intelligence that focuses on algorithms 
                that can learn from data without being explicitly programmed. It involves training 
                models on datasets to make predictions or decisions. Common types include supervised 
                learning, unsupervised learning, and reinforcement learning. Popular algorithms 
                include linear regression, decision trees, neural networks, and support vector machines.
                Applications range from image recognition to natural language processing.
                ''',
                'metadata': {
                    'category': 'AI/ML',
                    'difficulty': 'beginner',
                    'tags': ['machine learning', 'AI', 'algorithms', 'data science']
                }
            },
            {
                'title': 'Web Development with React',
                'content': '''
                React is a JavaScript library for building user interfaces, particularly web applications. 
                It uses a component-based architecture and virtual DOM for efficient rendering. React 
                applications are built using JSX, a syntax extension that allows HTML-like code in 
                JavaScript. Key concepts include components, props, state, hooks, and lifecycle methods. 
                React is often used with other libraries like Redux for state management and React Router 
                for navigation.
                ''',
                'metadata': {
                    'category': 'Web Development',
                    'difficulty': 'intermediate',
                    'tags': ['react', 'javascript', 'frontend', 'web development']
                }
            },
            {
                'title': 'Database Design Principles',
                'content': '''
                Database design involves creating an efficient and logical structure for storing data. 
                Key principles include normalization to reduce redundancy, proper indexing for performance, 
                and establishing relationships between tables. Common database types include relational 
                databases like MySQL and PostgreSQL, NoSQL databases like MongoDB, and graph databases 
                like Neo4j. Design considerations include scalability, consistency, and query performance.
                ''',
                'metadata': {
                    'category': 'Database',
                    'difficulty': 'intermediate',
                    'tags': ['database', 'SQL', 'design', 'normalization']
                }
            },
            {
                'title': 'Cloud Computing Architecture',
                'content': '''
                Cloud computing provides on-demand access to computing resources over the internet. 
                It includes Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and 
                Software as a Service (SaaS). Major cloud providers include AWS, Google Cloud, and 
                Microsoft Azure. Benefits include scalability, cost-effectiveness, and flexibility. 
                Key concepts include virtualization, containerization, microservices, and serverless 
                computing.
                ''',
                'metadata': {
                    'category': 'Cloud Computing',
                    'difficulty': 'intermediate',
                    'tags': ['cloud', 'AWS', 'Azure', 'microservices', 'serverless']
                }
            },
            {
                'title': 'Python Programming Best Practices',
                'content': '''
                Python is a versatile programming language known for its readability and simplicity. 
                Best practices include following PEP 8 style guidelines, using virtual environments, 
                writing comprehensive tests, and documenting code properly. Key features include dynamic 
                typing, extensive standard library, and strong community support. Popular frameworks 
                include Django for web development, Flask for APIs, and Pandas for data analysis.
                ''',
                'metadata': {
                    'category': 'Programming',
                    'difficulty': 'beginner',
                    'tags': ['python', 'programming', 'best practices', 'frameworks']
                }
            }
        ]
        
        return tech_articles
    
    def load_academic_papers(self) -> List[Dict[str, Any]]:
        """Load sample academic paper abstracts."""
        papers = [
            {
                'title': 'Attention Is All You Need',
                'content': '''
                The dominant sequence transduction models are based on complex recurrent or convolutional 
                neural networks that include an encoder and a decoder. The best performing models also 
                connect the encoder and decoder through an attention mechanism. We propose a new simple 
                network architecture, the Transformer, based solely on attention mechanisms, dispensing 
                with recurrence and convolutions entirely. Experiments on two machine translation tasks 
                show these models to be superior in quality while being more parallelizable and requiring 
                significantly less time to train.
                ''',
                'metadata': {
                    'authors': ['Vaswani et al.'],
                    'year': 2017,
                    'venue': 'NIPS',
                    'category': 'NLP',
                    'tags': ['transformer', 'attention', 'machine translation', 'neural networks']
                }
            },
            {
                'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
                'content': '''
                We introduce a new language representation model called BERT, which stands for 
                Bidirectional Encoder Representations from Transformers. Unlike recent language 
                representation models, BERT is designed to pre-train deep bidirectional representations 
                from unlabeled text by jointly conditioning on both left and right context in all layers. 
                As a result, the pre-trained BERT model can be fine-tuned with just one additional output 
                layer to create state-of-the-art models for a wide range of tasks.
                ''',
                'metadata': {
                    'authors': ['Devlin et al.'],
                    'year': 2018,
                    'venue': 'NAACL',
                    'category': 'NLP',
                    'tags': ['BERT', 'transformer', 'pre-training', 'language model']
                }
            }
        ]
        
        return papers
    
    def load_ecommerce_products(self) -> List[Dict[str, Any]]:
        """Load sample e-commerce product descriptions."""
        products = [
            {
                'title': 'Wireless Bluetooth Headphones',
                'content': '''
                High-quality wireless Bluetooth headphones with noise cancellation technology. 
                Features include 30-hour battery life, quick charge capability, premium sound 
                quality, and comfortable over-ear design. Compatible with all Bluetooth devices. 
                Perfect for music lovers, gamers, and professionals who need reliable audio 
                equipment. Includes carrying case and charging cable.
                ''',
                'metadata': {
                    'category': 'Electronics',
                    'price': 199.99,
                    'brand': 'AudioTech',
                    'rating': 4.5,
                    'tags': ['headphones', 'bluetooth', 'wireless', 'audio']
                }
            },
            {
                'title': 'Smart Fitness Tracker Watch',
                'content': '''
                Advanced fitness tracker with heart rate monitoring, GPS tracking, and sleep analysis. 
                Water-resistant design suitable for swimming and outdoor activities. Tracks steps, 
                calories burned, and workout intensity. Features include smartphone notifications, 
                music control, and customizable watch faces. Battery lasts up to 7 days with 
                normal use.
                ''',
                'metadata': {
                    'category': 'Wearables',
                    'price': 149.99,
                    'brand': 'FitTech',
                    'rating': 4.3,
                    'tags': ['fitness', 'watch', 'tracker', 'health']
                }
            }
        ]
        
        return products
    
    def generate_sample_dataset(self, size: int = 100) -> List[Dict[str, Any]]:
        """Generate a comprehensive sample dataset."""
        logger.info(f"Generating sample dataset with {size} documents...")
        
        all_documents = []
        
        # Load different types of documents
        all_documents.extend(self.load_tech_articles())
        all_documents.extend(self.load_academic_papers())
        all_documents.extend(self.load_ecommerce_products())
        
        # Add Wikipedia articles if more documents are needed
        if len(all_documents) < size:
            tech_topics = [
                'Artificial Intelligence', 'Machine Learning', 'Deep Learning',
                'Natural Language Processing', 'Computer Vision', 'Robotics',
                'Web Development', 'Mobile Development', 'Cloud Computing',
                'Cybersecurity', 'Data Science', 'Blockchain',
                'Python Programming', 'JavaScript', 'React Framework',
                'Database Management', 'DevOps', 'Microservices'
            ]
            
            wiki_docs = self.load_wikipedia_articles(tech_topics, size - len(all_documents))
            all_documents.extend(wiki_docs)
        
        # Add timestamps
        for i, doc in enumerate(all_documents):
            doc['created_at'] = datetime.utcnow().isoformat()
            doc['updated_at'] = datetime.utcnow().isoformat()
            doc['id'] = f"sample_doc_{i+1}"
        
        logger.info(f"Generated {len(all_documents)} sample documents")
        return all_documents[:size]
    
    def save_sample_dataset(self, documents: List[Dict[str, Any]], filename: str = "sample_dataset.json"):
        """Save sample dataset to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)
            logger.info(f"Sample dataset saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving sample dataset: {e}")
    
    def load_sample_dataset(self, filename: str = "sample_dataset.json") -> List[Dict[str, Any]]:
        """Load sample dataset from JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            logger.info(f"Loaded {len(documents)} documents from {filename}")
            return documents
        except Exception as e:
            logger.error(f"Error loading sample dataset: {e}")
            return []

