"""
Credit Risk Module - Main Entry Point

This module provides credit risk models for the Gnanam ESG platform.
"""

from .models.merton_model.model import MertonModel
from .models.merton_model.data_structures import (
    MertonInputData,
    CalibratedMertonModel,
    MertonOutputResults,
    MertonSimulationResult
)
from .models.merton_model.calculations import calculate_default_probability, calculate_credit_spread

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "MertonModel",
    "MertonInputData",
    "CalibratedMertonModel", 
    "MertonOutputResults",
    "MertonSimulationResult",
    "calculate_default_probability",
    "calculate_credit_spread"
]

def get_available_models():
    """Return list of available credit risk models."""
    return ["merton_model"]

def create_model(model_type: str):
    """Factory function to create credit risk models."""
    if model_type == "merton_model":
        return MertonModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_model_info(model_type: str):
    """Get information about a specific model."""
    if model_type == "merton_model":
        return {
            "name": "Merton Structural Model",
            "description": "Structural model for default probability estimation",
            "parameters": ["equity_value", "equity_volatility", "face_value_debt", "time_to_maturity", "risk_free_rate"],
            "outputs": ["default_probability", "credit_spread", "asset_value", "asset_volatility"]
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")

if __name__ == "__main__":
    # Example usage
    print("Credit Risk Module - Example Usage")
    print("=" * 40)
    
    # Create Merton model
    model = MertonModel()
    
    # Calibrate the model (this loads data from input files)
    try:
        calibrated_model = model.calibrate()
        print(f"Calibrated Asset Value: {calibrated_model.asset_value:.2f}")
        print(f"Calibrated Asset Volatility: {calibrated_model.asset_volatility:.4f}")
        
        # Calculate results
        results = model.calculate_results(calibrated_model)
        print(f"Default Probability: {results.default_probability:.4f}")
        print(f"Credit Spread: {results.credit_spread:.4f}")
        
    except FileNotFoundError:
        print("Input data files not found. Please ensure firm_data.csv exists in the input directory.")
        print("Example data structure:")
        print("- equity_value: 1000000")
        print("- equity_volatility: 0.30")
        print("- face_value_debt: 800000")
        print("- time_to_maturity: 1.0")
        print("- risk_free_rate: 0.05") 