# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC A basic example of an encryption method that returns the same string every time, using the unicode code point of each one character string rising to the key value and put back together.  The encryption and decrpytion functions are technically the same.  

# COMMAND ----------

key = 327

# COMMAND ----------

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

encrypt_message("Spark is awesome", key)

# COMMAND ----------

decrypt_message('ĔķĦĵĬŧĮĴŧĦİĢĴĨĪĢ', key)

# COMMAND ----------

# MAGIC %md
# MAGIC This version uses the crpyotoraphy package's hazmat classes and methods for creating a Cipher with a key and returns the same string each time.  The key used it still an integer turned to bytes.  

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

encrypt_message("Spark is awesome", key)

# COMMAND ----------

decrypt_message('b0a74079c722720d676fdcd84c0ba3378601552a448929f26ee69e7e55e507dd', key)

# COMMAND ----------

# MAGIC %md
# MAGIC Switch to use a bytes style key directly.  

# COMMAND ----------

import secrets

key = secrets.token_bytes(32)

# COMMAND ----------

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_message(message, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padded_message = message + ' ' * (16 - len(message) % 16)  # Padding to ensure block size compatibility
    encrypted_message = encryptor.update(padded_message.encode()) + encryptor.finalize()
    return encrypted_message.hex()

def decrypt_message(encrypted_message, key):
    encrypted_message_bytes = bytes.fromhex(encrypted_message)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
    return decrypted_message.rstrip().decode()  # Remove padding and decode

# COMMAND ----------

encrypt_message("Spark is awesome", key)

# COMMAND ----------

decrypt_message('408749fe92296692ccc1c8225587973d47b5be4debd651664b1970028d7d6fea', key)

# COMMAND ----------

decrypt_message(encrypt_message("This should work fine!", key), key)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC We can make the key more complicated by using the same method as the Fernet class, and supply a salt that is truly random using the os.urandom method.  If the key and the salt are stored and used the same, then the value returned from the encrpytion function will always be the same, otherwise if we allow the salt to vary we can have different encrpyted strings, but the key will decrypt the message.  

# COMMAND ----------

from cryptography.fernet import Fernet

# COMMAND ----------

key = Fernet.generate_key().decode()

# COMMAND ----------

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets

# COMMAND ----------

salt = secrets.token_bytes(16)

# COMMAND ----------

salt

# COMMAND ----------

salt_hex = salt.hex()

# COMMAND ----------

salt_hex

# COMMAND ----------

from databricks.sdk import dbutils

# COMMAND ----------

salt_bytes = bytes.fromhex(salt_hex)

# COMMAND ----------

salt_bytes == salt

# COMMAND ----------

def get_key_bytes(key_str, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64decode(key_str)
    return kdf.derive(key)

def encrypt_message(message, key_str, salt):
    key_bytes = get_key_bytes(key_str, salt)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(salt + encrypted_message).decode()

def decrypt_message(encrypted_message, key_str):
    encrypted_message_bytes = base64.urlsafe_b64decode(encrypted_message)
    salt = encrypted_message_bytes[:16]
    encrypted_message_bytes = encrypted_message_bytes[16:]
    key_bytes = get_key_bytes(key_str, salt)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_padded_message = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()
    return decrypted_message.decode()

# COMMAND ----------

encrypt_message("Spark is awesome", key, salt)

# COMMAND ----------

decrypt_message(encrypt_message("Spark is awesome", key, salt), key)

# COMMAND ----------

# MAGIC %md
# MAGIC What about Null values?

# COMMAND ----------

encrypt_message(None, key, salt)
