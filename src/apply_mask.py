# Databricks notebook source
# DBTITLE 1,Creating a Text Input Widget in Databricks
dbutils.widgets.text("bundle.catalog", "")

# COMMAND ----------

# DBTITLE 1,Accessing Database Widgets in Python Code
catalog_use = dbutils.widgets.get("bundle.catalog")

# COMMAND ----------

# DBTITLE 1,Switching Catalog and Schema in PySpark Queries
spark.sql(f"USE CATALOG {catalog_use}")
spark.sql("use schema hv_claims")
display(spark.sql("select current_catalog(), current_schema()"))

# COMMAND ----------

# DBTITLE 1,Pulling the Tagged Columns from the hv_claims schema
sqlStmt = f"""
  SELECT * FROM information_schema.column_tags where schema_name = 'hv_claims'
"""

tagged_columns = spark.sql(sqlStmt)
display(tagged_columns)

# COMMAND ----------

# DBTITLE 1,Apply Masks to Columns Tagged with PiI = True
# Iterate over each row in the DataFrame
for row in tagged_columns.collect():
    stmnt = f"""ALTER TABLE {row.catalog_name}.{row.schema_name}.{row.table_name} 
                ALTER COLUMN {row.column_name} SET MASK {catalog_use}.hv_claims.encryption_mask"""
    spark.sql(stmnt)

# After applying the masks, you can proceed with other operations

# COMMAND ----------

# DBTITLE 1,Show Masks
# MAGIC %sql
# MAGIC
# MAGIC select * from information_schema.column_masks
