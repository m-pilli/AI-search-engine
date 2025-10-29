#!/usr/bin/env python3
"""
Sample Data Loading Script for AI Search Engine

This script loads sample data into the search engine for testing and demonstration purposes.
"""

import os
import sys
import logging
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import Database
from app.services.semantic_search import SemanticSearchService
from app.services.keyword_search import KeywordSearchService
from app.services.hybrid_search import HybridSearchService
from app.utils.sample_data_loader import SampleDataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_sample_data():
    """Load sample data into the search engine."""
    try:
        # Initialize services
        logger.info("Initializing services...")
        
        # Database
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/search_engine')
        database = Database(mongodb_uri)
        
        # Search services
        semantic_service = SemanticSearchService()
        keyword_service = KeywordSearchService()
        hybrid_service = HybridSearchService(semantic_service, keyword_service)
        
        # Sample data loader
        data_loader = SampleDataLoader()
        
        logger.info("Services initialized successfully")
        
        # Generate sample data
        logger.info("Generating sample data...")
        sample_documents = data_loader.generate_sample_dataset(size=50)
        
        if not sample_documents:
            logger.error("No sample documents generated")
            return False
        
        logger.info(f"Generated {len(sample_documents)} sample documents")
        
        # Clear existing data (optional)
        clear_existing = input("Clear existing documents? (y/N): ").lower().strip()
        if clear_existing == 'y':
            logger.info("Clearing existing documents...")
            # Note: In production, you'd want to be more careful about this
            all_docs = database.get_all_documents()
            for doc in all_docs:
                database.delete_document(doc['_id'])
            logger.info("Existing documents cleared")
        
        # Load documents into database
        logger.info("Loading documents into database...")
        loaded_docs = []
        
        for i, doc in enumerate(sample_documents):
            try:
                # Add to database
                doc_id = database.add_document(
                    title=doc['title'],
                    content=doc['content'],
                    metadata=doc.get('metadata', {})
                )
                
                loaded_docs.append((doc_id, doc['content']))
                
                if (i + 1) % 10 == 0:
                    logger.info(f"Loaded {i + 1}/{len(sample_documents)} documents")
                    
            except Exception as e:
                logger.error(f"Error loading document {i}: {e}")
                continue
        
        logger.info(f"Successfully loaded {len(loaded_docs)} documents into database")
        
        # Build search indices
        logger.info("Building search indices...")
        
        # Semantic search index
        logger.info("Building semantic search index...")
        semantic_service.rebuild_index(loaded_docs)
        logger.info("Semantic search index built")
        
        # Keyword search index
        logger.info("Building keyword search index...")
        keyword_service.rebuild_index(loaded_docs)
        logger.info("Keyword search index built")
        
        # Test search functionality
        logger.info("Testing search functionality...")
        
        test_queries = [
            "machine learning algorithms",
            "web development with React",
            "database design principles",
            "cloud computing architecture",
            "python programming best practices"
        ]
        
        for query in test_queries:
            try:
                results = hybrid_service.search(query, k=3)
                logger.info(f"Query '{query}' returned {len(results['results'])} results")
            except Exception as e:
                logger.error(f"Error testing query '{query}': {e}")
        
        logger.info("Sample data loading completed successfully!")
        
        # Show statistics
        stats = hybrid_service.get_stats()
        logger.info("Search Engine Statistics:")
        logger.info(f"  Total documents: {stats['semantic_search']['total_documents']}")
        logger.info(f"  Model: {stats['semantic_search']['model_name']}")
        logger.info(f"  Embedding dimension: {stats['semantic_search']['embedding_dimension']}")
        logger.info(f"  Vocabulary size: {stats['keyword_search']['vocabulary_size']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading sample data: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("AI Search Engine - Sample Data Loader")
    print("=" * 60)
    print()
    
    # Check if MongoDB is available
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/search_engine')
        test_db = Database(mongodb_uri)
        test_db.get_all_documents(limit=1)
        logger.info("MongoDB connection successful")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        print("Please ensure MongoDB is running and accessible.")
        return 1
    
    # Load sample data
    success = load_sample_data()
    
    if success:
        print("\n" + "=" * 60)
        print("Sample data loading completed successfully!")
        print("You can now test the search engine at:")
        print("  Frontend: http://localhost:3000")
        print("  Backend API: http://localhost:5000/api")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("Sample data loading failed!")
        print("Please check the logs for error details.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

