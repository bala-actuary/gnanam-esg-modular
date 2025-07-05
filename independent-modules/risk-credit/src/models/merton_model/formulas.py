import numpy as np
from scipy.stats import norm


def d1(S, K, T, r, sigma):
    """Calculates the d1 term of the Black-Scholes formula."""
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma):
    """Calculates the d2 term of the Black-Scholes formula."""
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def black_scholes_call(S, K, T, r, sigma):
    """Calculates the Black-Scholes call option price."""
    d_1 = d1(S, K, T, r, sigma)
    d_2 = d2(S, K, T, r, sigma)
    return S * norm.cdf(d_1) - K * np.exp(-r * T) * norm.cdf(d_2)


def gbm_step(S_t, mu, sigma, dt, dW):
    """Calculates one step of the GBM process for asset value simulation."""
    return S_t * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * dW)
