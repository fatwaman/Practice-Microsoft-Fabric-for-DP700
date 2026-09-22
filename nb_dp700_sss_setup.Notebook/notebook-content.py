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

# ## **Spark Structured Streaming Setup**

# CELL ********************

import json
import os
import uuid
import random
import time
from datetime import datetime

#Setting
output_folder   = "/lakehouse/default/Files/dp700_data/source"
schema_name     = "dp700_data_stream"
num_files       = 10
wait_seconds    = 5

# Make sure that source folder and destination schema exist
os.makedirs(output_folder, exist_ok=True)
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for i in range(num_files):
    now = datetime.utcnow()
    timestamp_str = now.strftime("%Y%m%dT%H%M%SZ")

    # Simulate one temperature reading
    record = {
        "id": str(uuid.uuid4()),
        "temperature": round(random.uniform(18.0, 30.0), 2),
        "timestamp": now.isoformat()
    }

    # Build file path with name like temperature_20260914T101010Z.json
    filename = f"temperature_{timestamp_str}.json"
    filepath = os.path.join(output_folder, filename)

    # Write the JSON file
    with open(filepath, "w") as f:
        json.dump(record, f)

    print(f"✅ [{i+1}/{num_files}] Wrote: {filename}")
    time.sleep(wait_seconds)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
