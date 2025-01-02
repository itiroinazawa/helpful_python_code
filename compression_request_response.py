from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route("/api/data")
def get_data():
    large_data = {"data": "x" * 10000}
    return jsonify(large_data)

if __name__ == "__main__":
    app.run(debug=True)
