# Capstone Project Files

Code extracted from **Part 5** of the study guide, ready to drop into a Databricks
Repo instead of retyping it from the PDF. Full narrative, explanations, and the
steps that tie these files together are in
`../docs/DP-750_Complete_Study_and_Interview_Guide.pdf` (Part 5) — this folder is the
"just the code" companion to that chapter, not a replacement for reading it.

## What's here

```
capstone-project/
├── sql/
│   ├── 01_seed_source_db.sql              -- creates + seeds customers/products in Postgres
│   └── 02_catalog_schemas_and_governance.sql  -- Unity Catalog structure, grants, mask, row filter
├── notebooks/
│   ├── 01_bronze_orders_autoloader.py     -- Auto Loader: JSON orders -> bronze Delta table
│   ├── 02_bronze_jdbc_customers_products.py -- JDBC: Postgres -> bronze Delta tables
│   └── 03_gold_aggregates.py              -- silver -> gold MERGE aggregates (3 gold tables)
├── pipelines/
│   └── silver_pipeline.py                 -- Lakeflow Declarative Pipeline, bronze -> silver
├── bundle/
│   ├── databricks.yml                     -- Databricks Asset Bundle definition
│   └── resources/
│       ├── jobs.yml                       -- the orchestration job (bronze -> silver -> gold)
│       └── pipelines.yml                  -- the Lakeflow pipeline resource
└── README_TEMPLATE.md                     -- fill-in-the-blanks README for YOUR GitHub repo
```

## How to actually use this

1. Read Part 5 of the PDF first — these files only make sense with the narrative
   around them (why each design decision was made, what each grant is protecting
   against, etc.).
2. Get the sample data in place: see `../datasets/README.md` and
   `../scripts/upload_to_azure.md`.
3. Run `sql/01_seed_source_db.sql` against your Postgres instance (or skip it and
   use the fast path — `datasets/customers.csv` / `products.csv` directly).
4. Run `sql/02_catalog_schemas_and_governance.sql` in a Databricks SQL editor.
5. Either run the notebooks one at a time to see each step, or deploy the whole
   thing as a bundle:
   ```bash
   cd bundle
   databricks bundle validate -t dev
   databricks bundle deploy -t dev
   databricks bundle run retail_lakehouse_daily -t dev
   ```
6. Once it runs end to end, fill out `README_TEMPLATE.md` with your own screenshots
   and results, rename it to `README.md`, and push the whole `capstone-project/`
   folder (rename it to whatever you like) to your own GitHub as a portfolio piece.
7. Then go read `../docs/real_world_project_walkthrough.md` and compare your version
   against a real public project built the same way.
