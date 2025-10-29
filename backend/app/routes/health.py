from flask import Blueprint, jsonify
import logging
import time
from ..models.database import Database

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)

# Global database instance (will be set by app factory)
database = None

def init_health_services(db):
    """Initialize health check services."""
    global database
    database = db

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': time.time(),
            'service': 'AI Search Engine',
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with service status."""
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': time.time(),
            'service': 'AI Search Engine',
            'version': '1.0.0',
            'services': {}
        }
        
        # Check database connection
        try:
            if database:
                # Try to get document count
                docs = database.get_all_documents(limit=1)
                health_status['services']['database'] = {
                    'status': 'healthy',
                    'type': 'MongoDB',
                    'connected': True
                }
            else:
                health_status['services']['database'] = {
                    'status': 'unhealthy',
                    'error': 'Database not initialized'
                }
        except Exception as e:
            health_status['services']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # Check if any service is unhealthy
        unhealthy_services = [
            service for service in health_status['services'].values()
            if service['status'] == 'unhealthy'
        ]
        
        if unhealthy_services:
            health_status['status'] = 'degraded'
        
        return jsonify(health_status)
        
    except Exception as e:
        logger.error(f"Error in detailed health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }), 500

@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness check for Kubernetes/container orchestration."""
    try:
        # Check if all critical services are ready
        if not database:
            return jsonify({
                'status': 'not_ready',
                'reason': 'Database not initialized'
            }), 503
        
        # Try a simple database operation
        database.get_all_documents(limit=1)
        
        return jsonify({
            'status': 'ready',
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({
            'status': 'not_ready',
            'reason': str(e)
        }), 503

@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """Liveness check for Kubernetes/container orchestration."""
    try:
        return jsonify({
            'status': 'alive',
            'timestamp': time.time()
        })
    except Exception as e:
        logger.error(f"Liveness check failed: {e}")
        return jsonify({
            'status': 'dead',
            'error': str(e)
        }), 500

