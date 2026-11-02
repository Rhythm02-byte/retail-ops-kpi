"""Cleaning rules for the Online Retail II transactions.

Each rule is a separate function, so it can be tested and explained on its own.
Rows that fail a rule are dropped from the analysis tables but kept in the raw table.
"""
import pandas as pd

COLUMNS = {
    "Invoice": "invoice",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "Customer ID": "customer_id",
    "Country": "country",
}


def normalise_columns(df):
    out = df.rename(columns=COLUMNS)
    out["invoice"] = out["invoice"].astype(str)
    out["stock_code"] = out["stock_code"].astype(str)
    out["country"] = out["country"].astype(str)
    return out


def is_cancellation(invoice):
    # Invoice numbers that start with "C" are cancellations of an earlier order
    return invoice.str.startswith("C")


def clean_sales(df):
    """Return the rows used for sales KPIs, and the reason each dropped row was dropped."""
    df = normalise_columns(df).drop_duplicates()
    reasons = pd.Series("", index=df.index)
    reasons[is_cancellation(df["invoice"])] = "cancelled"
    reasons[(reasons == "") & (df["quantity"] <= 0)] = "non-positive quantity"
    reasons[(reasons == "") & (df["unit_price"] <= 0)] = "non-positive price"
    reasons[(reasons == "") & df["description"].isna()] = "missing description"
    df = df.assign(drop_reason=reasons)
    kept = df[df["drop_reason"] == ""].drop(columns="drop_reason")
    kept = kept.assign(revenue=kept["quantity"] * kept["unit_price"])
    return kept, df[df["drop_reason"] != ""]
