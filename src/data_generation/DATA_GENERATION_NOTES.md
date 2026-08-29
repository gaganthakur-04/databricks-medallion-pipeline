# Data Generation Notes

## Purpose

Generate realistic e-commerce CSV files for the Databricks Medallion assessment with **intentional data quality issues** for Silver layer validation.

## Script

```bash
pip install -r requirements.txt
python src/data_generation/generate_sample_data.py
```

Output: `data/customers.csv`, `data/orders.csv`, `data/products.csv`

## Row Counts

| File | Rows |
|------|------|
| customers.csv | 10,000 |
| orders.csv | 100,000 |
| products.csv | 500 |

## Intentional Quality Issues

### customers.csv

| Issue | Count | Implementation |
|-------|-------|----------------|
| NULL `email` | 50 | Random 50 rows set to empty |
| Duplicate `customer_id` | 10 | 10 rows assigned IDs 1–10 (already used) |

### orders.csv

| Issue | Count | Implementation |
|-------|-------|----------------|
| NULL `customer_id` | 100 | First 100 modified rows |
| NULL `product_id` | 200 | Next 200 modified rows |
| Orphan `customer_id` | 50 | IDs 90001–90050 (not in customers) |
| Orphan `product_id` | 30 | IDs 901–930 (not in products) |
| Duplicate `order_id` | 20 | 20 rows reuse order_ids 1–20 |

**Total problematic rows:** ~700 out of ~110,500 (0.7%)

### products.csv

No intentional issues.

## Design Choices

- **Faker** for realistic names, emails, product names
- **Fixed seed (42)** for reproducible output across runs
- **Disjoint row indices** for order DQ issues to simplify test assertions
- **Orphan IDs** use ranges outside valid parent key ranges

## Why These Issues Exist

Mirrors real-world data quality problems: missing fields, duplicate keys, and broken foreign keys. Silver layer must detect and flag them without deleting records.
