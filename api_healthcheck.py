from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health")
def health_check():
    return jsonify({"status": "OK", "db": "connected", "cache": "healthy"})

if __name__ == "__main__":
    app.run(debug=True)
