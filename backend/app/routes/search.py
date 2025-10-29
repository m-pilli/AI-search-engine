from flask import Blueprint, request, jsonify, current_app
import logging
from ..services.hybrid_search import HybridSearchService
from ..services.semantic_search import SemanticSearchService
from ..services.keyword_search import KeywordSearchService
from ..models.database import Database

logger = logging.getLogger(__name__)
search_bp = Blueprint('search', __name__)

# Initialize services (will be set by app factory)
hybrid_service = None
database = None

def init_search_services(app):
    """Initialize search services with app context."""
    global hybrid_service, database
    
    try:
        # Initialize database
        database = Database(app.config['MONGODB_URI'])
        
        # Initialize search services
        semantic_service = SemanticSearchService(
            model_name=app.config['EMBEDDING_MODEL']
        )
        keyword_service = KeywordSearchService()
        
        # Initialize hybrid service
        hybrid_service = HybridSearchService(semantic_service, keyword_service)
        
        logger.info("Search services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing search services: {e}")
        raise

@search_bp.route('/search', methods=['GET'])
def search():
    """Main search endpoint."""
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 10))
        alpha = float(request.args.get('alpha', 0.7))
        search_type = request.args.get('type', 'hybrid')  # hybrid, semantic, keyword
        
        # Validate parameters
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        if limit <= 0 or limit > 100:
            return jsonify({'error': 'Limit must be between 1 and 100'}), 400
        
        if alpha < 0 or alpha > 1:
            return jsonify({'error': 'Alpha must be between 0 and 1'}), 400
        
        if search_type not in ['hybrid', 'semantic', 'keyword']:
            return jsonify({'error': 'Search type must be hybrid, semantic, or keyword'}), 400
        
        # Perform search based on type
        if search_type == 'hybrid':
            search_results = hybrid_service.search(query, limit, alpha)
        elif search_type == 'semantic':
            search_results = hybrid_service.search_semantic_only(query, limit)
        else:  # keyword
            search_results = hybrid_service.search_keyword_only(query, limit)
        
        # Get full document details for results
        enriched_results = []
        for result in search_results['results']:
            doc_id = result['doc_id']
            doc = database.get_document(doc_id)
            
            if doc:
                enriched_result = {
                    'id': doc_id,
                    'title': doc['title'],
                    'content': doc['content'],
                    'metadata': doc.get('metadata', {}),
                    'score': result['score'],
                    'semantic_score': result.get('semantic_score', 0),
                    'keyword_score': result.get('keyword_score', 0),
                    'created_at': doc['created_at'].isoformat(),
                    'updated_at': doc['updated_at'].isoformat()
                }
                enriched_results.append(enriched_result)
        
        # Update results with enriched data
        search_results['results'] = enriched_results
        
        logger.info(f"Search completed: query='{query}', type={search_type}, results={len(enriched_results)}")
        return jsonify(search_results)
        
    except ValueError as e:
        logger.warning(f"Invalid parameter in search request: {e}")
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@search_bp.route('/search/suggestions', methods=['GET'])
def search_suggestions():
    """Get search suggestions based on partial query."""
    try:
        query = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 5))
        
        if not query or len(query) < 2:
            return jsonify({'suggestions': []})
        
        # Simple implementation - in production, you'd use a more sophisticated approach
        # like Elasticsearch completion suggester or a dedicated suggestion service
        suggestions = []
        
        # Get recent queries or popular queries from cache/database
        # This is a placeholder implementation
        popular_queries = [
            'machine learning',
            'artificial intelligence',
            'data science',
            'python programming',
            'web development'
        ]
        
        for popular_query in popular_queries:
            if query.lower() in popular_query.lower():
                suggestions.append(popular_query)
                if len(suggestions) >= limit:
                    break
        
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        logger.error(f"Error in search suggestions: {e}")
        return jsonify({'suggestions': []})

@search_bp.route('/search/stats', methods=['GET'])
def search_stats():
    """Get search engine statistics."""
    try:
        stats = hybrid_service.get_stats()
        
        # Add database stats
        all_docs = database.get_all_documents()
        stats['database'] = {
            'total_documents': len(all_docs),
            'total_content_length': sum(len(doc['content']) for doc in all_docs)
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting search stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

