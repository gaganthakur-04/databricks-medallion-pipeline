# Bronze Layer

Raw CSV ingestion into Delta tables. Preserves source data as-is with audit metadata.

## Planned Contents

- Ingestion scripts/notebooks for customers, orders, products
- Audit columns: `_ingested_at`, `_source_file`, `_batch_id`

## Target Tables

- `bronze.customers`
- `bronze.orders`
- `bronze.products`

## Status

Not started. See `cursor-workflow/task-breakdown.md` Phase 3.
