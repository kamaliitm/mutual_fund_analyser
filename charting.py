import pandas as pd
import matplotlib.pyplot as plt
import os

ROLLING_RET_TEMPLATE = "data/rolling_return_{period}.csv"
ROLLING_STD_TEMPLATE = "data/rolling_std_{period}.csv"
CHARTS_DIR = "charts"

PERIODS = ["3Y", "5Y", "7Y", "10Y"]

def plot_metric(period):
    """Plot charts directly from precomputed rolling return / std CSVs.

    This avoids recalculating rolling values using calendar-day offsets and ensures
    the plots match the exact metrics written to disk by `analytics.py`.
    """

    # Rolling returns (wide format: date + one column per fund name)
    rr_path = ROLLING_RET_TEMPLATE.format(period=period.lower())
    rr_df = pd.read_csv(rr_path, parse_dates=["date"])

    plt.figure(figsize=(10, 6))
    for col in rr_df.columns:
        if col == "date":
            continue
        plt.plot(rr_df["date"], rr_df[col], label=col)
    plt.title(f"Rolling Returns ({period})")
    plt.xlabel("Date")
    plt.ylabel("Rolling Return (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    fname = f"{CHARTS_DIR}/rolling_return_{period}.png"
    plt.savefig(fname)
    plt.close()
    print(f"Saved chart: {fname}")

    # Rolling standard deviation
    std_path = ROLLING_STD_TEMPLATE.format(period=period.lower())
    std_df = pd.read_csv(std_path, parse_dates=["date"])

    plt.figure(figsize=(10, 6))
    for col in std_df.columns:
        if col == "date":
            continue
        plt.plot(std_df["date"], std_df[col], label=col)
    plt.title(f"Rolling Std Dev ({period})")
    plt.xlabel("Date")
    plt.ylabel("Rolling Std Dev")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    fname = f"{CHARTS_DIR}/rolling_std_{period}.png"
    plt.savefig(fname)
    plt.close()
    print(f"Saved chart: {fname}")


def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)
    for period in PERIODS:
        plot_metric(period)

if __name__ == "__main__":
    main()
