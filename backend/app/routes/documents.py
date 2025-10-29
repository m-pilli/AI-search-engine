from flask import Blueprint, request, jsonify
import logging
from ..models.database import Database
from ..services.hybrid_search import HybridSearchService

logger = logging.getLogger(__name__)
documents_bp = Blueprint('documents', __name__)

# Initialize services (will be set by app factory)
database = None
hybrid_service = None

def init_document_services(db, search_service):
    """Initialize document services."""
    global database, hybrid_service
    database = db
    hybrid_service = search_service

@documents_bp.route('/documents', methods=['POST'])
def add_document():
    """Add a new document."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON data is required'}), 400
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        metadata = data.get('metadata', {})
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Add document to database
        doc_id = database.add_document(title, content, metadata)
        
        # Add to search index
        hybrid_service.add_document(doc_id, content)
        
        logger.info(f"Added document: {doc_id}")
        
        return jsonify({
            'id': doc_id,
            'title': title,
            'content': content,
            'metadata': metadata,
            'message': 'Document added successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@documents_bp.route('/documents/<doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a specific document."""
    try:
        doc = database.get_document(doc_id)
        
        if not doc:
            return jsonify({'error': 'Document not found'}), 404
        
        # Convert datetime objects to ISO format
        doc['created_at'] = doc['created_at'].isoformat()
        doc['updated_at'] = doc['updated_at'].isoformat()
        
        return jsonify(doc)
        
    except Exception as e:
        logger.error(f"Error getting document {doc_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@documents_bp.route('/documents/<doc_id>', methods=['PUT'])
def update_document(doc_id):
    """Update a document."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON data is required'}), 400
        
        title = data.get('title')
        content = data.get('content')
        metadata = data.get('metadata')
        
        # Check if document exists
        existing_doc = database.get_document(doc_id)
        if not existing_doc:
            return jsonify({'error': 'Document not found'}), 404
        
        # Update document
        success = database.update_document(doc_id, title, content, metadata)
        
        if not success:
            return jsonify({'error': 'Failed to update document'}), 500
        
        # Update search index if content changed
        if content is not None:
            hybrid_service.add_document(doc_id, content)
        
        logger.info(f"Updated document: {doc_id}")
        
        return jsonify({'message': 'Document updated successfully'})
        
    except Exception as e:
        logger.error(f"Error updating document {doc_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@documents_bp.route('/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document."""
    try:
        # Check if document exists
        existing_doc = database.get_document(doc_id)
        if not existing_doc:
            return jsonify({'error': 'Document not found'}), 404
        
        # Delete document
        success = database.delete_document(doc_id)
        
        if not success:
            return jsonify({'error': 'Failed to delete document'}), 500
        
        logger.info(f"Deleted document: {doc_id}")
        
        return jsonify({'message': 'Document deleted successfully'})
        
    except Exception as e:
        logger.error(f"Error deleting document {doc_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@documents_bp.route('/documents', methods=['GET'])
def list_documents():
    """List all documents with pagination."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        if page < 1:
            return jsonify({'error': 'Page must be >= 1'}), 400
        
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
        # Get all documents
        all_docs = database.get_all_documents()
        
        # Calculate pagination
        total_docs = len(all_docs)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_docs = all_docs[start_idx:end_idx]
        
        # Convert datetime objects to ISO format
        for doc in paginated_docs:
            doc['created_at'] = doc['created_at'].isoformat()
            doc['updated_at'] = doc['updated_at'].isoformat()
        
        return jsonify({
            'documents': paginated_docs,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_docs,
                'pages': (total_docs + per_page - 1) // per_page
            }
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@documents_bp.route('/documents/batch', methods=['POST'])
def add_documents_batch():
    """Add multiple documents at once."""
    try:
        data = request.get_json()
        
        if not data or 'documents' not in data:
            return jsonify({'error': 'Documents array is required'}), 400
        
        documents = data['documents']
        
        if not isinstance(documents, list):
            return jsonify({'error': 'Documents must be an array'}), 400
        
        if len(documents) > 100:
            return jsonify({'error': 'Maximum 100 documents per batch'}), 400
        
        added_docs = []
        errors = []
        
        for i, doc_data in enumerate(documents):
            try:
                title = doc_data.get('title', '').strip()
                content = doc_data.get('content', '').strip()
                metadata = doc_data.get('metadata', {})
                
                if not title or not content:
                    errors.append(f"Document {i}: Title and content are required")
                    continue
                
                doc_id = database.add_document(title, content, metadata)
                added_docs.append({
                    'id': doc_id,
                    'title': title,
                    'content': content,
                    'metadata': metadata
                })
                
            except Exception as e:
                errors.append(f"Document {i}: {str(e)}")
        
        # Add all successful documents to search index
        if added_docs:
            search_docs = [(doc['id'], doc['content']) for doc in added_docs]
            hybrid_service.add_documents_batch(search_docs)
        
        logger.info(f"Batch added {len(added_docs)} documents")
        
        return jsonify({
            'added_documents': added_docs,
            'total_added': len(added_docs),
            'errors': errors
        }), 201
        
    except Exception as e:
        logger.error(f"Error in batch document addition: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@documents_bp.route('/documents/rebuild-index', methods=['POST'])
def rebuild_search_index():
    """Rebuild the search index from all documents."""
    try:
        # Get all documents
        all_docs = database.get_all_documents()
        
        if not all_docs:
            return jsonify({'message': 'No documents to index'})
        
        # Prepare documents for indexing
        search_docs = [(doc['_id'], doc['content']) for doc in all_docs]
        
        # Rebuild index
        hybrid_service.rebuild_index(search_docs)
        
        logger.info(f"Rebuilt search index with {len(all_docs)} documents")
        
        return jsonify({
            'message': 'Search index rebuilt successfully',
            'total_documents': len(all_docs)
        })
        
    except Exception as e:
        logger.error(f"Error rebuilding search index: {e}")
        return jsonify({'error': 'Internal server error'}), 500

