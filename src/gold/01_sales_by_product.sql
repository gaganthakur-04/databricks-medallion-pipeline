-- Gold layer: Sales by Product aggregation
-- Source: valid Silver orders (Completed) joined to valid Silver products

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM silver.orders o
INNER JOIN silver.products p
    ON o.product_id = p.product_id
    AND p.is_valid = TRUE
WHERE o.is_valid = TRUE
  AND o.order_status = 'Completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;
