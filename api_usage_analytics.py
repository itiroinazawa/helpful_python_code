import time
from flask import Flask, request, g

app = Flask(__name__)

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request(response):
    duration = time.time() - g.start_time
    log_data = {
        "method": request.method,
        "url": request.url,
        "status": response.status_code,
        "duration": duration
    }
    print(log_data)  # Replace with database or monitoring service
    return response

if __name__ == "__main__":
    app.run(debug=True)