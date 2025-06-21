import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("EMAIL_ENCRYPTION_KEY")
fernet = Fernet(KEY.encode())

def load_emails_encrypted(filepath="emails.json"):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "rb") as f:
        ciphertext = f.read()
    try:
        decrypted = fernet.decrypt(ciphertext)
        return json.loads(decrypted.decode())
    except Exception:
        return []

def save_emails_encrypted(email_list, filepath="emails.json"):
    plaintext = json.dumps(email_list).encode()
    encrypted = fernet.encrypt(plaintext)
    with open(filepath, "wb") as f:
        f.write(encrypted)
