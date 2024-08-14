# Databricks notebook source
# DBTITLE 1,Upgrading the Databricks SDK with Pip
# MAGIC %pip install databricks-sdk --upgrade

# COMMAND ----------

# DBTITLE 1,Restart Python
dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Import the Cryptography Package
from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key().decode()

# COMMAND ----------

# DBTITLE 1,Databricks Workspace Client Initialization
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# COMMAND ----------

# DBTITLE 1,Listing Secret Scopes as Dictionaries in Python
scopes = w.secrets.list_scopes()
scopes = [scope.as_dict() for scope in scopes]

# COMMAND ----------

# DBTITLE 1,Exploring Python Scopes and Namespaces
scopes

# COMMAND ----------

# DBTITLE 1,Check for Encryption Demo Presence in Scopes
encryption_demo_exists = any(scope['name'] == 'encryptionCLM-demo' for scope in scopes)
display(encryption_demo_exists)

# COMMAND ----------

# DBTITLE 1,Create Encryption Demo Scope and With Encryption Key
if encryption_demo_exists == True:
  print("encrpytion-demo secret scope already exists")
else:
  w.secrets.create_scope(scope='encryptionCLM-demo')
  w.secrets.put_secret(scope='encryptionCLM-demo', key='encryption_key', string_value=key)

# COMMAND ----------

# DBTITLE 1,Retrieving Encryption Key with DBUtils Secrets
dbutils.secrets.get(scope='encryptionCLM-demo', key='encryption_key')
