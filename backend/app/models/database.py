from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database connection and operations."""
    
    def __init__(self, mongodb_uri):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client.search_engine
        self.documents = self.db.documents
        self.embeddings = self.db.embeddings
        
    def add_document(self, title, content, metadata=None):
        """Add a new document to the database."""
        try:
            doc = {
                'title': title,
                'content': content,
                'metadata': metadata or {},
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = self.documents.insert_one(doc)
            logger.info(f"Added document with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise
    
    def get_document(self, doc_id):
        """Get a document by ID."""
        try:
            doc = self.documents.find_one({'_id': ObjectId(doc_id)})
            if doc:
                doc['_id'] = str(doc['_id'])
            return doc
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {e}")
            return None
    
    def get_all_documents(self, limit=None):
        """Get all documents."""
        try:
            cursor = self.documents.find()
            if limit:
                cursor = cursor.limit(limit)
            
            docs = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                docs.append(doc)
            return docs
        except Exception as e:
            logger.error(f"Error getting all documents: {e}")
            return []
    
    def update_document(self, doc_id, title=None, content=None, metadata=None):
        """Update a document."""
        try:
            update_data = {'updated_at': datetime.utcnow()}
            if title is not None:
                update_data['title'] = title
            if content is not None:
                update_data['content'] = content
            if metadata is not None:
                update_data['metadata'] = metadata
            
            result = self.documents.update_one(
                {'_id': ObjectId(doc_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")
            return False
    
    def delete_document(self, doc_id):
        """Delete a document."""
        try:
            result = self.documents.delete_one({'_id': ObjectId(doc_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False
    
    def search_documents(self, query, limit=10):
        """Basic text search in documents."""
        try:
            cursor = self.documents.find(
                {'$text': {'$search': query}},
                {'score': {'$meta': 'textScore'}}
            ).sort([('score', {'$meta': 'textScore'})]).limit(limit)
            
            docs = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                docs.append(doc)
            return docs
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def add_embedding(self, doc_id, embedding):
        """Add or update document embedding."""
        try:
            self.embeddings.update_one(
                {'doc_id': ObjectId(doc_id)},
                {'$set': {'embedding': embedding, 'updated_at': datetime.utcnow()}},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error adding embedding for document {doc_id}: {e}")
    
    def get_embedding(self, doc_id):
        """Get document embedding."""
        try:
            result = self.embeddings.find_one({'doc_id': ObjectId(doc_id)})
            return result['embedding'] if result else None
        except Exception as e:
            logger.error(f"Error getting embedding for document {doc_id}: {e}")
            return None
    
    def get_all_embeddings(self):
        """Get all document embeddings."""
        try:
            cursor = self.embeddings.find()
            embeddings = []
            for doc in cursor:
                embeddings.append({
                    'doc_id': str(doc['doc_id']),
                    'embedding': doc['embedding']
                })
            return embeddings
        except Exception as e:
            logger.error(f"Error getting all embeddings: {e}")
            return []
    
    def close(self):
        """Close database connection."""
        self.client.close()

