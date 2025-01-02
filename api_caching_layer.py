import redis
from flask import Flask, jsonify

app = Flask(__name__)
cache = redis.Redis(host="localhost", port=6379)

@app.route("/api/data")
def get_data():
    cached_data = cache.get("data_key")
    if cached_data:
        return jsonify({"data": cached_data.decode("utf-8")})
    # Simulate fetching data
    data = "Expensive computation result"
    cache.setex("data_key", 3600, data)  # Cache for 1 hour
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run(debug=True)