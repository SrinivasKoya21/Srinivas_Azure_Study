# Retail Lakehouse on Azure Databricks

One-paragraph summary: what the project is, what business problem it solves,
and the stack (Azure Databricks, Unity Catalog, Delta Lake, Lakeflow
Declarative Pipelines, Lakeflow Jobs, Databricks Asset Bundles).

## Architecture
(Paste/link the architecture diagram from section 1.2, or a screenshot of the
job's DAG from the Databricks Workflows UI.)

## What it does
- Ingests customer/product data from Azure PostgreSQL and simulated
  order-event streams from cloud storage
- Cleans, deduplicates, and enforces data quality with declarative pipeline
  expectations
- Applies Unity Catalog governance (column masking, row filters)
- Produces three business-ready gold tables via incremental MERGE
- Orchestrates the whole pipeline on a schedule with retries and failure
  alerting
- Deploys via CI/CD using Databricks Asset Bundles (dev/prod targets)

## Repo structure
(Short description of each top-level folder — notebooks/, pipelines/,
resources/, scripts/, sql/.)

## How to run it
Link back to this chapter's steps, or summarize the CLI commands:
`databricks bundle deploy -t dev` / `databricks bundle run retail_lakehouse_daily -t dev`

## Sample output
(A screenshot or markdown table of a few rows from each gold table.)

## What I'd do differently at scale
(Adapt section 8.3 of this chapter — this section is a strong signal to
reviewers that you understand production tradeoffs, not just the happy path.)
