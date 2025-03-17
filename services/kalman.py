import numpy as np
from typing import List, Tuple, Any
from modelling.kalman_filter import KalmanFilter
from modelling.constants import F, H, Q, R, x0


def process_kalman_filter(input_data: List[List[float]]) -> List[float]:
    """
    Process input data through a Kalman filter.

    Args:
        input_data: List of lists of float values to be filtered
                   Each inner list represents a week of observations

    Returns:
        List of filtered values

    Raises:
        ValueError: If input data is invalid
    """
    try:
        # Basic validation - ensure we have data
        if not input_data or any(len(week) == 0 for week in input_data):
            raise ValueError(
                "Input data must contain non-empty lists of observations")

        # Convert directly to numpy array
        observations = np.array(input_data)

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
