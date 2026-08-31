# Databricks Asset Bundle

Deploy and run the Medallion pipeline (`Bronze → Silver → Gold`) on Databricks using [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/).

## Current Status

**Local validation:** complete (40 tests passing, 1 skipped; wheel builds successfully).

**Databricks deployment and end-to-end execution:** **complete** — validated 2026-08-31 on Databricks Free Edition using CLI profile `ce`.

| Step | Result |
|------|--------|
| `bundle validate -t dev --profile ce` | OK |
| `bundle deploy -t dev --profile ce` | OK |
| `bundle run medallion_pipeline -t dev --profile ce` | SUCCESS |
| Bronze row counts | 10,000 / 100,000 / 500 |
| Silver valid rows | 9,940 / 88,413 / 500 |
| Gold tables | 500 / 9,931 / 4 rows |

> **Free Edition notes:** Public DBFS `/FileStore` is disabled. Upload source CSVs to a UC volume (e.g. `workspace.default.ecommerce_raw`) and deploy with `--var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"`. Jobs require **serverless** compute (`environment_key` + `client: "2"`).

## Bundle Structure

```
databricks.yml                          # Bundle root config, variables, targets
resources/medallion_pipeline.job.yml    # Job: setup_schema → run_pipeline
scripts/
  setup_schema.py                       # Applies database/schema_community_edition.sql
  run_pipeline.py                       # Entry point → src.pipeline.run_all.main()
pyproject.toml                          # Wheel packaging for job libraries
```

The job reuses the existing pipeline implementation in `src/` — no business-logic changes.

## Prerequisites

1. **Databricks CLI** v0.218+ (`databricks --version`)
2. **Authenticated CLI profile** for your Databricks Free Edition workspace:

   ```bash
   databricks auth login --host https://<your-workspace>.cloud.databricks.com --profile ce
   databricks auth profiles
   # ce  https://<your-workspace>.cloud.databricks.com  YES
   ```

   Use `--profile ce` on all bundle commands below.

   > **Note:** Do not use an enterprise profile pointing at a different workspace. A `Forbidden` or IP ACL error means the profile is wrong or your network is blocked by that workspace.

3. **Source CSVs** uploaded to a readable path (see Free Edition notes below)
4. **Python 3.10+** locally for wheel build and tests (`source .venv/bin/activate` recommended)

## Configuration

All environment-specific values are bundle **variables** (no hardcoded secrets or workspace URLs in source control).

| Variable | Default | Description |
|----------|---------|-------------|
| `csv_input_dir` | `dbfs:/FileStore/ecommerce/raw` | Bronze CSV location (override for Free Edition — see below) |
| `bronze_database` | `bronze` | Bronze Hive database |
| `silver_database` | `silver` | Silver Hive database |
| `gold_database` | `gold` | Gold Hive database |
| `spark_version` | `15.4.x-scala2.12` | Legacy cluster runtime (not used on Free Edition serverless job) |
| `node_type_id` | `i3.xlarge` | Legacy cluster node type (not used on Free Edition serverless job) |

Override at deploy time:

```bash
databricks bundle validate -t dev --profile <your-profile>
```

Or create a local (gitignored) override file `bundle.local.yml` — do not commit secrets.

## Local Validation (before deploy)

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install build

# Build wheel (same as bundle artifact build)
pip wheel . --wheel-dir dist

# Run existing tests
pytest tests/bronze/test_bronze_config.py tests/bronze/test_bronze_datasets.py -v
pytest tests/silver/ tests/gold/ -v
pytest tests/bundle/ -v

# Validate bundle configuration (requires authenticated CLI profile)
databricks bundle validate -t dev --profile <your-profile>
```

## Deploy

```bash
source .venv/bin/activate
~/bin/databricks bundle deploy -t dev --profile ce \
  --var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"
```

> On Databricks Free Edition, public DBFS `/FileStore` is disabled. Upload CSVs to a UC volume and pass `csv_input_dir` as shown above.

## Run End-to-End Pipeline

```bash
~/bin/databricks bundle run medallion_pipeline -t dev --profile ce
```

Job tasks:

1. **setup_schema** — idempotent `CREATE DATABASE/TABLE IF NOT EXISTS` from `schema_community_edition.sql`
2. **run_pipeline** — `src.pipeline.run_all.main()` (Bronze → Silver → Gold)

## Post-Run Verification (SQL)

```sql
SELECT 'bronze.customers' AS t, COUNT(*) FROM bronze.customers
UNION ALL SELECT 'silver.customers', COUNT(*) FROM silver.customers
UNION ALL SELECT 'gold.sales_by_product', COUNT(*) FROM gold.sales_by_product;

SELECT segment_type, customer_count FROM gold.customer_segmentation;
```

Expected Bronze/Silver row counts: 10,000 / 100,000 / 500.

## Targets

| Target | Mode | Purpose |
|--------|------|---------|
| `dev` | development | Default; personal workspace deployment |
| `prod` | production | Future staging/production (same variables, different profile) |

## Community Edition / Free Edition Notes

- Use `schema_community_edition.sql` (Hive metastore databases `bronze`, `silver`, `gold`).
- **Serverless only** — job uses `environment_key` with `client: "2"` (cluster config is not supported).
- **Public DBFS `/FileStore` is disabled** — upload CSVs to a UC volume instead:

  ```bash
  databricks volumes create workspace default ecommerce_raw MANAGED --profile ce
  databricks fs cp data/customers.csv dbfs:/Volumes/workspace/default/ecommerce_raw/customers.csv --profile ce --overwrite
  # repeat for orders.csv and products.csv
  ```

- Deploy with `--var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"`.
- Use patched CLI `~/bin/databricks` v0.238.1+ if Homebrew CLI shows Terraform GPG errors.

## Limitations

- **Databricks SQL Dashboard UI** — SQL queries validated; visual dashboard must be created manually in the SQL UI.
- Bundle deploy/run requires authenticated CLI access to the target workspace.
- Wheel build requires `python3 -m pip` locally (activate `.venv` before deploy).
- Generated CSVs (`data/*.csv`) are excluded from bundle sync — upload separately to UC volume or DBFS.
- Dashboard visualizations are not included in the bundle job (run queries from `src/dashboard/dashboard_queries.sql`).
