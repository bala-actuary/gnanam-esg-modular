"""
Foreign Exchange Risk Module - Main Entry Point

This module provides foreign exchange risk models for the Gnanam ESG platform.
"""

from .models.gbm_model.model import FXGBMModel
from .models.gbm_model.data_structures import FXGBMInputData, FXGBMSimulationResult
from .models.gbm_model.formulas import fx_gbm_step

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "FXGBMModel",
    "FXGBMInputData",
    "FXGBMSimulationResult",
    "fx_gbm_step"
]

def get_available_models():
    """Return list of available foreign exchange risk models."""
    return ["fx_gbm_model"]

def create_model(model_type: str):
    """Factory function to create foreign exchange risk models."""
    if model_type == "fx_gbm_model":
        return FXGBMModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_model_info(model_type: str):
    """Get information about a specific model."""
    if model_type == "fx_gbm_model":
        return {
            "name": "FX Geometric Brownian Motion Model",
            "description": "Stochastic model for foreign exchange rate simulation",
            "parameters": ["initial_exchange_rate", "domestic_risk_free_rate", "foreign_risk_free_rate", "volatility", "time_horizon", "num_time_steps", "num_paths"],
            "outputs": ["exchange_rate_paths", "time_grid"]
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_supported_currency_pairs():
    """Return list of supported currency pairs."""
    return [
        "EUR/USD",
        "GBP/USD", 
        "USD/JPY",
        "USD/CHF",
        "AUD/USD",
        "USD/CAD",
        "NZD/USD",
        "EUR/GBP",
        "EUR/JPY",
        "GBP/JPY"
    ]

if __name__ == "__main__":
    # Example usage
    print("Foreign Exchange Risk Module - Example Usage")
    print("=" * 50)
    
    # Create FX GBM model
    model = FXGBMModel()
    
    # Define scenario parameters for EUR/USD
    scenario_definition = {
        "initial_exchange_rate": 1.2000,  # EUR/USD exchange rate
        "domestic_risk_free_rate": 0.05,  # USD rate
        "foreign_risk_free_rate": 0.03,   # EUR rate
        "volatility": 0.15,
        "time_horizon": 1.0,
        "num_time_steps": 252,
        "num_paths": 1000
    }
    
    # Simulate exchange rate paths
    try:
        simulation_result = model.simulate(scenario_definition)
        print(f"Generated {simulation_result.paths.shape[1]} FX rate paths")
        print(f"Time steps: {len(simulation_result.time_grid)}")
        print(f"Final rates range: {simulation_result.paths[:, -1].min():.4f} - {simulation_result.paths[:, -1].max():.4f}")
        
    except FileNotFoundError:
        print("Input data files not found. Please ensure fx_gbm_parameters.csv exists in the input directory.")
        print("Example data structure:")
        print("- initial_exchange_rate: 1.2000")
        print("- domestic_risk_free_rate: 0.05")
        print("- foreign_risk_free_rate: 0.03")
        print("- volatility: 0.15")
        print("- time_horizon: 1.0")
        print("- num_time_steps: 252")
        print("- num_paths: 1000")
    except Exception as e:
        print(f"Error during simulation: {e}")
        print("Please check model parameters and dependencies.") 