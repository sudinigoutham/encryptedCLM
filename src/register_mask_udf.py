# Databricks notebook source
dbutils.widgets.text("bundle.catalog", "")

# COMMAND ----------

catalog_use = dbutils.widgets.get("bundle.catalog")

# COMMAND ----------

spark.sql(f"USE CATALOG {catalog_use}")
spark.sql("use schema hv_claims")
display(spark.sql("select current_catalog(), current_schema()"))

# COMMAND ----------

function_stmnt = f"""
  CREATE OR REPLACE FUNCTION encryption_mask(input_text STRING)
  RETURN CASE
    when IS_MEMBER('encryptionCLM_demo_mask') then {catalog_use}.hv_claims.encrypt_text(input_text, secret('encryptionCLM-demo', 'encryption_key'))
    else input_text 
  END;
"""

# COMMAND ----------

spark.sql(function_stmnt)

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select encryption_mask('hello'), decrypt_text(encryption_mask('hello'), secret('encryptionCLM-demo', 'encryption_key')); 
