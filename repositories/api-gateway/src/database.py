"""
Database Connection Management for RiskModels
Supports PostgreSQL and SQLite with connection pooling
"""

import logging
from typing import Optional
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from config import settings

logger = logging.getLogger(__name__)

# Database engine and session factory
engine: Optional[create_engine] = None
SessionLocal: Optional[sessionmaker] = None
Base = declarative_base()

def get_database_url() -> str:
    """Get database URL from settings"""
    if settings.database_url:
        return settings.database_url
    
    # Default to SQLite for development
    return "sqlite:///./riskmodels.db"

def create_database_engine():
    """Create database engine with connection pooling"""
    global engine, SessionLocal
    
    database_url = get_database_url()
    
    # Engine configuration
    engine_kwargs = {
        "echo": settings.debug,  # Log SQL queries in debug mode
        "pool_pre_ping": True,   # Verify connections before use
    }
    
    # Add connection pooling for PostgreSQL
    if database_url.startswith("postgresql"):
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": settings.database_pool_size,
            "max_overflow": settings.database_max_overflow,
            "pool_timeout": settings.database_pool_timeout,
            "pool_recycle": 3600,  # Recycle connections every hour
        })
    
    try:
        engine = create_engine(database_url, **engine_kwargs)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        logger.info(f"Database engine created successfully: {database_url}")
        
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            logger.info("Database connection test successful")
            
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise

def get_db() -> Session:
    """Get database session"""
    if not SessionLocal:
        create_database_engine()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables"""
    if not engine:
        create_database_engine()
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

def check_database_health() -> bool:
    """Check database health"""
    try:
        if not engine:
            create_database_engine()
        
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

# Database models (basic structure for future use)
class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    # This is a placeholder - implement full model as needed
    pass

class ModelRun(Base):
    """Model run tracking"""
    __tablename__ = "model_runs"
    
    # This is a placeholder - implement full model as needed
    pass

# Initialize database on module import
try:
    create_database_engine()
except Exception as e:
    logger.warning(f"Database initialization failed: {e}")
    logger.info("Application will run without database support") 