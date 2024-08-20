# Databricks notebook source
# DBTITLE 1,Set Input Parameter for bundle.catalog
dbutils.widgets.text("bundle.catalog", "")

# COMMAND ----------

# DBTITLE 1,Retrieve bundle.catalog parameter value
catalog_use = dbutils.widgets.get("bundle.catalog")

# COMMAND ----------

# DBTITLE 1,Set Catalog and Schema to Use
spark.sql(f"USE CATALOG {catalog_use}")
spark.sql("use schema hv_claims")
display(spark.sql("select current_catalog(), current_schema()"))

# COMMAND ----------

# DBTITLE 1,Determine Columns with PII
sqlStmt = f"""
  SELECT table_name, column_name FROM information_schema.columns where column_name in ('npi', 'patient_id') and table_schema = 'hv_claims'
"""

pii_columns = spark.sql(sqlStmt)
display(pii_columns)

# COMMAND ----------

# DBTITLE 1,List Patient ID Table Names
from pyspark.sql.functions import col

patient_id_tables = pii_columns.filter(col("column_name") == "patient_id").select("table_name").collect()
patient_id_tables = [x.table_name for x in patient_id_tables]
patient_id_tables

# COMMAND ----------

# DBTITLE 1,List NPI Table Names
npi_tables = pii_columns.filter(col("column_name") == "npi").select("table_name").collect()
npi_tables = [x.table_name for x in npi_tables]
npi_tables

# COMMAND ----------

# DBTITLE 1,Set Task Values to Pass to the Apply Tags For Each Tasks
dbutils.jobs.taskValues.set(key = 'patient_id_tables', value = patient_id_tables)
dbutils.jobs.taskValues.set(key = 'npi_tables', value = npi_tables)
