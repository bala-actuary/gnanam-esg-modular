"""
Inflation Risk Module - Main Entry Point

This module provides inflation risk models for the Gnanam ESG platform.
"""

from .models.mean_reverting_model.model import MeanRevertingInflationModel
from .models.mean_reverting_model.data_structures import InflationInputData, InflationSimulationResult
from .models.mean_reverting_model.formulas import mean_reverting_step

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "MeanRevertingInflationModel",
    "InflationInputData",
    "InflationSimulationResult",
    "mean_reverting_step"
]

def get_available_models():
    """Return list of available inflation risk models."""
    return ["mean_reverting_inflation_model"]

def create_model(model_type: str):
    """Factory function to create inflation risk models."""
    if model_type == "mean_reverting_inflation_model":
        return MeanRevertingInflationModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_model_info(model_type: str):
    """Get information about a specific model."""
    if model_type == "mean_reverting_inflation_model":
        return {
            "name": "Mean Reverting Inflation Model (Ornstein-Uhlenbeck)",
            "description": "Stochastic model for inflation rate simulation with mean reversion",
            "parameters": ["initial_inflation_rate", "long_term_mean_inflation_rate", "mean_reversion_speed", "volatility", "time_horizon", "num_time_steps", "num_paths"],
            "outputs": ["inflation_rate_paths", "time_grid"]
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_central_bank_targets():
    """Return central bank inflation targets."""
    return {
        "Federal Reserve": 0.02,
        "European Central Bank": 0.02,
        "Bank of England": 0.02,
        "Bank of Japan": 0.02,
        "Reserve Bank of Australia": 0.025,
        "Bank of Canada": 0.02
    }

if __name__ == "__main__":
    # Example usage
    print("Inflation Risk Module - Example Usage")
    print("=" * 45)
    
    # Create mean reverting model
    model = MeanRevertingInflationModel()
    
    # Define scenario parameters
    scenario_definition = {
        "initial_inflation_rate": 0.025,  # 2.5% initial inflation
        "long_term_mean_inflation_rate": 0.02,  # 2% long-term target (Fed target)
        "mean_reversion_speed": 0.1,      # Speed of mean reversion
        "volatility": 0.05,               # Inflation volatility
        "time_horizon": 10.0,             # 10-year horizon
        "num_time_steps": 120,            # Monthly steps
        "num_paths": 1000
    }
    
    # Simulate inflation rate paths
    try:
        simulation_result = model.simulate(scenario_definition)
        print(f"Generated {simulation_result.paths.shape[1]} inflation rate paths")
        print(f"Time steps: {len(simulation_result.time_grid)}")
        print(f"Final rates range: {simulation_result.paths[:, -1].min():.4f} - {simulation_result.paths[:, -1].max():.4f}")
        
    except FileNotFoundError:
        print("Input data files not found. Please ensure inflation_parameters.csv exists in the input directory.")
        print("Example data structure:")
        print("- initial_inflation_rate: 0.025")
        print("- long_term_mean_inflation_rate: 0.02")
        print("- mean_reversion_speed: 0.1")
        print("- volatility: 0.05")
        print("- time_horizon: 10.0")
        print("- num_time_steps: 120")
        print("- num_paths: 1000")
    except Exception as e:
        print(f"Error during simulation: {e}")
        print("Please check model parameters and dependencies.") 