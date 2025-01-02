import requests

def send_with_retries(url, data, retries=3):
    for _ in range(retries):
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True
    return False

# Example Usage
send_with_retries("https://example.com/webhook", {"event": "test"})
