# Requirements Analysis

Analysis based solely on the assessment requirements provided. Items marked **(Assumption)** are not stated in the assessment and will be confirmed during design/implementation.

---

## 1. Business Context

Build a **production-quality Databricks Medallion Architecture pipeline** for an **e-commerce sales** use case. The pipeline must demonstrate the full **AI-assisted engineering lifecycle**, not only working code.

## 2. Functional Requirements

### 2.1 End-to-End Flow

```
Source CSV files → Bronze → Silver → Gold → Databricks SQL Dashboard
```

Each layer has a distinct responsibility in the Medallion pattern:

| Layer | Stated responsibility |
|-------|----------------------|
| Bronze | Ingest raw source CSV files |
| Silver | Detect data quality issues; retain invalid records with quality flags/reasons |
| Gold | Produce business analytics outputs |
| Dashboard | Visualize Gold-layer metrics |

### 2.2 Source Data

Three CSV files with fixed row counts and schemas:

#### customers.csv — 10,000 rows

| Column | Type | Constraints |
|--------|------|-------------|
| `customer_id` | INT | Primary key |
| `customer_name` | STRING | |
| `email` | STRING | |
| `country` | STRING | |
| `signup_date` | DATE | |
| `customer_segment` | STRING | Values: `Premium`, `Standard`, `Basic` |
| `lifetime_value` | DECIMAL | |

#### orders.csv — 100,000 rows

| Column | Type | Constraints |
|--------|------|-------------|
| `order_id` | INT | Primary key |
| `customer_id` | INT | Foreign key → `customers.customer_id` |
| `order_date` | DATE | |
| `product_id` | INT | Foreign key → `products.product_id` |
| `quantity` | INT | |
| `unit_price` | DECIMAL | |
| `total_amount` | DECIMAL | |
| `order_status` | STRING | Values: `Pending`, `Completed`, `Cancelled` |
| `payment_date` | DATE | Nullable |

#### products.csv — 500 rows

| Column | Type | Constraints |
|--------|------|-------------|
| `product_id` | INT | Primary key |
| `product_name` | STRING | |
| `category` | STRING | |
| `price` | DECIMAL | |
| `cost` | DECIMAL | |
| `stock_quantity` | INT | |
| `reorder_level` | INT | |

### 2.3 Intentional Data Quality Issues

These issues must be **present in generated source data** and **detected in Silver**:

#### customers.csv

| Issue | Count |
|-------|-------|
| NULL `email` | 50 |
| Duplicate `customer_id` | 10 |

#### orders.csv

| Issue | Count |
|-------|-------|
| NULL `customer_id` | 100 |
| NULL `product_id` | 200 |
| `customer_id` not in customers | 50 |
| `product_id` not in products | 30 |
| Duplicate `order_id` | 20 |

**products.csv** — no intentional DQ issues specified.

### 2.4 Silver Layer — Data Quality Behavior

> **Critical requirement:** Silver must **detect** these issues and **retain invalid records with quality flags/reasons** rather than silently deleting them.

Required quality areas:

1. **Completeness** — NULL/missing required fields
2. **Uniqueness** — duplicate primary keys
3. **Referential integrity** — foreign keys referencing non-existent parent records
4. **Type/business validation** — valid enums, types, and business rules

### 2.5 Gold Layer Outputs

Three required outputs:

1. **Sales by Product**
2. **Revenue by Customer**
3. **Customer Segmentation**

Specific column definitions and grain are **not specified** in the assessment. **(Assumption)** Gold tables will be defined in `data-model.md` and `cursor-workflow/spec.md` based on reasonable e-commerce analytics conventions.

### 2.6 Dashboard Requirements

Databricks SQL Dashboard with **at least**:

1. Top 10 products by revenue
2. Customer revenue distribution
3. Customer segmentation

Visualization types and exact SQL are **not specified**.

### 2.7 Repository Artifacts

The repository must contain areas for:

- Project documentation
- Cursor workflow/context
- AI prompt history
- Data generation
- Bronze processing
- Silver validation
- Gold transformations
- Dashboard queries
- Tests
- Seed/sample data
- Database/setup scripts

Required documentation files:

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `candidate-info.md` | Candidate and environment details |
| `requirements-analysis.md` | This document |
| `design-notes.md` | Architecture and design decisions |
| `data-model.md` | Schemas across all layers |
| `data-quality-strategy.md` | DQ rules and flagging approach |
| `debugging-notes.md` | Issues encountered and resolutions |
| `reflection.md` | Post-project reflection |
| `final-ai-usage-summary.md` | Summary of AI tool usage |
| `tool-workflow.md` | Part A: AI workflow foundation |

Cursor workflow files:

| File | Purpose |
|------|---------|
| `cursor-workflow/project-context.md` | Persistent project context |
| `cursor-workflow/spec.md` | Technical specification |
| `cursor-workflow/cursor-rules-or-instructions.md` | AI assistant rules |
| `cursor-workflow/task-breakdown.md` | Implementation sequence |

AI prompt history organized by: requirements, data generation, Bronze, Silver, Gold, dashboard, testing, debugging, documentation.

## 3. Non-Functional Requirements (Inferred)

The assessment calls for **production-quality** work. Reasonable interpretations:

| Area | Interpretation |
|------|----------------|
| Reliability | Idempotent loads; auditable Bronze metadata |
| Observability | DQ metrics/counts; flag columns on Silver |
| Testability | Automated tests for validation logic |
| Maintainability | Clear layer separation; documented design |
| AI lifecycle | Prompt history and reflection artifacts |

These are **inferred from "production-quality"** and the assessment structure — not explicitly listed as NFRs.

## 4. Out of Scope (Not Stated)

The assessment does **not** require:

- Real-time/streaming ingestion
- CI/CD pipeline (unless chosen as an assumption)
- Specific orchestration tool (Databricks Jobs, Airflow, etc.)
- Authentication/authorization beyond Databricks workspace access
- Data generation for `products.csv` DQ issues

## 5. Open Questions / Ambiguities

See [Section 9 in cursor-workflow/spec.md](cursor-workflow/spec.md#9-open-questions) for technical ambiguities tracked during design.

| # | Question | Impact |
|---|----------|--------|
| 1 | Gold output schemas and grain not defined | Affects Gold DDL and dashboard queries |
| 2 | Should Silver deduplicate valid records or only flag duplicates? | Affects Silver logic |
| 3 | Should Gold exclude invalid Silver records or include all? | Affects metric accuracy |
| 4 | Dashboard visualization types not specified | Affects dashboard design |
| 5 | Databricks deployment model not specified (notebooks vs bundles vs repos) | Affects project layout for code |
| 6 | Whether `total_amount` must equal `quantity × unit_price` | Affects business validation rules |
| 7 | Whether `lifetime_value` on customers is independent of orders | Affects Customer Segmentation logic |

## 6. Requirements Traceability Matrix

| Requirement | Artifact | Status |
|-------------|----------|--------|
| 10K customers with DQ issues | `src/data_generation/`, `src/silver/` | Complete — validated on Databricks |
| 100K orders with DQ issues | `src/data_generation/`, `src/silver/` | Complete — validated on Databricks |
| 500 products | `src/data_generation/` | Complete — validated on Databricks |
| Bronze ingestion | `src/bronze/` | Complete — 10K / 100K / 500 rows on Databricks |
| Silver DQ flagging (4 areas) | `src/silver/`, `data-quality-strategy.md` | Complete — 9,940 / 88,413 / 500 valid |
| Gold: Sales by Product | `src/gold/` | Complete — 500 rows |
| Gold: Revenue by Customer | `src/gold/` | Complete — 9,931 rows |
| Gold: Customer Segmentation | `src/gold/` | Complete — 4 segments |
| Dashboard (3 viz minimum) | `src/dashboard/` | SQL complete and validated; UI manual |
| Databricks Bundle deploy + E2E | `databricks.yml`, `BUNDLE.md` | Complete — 2026-08-31 |
| AI lifecycle artifacts | `ai-prompts/`, root docs | Complete |
| Tests | `tests/` | Complete — 40 passed, 1 skipped |
