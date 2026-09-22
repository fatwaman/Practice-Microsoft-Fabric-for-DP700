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
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## **Spark Structured Streaming Main**

# CELL ********************

from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType
import os
import json
import pyspark.sql.functions as F
import time

source_path = "Files/dp700_data/source"
checkpoint_path = "Files/dp700_data/checkpoint"
schema_name = "dp700_data_stream"
table_name = "temperature_stream"

# Schema for incoming JSON data
file_schema = StructType() \
    .add("id", StringType()) \
    .add("temperature", DoubleType()) \
    .add("timestamp", TimestampType())

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")    

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read streaming data to unbounded table/dataframe
raw_stream_df = spark.readStream \
    .schema(file_schema) \
    .option("maxFilesPerTrigger", 1) \
    .json(source_path)

# Example transformation that adds a processes_timestamp column to the data
transformed_stream_df = raw_stream_df \
    .withColumn("processed_timestamp", \
    F.current_timestamp())

# Stream data to a delta table
deltastream = transformed_stream_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", checkpoint_path) \
    .start(f"Tables/{schema_name}/{table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM lh_dp700_demo.dp700_data_stream.temperature_stream")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

deltastream.isActive

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

deltastream.status

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

deltastream.lastProgress

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

while deltastream.isActive:
    print("✅ Stream is running...")
    print("⏳ Last progress:,", deltastream.lastProgress)
    time.sleep(5)

print("❌ Stream has stopped.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

deltastream.stop()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
