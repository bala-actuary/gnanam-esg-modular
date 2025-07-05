"""
Interest Rate Risk Module

This module provides interest rate risk models for the Gnanam ESG platform.
"""

from .models.hull_white_one_factor.model import HullWhiteOneFactorModel
from .models.hull_white_one_factor.pricing import price_zero_coupon_bond
from .models.hull_white_one_factor.data_structures import ModelParameters

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Main exports
__all__ = [
    "HullWhiteOneFactorModel",
    "price_zero_coupon_bond", 
    "ModelParameters"
]

def get_available_models():
    """Return list of available interest rate models."""
    return ["hull_white_one_factor"]

def create_model(model_name: str):
    """Create a model instance by name."""
    if model_name == "hull_white_one_factor":
        return HullWhiteOneFactorModel()
    else:
        raise ValueError(f"Unknown model: {model_name}")

def get_model_info(model_name: str):
    """Get information about a specific model."""
    models_info = {
        "hull_white_one_factor": {
            "name": "Hull-White One-Factor Model",
            "description": "Mean-reverting interest rate model with one factor",
            "parameters": ["alpha", "sigma"],
            "features": ["zero-coupon bond pricing", "path simulation", "calibration"]
        }
    }
    
    if model_name not in models_info:
        raise ValueError(f"Unknown model: {model_name}")
    
    return models_info[model_name] 