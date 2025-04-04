from cryptography.fernet import Fernet
from datetime import datetime

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

def encrypt_number(number: float) -> str:
    """Encrypts a number (float or int)."""
    return encrypt_data(str(number))

def decrypt_number(encrypted_number: str) -> float:
    """Decrypts an encrypted number and returns it as a float."""
    return float(decrypt_data(encrypted_number))

def encrypt_datetime(dt: datetime) -> str:
    """Encrypts a datetime object."""
    return encrypt_data(dt.isoformat())

def decrypt_datetime(encrypted_dt: str) -> datetime:
    """Decrypts an encrypted datetime string and returns a datetime object."""
    return datetime.fromisoformat(decrypt_data(encrypted_dt))

def encrypt_user_dict(data: dict) -> dict:
    """Encrypts values in a dictionary."""
    data['nume'] = encrypt_data(data['nume'])
    data['prenume'] = encrypt_data(data['prenume'])
    data['email'] = encrypt_data(data['email'])
    data['parola'] = encrypt_data(data['parola'])
    data['venit'] = encrypt_number(data['venit'])
    data['procentNecesitati'] = encrypt_number(data['procentNecesitati'])
    data['procentDorinte'] = encrypt_number(data['procentDorinte'])
    data['procentEconomii'] = encrypt_number(data['procentEconomii'])
    return data

def encrypt_payment_dict(data: dict) -> dict:
    """Encrypts values in a payment dictionary."""
    data['categorie'] = encrypt_data(data['categorie'])
    data['descriere'] = encrypt_data(data['descriere'])
    data['suma'] = encrypt_number(data['suma'])
    data['data'] = encrypt_datetime(data['data'])
    return data

def decrypt_user_dict(data: dict) -> dict:
    """Decrypts values in a dictionary."""
    data['nume'] = decrypt_data(data['nume'])
    data['prenume'] = decrypt_data(data['prenume'])
    data['email'] = decrypt_data(data['email'])
    data['parola'] = decrypt_data(data['parola'])
    data['venit'] = decrypt_data(data['venit'])
    data['procentNecesitati'] = decrypt_number(data['procentNecesitati'])
    data['procentDorinte'] = decrypt_number(data['procentDorinte'])
    data['procentEconomii'] = decrypt_number(data['procentEconomii'])
    return data

def decrypt_payment_dict(data: dict) -> dict:
    """Decrypts values in a payment dictionary."""
    data['categorie'] = decrypt_data(data['categorie'])
    data['descriere'] = decrypt_data(data['descriere'])
    data['suma'] = decrypt_number(data['suma'])
    data['data'] = decrypt_datetime(data['data'])
    return data

if __name__ == "__main__":
    # Example usage
    original_date = datetime.now()
    print("Original Date:", original_date)

    encrypted_date = encrypt_datetime(original_date)
    print("Encrypted Date:", encrypted_date)

    decrypted_date = decrypt_datetime(encrypted_date)
    print("Decrypted Date:", decrypted_date)