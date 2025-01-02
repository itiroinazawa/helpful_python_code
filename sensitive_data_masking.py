def mask_sensitive_data(data):
    if "password" in data:
        data["password"] = "***"
    return data

# Example Usage
print(mask_sensitive_data({"username": "user", "password": "secret"}))
