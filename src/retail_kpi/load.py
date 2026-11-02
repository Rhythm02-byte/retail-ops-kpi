"""Load the Online Retail II workbook into PostgreSQL.

Creates two tables: raw_transactions (every row) and sales (rows that pass the cleaning rules).
Run from the project root:
    python -m retail_kpi.load
"""
import os
from pathlib import Path

import pandas as pd
import psycopg

from retail_kpi.clean import clean_sales, normalise_columns

ROOT = Path(__file__).resolve().parents[2]
WORKBOOK = ROOT / "data" / "online_retail_II.xlsx"
SCHEMA_SQL = ROOT / "sql" / "schema.sql"
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/retail_dev")


def read_workbook(path=WORKBOOK):
    # The workbook has one sheet per year, so read them all and stack them
    sheets = pd.read_excel(path, sheet_name=None)
    return pd.concat(sheets.values(), ignore_index=True)


def copy_frame(conn, df, table):
    # COPY loads the rows in bulk, which is much faster than one INSERT per row for a million rows
    columns = list(df.columns)
    conn.execute(f"TRUNCATE {table}")
    with conn.cursor().copy(f"COPY {table} ({', '.join(columns)}) FROM STDIN") as copy:
        for values in df.itertuples(index=False, name=None):
            copy.write_row([None if pd.isna(v) else v for v in values])


def load(path=WORKBOOK, url=DATABASE_URL):
    raw = normalise_columns(read_workbook(path))
    raw["customer_id"] = raw["customer_id"].astype("Int64")
    sales, dropped = clean_sales(raw)
    sales = sales.assign(customer_id=sales["customer_id"].astype("Int64"))

    with psycopg.connect(url) as conn:
        conn.execute(SCHEMA_SQL.read_text())
        copy_frame(conn, raw, "raw_transactions")
        copy_frame(conn, sales, "sales")
        conn.commit()
    return len(raw), len(sales), len(dropped)


if __name__ == "__main__":
    raw_rows, sales_rows, dropped_rows = load()
    print(f"raw_transactions: {raw_rows} rows")
    print(f"sales: {sales_rows} rows kept, {dropped_rows} dropped by the cleaning rules")
