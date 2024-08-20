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

# DBTITLE 1,Set Catalog for Health Verity Sample Patient Claims Data Set
# MAGIC %sql
# MAGIC
# MAGIC USE CATALOG healthverity_claims_sample_patient_dataset;

# COMMAND ----------

# DBTITLE 1,Set Schema for the Claims Sample
# MAGIC %sql
# MAGIC
# MAGIC USE SCHEMA hv_claims_sample;

# COMMAND ----------

# DBTITLE 1,Declare and Set Array of Tables Available
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

# DBTITLE 1,Return Table List in Python
table_list = spark.sql("select table_list").collect()[0].table_list
print(table_list)

# COMMAND ----------

# DBTITLE 1,Set Task Values for the CRTAS For Each Task
dbutils.jobs.taskValues.set(key = 'hv_tables', value = table_list)
