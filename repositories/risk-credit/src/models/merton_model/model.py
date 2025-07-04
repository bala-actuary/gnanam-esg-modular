from . import calculations, formulas
from .data_structures import (
    MertonInputData,
    CalibratedMertonModel,
    MertonOutputResults,
    MertonSimulationResult,
)
import pandas as pd
import os
from scipy.optimize import minimize
import numpy as np
from scipy.stats import norm


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
        raise NotImplementedError(
            "The Merton Model uses 'calibrate' and 'calculate_results' for its primary operations, not 'predict'."
        )


class MertonModel(ModelInterface):

    def __init__(
        self,
        input_dir="RiskModels/data/inputs/merton_model",
        output_dir="RiskModels/data/outputs/merton_model",
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "merton_model"

    def get_required_risk_factors(self) -> list[str]:
        return [
            "equity_value",
            "equity_volatility",
            "face_value_debt",
            "time_to_maturity",
            "risk_free_rate",
        ]

    # --- Public Methods (for file-based I/O and convenience) ---

    def calibrate(self) -> CalibratedMertonModel:
        input_data = self._load_and_prepare_data()
        return self._calibrate_logic(input_data)

    def calculate_results(
        self, calibrated_model: CalibratedMertonModel
    ) -> MertonOutputResults:
        input_data = self._load_and_prepare_data()
        results = self._calculate_results_logic(calibrated_model, input_data)

        output_path = os.path.join(self.output_dir, "merton_results.csv")
        pd.DataFrame(
            [
                {
                    "Implied_Asset_Value": calibrated_model.asset_value,
                    "Implied_Asset_Volatility": calibrated_model.asset_volatility,
                    "Default_Probability": results.default_probability,
                    "Credit_Spread": results.credit_spread,
                }
            ]
        ).to_csv(output_path, index=False)

        return results

    def simulate(
        self,
        calibrated_model: CalibratedMertonModel,
        scenario_definition: dict,
        correlated_shocks=None,
        plot_options: dict = None,
    ) -> MertonSimulationResult:
        input_data = (
            self._load_and_prepare_data()
        )  # To get Face_Value_Debt and Time_to_Maturity
        simulation_result = self._simulate_logic(
            calibrated_model,
            scenario_definition,
            input_data.face_value_debt,
            correlated_shocks,
        )

        # Convert simulation results to a DataFrame for consistent output and plotting
        simulation_df = pd.DataFrame(
            simulation_result.paths, index=simulation_result.time_grid
        )
        simulation_df.index.name = "Time"
        simulation_df.reset_index(inplace=True)
        simulation_df.columns = ["Time"] + [
            f"Path_{i}" for i in range(scenario_definition["num_paths"])
        ]

        # Add default events to the DataFrame
        default_events_df = pd.DataFrame(
            simulation_result.default_events, index=simulation_result.time_grid
        )
        default_events_df.index.name = "Time"
        default_events_df.reset_index(inplace=True)
        default_events_df.columns = ["Time"] + [
            f"Default_Path_{i}" for i in range(scenario_definition["num_paths"])
        ]

        # Save results to CSV
        output_path_csv = os.path.join(self.output_dir, "simulated_asset_paths.csv")
        simulation_df.to_csv(output_path_csv, index=False)

        # Generate and save plots based on plot_options
        if plot_options is None:
            plot_options = {
                "asset_paths": {"enabled": True},
                "default_probability_over_time": {"enabled": True},
            }

        from visualization.plotter import (
            plot_merton_asset_paths,
            plot_merton_default_probability_over_time,
        )

        if plot_options.get("asset_paths", {}).get("enabled", False):
            output_filename = plot_options["asset_paths"].get(
                "output_filename", "simulated_asset_paths.html"
            )
            plot_merton_asset_paths(
                simulation_df, os.path.join(self.output_dir, output_filename)
            )

        if plot_options.get("default_probability_over_time", {}).get("enabled", False):
            output_filename = plot_options["default_probability_over_time"].get(
                "output_filename", "default_probability_over_time.html"
            )
            plot_merton_default_probability_over_time(
                simulation_df,
                input_data.face_value_debt,
                input_data.time_to_maturity,
                input_data.risk_free_rate,
                calibrated_model.asset_volatility,
                os.path.join(self.output_dir, output_filename),
            )

        return simulation_result

    # --- Internal Logic Methods (for pure in-memory operations) ---

    def _load_and_prepare_data(self) -> MertonInputData:
        firm_data_path = os.path.join(self.input_dir, "firm_data.csv")
        df = pd.read_csv(firm_data_path)
        # Assuming single row for now
        return MertonInputData(
            equity_value=df["Equity_Value"].iloc[0],
            equity_volatility=df["Equity_Volatility"].iloc[0],
            face_value_debt=df["Face_Value_Debt"].iloc[0],
            time_to_maturity=df["Time_to_Maturity"].iloc[0],
            risk_free_rate=df["Risk_Free_Rate"].iloc[0],
        )

    def _calibrate_logic(self, input_data: MertonInputData) -> CalibratedMertonModel:
        E = input_data.equity_value
        sigma_E = input_data.equity_volatility
        F = input_data.face_value_debt
        T = input_data.time_to_maturity
        r = input_data.risk_free_rate

        # Objective function to minimize (sum of squared errors)
        def objective_sum_of_squares(p):
            V_A, sigma_A = p
            if V_A <= 0 or sigma_A <= 0:
                return 1e10  # Return a large error for invalid parameters

            d1_val = formulas.d1(V_A, F, T, r, sigma_A)
            d2_val = formulas.d2(V_A, F, T, r, sigma_A)

            # Calculate implied equity value and volatility
            implied_E = V_A * norm.cdf(d1_val) - F * np.exp(-r * T) * norm.cdf(d2_val)

            # Handle potential division by zero for implied_sigma_E
            if implied_E == 0:
                implied_sigma_E = 1e10  # Assign a large value to indicate error
            else:
                implied_sigma_E = (V_A * norm.pdf(d1_val) * sigma_A) / implied_E

            # Calculate errors
            error_E = implied_E - E
            error_sigma_E = implied_sigma_E - sigma_E

            return error_E**2 + error_sigma_E**2

        # Initial guess for V_A and sigma_A
        V_A_initial = E + F * np.exp(
            -r * T
        )  # Asset value is roughly Equity + PV of Debt
        sigma_A_initial = (
            sigma_E  # Asset volatility is often close to equity volatility initially
        )

        initial_guess = [V_A_initial, sigma_A_initial]

        # Bounds for V_A and sigma_A (must be positive)
        bounds = ((1e-6, None), (1e-6, None))  # (min, max) for each variable

        # Solve the minimization problem
        try:
            sol = minimize(
                objective_sum_of_squares,
                initial_guess,
                method="L-BFGS-B",
                bounds=bounds,
            )

            if not sol.success:
                raise RuntimeError(f"Merton Model calibration failed: {sol.message}")

            V_A_calibrated, sigma_A_calibrated = sol.x

        except Exception as e:
            raise RuntimeError(f"Merton Model calibration failed: {e}")

        # Basic validation of results
        if V_A_calibrated <= 0 or sigma_A_calibrated <= 0:
            raise RuntimeError(
                "Merton Model calibration resulted in non-positive asset value or "
                "volatility."
            )

        return CalibratedMertonModel(
            asset_value=V_A_calibrated, asset_volatility=sigma_A_calibrated
        )

    def _calculate_results_logic(
        self, calibrated_model: CalibratedMertonModel, input_data: MertonInputData
    ) -> MertonOutputResults:
        PD = calculations.calculate_default_probability(
            calibrated_model.asset_value,
            calibrated_model.asset_volatility,
            input_data.face_value_debt,
            input_data.time_to_maturity,
            input_data.risk_free_rate,
        )

        CS = calculations.calculate_credit_spread(
            calibrated_model.asset_value,
            calibrated_model.asset_volatility,
            input_data.face_value_debt,
            input_data.time_to_maturity,
            input_data.risk_free_rate,
        )

        return MertonOutputResults(default_probability=PD, credit_spread=CS)

    def _simulate_logic(
        self,
        calibrated_model: CalibratedMertonModel,
        scenario_definition: dict,
        face_value_debt: float,
        correlated_shocks=None,
    ) -> MertonSimulationResult:
        V0 = calibrated_model.asset_value
        sigma_A = calibrated_model.asset_volatility
        T = scenario_definition["time_horizon"]
        N = scenario_definition["num_time_steps"]
        M = scenario_definition["num_paths"]
        F = face_value_debt  # Debt value from input data

        dt = T / N
        time_grid = np.linspace(0, T, N + 1)

        if correlated_shocks is None:
            correlated_shocks = np.random.standard_normal(size=(N, M))

        paths = np.zeros((N + 1, M))
        paths[0, :] = V0

        default_events = np.zeros((N + 1, M), dtype=bool)

        for t in range(N):
            paths[t + 1, :] = formulas.gbm_step(
                paths[t, :], 0, sigma_A, dt, correlated_shocks[t, :]
            )  # Merton uses risk-neutral drift of 0 for asset value
            # Check for default at each step
            default_events[t + 1, :] = paths[t + 1, :] < F

        return MertonSimulationResult(
            paths=paths, time_grid=time_grid, default_events=default_events
        )

    def train(self, historical_data):
        raise NotImplementedError(
            "The Merton Model is a structural model and does not require training in "
            "this context."
        )

    def predict(self, input_features):
        raise NotImplementedError(
            "The Merton Model uses 'calibrate' and 'calculate_results' for its primary operations, not 'predict'."
        )
