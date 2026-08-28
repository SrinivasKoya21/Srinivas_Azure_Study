# notebooks/02_bronze_jdbc_customers_products.py
from pyspark.sql import functions as F

jdbc_host = "pg-northwind-retail.postgres.database.azure.com"
jdbc_port = 5432
jdbc_db = "northwind"
jdbc_url = f"jdbc:postgresql://{jdbc_host}:{jdbc_port}/{jdbc_db}?sslmode=require"

pg_user = dbutils.secrets.get("retail_lakehouse", "pg_user")
pg_password = dbutils.secrets.get("retail_lakehouse", "pg_password")

connection_props = {
    "user": pg_user,
    "password": pg_password,
    "driver": "org.postgresql.Driver",
}

def load_table_to_bronze(source_table: str, target_table: str):
    df = (
        spark.read.jdbc(url=jdbc_url, table=source_table, properties=connection_props)
        .withColumn("_ingested_at", F.current_timestamp())
    )
    (
        df.write
          .format("delta")
          .mode("overwrite")
          .option("overwriteSchema", "true")
          .saveAsTable(target_table)
    )
    print(f"Loaded {df.count()} rows from {source_table} into {target_table}")

load_table_to_bronze("customers", "retail_lakehouse.bronze.customers_raw")
load_table_to_bronze("products", "retail_lakehouse.bronze.products_raw")
