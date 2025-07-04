from . import pricing, formulas
from .data_structures import CalibratedHW1FModel, HW1FSimulationResult
from scipy.optimize import minimize
from scipy.interpolate import interp1d
import numpy as np
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


class HullWhiteOneFactor(ModelInterface):

    def __init__(
        self,
        input_dir="RiskModels/data/inputs/hull_white_one_factor",
        output_dir="RiskModels/data/outputs/hull_white_one_factor",
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_name(self) -> str:
        return "hull_white_one_factor"

    def get_required_risk_factors(self) -> list[str]:
        return ["risk_free_rate_curve", "swaption_volatility_surface"]

    def _load_and_prepare_data(self):
        # Load data from CSV files
        zcb_curve_path = os.path.join(self.input_dir, "initial_zcb_curve.csv")

        zcb_df = pd.read_csv(zcb_curve_path)

        # Create an interpolated pricer function from the ZCB curve data
        initial_zero_coupon_bond_pricer = interp1d(
            zcb_df["Maturity"], zcb_df["Price"], kind="cubic", fill_value="extrapolate"
        )

        # Convert swaption volatility dataframe to a list of dicts for calibration
        # This part needs a more robust implementation based on how swaption details are provided.
        # For now, we assume a simplified structure.
        market_swaptions = []  # This would be built from swaptions_df

        return initial_zero_coupon_bond_pricer, market_swaptions

    def _calibrate_logic(
        self, initial_zero_coupon_bond_pricer, market_swaptions
    ) -> CalibratedHW1FModel:
        def objective_function(params):
            a, sigma = params
            if a <= 0 or sigma <= 0:  # Ensure positive parameters
                return np.inf

            # Generate theta function for current a, sigma
            theta_func = formulas.generate_theta_function(
                a, sigma, initial_zero_coupon_bond_pricer
            )

            # Create a temporary calibrated model for pricing
            temp_calibrated_model = CalibratedHW1FModel(
                a=a,
                sigma=sigma,
                theta_function=theta_func,
                calibration_error=0.0,  # Placeholder
                initial_zero_coupon_bond_pricer=initial_zero_coupon_bond_pricer,
            )

            total_error = 0.0
            for swaption in market_swaptions:
                model_price = pricing.price_european_swaption(
                    swap_rate=swaption["swap_rate"],
                    expiry=swaption["expiry"],
                    tenor_start=swaption["tenor_start"],
                    tenor_end=swaption["tenor_end"],
                    fixed_frequency=swaption["fixed_frequency"],
                    calibrated_model=temp_calibrated_model,
                    option_type=swaption.get(
                        "option_type", "payer"
                    ),  # Default to payer
                )
                total_error += (model_price - swaption["market_price"]) ** 2
            return total_error

        # Initial guess for a and sigma (can be refined)
        initial_guess = [0.1, 0.01]  # Example values
        bounds = ((1e-5, None), (1e-5, None))  # a > 0, sigma > 0

        result = minimize(
            objective_function, initial_guess, method="L-BFGS-B", bounds=bounds
        )

        if not result.success:
            raise RuntimeError(f"Calibration failed: {result.message}")

        calibrated_a, calibrated_sigma = result.x
        final_theta_func = formulas.generate_theta_function(
            calibrated_a, calibrated_sigma, initial_zero_coupon_bond_pricer
        )

        return CalibratedHW1FModel(
            a=calibrated_a,
            sigma=calibrated_sigma,
            theta_function=final_theta_func,
            calibration_error=result.fun,
            initial_zero_coupon_bond_pricer=initial_zero_coupon_bond_pricer,
        )

    def calibrate(self) -> CalibratedHW1FModel:
        initial_zero_coupon_bond_pricer, market_swaptions = (
            self._load_and_prepare_data()
        )
        return self._calibrate_logic(initial_zero_coupon_bond_pricer, market_swaptions)

    def _simulate_logic(
        self,
        calibrated_model: CalibratedHW1FModel,
        scenario_definition,
        correlated_shocks,
    ) -> HW1FSimulationResult:
        a = calibrated_model.a
        sigma = calibrated_model.sigma
        theta_function = calibrated_model.theta_function
        initial_zero_coupon_bond_pricer = (
            calibrated_model.initial_zero_coupon_bond_pricer
        )

        num_paths = scenario_definition["num_paths"]
        time_horizon = scenario_definition["time_horizon"]
        dt = scenario_definition["dt"]

        num_timesteps = int(time_horizon / dt) + 1
        time_grid = np.linspace(0, time_horizon, num_timesteps)

        # Get initial short rate r(0) from the initial curve
        # f(0,0) is not well-defined, so we use f(0, epsilon) as an approximation for r(0)
        epsilon = 1e-5
        r0 = formulas.instantaneous_forward_rate(
            epsilon, initial_zero_coupon_bond_pricer
        )

        paths = np.zeros((num_timesteps, num_paths))
        paths[0, :] = r0

        for i in range(num_timesteps - 1):
            t = time_grid[i]
            r_t = paths[i, :]
            dW_t = correlated_shocks[i, :]

            drift = (theta_function(t) - a * r_t) * dt
            stochastic = sigma * np.sqrt(dt) * dW_t

            paths[i + 1, :] = r_t + drift + stochastic

        return HW1FSimulationResult(paths=paths, time_grid=time_grid)

    def simulate(
        self,
        calibrated_model: CalibratedHW1FModel,
        scenario_definition,
        correlated_shocks=None,
        plot_options: dict = None,
    ) -> HW1FSimulationResult:
        num_paths = scenario_definition["num_paths"]
        time_horizon = scenario_definition["time_horizon"]
        dt = scenario_definition["dt"]
        num_timesteps = int(time_horizon / dt) + 1

        if correlated_shocks is None:
            correlated_shocks = np.random.standard_normal(
                size=(num_timesteps - 1, num_paths)
            )

        simulation_result = self._simulate_logic(
            calibrated_model, scenario_definition, correlated_shocks
        )

        # Convert simulation results to a DataFrame for consistent output and plotting
        simulation_df = pd.DataFrame(
            simulation_result.paths, index=simulation_result.time_grid
        )
        simulation_df.index.name = "Time"
        simulation_df.reset_index(inplace=True)
        simulation_df.columns = ["Time"] + [f"Path_{i}" for i in range(num_paths)]

        # Save results to CSV
        output_path_csv = os.path.join(self.output_dir, "simulated_short_rates.csv")
        simulation_df.to_csv(output_path_csv)

        # Generate and save plots based on plot_options
        if plot_options is None:
            plot_options = {
                "short_rate_paths": {"enabled": True},
                "short_rate_distribution": {
                    "enabled": True,
                    "time_points": [1.0, 3.0, 5.0],
                },
            }

        from visualization.plotter import (
            plot_short_rate_paths,
            plot_short_rate_distribution,
        )

        if plot_options.get("short_rate_paths", {}).get("enabled", False):
            output_filename = plot_options["short_rate_paths"].get(
                "output_filename", "simulated_short_rate_paths.html"
            )
            plot_short_rate_paths(
                simulation_df, os.path.join(self.output_dir, output_filename)
            )

        if plot_options.get("short_rate_distribution", {}).get("enabled", False):
            selected_time_points = plot_options["short_rate_distribution"].get(
                "time_points", [1.0, 3.0, 5.0]
            )
            output_filename = plot_options["short_rate_distribution"].get(
                "output_filename", "simulated_short_rate_distribution.html"
            )
            plot_short_rate_distribution(
                simulation_df,
                selected_time_points,
                os.path.join(self.output_dir, output_filename),
            )

        return simulation_result

    def train(self, historical_data):
        # This method is primarily for Machine Learning models.
        # For the Hull-White One-Factor model, it is not applicable.
        raise NotImplementedError(
            "The Hull-White One-Factor model is a traditional stochastic model and does not require training."
        )

    def predict(self, input_features):
        # This method is primarily for Machine Learning models.
        # For the Hull-White One-Factor model, simulation is the equivalent operation.
        raise NotImplementedError(
            "The Hull-White One-Factor model uses 'simulate' for generating future paths, not 'predict'."
        )
