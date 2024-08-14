# Databricks notebook source
# MAGIC %md 
# MAGIC
# MAGIC # Catalog and Schema Set Up
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC The purpose of this notebook is to create the "hv_claims" schema if it doesn't already exist in the catalog of choice.  
# MAGIC
# MAGIC The "catalog" parameter is used to dynamically set the catalog that the "hv_claims" schema will be created and the free Databricks Marketplace Health Verity Claims sample data will be copied into.  
# MAGIC
# MAGIC Note that while this notebook is entirely SQL statements that the "CREATE CATALOG" statement may not be run against a serverless DBSQL warehouse endpoint, therefore generic serverless (or classic) compute is utilized for this notebook task.  

# COMMAND ----------

# DBTITLE 1,Declaring and Setting the new_catalog Variable in SQL
# MAGIC %sql
# MAGIC
# MAGIC DECLARE OR REPLACE VARIABLE new_catalog STRING;
# MAGIC SET VAR new_catalog = :`bundle.catalog`;
# MAGIC SELECT new_catalog;

# COMMAND ----------

# DBTITLE 1,Creating a New SQL Catalog if Absent
# MAGIC %sql
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create catalog if not exists new_catalog;" 

# COMMAND ----------

# DBTITLE 1,Create the New Schema If Absent
# MAGIC %sql 
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create schema if not exists IDENTIFIER(new_catalog || '.hv_claims');"  
