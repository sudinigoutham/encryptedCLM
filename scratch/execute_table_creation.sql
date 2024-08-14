-- Databricks notebook source
USE CATALOG healthverity_claims_sample_patient_dataset;

-- COMMAND ----------

USE SCHEMA hv_claims_sample;

-- COMMAND ----------

SHOW TABLES;

-- COMMAND ----------

DECLARE OR REPLACE VARIABLE table_list ARRAY<STRING> DEFAULT ARRAY("diagnosis");

SET VAR table_list = (
  SELECT ARRAY_AGG(table_name)
  FROM information_schema.tables 
  WHERE table_schema = 'hv_claims_sample'
);

-- COMMAND ----------

SELECT table_list;

-- COMMAND ----------

VALUES (table_list[0]);

-- COMMAND ----------

DECLARE OR REPLACE VARIABLE table_cnt INT;
EXECUTE IMMEDIATE "select size(table_list)" into table_cnt;
SELECT table_cnt;

-- COMMAND ----------

DECLARE OR REPLACE VARIABLE crtasSQL STRING;
DECLARE OR REPLACE VARIABLE new_catalog STRING;
DECLARE OR REPLACE VARIABLE new_schema STRING;
DECLARE OR REPLACE VARIABLE i INT DEFAULT 0;

-- Set the variables directly instead of using DEFAULT with parameter markers
SET VAR new_catalog = :new_catalog;
SET VAR new_schema = :new_schema;

SET VAR crtasSQL = "
  CREATE OR REPLACE TABLE IDENTIFIER(new_catalog || '.' || new_schema || '.' || table_list[i]) AS
  SELECT * FROM IDENTIFIER(table_list[i])
";

-- COMMAND ----------

EXECUTE IMMEDIATE "create schema if not exists IDENTIFIER(new_catalog || '.' || new_schema)";

-- COMMAND ----------

SET VAR i = :i;

EXECUTE IMMEDIATE crtasSQL 
USING (0 AS i);
