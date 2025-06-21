import os
'''
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
print(f"[DEBUG] Current working dir: {os.getcwd()}")
'''
import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

def get_fernet():
    load_dotenv()
    key = os.getenv("EMAIL_ENCRYPTION_KEY")
    print(f"[DEBUG] Fernet key raw value: {repr(key)}")
    if not key:
        raise ValueError("EMAIL_ENCRYPTION_KEY is missing or empty")
    return Fernet(key.encode())

def load_emails_encrypted(filepath="emails.json"):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "rb") as f:
        ciphertext = f.read()
    try:
        fernet = get_fernet()
        decrypted = fernet.decrypt(ciphertext)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}")
        return []

def save_emails_encrypted(email_list, filepath="emails.json"):
    plaintext = json.dumps(email_list).encode()
    fernet = get_fernet()
    encrypted = fernet.encrypt(plaintext)
    with open(filepath, "wb") as f:
        f.write(encrypted)