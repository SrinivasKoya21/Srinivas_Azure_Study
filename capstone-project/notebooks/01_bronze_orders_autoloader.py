# notebooks/01_bronze_orders_autoloader.py
from pyspark.sql import functions as F

landing_path = "/Volumes/retail_lakehouse/bronze/landing/orders"
checkpoint_path = "/Volumes/retail_lakehouse/bronze/landing/_checkpoints/orders_autoloader"
schema_location = "/Volumes/retail_lakehouse/bronze/landing/_schemas/orders_autoloader"

bronze_orders_df = (
    spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", schema_location)
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .load(landing_path)
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
)

(
    bronze_orders_df.writeStream
        .format("delta")
        .option("checkpointLocation", checkpoint_path)
        .option("mergeSchema", "true")
        .trigger(availableNow=True)   # process everything currently in the volume, then stop
        .toTable("retail_lakehouse.bronze.orders_raw")
)
