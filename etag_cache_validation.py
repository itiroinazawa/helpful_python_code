from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/resource")
def resource():
    data = {"id": 1, "value": "important-data"}
    etag = f"etag-{data['id']}"
    if request.headers.get("If-None-Match") == etag:
        return "", 304
    return jsonify(data), 200, {"ETag": etag}

if __name__ == "__main__":
    app.run(debug=True)
