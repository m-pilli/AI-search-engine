import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import pickle
import os
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

class SemanticSearchService:
    """Semantic search using sentence transformers and FAISS."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='./data/faiss_index'):
        self.model_name = model_name
        self.index_path = index_path
        self.model = None
        self.index = None
        self.document_ids = []
        self.embeddings_cache = {}
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        self._load_model()
        self._load_index()
    
    def _load_model(self):
        """Load the sentence transformer model."""
        try:
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _load_index(self):
        """Load or create FAISS index."""
        try:
            index_file = f"{self.index_path}.faiss"
            ids_file = f"{self.index_path}.pkl"
            
            if os.path.exists(index_file) and os.path.exists(ids_file):
                logger.info("Loading existing FAISS index")
                self.index = faiss.read_index(index_file)
                with open(ids_file, 'rb') as f:
                    self.document_ids = pickle.load(f)
                logger.info(f"Loaded index with {len(self.document_ids)} documents")
            else:
                logger.info("Creating new FAISS index")
                # Create a placeholder index - will be updated when documents are added
                dimension = self.model.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                self.document_ids = []
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            raise
    
    def _save_index(self):
        """Save FAISS index and document IDs."""
        try:
            index_file = f"{self.index_path}.faiss"
            ids_file = f"{self.index_path}.pkl"
            
            faiss.write_index(self.index, index_file)
            with open(ids_file, 'wb') as f:
                pickle.dump(self.document_ids, f)
            logger.info("Index saved successfully")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def encode_text(self, text: str) -> np.ndarray:
        """Encode text to embedding vector."""
        try:
            if text in self.embeddings_cache:
                return self.embeddings_cache[text]
            
            embedding = self.model.encode([text])[0]
            self.embeddings_cache[text] = embedding
            return embedding
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            raise
    
    def encode_documents(self, documents: List[str]) -> np.ndarray:
        """Encode multiple documents to embedding vectors."""
        try:
            embeddings = self.model.encode(documents)
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding documents: {e}")
            raise
    
    def add_document(self, doc_id: str, content: str):
        """Add a document to the search index."""
        try:
            # Encode the document
            embedding = self.encode_text(content)
            
            # Normalize for cosine similarity
            embedding = embedding / np.linalg.norm(embedding)
            
            # Add to FAISS index
            self.index.add(embedding.reshape(1, -1))
            self.document_ids.append(doc_id)
            
            logger.info(f"Added document {doc_id} to semantic index")
        except Exception as e:
            logger.error(f"Error adding document {doc_id}: {e}")
            raise
    
    def add_documents_batch(self, documents: List[Tuple[str, str]]):
        """Add multiple documents to the search index."""
        try:
            doc_ids, contents = zip(*documents)
            
            # Encode all documents
            embeddings = self.encode_documents(contents)
            
            # Normalize for cosine similarity
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
            
            # Add to FAISS index
            self.index.add(embeddings)
            self.document_ids.extend(doc_ids)
            
            logger.info(f"Added {len(documents)} documents to semantic index")
        except Exception as e:
            logger.error(f"Error adding documents batch: {e}")
            raise
    
    def search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        """Search for similar documents."""
        try:
            # Encode query
            query_embedding = self.encode_text(query)
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            
            # Search in FAISS index
            scores, indices = self.index.search(query_embedding.reshape(1, -1), k)
            
            # Return results with document IDs and scores
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.document_ids):
                    results.append((self.document_ids[idx], float(score)))
            
            logger.info(f"Semantic search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def rebuild_index(self, documents: List[Tuple[str, str]]):
        """Rebuild the entire search index."""
        try:
            logger.info("Rebuilding semantic search index")
            
            # Clear existing index
            dimension = self.model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatIP(dimension)
            self.document_ids = []
            
            # Add all documents
            self.add_documents_batch(documents)
            
            # Save the new index
            self._save_index()
            
            logger.info(f"Rebuilt index with {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error rebuilding index: {e}")
            raise
    
    def get_stats(self) -> Dict:
        """Get index statistics."""
        return {
            'total_documents': len(self.document_ids),
            'model_name': self.model_name,
            'embedding_dimension': self.model.get_sentence_embedding_dimension(),
            'index_type': 'FAISS_IndexFlatIP'
        }

