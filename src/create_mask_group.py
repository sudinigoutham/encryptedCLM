# Databricks notebook source
# DBTITLE 1,Upgrading Databricks SDK with pip command
# MAGIC %pip install databricks-sdk --upgrade

# COMMAND ----------

# DBTITLE 1,Restart Python
dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Initialize Workspace Client
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# COMMAND ----------

# DBTITLE 1,List Groups in the Workspace
groups = w.groups.list()
groups = [group.as_dict() for group in groups]

# COMMAND ----------

# DBTITLE 1,Determine If the Encryption Demo Mask Group is Set
encryption_group_exists = any(group['displayName'] == 'encryptionCLM_demo_mask' for group in groups)
display(encryption_group_exists)

# COMMAND ----------

# DBTITLE 1,Create Encryption Demo Mask Group If It Doesn't Exist
if encryption_group_exists == True:
  print('Group already exists')
  group = [group for group in groups if group['displayName'] == 'encryptionCLM_demo_mask']
else:
  group = w.groups.create(display_name = 'encryptionCLM_demo_mask')
  group = group.as_dict()

display(group)
