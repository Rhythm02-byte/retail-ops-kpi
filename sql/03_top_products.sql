-- The ten products with the highest revenue over the whole period.
SELECT
    stock_code,
    MAX(description)            AS description,
    ROUND(SUM(revenue), 2)      AS revenue,
    SUM(quantity)               AS units
FROM sales
GROUP BY stock_code
ORDER BY revenue DESC
LIMIT 10;
