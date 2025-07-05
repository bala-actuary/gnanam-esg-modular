from . import calculations
from .data_structures import CashFlowInputData, CashFlowResults
import pandas as pd
import os


# Assume ModelInterface is imported from the Core Engine
# For now, we'll define a dummy ModelInterface for development purposes.
class ModelInterface:
    def get_name(self) -> str:
        raise NotImplementedError

    def get_required_risk_factors(self) -> list[str]:
        raise NotImplementedError

    def calibrate(self, initial_zero_coupon_bond_pricer, market_swaptions):
        raise NotImplementedError

    def simulate(self, calibrated_model, scenario_definition, correlated_shocks):
        raise NotImplementedError

    def train(self, historical_data):
        raise NotImplementedError

    def predict(self, input_features):
        raise NotImplementedError


class CashFlowShortfallModel(ModelInterface):

    def __init__(
        self,
        input_dir="RiskModels/data/inputs/liquidity_model",
        output_dir="RiskModels/data/outputs/liquidity_model",
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "cash_flow_shortfall_model"

    def get_required_risk_factors(self) -> list[str]:
        return ["cash_inflows", "cash_outflows", "time_horizon", "frequency"]

    # --- Public Methods (for file-based I/O and convenience) ---

    def calculate(
        self, scenario_definition: dict = None, plot_options: dict = None
    ) -> CashFlowResults:
        input_data = (
            self._load_and_prepare_data()
        )  # scenario_definition can be used for filtering/transforming data
        results = self._calculate_logic(input_data)

        # Save results to CSV
        output_path_csv = os.path.join(self.output_dir, "cash_flow_results.csv")
        results.results_df.to_csv(output_path_csv, index=False)

        # Generate and save plots based on plot_options
        if plot_options is None:
            plot_options = {
                "net_cash_flow_plot": {"enabled": True},
                "cumulative_cash_flow_plot": {"enabled": True},
            }

        from visualization.plotter import plot_net_cash_flow, plot_cumulative_cash_flow

        if plot_options.get("net_cash_flow_plot", {}).get("enabled", False):
            output_filename = plot_options["net_cash_flow_plot"].get(
                "output_filename", "net_cash_flow_plot.html"
            )
            plot_net_cash_flow(
                results.results_df, os.path.join(self.output_dir, output_filename)
            )

        if plot_options.get("cumulative_cash_flow_plot", {}).get("enabled", False):
            output_filename = plot_options["cumulative_cash_flow_plot"].get(
                "output_filename", "cumulative_cash_flow_plot.html"
            )
            plot_cumulative_cash_flow(
                results.results_df, os.path.join(self.output_dir, output_filename)
            )

        return results

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self) -> CashFlowInputData:
        cash_flows_path = os.path.join(self.input_dir, "cash_flows.csv")
        df = pd.read_csv(cash_flows_path, parse_dates=["Date"])
        return CashFlowInputData(cash_flows_df=df)

    def _calculate_logic(self, input_data: CashFlowInputData) -> CashFlowResults:
        df = input_data.cash_flows_df.copy()
        df["Net_Cash_Flow"] = calculations.calculate_net_cash_flow(
            df["Inflows"], df["Outflows"]
        )
        df["Cumulative_Cash_Flow"] = calculations.calculate_cumulative_cash_flow(
            df["Net_Cash_Flow"]
        )
        df["Shortfall"] = calculations.identify_shortfalls(df["Cumulative_Cash_Flow"])
        return CashFlowResults(results_df=df)

    def calibrate(self, *args, **kwargs):
        raise NotImplementedError(
            "Cash Flow Shortfall Model does not require calibration."
        )

    def simulate(self, *args, **kwargs):
        raise NotImplementedError(
            "Cash Flow Shortfall Model performs calculations, not simulations."
        )

    def train(self, historical_data):
        raise NotImplementedError(
            "The Cash Flow Shortfall Model is a deterministic model and does not require training."
        )

    def predict(self, input_features):
        raise NotImplementedError(
            "The Cash Flow Shortfall Model uses 'calculate' for its primary operations, not 'predict'."
        )
