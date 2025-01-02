def sanitize_input(input_string):
    return input_string.replace("'", "''")

# Example Usage
print(sanitize_input("SELECT * FROM users WHERE name='admin'"))