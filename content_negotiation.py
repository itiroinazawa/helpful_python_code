from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route("/api/resource")
def resource():
    data = {"message": "Hello, world!"}
    if request.headers.get("Accept") == "application/xml":
        xml_data = f"<response><message>{data['message']}</message></response>"
        return Response(xml_data, mimetype="application/xml")
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
