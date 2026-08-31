# Databricks Asset Bundle

Deploy and run the Medallion pipeline (`Bronze → Silver → Gold`) on Databricks using [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/).

## Current Status

**Local validation:** complete (20 tests passing, wheel builds successfully).

**Databricks deployment and end-to-end execution:** **not completed** — pending authentication.

> Databricks deployment and end-to-end execution could not be completed because the available Databricks CLI profiles are not authenticated/authorized for the required Community Edition workspace.

The only configured local profile (`dev`) points to an enterprise workspace and returns `Forbidden` / IP ACL errors. No Databricks E2E results are claimed until a valid CE profile is configured and the job is run.

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
2. **Authenticated CLI profile** for your workspace (Community Edition or other):

   ```bash
   # Log in to your Community Edition workspace (browser OAuth — no token in repo)
   databricks auth login --host https://community.cloud.databricks.com --profile community
   ```

   Verify:

   ```bash
   databricks auth profiles
   # community  https://community.cloud.databricks.com  YES
   ```

   Use `--profile community` (or your profile name) on all bundle commands below.

   > **Note:** Do not use an enterprise profile pointing at a different workspace. A `Forbidden` or IP ACL error means the profile is wrong or your network is blocked by that workspace.

3. **Source CSVs** uploaded to DBFS (default: `dbfs:/FileStore/ecommerce/raw/`)
4. **Python 3.10+** locally for wheel build and tests

## Configuration

All environment-specific values are bundle **variables** (no hardcoded secrets or workspace URLs in source control).

| Variable | Default | Description |
|----------|---------|-------------|
| `csv_input_dir` | `dbfs:/FileStore/ecommerce/raw` | Bronze CSV location |
| `bronze_database` | `bronze` | Bronze Hive database |
| `silver_database` | `silver` | Silver Hive database |
| `gold_database` | `gold` | Gold Hive database |
| `spark_version` | `15.4.x-scala2.12` | Job cluster runtime |
| `node_type_id` | `i3.xlarge` | Override for CE / cloud provider |

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
databricks bundle deploy -t dev --profile <your-profile>
```

## Run End-to-End Pipeline

```bash
databricks bundle run medallion_pipeline -t dev --profile <your-profile>
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

## Community Edition Notes

- Use `schema_community_edition.sql` (Hive metastore — no Unity Catalog).
- Override `node_type_id` and `spark_version` if the default cluster spec is unavailable.
- Upload CSVs to `/FileStore/ecommerce/raw/` before running the job.
- CE may restrict cluster types; check **Compute** in your workspace UI.

## Limitations

- **Databricks E2E validation is pending** — requires a valid CE CLI profile (see Prerequisites).
- Bundle deploy/run requires authenticated CLI access to the target workspace.
- Wheel build requires `pip` locally; cluster runtime provides PySpark/Delta.
- Generated CSVs (`data/*.csv`) are excluded from bundle sync — use DBFS upload.
- Dashboard phase is not included in this job.
