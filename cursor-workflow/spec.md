# Technical Specification

Initial technical specification for the Databricks Medallion e-commerce pipeline. Requirements sourced from the assessment; items marked **(Assumption)** are design choices not explicitly stated.

---

## 1. System Overview

### 1.1 Pipeline Flow

```mermaid
flowchart LR
    CSV[Source CSVs] --> B[Bronze Layer]
    B --> S[Silver Layer]
    S --> G[Gold Layer]
    G --> D[SQL Dashboard]
```

### 1.2 Components

| Component | Location | Technology |
|-----------|----------|------------|
| Data generator | `data-generation/` | Python **(Assumption)** |
| Bronze ingest | `bronze/` | PySpark / Delta **(Assumption)** |
| Silver validation | `silver/` | PySpark / Delta **(Assumption)** |
| Gold transforms | `gold/` | PySpark / Delta **(Assumption)** |
| Dashboard queries | `dashboard/` | Databricks SQL |
| Setup | `setup/` | SQL DDL + optional Python |
| Tests | `tests/` | pytest **(Assumption)** |

---

## 2. Source Data Specification

### 2.1 File Inventory

| File | Rows | Delimiter | Header |
|------|------|-----------|--------|
| `customers.csv` | 10,000 | comma **(Assumption)** | yes **(Assumption)** |
| `orders.csv` | 100,000 | comma **(Assumption)** | yes **(Assumption)** |
| `products.csv` | 500 | comma **(Assumption)** | yes **(Assumption)** |

### 2.2 Schemas

Defined in `docs/data-model.md` and `docs/requirements-analysis.md`.

### 2.3 Intentional DQ Injection

The data generator (`data-generation/`) must produce exactly:

| File | Issue | Count |
|------|-------|-------|
| customers | NULL `email` | 50 |
| customers | duplicate `customer_id` | 10 |
| orders | NULL `customer_id` | 100 |
| orders | NULL `product_id` | 200 |
| orders | orphan `customer_id` | 50 |
| orders | orphan `product_id` | 30 |
| orders | duplicate `order_id` | 20 |

All other rows should be valid. Products have no intentional issues.

---

## 3. Bronze Layer

### 3.1 Responsibilities

- Read CSV files from `data/sample/` (local) or cloud path **(Assumption)**
- Write to Delta tables with source schema preserved
- Add audit columns: `_ingested_at`, `_source_file`, `_batch_id` **(Assumption)**
- No validation, deduplication, or type coercion beyond Spark CSV inference

### 3.2 Tables

- `bronze.customers`
- `bronze.orders`
- `bronze.products`

### 3.3 Idempotency **(Assumption)**

Full reload per run (overwrite) for assessment simplicity. Incremental/autoloader deferred unless required.

---

## 4. Silver Layer

### 4.1 Responsibilities

- Read from Bronze
- Apply DQ rules across four areas
- Add `is_valid`, `quality_flags`, `quality_reasons`, `_silver_processed_at`
- **Retain all records** — no silent deletion

### 4.2 Rule Catalog

See `docs/data-quality-strategy.md` and `docs/data-model.md`.

### 4.3 Tables

- `silver.customers`
- `silver.orders`
- `silver.products`

### 4.4 Processing Order **(Assumption)**

1. `silver.products` (no FK dependencies)
2. `silver.customers` (no FK dependencies)
3. `silver.orders` (depends on customers and products for referential checks)

### 4.5 Referential Integrity Logic

- `ORD_REF_001`: `customer_id` must exist in distinct valid `customer_id` from `silver.customers`
- `ORD_REF_002`: `product_id` must exist in distinct valid `product_id` from `silver.products`
- NULL FKs flagged as completeness, not referential integrity

---

## 5. Gold Layer

### 5.1 Responsibilities

- Read from valid Silver records (`is_valid = true`) **(Assumption)**
- Join across entities as needed
- Produce three analytics tables

### 5.2 Outputs

#### gold.sales_by_product

Product-level sales metrics. See `docs/data-model.md`.

#### gold.revenue_by_customer

Customer-level revenue metrics. See `docs/data-model.md`.

#### gold.customer_segmentation

Segment-level rollups: Premium, Standard, Basic.

### 5.3 Business Rules **(Assumption)**

- Revenue metrics based on `orders.total_amount`
- Order status filter for revenue: `Completed` only **(Assumption — not stated in assessment)**
- Cancelled/Pending orders excluded from revenue **(Assumption)**

---

## 6. Dashboard

### 6.1 Platform

Databricks SQL Dashboard **(stated)**.

### 6.2 Required Visualizations

| # | Visualization | Data source |
|---|---------------|-------------|
| 1 | Top 10 products by revenue | `gold.sales_by_product` |
| 2 | Customer revenue distribution | `gold.revenue_by_customer` |
| 3 | Customer segmentation | `gold.customer_segmentation` |

### 6.3 Query Location

SQL files in `dashboard/` with one file per visualization **(Assumption)**.

---

## 7. Testing

### 7.1 Scope

| Layer | Test focus |
|-------|------------|
| Data generation | Row counts, issue counts, schema |
| Silver | Rule logic, flag assignment, record retention |
| Gold | Aggregation correctness on known inputs |
| Integration | CSV → Bronze → Silver → Gold flag counts |

### 7.2 Framework

pytest **(Assumption)**. PySpark local session or test doubles for unit tests.

### 7.3 Validation Targets

Silver flag counts must match intentional issue counts (see `docs/data-quality-strategy.md`).

---

## 8. Setup & Deployment

### 8.1 Setup Scripts (`setup/`)

- Create catalog/schema **(Assumption: Unity Catalog)**
- Grant permissions **(Assumption: workspace default)**
- Optional: volume/path for CSV landing zone

### 8.2 Execution Order

1. Run `setup/` scripts
2. Generate CSVs → `data/sample/`
3. Bronze ingest
4. Silver validation
5. Gold transforms
6. Import dashboard queries

### 8.3 Orchestration **(Assumption)**

Manual or Databricks Job with tasks in layer order. Not specified in assessment.

---

## 9. Open Questions

| # | Question | Default if unresolved |
|---|----------|----------------------|
| 1 | Gold order status filter? | `Completed` only for revenue |
| 2 | Duplicate handling: flag all or only extras? | Flag all duplicate PK rows |
| 3 | Notebooks vs .py modules? | Python modules with optional notebooks |
| 4 | Unity Catalog catalog name? | `ecommerce_dev` |
| 5 | Commit generated CSVs? | Small samples in repo; full files gitignored |
| 6 | `total_amount` = `qty × price` validation? | Add as optional business rule |

---

## 10. Acceptance Criteria

- [ ] Three CSVs generated with correct row counts and DQ issues
- [ ] Bronze tables contain all source rows
- [ ] Silver tables contain all Bronze rows with quality metadata
- [ ] All intentional DQ issues detected and flagged
- [ ] Gold tables: `sales_by_product`, `revenue_by_customer`, `customer_segmentation`
- [ ] Dashboard with 3+ required visualizations
- [ ] Tests pass
- [ ] Documentation and AI artifacts complete
