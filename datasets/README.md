# Datasets — Retail Lakehouse Practice Data

These are the exact sample datasets used by the capstone project in **Part 5** of the
study guide (`docs/DP-750_Complete_Study_and_Interview_Guide.pdf`). They're small,
real, ready-to-use files — no need to generate anything yourself unless you want more.

## What's here

| File / folder | Rows | What it represents | Matches book section |
|---|---|---|---|
| `customers.csv` | 15 | The `customers` table you'd normally seed into Postgres | Part 5, section 2.2 |
| `products.csv` | 15 | The `products` table you'd normally seed into Postgres | Part 5, section 2.2 |
| `orders/*.json` | 6 files, 150 order events | Simulated e-commerce order events (newline-delimited JSON) — the "streaming" source Auto Loader ingests | Part 5, section 2.3 |

`customer_id` in `customers.csv` and `product_id` in `products.csv` line up exactly
with the `customer_id` / `product_id` values referenced inside the order JSON files
(IDs 1–15 for both), so joins work out of the box.

**Heads up — the order data is intentionally a little dirty.** About 3% of orders
have a missing `order_id`, about 3% have an invalid negative `quantity`, and about 3%
reference a `customer_id` that doesn't exist (9999). That's on purpose — it gives your
silver-layer data quality constraints and Lakeflow expectations (Part 3 and Part 5,
section 3) something real to catch instead of a suspiciously perfect dataset.

## Two ways to use this data

**Option A — the full capstone path (relational + streaming sources).**
Load `customers.csv` and `products.csv` into a real Postgres database (Part 5, section
2.1–2.2 walks through Azure Database for PostgreSQL — Flexible Server, or a free local
Docker Postgres as the lighter alternative) and ingest them into bronze via JDBC. Land
the `orders/*.json` files in a Unity Catalog Volume and ingest them with Auto Loader.
This is the path that best rehearses the real exam and real interview scenarios.

**Option B — the fast path (skip the database).**
If you just want to start writing PySpark/SQL today without setting up Postgres yet,
upload all three (`customers.csv`, `products.csv`, `orders/`) straight into a Unity
Catalog Volume and read `customers.csv`/`products.csv` with `spark.read.csv(...)`
instead of JDBC. You lose the JDBC-ingestion rehearsal, but everything else in the
capstone (bronze → silver → gold, governance, orchestration) works identically. Come
back to Option A later once Part 1's environment setup is fully done.

See `../scripts/upload_to_azure.md` for the exact upload commands for both options,
and `../capstone-project/` for the notebooks and SQL that consume this data.

## Want more order data?

Run the generator again any time — it makes new, randomized batches with the same
customer/product IDs:

```bash
cd ../scripts
pip install faker
python generate_orders.py --batches 10 --orders-per-batch 50 --local-dir ../datasets/orders
```
