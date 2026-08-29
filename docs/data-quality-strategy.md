# Data Quality Strategy

## Principles

1. **Detect, don't delete** — Silver retains all records; invalid rows are flagged, not silently removed.
2. **Explicit over implicit** — Every failure maps to a rule ID, quality area, and human-readable reason.
3. **Traceable** — Rule IDs link back to assessment requirements and test cases.
4. **Measurable** — DQ summary metrics can be queried per load batch.

## Quality Areas

| Area | Definition | Applies to |
|------|------------|------------|
| Completeness | Required fields are present (not NULL) | customers, orders |
| Uniqueness | Primary key values are unique | customers, orders, products |
| Referential integrity | Foreign keys resolve to existing parent records | orders → customers, orders → products |
| Type/business validation | Values conform to domain rules and enums | all entities |

## Silver Flagging Approach

### Record-level metadata

Each Silver record carries:

- `is_valid` — `false` if **any** rule fails
- `quality_flags` — machine-readable rule IDs (e.g., `ORD_REF_001`)
- `quality_reasons` — human-readable descriptions

### Handling duplicates

**(Assumption)** Duplicate primary key records are **all retained** with `CUST_UNIQ_001` / `ORD_UNIQ_001` flags. Gold layer excludes flagged duplicates. Alternative: mark only subsequent occurrences — to be decided during implementation.

### Referential integrity scope

For orphan foreign keys (`ORD_REF_001`, `ORD_REF_002`):

- Check against the set of **valid** parent `customer_id` / `product_id` values
- **(Assumption)** "Valid" parent = distinct IDs from Silver parents where the parent itself passes uniqueness checks

### NULL foreign keys

NULL `customer_id` and `product_id` are flagged under **Completeness** (`ORD_COMP_001`, `ORD_COMP_002`), not referential integrity, since NULL cannot reference a parent.

## Rule Catalog

See [data-model.md](data-model.md#silver-layer) for the full rule catalog with IDs.

## Expected Issue Counts (Validation Targets)

After Silver processing of intentionally seeded data:

| Entity | Rule | Expected flagged records |
|--------|------|--------------------------|
| customers | `CUST_COMP_001` | 50 |
| customers | `CUST_UNIQ_001` | 10 (duplicate rows; exact flagged count depends on duplicate-handling approach) |
| orders | `ORD_COMP_001` | 100 |
| orders | `ORD_COMP_002` | 200 |
| orders | `ORD_REF_001` | 50 |
| orders | `ORD_REF_002` | 30 |
| orders | `ORD_UNIQ_001` | 20 (duplicate rows) |

> **Note:** A single order row may trigger multiple flags (e.g., NULL `customer_id` AND NULL `product_id`). Total flagged rows may exceed individual issue counts.

## DQ Monitoring Queries (planned)

**(Assumption)** Summary views or queries:

```sql
-- Example: flag counts by rule (to be implemented)
SELECT quality_flag, COUNT(*) AS record_count
FROM silver.orders
LATERAL VIEW EXPLODE(quality_flags) f AS quality_flag
GROUP BY quality_flag;
```

## Gold Layer Inclusion Policy

**(Assumption)** Gold aggregates use only `is_valid = true` records. Invalid records remain queryable in Silver for audit and debugging.

## Testing Strategy for DQ

| Test type | Scope |
|-----------|-------|
| Unit tests | Individual rule functions with known good/bad inputs |
| Integration tests | End-to-end: generated CSVs → Silver → verify flag counts |
| Regression tests | Ensure flag counts match expected intentional issue counts |
