# Candidate Information

| Field | Value |
|-------|-------|
| **Name** | Gagan Thakur |
| **Email** | gagan.thakur@tothenew.com |
| **Assessment date** | 2026-08-31 |
| **Repository URL** | https://github.com/gaganthakur-04/databricks-medallion-pipeline |
| **Git branch** | `cursor/assessment-completion` |

## Databricks Environment

| Item | Value |
|------|-------|
| **Workspace type** | Databricks Free Edition (formerly Community Edition) |
| **Workspace URL** | `https://dbc-78795322-d3ee.cloud.databricks.com` |
| **CLI profile** | `ce` (OAuth — do not commit tokens) |
| **Databricks user** | `gagan.thakur@tothenew.com` |
| **Databricks runtime** | Serverless compute — job environment `client: "2"` |
| **SQL warehouse** | Serverless Starter Warehouse (`af2185be52aa39f9`) |
| **Metastore** | Hive metastore databases: `bronze`, `silver`, `gold` |
| **Source data location** | UC volume `workspace.default.ecommerce_raw` → `/Volumes/workspace/default/ecommerce_raw` |
| **Bundle target** | `dev` |
| **Bundle job name** | `[dev gagan_thakur] [dev] medallion-pipeline` |
| **Bundle job ID** | `736231110157110` |
| **Dashboard URL** | Not created — SQL queries validated; visual dashboard UI must be built manually in Databricks SQL |

> **Note:** Public DBFS `/FileStore` is disabled on this workspace. Source CSVs were uploaded to the UC volume above and the bundle was deployed with `--var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"`.

## Validated End-to-End Results (2026-08-31)

| Layer / check | Result |
|---------------|--------|
| `databricks bundle validate -t dev --profile ce` | OK |
| `databricks bundle deploy -t dev --profile ce` | OK |
| `databricks bundle run medallion_pipeline -t dev --profile ce` | **SUCCESS** |
| `bronze.customers` row count | 10,000 |
| `bronze.orders` row count | 100,000 |
| `bronze.products` row count | 500 |
| `silver.customers` valid rows | 9,940 / 10,000 (99.4%) |
| `silver.orders` valid rows | 88,413 / 100,000 (88.41%) |
| `silver.products` valid rows | 500 / 500 (100%) |
| `gold.sales_by_product` row count | 500 |
| `gold.revenue_by_customer` row count | 9,931 |
| `gold.customer_segmentation` row count | 4 segments |
| Total revenue (`gold.revenue_by_customer`) | 37,330,329.04 |
| Dashboard SQL — top 10 products | 10 rows returned |
| Dashboard SQL — revenue distribution | 5 buckets returned |
| Dashboard SQL — segmentation | 4 segments returned |
| Local pytest | 40 passed, 1 skipped |

## Submission Checklist

| Item | Status |
|------|--------|
| Source data generation (10K / 100K / 500 rows, intentional DQ issues) | Complete |
| Bronze layer (CSV ingest, audit columns, Delta tables) | Complete — validated on Databricks |
| Silver layer (DQ validation, rule IDs, retain all rows) | Complete — validated on Databricks |
| Gold layer (sales_by_product, revenue_by_customer, customer_segmentation) | Complete — validated on Databricks |
| End-to-end pipeline (`src/pipeline/run_all.py`) | Complete — validated on Databricks |
| Databricks Asset Bundle (`databricks.yml`, job definition) | Complete — deploy + run validated |
| Automated tests (Bronze, Silver, Gold, Bundle, data generation) | Complete — 40 passed, 1 skipped |
| Documentation (design, DQ strategy, data model, BUNDLE.md) | Complete |
| AI prompt history (`ai-prompts/`) | Complete |
| Dashboard SQL queries (`src/dashboard/dashboard_queries.sql`) | Complete — validated on Databricks |
| Databricks end-to-end execution (Bundle deploy + job run) | **Complete** — 2026-08-31 |
| Databricks SQL Dashboard UI (deployed visualizations) | **Not done** — SQL validated; manual UI creation required |

## Deploy Commands (reference)

```bash
cd ~/databricks-medallion-pipeline
source .venv/bin/activate

# Upload CSVs (Free Edition — UC volume)
databricks fs cp data/customers.csv dbfs:/Volumes/workspace/default/ecommerce_raw/customers.csv --profile ce --overwrite
databricks fs cp data/orders.csv    dbfs:/Volumes/workspace/default/ecommerce_raw/orders.csv    --profile ce --overwrite
databricks fs cp data/products.csv  dbfs:/Volumes/workspace/default/ecommerce_raw/products.csv  --profile ce --overwrite

# Deploy and run
~/bin/databricks bundle deploy -t dev --profile ce \
  --var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"
~/bin/databricks bundle run medallion_pipeline -t dev --profile ce
```

## Notes

- Enterprise CLI profile `dev` (Tabcorp workspace) is separate and was not used for this assessment.
- Use patched CLI `~/bin/databricks` v0.238.1+ if Homebrew CLI shows Terraform GPG errors.
- Dashboard visual widgets are the only remaining manual step; all underlying SQL and Gold data are validated.
