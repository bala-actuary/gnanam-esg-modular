"""
Counterparty Risk Module - Main Entry Point

This module provides counterparty risk models for the Gnanam ESG platform.
"""

from .models.basic_exposure_model.model import BasicExposureModel
from .models.basic_exposure_model.data_structures import TradePortfolioInputData, ExposureResults
from .models.basic_exposure_model.calculations import calculate_counterparty_exposures

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "BasicExposureModel",
    "TradePortfolioInputData",
    "ExposureResults",
    "calculate_counterparty_exposures"
]

def get_available_models():
    """Return list of available counterparty risk models."""
    return ["basic_exposure_model"]

def create_model(model_type: str):
    """Factory function to create counterparty risk models."""
    if model_type == "basic_exposure_model":
        return BasicExposureModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_model_info(model_type: str):
    """Get information about a specific model."""
    if model_type == "basic_exposure_model":
        return {
            "name": "Basic Exposure Model",
            "description": "Model for calculating counterparty credit exposure and risk metrics",
            "parameters": ["counterparty_id", "trade_id", "market_value"],
            "outputs": ["total_exposure", "positive_exposure", "negative_exposure"]
        }
    else:
        raise ValueError(f"Unknown model type: {model_type}")

def get_risk_metrics():
    """Return available counterparty risk metrics."""
    return {
        "total_exposure": {
            "name": "Total Exposure",
            "description": "Total market value exposure to counterparty",
            "unit": "currency"
        },
        "positive_exposure": {
            "name": "Positive Exposure",
            "description": "Sum of positive market values",
            "unit": "currency"
        },
        "negative_exposure": {
            "name": "Negative Exposure",
            "description": "Sum of negative market values",
            "unit": "currency"
        },
        "net_exposure": {
            "name": "Net Exposure",
            "description": "Net exposure (positive - negative)",
            "unit": "currency"
        }
    }

def get_regulatory_frameworks():
    """Return regulatory frameworks for counterparty risk."""
    return {
        "basel_iii": {
            "name": "Basel III",
            "description": "Credit risk capital requirements",
            "components": ["PD", "LGD", "EAD", "M"]
        },
        "ifrs_9": {
            "name": "IFRS 9",
            "description": "Expected credit loss provisioning",
            "components": ["12-month ECL", "Lifetime ECL"]
        },
        "cva_capital": {
            "name": "CVA Capital",
            "description": "Credit value adjustment capital",
            "components": ["CVA risk capital", "Default risk capital"]
        }
    }

if __name__ == "__main__":
    # Example usage
    print("Counterparty Risk Module - Example Usage")
    print("=" * 50)
    
    # Create basic exposure model
    model = BasicExposureModel()
    
    # Calculate exposure analysis
    try:
        results = model.calculate()
        print(f"Analysis completed successfully")
        print(f"Results saved to: {model.output_dir}")
        print(f"Number of counterparties analyzed: {len(results.results_df)}")
        
        # Show summary statistics
        if len(results.results_df) > 0:
            total_exposures = results.results_df["Total_Exposure"]
            positive_exposures = results.results_df["Positive_Exposure"]
            negative_exposures = results.results_df["Negative_Exposure"]
            
            print(f"Total portfolio exposure: {total_exposures.sum():.2f}")
            print(f"Total positive exposure: {positive_exposures.sum():.2f}")
            print(f"Total negative exposure: {negative_exposures.sum():.2f}")
        
    except FileNotFoundError:
        print("Input data files not found. Please ensure trade_portfolio.csv exists in the input directory.")
        print("Example data structure:")
        print("- Counterparty_ID: CP001, CP002, CP003, ...")
        print("- Trade_ID: T001, T002, T003, ...")
        print("- Market_Value: 100000, -50000, 75000, ...")
    except Exception as e:
        print(f"Error during calculation: {e}")
        print("Please check model parameters and dependencies.") 