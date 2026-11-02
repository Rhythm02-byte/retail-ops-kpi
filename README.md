# Operations KPI Dashboard: Online Retail II

SQL analysis of two years of transactions from a UK-based online gift retailer. The raw data is loaded into PostgreSQL, cleaned with explicit rules, and summarised with SQL queries. The results are charted and written up with three recommendations.

## Findings

Covering 1 December 2009 to 9 December 2011, after cleaning:

- **Revenue: £20.48 million** from 40,077 orders and 1,007,913 sales lines.
- **Strong seasonality.** Revenue peaks in October and November each year. November 2010 and November 2011 are both about £1.5 million, against roughly £0.6 to £0.8 million in a typical quiet month.
- **Concentrated market.** The United Kingdom makes up 85.0% of revenue. The next largest country, Ireland (EIRE), makes up 3.2%.
- **Customers come back.** Of 5,878 identified customers, 72.4% ordered more than once. Most customers are wholesalers, according to the dataset description.
- **Cancellations are high.** 15.5% of invoices (8,292 of 53,628) are cancellations.

### Recommendations

1. **Plan stock and staffing for the Q4 peak.** Revenue in October and November is about double a quiet month. Build the stock and temporary staffing plan from the same months in previous years, and start in September.
2. **Investigate the 15.5% cancellation rate.** This is the largest leak in the data. Check whether cancellations cluster by country, product, or customer type, and whether a clearer order confirmation would reduce them.
3. **Protect the repeat customers.** Repeat buyers are 72% of identified customers, and most are wholesalers. A reorder reminder or a trade-account programme for them is cheaper than winning new customers.

## Data

- **Source:** Online Retail II, UCI Machine Learning Repository. Donated by Daqing Chen. DOI [10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D).
- **Licence:** Creative Commons Attribution 4.0 (CC BY 4.0).
- **Not included in this repository.** Download the workbook yourself and place it at `data/online_retail_II.xlsx` (see Reproduce below).

### Cleaning rules

Applied in `src/retail_kpi/clean.py`. Each rule has a test in `tests/test_clean.py`.

| Step | Rows |
|---|---|
| Rows in the workbook (two sheets, one per year) | 1,067,371 |
| Exact duplicate rows removed | 34,335 |
| Cancelled invoices (invoice starts with "C") | dropped |
| Quantity zero or negative | dropped |
| Unit price zero or negative | dropped |
| Description missing | dropped |
| **Rows in `sales`** | **1,007,913** |

Rows without a customer ID are kept in `sales`. Revenue and product results include them. Only the customer KPIs leave them out.

Raw rows are kept in the `raw_transactions` table, so the cleaning can be checked against them. The cancellation rate uses the raw table, because cancelled invoices are not in `sales`.

## KPIs

Each query is in `sql/`, and its result is in `results/` as a CSV.

| File | What it shows |
|---|---|
| `01_monthly_revenue.sql` | Revenue, orders, units and average order value per month |
| `02_revenue_by_country.sql` | Revenue, orders and share by country |
| `03_top_products.sql` | The ten highest-revenue product codes |
| `04_customer_repeat_rate.sql` | Share of identified customers who ordered more than once |
| `05_cancellation_rate.sql` | Share of invoices that were cancelled |

Charts: `results/monthly_revenue.png` and `results/revenue_by_country.png`.

## Checks

- The SQL monthly revenue total (£20,476,260.43) matches an independent pandas calculation (£20,476,260.45). The difference is rounding, because the SQL rounds each month.
- The order count (40,077) and the cancellation rate (15.46%) also match the pandas calculation.

## Limits

- **No delivery or stock data.** The original plan asked for on-time delivery and inventory turnover. This dataset has neither, so those KPIs are not included.
- **Non-product codes.** Some stock codes are not products. "M" is manual adjustments and "DOT" is postage. They appear among the top products, so a product analysis should exclude them. The totals above include them.
- **Partial last month.** The data ends on 9 December 2011, so December 2011 is incomplete. It is shown separately in the chart.
- **Wholesale-heavy customers.** Repeat rates and average order values reflect a customer base that is mostly wholesalers, not individual shoppers.
- **Power BI not used.** Power BI Desktop runs only on Windows. The charts are drawn with matplotlib instead.

## Reproduce

```bash
conda create -n retail python=3.11 -y
conda activate retail
pip install -r requirements.txt
createdb retail_dev

# Download the workbook into data/ (about 45 MB), which unzips to data/online_retail_II.xlsx
mkdir -p data
curl -L -o data/online_retail_II.zip "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
unzip data/online_retail_II.zip -d data && rm data/online_retail_II.zip

PYTHONPATH=src python -m retail_kpi.load     # creates the tables and loads the cleaned data
PYTHONPATH=src python -m retail_kpi.kpis     # runs the queries and writes results/*.csv
PYTHONPATH=src python -m retail_kpi.plots    # draws the two charts
pytest
```

## Project structure

```
sql/                  schema and the five KPI queries
src/retail_kpi/
  clean.py            cleaning rules
  load.py             loads the workbook into PostgreSQL
  kpis.py             runs the queries and saves the results
  plots.py            draws the charts
tests/test_clean.py   tests for the cleaning rules
results/              KPI CSVs and charts
```
