#!/bin/bash

# ESG Platform Deployment Script
# Supports multiple environments and module-specific deployments

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DEPLOYMENT_CONFIG="${SCRIPT_DIR}/config.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Help function
show_help() {
    cat << EOF
ESG Platform Deployment Script

Usage: $0 [OPTIONS] COMMAND

Commands:
    deploy          Deploy the entire platform
    deploy-module   Deploy a specific module
    rollback        Rollback to previous version
    status          Show deployment status
    health-check    Run health checks
    logs            Show deployment logs

Options:
    -e, --environment ENV    Deployment environment (staging|production)
    -m, --module MODULE      Specific module to deploy
    -v, --version VERSION    Version to deploy
    -f, --force             Force deployment without confirmation
    -h, --help              Show this help message

Examples:
    $0 deploy -e staging
    $0 deploy-module -e production -m api-gateway -v 1.2.0
    $0 status -e production
    $0 rollback -e production -v 1.1.0

EOF
}

# Parse command line arguments
parse_args() {
    COMMAND=""
    ENVIRONMENT=""
    MODULE=""
    VERSION=""
    FORCE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -m|--module)
                MODULE="$2"
                shift 2
                ;;
            -v|--version)
                VERSION="$2"
                shift 2
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            deploy|deploy-module|rollback|status|health-check|logs)
                COMMAND="$1"
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$COMMAND" ]]; then
        log_error "Command is required"
        show_help
        exit 1
    fi

    if [[ "$COMMAND" == "deploy" || "$COMMAND" == "deploy-module" || "$COMMAND" == "rollback" || "$COMMAND" == "status" || "$COMMAND" == "health-check" || "$COMMAND" == "logs" ]]; then
        if [[ -z "$ENVIRONMENT" ]]; then
            log_error "Environment (-e) is required"
            exit 1
        fi
    fi
}

# Load deployment configuration
load_config() {
    if [[ ! -f "$DEPLOYMENT_CONFIG" ]]; then
        log_error "Deployment configuration not found: $DEPLOYMENT_CONFIG"
        exit 1
    fi

    log_info "Loading deployment configuration..."
    
    # Parse YAML configuration (simplified)
    ENV_CONFIG=$(grep -A 20 "environment: $ENVIRONMENT" "$DEPLOYMENT_CONFIG" || true)
    
    if [[ -z "$ENV_CONFIG" ]]; then
        log_error "Environment '$ENVIRONMENT' not found in configuration"
        exit 1
    fi
}

# Validate deployment prerequisites
validate_prerequisites() {
    log_info "Validating deployment prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi

    # Check kubectl (if using Kubernetes)
    if command -v kubectl &> /dev/null; then
        log_info "Kubernetes CLI found"
    else
        log_warning "Kubernetes CLI not found - Kubernetes deployments will be skipped"
    fi

    # Check Helm (if using Helm)
    if command -v helm &> /dev/null; then
        log_info "Helm found"
    else
        log_warning "Helm not found - Helm deployments will be skipped"
    fi

    log_success "Prerequisites validation completed"
}

# Build Docker images
build_images() {
    log_info "Building Docker images..."

    local modules=(
        "api-gateway"
        "aggregation-engine"
        "monitoring-dashboard"
        "ai-gateway"
        "web-frontend"
        "risk-interest-rate"
        "risk-credit"
        "risk-equity"
        "risk-foreign-exchange"
        "risk-inflation"
        "risk-liquidity"
        "risk-counterparty"
    )

    for module in "${modules[@]}"; do
        if [[ -n "$MODULE" && "$MODULE" != "$module" ]]; then
            continue
        fi

        local module_dir="$PROJECT_ROOT/repositories/$module"
        if [[ -f "$module_dir/Dockerfile" ]]; then
            log_info "Building image for $module..."
            
            local image_tag="gnanam-esg/$module:$VERSION"
            if [[ -z "$VERSION" ]]; then
                image_tag="gnanam-esg/$module:latest"
            fi

            docker build -t "$image_tag" "$module_dir"
            log_success "Built image: $image_tag"
        else
            log_warning "No Dockerfile found for $module"
        fi
    done
}

# Deploy using Docker Compose
deploy_docker_compose() {
    log_info "Deploying using Docker Compose..."

    local compose_file="$SCRIPT_DIR/docker-compose.$ENVIRONMENT.yml"
    
    if [[ ! -f "$compose_file" ]]; then
        log_error "Docker Compose file not found: $compose_file"
        exit 1
    fi

    # Set environment variables
    export ENVIRONMENT="$ENVIRONMENT"
    export VERSION="${VERSION:-latest}"
    
    # Deploy
    docker-compose -f "$compose_file" up -d
    
    log_success "Docker Compose deployment completed"
}

# Deploy using Kubernetes
deploy_kubernetes() {
    if ! command -v kubectl &> /dev/null; then
        log_warning "Skipping Kubernetes deployment - kubectl not available"
        return
    fi

    log_info "Deploying using Kubernetes..."

    local k8s_dir="$SCRIPT_DIR/k8s/$ENVIRONMENT"
    
    if [[ ! -d "$k8s_dir" ]]; then
        log_warning "Kubernetes manifests not found: $k8s_dir"
        return
    fi

    # Apply namespace
    kubectl apply -f "$k8s_dir/namespace.yaml" || true

    # Apply all manifests
    kubectl apply -f "$k8s_dir/" --recursive

    log_success "Kubernetes deployment completed"
}

# Deploy using Helm
deploy_helm() {
    if ! command -v helm &> /dev/null; then
        log_warning "Skipping Helm deployment - helm not available"
        return
    fi

    log_info "Deploying using Helm..."

    local helm_chart="$SCRIPT_DIR/helm-charts/esg-platform"
    
    if [[ ! -d "$helm_chart" ]]; then
        log_warning "Helm chart not found: $helm_chart"
        return
    fi

    # Set values
    local values_file="$SCRIPT_DIR/helm-values.$ENVIRONMENT.yaml"
    local set_values=""
    
    if [[ -n "$VERSION" ]]; then
        set_values="--set version=$VERSION"
    fi

    # Deploy/upgrade
    helm upgrade --install esg-platform "$helm_chart" \
        --namespace "$ENVIRONMENT" \
        --create-namespace \
        --values "$values_file" \
        $set_values

    log_success "Helm deployment completed"
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."

    local health_script="$SCRIPT_DIR/health-check.sh"
    
    if [[ -f "$health_script" ]]; then
        bash "$health_script" -e "$ENVIRONMENT"
    else
        log_warning "Health check script not found: $health_script"
        
        # Basic health checks
        log_info "Running basic health checks..."
        
        # Check if services are responding
        local services=("api-gateway" "monitoring-dashboard" "web-frontend")
        for service in "${services[@]}"; do
            local url="http://localhost:8000/health"
            if curl -f -s "$url" > /dev/null; then
                log_success "$service is healthy"
            else
                log_error "$service health check failed"
            fi
        done
    fi
}

# Show deployment status
show_status() {
    log_info "Showing deployment status for environment: $ENVIRONMENT"

    # Docker Compose status
    local compose_file="$SCRIPT_DIR/docker-compose.$ENVIRONMENT.yml"
    if [[ -f "$compose_file" ]]; then
        echo "=== Docker Compose Status ==="
        docker-compose -f "$compose_file" ps
        echo
    fi

    # Kubernetes status
    if command -v kubectl &> /dev/null; then
        echo "=== Kubernetes Status ==="
        kubectl get pods -n "$ENVIRONMENT" 2>/dev/null || true
        echo
        
        echo "=== Kubernetes Services ==="
        kubectl get services -n "$ENVIRONMENT" 2>/dev/null || true
        echo
    fi

    # Helm status
    if command -v helm &> /dev/null; then
        echo "=== Helm Releases ==="
        helm list -n "$ENVIRONMENT" 2>/dev/null || true
        echo
    fi
}

# Rollback deployment
rollback_deployment() {
    log_info "Rolling back to version: $VERSION"

    if [[ -z "$VERSION" ]]; then
        log_error "Version is required for rollback"
        exit 1
    fi

    # Docker Compose rollback
    local compose_file="$SCRIPT_DIR/docker-compose.$ENVIRONMENT.yml"
    if [[ -f "$compose_file" ]]; then
        export VERSION="$VERSION"
        docker-compose -f "$compose_file" up -d
        log_success "Docker Compose rollback completed"
    fi

    # Kubernetes rollback
    if command -v kubectl &> /dev/null; then
        kubectl rollout undo deployment -n "$ENVIRONMENT" --to-revision="$VERSION" 2>/dev/null || true
        log_success "Kubernetes rollback completed"
    fi

    # Helm rollback
    if command -v helm &> /dev/null; then
        helm rollback esg-platform "$VERSION" -n "$ENVIRONMENT" 2>/dev/null || true
        log_success "Helm rollback completed"
    fi
}

# Show logs
show_logs() {
    log_info "Showing logs for environment: $ENVIRONMENT"

    # Docker Compose logs
    local compose_file="$SCRIPT_DIR/docker-compose.$ENVIRONMENT.yml"
    if [[ -f "$compose_file" ]]; then
        echo "=== Docker Compose Logs ==="
        docker-compose -f "$compose_file" logs --tail=50
        echo
    fi

    # Kubernetes logs
    if command -v kubectl &> /dev/null; then
        echo "=== Kubernetes Logs ==="
        kubectl logs -n "$ENVIRONMENT" --tail=50 -l app=esg-platform 2>/dev/null || true
        echo
    fi
}

# Main deployment function
deploy() {
    log_info "Starting deployment to $ENVIRONMENT environment"
    
    if [[ -n "$MODULE" ]]; then
        log_info "Deploying specific module: $MODULE"
    fi
    
    if [[ -n "$VERSION" ]]; then
        log_info "Deploying version: $VERSION"
    fi

    # Confirm deployment (unless forced)
    if [[ "$FORCE" != true ]]; then
        echo
        echo "Deployment Summary:"
        echo "  Environment: $ENVIRONMENT"
        echo "  Module: ${MODULE:-all}"
        echo "  Version: ${VERSION:-latest}"
        echo
        read -p "Do you want to proceed with deployment? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Deployment cancelled"
            exit 0
        fi
    fi

    # Load configuration
    load_config

    # Validate prerequisites
    validate_prerequisites

    # Build images
    build_images

    # Deploy based on configuration
    deploy_docker_compose
    deploy_kubernetes
    deploy_helm

    # Run health checks
    run_health_checks

    log_success "Deployment completed successfully!"
}

# Main execution
main() {
    parse_args "$@"

    case "$COMMAND" in
        deploy)
            deploy
            ;;
        deploy-module)
            deploy
            ;;
        rollback)
            rollback_deployment
            ;;
        status)
            show_status
            ;;
        health-check)
            run_health_checks
            ;;
        logs)
            show_logs
            ;;
        *)
            log_error "Unknown command: $COMMAND"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 