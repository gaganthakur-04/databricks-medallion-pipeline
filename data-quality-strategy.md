# Data Quality Strategy

## Principles

1. **Detect, don't delete** — Silver retains all records; invalid rows are flagged via `quality_check_result`.
2. **Four quality checks** — Completeness, Uniqueness, Referential integrity, Type/business validation.
3. **Measurable** — Quality metrics report shows % passed per check.
4. **Traceable** — Failed checks documented with clear reasons.

## Quality Checks Overview

### 1. Completeness

- **What:** No NULLs in critical fields
- **How:** COUNT NULL values in `email`, `customer_id`, `product_id`
- **Threshold:** >99% complete
- **Result:** Flag rows with NULLs

| Field | Entity |
|-------|--------|
| `email` | customers |
| `customer_id` | orders |
| `product_id` | orders |

### 2. Uniqueness

- **What:** No duplicate primary keys
- **How:** Detect duplicate `customer_id`, `order_id`
- **Threshold:** 100% unique
- **Result:** Flag duplicate rows

### 3. Referential Integrity

- **What:** Foreign keys exist in parent tables
- **How:** `customer_id` in customers; `product_id` in products
- **Threshold:** >99.9% valid
- **Result:** Flag orphan records

NULL foreign keys are flagged under **Completeness**, not referential integrity.

### 4. Type/Business Validation

- **What:** Values conform to domain rules
- **How:** Enum checks, numeric constraints, `total_amount` = `quantity × unit_price`
- **Result:** Flag invalid rows

## Silver Flagging

Assessment requires `quality_check_result` column on Silver tables. Format **(Assumption):**

```
PASS
FAIL: completeness — email is NULL
FAIL: uniqueness — duplicate customer_id; referential_integrity — customer_id not found
```

## Quality Metrics Report

Required deliverable: % passed for each check per load.

```sql
-- Planned: silver quality summary view
SELECT
  check_name,
  total_rows,
  passed_rows,
  ROUND(100.0 * passed_rows / total_rows, 2) AS pct_passed
FROM silver.quality_metrics;
```

## Expected Issue Counts

| Entity | Check | Expected flagged rows |
|--------|-------|-------------------------|
| customers | Completeness (NULL email) | 50 |
| customers | Uniqueness (duplicate PK) | 10 |
| orders | Completeness (NULL customer_id) | 100 |
| orders | Completeness (NULL product_id) | 200 |
| orders | Referential integrity (orphan customer_id) | 50 |
| orders | Referential integrity (orphan product_id) | 30 |
| orders | Uniqueness (duplicate PK) | 20 |

> Rows may have multiple failures. Total unique flagged rows can exceed individual counts.

## Gold Inclusion Policy

**(Assumption)** Gold aggregates use Silver rows where `quality_check_result = 'PASS'` (or equivalent).

## Testing

See [test-strategy.md](test-strategy.md).
