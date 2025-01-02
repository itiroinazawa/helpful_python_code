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
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)

class Permission(db.Model):
    __tablename__ = 'permissions'
    permission_id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(50), nullable=False, unique=True)

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.permission_id'), nullable=False)

# --- database.py ---
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initialize_database():
    from models import Role, Permission, RolePermission, User

    db.create_all()

    if not Role.query.first():
        # Seed Roles
        admin_role = Role(role_name="Admin")
        manager_role = Role(role_name="Manager")
        user_role = Role(role_name="User")
        db.session.add_all([admin_role, manager_role, user_role])
        db.session.commit()

        # Seed Permissions
        read_perm = Permission(permission_name="READ")
        write_perm = Permission(permission_name="WRITE")
        delete_perm = Permission(permission_name="DELETE")
        update_perm = Permission(permission_name="UPDATE")
        db.session.add_all([read_perm, write_perm, delete_perm, update_perm])
        db.session.commit()

        # Seed Role-Permissions
        db.session.add_all([
            RolePermission(role_id=admin_role.role_id, permission_id=read_perm.permission_id),
            RolePermission(role_id=admin_role.role_id, permission_id=write_perm.permission_id),
            RolePermission(role_id=admin_role.role_id, permission_id=delete_perm.permission_id),
            RolePermission(role_id=admin_role.role_id, permission_id=update_perm.permission_id),
            RolePermission(role_id=manager_role.role_id, permission_id=read_perm.permission_id),
            RolePermission(role_id=manager_role.role_id, permission_id=write_perm.permission_id),
            RolePermission(role_id=user_role.role_id, permission_id=read_perm.permission_id),
        ])
        db.session.commit()

        # Seed Users
        db.session.add_all([
            User(username="admin", role_id=admin_role.role_id),
            User(username="manager", role_id=manager_role.role_id),
            User(username="user", role_id=user_role.role_id),
        ])
        db.session.commit()

# --- config.py ---
SECRET_KEY = "your_secret_key"
DATABASE_URI = "sqlite:///rbac.db"

# --- auth.py ---
from flask import request, abort
from functools import wraps
import jwt
from config import SECRET_KEY
from models import User, Permission, RolePermission

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_role_permissions(role_id):
    return [rp.permission_id for rp in RolePermission.query.filter_by(role_id=role_id).all()]

def has_permission(user, required_permission):
    role_permissions = get_role_permissions(user.role_id)
    permission = Permission.query.filter_by(permission_name=required_permission).first()
    if permission:
        return permission.permission_id in role_permissions
    return False

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

def authorize(required_permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not has_permission(user, required_permission):
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

    @app.route('/resource', methods=['GET'])
    @authorize('READ')
    def get_resource():
        return jsonify({"message": "This is a protected resource."})

    @app.route('/resource', methods=['POST'])
    @authorize('WRITE')
    def create_resource():
        return jsonify({"message": "Resource created successfully."})

    @app.route('/resource', methods=['DELETE'])
    @authorize('DELETE')
    def delete_resource():
        return jsonify({"message": "Resource deleted successfully."})
