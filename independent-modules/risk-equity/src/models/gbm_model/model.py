from . import formulas
from .data_structures import GBMInputData, GBMSimulationResult
import pandas as pd
import os
import numpy as np


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


class GBMModel(ModelInterface):

    def __init__(
        self,
        input_dir="RiskModels/data/inputs/gbm_model",
        output_dir="RiskModels/data/outputs/gbm_model",
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "gbm_model"

    def get_required_risk_factors(self) -> list[str]:
        return [
            "initial_price",
            "expected_return",
            "volatility",
            "time_horizon",
            "num_time_steps",
            "num_paths",
        ]

    # --- Public Methods (for file-based I/O and convenience) ---

    def simulate(
        self,
        scenario_definition: dict,
        correlated_shocks=None,
        plot_options: dict = None,
    ) -> GBMSimulationResult:
        input_data = self._load_and_prepare_data(
            scenario_definition
        )  # scenario_definition can override file data
        simulation_result = self._simulate_logic(input_data, correlated_shocks)

        # Convert simulation results to a DataFrame for consistent output and plotting
        simulation_df = pd.DataFrame(
            simulation_result.paths, index=simulation_result.time_grid
        )
        simulation_df.index.name = "Time"
        simulation_df.reset_index(inplace=True)
        simulation_df.columns = ["Time"] + [
            f"Path_{i}" for i in range(input_data.num_paths)
        ]

        # Save results to CSV
        output_path_csv = os.path.join(self.output_dir, "simulated_prices.csv")
        simulation_df.to_csv(output_path_csv, index=False)

        # Generate and save plots based on plot_options
        if plot_options is None:
            plot_options = {
                "price_paths": {"enabled": True},
                "price_distribution_at_maturity": {"enabled": True},
            }

        from visualization.plotter import (
            plot_price_paths,
            plot_price_distribution_at_maturity,
        )

        if plot_options.get("price_paths", {}).get("enabled", False):
            output_filename = plot_options["price_paths"].get(
                "output_filename", "simulated_price_paths.html"
            )
            plot_price_paths(
                simulation_df, os.path.join(self.output_dir, output_filename)
            )

        if plot_options.get("price_distribution_at_maturity", {}).get("enabled", False):
            output_filename = plot_options["price_distribution_at_maturity"].get(
                "output_filename", "price_distribution_at_maturity.html"
            )
            plot_price_distribution_at_maturity(
                simulation_df, os.path.join(self.output_dir, output_filename)
            )

        return simulation_result

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self, scenario_definition: dict) -> GBMInputData:
        # Load data from CSV file, but allow scenario_definition to override
        gbm_data_path = os.path.join(self.input_dir, "gbm_parameters.csv")
        df = pd.read_csv(gbm_data_path)

        # Use values from scenario_definition if provided, otherwise from CSV
        return GBMInputData(
            initial_price=scenario_definition.get(
                "initial_price", df["Initial_Price"].iloc[0]
            ),
            expected_return=scenario_definition.get(
                "expected_return", df["Expected_Return"].iloc[0]
            ),
            volatility=scenario_definition.get("volatility", df["Volatility"].iloc[0]),
            time_horizon=scenario_definition.get(
                "time_horizon", df["Time_Horizon"].iloc[0]
            ),
            num_time_steps=scenario_definition.get(
                "num_time_steps", df["Num_Time_Steps"].iloc[0]
            ),
            num_paths=scenario_definition.get("num_paths", df["Num_Paths"].iloc[0]),
        )

    def _simulate_logic(
        self, input_data: GBMInputData, correlated_shocks=None
    ) -> GBMSimulationResult:
        S0 = input_data.initial_price
        mu = input_data.expected_return
        sigma = input_data.volatility
        T = input_data.time_horizon
        N = input_data.num_time_steps
        M = input_data.num_paths

        dt = T / N
        time_grid = np.linspace(0, T, N + 1)

        if correlated_shocks is None:
            # Generate standard normal random variables for each time step and path
            correlated_shocks = np.random.standard_normal(size=(N, M))

        # Initialize array to store simulation paths
        paths = np.zeros((N + 1, M))
        paths[0, :] = S0

        for t in range(N):
            # Apply GBM step for each path
            paths[t + 1, :] = formulas.gbm_step(
                paths[t, :], mu, sigma, dt, correlated_shocks[t, :]
            )

        return GBMSimulationResult(paths=paths, time_grid=time_grid)

    def calibrate(self, *args, **kwargs):
        raise NotImplementedError(
            "GBM Model does not require calibration in this context; parameters are direct inputs."
        )

    def train(self, historical_data):
        raise NotImplementedError(
            "The GBM Model is a stochastic model and does not require training."
        )

    def predict(self, input_features):
        raise NotImplementedError(
            "The GBM Model uses 'simulate' for generating future paths, not 'predict'."
        )
