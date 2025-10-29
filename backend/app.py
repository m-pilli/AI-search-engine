import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/search_engine')
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    app.config['EMBEDDING_MODEL'] = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    app.config['CACHE_TTL'] = int(os.getenv('CACHE_TTL', '3600'))
    
    # Initialize services
    from app.models.database import Database
    from app.services.semantic_search import SemanticSearchService
    from app.services.keyword_search import KeywordSearchService
    from app.services.hybrid_search import HybridSearchService
    
    # Initialize database
    db = Database(app.config['MONGODB_URI'])
    
    # Initialize search services
    semantic_service = SemanticSearchService(
        model_name=app.config['EMBEDDING_MODEL']
    )
    keyword_service = KeywordSearchService()
    hybrid_service = HybridSearchService(semantic_service, keyword_service)
    
    # Register blueprints
    from app.routes.search import search_bp, init_search_services
    from app.routes.documents import documents_bp, init_document_services
    from app.routes.health import health_bp, init_health_services
    
    # Initialize route services
    init_search_services(app)
    init_document_services(db, hybrid_service)
    init_health_services(db)
    
    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(documents_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting AI Search Engine on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
