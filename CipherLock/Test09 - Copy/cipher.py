import os
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

# File path for storing ciphers
CIPHERS_FILE = "ciphers.json"
ADMIN_USERNAME = 'admin1'

# Initialize key and IV globally
key = get_random_bytes(32)  # 32 bytes for 256-bit key
iv = get_random_bytes(16)   # 16 bytes for IV

# Placeholder for cipher storage (in-memory dictionary)
ciphers_dict = {}

def load_ciphers():
    global ciphers_dict
    if os.path.exists(CIPHERS_FILE):
        with open(CIPHERS_FILE, "r") as file:
            ciphers_dict = json.load(file)

def save_ciphers():
    with open(CIPHERS_FILE, "w") as file:
        json.dump(ciphers_dict, file)

def store_cipher(username, name, password):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_password = password + (16 - len(password) % 16) * chr(16 - len(password) % 16)
    encrypted_password = cipher.encrypt(padded_password.encode())
    salted_cipher = b64encode(iv + encrypted_password).decode()
    if username not in ciphers_dict:
        ciphers_dict[username] = {}
    ciphers_dict[username][name] = salted_cipher
    save_ciphers()
    return salted_cipher

def decrypt_cipher(username, ciphertext):
    if username in ciphers_dict:
        salted_cipher = b64decode(ciphertext.encode())
        iv = salted_cipher[:16]
        encrypted_password = salted_cipher[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_password = cipher.decrypt(encrypted_password)
        decrypted_password = decrypted_password.rstrip(b"\x06").decode()  # Remove padding and decode
        return decrypted_password
    return None

def get_all_ciphers(username=None):
    if username == ADMIN_USERNAME:
        all_ciphers = []
        for user, ciphers in ciphers_dict.items():
            for name, cipher in ciphers.items():
                all_ciphers.append((user, name, cipher))  # Changed to tuple
        return all_ciphers
    return []



def clear_user_ciphers(username):
    if username in ciphers_dict:
        ciphers_dict[username] = {}
        save_ciphers()
        return True
    return False

# Load ciphers when module is imported
load_ciphers()
