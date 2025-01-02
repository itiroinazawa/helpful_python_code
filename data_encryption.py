from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_data(data):
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data).decode()

# Example Usage
encrypted = encrypt_data("Sensitive Information")
decrypted = decrypt_data(encrypted)
