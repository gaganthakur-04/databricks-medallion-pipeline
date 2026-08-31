# Project Context

Persistent context for Cursor and other AI assistants working on this repository.

## What This Project Is

An **AI-first data engineering assessment** requiring a **production-quality Databricks Medallion Architecture pipeline** for e-commerce sales data. The deliverable is not only working pipeline code but also documented evidence of the AI-assisted engineering lifecycle.

## Core Objective

```
customers.csv + orders.csv + products.csv
    → Bronze (raw ingest)
    → Silver (DQ validation with flags; retain invalid records)
    → Gold (business aggregates)
    → Databricks SQL Dashboard
```

## Non-Negotiable Requirements

1. **Source data specs are fixed** — row counts, schemas, enum values, and intentional DQ issue counts must match the assessment exactly.
2. **Silver must not silently delete bad data** — flag invalid records with reasons; retain them.
3. **Four DQ areas** — Completeness, Uniqueness, Referential integrity, Type/business validation.
4. **Three Gold outputs** — Sales by Product, Revenue by Customer, Customer Segmentation.
5. **Dashboard minimum** — Top 10 products by revenue, customer revenue distribution, customer segmentation.
6. **AI lifecycle artifacts** — prompt history, reflection, usage summary.

## Source Data Quick Reference

| File | Rows | PK | Key enums |
|------|------|----|-----------|
| `customers.csv` | 10,000 | `customer_id` | segment: Premium/Standard/Basic |
| `orders.csv` | 100,000 | `order_id` | status: Pending/Completed/Cancelled |
| `products.csv` | 500 | `product_id` | — |

## Intentional DQ Issues (must be seeded and detected)

**customers:** 50 NULL emails, 10 duplicate `customer_id`  
**orders:** 100 NULL `customer_id`, 200 NULL `product_id`, 50 orphan `customer_id`, 30 orphan `product_id`, 20 duplicate `order_id`

## Repository Conventions

| Convention | Value |
|------------|-------|
| Pipeline code | `src/bronze/`, `src/silver/`, `src/gold/`, `src/dashboard/` |
| Data generation | `src/data_generation/` |
| Documentation | Root-level `.md` files (per assessment template) |
| Cursor workflow | `cursor-workflow/` |
| AI prompts | `ai-prompts/*.md` |
| Generated CSVs | `data/*.csv` (gitignored) |
| Database setup | `database/` |
| Tests | `tests/` |

## Technology Stack **(Assumption)**

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Platform | Databricks | Stated in assessment |
| Storage | Delta Lake | Databricks standard for Medallion |
| Processing | PySpark | Common Databricks pattern |
| SQL | Databricks SQL | Dashboard requirement |
| Local testing | pytest + PySpark local or mock | Enables CI without cluster |
| Catalog | Unity Catalog **(Assumption)** | Modern Databricks default |

## Naming Conventions **(Assumption)**

```
{catalog}.{schema}.{table}

Schemas:
  bronze   — raw ingested tables
  silver   — validated tables with DQ flags
  gold     — business aggregate tables

Tables:
  bronze.customers, bronze.orders, bronze.products
  silver.customers, silver.orders, silver.products
  gold.sales_by_product, gold.revenue_by_customer, gold.customer_segmentation
```

Catalog name to be set in `database/` and `candidate-info.md`.

## Silver Quality Flag Schema

Per assessment spec:

```text
quality_check_result  STRING   -- failed check(s) and reasons; PASS if valid
_silver_processed_at  TIMESTAMP
```

## Gold Inclusion Policy **(Assumption)**

Gold aggregates use `is_valid = true` Silver records only. Invalid records remain in Silver for audit.

## Key Reference Documents

| Document | When to consult |
|----------|-----------------|
| `cursor-workflow/spec.md` | Technical implementation details |
| `requirements-analysis.md` | What the assessment requires |
| `data-model.md` | Schemas and relationships |
| `data-quality-strategy.md` | DQ rules and flagging |
| `cursor-workflow/task-breakdown.md` | What to build next |

## What NOT to Do

- Do not silently drop or filter invalid records in Silver
- Do not invent assessment requirements without marking as assumptions
- Do not commit large generated CSVs without `.gitignore` consideration
- Do not hardcode credentials or workspace secrets
- Do not skip updating prompt history after significant AI-assisted work

## Current Project State

**Phase:** End-to-end pipeline implemented and **validated on Databricks Free Edition** (2026-08-31). Dashboard SQL queries validated; dashboard UI creation remains manual.

See `README.md` status table for latest progress.
