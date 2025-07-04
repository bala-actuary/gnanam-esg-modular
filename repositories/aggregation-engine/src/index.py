"""
Aggregation Engine Module - Main Entry Point

This module provides the Risk Aggregation and Distribution Framework (RADF) for the Gnanam ESG platform.
"""

from .orchestrator import RADFOrchestrator
from .config import load_config, validate_config

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "RADFOrchestrator",
    "load_config",
    "validate_config"
]

def get_orchestrator(config_path: str = "config.yaml"):
    """Get the RADF orchestrator instance."""
    return RADFOrchestrator(config_path)

def get_engine_info():
    """Get information about the aggregation engine."""
    return {
        "name": "RADF Aggregation Engine",
        "description": "Risk Aggregation and Distribution Framework",
        "version": __version__,
        "capabilities": [
            "multi-risk scenario aggregation",
            "portfolio risk distribution",
            "correlation matrix integration",
            "Monte Carlo simulation",
            "stress testing",
            "plugin system"
        ]
    }

def get_available_methods():
    """Return available aggregation methods."""
    return {
        "monte_carlo": {
            "name": "Monte Carlo Simulation",
            "description": "Stochastic scenario generation with correlation",
            "parameters": ["num_scenarios", "correlation_matrix", "confidence_level"]
        },
        "analytical": {
            "name": "Analytical Aggregation",
            "description": "Variance-covariance approach",
            "parameters": ["portfolio_weights", "covariance_matrix"]
        },
        "historical": {
            "name": "Historical Simulation",
            "description": "Historical scenario analysis",
            "parameters": ["historical_data", "window_size"]
        },
        "copula": {
            "name": "Copula-based Aggregation",
            "description": "Flexible dependency modeling",
            "parameters": ["copula_type", "marginal_distributions"]
        }
    }

def get_risk_metrics():
    """Return available risk metrics."""
    return {
        "var": {
            "name": "Value at Risk (VaR)",
            "description": "Maximum expected loss at confidence level",
            "unit": "currency"
        },
        "es": {
            "name": "Expected Shortfall (ES)",
            "description": "Average loss beyond VaR",
            "unit": "currency"
        },
        "volatility": {
            "name": "Portfolio Volatility",
            "description": "Standard deviation of portfolio returns",
            "unit": "percentage"
        },
        "risk_contribution": {
            "name": "Risk Contribution",
            "description": "Individual asset risk contribution",
            "unit": "currency"
        },
        "diversification_ratio": {
            "name": "Diversification Ratio",
            "description": "Portfolio diversification measure",
            "unit": "ratio"
        }
    }

if __name__ == "__main__":
    # Example usage
    print("RADF Aggregation Engine - Example Usage")
    print("=" * 45)
    
    # Get engine information
    info = get_engine_info()
    print(f"Engine: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Description: {info['description']}")
    
    # Show available methods
    methods = get_available_methods()
    print(f"\nAvailable Aggregation Methods:")
    for method_id, method_info in methods.items():
        print(f"- {method_info['name']}: {method_info['description']}")
    
    # Show available metrics
    metrics = get_risk_metrics()
    print(f"\nAvailable Risk Metrics:")
    for metric_id, metric_info in metrics.items():
        print(f"- {metric_info['name']}: {metric_info['description']}")
    
    print(f"\nUse: python src/__main__.py --help for command line options")
    print(f"Or: npm run dev for development mode") 