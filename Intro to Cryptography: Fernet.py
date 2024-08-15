# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Cryptography: Fernet
# MAGIC
# MAGIC Fernet guarantees that a message encrypted using it can not be manipulated or read without its key.  Fernet is a type of "symmetric encrpytion", also known as "secret-key" encrpytion.  
# MAGIC
# MAGIC Messages encrpyted with the secret key can be retreived only with the key.  Keys must be base64 encoded 32 bit strings. 
# MAGIC
# MAGIC Keys can be rotated using MultiFernet, or keys can be generated using a passphrase.  
# MAGIC
# MAGIC Keep your keys safe!  If a key is lost then the encrypted data can not be returned to its original form.  If a key is stolen, then a nefarious actor can decrypt senestive data.  
# MAGIC
# MAGIC For more information and full documentation, please visit the following page:  
# MAGIC
# MAGIC [https://cryptography.io/en/latest/fernet/](https://cryptography.io/en/latest/fernet/)
# MAGIC
# MAGIC *** 
# MAGIC   
# MAGIC   
# MAGIC ## Basic Use

# COMMAND ----------

# DBTITLE 1,Import the Python Cryptography with Fernet Module
from cryptography.fernet import Fernet

# COMMAND ----------

# DBTITLE 1,Generating a Key with Fernet in Python
# Generate a key
key = Fernet.generate_key()
key

# COMMAND ----------

# DBTITLE 1,Create a Cipher Using the Key
cipher_suite = Fernet(key)

# COMMAND ----------

# DBTITLE 1,Encrypting a Message with the Cipher
# Encrypt a message
message = "Secret Message"
encrypted_text = cipher_suite.encrypt(message.encode())
display(encrypted_text)

# COMMAND ----------

# DBTITLE 1,Decrypting and Displaying Encrypted Text
# Decrypt the message
decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
display(decrypted_text)

# COMMAND ----------

# MAGIC %md
# MAGIC ***
# MAGIC
# MAGIC ## Using Multiple Keys

# COMMAND ----------

# DBTITLE 1,Import MultiFernet
from cryptography.fernet import Fernet, MultiFernet

# COMMAND ----------

# MAGIC %md
# MAGIC Using multiple keys essentailly means creating more than one cypher.  We combine the cyphers using MultiFernet. 

# COMMAND ----------

# DBTITLE 1,Create a new cypher
# generate a new key to be used for encryption 
new_key = Fernet.generate_key()

# create a new cypher from the key
new_cipher = Fernet(new_key)

# create a list of ciphers
cipher_list = [new_cipher, cipher_suite]

# create a multi-cipher
multi_cipher = MultiFernet(cipher_list)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC With a MultiFernet, new messages are encrypted with the first key in the list, and each key is used to attempt to decrypt.  If the correct key is not found in the list then an exception is thrown.  

# COMMAND ----------

# DBTITLE 1,Decrypt the original message
multi_cipher.decrypt(encrypted_text).decode()

# COMMAND ----------

# DBTITLE 1,Encrypting a Message with Multi Cypher Technique
new_message = "This is a brand new message"
new_encrypted_message = multi_cipher.encrypt(new_message.encode())
display(new_encrypted_message)

# COMMAND ----------

# MAGIC %md
# MAGIC The newly encrpyted message can be decrypted with the latest cypher:

# COMMAND ----------

# DBTITLE 1,Decrpt the new message
new_cipher.decrypt(new_encrypted_message).decode()

# COMMAND ----------

# MAGIC %md
# MAGIC Or the multi-cypher: 

# COMMAND ----------


multi_cipher.decrypt(new_encrypted_message).decode()

# COMMAND ----------

# MAGIC %md
# MAGIC But not the original cypher:  

# COMMAND ----------

try:
    decrypted_text = cipher_suite.decrypt(new_encrypted_message).decode()
    display(decrypted_text)
except Exception as e:
    display(f"An error occurred: InvalidToken")

# COMMAND ----------

# MAGIC %md
# MAGIC ***
# MAGIC
# MAGIC ## Rotating Keys
# MAGIC
# MAGIC In addition to using more than one key, keys may be rotated allowing for previously encrpyted messages to be re-encrpyted using the latest key (first key in the list used for the MultiFernet).  This implies that keys eventually can be dropped once all previously encrypted messages have been rotated to the new key.   

# COMMAND ----------

# DBTITLE 1,Yet Another Cypher
# create a third key and a third cypher based on that key
third_key = Fernet.generate_key()
third_cipher = Fernet(third_key)

# add it to the front of the list
cipher_list.insert(0, third_cipher)

# COMMAND ----------

# DBTITLE 1,New multi-cipher
multi_cipher = MultiFernet(cipher_list)

# COMMAND ----------

# DBTITLE 1,Display the original encryped text from "Secret Message"
# Display the origina secret text from the first "Secret Message"
encrypted_text

# COMMAND ----------

# MAGIC %md
# MAGIC Now we'll re-encrypt the original "Secret Message" by rotating the keys:  

# COMMAND ----------

# DBTITLE 1,Re-encrypt
encrypted_text = multi_cipher.rotate(encrypted_text)
encrypted_text

# COMMAND ----------

# MAGIC %md 
# MAGIC The new cipher can decrypt this message: 

# COMMAND ----------

third_cipher.decrypt(encrypted_text).decode()

# COMMAND ----------

# MAGIC %md
# MAGIC But the original cipher suite no longer has the appropriate key.  

# COMMAND ----------

try:
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    display(decrypted_text)
except Exception as e:
    display(f"An error occurred: InvalidToken")

# COMMAND ----------

# MAGIC %md
# MAGIC *** 
# MAGIC
# MAGIC ## Using a Passphrase to Generate Keys 
# MAGIC
# MAGIC A passphrase may be used to generate a key, making it harder to lose a key at the risk of having others remember your passphrase if it becomes known.  Any key generating function may be used to convert the passphrase, so long as the resulting key is **base64 encoded** and 32 bytes.  

# COMMAND ----------

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
password = b"password"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)
token = f.encrypt(b"Secret message!")
token

# COMMAND ----------

f.decrypt(token)
