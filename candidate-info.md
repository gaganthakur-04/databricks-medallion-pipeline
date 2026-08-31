# Candidate Information

| Field | Value |
|-------|-------|
| **Name** | Gagan Thakur |
| **Email** | Not available / pending (see GitHub repository owner) |
| **Assessment date** | 2026-08-31 |
| **Databricks workspace** | Not available / pending Databricks workspace access |
| **Repository URL** | https://github.com/gaganthakur-04/databricks-medallion-pipeline |

## Environment Details

| Item | Value |
|------|-------|
| Databricks runtime | Not available / pending Databricks workspace access |
| Cluster / SQL warehouse | Not available / pending Databricks workspace access |
| Catalog / schema naming | Hive metastore databases: `bronze`, `silver`, `gold` (Community Edition) |
| Dashboard URL | Not available / pending Databricks workspace access |

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
| Databricks SQL Dashboard UI (deployed visualizations) | **Pending** — workspace authentication unavailable |
| Databricks end-to-end execution (Bundle deploy + job run) | **Pending** — workspace authentication unavailable |

## Notes

- Local validation: pytest suite and Python wheel build pass.
- Databricks deployment and dashboard UI creation were not completed because the available CLI profiles are not authenticated/authorized for the required Community Edition workspace.
- See `BUNDLE.md` for deploy/run steps once workspace access is configured.
