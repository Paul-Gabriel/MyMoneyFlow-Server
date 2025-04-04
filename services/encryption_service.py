from cryptography.fernet import Fernet

# Generate a key (do this once and store it securely)
# key = Fernet.generate_key()
# Save the key securely, e.g., in an environment variable or a secrets manager
SECRET_KEY = b'B3W2BhPZaDdUofpVe8L7P2Jnpxw6WUztXo_XEvPn-Ow='  # Replace with your actual key
cipher = Fernet(SECRET_KEY)

def encrypt_data(data: str) -> str:
    """Encrypts a string."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    """Decrypts a string."""
    return cipher.decrypt(data.encode()).decode()