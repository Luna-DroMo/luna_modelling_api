import requests
import json
import uuid
import sys

# API endpoint
BASE_URL = "http://localhost:8000/api/v1"

# Replace with your actual API key and account ID
API_KEY = "your-api-key-here"  # Replace with your actual API key
ACCOUNT_ID = 1  # Replace with your actual account ID

# Sample PANAS form data (20 items, values between 1-5)
sample_data = {
    "results": [5, 4, 5, 2, 4, 1, 5, 2, 5, 1, 4, 2, 5, 4, 5, 4, 5, 2, 3, 1]
}


def test_panas_endpoint():
    """Test the PANAS endpoint with sample data."""
    url = f"{BASE_URL}/{ACCOUNT_ID}/panas"

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=sample_data)

        # Print status code and response
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\nPANAS Results:")
            print(f"Positive Affect (PA): {result['positive_affect']}")
            print(f"Negative Affect (NA): {result['negative_affect']}")
            print("\nFull Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    test_panas_endpoint()
