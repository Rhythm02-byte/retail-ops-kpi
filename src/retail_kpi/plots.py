"""Charts from the KPI results in results/. Run after retail_kpi.kpis.

    PYTHONPATH=src python -m retail_kpi.plots
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "results"


def plot_monthly_revenue(path):
    monthly = pd.read_csv(RESULTS_DIR / "01_monthly_revenue.csv", parse_dates=["month"])
    # The last month is partial (data ends 9 Dec 2011), so it is drawn hollow and labelled
    complete, partial = monthly.iloc[:-1], monthly.iloc[-1:]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(complete["month"], complete["revenue"] / 1e3, marker="o", label="complete months")
    ax.scatter(partial["month"], partial["revenue"] / 1e3, facecolors="none", edgecolors="C0", label="Dec 2011 (partial)")
    ax.set_ylabel("revenue (thousands, GBP)")
    ax.set_title("Monthly revenue, Dec 2009 to Dec 2011")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_revenue_by_country(path, top=10):
    by_country = pd.read_csv(RESULTS_DIR / "02_revenue_by_country.csv").head(top).iloc[::-1]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(by_country["country"], by_country["share_pct"])
    for y, share in enumerate(by_country["share_pct"]):
        ax.text(share + 0.5, y, f"{share:.1f}%", va="center", fontsize=9)
    ax.set_xlabel("share of total revenue (%)")
    ax.set_title(f"Top {top} countries by revenue")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    plot_monthly_revenue(RESULTS_DIR / "monthly_revenue.png")
    plot_revenue_by_country(RESULTS_DIR / "revenue_by_country.png")
    print("Saved results/monthly_revenue.png and results/revenue_by_country.png")
