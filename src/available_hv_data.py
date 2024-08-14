# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Determine Available Health Verity Claims Tables 
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC The purpose of this notebook is to dynamically determine the names of the tables currently available in the Databricks Marketplace Health Verity Sample Claims data sets.  
# MAGIC
# MAGIC We'll pass the names of the tables onto a task value to be used in our workflow's "forEach" task. 
# MAGIC
# MAGIC Note that while this notebook is mostly SQL, the task values utility is not available yet in SQL notebooks at the time of writing.  

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC USE CATALOG healthverity_claims_sample_patient_dataset;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC USE SCHEMA hv_claims_sample;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DECLARE OR REPLACE VARIABLE table_list ARRAY<STRING> DEFAULT ARRAY("diagnosis");
# MAGIC
# MAGIC SET VAR table_list = (
# MAGIC   SELECT ARRAY_AGG(table_name)
# MAGIC   FROM information_schema.tables 
# MAGIC   WHERE table_schema = 'hv_claims_sample'
# MAGIC );

# COMMAND ----------

table_list = spark.sql("select table_list").collect()[0].table_list
print(table_list)

# COMMAND ----------

dbutils.jobs.taskValues.set(key = 'hv_tables', value = table_list)
