import numpy as np
from typing import List, Tuple, Any, Dict, Optional
from modelling.kalman_filter import KalmanFilter
from modelling.constants import F, H, Q, R, x0


def process_kalman_filter(input_data: List[List[float]], save: bool = False) -> Dict[str, List[float]]:
    """
    Process input data through a Kalman filter.

    Args:
        input_data: List of lists of float values to be filtered
                   Each inner list represents a week of observations
        save: Whether to save the results to the database (not implemented yet)

    Returns:
        Dictionary containing filtered values, raw state, and smoothed state

    Raises:
        ValueError: If input data is invalid
    """
    try:
        # Basic validation - ensure we have data
        if not input_data or any(len(week) == 0 for week in input_data):
            raise ValueError(
                "Input data must contain non-empty lists of observations")

        if save:
            return {"message": "Results saved to database"}
        else:
            # Convert directly to numpy array
            observations = np.array(input_data)

            # Create and run Kalman filter with constants from constants.py
            kf = KalmanFilter(F=F, H=H, Q=Q, R=R, x0=x0)

            # Run the filter forward pass
            raw_state, predictions_cov, predictions_obs = kf.forward(
                observations)

            # Run the smoother
            smooth_state, cov_smooth, K = kf.smooth(
                np.array(raw_state), np.array(predictions_cov)
            )

            # Flatten the arrays for easier handling
            raw_state_flat = np.array(raw_state).flatten().tolist()
            smooth_state_flat = np.array(smooth_state).flatten().tolist()

            # Convert numpy arrays to Python lists for JSON serialization
            filtered_data = [float(obs[0][0]) for obs in predictions_obs]

            # If save is True, we would save the results to the database here
            # Not implemented yet

            # Return all the data
            return {
                "filtered_data": filtered_data,
                "raw_state": raw_state_flat,
                "smooth_state": smooth_state_flat
            }

    except Exception as e:
        # Re-raise with more context
        raise ValueError(f"Error processing Kalman filter: {str(e)}")
