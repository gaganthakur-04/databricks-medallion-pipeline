-- Gold layer: Revenue by Customer aggregation
-- Source: valid Silver orders (Completed) joined to valid Silver customers

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(*) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(SUM(o.total_amount), 2) AS lifetime_value_actual
FROM silver.orders o
INNER JOIN silver.customers c
    ON o.customer_id = c.customer_id
    AND c.is_valid = TRUE
WHERE o.is_valid = TRUE
  AND o.order_status = 'Completed'
GROUP BY c.customer_id, c.customer_name, c.customer_segment
ORDER BY total_revenue DESC;
