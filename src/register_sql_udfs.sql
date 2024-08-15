-- Databricks notebook source
DECLARE OR REPLACE VARIABLE catalog_use STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SELECT catalog_use;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  import cryptography.fernet as fernet
  cipher_suite = fernet.Fernet(key.encode())
  encrypted_text = cipher_suite.encrypt(input_text.encode())
  return encrypted_text.decode()
$$;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.decrypt_text') (input_text STRING, key STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  import cryptography.fernet as fernet
  cipher_suite = fernet.Fernet(key.encode())
  decrypted_text = cipher_suite.decrypt(input_text.encode())
  return decrypted_text.decode()
$$;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION IDENTIFIER(catalog_use || '.hv_claims.encryption_mask') (input_text STRING)
RETURNS STRING
LANGUAGE PYTHON
AS $$
  key = dbutils.secrets.get(scope='encryptionCLM-demo', key='encryption_key')
  if IS_ACCOUNT_GROUP_MEMBER('encryptionCLM_demo_mask'):
    return IDENTIFIER(catalog_use || '.hv_claims.encrypt_text')(input_text, key)
  else:
    return input_text
$$;
