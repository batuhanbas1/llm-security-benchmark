import requests

def fetch_data():
    response = requests.get("https://example.com/api/data", timeout=5)
    response.raise_for_status()
    return response.json()