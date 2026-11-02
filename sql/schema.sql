-- Every row from the workbook, as it was delivered.
CREATE TABLE IF NOT EXISTS raw_transactions (
    invoice      TEXT,
    stock_code   TEXT,
    description  TEXT,
    quantity     INTEGER,
    invoice_date TIMESTAMP,
    unit_price   NUMERIC(10, 2),
    customer_id  BIGINT,
    country      TEXT
);

-- Rows that pass the cleaning rules in src/retail_kpi/clean.py, with revenue per line.
CREATE TABLE IF NOT EXISTS sales (
    invoice      TEXT,
    stock_code   TEXT,
    description  TEXT,
    quantity     INTEGER,
    invoice_date TIMESTAMP,
    unit_price   NUMERIC(10, 2),
    customer_id  BIGINT,
    country      TEXT,
    revenue      NUMERIC(12, 2)
);
