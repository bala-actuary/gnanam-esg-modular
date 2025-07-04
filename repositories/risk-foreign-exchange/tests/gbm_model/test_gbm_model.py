import pytest
import numpy as np
import pandas as pd
import os

from models.Equity_Risk.gbm_model.formulas import gbm_step
from models.Equity_Risk.gbm_model.data_structures import GBMInputData, GBMSimulationResult
from models.Equity_Risk.gbm_model.model import GBMModel

# --- Fixtures for testing ---

@pytest.fixture
def sample_gbm_input_data():
    return GBMInputData(
        initial_price=100.0,
        expected_return=0.10,
        volatility=0.20,
        time_horizon=1.0,
        num_time_steps=252,
        num_paths=10
    )

@pytest.fixture
def setup_temp_data_dirs(tmp_path):
    input_dir = tmp_path / "inputs" / "gbm_model"
    output_dir = tmp_path / "outputs" / "gbm_model"
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    # Create dummy gbm_parameters.csv
    gbm_data = {
        'Initial_Price': [100.0],
        'Expected_Return': [0.10],
        'Volatility': [0.20],
        'Time_Horizon': [1.0],
        'Num_Time_Steps': [252],
        'Num_Paths': [10]
    }
    pd.DataFrame(gbm_data).to_csv(input_dir / "gbm_parameters.csv", index=False)

    return str(input_dir), str(output_dir)

# --- Unit Tests ---

# Target: formulas.py
def test_gbm_step_calculation():
    # TC-U-01
    S_t = 100.0
    mu = 0.10
    sigma = 0.20
    dt = 1/252
    dW = np.array([0.5, -0.5]) # Example random shocks

    expected_S_t_plus_dt = S_t * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dW)
    
    assert np.allclose(gbm_step(S_t, mu, sigma, dt, dW), expected_S_t_plus_dt)

# Target: model.py (Basic Methods)
def test_get_name():
    # TC-U-02
    gbm_model = GBMModel()
    assert gbm_model.get_name() == "gbm_model"

def test_get_required_risk_factors():
    # TC-U-03
    gbm_model = GBMModel()
    expected_factors = ["initial_price", "expected_return", "volatility", "time_horizon", "num_time_steps", "num_paths"]
    assert gbm_model.get_required_risk_factors() == expected_factors

def test_calibrate_raises_not_implemented_error():
    # TC-U-04
    gbm_model = GBMModel()
    with pytest.raises(NotImplementedError, match="GBM Model does not require calibration in this context; parameters are direct inputs."):
        gbm_model.calibrate()

def test_train_raises_not_implemented_error():
    # TC-U-05
    gbm_model = GBMModel()
    with pytest.raises(NotImplementedError, match="The GBM Model is a stochastic model and does not require training."):
        gbm_model.train(None)

def test_predict_raises_not_implemented_error():
    # TC-U-05
    gbm_model = GBMModel()
    with pytest.raises(NotImplementedError, match="The GBM Model uses 'simulate' for generating future paths, not 'predict'."):
        gbm_model.predict(None)

# --- Integration Tests ---

def test_load_and_prepare_data_from_file(setup_temp_data_dirs):
    # TC-I-01 (from file)
    input_dir, _ = setup_temp_data_dirs
    gbm_model = GBMModel(input_dir=input_dir)
    input_data = gbm_model._load_and_prepare_data(scenario_definition={})

    assert isinstance(input_data, GBMInputData)
    assert np.isclose(input_data.initial_price, 100.0)
    assert np.isclose(input_data.expected_return, 0.10)
    assert np.isclose(input_data.volatility, 0.20)
    assert np.isclose(input_data.time_horizon, 1.0)
    assert input_data.num_time_steps == 252
    assert input_data.num_paths == 10

def test_load_and_prepare_data_with_override(setup_temp_data_dirs):
    # TC-I-01 (with override)
    input_dir, _ = setup_temp_data_dirs
    gbm_model = GBMModel(input_dir=input_dir)
    
    scenario_override = {
        'initial_price': 120.0,
        'num_paths': 50
    }
    input_data = gbm_model._load_and_prepare_data(scenario_override)

    assert isinstance(input_data, GBMInputData)
    assert np.isclose(input_data.initial_price, 120.0)
    assert np.isclose(input_data.expected_return, 0.10) # Should come from file
    assert input_data.num_paths == 50

def test_simulate_logic(sample_gbm_input_data):
    # TC-I-02
    gbm_model = GBMModel() # Directories don't matter for logic methods
    simulation_result = gbm_model._simulate_logic(sample_gbm_input_data)

    assert isinstance(simulation_result, GBMSimulationResult)
    assert simulation_result.paths.shape == (sample_gbm_input_data.num_time_steps + 1, sample_gbm_input_data.num_paths)
    assert simulation_result.time_grid.shape == (sample_gbm_input_data.num_time_steps + 1,)
    assert np.allclose(simulation_result.paths[0, :], sample_gbm_input_data.initial_price)

def test_simulate_public_method(setup_temp_data_dirs):
    # TC-I-03
    input_dir, output_dir = setup_temp_data_dirs
    gbm_model = GBMModel(input_dir=input_dir, output_dir=output_dir)

    scenario_definition = {
        'initial_price': 100.0,
        'expected_return': 0.10,
        'volatility': 0.20,
        'time_horizon': 1.0,
        'num_time_steps': 252,
        'num_paths': 10
    }

    # Test with default plot options (both enabled)
    simulation_result = gbm_model.simulate(scenario_definition)

    assert isinstance(simulation_result, GBMSimulationResult)
    output_csv_path = os.path.join(output_dir, "simulated_prices.csv")
    assert os.path.exists(output_csv_path)
    output_df = pd.read_csv(output_csv_path)
    assert not output_df.empty

    # Check if default plot files were created
    assert os.path.exists(os.path.join(output_dir, "simulated_price_paths.html"))
    assert os.path.exists(os.path.join(output_dir, "price_distribution_at_maturity.html"))

    # Test with custom plot options (only one enabled)
    # Need to create a new instance or clear output_dir for clean test
    # For simplicity, we'll just check if the custom file is created
    custom_output_dir = os.path.join(output_dir, "custom_plots")
    os.makedirs(custom_output_dir, exist_ok=True)
    gbm_model_custom = GBMModel(input_dir=input_dir, output_dir=custom_output_dir)

    custom_plot_options = {
        "price_paths": {"enabled": True, "output_filename": "custom_gbm_paths.html"},
        "price_distribution_at_maturity": {"enabled": False}
    }
    gbm_model_custom.simulate(scenario_definition, plot_options=custom_plot_options)

    assert os.path.exists(os.path.join(custom_output_dir, "custom_gbm_paths.html"))
    assert not os.path.exists(os.path.join(custom_output_dir, "price_distribution_at_maturity.html"))

# --- Validation Tests ---

def test_expected_mean_of_log_prices(sample_gbm_input_data):
    # TC-V-01
    # Run a large simulation to get good statistics
    input_data_large = GBMInputData(
        initial_price=sample_gbm_input_data.initial_price,
        expected_return=sample_gbm_input_data.expected_return,
        volatility=sample_gbm_input_data.volatility,
        time_horizon=sample_gbm_input_data.time_horizon,
        num_time_steps=sample_gbm_input_data.num_time_steps,
        num_paths=50 # Large number of paths for statistical accuracy
    )
    gbm_model = GBMModel()
    simulation_result = gbm_model._simulate_logic(input_data_large)

    final_prices = simulation_result.paths[-1, :]
    log_final_prices = np.log(final_prices)

    # Analytical expected mean of log-prices
    expected_log_mean = np.log(input_data_large.initial_price) + \
                        (input_data_large.expected_return - 0.5 * input_data_large.volatility**2) * \
                        input_data_large.time_horizon
    
    assert np.isclose(np.mean(log_final_prices), expected_log_mean, atol=1e-2)

def test_expected_variance_of_log_prices(sample_gbm_input_data):
    # TC-V-02
    # Run a large simulation to get good statistics
    input_data_large = GBMInputData(
        initial_price=sample_gbm_input_data.initial_price,
        expected_return=sample_gbm_input_data.expected_return,
        volatility=sample_gbm_input_data.volatility,
        time_horizon=sample_gbm_input_data.time_horizon,
        num_time_steps=sample_gbm_input_data.num_time_steps,
        num_paths=50 # Large number of paths for statistical accuracy
    )
    gbm_model = GBMModel()
    simulation_result = gbm_model._simulate_logic(input_data_large)

    final_prices = simulation_result.paths[-1, :]
    log_final_prices = np.log(final_prices)

    # Analytical expected variance of log-prices
    expected_log_variance = (input_data_large.volatility**2) * input_data_large.time_horizon
    
    assert np.isclose(np.var(log_final_prices), expected_log_variance, atol=1e-2)

# --- Performance Tests ---

@pytest.mark.benchmark(min_rounds=5, warmup=True)
def test_simulation_performance(sample_gbm_input_data):
    # TC-P-01
    gbm_model = GBMModel()
    # Use a larger number of paths for performance testing
    input_data_perf = GBMInputData(
        initial_price=sample_gbm_input_data.initial_price,
        expected_return=sample_gbm_input_data.expected_return,
        volatility=sample_gbm_input_data.volatility,
        time_horizon=sample_gbm_input_data.time_horizon,
        num_time_steps=sample_gbm_input_data.num_time_steps,
        num_paths=50 # Large number of paths for performance testing
    )
    gbm_model._simulate_logic(input_data_perf)
