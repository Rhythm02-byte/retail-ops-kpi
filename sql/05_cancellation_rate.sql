-- Share of invoices that were cancelled. Uses the raw table, because cancelled invoices are dropped from sales.
SELECT
    COUNT(DISTINCT invoice)                                                        AS invoices,
    COUNT(DISTINCT invoice) FILTER (WHERE invoice LIKE 'C%')                       AS cancelled,
    ROUND(100.0 * COUNT(DISTINCT invoice) FILTER (WHERE invoice LIKE 'C%')
          / COUNT(DISTINCT invoice), 2)                                            AS cancellation_rate_pct
FROM raw_transactions;
