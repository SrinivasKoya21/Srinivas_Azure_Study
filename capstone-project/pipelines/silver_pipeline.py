# pipelines/silver_pipeline.py
import dlt
from pyspark.sql import functions as F

# ---------------------------------------------------------------------------
# SILVER: orders
# ---------------------------------------------------------------------------
@dlt.table(
    name="orders",
    comment="Cleaned, deduplicated order events with valid business keys.",
    table_properties={"quality": "silver"},
)
@dlt.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dlt.expect_or_drop("valid_quantity", "quantity > 0")
@dlt.expect("known_customer", "customer_id IS NOT NULL")  # warn only, don't drop
def orders():
    return (
        dlt.read_stream("retail_lakehouse.bronze.orders_raw")
        .withColumn("order_timestamp", F.to_timestamp("order_timestamp"))
        .withColumn("order_date", F.to_date("order_timestamp"))
        .withColumn("line_total", F.col("quantity") * F.col("unit_price"))
        .dropDuplicates(["order_id"])
        .select(
            "order_id", "customer_id", "product_id", "quantity", "unit_price",
            "line_total", "order_status", "order_timestamp", "order_date",
            "shipping_country",
        )
    )


# ---------------------------------------------------------------------------
# SILVER: customers
# ---------------------------------------------------------------------------
@dlt.table(
    name="customers",
    comment="Conformed customer dimension with validated email format.",
    table_properties={"quality": "silver"},
)
@dlt.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
@dlt.expect_or_drop(
    "valid_email_format",
    r"email RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
)
@dlt.expect("known_region", "region IN ('North America','Europe','APAC','LATAM')")
def customers():
    return (
        dlt.read("retail_lakehouse.bronze.customers_raw")
        .dropDuplicates(["customer_id"])
        .select(
            "customer_id", "first_name", "last_name", "email", "region",
            "signup_date",
        )
    )


# ---------------------------------------------------------------------------
# SILVER: products
# ---------------------------------------------------------------------------
@dlt.table(
    name="products",
    comment="Conformed product dimension.",
    table_properties={"quality": "silver"},
)
@dlt.expect_or_drop("valid_product_id", "product_id IS NOT NULL")
@dlt.expect_or_drop("valid_price", "unit_price > 0")
def products():
    return (
        dlt.read("retail_lakehouse.bronze.products_raw")
        .dropDuplicates(["product_id"])
        .select("product_id", "product_name", "category", "unit_price")
    )
