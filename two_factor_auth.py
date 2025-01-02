import pyotp

def generate_otp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()

# Example Usage
secret = pyotp.random_base32()
otp = generate_otp(secret)
print(f"Your OTP is: {otp}")
