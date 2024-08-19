-- Databricks notebook source
DECLARE OR REPLACE VARIABLE catalog_use STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SELECT catalog_use;

-- COMMAND ----------

-- CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encrypt_text') (input_text STRING, key STRING)
-- RETURNS STRING
-- LANGUAGE PYTHON
-- AS $$
--   import cryptography.fernet as fernet
--   cipher_suite = fernet.Fernet(key.encode())
--   encrypted_text = cipher_suite.encrypt_at_time(input_text.encode(), 1723705758)
--   return encrypted_text.decode()
-- $$;

-- COMMAND ----------

-- CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.decrypt_text') (input_text STRING, key STRING)
-- RETURNS STRING
-- LANGUAGE PYTHON
-- AS $$
--   import cryptography.fernet as fernet
--   cipher_suite = fernet.Fernet(key.encode())
--   decrypted_text = cipher_suite.decrypt(input_text.encode())
--   return decrypted_text.decode()
-- $$;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encrypt_text') (input_text STRING, key_str STRING, salt STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives import padding
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend
  from cryptography.hazmat.primitives import hashes
  from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
  import base64

  backend = default_backend()
  kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bytes.fromhex(salt),
        iterations=100000,
        backend=backend
    )
  key = base64.urlsafe_b64decode(key_str)
  key_bytes = kdf.derive(key)
  cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  padder = padding.PKCS7(128).padder()
  padded_data = padder.update(input_text.encode()) + padder.finalize()
  encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
  return base64.urlsafe_b64encode(encrypted_message).decode()
$$;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.decrypt_text') (input_text STRING, key_str STRING, salt STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives import padding
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend
  from cryptography.hazmat.primitives import hashes
  from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
  import base64

  backend = default_backend()
  kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bytes.fromhex(salt),
        iterations=100000,
        backend=backend
    )
  key = base64.urlsafe_b64decode(key_str)
  key_bytes = kdf.derive(key)
  cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()
  encrypted_message_bytes = base64.urlsafe_b64decode(input_text)
  decrypted_padded_message = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
  unpadder = padding.PKCS7(128).unpadder()
  decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()
  return decrypted_message.decode()
$$;

-- COMMAND ----------

EXECUTE IMMEDIATE "select 
  IDENTIFIER(catalog_use || '.hv_claims.encrypt_text')('Spark is awesome', secret('encryptionCLM-demo', 'encryption_key'), secret('encryptionCLM-demo', 'encryption_salt')) as encrypted_text"

-- COMMAND ----------

EXECUTE IMMEDIATE "select
  IDENTIFIER(catalog_use || '.hv_claims.decrypt_text')('6Mxhau5IcNtDb2r2_Bcez_6wRrCWd7tTe92ii4vBZJQ=', secret('encryptionCLM-demo', 'encryption_key'), secret('encryptionCLM-demo', 'encryption_salt')) as decrypted_text"
