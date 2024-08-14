-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC # Create Or Replace Health Verity Tables in New Catalog
-- MAGIC
-- MAGIC *** 
-- MAGIC
-- MAGIC The purpose of this notebook is to create or replace the tables in the desingated catalog's "hv_claims" schema from the Databricks Marketplace's Health Verity Claims Sample data for use in the column level masking demo.  

-- COMMAND ----------

USE CATALOG healthverity_claims_sample_patient_dataset;

-- COMMAND ----------

USE SCHEMA hv_claims_sample;

-- COMMAND ----------

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

EXECUTE IMMEDIATE crtasSQL;

-- COMMAND ----------

EXECUTE IMMEDIATE "select * from IDENTIFIER(new_catalog || '.hv_claims.' || table_name) limit 10";
