-- Share of identified customers who ordered more than once. Rows without a customer ID are left out.
WITH orders_per_customer AS (
    SELECT customer_id, COUNT(DISTINCT invoice) AS orders
    FROM sales
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
)
SELECT
    COUNT(*)                                                       AS customers,
    COUNT(*) FILTER (WHERE orders > 1)                             AS repeat_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE orders > 1) / COUNT(*), 2) AS repeat_rate_pct
FROM orders_per_customer;
