"""
Monitoring Dashboard Module - Main Entry Point

This module provides the monitoring dashboard service for the Gnanam ESG platform.
"""

from .monitoring import (
    StructuredLogger, 
    PerformanceMonitor, 
    HealthChecker, 
    MonitoringMiddleware,
    create_monitoring_system
)

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "StructuredLogger",
    "PerformanceMonitor", 
    "HealthChecker",
    "MonitoringMiddleware",
    "create_monitoring_system"
]

def get_monitoring_service():
    """Get the monitoring service instance."""
    return create_monitoring_system()

def get_dashboard_info():
    """Get information about the monitoring dashboard."""
    return {
        "name": "ESG Monitoring Dashboard",
        "description": "Real-time monitoring and visualization service",
        "version": __version__,
        "capabilities": [
            "real-time system monitoring",
            "risk model performance tracking",
            "interactive dashboards",
            "alerting and notifications",
            "performance metrics",
            "data visualization"
        ]
    }

def get_available_dashboards():
    """Return available dashboard types."""
    return {
        "system_health": {
            "name": "System Health Dashboard",
            "description": "Real-time system status and performance",
            "metrics": ["cpu_usage", "memory_usage", "disk_usage", "network_io"]
        },
        "risk_analytics": {
            "name": "Risk Analytics Dashboard",
            "description": "Portfolio risk metrics and analysis",
            "metrics": ["var", "expected_shortfall", "volatility", "correlation"]
        },
        "performance": {
            "name": "Performance Dashboard",
            "description": "API and service performance metrics",
            "metrics": ["response_time", "throughput", "error_rate", "availability"]
        },
        "aggregation": {
            "name": "Aggregation Dashboard",
            "description": "RADF workflow monitoring",
            "metrics": ["workflow_status", "execution_time", "success_rate"]
        }
    }

def get_alert_channels():
    """Return available alert notification channels."""
    return {
        "email": {
            "name": "Email Notifications",
            "description": "SMTP-based email alerts",
            "config": ["smtp_server", "smtp_port", "username", "password"]
        },
        "slack": {
            "name": "Slack Notifications",
            "description": "Slack webhook integration",
            "config": ["webhook_url", "channel", "username"]
        },
        "webhook": {
            "name": "Webhook Notifications",
            "description": "Custom webhook endpoints",
            "config": ["webhook_url", "headers", "timeout"]
        },
        "pagerduty": {
            "name": "PagerDuty Integration",
            "description": "Incident management integration",
            "config": ["api_key", "service_id", "urgency"]
        }
    }

def get_visualization_types():
    """Return available visualization types."""
    return {
        "time_series": {
            "name": "Time Series Charts",
            "description": "Historical trend analysis",
            "use_cases": ["performance_trends", "risk_metrics_history"]
        },
        "heatmap": {
            "name": "Heatmaps",
            "description": "Correlation and risk matrices",
            "use_cases": ["correlation_matrix", "risk_heatmap"]
        },
        "scatter": {
            "name": "Scatter Plots",
            "description": "Risk factor relationships",
            "use_cases": ["risk_factor_analysis", "portfolio_scatter"]
        },
        "gauge": {
            "name": "Gauge Charts",
            "description": "Real-time metrics",
            "use_cases": ["system_health", "risk_limits"]
        },
        "network": {
            "name": "Network Graphs",
            "description": "System dependencies",
            "use_cases": ["service_dependencies", "risk_flows"]
        }
    }

if __name__ == "__main__":
    # Example usage
    print("ESG Monitoring Dashboard - Example Usage")
    print("=" * 45)
    
    # Get dashboard information
    info = get_dashboard_info()
    print(f"Dashboard: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Description: {info['description']}")
    
    # Show available dashboards
    dashboards = get_available_dashboards()
    print(f"\nAvailable Dashboards:")
    for dashboard_id, dashboard_info in dashboards.items():
        print(f"- {dashboard_info['name']}: {dashboard_info['description']}")
    
    # Show alert channels
    channels = get_alert_channels()
    print(f"\nAlert Channels:")
    for channel_id, channel_info in channels.items():
        print(f"- {channel_info['name']}: {channel_info['description']}")
    
    # Show visualization types
    viz_types = get_visualization_types()
    print(f"\nVisualization Types:")
    for viz_id, viz_info in viz_types.items():
        print(f"- {viz_info['name']}: {viz_info['description']}")
    
    print(f"\nUse: npm run dashboard to start Streamlit dashboard")
    print(f"Or: npm run dev for development mode") 