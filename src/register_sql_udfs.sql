-- Databricks notebook source
-- DBTITLE 1,SQL Code for Setting Catalog Use Variable
DECLARE OR REPLACE VARIABLE catalog_use STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SELECT catalog_use;

-- COMMAND ----------

-- DBTITLE 1,SQL UDF For Encrypting Text Fields
CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
  from cryptography.hazmat.backends import default_backend

  backend = default_backend()
  cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  padded_message = input_text + ' ' * (16 - len(input_text) % 16) 
  encrypted_message = encryptor.update(padded_message.encode()) + encryptor.finalize()
  return encrypted_message.hex()
$$;

-- COMMAND ----------

-- DBTITLE 1,SQL UDF For Decrypting Text Fields
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

-- DBTITLE 1,Encrypt a Sample Message Using UDF
EXECUTE IMMEDIATE "select 
  IDENTIFIER(catalog_use || '.hv_claims.encrypt_text')('Spark is awesome', secret('encryptionCLM-demo', 'encryption_key')) as encrypted_text"

-- COMMAND ----------

-- DBTITLE 1,Decrypt the token to return the message
EXECUTE IMMEDIATE "select
  IDENTIFIER(catalog_use || '.hv_claims.decrypt_text')('9a739ecbd5f09091ae8a1fd12116a02e8e91b2585a169c5c73eb80f5c682db93', secret('encryptionCLM-demo', 'encryption_key')) as decrypted_text"
