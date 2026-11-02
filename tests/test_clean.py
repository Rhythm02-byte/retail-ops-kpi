import pandas as pd

from retail_kpi.clean import clean_sales


def sample(rows):
    columns = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
    return pd.DataFrame(rows, columns=columns)


def row(invoice="1", quantity=2, price=5.0, description="MUG", customer=10.0):
    return [invoice, "85123A", description, quantity, pd.Timestamp("2010-01-05"), price, customer, "France"]


def test_normal_sale_is_kept_with_revenue():
    kept, dropped = clean_sales(sample([row(quantity=2, price=5.0)]))

    assert len(kept) == 1
    assert kept["revenue"].iloc[0] == 10.0
    assert dropped.empty


def test_cancellation_is_dropped_with_reason():
    kept, dropped = clean_sales(sample([row(invoice="C5001")]))

    assert kept.empty
    assert dropped["drop_reason"].tolist() == ["cancelled"]


def test_non_positive_quantity_and_price_are_dropped():
    kept, dropped = clean_sales(sample([row(quantity=-1), row(price=0.0)]))

    assert kept.empty
    assert sorted(dropped["drop_reason"]) == ["non-positive price", "non-positive quantity"]


def test_exact_duplicates_are_removed_once():
    kept, _ = clean_sales(sample([row(), row()]))

    assert len(kept) == 1


def test_missing_description_is_dropped():
    kept, dropped = clean_sales(sample([row(description=None)]))

    assert kept.empty
    assert dropped["drop_reason"].tolist() == ["missing description"]
