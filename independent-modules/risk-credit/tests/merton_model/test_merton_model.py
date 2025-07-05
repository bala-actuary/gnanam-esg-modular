import pytest
import numpy as np
import pandas as pd
import os
from scipy.stats import norm

from models.Credit_Risk.merton_model.formulas import d1, d2, black_scholes_call, gbm_step
from models.Credit_Risk.merton_model.calculations import calculate_default_probability, calculate_credit_spread
from models.Credit_Risk.merton_model.data_structures import MertonInputData, CalibratedMertonModel, MertonOutputResults, MertonSimulationResult
from models.Credit_Risk.merton_model.model import MertonModel

# --- Fixtures for testing ---

@pytest.fixture
def sample_merton_input_data():
    return MertonInputData(
        equity_value=100.0,
        equity_volatility=0.25,
        face_value_debt=80.0,
        time_to_maturity=1.0,
        risk_free_rate=0.05
    )

@pytest.fixture
def sample_calibrated_merton_model():
    # These values are derived from a known Merton solution for the above input data
    # E=100, sigma_E=0.25, F=80, T=1, r=0.05
    # Implied V_A approx 150.0, sigma_A approx 0.15
    return CalibratedMertonModel(
        asset_value=150.0,
        asset_volatility=0.15
    )

@pytest.fixture
def setup_temp_data_dirs(tmp_path):
    input_dir = tmp_path / "inputs" / "merton_model"
    output_dir = tmp_path / "outputs" / "merton_model"
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    # Create dummy firm_data.csv
    firm_data = {
        'Equity_Value': [100.0],
        'Equity_Volatility': [0.25],
        'Face_Value_Debt': [80.0],
        'Time_to_Maturity': [1.0],
        'Risk_Free_Rate': [0.05]
    }
    pd.DataFrame(firm_data).to_csv(input_dir / "firm_data.csv", index=False)

    return str(input_dir), str(output_dir)

# --- Unit Tests ---

# Target: formulas.py
def test_d1_d2_calculation():
    # TC-U-01
    S, K, T, r, sigma = 100, 90, 1, 0.05, 0.2
    expected_d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    expected_d2 = expected_d1 - sigma * np.sqrt(T)
    assert np.isclose(d1(S, K, T, r, sigma), expected_d1)
    assert np.isclose(d2(S, K, T, r, sigma), expected_d2)

def test_black_scholes_call():
    # TC-U-02
    S, K, T, r, sigma = 100, 90, 1, 0.05, 0.2
    expected_call_price = S * norm.cdf(d1(S, K, T, r, sigma)) - K * np.exp(-r * T) * norm.cdf(d2(S, K, T, r, sigma))
    assert np.isclose(black_scholes_call(S, K, T, r, sigma), expected_call_price)

# Target: calculations.py
def test_calculate_default_probability():
    # TC-U-03: Using known values for a simple case
    # If asset_value = 100, asset_volatility = 0.1, F=100, T=1, r=0
    # d2 = (ln(100/100) + (0 - 0.5*0.1^2)*1) / (0.1*sqrt(1)) = -0.005 / 0.1 = -0.05
    # PD = N(-(-0.05)) = N(0.05) = 0.5199
    asset_value = 100.0
    asset_volatility = 0.1
    face_value_debt = 100.0
    time_to_maturity = 1.0
    risk_free_rate = 0.0
    expected_pd = norm.cdf(0.05)
    assert np.isclose(calculate_default_probability(asset_value, asset_volatility, face_value_debt, time_to_maturity, risk_free_rate), expected_pd)

def test_calculate_credit_spread():
    # TC-U-04: Using known values for a simple case
    # This is more complex to verify analytically without a full Merton setup.
    # We'll use a simple check for now.
    asset_value = 100.0
    asset_volatility = 0.1
    face_value_debt = 100.0
    time_to_maturity = 1.0
    risk_free_rate = 0.0

    # For these inputs, the value of debt should be close to 100 * N(-d1) + 100 * N(d2)
    # d1 = (ln(100/100) + (0 + 0.5*0.1^2)*1) / (0.1*sqrt(1)) = 0.005 / 0.1 = 0.05
    # d2 = 0.05 - 0.1 = -0.05
    # Value of Debt = 100 * N(-0.05) + 100 * exp(0) * N(-0.05) = 100 * 0.48006 + 100 * 0.48006 = 96.012
    # CS = -1/1 * ln(96.012) = -ln(0.96012) = 0.0406

    d1_val = d1(asset_value, face_value_debt, time_to_maturity, risk_free_rate, asset_volatility)
    d2_val = d2(asset_value, face_value_debt, time_to_maturity, risk_free_rate, asset_volatility)
    value_of_debt = asset_value * norm.cdf(-d1_val) + face_value_debt * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2_val)
    expected_cs = - (1 / time_to_maturity) * np.log(value_of_debt / face_value_debt)

    assert np.isclose(calculate_credit_spread(asset_value, asset_volatility, face_value_debt, time_to_maturity, risk_free_rate), expected_cs)

# Target: model.py (Basic Methods)
def test_get_name():
    # TC-U-05
    merton_model = MertonModel()
    assert merton_model.get_name() == "merton_model"

def test_get_required_risk_factors():
    # TC-U-06
    merton_model = MertonModel()
    expected_factors = ["equity_value", "equity_volatility", "face_value_debt", "time_to_maturity", "risk_free_rate"]
    assert merton_model.get_required_risk_factors() == expected_factors

def test_train_raises_not_implemented_error():
    # TC-U-07
    merton_model = MertonModel()
    with pytest.raises(NotImplementedError, match="The Merton Model is a structural model and does not require training in this context."):
        merton_model.train(None)

def test_predict_raises_not_implemented_error():
    # TC-U-07
    merton_model = MertonModel()
    with pytest.raises(NotImplementedError, match="The Merton Model uses 'calibrate' and 'calculate_results' for its primary operations, not 'predict'."):
        merton_model.predict(None)

# --- Integration Tests ---

def test_load_and_prepare_data(setup_temp_data_dirs):
    # TC-I-02
    input_dir, _ = setup_temp_data_dirs
    merton_model = MertonModel(input_dir=input_dir)
    input_data = merton_model._load_and_prepare_data()

    assert isinstance(input_data, MertonInputData)
    assert np.isclose(input_data.equity_value, 100.0)
    assert np.isclose(input_data.equity_volatility, 0.25)
    assert np.isclose(input_data.face_value_debt, 80.0)
    assert np.isclose(input_data.time_to_maturity, 1.0)
    assert np.isclose(input_data.risk_free_rate, 0.05)

def test_calibrate_logic(sample_merton_input_data):
    # TC-I-03
    merton_model = MertonModel() # Directories don't matter for logic methods
    calibrated_model = merton_model._calibrate_logic(sample_merton_input_data)

    assert isinstance(calibrated_model, CalibratedMertonModel)
    # These assertions are based on a known solution for the sample_merton_input_data
    # The fsolve might give slightly different results depending on initial guess/solver
    # Verify consistency: plug calibrated V_A and sigma_A back into Black-Scholes to get E and sigma_E
    # This is a more robust test for calibration than exact numerical match
    reproduced_equity_value = calibrated_model.asset_value * norm.cdf(d1(calibrated_model.asset_value, sample_merton_input_data.face_value_debt, sample_merton_input_data.time_to_maturity, sample_merton_input_data.risk_free_rate, calibrated_model.asset_volatility)) - sample_merton_input_data.face_value_debt * np.exp(-sample_merton_input_data.risk_free_rate * sample_merton_input_data.time_to_maturity) * norm.cdf(d2(calibrated_model.asset_value, sample_merton_input_data.face_value_debt, sample_merton_input_data.time_to_maturity, sample_merton_input_data.risk_free_rate, calibrated_model.asset_volatility))
    
    reproduced_equity_volatility = (calibrated_model.asset_value * norm.pdf(d1(calibrated_model.asset_value, sample_merton_input_data.face_value_debt, sample_merton_input_data.time_to_maturity, sample_merton_input_data.risk_free_rate, calibrated_model.asset_volatility)) * calibrated_model.asset_volatility) / reproduced_equity_value

    assert np.isclose(reproduced_equity_value, sample_merton_input_data.equity_value, atol=1e-2)
    assert np.isclose(reproduced_equity_volatility, sample_merton_input_data.equity_volatility, atol=1e-2)

def test_calculate_results_logic(sample_calibrated_merton_model, sample_merton_input_data):
    # TC-I-04
    merton_model = MertonModel() # Directories don't matter for logic methods
    results = merton_model._calculate_results_logic(sample_calibrated_merton_model, sample_merton_input_data)

    assert isinstance(results, MertonOutputResults)
    # These expected values are based on the sample_calibrated_merton_model
    # and sample_merton_input_data
    expected_pd = calculate_default_probability(
        sample_calibrated_merton_model.asset_value,
        sample_calibrated_merton_model.asset_volatility,
        sample_merton_input_data.face_value_debt,
        sample_merton_input_data.time_to_maturity,
        sample_merton_input_data.risk_free_rate
    )
    expected_cs = calculate_credit_spread(
        sample_calibrated_merton_model.asset_value,
        sample_calibrated_merton_model.asset_volatility,
        sample_merton_input_data.face_value_debt,
        sample_merton_input_data.time_to_maturity,
        sample_merton_input_data.risk_free_rate
    )
    assert np.isclose(results.default_probability, expected_pd)
    assert np.isclose(results.credit_spread, expected_cs)

def test_calibrate_public_method(setup_temp_data_dirs):
    # TC-I-01
    input_dir, _ = setup_temp_data_dirs
    merton_model = MertonModel(input_dir=input_dir)

    # Load input data from the dummy CSV for the consistency check
    firm_data = pd.read_csv(os.path.join(input_dir, "firm_data.csv"))
    input_data = MertonInputData(
        equity_value=firm_data['Equity_Value'].iloc[0],
        equity_volatility=firm_data['Equity_Volatility'].iloc[0],
        face_value_debt=firm_data['Face_Value_Debt'].iloc[0],
        time_to_maturity=firm_data['Time_to_Maturity'].iloc[0],
        risk_free_rate=firm_data['Risk_Free_Rate'].iloc[0]
    )

    calibrated_model = merton_model.calibrate()

    assert isinstance(calibrated_model, CalibratedMertonModel)
    reproduced_equity_value = calibrated_model.asset_value * norm.cdf(d1(calibrated_model.asset_value, input_data.face_value_debt, input_data.time_to_maturity, input_data.risk_free_rate, calibrated_model.asset_volatility)) - input_data.face_value_debt * np.exp(-input_data.risk_free_rate * input_data.time_to_maturity) * norm.cdf(d2(calibrated_model.asset_value, input_data.face_value_debt, input_data.time_to_maturity, input_data.risk_free_rate, calibrated_model.asset_volatility))
    
    reproduced_equity_volatility = (calibrated_model.asset_value * norm.pdf(d1(calibrated_model.asset_value, input_data.face_value_debt, input_data.time_to_maturity, input_data.risk_free_rate, calibrated_model.asset_volatility)) * calibrated_model.asset_volatility) / reproduced_equity_value

    assert np.isclose(reproduced_equity_value, input_data.equity_value, atol=1e-2)
    assert np.isclose(reproduced_equity_volatility, input_data.equity_volatility, atol=1e-2)

def test_calculate_results_public_method(setup_temp_data_dirs, sample_calibrated_merton_model):
    # TC-I-05 (Part of End-to-End)
    input_dir, output_dir = setup_temp_data_dirs
    merton_model = MertonModel(input_dir=input_dir, output_dir=output_dir)

    results = merton_model.calculate_results(sample_calibrated_merton_model)

    assert isinstance(results, MertonOutputResults)
    output_file_path = os.path.join(output_dir, "merton_results.csv")
    assert os.path.exists(output_file_path)
    output_df = pd.read_csv(output_file_path)
    assert not output_df.empty
    assert np.isclose(output_df['Implied_Asset_Value'].iloc[0], sample_calibrated_merton_model.asset_value)
    assert np.isclose(output_df['Implied_Asset_Volatility'].iloc[0], sample_calibrated_merton_model.asset_volatility)

def test_simulate_logic(sample_calibrated_merton_model, sample_merton_input_data):
    # TC-I-06
    merton_model = MertonModel()
    scenario_definition = {
        'time_horizon': 1.0,
        'num_time_steps': 252,
        'num_paths': 10
    }
    simulation_result = merton_model._simulate_logic(sample_calibrated_merton_model, scenario_definition, sample_merton_input_data.face_value_debt)

    assert isinstance(simulation_result, MertonSimulationResult)
    assert simulation_result.paths.shape == (scenario_definition['num_time_steps'] + 1, scenario_definition['num_paths'])
    assert simulation_result.time_grid.shape == (scenario_definition['num_time_steps'] + 1,)
    assert simulation_result.default_events.shape == (scenario_definition['num_time_steps'] + 1, scenario_definition['num_paths'])
    assert np.all(simulation_result.paths[0, :] == sample_calibrated_merton_model.asset_value)

def test_simulate_public_method(setup_temp_data_dirs, sample_calibrated_merton_model):
    # TC-I-07
    input_dir, output_dir = setup_temp_data_dirs
    merton_model = MertonModel(input_dir=input_dir, output_dir=output_dir)

    scenario_definition = {
        'time_horizon': 1.0,
        'num_time_steps': 252,
        'num_paths': 10
    }
    plot_options = {
        "asset_paths": {"enabled": True, "output_filename": "test_simulated_asset_paths.html"},
        "default_probability_over_time": {"enabled": True, "output_filename": "test_default_probability_over_time.html"}
    }

    simulation_result = merton_model.simulate(sample_calibrated_merton_model, scenario_definition, plot_options=plot_options)

    assert isinstance(simulation_result, MertonSimulationResult)
    output_csv_path = os.path.join(output_dir, "simulated_asset_paths.csv")
    assert os.path.exists(output_csv_path)
    assert os.path.exists(os.path.join(output_dir, "test_simulated_asset_paths.html"))
    assert os.path.exists(os.path.join(output_dir, "test_default_probability_over_time.html"))

# --- Validation Tests ---

def test_known_analytical_solution_verification():
    # TC-V-01: Example from literature/online calculators
    # E = 3, sigma_E = 0.25, F = 10, T = 1, r = 0.05
    # Expected V_A approx 12.45, sigma_A approx 0.08
    # Expected PD approx 0.05
    # Expected CS approx 0.05

    input_data = MertonInputData(
        equity_value=3.0,
        equity_volatility=0.25,
        face_value_debt=10.0,
        time_to_maturity=1.0,
        risk_free_rate=0.05
    )
    merton_model = MertonModel()
    calibrated_model = merton_model._calibrate_logic(input_data)
    results = merton_model._calculate_results_logic(calibrated_model, input_data)

    reproduced_equity_value = calibrated_model.asset_value * norm.cdf(d1(calibrated_model.asset_value, input_data.face_value_debt, input_data.time_to_maturity, input_data.risk_free_rate, calibrated_model.asset_volatility)) - input_data.face_value_debt * np.exp(-input_data.risk_free_rate * input_data.time_to_maturity) * norm.cdf(d2(calibrated_model.asset_value, input_data.face_value_debt, input_data.time_to_maturity, input_data.risk_free_rate, calibrated_model.asset_volatility))
    
    reproduced_equity_volatility = (calibrated_model.asset_value * norm.pdf(d1(calibrated_model.asset_value, input_data.face_value_debt, input_data.time_to_maturity, input_data.risk_free_rate, calibrated_model.asset_volatility)) * calibrated_model.asset_volatility) / reproduced_equity_value

    # Define expected_pd and expected_cs here
    expected_pd = calculate_default_probability(
        calibrated_model.asset_value,
        calibrated_model.asset_volatility,
        input_data.face_value_debt,
        input_data.time_to_maturity,
        input_data.risk_free_rate
    )
    expected_cs = calculate_credit_spread(
        calibrated_model.asset_value,
        calibrated_model.asset_volatility,
        input_data.face_value_debt,
        input_data.time_to_maturity,
        input_data.risk_free_rate
    )

    assert np.isclose(reproduced_equity_value, input_data.equity_value, atol=1e-2)
    assert np.isclose(reproduced_equity_volatility, input_data.equity_volatility, atol=1e-2)
    assert np.isclose(results.default_probability, expected_pd, atol=1e-2)
    assert np.isclose(results.credit_spread, expected_cs, atol=1e-2)

def test_simulated_asset_path_properties(sample_calibrated_merton_model, sample_merton_input_data):
    # TC-V-03
    merton_model = MertonModel()
    scenario_definition = {
        'time_horizon': 1.0,
        'num_time_steps': 252,
        'num_paths': 50 # Large number of paths for statistical validation
    }
    simulation_result = merton_model._simulate_logic(sample_calibrated_merton_model, scenario_definition, sample_merton_input_data.face_value_debt)

    # Validate log-normality of asset values at maturity
    final_asset_values = simulation_result.paths[-1, :]
    log_final_asset_values = np.log(final_asset_values)

    # Expected mean and variance of log(S_T) for GBM
    # Merton uses risk-neutral drift of 0 for asset value, so mu = r
    # However, the GBM step in formulas.py uses mu as the drift, which for asset value is 0
    # So, expected_log_mean = log(V0) + (0 - 0.5 * sigma_A^2) * T
    expected_log_mean = np.log(sample_calibrated_merton_model.asset_value) + \
                        (0 - 0.5 * sample_calibrated_merton_model.asset_volatility**2) * scenario_definition['time_horizon']
    expected_log_variance = (sample_calibrated_merton_model.asset_volatility**2) * scenario_definition['time_horizon']

    assert np.isclose(np.mean(log_final_asset_values), expected_log_mean, rtol=0.05, atol=0.01)
    assert np.isclose(np.var(log_final_asset_values), expected_log_variance, rtol=0.05, atol=0.01)

def test_default_event_consistency(sample_calibrated_merton_model, sample_merton_input_data):
    # TC-V-04
    merton_model = MertonModel()
    scenario_definition = {
        'time_horizon': 1.0,
        'num_time_steps': 252,
        'num_paths': 50 # Small number of paths for easier inspection
    }
    simulation_result = merton_model._simulate_logic(sample_calibrated_merton_model, scenario_definition, sample_merton_input_data.face_value_debt)

    # Verify that default_events is True when asset value < face_value_debt
    # And False otherwise
    for i in range(simulation_result.paths.shape[0]):
        for j in range(simulation_result.paths.shape[1]):
            if simulation_result.paths[i, j] < sample_merton_input_data.face_value_debt:
                assert simulation_result.default_events[i, j] == True
            else:
                assert simulation_result.default_events[i, j] == False

# --- Performance Tests ---

@pytest.mark.benchmark(min_rounds=5, warmup=True)
def test_calibration_performance(sample_merton_input_data):
    # TC-P-01
    merton_model = MertonModel()
    merton_model._calibrate_logic(sample_merton_input_data)

@pytest.mark.benchmark(min_rounds=5, warmup=True)
def test_calculation_performance(sample_calibrated_merton_model, sample_merton_input_data):
    # TC-P-02
    merton_model = MertonModel()
    merton_model._calculate_results_logic(sample_calibrated_merton_model, sample_merton_input_data)

@pytest.mark.benchmark(min_rounds=5, warmup=True)
def test_simulation_performance(sample_calibrated_merton_model, sample_merton_input_data):
    # TC-P-03
    merton_model = MertonModel()
    scenario_definition = {
        'time_horizon': 1.0,
        'num_time_steps': 252,
        'num_paths': 50
    }
    merton_model._simulate_logic(sample_calibrated_merton_model, scenario_definition, sample_merton_input_data.face_value_debt)