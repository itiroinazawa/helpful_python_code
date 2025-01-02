# --- app.py ---
from flask import Flask
from database import db, initialize_database
from config import SECRET_KEY, DATABASE_URI
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
    attributes = db.Column(db.JSON, nullable=False)  # Stores user attributes

class Resource(db.Model):
    __tablename__ = 'resources'
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(50), nullable=False, unique=True)
    attributes = db.Column(db.JSON, nullable=False)  # Stores resource attributes

# --- database.py ---
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initialize_database():
    from models import User, Resource

    db.create_all()

    if not User.query.first():
        # Seed Users
        db.session.add_all([
            User(username="admin", attributes={"role": "admin", "department": "IT"}),
            User(username="manager", attributes={"role": "manager", "department": "HR"}),
            User(username="employee", attributes={"role": "employee", "department": "Finance"}),
        ])
        db.session.commit()

    if not Resource.query.first():
        # Seed Resources
        db.session.add_all([
            Resource(resource_name="confidential_report", attributes={"department": "IT", "classification": "high"}),
            Resource(resource_name="employee_handbook", attributes={"department": "HR", "classification": "low"}),
        ])
        db.session.commit()

# --- config.py ---
SECRET_KEY = "your_secret_key"
DATABASE_URI = "sqlite:///abac.db"

# --- auth.py ---
from flask import request, abort
from functools import wraps
import jwt
from config import SECRET_KEY
from models import User, Resource

# ABAC Policy Evaluation
def evaluate_policy(user_attributes, resource_attributes, action):
    # Example ABAC policy
    if action == "view" and user_attributes.get("department") == resource_attributes.get("department"):
        return True
    if action == "edit" and user_attributes.get("role") == "admin":
        return True
    return False

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_resource_by_name(resource_name):
    return Resource.query.filter_by(resource_name=resource_name).first()

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

def authorize(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            resource_name = kwargs.get("resource_name")
            resource = get_resource_by_name(resource_name)
            if not resource:
                abort(404, description="Resource not found")

            if not evaluate_policy(user.attributes, resource.attributes, action):
                abort(403, description="Forbidden")

            return func(*args, **kwargs)
        return wrapper
    return decorator

# --- routes.py ---
from flask import jsonify, request, abort
from auth import authorize
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

    @app.route('/resource/<string:resource_name>/view', methods=['GET'])
    @authorize('view')
    def view_resource(resource_name):
        return jsonify({"message": f"You are viewing resource: {resource_name}"})

    @app.route('/resource/<string:resource_name>/edit', methods=['POST'])
    @authorize('edit')
    def edit_resource(resource_name):
        return jsonify({"message": f"You edited resource: {resource_name}"})
