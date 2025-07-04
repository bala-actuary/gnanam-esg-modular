import numpy as np


def gbm_step(S_t, mu, sigma, dt, dW):
    """Calculates one step of the GBM process."""
    return S_t * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dW)
