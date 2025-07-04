"""
Configuration Management for RiskModels FastAPI Application
Handles environment variables, validation, and default settings
"""

import os
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # =============================================================================
    # SECURITY SETTINGS
    # =============================================================================
    secret_key: str = Field(env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    max_requests_per_minute: int = Field(default=100, env="MAX_REQUESTS_PER_MINUTE")
    max_requests_per_hour: int = Field(default=1000, env="MAX_REQUESTS_PER_HOUR")
    
    # =============================================================================
    # APPLICATION SETTINGS
    # =============================================================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # API Settings
    api_host: str = Field(default="0.0.0.0", env="HOST")
    api_port: int = Field(default=8000, env="PORT")
    workers: int = 1
    
    # CORS Settings
    allowed_origins: List[str] = Field(default=["http://localhost:3000"], env="ALLOWED_ORIGINS")
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: List[str] = ["*"]
    
    # =============================================================================
    # DATABASE SETTINGS
    # =============================================================================
    database_url: str = Field(env="DATABASE_URL")
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    database_pool_timeout: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    
    # =============================================================================
    # CACHE & SESSION SETTINGS
    # =============================================================================
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_ssl: bool = False
    
    session_secret_key: str = "your-session-secret-key-here"
    session_expire_minutes: int = 1440
    
    # =============================================================================
    # MONITORING & LOGGING
    # =============================================================================
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    enable_health_checks: bool = Field(default=True, env="ENABLE_HEALTH_CHECKS")
    enable_audit_logging: bool = True
    audit_log_file: str = "audit.log"
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # External monitoring
    sentry_dsn: Optional[str] = None
    new_relic_license_key: Optional[str] = None
    
    # =============================================================================
    # EXTERNAL SERVICES
    # =============================================================================
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
    
    # Email settings
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True
    
    # Storage settings
    storage_type: str = "local"
    storage_path: str = "./data/uploads"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_s3_bucket: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # =============================================================================
    # MODEL-SPECIFIC SETTINGS
    # =============================================================================
    default_num_paths: int = 1000
    default_time_steps: int = 252
    max_computation_time: int = 300
    enable_model_caching: bool = True
    
    # Hull-White model settings
    hw_default_alpha: float = 0.1
    hw_default_sigma: float = 0.02
    
    # GBM model settings
    gbm_default_mu: float = 0.05
    gbm_default_sigma: float = 0.2
    
    # =============================================================================
    # PERFORMANCE & SCALING
    # =============================================================================
    max_concurrent_requests: int = 100
    request_timeout: int = 60
    enable_rate_limiting: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    max_memory_usage: int = 80
    enable_memory_monitoring: bool = True
    
    # =============================================================================
    # DEVELOPMENT SETTINGS
    # =============================================================================
    enable_swagger_ui: bool = False
    enable_reload: bool = False
    
    # Application Settings
    app_name: str = "RiskModels"
    version: str = "1.0.0"
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Cache Settings
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    cache_ttl_seconds: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    enable_memory_cache: bool = Field(default=True, env="ENABLE_MEMORY_CACHE")
    enable_redis_cache: bool = Field(default=False, env="ENABLE_REDIS_CACHE")
    
    # Model Settings
    default_model_timeout: int = Field(default=300, env="DEFAULT_MODEL_TIMEOUT")  # 5 minutes
    max_concurrent_models: int = Field(default=5, env="MAX_CONCURRENT_MODELS")
    model_cache_enabled: bool = Field(default=True, env="MODEL_CACHE_ENABLED")
    
    # API Settings
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    enable_docs: bool = Field(default=True, env="ENABLE_DOCS")
    enable_openapi: bool = Field(default=True, env="ENABLE_OPENAPI")
    
    # Performance Settings
    max_workers: int = Field(default=10, env="MAX_WORKERS")
    enable_async_processing: bool = Field(default=True, env="ENABLE_ASYNC_PROCESSING")
    enable_connection_pooling: bool = Field(default=True, env="ENABLE_CONNECTION_POOLING")
    
    # File Upload Settings
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    allowed_file_types: List[str] = Field(default=[".csv", ".xlsx", ".json"], env="ALLOWED_FILE_TYPES")
    upload_directory: str = Field(default="uploads", env="UPLOAD_DIRECTORY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator("secret_key")
    def validate_secret_key(cls, v):
        if v == "CHANGE_THIS_SECRET_KEY" and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("SECRET_KEY must be changed in production")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("allowed_origins", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            # Handle JSON string format
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    @validator("environment")
    def validate_environment(cls, v):
        valid_environments = ["development", "staging", "production", "testing"]
        if v not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

def setup_logging():
    """Setup application logging based on configuration"""
    log_config = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    # Configure root logger
    logging.basicConfig(
        level=log_config.get(settings.log_level, logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.audit_log_file) if settings.enable_audit_logging else logging.NullHandler(),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)

def validate_production_settings():
    """Validate critical settings for production deployment"""
    errors = []
    
    if settings.environment == "production":
        if settings.secret_key == "CHANGE_THIS_SECRET_KEY":
            errors.append("SECRET_KEY must be changed in production")
        
        if settings.debug:
            errors.append("DEBUG should be False in production")
        
        if not settings.database_url:
            errors.append("DATABASE_URL must be set in production")
        
        if not settings.redis_url:
            errors.append("REDIS_URL should be set in production for caching")
    
    if errors:
        raise ValueError(f"Production validation failed: {'; '.join(errors)}")

def get_database_config():
    """Get database configuration"""
    return {
        "url": settings.database_url,
        "pool_size": settings.database_pool_size,
        "max_overflow": settings.database_max_overflow,
        "pool_timeout": settings.database_pool_timeout
    }

def get_redis_config():
    """Get Redis configuration"""
    return {
        "url": settings.redis_url,
        "db": settings.redis_db,
        "password": settings.redis_password,
        "ssl": settings.redis_ssl
    }

def get_cors_config():
    """Get CORS configuration"""
    return {
        "allow_origins": settings.allowed_origins,
        "allow_methods": settings.allowed_methods,
        "allow_headers": settings.allowed_headers
    }

def get_model_config():
    """Get model-specific configuration"""
    return {
        "default_num_paths": settings.default_num_paths,
        "default_time_steps": settings.default_time_steps,
        "max_computation_time": settings.max_computation_time,
        "enable_caching": settings.enable_model_caching,
        "hw_alpha": settings.hw_default_alpha,
        "hw_sigma": settings.hw_default_sigma,
        "gbm_mu": settings.gbm_default_mu,
        "gbm_sigma": settings.gbm_default_sigma
    }

# Initialize logging on module import
setup_logging() 