-- Databricks notebook source
DECLARE OR REPLACE VARIABLE catalog_use STRING;
DECLARE OR REPLACE VARIABLE tableName STRING;

SET VAR catalog_use = :`bundle.catalog`; 
SET VAR tableName = :table;

SELECT catalog_use, tableName;

-- COMMAND ----------

DECLARE OR REPLACE VARIABLE tag_statement STRING;

SET VAR tag_statement = "alter table IDENTIFIER(catalog_use || '.hv_claims.' || tableName) alter column npi set tags ('pii' = 'true');"

-- COMMAND ----------

EXECUTE IMMEDIATE tag_statement;

-- COMMAND ----------

EXECUTE IMMEDIATE "select * from IDENTIFIER(catalog_use || '.information_schema.column_tags') where schema_name = 'hv_claims'";
