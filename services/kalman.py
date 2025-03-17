import numpy as np
from typing import List, Tuple, Any
from modelling.kalman_filter import KalmanFilter
from modelling.constants import F, H, Q, R, x0


def process_kalman_filter(input_data: List[List[float]]) -> List[float]:
    """
    Process input data through a Kalman filter.

    Args:
        input_data: List of lists of float values to be filtered
                   The inner list contains multiple observations as a time series

    Returns:
        List of filtered values

    Raises:
        ValueError: If input data is invalid
    """
    try:
        # Validate input structure
        if len(input_data) != 1:
            raise ValueError(
                "Input data must contain exactly one list of observations")

        if len(input_data[0]) < 1:
            raise ValueError(
                "Input data must contain at least one observation")

        # Extract the time series data from the inner list
        time_series = input_data[0]

        # Convert each element in the time series to a single-element observation
        # This creates a list of column vectors, each with one element
        observations = np.array([[x] for x in time_series])

        # Check if each observation has the correct dimension
        expected_dim = H.shape[0]
        if observations.shape[1] != expected_dim:
            raise ValueError(
                f"Each observation must have {expected_dim} element(s)")

        # Create and run Kalman filter with constants from constants.py
        kf = KalmanFilter(F=F, H=H, Q=Q, R=R, x0=x0)

        # Run the filter forward pass
        predictions_state, predictions_cov, predictions_obs = kf.forward(
            observations)

        # Convert numpy arrays to Python lists for JSON serialization
        filtered_data = [float(obs[0][0]) for obs in predictions_obs]

        return filtered_data

    except Exception as e:
        # Re-raise with more context
        raise ValueError(f"Error processing Kalman filter: {str(e)}")
