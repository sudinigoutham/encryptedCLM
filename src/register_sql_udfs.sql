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

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend
  backend = default_backend()
  key_bytes = key.to_bytes(32, byteorder='big') 
  cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  padded_message = input_text + ' ' * (16 - len(input_text) % 16) 
  encrypted_message = encryptor.update(padded_message.encode()) + encryptor.finalize()
  return encrypted_message.hex()
$$;

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

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.decrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend
  encrypted_message_bytes = bytes.fromhex(encrypted_message)
  backend = default_backend()
  key_bytes = key.to_bytes(32, byteorder='big')  # Adjust key size as needed
  cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()
  decrypted_message = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
  return decrypted_message.rstrip().decode()  # Remove padding and decode
$$;
