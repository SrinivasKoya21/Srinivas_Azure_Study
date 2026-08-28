# Learning From a Real GitHub Project

Everything in `capstone-project/` is a project *you* build from the ground up. It's
worth also looking at how other people have structured a similar project and put it
on GitHub — partly to see that the shape of a "real" project isn't that different
from what you just built, and partly because browsing other people's data
engineering repos is exactly what you'll do on the job.

Below is a walkthrough of one real, public repo that maps almost one-to-one onto the
DP-750 exam, plus a second one worth bookmarking for later.

> A note on sourcing: both repos below are real, public GitHub projects, found and
> read directly for this walkthrough. Treat descriptions of their exact folder
> contents as accurate as of when this was written (August 2026) — a repo's structure
> can change after that, so if something doesn't match when you look, the repo simply
> moved on; check its own README for the current layout.

## Main example: an End-to-End Azure Databricks ETL Pipeline

**Repo:** [`aishincp/End-To-End-Data-Engineering-ETL-Pipeline-Project-Azure-Databricks-Spark-UnityCatalog`](https://github.com/aishincp/End-To-End-Data-Engineering-ETL-Pipeline-Project-Azure-Databricks-Spark-UnityCatalog)

### Why this one

Its tech stack is almost a checklist of the exam's skills-measured domains: Azure
Data Factory, Azure Data Lake Storage Gen2, Azure Databricks, Delta Lake, Delta Live
Tables, Unity Catalog, and Power BI on top. If you can explain what every piece of
this repo does and why, you can explain what DP-750 is testing.

### The architecture, in plain terms

The project moves four source files — `customers.parquet`, `products.parquet`,
`orders.parquet`, `regions.parquet` — through the same medallion shape you just built
in `capstone-project/`:

- **Source container** — the four raw parquet files land here first, untouched.
- **Bronze container** — Azure Data Factory copies the source files in on a schedule
  (this is the one piece your own capstone project didn't use ADF for — worth
  comparing the two approaches: your capstone used Auto Loader/JDBC directly from
  Databricks, this repo puts ADF in front as a dedicated orchestration/copy layer).
- **Silver container** — Databricks notebooks clean the data: dropping columns
  nobody needs, filtering to the top few `email` domains, concatenating first/last
  name into a single field. Small, unglamorous cleanup steps — which is realistic;
  most silver-layer work looks exactly like this, not like anything clever.
  Look at how this compares to your own `pipelines/silver_pipeline.py`.
- **Gold container** — the data becomes a proper **star schema**: `DimCustomerKey`
  and `DimProductKey` dimension tables, plus a `FactOrders` fact table. Delta Live
  Tables (the older name for what the book calls Lakeflow Declarative Pipelines —
  see Part 3) manages the dependencies between these tables automatically.
- **Logs container** — a dedicated container just for pipeline run logs, which is a
  detail worth stealing for your own projects: don't let logs mix in with data
  containers.
- **Unity Catalog** sits over all of it for governance, and **Power BI** connects on
  top of the gold layer for the actual dashboards a business user would look at.

### What to actually do with this repo

1. Open the repo and read its `README.md` first, then look at the `azure
   screenshots/databricks/` folder — actual screenshots of a real workspace
   configuration are worth more than a description of one.
2. Open whatever's in `scripts/python/` and try to name, before you read the code,
   which medallion layer each script is probably for, based only on its filename.
   Then check yourself.
3. Compare the gold-layer **star schema** approach here (dimension tables + fact
   table) against your own capstone's gold tables (which were flatter, purpose-built
   aggregates like `daily_revenue_by_category`). Both are valid gold-layer designs —
   this is a great "which would you choose and why" question to be ready for in an
   interview (see Part 7, scenario question set).
4. Notice where **Azure Data Factory** does the work in this repo versus where your
   capstone had Databricks do it directly with Auto Loader/JDBC. Neither is "more
   correct" — ADF-in-front is common in shops with existing ADF investment or
   non-Databricks-native sources; Databricks-native ingestion (your capstone's
   approach, and the one DP-750 focuses on) is more common in Databricks-first
   shops. Being able to explain that tradeoff out loud is a real interview question.

## Second example, worth bookmarking

**Repo:** [`DataWithBaraa/databricks_bootcamp_2026`](https://github.com/DataWithBaraa/databricks_bootcamp_2026)

This one is explicitly built as a teaching project — "designed for learning,
portfolio building, and job interviews," in the author's own words — covering the
same bronze/silver/gold shape with PySpark, Spark SQL, Delta Lake, and Unity Catalog,
plus exercises. It's a good second opinion on the same architecture pattern once
you've digested the first repo, and useful specifically for its structured
exercises if you want extra reps beyond this book's own practice bank.

## A third resource, official and worth knowing about

Databricks itself maintains **[dbdemos](https://github.com/databricks-demos/dbdemos)**
— not a single repo to read top-to-bottom, but an installer (`pip install dbdemos`)
that deploys real, runnable demo pipelines (including several Lakeflow/Delta Live
Tables and Unity Catalog governance demos) directly into your own workspace with one
Python command. Once your Databricks Free Edition or Azure workspace is set up (Part
1), running `dbdemos.install('dlt-cdc')` or similar is a fast way to see an
official, production-quality pipeline running live, end to end, in your own account —
genuinely worth 20 minutes once you're past the basics.

## The habit worth building

Interviewers care less about whether you've memorized medallion architecture and more
about whether you can open an unfamiliar repo and reconstruct its design just from
the folder structure and a few files — because that's the actual job. Do the
three-repo tour above once now, and once more the week before your exam.
