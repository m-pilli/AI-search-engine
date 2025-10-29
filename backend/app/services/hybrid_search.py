import logging
from typing import List, Dict, Tuple
import time
from .semantic_search import SemanticSearchService
from .keyword_search import KeywordSearchService

logger = logging.getLogger(__name__)

class HybridSearchService:
    """Hybrid search combining semantic and keyword search."""
    
    def __init__(self, semantic_service: SemanticSearchService, keyword_service: KeywordSearchService):
        self.semantic_service = semantic_service
        self.keyword_service = keyword_service
        self.default_alpha = 0.7  # Weight for semantic search (0.7 = 70% semantic, 30% keyword)
    
    def search(self, query: str, k: int = 10, alpha: float = None) -> Dict:
        """Perform hybrid search combining semantic and keyword results."""
        start_time = time.time()
        
        try:
            if alpha is None:
                alpha = self.default_alpha
            
            # Perform both searches
            semantic_results = self.semantic_service.search(query, k * 2)  # Get more results for better ranking
            keyword_results = self.keyword_service.search(query, k * 2)
            
            # Convert to dictionaries for easier merging
            semantic_scores = {doc_id: score for doc_id, score in semantic_results}
            keyword_scores = {doc_id: score for doc_id, score in keyword_results}
            
            # Get all unique document IDs
            all_doc_ids = set(semantic_scores.keys()) | set(keyword_scores.keys())
            
            # Calculate hybrid scores
            hybrid_scores = {}
            for doc_id in all_doc_ids:
                semantic_score = semantic_scores.get(doc_id, 0.0)
                keyword_score = keyword_scores.get(doc_id, 0.0)
                
                # Normalize scores to [0, 1] range
                semantic_norm = semantic_score  # Already normalized
                keyword_norm = keyword_score    # Already normalized
                
                # Calculate hybrid score
                hybrid_score = alpha * semantic_norm + (1 - alpha) * keyword_norm
                
                hybrid_scores[doc_id] = {
                    'hybrid_score': hybrid_score,
                    'semantic_score': semantic_score,
                    'keyword_score': keyword_score
                }
            
            # Sort by hybrid score and get top k
            sorted_results = sorted(
                hybrid_scores.items(),
                key=lambda x: x[1]['hybrid_score'],
                reverse=True
            )[:k]
            
            # Format results
            results = []
            for doc_id, scores in sorted_results:
                results.append({
                    'doc_id': doc_id,
                    'score': scores['hybrid_score'],
                    'semantic_score': scores['semantic_score'],
                    'keyword_score': scores['keyword_score']
                })
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            logger.info(f"Hybrid search completed in {response_time:.2f}ms with {len(results)} results")
            
            return {
                'results': results,
                'query': query,
                'total_results': len(results),
                'response_time_ms': round(response_time, 2),
                'alpha': alpha,
                'search_stats': {
                    'semantic_results_count': len(semantic_results),
                    'keyword_results_count': len(keyword_results),
                    'unique_documents': len(all_doc_ids)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': (time.time() - start_time) * 1000,
                'error': str(e)
            }
    
    def add_document(self, doc_id: str, content: str):
        """Add a document to both search indices."""
        try:
            self.semantic_service.add_document(doc_id, content)
            self.keyword_service.add_document(doc_id, content)
            logger.info(f"Added document {doc_id} to hybrid search index")
        except Exception as e:
            logger.error(f"Error adding document {doc_id}: {e}")
            raise
    
    def add_documents_batch(self, documents: List[Tuple[str, str]]):
        """Add multiple documents to both search indices."""
        try:
            self.semantic_service.add_documents_batch(documents)
            self.keyword_service.add_documents_batch(documents)
            logger.info(f"Added {len(documents)} documents to hybrid search index")
        except Exception as e:
            logger.error(f"Error adding documents batch: {e}")
            raise
    
    def rebuild_index(self, documents: List[Tuple[str, str]]):
        """Rebuild both search indices."""
        try:
            logger.info("Rebuilding hybrid search index")
            self.semantic_service.rebuild_index(documents)
            self.keyword_service.rebuild_index(documents)
            logger.info("Hybrid search index rebuilt successfully")
        except Exception as e:
            logger.error(f"Error rebuilding hybrid index: {e}")
            raise
    
    def get_stats(self) -> Dict:
        """Get statistics for both search services."""
        return {
            'semantic_search': self.semantic_service.get_stats(),
            'keyword_search': self.keyword_service.get_stats(),
            'default_alpha': self.default_alpha
        }
    
    def set_alpha(self, alpha: float):
        """Set the default alpha value for hybrid ranking."""
        if 0 <= alpha <= 1:
            self.default_alpha = alpha
            logger.info(f"Set hybrid search alpha to {alpha}")
        else:
            raise ValueError("Alpha must be between 0 and 1")
    
    def search_semantic_only(self, query: str, k: int = 10) -> Dict:
        """Perform semantic search only."""
        start_time = time.time()
        
        try:
            results = self.semantic_service.search(query, k)
            
            formatted_results = []
            for doc_id, score in results:
                formatted_results.append({
                    'doc_id': doc_id,
                    'score': score,
                    'semantic_score': score,
                    'keyword_score': 0.0
                })
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                'results': formatted_results,
                'query': query,
                'total_results': len(formatted_results),
                'response_time_ms': round(response_time, 2),
                'search_type': 'semantic_only'
            }
        except Exception as e:
            logger.error(f"Error in semantic-only search: {e}")
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': (time.time() - start_time) * 1000,
                'error': str(e)
            }
    
    def search_keyword_only(self, query: str, k: int = 10) -> Dict:
        """Perform keyword search only."""
        start_time = time.time()
        
        try:
            results = self.keyword_service.search(query, k)
            
            formatted_results = []
            for doc_id, score in results:
                formatted_results.append({
                    'doc_id': doc_id,
                    'score': score,
                    'semantic_score': 0.0,
                    'keyword_score': score
                })
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                'results': formatted_results,
                'query': query,
                'total_results': len(formatted_results),
                'response_time_ms': round(response_time, 2),
                'search_type': 'keyword_only'
            }
        except Exception as e:
            logger.error(f"Error in keyword-only search: {e}")
            return {
                'results': [],
                'query': query,
                'total_results': 0,
                'response_time_ms': (time.time() - start_time) * 1000,
                'error': str(e)
            }

