-- Gold layer: Customer Segmentation (behavioral)
-- Segments: High-Value, Repeat, One-Time, Inactive
-- Uses valid Silver customers and Completed valid Silver orders

WITH completed AS (
    SELECT
        customer_id,
        COUNT(*) AS completed_order_count,
        SUM(total_amount) AS total_revenue
    FROM silver.orders
    WHERE is_valid = TRUE
      AND order_status = 'Completed'
    GROUP BY customer_id
),
customer_activity AS (
    SELECT
        c.customer_id,
        COALESCE(completed.completed_order_count, 0) AS completed_order_count,
        COALESCE(completed.total_revenue, 0) AS total_revenue
    FROM silver.customers c
    LEFT JOIN completed
        ON c.customer_id = completed.customer_id
    WHERE c.is_valid = TRUE
),
threshold AS (
    SELECT APPROX_PERCENTILE(total_revenue, 0.75) AS p75_revenue
    FROM customer_activity
    WHERE completed_order_count > 0
),
segmented AS (
    SELECT
        ca.customer_id,
        ca.total_revenue,
        CASE
            WHEN ca.completed_order_count = 0 THEN 'Inactive'
            WHEN ca.total_revenue >= t.p75_revenue THEN 'High-Value'
            WHEN ca.completed_order_count > 1 THEN 'Repeat'
            ELSE 'One-Time'
        END AS segment_type
    FROM customer_activity ca
    CROSS JOIN threshold t
)
SELECT
    segment_type,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_revenue), 2) AS avg_revenue,
    ROUND(SUM(total_revenue), 2) AS total_revenue
FROM segmented
GROUP BY segment_type
ORDER BY segment_type;
