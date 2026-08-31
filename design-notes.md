# Design Notes

> Initial placeholder. To be populated during implementation.

## Purpose

Capture architecture decisions, trade-offs, and rationale as the pipeline is built.

## Planned Topics

- [ ] Medallion layer responsibilities and naming conventions
- [ ] Storage format (Delta Lake) and catalog/schema layout
- [ ] Bronze ingestion approach (autoloader vs batch read)
- [ ] Silver quality-flag schema design
- [ ] Gold table grain and join strategy
- [ ] Dashboard data source selection (Gold tables vs SQL views)
- [ ] Testing strategy (local vs cluster)
- [ ] Orchestration approach

## Decision Log

| Date | Decision | Rationale | Alternatives considered |
|------|----------|-----------|------------------------|
| 2026-08-29 | Repository structure aligned to assessment template | Required for submission compliance | Prior flat layer folders at root |
| 2026-08-30 | Separate `schema_community_edition.sql` for CE | Community Edition lacks Unity Catalog | Modify `schema.sql` only; runtime catalog detection |
| 2026-08-30 | Bronze batch CSV ingest with Delta overwrite | Simple, idempotent, matches spec | Autoloader, append mode, incremental |
| 2026-08-30 | Hive database `bronze` on CE | Standard CE metastore pattern | Unity Catalog `ecommerce_dev.bronze` |
| 2026-08-30 | Shared `ingest_utils.py` + `ingest_all.py` | Consistent ingest, one batch id per run | Three independent scripts only |
| 2026-08-31 | Silver rule IDs in `quality_check_result` | Traceable DQ failures per assessment | Free-text only |
| 2026-08-31 | `is_valid` boolean on Silver tables | Clear valid/invalid filter for Gold | Parse `quality_check_result` only |
| 2026-08-31 | Gold uses valid Silver + Completed orders | Accurate revenue metrics | All order statuses |
| 2026-08-31 | Serverless bundle job on Free Edition | Only serverless compute supported; `environment_key` + `client: "2"` | Classic job clusters |
| 2026-08-31 | UC volume for source CSVs on Free Edition | Public DBFS `/FileStore` disabled | DBFS FileStore default path |
| 2026-08-31 | Databricks E2E validated via bundle job | Confirmed Bronze→Silver→Gold on live workspace | Local-only validation |

## Bronze Layer (implemented)

- **Input:** `customers.csv`, `orders.csv`, `products.csv` from configurable directory
- **Output:** `bronze.customers`, `bronze.orders`, `bronze.products` (Delta)
- **Transformations:** audit columns only (`_ingested_at`, `_source_file`, `_batch_id`)
- **Write mode:** overwrite (full reload)
- **Default paths:** local `data/`; Databricks `dbfs:/FileStore/ecommerce/raw` (or UC volume on Free Edition — see `BUNDLE.md`)

## Silver Layer (implemented)

- **Input:** Bronze Delta tables
- **Output:** `silver.customers`, `silver.orders`, `silver.products`
- **Columns added:** `quality_check_result`, `is_valid`, `_silver_processed_at`
- **Behavior:** retain all rows; flag failures with rule IDs; no silent deletion
- **Processing order:** products → customers → orders

## Gold Layer (implemented)

- **Input:** valid Silver rows (`is_valid = true`)
- **Output:** `gold.sales_by_product`, `gold.revenue_by_customer`, `gold.customer_segmentation`
- **Revenue filter:** `order_status = 'Completed'`
- **Orchestration:** `src/pipeline/run_all.py` runs Bronze → Silver → Gold
- **Bundle:** `databricks.yml` + `resources/medallion_pipeline.job.yml` (see `BUNDLE.md`)
