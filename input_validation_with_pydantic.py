from pydantic import BaseModel, ValidationError

class UserData(BaseModel):
    username: str
    email: str
    age: int

def validate_input(data):
    try:
        user = UserData(**data)
        return user
    except ValidationError as e:
        return {"error": e.errors()}

# Example Usage
data = {"username": "john", "email": "john@example.com", "age": 25}
validated = validate_input(data)
