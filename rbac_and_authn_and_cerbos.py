# --- app.py ---
from flask import Flask
from database import db, initialize_database
from config import SECRET_KEY, DATABASE_URI, CERBOS_HOST
from routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
register_routes(app)

@app.before_first_request
def setup():
    initialize_database()

if __name__ == '__main__':
    app.run(debug=True)

# --- models.py ---
from database import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)  # Simplified for Cerbos

# --- database.py ---
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initialize_database():
    from models import User

    db.create_all()

    if not User.query.first():
        # Seed Users
        db.session.add_all([
            User(username="admin", role="admin"),
            User(username="manager", role="manager"),
            User(username="user", role="user"),
        ])
        db.session.commit()

# --- config.py ---
SECRET_KEY = "your_secret_key"
DATABASE_URI = "sqlite:///cerbos_rbac.db"
CERBOS_HOST = "http://localhost:3592"  # Replace with your Cerbos instance URL

# --- auth.py ---
from flask import request, abort
import jwt
import requests
from config import SECRET_KEY, CERBOS_HOST
from models import User


def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_current_user():
    token = request.headers.get('Authorization')
    if not token:
        abort(401, description="Missing token")

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = get_user_by_id(decoded_token['user_id'])
        if not user:
            abort(401, description="Invalid user")
        return user
    except jwt.ExpiredSignatureError:
        abort(401, description="Token expired")
    except jwt.InvalidTokenError:
        abort(401, description="Invalid token")

def cerbos_authorize(action, resource):
    user = get_current_user()

    payload = {
        "principal": {
            "id": user.user_id,
            "roles": [user.role],
            "attributes": {
                "username": user.username
            }
        },
        "resource": {
            "kind": resource,
            "id": "1",  # Adjust resource ID as necessary
            "attributes": {}
        },
        "actions": [action]
    }

    response = requests.post(f"{CERBOS_HOST}/api/check", json=payload)

    if response.status_code != 200:
        abort(500, description="Authorization service error")

    result = response.json()
    if not result.get("results", [{}])[0].get("isAllowed", False):
        abort(403, description="Forbidden")

# --- routes.py ---
from flask import jsonify, request, abort
from auth import cerbos_authorize
from models import User
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

def register_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        user = User.query.filter_by(username=username).first()

        if not user:
            abort(401, description="Invalid credentials")

        token = jwt.encode({
            "user_id": user.user_id,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

    @app.route('/resource/<string:resource_name>/<string:action>', methods=['GET', 'POST', 'DELETE'])
    def manage_resource(resource_name, action):
        cerbos_authorize(action, resource_name)
        return jsonify({"message": f"Action {action} on resource {resource_name} completed successfully."})
