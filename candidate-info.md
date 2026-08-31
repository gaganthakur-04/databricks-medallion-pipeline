# Candidate Information

| Field | Value |
|-------|-------|
| **Name** | Gagan Thakur |
| **Email** | gagan.thakur@tothenew.com |
| **Assessment date** | 2026-08-31 |
| **Databricks workspace** | Databricks Free Edition (`dbc-78795322-d3ee.cloud.databricks.com`) |
| **Repository URL** | https://github.com/gaganthakur-04/databricks-medallion-pipeline |

## Environment Details

| Item | Value |
|------|-------|
| Databricks runtime | Serverless compute (Free Edition job environment, client channel `2`) |
| Cluster / SQL warehouse | Serverless Starter Warehouse (`af2185be52aa39f9`) |
| Catalog / schema naming | Hive metastore databases: `bronze`, `silver`, `gold`; source CSVs in UC volume `workspace.default.ecommerce_raw` |
| Dashboard URL | Not created — SQL queries validated; manual dashboard UI setup still required |

## Submission Checklist

| Item | Status |
|------|--------|
| Source data generation (10K / 100K / 500 rows, intentional DQ issues) | Complete |
| Bronze layer (CSV ingest, audit columns, Delta tables) | Complete |
| Silver layer (DQ validation, rule IDs, retain all rows) | Complete |
| Gold layer (sales_by_product, revenue_by_customer, customer_segmentation) | Complete |
| End-to-end pipeline (`src/pipeline/run_all.py`) | Complete |
| Databricks Asset Bundle (`databricks.yml`, job definition) | Complete |
| Automated tests (Bronze, Silver, Gold, Bundle, data generation) | Complete — 40 passed, 1 skipped locally |
| Documentation (design, DQ strategy, data model, BUNDLE.md) | Complete |
| AI prompt history (`ai-prompts/`) | Complete |
| Dashboard SQL queries (`src/dashboard/dashboard_queries.sql`) | Complete |
| Databricks SQL Dashboard UI (deployed visualizations) | **Pending** — SQL queries validated; manual UI creation not performed |
| Databricks end-to-end execution (Bundle deploy + job run) | **Complete** — validated 2026-08-31 (`ce` profile, job run succeeded) |

## Notes

- **Databricks E2E (2026-08-31):** Bundle deploy and job run succeeded on Free Edition. Bronze 10,000 / 100,000 / 500 rows; Silver DQ and Gold aggregations validated via SQL.
- Source CSVs uploaded to UC volume `/Volumes/workspace/default/ecommerce_raw` (public DBFS `/FileStore` is disabled on this workspace).
- Dashboard SQL queries execute successfully; Databricks SQL Dashboard UI was not created in this pass.
