-- Databricks notebook source
-- DBTITLE 1,Variable Declaration and Assignment in SQL
DECLARE OR REPLACE VARIABLE catalog_use STRING;
DECLARE OR REPLACE VARIABLE tableName STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SET VAR tableName = :table_name;

SELECT catalog_use, tableName;

-- COMMAND ----------

-- DBTITLE 1,Tagging Columns for Privacy in SQL Queries
DECLARE OR REPLACE VARIABLE tag_statement STRING;

SET VAR tag_statement = "alter table IDENTIFIER(catalog_use || '.hv_claims.' || tableName) alter column npi set tags ('pii' = 'true');"

-- COMMAND ----------

-- DBTITLE 1,Executing Immediate SQL Commands Dynamically
EXECUTE IMMEDIATE tag_statement;

-- COMMAND ----------

-- DBTITLE 1,Return tagged columns
EXECUTE IMMEDIATE "select * from IDENTIFIER(catalog_use || '.information_schema.column_tags') where schema_name = 'hv_claims'";
