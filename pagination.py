from flask import Flask, request, jsonify

app = Flask(__name__)

DATA = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]  # Example data

@app.route("/api/items")
def get_items():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(DATA[start:end])

if __name__ == "__main__":
    app.run(debug=True)
