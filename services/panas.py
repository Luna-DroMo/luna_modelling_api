import numpy as np
from modelling.constants import panas_loadings


def process_panas_form(form_data):
    """
    Process a single PANAS form to get PA and NA scores.

    Args:
        form_data: List or array of 20 Likert scale responses (0-5)
                  in the order of the PANAS questionnaire

    Returns:
        tuple: (pa, na) - Positive Affect and Negative Affect scores
    """
    # Convert to numpy array if not already
    form_data = np.array(form_data, dtype=float)

    # Validate input
    if len(form_data) != 20:
        raise ValueError(
            f"PANAS form data must have 20 items, got {len(form_data)}")

    # Calculate PA and NA using matrix multiplication
    # This is exactly the same logic as in your original code:
    # pa_na = (form_data @ panas_loadings).flatten()
    pa_na = (form_data @ panas_loadings).flatten()

    return pa_na  # Returns [PA, NA] array
