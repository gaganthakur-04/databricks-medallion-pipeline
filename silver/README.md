# Silver Layer

Data quality validation and flagging. Retains all records with quality metadata.

## Planned Contents

- DQ rule definitions (Completeness, Uniqueness, Referential integrity, Type/business)
- Silver transform logic per entity
- Quality columns: `is_valid`, `quality_flags`, `quality_reasons`

## Target Tables

- `silver.customers`
- `silver.orders`
- `silver.products`

## Status

Not started. See `cursor-workflow/task-breakdown.md` Phase 4.
