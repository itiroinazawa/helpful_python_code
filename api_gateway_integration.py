import requests

def forward_request(api_gateway_url, endpoint, data):
    response = requests.post(f"{api_gateway_url}/{endpoint}", json=data)
    return response.json()

# Example Usage
result = forward_request("https://api.gateway.com", "endpoint", {"key": "value"})
print(result)
