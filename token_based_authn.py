import jwt
import datetime

SECRET_KEY = "your_secret_key"

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def refresh_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return generate_token(payload["user_id"])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")

# Usage
token = generate_token(123)
refreshed_token = refresh_token(token)