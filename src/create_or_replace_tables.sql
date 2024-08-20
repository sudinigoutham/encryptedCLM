-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC # Create Or Replace Health Verity Tables in New Catalog
-- MAGIC
-- MAGIC *** 
-- MAGIC
-- MAGIC The purpose of this notebook is to create or replace the tables in the desingated catalog's "hv_claims" schema from the Databricks Marketplace's Health Verity Claims Sample data for use in the column level masking demo.  

-- COMMAND ----------

-- DBTITLE 1,Set HV Catalog To Pull From
USE CATALOG healthverity_claims_sample_patient_dataset;

-- COMMAND ----------

-- DBTITLE 1,Set Claims Sample Schema Containing Marketplace Tables
USE SCHEMA hv_claims_sample;

-- COMMAND ----------

-- DBTITLE 1,Declare CRTAS SQL Statements
DECLARE OR REPLACE VARIABLE crtasSQL STRING;
DECLARE OR REPLACE VARIABLE new_catalog STRING;
DECLARE OR REPLACE VARIABLE table_name STRING;

SET VAR new_catalog = :`bundle.catalog`;
SET VAR table_name = :table_name;

SET VAR crtasSQL = "
  create or replace table IDENTIFIER(new_catalog || '.hv_claims.' || table_name) as
  select * from IDENTIFIER(table_name)
";


SELECT new_catalog, table_name, crtasSQL;

-- COMMAND ----------

-- DBTITLE 1,Execute CRTAS SQL
EXECUTE IMMEDIATE crtasSQL;

-- COMMAND ----------

-- DBTITLE 1,Select LIMIT 10 From New Table
EXECUTE IMMEDIATE "select * from IDENTIFIER(new_catalog || '.hv_claims.' || table_name) limit 10";
