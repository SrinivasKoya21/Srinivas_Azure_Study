# notebooks/03_gold_aggregates.py
from pyspark.sql import functions as F
from delta.tables import DeltaTable

spark.sql("USE CATALOG retail_lakehouse")

# ---------------------------------------------------------------------------
# GOLD 1: daily_revenue_by_category
# "What was our revenue by product category, per day?"
# ---------------------------------------------------------------------------
daily_revenue = (
    spark.table("silver.orders").filter("order_status = 'PLACED'")
    .join(spark.table("silver.products"), "product_id")
    .groupBy("order_date", "category")
    .agg(
        F.sum("line_total").alias("revenue"),
        F.count("order_id").alias("order_count"),
        F.sum("quantity").alias("units_sold"),
    )
)

spark.sql("""
CREATE TABLE IF NOT EXISTS gold.daily_revenue_by_category (
    order_date DATE,
    category STRING,
    revenue DECIMAL(12,2),
    order_count BIGINT,
    units_sold BIGINT
) USING DELTA
""")

target = DeltaTable.forName(spark, "gold.daily_revenue_by_category")
(
    target.alias("t")
    .merge(daily_revenue.alias("s"), "t.order_date = s.order_date AND t.category = s.category")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# ---------------------------------------------------------------------------
# GOLD 2: customer_lifetime_value
# "How much has each customer spent overall, and when did they last order?"
# ---------------------------------------------------------------------------
clv = (
    spark.table("silver.orders").filter("order_status = 'PLACED'")
    .groupBy("customer_id")
    .agg(
        F.sum("line_total").alias("lifetime_revenue"),
        F.count("order_id").alias("total_orders"),
        F.max("order_date").alias("last_order_date"),
    )
    .join(spark.table("silver.customers"), "customer_id")
    .select(
        "customer_id", "first_name", "last_name", "region",
        "lifetime_revenue", "total_orders", "last_order_date",
    )
)

spark.sql("""
CREATE TABLE IF NOT EXISTS gold.customer_lifetime_value (
    customer_id INT,
    first_name STRING,
    last_name STRING,
    region STRING,
    lifetime_revenue DECIMAL(12,2),
    total_orders BIGINT,
    last_order_date DATE
) USING DELTA
""")

target = DeltaTable.forName(spark, "gold.customer_lifetime_value")
(
    target.alias("t")
    .merge(clv.alias("s"), "t.customer_id = s.customer_id")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# ---------------------------------------------------------------------------
# GOLD 3: top_products_by_region
# "What are the best-selling products in each region?"
# ---------------------------------------------------------------------------
top_products = (
    spark.table("silver.orders").filter("order_status = 'PLACED'")
    .join(spark.table("silver.customers").select("customer_id", "region"), "customer_id")
    .join(spark.table("silver.products"), "product_id")
    .groupBy("region", "product_id", "product_name", "category")
    .agg(
        F.sum("line_total").alias("revenue"),
        F.sum("quantity").alias("units_sold"),
    )
)

spark.sql("""
CREATE TABLE IF NOT EXISTS gold.top_products_by_region (
    region STRING,
    product_id INT,
    product_name STRING,
    category STRING,
    revenue DECIMAL(12,2),
    units_sold BIGINT
) USING DELTA
""")

target = DeltaTable.forName(spark, "gold.top_products_by_region")
(
    target.alias("t")
    .merge(
        top_products.alias("s"),
        "t.region = s.region AND t.product_id = s.product_id",
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

print("Gold layer refreshed.")
