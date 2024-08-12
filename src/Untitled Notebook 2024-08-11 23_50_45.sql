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

VALUES (table_list);

-- COMMAND ----------

SET TASK VALUE 
