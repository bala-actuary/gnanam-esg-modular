"""
Liquidity Risk Module - Main Entry Point

This module provides liquidity risk models for the Gnanam ESG platform.
"""

from .models.cash_flow_shortfall_model.model import CashFlowShortfallModel
from .models.cash_flow_shortfall_model.data_structures import CashFlowInputData, CashFlowResults
from .models.cash_flow_shortfall_model.calculations import calculate_net_cash_flow, calculate_cumulative_cash_flow, identify_shortfalls

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "CashFlowShortfallModel",
    "CashFlowInputData",
    "CashFlowResults",
    "calculate_net_cash_flow",
    "calculate_cumulative_cash_flow",
    "identify_shortfalls"
]

def get_available_models():
    """Return list of available liquidity risk models."""
    return ["cash_flow_shortfall_model"]

def create_model(model_type: str):
    """Factory function to create liquidity risk models."""
    if model_type == "cash_flow_shortfall_model":
        return CashFlowShortfallModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_model_info(model_type: str):
    """Get information about a specific model."""
    if model_type == "cash_flow_shortfall_model":
        return {
            "name": "Cash Flow Shortfall Model",
            "description": "Model for assessing liquidity risk through cash flow analysis",
            "parameters": ["cash_inflows", "cash_outflows", "time_horizon", "frequency"],
            "outputs": ["net_cash_flow", "cumulative_cash_flow", "shortfall_identification"]
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_stress_scenarios():
    """Return predefined stress scenarios."""
    return {
        "base": {
            "name": "Base Scenario",
            "description": "Normal market conditions",
            "cash_flow_adjustment": 1.0
        },
        "adverse": {
            "name": "Adverse Scenario",
            "description": "Moderate stress conditions",
            "cash_flow_adjustment": 0.8
        },
        "severe": {
            "name": "Severe Scenario",
            "description": "Extreme stress conditions",
            "cash_flow_adjustment": 0.5
        }
    }

def get_regulatory_requirements():
    """Return regulatory liquidity requirements."""
    return {
        "LCR": {
            "name": "Liquidity Coverage Ratio",
            "minimum_ratio": 1.0,
            "description": "High-quality liquid assets / Net cash outflows"
        },
        "NSFR": {
            "name": "Net Stable Funding Ratio",
            "minimum_ratio": 1.0,
            "description": "Available stable funding / Required stable funding"
        }
    }

if __name__ == "__main__":
    # Example usage
    print("Liquidity Risk Module - Example Usage")
    print("=" * 45)
    
    # Create cash flow shortfall model
    model = CashFlowShortfallModel()
    
    # Calculate cash flow analysis
    try:
        results = model.calculate()
        print(f"Analysis completed successfully")
        print(f"Results saved to: {model.output_dir}")
        print(f"Number of periods analyzed: {len(results.results_df)}")
        
        # Show summary statistics
        if len(results.results_df) > 0:
            net_cash_flows = results.results_df["Net_Cash_Flow"]
            cumulative_cash_flows = results.results_df["Cumulative_Cash_Flow"]
            shortfalls = results.results_df["Shortfall"]
            
            print(f"Total net cash flow: {net_cash_flows.sum():.2f}")
            print(f"Final cumulative cash flow: {cumulative_cash_flows.iloc[-1]:.2f}")
            print(f"Number of shortfall periods: {shortfalls.sum()}")
        
    except FileNotFoundError:
        print("Input data files not found. Please ensure cash_flows.csv exists in the input directory.")
        print("Example data structure:")
        print("- Date: 2024-01-01, 2024-02-01, 2024-03-01, ...")
        print("- Inflows: 50000, 75000, 100000, ...")
        print("- Outflows: 80000, 90000, 110000, ...")
    except Exception as e:
        print(f"Error during calculation: {e}")
        print("Please check model parameters and dependencies.") 