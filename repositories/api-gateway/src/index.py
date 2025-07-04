"""
API Gateway Module - Main Entry Point

This module provides the main API Gateway service for the Gnanam ESG platform.
"""

from .main import app
from .config import get_settings

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main application
__all__ = ["app", "get_settings"]

def get_app():
    """Get the FastAPI application instance."""
    return app

def get_health_status():
    """Get the current health status of the API Gateway."""
    return {
        "status": "healthy",
        "version": __version__,
        "service": "api-gateway"
    }

def get_service_info():
    """Get information about the API Gateway service."""
    return {
        "name": "API Gateway",
        "description": "Main entry point for Gnanam ESG platform",
        "version": __version__,
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "metrics": "/metrics",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    # Run the application using the main.py entry point
    print("Starting API Gateway...")
    print("Use: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
    print("Or: npm run dev") 