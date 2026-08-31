# Database Setup Notes

## Databricks Free Edition (validated 2026-08-31)

Free Edition uses the **Hive metastore** (`CREATE DATABASE`) for `bronze`, `silver`, and `gold`. Public DBFS `/FileStore` is **disabled** on Free Edition — use a UC volume for source CSVs.

1. Create a volume and upload generated CSVs from local `data/`:

   ```bash
   databricks volumes create workspace default ecommerce_raw MANAGED --profile ce
   databricks fs cp data/customers.csv dbfs:/Volumes/workspace/default/ecommerce_raw/customers.csv --profile ce --overwrite
   databricks fs cp data/orders.csv dbfs:/Volumes/workspace/default/ecommerce_raw/orders.csv --profile ce --overwrite
   databricks fs cp data/products.csv dbfs:/Volumes/workspace/default/ecommerce_raw/products.csv --profile ce --overwrite
   ```

2. Deploy and run the bundle (see `BUNDLE.md`) with:

   ```bash
   --var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"
   ```

3. Verify after job run:

   ```sql
   SELECT 'bronze.customers' AS t, COUNT(*) FROM bronze.customers
   UNION ALL SELECT 'bronze.orders', COUNT(*) FROM bronze.orders
   UNION ALL SELECT 'bronze.products', COUNT(*) FROM bronze.products;
   -- Expected: 10000 / 100000 / 500
   ```

Default Bronze CSV path variable in `databricks.yml`: `dbfs:/FileStore/ecommerce/raw` (override on Free Edition as above).

---

## Legacy Community Edition (DBFS FileStore)

If your workspace still allows public DBFS:

1. Upload CSVs to:

   ```
   /FileStore/ecommerce/raw/customers.csv
   /FileStore/ecommerce/raw/orders.csv
   /FileStore/ecommerce/raw/products.csv
   ```

2. Open a notebook and run `database/schema_community_edition.sql` (copy/paste or `%run` if synced to workspace).

3. Verify:

   ```sql
   SHOW DATABASES;
   SHOW TABLES IN bronze;
   SHOW TABLES IN silver;
   SHOW TABLES IN gold;
   ```

4. Run Bronze ingestion (`src/bronze/ingest_all.py`) — see `src/bronze/README.md`.

Default Bronze CSV path on Databricks: `dbfs:/FileStore/ecommerce/raw`

---

## Unity Catalog workspaces (optional / enterprise)

If your workspace has Unity Catalog enabled:

1. Open `database/schema.sql` in a Databricks SQL editor or notebook
2. Run the full script to create catalog, schemas, and empty Delta tables
3. Verify:

   ```sql
   SHOW SCHEMAS IN ecommerce_dev;
   SHOW TABLES IN ecommerce_dev.bronze;
   ```

Update catalog name in `candidate-info.md` if not using `ecommerce_dev`.

## CSV Landing Zone

Upload generated CSVs from local `data/` to the workspace landing zone:

| Environment | Path |
|-------------|------|
| Databricks Free Edition (validated) | `/Volumes/workspace/default/ecommerce_raw/` |
| Legacy CE / DBFS-enabled workspaces | `dbfs:/FileStore/ecommerce/raw/` |
| Local dev / tests | `<repo>/data/` |

Bronze ingestion paths are configurable via `--input-dir` (see `src/bronze/README.md`).
