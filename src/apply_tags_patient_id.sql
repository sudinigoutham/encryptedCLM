-- Databricks notebook source
-- DBTITLE 1,Declare Variable for Catalog And Table
DECLARE OR REPLACE VARIABLE catalog_use STRING;
DECLARE OR REPLACE VARIABLE tableName STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SET VAR tableName = :table_name;

SELECT catalog_use, tableName;

-- COMMAND ----------

-- DBTITLE 1,Declare Tagging Statement
DECLARE OR REPLACE VARIABLE tag_statement STRING;

SET VAR tag_statement = "alter table IDENTIFIER(catalog_use || '.hv_claims.' || tableName) alter column patient_id set tags ('pii' = 'true');"

-- COMMAND ----------

-- DBTITLE 1,Execute Immediate
EXECUTE IMMEDIATE tag_statement;

-- COMMAND ----------

-- DBTITLE 1,Return Tagged Columns
EXECUTE IMMEDIATE "select * from IDENTIFIER(catalog_use || '.information_schema.column_tags') where schema_name = 'hv_claims'";
