# Gold Layer

Builds three business aggregation tables from **valid** Silver records (`is_valid = true`).

## What Gold Does

1. Reads `silver.customers`, `silver.orders`, `silver.products`
2. Filters to valid rows; revenue metrics use **Completed** orders only
3. Writes `gold.sales_by_product`, `gold.revenue_by_customer`, `gold.customer_segmentation`

## Tables

| Table | Grain | Key metrics |
|-------|-------|---------------|
| `gold.sales_by_product` | product | total_orders, total_revenue, avg_order_value |
| `gold.revenue_by_customer` | customer | total_orders, total_revenue, avg_order_value, lifetime_value_actual |
| `gold.customer_segmentation` | segment_type | customer_count, avg_revenue, total_revenue |

## Behavioral Segments

| Segment | Criteria (priority order) |
|---------|---------------------------|
| Inactive | 0 completed orders |
| High-Value | total revenue ≥ 75th percentile (among customers with completed orders) |
| Repeat | more than 1 completed order |
| One-Time | exactly 1 completed order |

## Run in Databricks

```python
from src.gold.build_all import main
main()
```

Reference SQL for dashboards: `src/gold/01_sales_by_product.sql`, `02_revenue_by_customer.sql`, `04_customer_segmentation.sql`.

## End-to-End

```python
from src.pipeline.run_all import main
main()
```
