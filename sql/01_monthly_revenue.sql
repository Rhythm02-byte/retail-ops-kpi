-- Revenue, orders and units per month. The last month in the data is partial (data ends 9 Dec 2011).
SELECT
    date_trunc('month', invoice_date)::date           AS month,
    ROUND(SUM(revenue), 2)                             AS revenue,
    COUNT(DISTINCT invoice)                            AS orders,
    SUM(quantity)                                      AS units,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice), 2)   AS average_order_value
FROM sales
GROUP BY 1
ORDER BY 1;
