# Uploading the practice datasets to Azure / Databricks

Three ways to get `../datasets/` into a place your notebooks can read from,
easiest first. All three assume you've completed Part 1's environment setup
(Databricks CLI installed and configured, or a workspace with Unity Catalog).

## Option 1 — Drag and drop in the Databricks UI (fastest, zero setup)

1. In your Databricks workspace, go to **Catalog** in the left sidebar.
2. Create the catalog/schema/volume structure first by running
   `capstone-project/sql/02_catalog_schemas_and_governance.sql` (just Part A) in a
   SQL editor cell — this creates `retail_lakehouse.bronze.landing` for you.
3. Navigate to **Catalog → retail_lakehouse → bronze → landing** (the Volume).
4. Click **Upload to this volume** and drag in the whole `orders/` folder's `.json`
   files.
5. For `customers.csv` / `products.csv`: if you're doing the fast path (Option B in
   `datasets/README.md`), upload these into the same volume, or a new
   `retail_lakehouse.bronze.reference` volume — your call.

## Option 2 — Databricks CLI (`databricks fs cp`)

Once `databricks configure` has been run (Part 1, section 3.4):

```bash
# Orders (matches Part 5's Auto Loader lab exactly)
databricks fs cp -r ./datasets/orders dbfs:/Volumes/retail_lakehouse/bronze/landing/orders

# Customers/products, if you're using the fast path instead of Postgres+JDBC
databricks fs cp ./datasets/customers.csv dbfs:/Volumes/retail_lakehouse/bronze/reference/customers.csv
databricks fs cp ./datasets/products.csv dbfs:/Volumes/retail_lakehouse/bronze/reference/products.csv
```

## Option 3 — Azure CLI, straight into ADLS Gen2 (the "real" path)

Use this if you want the practice data sitting directly in your own storage account
(useful for rehearsing external locations/storage credentials from Part 2):

```bash
# One-time: point an external location at a container in your storage account
az storage container create \
  --account-name <your-storage-account> \
  --name retail-landing

az storage blob upload-batch \
  --account-name <your-storage-account> \
  --destination retail-landing/orders \
  --source ./datasets/orders

az storage blob upload-batch \
  --account-name <your-storage-account> \
  --destination retail-landing/reference \
  --source . \
  --pattern "*.csv"
```

Then create an external location/storage credential pointing at
`abfss://retail-landing@<your-storage-account>.dfs.core.windows.net/` (full steps in
Part 2, section 2 of the book) and point Auto Loader / `spark.read` at that path
instead of a Volume path.

## Which one should you actually use?

Start with **Option 1** today so you're unblocked immediately. Redo the same upload
with **Option 3** later specifically to practice the external-location/storage-credential
labs from Part 2 — that combination (drag-and-drop first, ADLS Gen2 second) covers
both the "easy way" and the "exam-tested way," which is worth doing once each.
