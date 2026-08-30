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

## Bronze Layer (implemented)

- **Input:** `customers.csv`, `orders.csv`, `products.csv` from configurable directory
- **Output:** `bronze.customers`, `bronze.orders`, `bronze.products` (Delta)
- **Transformations:** audit columns only (`_ingested_at`, `_source_file`, `_batch_id`)
- **Write mode:** overwrite (full reload)
- **Default paths:** local `data/`; Databricks `dbfs:/FileStore/ecommerce/raw`
