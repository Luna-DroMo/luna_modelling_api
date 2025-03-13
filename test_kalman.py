import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from uuid import UUID

# API endpoint
BASE_URL = "http://localhost:8000/api/v1"


def test_kalman_filter():
    # Test data: noisy sine wave
    t = np.linspace(0, 10, 100)
    true_signal = np.sin(t)
    noise = np.random.normal(0, 0.2, len(t))
    noisy_signal = true_signal + noise

    # Account ID and API key
    # In a real scenario, you would get these from the database
    # For testing, we'll use a placeholder
    account_id = "1"  # Replace with an actual account ID
    api_key = "00000000-0000-0000-0000-000000000000"  # Replace with an actual API key

    # Prepare request data
    data = {
        "data": noisy_signal.tolist()
    }

    # Set headers with API key
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key
    }

    # Make POST request to Kalman filter endpoint
    try:
        response = requests.post(
            f"{BASE_URL}/{account_id}/kalman",
            headers=headers,
            data=json.dumps(data)
        )

        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            filtered_data = result["processed_results"]
            input_data = result["input_data"]

            # Plot results
            plt.figure(figsize=(10, 6))
            plt.plot(t, true_signal, 'g-', label='True Signal')
            plt.plot(t, input_data, 'b.', label='Noisy Measurements')
            plt.plot(t, filtered_data, 'r-', label='Kalman Filter')
            plt.legend()
            plt.title('Kalman Filter Results')
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.grid(True)
            plt.savefig('kalman_filter_results.png')
            plt.show()

            print("Kalman filter test completed successfully!")
            print(f"Results: {result}")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Exception: {str(e)}")


if __name__ == "__main__":
    test_kalman_filter()
