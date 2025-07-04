import numpy as np


def fx_gbm_step(S_t, r_d, r_f, sigma, dt, dW):
    """Calculates one step of the FX GBM process."""
    return S_t * np.exp((r_d - r_f - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dW)
