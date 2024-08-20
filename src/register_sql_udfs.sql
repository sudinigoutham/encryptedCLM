-- Databricks notebook source
DECLARE OR REPLACE VARIABLE catalog_use STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SELECT catalog_use;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend

  backend = default_backend()
  cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  padded_message = input_text + ' ' * (16 - len(input_text) % 16)  # Padding to ensure block size compatibility
  encrypted_message = encryptor.update(padded_message.encode()) + encryptor.finalize()
  return encrypted_message.hex()
$$;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.decrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend

  encrypted_message_bytes = bytes.fromhex(input_text)
  backend = default_backend()
  cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()
  decrypted_message = decryptor.update(encrypted_message_bytes) + decryptor.finalize()
  return decrypted_message.rstrip().decode()
$$;

-- COMMAND ----------

EXECUTE IMMEDIATE "select 
  IDENTIFIER(catalog_use || '.hv_claims.encrypt_text')('Spark is awesome', secret('encryptionCLM-demo', 'encryption_key')) as encrypted_text"

-- COMMAND ----------

EXECUTE IMMEDIATE "select
  IDENTIFIER(catalog_use || '.hv_claims.decrypt_text')('edc3528531b87f36999f27a9302f18ebec93a785b2dfc4c8a2c3468983538aa2', secret('encryptionCLM-demo', 'encryption_key')) as decrypted_text"

-- COMMAND ----------

EXECUTE IMMEDIATE "select
  IDENTIFIER(catalog_use || '.hv_claims.encrypt_text')('93af469dadce578e4e9f06baf77dcefd', secret('encryptionCLM-demo', 'encryption_key')) as encrypted_text"

-- COMMAND ----------

EXECUTE IMMEDIATE "select
  IDENTIFIER(catalog_use || '.hv_claims.decrypt_text')('b27255cf9a42956037a4aea4f80137a150a3b8a92cb298166e6b7468ec7a2837ec93a785b2dfc4c8a2c3468983538aa2', secret('encryptionCLM-demo', 'encryption_key')) as decrypted_text"
