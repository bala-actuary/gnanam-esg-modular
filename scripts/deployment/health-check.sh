#!/bin/bash

# ESG Platform Health Check Script
# Performs comprehensive health checks across all services

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Health check results
HEALTH_STATUS=0
FAILED_CHECKS=()
PASSED_CHECKS=()

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
ESG Platform Health Check Script

Usage: $0 [OPTIONS]

Options:
    -e, --environment ENV    Environment to check (staging|production|development)
    -s, --service SERVICE    Check specific service only
    -t, --timeout SECONDS    Timeout for health checks (default: 30)
    -v, --verbose           Verbose output
    -h, --help              Show this help message

Examples:
    $0 -e production
    $0 -e staging -s api-gateway
    $0 -e development -v

EOF
}

# Parse command line arguments
parse_args() {
    ENVIRONMENT=""
    SERVICE=""
    TIMEOUT=30
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -s|--service)
                SERVICE="$2"
                shift 2
                ;;
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    if [[ -z "$ENVIRONMENT" ]]; then
        log_error "Environment (-e) is required"
        show_help
        exit 1
    fi
}

# Load configuration
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_error "Configuration file not found: $CONFIG_FILE"
        exit 1
    fi

    log_info "Loading configuration for environment: $ENVIRONMENT"
    
    # Parse environment configuration (simplified)
    ENV_CONFIG=$(grep -A 50 "environment: $ENVIRONMENT" "$CONFIG_FILE" || true)
    
    if [[ -z "$ENV_CONFIG" ]]; then
        log_error "Environment '$ENVIRONMENT' not found in configuration"
        exit 1
    fi
}

# Check if service is running (Docker Compose)
check_docker_service() {
    local service_name="$1"
    local compose_file="${SCRIPT_DIR}/docker-compose.${ENVIRONMENT}.yml"
    
    if [[ ! -f "$compose_file" ]]; then
        return 1
    fi

    local status=$(docker-compose -f "$compose_file" ps -q "$service_name" 2>/dev/null | wc -l)
    [[ $status -gt 0 ]]
}

# Check if service is running (Kubernetes)
check_k8s_service() {
    local service_name="$1"
    
    if ! command -v kubectl &> /dev/null; then
        return 1
    fi

    local status=$(kubectl get pods -n "$ENVIRONMENT" -l app="$service_name" --field-selector=status.phase=Running 2>/dev/null | wc -l)
    [[ $status -gt 0 ]]
}

# Check HTTP endpoint
check_http_endpoint() {
    local url="$1"
    local timeout="$2"
    local expected_status="${3:-200}"
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$timeout" "$url" 2>/dev/null || echo "000")
    [[ "$response" == "$expected_status" ]]
}

# Check database connectivity
check_database() {
    local db_type="$1"
    local host="$2"
    local port="$3"
    local database="$4"
    
    case "$db_type" in
        postgres)
            # Check PostgreSQL
            if command -v psql &> /dev/null; then
                PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$host" -p "$port" -d "$database" -c "SELECT 1;" > /dev/null 2>&1
            else
                # Use Docker if psql not available
                docker run --rm postgres:15 psql -h "$host" -p "$port" -d "$database" -U postgres -c "SELECT 1;" > /dev/null 2>&1
            fi
            ;;
        redis)
            # Check Redis
            if command -v redis-cli &> /dev/null; then
                redis-cli -h "$host" -p "$port" ping > /dev/null 2>&1
            else
                # Use Docker if redis-cli not available
                docker run --rm redis:7-alpine redis-cli -h "$host" -p "$port" ping > /dev/null 2>&1
            fi
            ;;
        *)
            return 1
            ;;
    esac
}

# Check service health
check_service_health() {
    local service_name="$1"
    local port="$2"
    local health_path="$3"
    
    local base_url="http://localhost:$port"
    local health_url="$base_url$health_path"
    
    # Check if service is running
    if ! check_docker_service "$service_name" && ! check_k8s_service "$service_name"; then
        log_error "Service $service_name is not running"
        return 1
    fi
    
    # Check health endpoint
    if ! check_http_endpoint "$health_url" "$TIMEOUT"; then
        log_error "Health check failed for $service_name at $health_url"
        return 1
    fi
    
    log_success "Service $service_name is healthy"
    return 0
}

# Check all services
check_all_services() {
    log_info "Checking all services..."
    
    local services=(
        "api-gateway:8000:/health"
        "aggregation-engine:8001:/health"
        "monitoring-dashboard:8002:/health"
        "ai-gateway:8003:/health"
        "web-frontend:3000:/"
        "risk-interest-rate:8010:/health"
        "risk-credit:8011:/health"
        "risk-equity:8012:/health"
        "risk-foreign-exchange:8013:/health"
        "risk-inflation:8014:/health"
        "risk-liquidity:8015:/health"
        "risk-counterparty:8016:/health"
    )
    
    for service_config in "${services[@]}"; do
        IFS=':' read -r service_name port health_path <<< "$service_config"
        
        if [[ -n "$SERVICE" && "$SERVICE" != "$service_name" ]]; then
            continue
        fi
        
        log_info "Checking $service_name..."
        
        if check_service_health "$service_name" "$port" "$health_path"; then
            PASSED_CHECKS+=("$service_name")
        else
            FAILED_CHECKS+=("$service_name")
            HEALTH_STATUS=1
        fi
    done
}

# Check databases
check_databases() {
    log_info "Checking databases..."
    
    # PostgreSQL
    if [[ "$ENVIRONMENT" == "production" ]]; then
        local pg_host="production-postgres"
        local pg_db="esg_production"
    elif [[ "$ENVIRONMENT" == "staging" ]]; then
        local pg_host="staging-postgres"
        local pg_db="esg_staging"
    else
        local pg_host="dev-postgres"
        local pg_db="esg_development"
    fi
    
    log_info "Checking PostgreSQL..."
    if check_database "postgres" "$pg_host" "5432" "$pg_db"; then
        log_success "PostgreSQL is healthy"
        PASSED_CHECKS+=("postgresql")
    else
        log_error "PostgreSQL health check failed"
        FAILED_CHECKS+=("postgresql")
        HEALTH_STATUS=1
    fi
    
    # Redis
    if [[ "$ENVIRONMENT" == "production" ]]; then
        local redis_host="production-redis"
    elif [[ "$ENVIRONMENT" == "staging" ]]; then
        local redis_host="staging-redis"
    else
        local redis_host="dev-redis"
    fi
    
    log_info "Checking Redis..."
    if check_database "redis" "$redis_host" "6379"; then
        log_success "Redis is healthy"
        PASSED_CHECKS+=("redis")
    else
        log_error "Redis health check failed"
        FAILED_CHECKS+=("redis")
        HEALTH_STATUS=1
    fi
}

# Check system resources
check_system_resources() {
    log_info "Checking system resources..."
    
    # Check CPU usage
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        log_warning "High CPU usage: ${cpu_usage}%"
        FAILED_CHECKS+=("cpu_usage")
        HEALTH_STATUS=1
    else
        log_success "CPU usage is normal: ${cpu_usage}%"
        PASSED_CHECKS+=("cpu_usage")
    fi
    
    # Check memory usage
    local mem_usage=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
    if (( $(echo "$mem_usage > 85" | bc -l) )); then
        log_warning "High memory usage: ${mem_usage}%"
        FAILED_CHECKS+=("memory_usage")
        HEALTH_STATUS=1
    else
        log_success "Memory usage is normal: ${mem_usage}%"
        PASSED_CHECKS+=("memory_usage")
    fi
    
    # Check disk usage
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    if [[ $disk_usage -gt 85 ]]; then
        log_warning "High disk usage: ${disk_usage}%"
        FAILED_CHECKS+=("disk_usage")
        HEALTH_STATUS=1
    else
        log_success "Disk usage is normal: ${disk_usage}%"
        PASSED_CHECKS+=("disk_usage")
    fi
}

# Check network connectivity
check_network() {
    log_info "Checking network connectivity..."
    
    # Check external connectivity
    if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
        log_success "External network connectivity is working"
        PASSED_CHECKS+=("external_network")
    else
        log_error "External network connectivity failed"
        FAILED_CHECKS+=("external_network")
        HEALTH_STATUS=1
    fi
    
    # Check DNS resolution
    if nslookup google.com > /dev/null 2>&1; then
        log_success "DNS resolution is working"
        PASSED_CHECKS+=("dns_resolution")
    else
        log_error "DNS resolution failed"
        FAILED_CHECKS+=("dns_resolution")
        HEALTH_STATUS=1
    fi
}

# Check SSL certificates (for production)
check_ssl_certificates() {
    if [[ "$ENVIRONMENT" != "production" ]]; then
        return 0
    fi
    
    log_info "Checking SSL certificates..."
    
    local domain="esg.gnanam.com"
    local cert_info=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
    
    if [[ -n "$cert_info" ]]; then
        log_success "SSL certificate is valid"
        PASSED_CHECKS+=("ssl_certificate")
    else
        log_error "SSL certificate check failed"
        FAILED_CHECKS+=("ssl_certificate")
        HEALTH_STATUS=1
    fi
}

# Generate health report
generate_report() {
    local report_file="${SCRIPT_DIR}/health-report-${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S).json"
    
    cat > "$report_file" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "environment": "$ENVIRONMENT",
  "overall_status": "$(if [[ $HEALTH_STATUS -eq 0 ]]; then echo "healthy"; else echo "unhealthy"; fi)",
  "checks": {
    "passed": $(printf '%s\n' "${PASSED_CHECKS[@]}" | jq -R . | jq -s .),
    "failed": $(printf '%s\n' "${FAILED_CHECKS[@]}" | jq -R . | jq -s .)
  },
  "summary": {
    "total_checks": $(( ${#PASSED_CHECKS[@]} + ${#FAILED_CHECKS[@]} )),
    "passed_checks": ${#PASSED_CHECKS[@]},
    "failed_checks": ${#FAILED_CHECKS[@]},
    "success_rate": "$(if [[ $(( ${#PASSED_CHECKS[@]} + ${#FAILED_CHECKS[@]} )) -gt 0 ]]; then echo "$(( ${#PASSED_CHECKS[@]} * 100 / (${#PASSED_CHECKS[@]} + ${#FAILED_CHECKS[@]}) ))%"; else echo "0%"; fi)"
  }
}
EOF

    log_info "Health report generated: $report_file"
}

# Main health check function
main() {
    parse_args "$@"
    
    log_info "Starting health checks for environment: $ENVIRONMENT"
    
    # Load configuration
    load_config
    
    # Run health checks
    check_all_services
    check_databases
    check_system_resources
    check_network
    check_ssl_certificates
    
    # Generate report
    generate_report
    
    # Print summary
    echo
    echo "=== Health Check Summary ==="
    echo "Environment: $ENVIRONMENT"
    echo "Overall Status: $(if [[ $HEALTH_STATUS -eq 0 ]]; then echo -e "${GREEN}HEALTHY${NC}"; else echo -e "${RED}UNHEALTHY${NC}"; fi)"
    echo "Passed Checks: ${#PASSED_CHECKS[@]}"
    echo "Failed Checks: ${#FAILED_CHECKS[@]}"
    
    if [[ ${#FAILED_CHECKS[@]} -gt 0 ]]; then
        echo
        echo "Failed Checks:"
        for check in "${FAILED_CHECKS[@]}"; do
            echo "  - $check"
        done
    fi
    
    if [[ $VERBOSE == true && ${#PASSED_CHECKS[@]} -gt 0 ]]; then
        echo
        echo "Passed Checks:"
        for check in "${PASSED_CHECKS[@]}"; do
            echo "  - $check"
        done
    fi
    
    echo
    echo "Success Rate: $(if [[ $(( ${#PASSED_CHECKS[@]} + ${#FAILED_CHECKS[@]} )) -gt 0 ]]; then echo "$(( ${#PASSED_CHECKS[@]} * 100 / (${#PASSED_CHECKS[@]} + ${#FAILED_CHECKS[@]}) ))%"; else echo "0%"; fi)"
    
    exit $HEALTH_STATUS
}

# Run main function with all arguments
main "$@" 