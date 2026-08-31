# Bronze Layer

Raw CSV ingestion into Delta tables. Bronze preserves source columns as read from CSV and adds audit metadata only — no Silver-style validation or business transformations.

## What Bronze Does

1. Reads `customers.csv`, `orders.csv`, and `products.csv` from a configurable input directory
2. Infers schema from CSV headers (Spark `inferSchema`)
3. Appends audit columns: `_ingested_at`, `_source_file`, `_batch_id`
4. Overwrites the target Bronze Delta table (full reload per run)

## Expected Input Files

| File | Description |
|------|-------------|
| `customers.csv` | 10,000 customer rows |
| `orders.csv` | 100,000 order rows |
| `products.csv` | 500 product rows |

Generated locally via `src/data_generation/generate_sample_data.py` into `data/`, then uploaded to Databricks for job execution.

| Workspace type | Upload target |
|----------------|---------------|
| Free Edition (validated) | UC volume `/Volumes/workspace/default/ecommerce_raw/` |
| DBFS-enabled workspaces | `dbfs:/FileStore/ecommerce/raw/` |

## Bronze Table Names

| Source file | Bronze table |
|-------------|--------------|
| `customers.csv` | `bronze.customers` |
| `orders.csv` | `bronze.orders` |
| `products.csv` | `bronze.products` |

On Community Edition, `bronze` is a Hive database (not a Unity Catalog schema).

## Audit Columns

| Column | Type | Description |
|--------|------|-------------|
| `_ingested_at` | TIMESTAMP | UTC timestamp when the row was ingested |
| `_source_file` | STRING | Source CSV filename (e.g. `customers.csv`) |
| `_batch_id` | STRING | Shared batch id for one ingest run (all three tables) |

## Project Layout

```
src/bronze/
├── config.py              # Paths, CLI args, batch id
├── ingest_utils.py        # Shared read / audit / write logic
├── 01_ingest_customers.py # Single-dataset entry point
├── 02_ingest_orders.py
├── 03_ingest_products.py
└── ingest_all.py          # Ingest all three datasets (recommended)
```

## Run in Databricks Community Edition

### 1. Create tables

Run `database/schema_community_edition.sql` in a SQL notebook or via `%sql` cells.

### 2. Upload CSVs

**Free Edition:** upload to UC volume `workspace.default.ecommerce_raw` (see `BUNDLE.md`).

**DBFS-enabled workspaces:** upload to `/FileStore/ecommerce/raw/` (default input path).

### 3. Sync code to workspace

Clone or upload this repository to your Databricks workspace (Repos recommended).

### 4. Run ingestion

**Option A — ingest all (recommended):**

```python
%run ./src/bronze/ingest_all
```

Or as a Python notebook cell:

```python
from src.bronze.ingest_all import main
main()
```

**Option B — single dataset:**

```python
%run ./src/bronze/01_ingest_customers
```

**Custom paths:**

```python
from src.bronze.ingest_all import main
main(["--input-dir", "dbfs:/FileStore/ecommerce/raw", "--database", "bronze"])
```

Use a cluster with **Delta Lake** enabled (default on Databricks runtimes).

## Verify Records Loaded

```sql
-- Row counts (expected: 10000 / 100000 / 500)
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM bronze.customers
UNION ALL SELECT 'orders', COUNT(*) FROM bronze.orders
UNION ALL SELECT 'products', COUNT(*) FROM bronze.products;

-- Audit columns present
SELECT _batch_id, _source_file, MIN(_ingested_at), MAX(_ingested_at)
FROM bronze.customers
GROUP BY _batch_id, _source_file;

-- Sample raw data (source columns unchanged)
SELECT * FROM bronze.customers LIMIT 5;
```

## Local Development / Testing

Default local input: `<repo>/data/` (auto-detected when not on Databricks).

```bash
# Config unit tests (no Spark required)
pytest tests/bronze/test_bronze_config.py -v

# Full ingest tests (requires Java, pyspark, delta-spark)
pytest tests/bronze/test_bronze_ingest.py -v
```

Local Spark ingest example (after `pip install pyspark delta-spark`):

```bash
python -m src.bronze.ingest_all --input-dir ./data --database bronze
```

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--input-dir` | `data/` locally; `dbfs:/FileStore/ecommerce/raw` on Databricks | CSV directory |
| `--database` | `bronze` | Hive database name |
| `--batch-id` | auto-generated | Optional fixed batch id |

Environment variable `BRONZE_DATABASE` overrides the default database name.
