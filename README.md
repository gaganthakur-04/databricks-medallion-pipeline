# Databricks Medallion Pipeline — E-Commerce Sales

Production-quality Databricks Medallion Architecture pipeline for an e-commerce sales use case, built as part of an AI-first data engineering assessment.

## Purpose

Ingest source CSV files through Bronze → Silver → Gold layers and expose business metrics via a Databricks SQL Dashboard. The project demonstrates not only a working pipeline but also the full AI-assisted engineering lifecycle: requirement analysis, design, prompting, implementation, validation, testing, debugging, data quality handling, and reflection.

## Architecture Overview

```
Source CSVs (customers, orders, products)
        │
        ▼
   Bronze Layer          Raw ingestion, schema-on-read, audit metadata
        │
        ▼
   Silver Layer          Validation, quality flags, invalid records retained
        │
        ▼
   Gold Layer            Business aggregates and analytics-ready tables
        │
        ▼
   Databricks SQL        Top products, revenue distribution, segmentation
   Dashboard
```

## Current Status

| Phase | Status |
|-------|--------|
| Requirements analysis | Initial draft complete |
| Project structure & documentation | In progress |
| Data generation | Not started |
| Bronze layer | Not started |
| Silver layer (DQ validation) | Not started |
| Gold layer | Not started |
| Dashboard | Not started |
| Tests | Not started |

## Repository Layout

| Path | Purpose |
|------|---------|
| `docs/` | Assessment documentation (design, data model, DQ strategy, reflection) |
| `cursor-workflow/` | Persistent Cursor context, spec, rules, and task breakdown |
| `ai-prompt-history/` | AI prompt logs organized by major activity |
| `data-generation/` | Scripts to generate source CSVs with intentional DQ issues |
| `bronze/` | Bronze ingestion notebooks/scripts |
| `silver/` | Silver validation and quality-flagging logic |
| `gold/` | Gold transformation logic |
| `dashboard/` | Databricks SQL queries for the dashboard |
| `tests/` | Unit and integration tests |
| `data/sample/` | Seed/sample CSV files (generated, not committed at scale) |
| `setup/` | Databricks catalog, schema, and environment setup scripts |

## Source Data

| File | Rows | Description |
|------|------|-------------|
| `customers.csv` | 10,000 | Customer master with segment and lifetime value |
| `orders.csv` | 100,000 | Order transactions with status and payment date |
| `products.csv` | 500 | Product catalog with pricing and inventory |

See [docs/data-model.md](docs/data-model.md) and [docs/requirements-analysis.md](docs/requirements-analysis.md) for full schemas and quality requirements.

## Gold Outputs

- **Sales by Product** — product-level revenue and volume metrics
- **Revenue by Customer** — customer-level revenue aggregation
- **Customer Segmentation** — segment-level analytics

## Dashboard (minimum)

- Top 10 products by revenue
- Customer revenue distribution
- Customer segmentation

## Documentation Index

- [Requirements Analysis](docs/requirements-analysis.md)
- [Design Notes](docs/design-notes.md)
- [Data Model](docs/data-model.md)
- [Data Quality Strategy](docs/data-quality-strategy.md)
- [Candidate Info](docs/candidate-info.md)
- [Cursor Project Context](cursor-workflow/project-context.md)
- [Technical Spec](cursor-workflow/spec.md)
- [Task Breakdown](cursor-workflow/task-breakdown.md)

## Getting Started

> Implementation is not yet in place. Follow [cursor-workflow/task-breakdown.md](cursor-workflow/task-breakdown.md) for the planned build sequence.

1. Review `cursor-workflow/project-context.md` and `cursor-workflow/spec.md`
2. Generate source data (see `data-generation/`)
3. Run setup scripts (see `setup/`)
4. Execute Bronze → Silver → Gold pipelines
5. Deploy dashboard queries from `dashboard/`

## Assessment Artifacts

This repository is structured to capture the full AI-assisted engineering lifecycle. Prompt history is maintained under `ai-prompt-history/` by activity area. Reflection and AI usage summaries live in `docs/reflection.md` and `docs/final-ai-usage-summary.md`.
