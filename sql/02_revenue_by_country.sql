-- Where the revenue comes from, with each country's share of the total.
SELECT
    country,
    ROUND(SUM(revenue), 2)                                              AS revenue,
    COUNT(DISTINCT invoice)                                             AS orders,
    ROUND(100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (), 2)          AS share_pct
FROM sales
GROUP BY country
ORDER BY revenue DESC;
