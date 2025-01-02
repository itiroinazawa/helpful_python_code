import logging
from functools import wraps
from flask import jsonify
import inspect

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_errors.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def error_handler(func):
    """
    A decorator to handle exceptions in API endpoints.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        service_name = inspect.getfile(func)
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"ValueError in {service_name}.{func.__name__}: {e}")
            return jsonify({"error": "Invalid input", "message": str(e)}), 400
        except KeyError as e:
            logger.error(f"KeyError in {service_name}.{func.__name__}: {e}")
            return jsonify({"error": "Missing key", "message": str(e)}), 400
        except Exception as e:
            logger.exception(f"Unhandled exception in {service_name}.{func.__name__}")
            return jsonify({"error": "Internal server error", "message": "An unexpected error occurred."}), 500
    return wrapper

# Example usage with Flask
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/example', methods=['POST'])
@error_handler
def example_endpoint():
    data = request.get_json()
    if not data:
        raise ValueError("No JSON payload provided")
    if "key" not in data:
        raise KeyError("'key' is required in the payload")
    return jsonify({"message": "Success", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True)
