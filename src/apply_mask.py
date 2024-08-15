# Databricks notebook source
dbutils.widgets.text("bundle.catalog", "")

# COMMAND ----------

catalog_use = dbutils.widgets.get("bundle.catalog")

# COMMAND ----------

spark.sql(f"USE CATALOG {catalog_use}")
spark.sql("use schema hv_claims")
display(spark.sql("select current_catalog(), current_schema()"))

# COMMAND ----------

sqlStmt = f"""
  SELECT * FROM information_schema.column_tags where schema_name = 'hv_claims'
"""

tagged_columns = spark.sql(sqlStmt)
display(tagged_columns)

# COMMAND ----------

# Iterate over each row in the DataFrame
for row in tagged_columns.collect():
    stmnt = f"""ALTER TABLE {row.catalog_name}.{row.schema_name}.{row.table_name} 
                ALTER COLUMN {row.column_name} SET MASK {catalog_use}.hv_claims.encryption_mask"""
    spark.sql(stmnt)

# After applying the masks, you can proceed with other operations

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from information_schema.column_masks
