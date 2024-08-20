# Databricks notebook source
# DBTITLE 1,Creating Text Widgets with DBUtils in Python
dbutils.widgets.text("bundle.catalog", "")

# COMMAND ----------

# DBTITLE 1,Accessing Bundle Catalog with DBUtils in Python
catalog_use = dbutils.widgets.get("bundle.catalog")

# COMMAND ----------

# DBTITLE 1,Switching Database Contexts in Spark SQL Queries
spark.sql(f"USE CATALOG {catalog_use}")
spark.sql("use schema hv_claims")
display(spark.sql("select current_catalog(), current_schema()"))

# COMMAND ----------

# DBTITLE 1,Creating an Encryption Mask Function in SQL
function_stmnt = f"""
  CREATE OR REPLACE FUNCTION encryption_mask(input_text STRING)
  RETURN CASE
    when IS_MEMBER('encryptionCLM_demo_mask') then input_text
    else {catalog_use}.hv_claims.encrypt_text(input_text, secret('encryptionCLM-demo', 'encryption_key')) 
  END;
"""

# COMMAND ----------

# DBTITLE 1,Executing SQL Commands with Spark in Python
spark.sql(function_stmnt)

# COMMAND ----------

# DBTITLE 1,SQL Function for Conditional Text Decryption
function_stmnt = f"""
  CREATE OR REPLACE FUNCTION decryption_mask(input_text STRING)
  RETURN CASE
    when IS_MEMBER('encryptionCLM_demo_mask') then {catalog_use}.hv_claims.decrypt_text(input_text, secret('encryptionCLM-demo', 'encryption_key')) 
    else input_text
  END;
"""

# COMMAND ----------

# DBTITLE 1,Executing SQL Queries with Spark
spark.sql(function_stmnt)
