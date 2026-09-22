# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e65a43b2-b89c-4d57-b796-b9f2946506f7",
# META       "default_lakehouse_name": "lh_dp700_demo",
# META       "default_lakehouse_workspace_id": "c8a28174-0838-4802-87c4-fd773d95207b",
# META       "known_lakehouses": [
# META         {
# META           "id": "e65a43b2-b89c-4d57-b796-b9f2946506f7"
# META         }
# META       ]
# META     },
# META     "warehouse": {}
# META   }
# META }

# MARKDOWN ********************

# ## **DP-700 Examp Prep**

# MARKDOWN ********************

# #### **🔷 Parameters**

# PARAMETERS CELL ********************

dataset = "animals"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### **🔷 Reading data from a file in Lakehouse**

# CELL ********************

df = spark.read.format("csv").option("header","true").load(f"Files/dp700_data/{dataset}.csv")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### **🔷 Displaying data**

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### **🔷 Using Spark SQL**

# CELL ********************

df.createOrReplaceTempView("df_view")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT *,
# MAGIC     now() as ts
# MAGIC FROM df_view

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_ts = spark.sql('''
    SELECT *,
        now() as ts
    FROM df_view
''')

display(df_ts)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### **🔷 Writing data to a stable in Lakehouse**

# CELL ********************

spark.sql('''
    CREATE SCHEMA IF NOT EXISTS dp700_data
''')

df_ts.write.mode("overwrite").format("delta").saveAsTable(f"dp700_data.{dataset}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### **🔷 Reading data from a table in Lakehouse**

# CELL ********************

df_table = spark.sql(f"SELECT * FROM lh_dp700_demo.dp700_data.{dataset}")
display(df_table)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### **🔷 Using notebookutils to set an exit value for the Notebook**

# CELL ********************

notebookutils.notebook.exit(f"Dataset {dataset} was processed ok!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
