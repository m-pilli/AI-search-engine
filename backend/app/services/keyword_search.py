import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict, Tuple
import pickle
import os

logger = logging.getLogger(__name__)

class KeywordSearchService:
    """Keyword search using TF-IDF and BM25."""
    
    def __init__(self, vectorizer_path='./data/tfidf_vectorizer.pkl'):
        self.vectorizer_path = vectorizer_path
        self.vectorizer = None
        self.tfidf_matrix = None
        self.document_ids = []
        self.documents = []
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
        
        self._load_vectorizer()
    
    def _load_vectorizer(self):
        """Load or create TF-IDF vectorizer."""
        try:
            if os.path.exists(self.vectorizer_path):
                logger.info("Loading existing TF-IDF vectorizer")
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            else:
                logger.info("Creating new TF-IDF vectorizer")
                self.vectorizer = TfidfVectorizer(
                    max_features=10000,
                    stop_words='english',
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95
                )
        except Exception as e:
            logger.error(f"Error loading vectorizer: {e}")
            raise
    
    def _save_vectorizer(self):
        """Save TF-IDF vectorizer."""
        try:
            with open(self.vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            logger.info("Vectorizer saved successfully")
        except Exception as e:
            logger.error(f"Error saving vectorizer: {e}")
    
    def add_document(self, doc_id: str, content: str):
        """Add a document to the keyword search index."""
        try:
            self.document_ids.append(doc_id)
            self.documents.append(content)
            
            # Rebuild TF-IDF matrix
            self._rebuild_tfidf_matrix()
            
            logger.info(f"Added document {doc_id} to keyword index")
        except Exception as e:
            logger.error(f"Error adding document {doc_id}: {e}")
            raise
    
    def add_documents_batch(self, documents: List[Tuple[str, str]]):
        """Add multiple documents to the keyword search index."""
        try:
            doc_ids, contents = zip(*documents)
            
            self.document_ids.extend(doc_ids)
            self.documents.extend(contents)
            
            # Rebuild TF-IDF matrix
            self._rebuild_tfidf_matrix()
            
            logger.info(f"Added {len(documents)} documents to keyword index")
        except Exception as e:
            logger.error(f"Error adding documents batch: {e}")
            raise
    
    def _rebuild_tfidf_matrix(self):
        """Rebuild the TF-IDF matrix."""
        try:
            if not self.documents:
                self.tfidf_matrix = None
                return
            
            # Fit and transform documents
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
            
            # Save the updated vectorizer
            self._save_vectorizer()
            
            logger.info(f"Rebuilt TF-IDF matrix with {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"Error rebuilding TF-IDF matrix: {e}")
            raise
    
    def search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        """Search for documents using keyword matching."""
        try:
            if self.tfidf_matrix is None or len(self.documents) == 0:
                return []
            
            # Transform query to TF-IDF vector
            query_vector = self.vectorizer.transform([query])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top k results
            top_indices = np.argsort(similarities)[::-1][:k]
            
            # Return results with document IDs and scores
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Only return documents with non-zero similarity
                    results.append((self.document_ids[idx], float(similarities[idx])))
            
            logger.info(f"Keyword search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error in keyword search: {e}")
            return []
    
    def get_keywords(self, doc_id: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Get top keywords for a specific document."""
        try:
            if doc_id not in self.document_ids:
                return []
            
            doc_idx = self.document_ids.index(doc_id)
            doc_vector = self.tfidf_matrix[doc_idx].toarray().flatten()
            
            # Get feature names
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get top keywords
            top_indices = np.argsort(doc_vector)[::-1][:top_k]
            
            keywords = []
            for idx in top_indices:
                if doc_vector[idx] > 0:
                    keywords.append((feature_names[idx], float(doc_vector[idx])))
            
            return keywords
        except Exception as e:
            logger.error(f"Error getting keywords for document {doc_id}: {e}")
            return []
    
    def get_query_keywords(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Get top keywords from a query."""
        try:
            query_vector = self.vectorizer.transform([query]).toarray().flatten()
            feature_names = self.vectorizer.get_feature_names_out()
            
            top_indices = np.argsort(query_vector)[::-1][:top_k]
            
            keywords = []
            for idx in top_indices:
                if query_vector[idx] > 0:
                    keywords.append((feature_names[idx], float(query_vector[idx])))
            
            return keywords
        except Exception as e:
            logger.error(f"Error getting query keywords: {e}")
            return []
    
    def rebuild_index(self, documents: List[Tuple[str, str]]):
        """Rebuild the entire keyword search index."""
        try:
            logger.info("Rebuilding keyword search index")
            
            # Clear existing data
            self.document_ids = []
            self.documents = []
            
            # Add all documents
            self.add_documents_batch(documents)
            
            logger.info(f"Rebuilt keyword index with {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error rebuilding keyword index: {e}")
            raise
    
    def get_stats(self) -> Dict:
        """Get index statistics."""
        return {
            'total_documents': len(self.documents),
            'vocabulary_size': len(self.vectorizer.vocabulary_) if self.vectorizer.vocabulary_ else 0,
            'max_features': self.vectorizer.max_features,
            'ngram_range': self.vectorizer.ngram_range
        }

