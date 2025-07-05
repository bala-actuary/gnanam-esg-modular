import numpy as np


def mean_reverting_step(I_t, theta, kappa, sigma, dt, dW):
    """Calculates one step of the mean-reverting process."""
    # Euler-Maruyama discretization of Ornstein-Uhlenbeck process
    return I_t + kappa * (theta - I_t) * dt + sigma * np.sqrt(dt) * dW
