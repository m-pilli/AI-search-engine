#!/bin/bash

# AI Search Engine Deployment Script
# This script handles the complete deployment of the AI Search Engine

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ai-search-engine"
BACKEND_IMAGE="ai-search-backend"
FRONTEND_IMAGE="ai-search-frontend"
REGISTRY="your-registry.com"  # Change this to your Docker registry

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    log_success "Docker is running"
}

# Build Docker images
build_images() {
    log_info "Building Docker images..."
    
    # Build backend
    log_info "Building backend image..."
    docker build -t ${BACKEND_IMAGE}:latest ./backend
    log_success "Backend image built successfully"
    
    # Build frontend
    log_info "Building frontend image..."
    docker build -t ${FRONTEND_IMAGE}:latest ./frontend
    log_success "Frontend image built successfully"
}

# Tag images for registry
tag_images() {
    log_info "Tagging images for registry..."
    docker tag ${BACKEND_IMAGE}:latest ${REGISTRY}/${BACKEND_IMAGE}:latest
    docker tag ${FRONTEND_IMAGE}:latest ${REGISTRY}/${FRONTEND_IMAGE}:latest
    log_success "Images tagged successfully"
}

# Push images to registry
push_images() {
    log_info "Pushing images to registry..."
    docker push ${REGISTRY}/${BACKEND_IMAGE}:latest
    docker push ${REGISTRY}/${FRONTEND_IMAGE}:latest
    log_success "Images pushed successfully"
}

# Deploy with Docker Compose
deploy_compose() {
    log_info "Deploying with Docker Compose..."
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        log_warning ".env file not found. Creating from example..."
        cp env.prod.example .env
        log_warning "Please update .env file with your actual values before continuing."
        read -p "Press Enter to continue after updating .env file..."
    fi
    
    # Stop existing containers
    docker-compose -f docker-compose.prod.yml down
    
    # Start services
    docker-compose -f docker-compose.prod.yml up -d
    
    log_success "Services deployed successfully"
    log_info "Services are starting up. This may take a few minutes..."
    
    # Wait for services to be healthy
    wait_for_services
}

# Deploy with Kubernetes
deploy_k8s() {
    log_info "Deploying with Kubernetes..."
    
    # Create namespace
    kubectl create namespace ${PROJECT_NAME} --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply configurations
    kubectl apply -f k8s/mongodb.yaml
    kubectl apply -f k8s/redis.yaml
    kubectl apply -f k8s/backend.yaml
    kubectl apply -f k8s/frontend.yaml
    kubectl apply -f k8s/ingress.yaml
    
    log_success "Kubernetes deployment completed"
    log_info "Waiting for pods to be ready..."
    
    # Wait for pods
    kubectl wait --for=condition=ready pod -l app=backend -n ${PROJECT_NAME} --timeout=300s
    kubectl wait --for=condition=ready pod -l app=frontend -n ${PROJECT_NAME} --timeout=300s
    
    log_success "All pods are ready"
}

# Wait for services to be healthy
wait_for_services() {
    log_info "Waiting for services to be healthy..."
    
    # Wait for backend
    for i in {1..30}; do
        if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
            log_success "Backend is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Backend failed to become healthy"
            exit 1
        fi
        sleep 10
    done
    
    # Wait for frontend
    for i in {1..30}; do
        if curl -f http://localhost:3000 > /dev/null 2>&1; then
            log_success "Frontend is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Frontend failed to become healthy"
            exit 1
        fi
        sleep 10
    done
}

# Show deployment status
show_status() {
    log_info "Deployment Status:"
    echo ""
    
    if command -v docker-compose > /dev/null 2>&1; then
        docker-compose -f docker-compose.prod.yml ps
    fi
    
    if command -v kubectl > /dev/null 2>&1; then
        kubectl get pods -n ${PROJECT_NAME}
    fi
    
    echo ""
    log_info "Access URLs:"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:5000/api"
    echo "Health Check: http://localhost:5000/api/health"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up..."
    docker-compose -f docker-compose.prod.yml down
    kubectl delete namespace ${PROJECT_NAME} --ignore-not-found=true
    log_success "Cleanup completed"
}

# Main deployment function
main() {
    echo "=========================================="
    echo "AI Search Engine Deployment Script"
    echo "=========================================="
    echo ""
    
    # Parse command line arguments
    case "${1:-compose}" in
        "compose")
            check_docker
            build_images
            deploy_compose
            show_status
            ;;
        "k8s")
            check_docker
            build_images
            tag_images
            push_images
            deploy_k8s
            show_status
            ;;
        "build")
            check_docker
            build_images
            log_success "Images built successfully"
            ;;
        "cleanup")
            cleanup
            ;;
        "status")
            show_status
            ;;
        *)
            echo "Usage: $0 {compose|k8s|build|cleanup|status}"
            echo ""
            echo "Commands:"
            echo "  compose  - Deploy using Docker Compose (default)"
            echo "  k8s      - Deploy using Kubernetes"
            echo "  build    - Build Docker images only"
            echo "  cleanup  - Clean up all deployments"
            echo "  status   - Show deployment status"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"

