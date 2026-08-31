# AI Prompts — Dashboard

## Prompt 1: Final assessment dashboard SQL (2026-08-31)

**PROMPT SENT:**

> Final assessment-completeness pass. Dashboard requirement: three visualizations — (1) Top 10 products by revenue bar chart from `gold.sales_by_product`, (2) customer revenue distribution histogram from `gold.revenue_by_customer`, (3) customer segmentation pie chart from `gold.customer_segmentation`. Replace placeholder queries in `dashboard_queries.sql`. Update `DASHBOARD_GUIDE.md`. State that Databricks SQL Dashboard UI could not be created/validated because workspace authentication is unavailable. Do not claim dashboard deployed. Do not change Gold logic.

**AI RESPONSE SUMMARY:**

Replaced placeholder queries in `dashboard_queries.sql` with three executable SQL blocks against `gold.sales_by_product`, `gold.revenue_by_customer`, and `gold.customer_segmentation`. Updated `DASHBOARD_GUIDE.md` with chart mapping and explicit note that Databricks SQL Dashboard UI was not created/validated due to authentication limitation.

**YOUR EVALUATION:** _Pending_

---

## Prompt 2: Dashboard SQL runtime validation (2026-08-31)

**PROMPT SENT:**

> Part of Databricks E2E validation pass — run dashboard SQL queries against live Gold tables after pipeline job succeeds. Verify all three required datasets return usable data for bar, histogram, and pie visualizations.

**AI RESPONSE SUMMARY:**

After successful bundle job run on Free Edition (`ce` profile), executed all three queries via SQL warehouse against live Gold tables:

| Query | Rows | Result |
|-------|------|--------|
| Top 10 products by revenue | 10 | Usable for bar chart |
| Customer revenue distribution | 5 buckets | Usable for histogram |
| Customer segmentation | 4 segments | Usable for pie chart |

Top product by revenue: `Innovative scalable interface` (242,874.44). Segments: Repeat (7,390), High-Value (2,484), One-Time (57), Inactive (9). Databricks SQL Dashboard UI was not created — SQL validation only. Updated `DASHBOARD_GUIDE.md` and `candidate-info.md`.

**YOUR EVALUATION:** _Pending_
