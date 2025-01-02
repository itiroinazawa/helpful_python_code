from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)

def validate_user(data):
    schema = UserSchema()
    try:
        return schema.load(data)
    except ValidationError as e:
        return {"errors": e.messages}

# Example Usage
data = {"username": "john", "email": "invalid-email"}
print(validate_user(data))
