# Data Model

> Initial draft based on stated requirements. Gold-layer detail marked **(Assumption)** where not specified in the assessment.

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

## Bronze Layer

**Purpose:** Raw ingestion with minimal transformation. Preserve source values as-is.

**(Assumption)** Bronze tables mirror source CSV schemas with additional audit columns:

| Audit column | Type | Description |
|--------------|------|-------------|
| `_ingested_at` | TIMESTAMP | Ingestion timestamp |
| `_source_file` | STRING | Source file name |
| `_batch_id` | STRING | Load batch identifier |

### bronze.customers

Source schema + audit columns. No deduplication or validation.

### bronze.orders

Source schema + audit columns. Nullable columns preserved.

### bronze.products

Source schema + audit columns.

## Silver Layer

**Purpose:** Apply data quality rules. **Retain all records**; add quality metadata.

**(Assumption)** Each Silver table includes:

| Quality column | Type | Description |
|----------------|------|-------------|
| `is_valid` | BOOLEAN | `true` if record passes all checks |
| `quality_flags` | ARRAY<STRING> or STRING | List of failed rule codes |
| `quality_reasons` | ARRAY<STRING> or STRING | Human-readable failure descriptions |
| `_silver_processed_at` | TIMESTAMP | Processing timestamp |

### Silver Quality Rules (by entity)

#### silver.customers

| Rule ID | Area | Check |
|---------|------|-------|
| `CUST_COMP_001` | Completeness | `email` IS NOT NULL |
| `CUST_UNIQ_001` | Uniqueness | `customer_id` is unique within dataset |
| `CUST_TYPE_001` | Type/business | `customer_segment` IN (`Premium`, `Standard`, `Basic`) |

#### silver.orders

| Rule ID | Area | Check |
|---------|------|-------|
| `ORD_COMP_001` | Completeness | `customer_id` IS NOT NULL |
| `ORD_COMP_002` | Completeness | `product_id` IS NOT NULL |
| `ORD_UNIQ_001` | Uniqueness | `order_id` is unique within dataset |
| `ORD_REF_001` | Referential integrity | `customer_id` exists in `silver.customers` (valid IDs) |
| `ORD_REF_002` | Referential integrity | `product_id` exists in `silver.products` |
| `ORD_TYPE_001` | Type/business | `order_status` IN (`Pending`, `Completed`, `Cancelled`) |

**(Assumption)** `ORD_TYPE_002`: `total_amount` = `quantity * unit_price` (tolerance TBD).

#### silver.products

| Rule ID | Area | Check |
|---------|------|-------|
| `PROD_UNIQ_001` | Uniqueness | `product_id` is unique |
| `PROD_TYPE_001` | Type/business | `price` >= 0, `cost` >= 0, `stock_quantity` >= 0 |

No intentional source DQ issues specified for products; rules support general validation.

## Gold Layer

**(Assumption)** Gold reads from **valid Silver records only** (`is_valid = true`) unless debugging views are added separately. This assumption should be confirmed — see open questions in requirements analysis.

### gold.sales_by_product

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | INT | Product identifier |
| `product_name` | STRING | From products |
| `category` | STRING | From products |
| `total_orders` | BIGINT | Count of completed orders **(Assumption: Completed only)** |
| `total_quantity` | BIGINT | Sum of quantity |
| `total_revenue` | DECIMAL | Sum of `total_amount` |
| `avg_order_value` | DECIMAL | `total_revenue / total_orders` |

### gold.revenue_by_customer

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | INT | Customer identifier |
| `customer_name` | STRING | From customers |
| `country` | STRING | From customers |
| `customer_segment` | STRING | From customers |
| `total_orders` | BIGINT | Order count |
| `total_revenue` | DECIMAL | Sum of `total_amount` |
| `avg_order_value` | DECIMAL | Average order value |
| `lifetime_value` | DECIMAL | From source customers table |

### gold.customer_segmentation

| Column | Type | Description |
|--------|------|-------------|
| `customer_segment` | STRING | Premium / Standard / Basic |
| `customer_count` | BIGINT | Distinct customers in segment |
| `total_revenue` | DECIMAL | Segment revenue from orders |
| `avg_revenue_per_customer` | DECIMAL | `total_revenue / customer_count` |
| `avg_lifetime_value` | DECIMAL | Average source `lifetime_value` |
| `pct_of_total_revenue` | DECIMAL | Segment share of total revenue |

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  customers  │       │   orders    │       │  products   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ customer_id │◄──┐   │ order_id    │   ┌──►│ product_id  │
│ ...         │   └───│ customer_id │   │   │ ...         │
└─────────────┘       │ product_id  │───┘   └─────────────┘
                      │ ...         │
                      └─────────────┘
```

## Intentional DQ Issue Mapping

| Source issue | Silver rule(s) | Expected flag |
|--------------|----------------|---------------|
| 50 NULL emails | `CUST_COMP_001` | Completeness |
| 10 duplicate customer_ids | `CUST_UNIQ_001` | Uniqueness |
| 100 NULL customer_ids | `ORD_COMP_001` | Completeness |
| 200 NULL product_ids | `ORD_COMP_002` | Completeness |
| 50 orphan customer_ids | `ORD_REF_001` | Referential integrity |
| 30 orphan product_ids | `ORD_REF_002` | Referential integrity |
| 20 duplicate order_ids | `ORD_UNIQ_001` | Uniqueness |
