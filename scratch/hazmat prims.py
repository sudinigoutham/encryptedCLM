# Databricks notebook source
# super basic encryption/decryption
def encrypt_message(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_char = chr(ord(char) ^ key)
        encrypted_message += encrypted_char
    return encrypted_message

def decrypt_message(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_char = chr(ord(char) ^ key)
        decrypted_message += decrypted_char
    return decrypted_message

# COMMAND ----------

# a more exiciting version 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_message(message, key):
    backend = default_backend()
    key_bytes = key.to_bytes(32, byteorder='big')  # Adjust key size as needed
    cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padded_message = message + ' ' * (16 - len(message) % 16)  # Padding to ensure block size compatibility
    encrypted_message = encryptor.update(padded_message.encode()) + encryptor.finalize()
    return encrypted_message.hex()

def decrypt_message(encrypted_message, key):
    encrypted_message_bytes = bytes.fromhex(encrypted_message)
    backend = default_backend()
    key_bytes = key.to_bytes(32, byteorder='big')  # Adjust key size as needed
    cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
    return decrypted_message.rstrip().decode()  # Remove padding and decode

# COMMAND ----------

encrypt_message("Spark is awesome", 5)

# COMMAND ----------

encrypt_message("Spark is awesome", 5)

# COMMAND ----------

decrypt_message('6b382772e73e622dcfedb1ed70c486f526912f568ee4cf1e45fa847a8b0cde67', 5)
