# Database Setup Notes

## Databricks Community Edition (recommended for this assessment)

Community Edition uses the **Hive metastore** (`CREATE DATABASE`), not Unity Catalog.

1. Upload generated CSVs to DBFS (Databricks UI → **Data** → **Upload**):

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
| Community Edition | `dbfs:/FileStore/ecommerce/raw/` |
| Local dev / tests | `<repo>/data/` |

Bronze ingestion paths are configurable via `--input-dir` (see `src/bronze/README.md`).
