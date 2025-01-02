from flask import Flask, request

app = Flask(__name__)

@app.route("/api/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    file.save(f"./uploads/{file.filename}")
    return {"message": "File uploaded successfully"}

if __name__ == "__main__":
    app.run(debug=True)
