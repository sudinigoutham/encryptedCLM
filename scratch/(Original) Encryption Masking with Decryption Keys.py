# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC

# COMMAND ----------

import time
int(time.time())

# COMMAND ----------

from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt a message
message = "Secret Message"
encrypted_text = cipher_suite.encrypt(message.encode())
display(encrypted_text)

# Decrypt the message
decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
display(decrypted_text)

# COMMAND ----------

key

# COMMAND ----------

dbutils.widgets.text("encryption_key", "4cXmMFsSKYg5Y3VVhhDGaNLGCbrptDAo7LaW8hUCJig=")

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog mgiglia;
# MAGIC use schema synthea_dev;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE FUNCTION encrypt_text(input_text STRING, key STRING)
# MAGIC RETURNS STRING
# MAGIC LANGUAGE PYTHON
# MAGIC AS $$
# MAGIC   import cryptography.fernet as fernet
# MAGIC   cipher_suite = fernet.Fernet(key.encode())
# MAGIC   encrypted_text = cipher_suite.encrypt_at_time(input_text.encode(), 1723705758)
# MAGIC   return encrypted_text.decode()
# MAGIC $$;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select encrypt_text("my message", :encryption_key) as secret_message;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select encrypt_text(coalesce(null, ""), :encryption_key) as null_message;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE FUNCTION decrypt_text(input_text STRING, key STRING)
# MAGIC RETURNS STRING
# MAGIC LANGUAGE PYTHON
# MAGIC AS $$
# MAGIC   import cryptography.fernet as fernet
# MAGIC   cipher_suite = fernet.Fernet(key.encode())
# MAGIC   decrypted_text = cipher_suite.decrypt(input_text.encode())
# MAGIC   return decrypted_text.decode()
# MAGIC $$;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC with t as (
# MAGIC   select 
# MAGIC     encrypt_text("my message", :encryption_key) as secret_message
# MAGIC )
# MAGIC select 
# MAGIC   decrypt_text(secret_message, :encryption_key) as decrypted_message
# MAGIC from 
# MAGIC   t
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC with t as (
# MAGIC   select 
# MAGIC     encrypt_text(coalesce(null, ""), :encryption_key) as null_message
# MAGIC )
# MAGIC select 
# MAGIC   decrypt_text(null_message, :encryption_key) as decrypted_message
# MAGIC from 
# MAGIC   t
# MAGIC ;

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC select 
# MAGIC   patient_id
# MAGIC   ,birth_date
# MAGIC   ,ssn
# MAGIC   ,drivers
# MAGIC   ,passport
# MAGIC   ,concat(first, " ", middle, " ", last) as name
# MAGIC from 
# MAGIC   patients
# MAGIC limit 10
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC   encrypt_text(COALESCE(patient_id, ''), :encryption_key) as patient_id,
# MAGIC   birth_date,
# MAGIC   ssn,
# MAGIC   drivers,
# MAGIC   passport,
# MAGIC   encrypt_text(COALESCE(first, '') || " " || COALESCE(middle, '') || " " || COALESCE(last, ''), :encryption_key) as name
# MAGIC from
# MAGIC   patients
# MAGIC limit 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table mgiglia.synthea.patients as
# MAGIC select
# MAGIC   encrypt_text(COALESCE(patient_id, ''), :encryption_key) as patient_id
# MAGIC   ,birth_date
# MAGIC   ,death_date
# MAGIC   ,encrypt_text(COALESCE(ssn, ''), :encryption_key) as ssn
# MAGIC   ,drivers
# MAGIC   ,passport
# MAGIC   ,prefix
# MAGIC   ,first
# MAGIC   ,middle
# MAGIC   ,last
# MAGIC   ,suffix
# MAGIC   ,maiden
# MAGIC   ,marital
# MAGIC   ,race
# MAGIC   ,ethnicity
# MAGIC   ,gender
# MAGIC   ,birth_place
# MAGIC   ,address
# MAGIC   ,city
# MAGIC   ,state
# MAGIC   ,county
# MAGIC   ,fips
# MAGIC   ,zip
# MAGIC   ,lat
# MAGIC   ,lon
# MAGIC   ,healthcare_expenses
# MAGIC   ,healthcare_coverage
# MAGIC   ,income
# MAGIC from patients;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from mgiglia.synthea.patients;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC with t as (
# MAGIC   select 
# MAGIC     patient_id as encrypted_patient_id 
# MAGIC     ,decrypt_text(encrypted_patient_id, :encryption_key) as decrpyted_patient_id
# MAGIC   from 
# MAGIC     mgiglia.synthea.patients
# MAGIC )
# MAGIC select 
# MAGIC   t1.encrypted_patient_id
# MAGIC   ,t1.decrpyted_patient_id
# MAGIC   ,t2.patient_id 
# MAGIC from 
# MAGIC   t t1
# MAGIC   ,patients t2
# MAGIC where 
# MAGIC   t1.decrpyted_patient_id = t2.patient_id
# MAGIC ;

# COMMAND ----------


