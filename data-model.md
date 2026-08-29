# Data Model

> Updated per official assessment document (`DE_C1_Coding_Evaluation.docx`).

## Overview

```
customers.csv ──┐
                ├──► bronze.customers / bronze.orders / bronze.products
orders.csv   ───┤         │
                │         ▼
products.csv ───┘    silver.customers / silver.orders / silver.products
                              │
                              ▼
                     gold.sales_by_product
                     gold.revenue_by_customer
                     gold.customer_segmentation
```

## Source Layer (CSV)

See [requirements-analysis.md](requirements-analysis.md#22-source-data) for full source schemas.

Output location: `data/customers.csv`, `data/orders.csv`, `data/products.csv`

## Bronze Layer

**Purpose:** Raw ingestion with minimal transformation. Preserve source values as-is.

Audit columns:

| Audit column | Type | Description |
|--------------|------|-------------|
| `_ingested_at` | TIMESTAMP | Ingestion timestamp |
| `_source_file` | STRING | Source file name |
| `_batch_id` | STRING | Load batch identifier |

## Silver Layer

**Purpose:** Apply four quality checks. **Retain all records**; flag failures.

Per assessment spec, each Silver table includes:

| Column | Type | Description |
|--------|------|-------------|
| `quality_check_result` | STRING | Failed check(s) and reasons (assessment naming) |
| `_silver_processed_at` | TIMESTAMP | Processing timestamp |

### Four Quality Checks

| # | Check | Fields |
|---|-------|--------|
| 1 | Completeness | No NULLs in `email`, `customer_id`, `product_id` |
| 2 | Uniqueness | No duplicate `order_id`, `customer_id` |
| 3 | Referential integrity | `customer_id` in customers; `product_id` in products |
| 4 | Type/business validation | Valid enums, types, business rules |

### Type/Business Rules **(Assumption)**

| Entity | Rules |
|--------|-------|
| customers | `customer_segment` IN (Premium, Standard, Basic) |
| orders | `order_status` IN (Pending, Completed, Cancelled); `total_amount` = `quantity × unit_price` |
| products | `price`, `cost` >= 0; `stock_quantity` >= 0 |

## Gold Layer

Gold reads from **valid Silver records** (rows with no quality failures) **(Assumption)**.

### gold.sales_by_product

| Column | Type |
|--------|------|
| `product_id` | INT |
| `product_name` | STRING |
| `category` | STRING |
| `total_orders` | BIGINT |
| `total_revenue` | DECIMAL |
| `avg_order_value` | DECIMAL |

### gold.revenue_by_customer

| Column | Type |
|--------|------|
| `customer_id` | INT |
| `customer_name` | STRING |
| `customer_segment` | STRING (Premium/Standard/Basic from source) |
| `total_orders` | BIGINT |
| `total_revenue` | DECIMAL |
| `avg_order_value` | DECIMAL |
| `lifetime_value_actual` | DECIMAL (computed from orders) |

### gold.customer_segmentation

**Behavioral segments** (derived from order activity, not source `customer_segment`):

| Column | Type |
|--------|------|
| `segment_type` | STRING: High-Value / Repeat / One-Time / Inactive |
| `customer_count` | BIGINT |
| `avg_revenue` | DECIMAL |
| `total_revenue` | DECIMAL |

#### Segmentation logic **(Assumption — to be finalized in Gold implementation)**

| Segment | Criteria |
|---------|----------|
| High-Value | Total revenue above threshold (e.g. top quartile) |
| Repeat | More than 1 completed order |
| One-Time | Exactly 1 completed order |
| Inactive | No completed orders |

## Intentional DQ Issue Mapping

| Source issue | Quality check | Expected count |
|--------------|---------------|----------------|
| NULL emails | Completeness | 50 |
| Duplicate customer_ids | Uniqueness | 10 |
| NULL customer_ids | Completeness | 100 |
| NULL product_ids | Completeness | 200 |
| Orphan customer_ids | Referential integrity | 50 |
| Orphan product_ids | Referential integrity | 30 |
| Duplicate order_ids | Uniqueness | 20 |
