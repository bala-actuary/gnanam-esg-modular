"""
Monitoring and Logging System for RiskModels
Provides comprehensive application monitoring, metrics collection, and structured logging
"""

import logging
import time
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from contextlib import contextmanager
from dataclasses import dataclass
import json
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse

# =============================================================================
# PROMETHEUS METRICS
# =============================================================================

# Request metrics
REQUEST_COUNT = Counter('riskmodels_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('riskmodels_request_duration_seconds', 'Request duration', ['method', 'endpoint'])

# Model execution metrics
MODEL_EXECUTION_COUNT = Counter('riskmodels_model_executions_total', 'Model executions', ['model_name', 'status'])
MODEL_EXECUTION_DURATION = Histogram('riskmodels_model_execution_duration_seconds', 'Model execution time', ['model_name'])

# System metrics
SYSTEM_MEMORY_USAGE = Gauge('riskmodels_memory_usage_bytes', 'Memory usage in bytes')
SYSTEM_CPU_USAGE = Gauge('riskmodels_cpu_usage_percent', 'CPU usage percentage')
SYSTEM_DISK_USAGE = Gauge('riskmodels_disk_usage_bytes', 'Disk usage in bytes')

# Database metrics
DATABASE_CONNECTIONS = Gauge('riskmodels_database_connections', 'Active database connections')
DATABASE_QUERY_DURATION = Histogram('riskmodels_database_query_duration_seconds', 'Database query duration')

# Cache metrics
CACHE_HITS = Counter('riskmodels_cache_hits_total', 'Cache hits')
CACHE_MISSES = Counter('riskmodels_cache_misses_total', 'Cache misses')

# =============================================================================
# STRUCTURED LOGGING
# =============================================================================

@dataclass
class LogContext:
    """Context for structured logging"""
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    model_name: Optional[str] = None
    operation: Optional[str] = None
    duration: Optional[float] = None
    status: Optional[str] = None
    error: Optional[str] = None

class StructuredLogger:
    """Structured logging with context"""
    
    def __init__(self, name: str = "riskmodels"):
        self.logger = logging.getLogger(name)
        self.context = LogContext()
    
    def set_context(self, **kwargs):
        """Set logging context"""
        for key, value in kwargs.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)
    
    def _format_message(self, message: str, extra: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format log message with context"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "level": "INFO",
        }
        
        # Add context
        context_data = {k: v for k, v in self.context.__dict__.items() if v is not None}
        if context_data:
            log_data["context"] = context_data
        
        # Add extra data
        if extra:
            log_data["extra"] = extra
        
        return log_data
    
    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message"""
        log_data = self._format_message(message, extra)
        log_data["level"] = "INFO"
        self.logger.info(json.dumps(log_data))
    
    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message"""
        log_data = self._format_message(message, extra)
        log_data["level"] = "WARNING"
        self.logger.warning(json.dumps(log_data))
    
    def error(self, message: str, extra: Dict[str, Any] = None):
        """Log error message"""
        log_data = self._format_message(message, extra)
        log_data["level"] = "ERROR"
        self.logger.error(json.dumps(log_data))
    
    def critical(self, message: str, extra: Dict[str, Any] = None):
        """Log critical message"""
        log_data = self._format_message(message, extra)
        log_data["level"] = "CRITICAL"
        self.logger.critical(json.dumps(log_data))

# =============================================================================
# PERFORMANCE MONITORING
# =============================================================================

class PerformanceMonitor:
    """Performance monitoring and profiling"""
    
    def __init__(self):
        self.start_time = time.time()
        self.operation_times = {}
    
    @contextmanager
    def monitor_operation(self, operation_name: str):
        """Context manager for monitoring operation performance"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.operation_times[operation_name] = duration
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Update Prometheus metrics
            SYSTEM_MEMORY_USAGE.set(memory.used)
            SYSTEM_CPU_USAGE.set(cpu_percent)
            SYSTEM_DISK_USAGE.set(disk.used)
            
            return {
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "percent": memory.percent
                },
                "cpu": {
                    "percent": cpu_percent
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                },
                "uptime": time.time() - self.start_time
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        return {
            "operation_times": self.operation_times,
            "average_operation_time": sum(self.operation_times.values()) / len(self.operation_times) if self.operation_times else 0,
            "total_operations": len(self.operation_times)
        }

# =============================================================================
# HEALTH CHECKS
# =============================================================================

class HealthChecker:
    """Application health checking"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.checks = {}
    
    def register_check(self, name: str, check_func):
        """Register a health check"""
        self.checks[name] = check_func
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {}
        overall_status = "healthy"
        
        for name, check_func in self.checks.items():
            try:
                start_time = time.time()
                result = check_func()
                duration = time.time() - start_time
                
                results[name] = {
                    "status": "healthy" if result else "unhealthy",
                    "duration": duration,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                if not result:
                    overall_status = "unhealthy"
                    
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "duration": 0,
                    "timestamp": datetime.utcnow().isoformat()
                }
                overall_status = "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": results
        }

# =============================================================================
# MIDDLEWARE AND INTEGRATION
# =============================================================================

class MonitoringMiddleware:
    """FastAPI middleware for request monitoring"""
    
    def __init__(self, app, logger: StructuredLogger):
        self.app = app
        self.logger = logger
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        start_time = time.time()
        request = Request(scope, receive)
        
        # Set request context
        self.logger.set_context(
            request_id=str(hash(request.url)),
            operation=f"{request.method} {request.url.path}"
        )
        
        # Log request start
        self.logger.info("Request started", {
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": request.client.host if request.client else None
        })
        
        # Process request
        try:
            await self.app(scope, receive, send)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Update metrics
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=200  # We don't have access to response status here
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            # Log successful request
            self.logger.set_context(duration=duration, status="success")
            self.logger.info("Request completed successfully")
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Update error metrics
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            
            # Log error
            self.logger.set_context(duration=duration, status="error", error=str(e))
            self.logger.error("Request failed")
            raise

# =============================================================================
# METRICS ENDPOINTS
# =============================================================================

async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    return PlainTextResponse(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

async def health_endpoint(health_checker: HealthChecker):
    """Health check endpoint"""
    health_data = health_checker.run_health_checks()
    
    status_code = 200 if health_data["status"] == "healthy" else 503
    
    return {
        "status": health_data["status"],
        "timestamp": health_data["timestamp"],
        "checks": health_data["checks"]
    }

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def setup_logging(log_level: str = "INFO", log_file: str = "logs/riskmodels.log"):
    """Setup structured logging"""
    # Create logs directory
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(message)s',  # We handle formatting in StructuredLogger
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def create_monitoring_system() -> tuple[StructuredLogger, PerformanceMonitor, HealthChecker]:
    """Create monitoring system components"""
    logger = StructuredLogger("riskmodels")
    performance_monitor = PerformanceMonitor()
    health_checker = HealthChecker(logger)
    
    # Register default health checks
    health_checker.register_check("system", lambda: True)  # Placeholder
    health_checker.register_check("database", lambda: True)  # Placeholder
    health_checker.register_check("cache", lambda: True)  # Placeholder
    
    return logger, performance_monitor, health_checker

# Global instances
logger, performance_monitor, health_checker = create_monitoring_system() 