# Silver Layer

Applies four data-quality check areas to Bronze tables, retains every row, and flags issues with rule IDs.

## What Silver Does

1. Reads `bronze.products`, `bronze.customers`, `bronze.orders`
2. Applies completeness, uniqueness, referential integrity, and business validation rules
3. Adds `quality_check_result`, `is_valid`, and `_silver_processed_at`
4. Writes to `silver.*` Delta tables (overwrite)

Processing order: **products → customers → orders** (orders use Bronze parent keys for referential checks).

## Quality Columns

| Column | Description |
|--------|-------------|
| `quality_check_result` | `PASS` or `FAIL: <rule_id> — <message>; ...` |
| `is_valid` | `true` when `quality_check_result = PASS` |
| `_silver_processed_at` | Processing timestamp |

## Rule IDs

| Rule ID | Check | Entity |
|---------|-------|--------|
| `CUST_COMP_001` | NULL email | customers |
| `CUST_UNIQ_001` | duplicate customer_id | customers |
| `CUST_BIZ_001` | invalid customer_segment | customers |
| `ORD_COMP_001` | NULL customer_id | orders |
| `ORD_COMP_002` | NULL product_id | orders |
| `ORD_UNIQ_001` | duplicate order_id | orders |
| `ORD_REF_001` | orphan customer_id | orders |
| `ORD_REF_002` | orphan product_id | orders |
| `ORD_BIZ_001` | invalid order_status | orders |
| `ORD_BIZ_002` | total_amount mismatch | orders |
| `PROD_BIZ_001` | negative price | products |
| `PROD_BIZ_002` | negative cost | products |
| `PROD_BIZ_003` | negative stock_quantity | products |

## Run in Databricks

```python
import sys
sys.path.insert(0, "/Repos/<you>/databricks-medallion-pipeline")

from src.silver.validate_all import main
main()
```

## Verify

```sql
SELECT is_valid, COUNT(*) FROM silver.customers GROUP BY is_valid;
SELECT quality_check_result FROM silver.orders WHERE NOT is_valid LIMIT 10;
```

## Validated on Databricks (2026-08-31)

| Table | Rows | Valid rows |
|-------|------|------------|
| `silver.customers` | 10,000 | 9,940 (99.4%) |
| `silver.orders` | 100,000 | 88,413 (88.41%) |
| `silver.products` | 500 | 500 (100%) |
