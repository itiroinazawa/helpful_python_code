from flask import Flask, request, jsonify

app = Flask(__name__)
ALLOWED_COUNTRIES = ["US", "CA"]

@app.route("/api/geo-protected")
def geo_protected():
    country = request.headers.get("X-Country")
    if country not in ALLOWED_COUNTRIES:
        return jsonify({"error": "Access denied"}), 403
    return jsonify({"message": "Access granted"})

if __name__ == "__main__":
    app.run(debug=True)
