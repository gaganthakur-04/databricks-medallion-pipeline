-- Databricks SQL Dashboard queries
-- Source: Gold layer tables (run after pipeline completes)
-- See src/dashboard/DASHBOARD_GUIDE.md for visualization setup

-- =============================================================================
-- 1. Top 10 products by revenue (bar chart)
--    X-axis: product_name | Y-axis: total_revenue
-- =============================================================================
SELECT
    product_name,
    category,
    total_revenue,
    total_orders,
    avg_order_value
FROM gold.sales_by_product
ORDER BY total_revenue DESC
LIMIT 10;

-- =============================================================================
-- 2. Customer revenue distribution (histogram)
--    Binned customer counts by revenue range
-- =============================================================================
SELECT
    CASE
        WHEN total_revenue < 100 THEN '0-99'
        WHEN total_revenue < 500 THEN '100-499'
        WHEN total_revenue < 1000 THEN '500-999'
        WHEN total_revenue < 5000 THEN '1000-4999'
        ELSE '5000+'
    END AS revenue_bucket,
    COUNT(*) AS customer_count
FROM gold.revenue_by_customer
GROUP BY
    CASE
        WHEN total_revenue < 100 THEN '0-99'
        WHEN total_revenue < 500 THEN '100-499'
        WHEN total_revenue < 1000 THEN '500-999'
        WHEN total_revenue < 5000 THEN '1000-4999'
        ELSE '5000+'
    END
ORDER BY revenue_bucket;

-- =============================================================================
-- 3. Customer segmentation (pie chart)
--    Slice: segment_type | Value: customer_count
-- =============================================================================
SELECT
    segment_type,
    customer_count,
    total_revenue,
    avg_revenue
FROM gold.customer_segmentation
ORDER BY customer_count DESC;
