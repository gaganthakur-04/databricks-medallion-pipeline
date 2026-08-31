# Dashboard Guide

## Required Visualizations

| # | Visualization | Chart type | Gold source | Query section |
|---|---------------|------------|-------------|---------------|
| 1 | Top 10 products by revenue | Bar | `gold.sales_by_product` | Query 1 in `dashboard_queries.sql` |
| 2 | Customer revenue distribution | Histogram | `gold.revenue_by_customer` | Query 2 in `dashboard_queries.sql` |
| 3 | Customer segmentation | Pie | `gold.customer_segmentation` | Query 3 in `dashboard_queries.sql` |

## SQL Queries

All queries are in [`dashboard_queries.sql`](dashboard_queries.sql). They read from Gold tables populated by `src/pipeline/run_all.py` (or the Databricks Bundle job).

### Query 1 — Top 10 products (bar chart)

- **Columns:** `product_name`, `category`, `total_revenue`, `total_orders`, `avg_order_value`
- **Chart config:** Bar chart with `product_name` on X-axis, `total_revenue` on Y-axis, `LIMIT 10`

### Query 2 — Customer revenue distribution (histogram)

- **Columns:** `revenue_bucket`, `customer_count`
- **Chart config:** Bar/histogram with `revenue_bucket` on X-axis, `customer_count` on Y-axis

### Query 3 — Customer segmentation (pie chart)

- **Columns:** `segment_type`, `customer_count`, `total_revenue`, `avg_revenue`
- **Chart config:** Pie chart with `segment_type` as slice, `customer_count` as value

## Setup in Databricks SQL (when workspace access is available)

1. Ensure Gold tables are populated (`gold.sales_by_product`, `gold.revenue_by_customer`, `gold.customer_segmentation`).
2. Open **SQL** → **Dashboards** → **Create dashboard**.
3. Add a **Query** for each of the three SQL blocks in `dashboard_queries.sql`.
4. Configure visualization types (bar, histogram/bar, pie) per table above.
5. Save the dashboard and note the URL in `candidate-info.md`.

## Current Status

**SQL queries:** implemented in `dashboard_queries.sql`.

**Databricks SQL Dashboard UI:** **not created or validated.**

> The actual Databricks SQL Dashboard could not be created or validated because Databricks workspace authentication is currently unavailable. Deployment and end-to-end execution remain pending until a valid Community Edition CLI profile is configured.

Do not assume the dashboard has been deployed until it is created manually in the workspace.

## Prerequisites

- Gold layer pipeline must have run successfully
- Hive databases `gold` with three aggregation tables (see `database/schema_community_edition.sql`)
- Databricks SQL access in the target workspace
