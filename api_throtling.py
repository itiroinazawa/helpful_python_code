from flask import Flask, request, jsonify
from flask_limiter import Limiter

app = Flask(__name__)
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route("/api/resource")
@limiter.limit("10 per minute")  # Limit to 10 requests per minute per IP
def resource():
    return jsonify({"message": "Welcome to the API!"})

if __name__ == "__main__":
    app.run(debug=True)
