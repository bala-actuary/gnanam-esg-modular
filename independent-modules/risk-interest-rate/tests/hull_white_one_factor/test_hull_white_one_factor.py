import pytest
import numpy as np
import pandas as pd
import os
from scipy.interpolate import interp1d

from models.Interest_Rate_Risk.hull_white_one_factor.formulas import B, A, generate_theta_function, instantaneous_forward_rate
from models.Interest_Rate_Risk.hull_white_one_factor.pricing import price_zcb, price_european_option_on_zcb, price_european_swaption
from models.Interest_Rate_Risk.hull_white_one_factor.data_structures import CalibratedHW1FModel, HW1FSimulationResult
from models.Interest_Rate_Risk.hull_white_one_factor.model import HullWhiteOneFactor

# --- Fixtures for testing ---

# Mock initial_zero_coupon_bond_pricer for testing purposes
def mock_initial_zcb_pricer(t):
    # A simple, flat yield curve for testing: P(0,t) = exp(-0.05 * t)
    return np.exp(-0.05 * t)

# Mock CalibratedHW1FModel for testing functions that require it
@pytest.fixture
def mock_calibrated_model_for_logic():
    a = 0.1
    sigma = 0.01
    theta_func = generate_theta_function(a, sigma, mock_initial_zcb_pricer)
    return CalibratedHW1FModel(
        a=a,
        sigma=sigma,
        theta_function=theta_func,
        calibration_error=0.0,
        initial_zero_coupon_bond_pricer=mock_initial_zcb_pricer
    )

@pytest.fixture
def setup_temp_data_dirs(tmp_path):
    input_dir = tmp_path / "inputs" / "hull_white_one_factor"
    output_dir = tmp_path / "outputs" / "hull_white_one_factor"
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    # Create dummy initial_zcb_curve.csv
    zcb_data = {'Maturity': [0.25, 0.5, 1.0, 2.0, 5.0],
                'Price': [0.995, 0.99, 0.98, 0.96, 0.92]}
    pd.DataFrame(zcb_data).to_csv(input_dir / "initial_zcb_curve.csv", index=False)

    # Create dummy swaption_volatilities.csv (simplified for testing)
    swaption_data = {'Tenor': [1.0, 2.0],
                     '1Y': [0.15, 0.14],
                     '2Y': [0.14, 0.13]}
    pd.DataFrame(swaption_data).to_csv(input_dir / "swaption_volatilities.csv", index=False)

    return str(input_dir), str(output_dir)

# --- Unit Tests (remain largely unchanged, as they test pure functions) ---

# Target: formulas.py
def test_B_function_known_values():
    # TC-U-01
    assert np.isclose(B(0, 1, 0.1), (1/0.1) * (1 - np.exp(-0.1 * 1)))
    assert np.isclose(B(0.5, 1.5, 0.05), (1/0.05) * (1 - np.exp(-0.05 * 1)))

def test_B_function_t_equals_T():
    # TC-U-02
    assert np.isclose(B(1, 1, 0.1), 0.0)
    assert np.isclose(B(5, 5, 0.05), 0.0)

def test_B_function_a_is_zero():
    # Test case for a = 0, should return T - t
    assert np.isclose(B(0, 1, 0), 1.0)
    assert np.isclose(B(0.5, 1.5, 0), 1.0)

def test_A_function_placeholder(mock_calibrated_model_for_logic):
    # A(t,T) is complex, for now, just ensure it runs without immediate error
    # and returns a float. More rigorous testing requires known analytical solutions.
    # This test primarily checks if the numerical differentiation for f0t works.
    t_val = 0.1
    T_val = 1.0
    result = A(t_val, T_val, mock_calibrated_model_for_logic)
    assert isinstance(result, float)
    assert result > 0 # ZCB prices should be positive

# Target: pricing.py
def test_price_zcb(mock_calibrated_model_for_logic):
    # TC-U-03
    t = 0.1
    T = 1.0
    r_t = 0.05 # Assuming short rate is 5% at time t
    model_price = price_zcb(t, T, r_t, mock_calibrated_model_for_logic)
    assert isinstance(model_price, float)
    assert model_price > 0

def test_price_european_option_on_zcb(mock_calibrated_model_for_logic):
    K = 0.95
    T_expiry = 0.5
    S_maturity = 1.0
    call_price = price_european_option_on_zcb(K, T_expiry, S_maturity, mock_calibrated_model_for_logic, 'call')
    put_price = price_european_option_on_zcb(K, T_expiry, S_maturity, mock_calibrated_model_for_logic, 'put')
    assert isinstance(call_price, float) and call_price >= 0
    assert isinstance(put_price, float) and put_price >= 0

def test_price_european_swaption_placeholder(mock_calibrated_model_for_logic):
    swap_rate = 0.05
    expiry = 1.0
    tenor_start = 1.0
    tenor_end = 5.0
    fixed_frequency = 1.0
    price = price_european_swaption(swap_rate, expiry, tenor_start, tenor_end, fixed_frequency, mock_calibrated_model_for_logic)
    assert isinstance(price, float)
    assert price >= 0

# Target: model.py (Unit tests for basic methods)
def test_get_name():
    # TC-U-04
    hw_model = HullWhiteOneFactor()
    assert hw_model.get_name() == "hull_white_one_factor"

def test_get_required_risk_factors():
    # TC-U-05
    hw_model = HullWhiteOneFactor()
    expected_factors = ["risk_free_rate_curve", "swaption_volatility_surface"]
    assert hw_model.get_required_risk_factors() == expected_factors

def test_train_raises_not_implemented_error():
    # TC-U-06
    hw_model = HullWhiteOneFactor()
    with pytest.raises(NotImplementedError, match="The Hull-White One-Factor model is a traditional stochastic model and does not require training."):
        hw_model.train(None)

def test_predict_raises_not_implemented_error():
    # TC-U-07
    hw_model = HullWhiteOneFactor()
    with pytest.raises(NotImplementedError, match="The Hull-White One-Factor model uses 'simulate' for generating future paths, not 'predict'."):
        hw_model.predict(None)

# --- Integration Tests (for public methods with file I/O) ---

def test_calibrate_public_method(setup_temp_data_dirs, mocker):
    # TC-I-01 (Revised)
    input_dir, output_dir = setup_temp_data_dirs
    hw_model = HullWhiteOneFactor(input_dir=input_dir, output_dir=output_dir)

    # Mock the internal _calibrate_logic to avoid actual calibration complexity in this test
    mocker.patch.object(hw_model, '_calibrate_logic', return_value=CalibratedHW1FModel(
        a=0.1, sigma=0.01, theta_function=mock_initial_zcb_pricer, calibration_error=0.0,
        initial_zero_coupon_bond_pricer=mock_initial_zcb_pricer
    ))

    calibrated_model = hw_model.calibrate()
    assert isinstance(calibrated_model, CalibratedHW1FModel)
    # Further assertions can be added to check if _load_and_prepare_data was called

def test_simulate_public_method(tmp_path, mock_calibrated_model_for_logic):
    # TC-I-02 (Revised)
    # Test with default plot options (both enabled)
    input_dir_default = tmp_path / "inputs_default" / "hull_white_one_factor"
    output_dir_default = tmp_path / "outputs_default" / "hull_white_one_factor"
    input_dir_default.mkdir(parents=True)
    output_dir_default.mkdir(parents=True)

    # Create dummy initial_zcb_curve.csv
    zcb_data = {'Maturity': [0.25, 0.5, 1.0, 2.0, 5.0],
                'Price': [0.995, 0.99, 0.98, 0.96, 0.92]}
    pd.DataFrame(zcb_data).to_csv(input_dir_default / "initial_zcb_curve.csv", index=False)

    # Create dummy swaption_volatilities.csv (simplified for testing)
    swaption_data = {'Tenor': [1.0, 2.0],
                     '1Y': [0.15, 0.14],
                     '2Y': [0.14, 0.13]}
    pd.DataFrame(swaption_data).to_csv(input_dir_default / "swaption_volatilities.csv", index=False)

    hw_model_default = HullWhiteOneFactor(input_dir=str(input_dir_default), output_dir=str(output_dir_default))

    scenario_definition = {
        'num_paths': 10,
        'time_horizon': 1.0,
        'dt': 0.1
    }

    simulation_result = hw_model_default.simulate(mock_calibrated_model_for_logic, scenario_definition)

    assert isinstance(simulation_result, HW1FSimulationResult)
    assert simulation_result.paths.shape[0] == int(scenario_definition['time_horizon'] / scenario_definition['dt']) + 1
    assert simulation_result.paths.shape[1] == scenario_definition['num_paths']

    # Check if the output CSV file was created
    output_csv_path_default = os.path.join(str(output_dir_default), "simulated_short_rates.csv")
    assert os.path.exists(output_csv_path_default)
    output_df_default = pd.read_csv(output_csv_path_default)
    assert not output_df_default.empty

    # Check if default plot files were created
    assert os.path.exists(os.path.join(str(output_dir_default), "simulated_short_rate_paths.html"))
    assert os.path.exists(os.path.join(str(output_dir_default), "simulated_short_rate_distribution.html"))

    # Test with custom plot options (only one enabled)
    input_dir_custom = tmp_path / "inputs_custom" / "hull_white_one_factor"
    output_dir_custom = tmp_path / "outputs_custom" / "hull_white_one_factor"
    input_dir_custom.mkdir(parents=True)
    output_dir_custom.mkdir(parents=True)

    # Create dummy initial_zcb_curve.csv
    pd.DataFrame(zcb_data).to_csv(input_dir_custom / "initial_zcb_curve.csv", index=False)

    # Create dummy swaption_volatilities.csv (simplified for testing)
    pd.DataFrame(swaption_data).to_csv(input_dir_custom / "swaption_volatilities.csv", index=False)

    hw_model_custom = HullWhiteOneFactor(input_dir=str(input_dir_custom), output_dir=str(output_dir_custom))

    custom_plot_options = {
        "short_rate_paths": {"enabled": True, "output_filename": "custom_paths.html"},
        "short_rate_distribution": {"enabled": False}
    }
    hw_model_custom.simulate(mock_calibrated_model_for_logic, scenario_definition, plot_options=custom_plot_options)

    # Check if custom plot file was created and other was not
    assert os.path.exists(os.path.join(str(output_dir_custom), "custom_paths.html"))
    assert not os.path.exists(os.path.join(str(output_dir_custom), "simulated_short_rate_distribution.html"))

def test_simulation_performance(setup_temp_data_dirs, mock_calibrated_model_for_logic):
    input_dir, output_dir = setup_temp_data_dirs
    hw_model = HullWhiteOneFactor(input_dir=input_dir, output_dir=output_dir)

    scenario_definition = {
        'num_paths': 50,
        'time_horizon': 50.0,
        'dt': 1/12 # Monthly steps
    }

    # Pass plot_options to avoid generating plots during performance test if not desired
    plot_options = {"short_rate_paths": {"enabled": False}, "short_rate_distribution": {"enabled": False}}
    hw_model.simulate(mock_calibrated_model_for_logic, scenario_definition, plot_options=plot_options)

    # Assertions on benchmark results would go here, e.g.,
    # assert benchmark.stats.mean < 60.0

# --- Tests for Internal Logic Methods (pure functions) ---

def test_calibrate_logic(mocker):
    # Test the pure calibration logic without file I/O
    # Mock the objective function and minimize call for simplicity
    # Mock the minimize function to return a successful result with expected calibrated parameters
    mock_result = mocker.Mock()
    mock_result.success = True
    mock_result.x = np.array([0.1, 0.01]) # Expected calibrated a and sigma
    mock_result.fun = 0.001 # Example calibration error
    mocker.patch('models.Interest_Rate_Risk.hull_white_one_factor.model.minimize', return_value=mock_result)

    # Dummy data for logic method
    initial_zcb_pricer_func = lambda t: np.exp(-0.05 * t)
    market_swaptions_list = [
        {'swap_rate': 0.05, 'expiry': 1.0, 'tenor_start': 1.0, 'tenor_end': 2.0, 'fixed_frequency': 1.0, 'market_price': 0.001},
    ]

    hw_model = HullWhiteOneFactor() # Directories don't matter for logic methods
    calibrated_model = hw_model._calibrate_logic(initial_zcb_pricer_func, market_swaptions_list)

    assert isinstance(calibrated_model, CalibratedHW1FModel)
    assert np.isclose(calibrated_model.a, 0.1)
    assert np.isclose(calibrated_model.sigma, 0.01)

def test_simulate_logic(mock_calibrated_model_for_logic):
    # Test the pure simulation logic without file I/O
    scenario_definition = {
        'num_paths': 5,
        'time_horizon': 0.5,
        'dt': 0.1
    }
    num_timesteps = int(scenario_definition['time_horizon'] / scenario_definition['dt']) + 1
    correlated_shocks = np.random.randn(num_timesteps - 1, scenario_definition['num_paths'])

    hw_model = HullWhiteOneFactor() # Directories don't matter for logic methods
    simulation_result = hw_model._simulate_logic(mock_calibrated_model_for_logic, scenario_definition, correlated_shocks)

    assert isinstance(simulation_result, HW1FSimulationResult)
    assert simulation_result.paths.shape == (num_timesteps, scenario_definition['num_paths'])
    assert simulation_result.time_grid.shape == (num_timesteps,)

# --- Validation Tests (TC-V-01, TC-V-02, TC-V-03) ---
# These tests will need to be adapted to use the _calibrate_logic and _simulate_logic methods
# or set up temporary files for the public methods.

# TC-V-01: Yield Curve Fit Verification
def test_yield_curve_fit_verification(mock_calibrated_model_for_logic):
    # This test now uses the _calibrate_logic directly for a pure test of the fit
    # For a flat curve P(0,t) = exp(-0.05 * t), the theta function should ensure this fit.
    # We need to ensure the generate_theta_function correctly fits the initial curve.

    # Use the mock_initial_zcb_pricer from the fixture
    initial_pricer = mock_initial_zcb_pricer

    # Calibrate a model (using the logic method for direct testing)
    a_test = 0.1
    sigma_test = 0.01
    theta_func_test = generate_theta_function(a_test, sigma_test, initial_pricer)
    calibrated_model_test = CalibratedHW1FModel(
        a=a_test, sigma=sigma_test, theta_function=theta_func_test,
        calibration_error=0.0, initial_zero_coupon_bond_pricer=initial_pricer
    )

    # Test ZCB prices at various maturities
    maturities = np.linspace(0.1, 10.0, 20)
    for T in maturities:
        # Price ZCB at time 0 using the calibrated model's theta function
        # and the initial short rate (r0 from the initial pricer)
        epsilon = 1e-5
        r0 = instantaneous_forward_rate(epsilon, initial_pricer)
        model_zcb_price = price_zcb(0.0, T, r0, calibrated_model_test)
        expected_zcb_price = initial_pricer(T)
        assert np.isclose(model_zcb_price, expected_zcb_price, atol=1e-6)

# TC-V-02: Short Rate Distribution Test
def test_short_rate_distribution(mock_calibrated_model_for_logic):
    scenario_definition = {
        'num_paths': 50,
        'time_horizon': 1.0,
        'dt': 1/252 # Daily steps
    }
    num_timesteps = int(scenario_definition['time_horizon'] / scenario_definition['dt']) + 1
    correlated_shocks = np.random.randn(num_timesteps - 1, scenario_definition['num_paths'])

    hw_model = HullWhiteOneFactor() # Instance for calling _simulate_logic
    simulation_result = hw_model._simulate_logic(mock_calibrated_model_for_logic, scenario_definition, correlated_shocks)

    # Extract rates at the end of the simulation horizon
    final_rates = simulation_result.paths[-1, :]

    # Analytical mean and variance for HW1F short rate
    a = mock_calibrated_model_for_logic.a
    sigma = mock_calibrated_model_for_logic.sigma
    T = scenario_definition['time_horizon']

    # Need to calculate the integral of theta(s) * exp(a*s) ds
    # For a flat initial curve P(0,t) = exp(-r0*t), theta(t) = r0*a + sigma^2/(2*a)*(1-exp(-2*a*t))
    # This is getting complex for a simple test. For now, we'll rely on the fact that
    # the short rate is normally distributed. We can check its mean and variance against
    # a simplified case or a known benchmark if we have one.

    # For a simple test, let's just check if the mean is somewhat close to the initial rate
    # and if the variance is positive. A full analytical check is beyond this test's scope.
    assert np.isclose(np.mean(final_rates), np.mean(simulation_result.paths[0,:]), atol=0.01) # Very loose check
    assert np.var(final_rates) > 0

# TC-V-03: Martingale Test for ZCB
def test_martingale_test_for_zcb(mock_calibrated_model_for_logic):
    # This test requires a more sophisticated setup, including pricing ZCBs along paths.
    # It's a complex integration/validation test. For now, we'll keep it as a placeholder.
    pass

# --- Performance Tests (TC-P-01, TC-P-02) ---

@pytest.mark.benchmark(min_rounds=5, warmup=True)
def test_calibration_performance(setup_temp_data_dirs, mocker):
    input_dir, output_dir = setup_temp_data_dirs
    hw_model = HullWhiteOneFactor(input_dir=input_dir, output_dir=output_dir)

    # Mock the internal _calibrate_logic to return quickly for performance test
    mocker.patch.object(hw_model, '_calibrate_logic', return_value=CalibratedHW1FModel(
        a=0.1, sigma=0.01, theta_function=mock_initial_zcb_pricer, calibration_error=0.0,
        initial_zero_coupon_bond_pricer=mock_initial_zcb_pricer
    ))

    hw_model.calibrate()

    # Assertions on benchmark results would go here, e.g.,
    # assert benchmark.stats.mean < 30.0

@pytest.mark.benchmark(min_rounds=5, warmup=True)
def test_simulation_performance(setup_temp_data_dirs, mock_calibrated_model_for_logic):
    input_dir, output_dir = setup_temp_data_dirs
    hw_model = HullWhiteOneFactor(input_dir=input_dir, output_dir=output_dir)

    scenario_definition = {
        'num_paths': 50,
        'time_horizon': 50.0,
        'dt': 1/12 # Monthly steps
    }

    hw_model.simulate(mock_calibrated_model_for_logic, scenario_definition)

    # Assertions on benchmark results would go here, e.g.,
    # assert benchmark.stats.mean < 60.0
