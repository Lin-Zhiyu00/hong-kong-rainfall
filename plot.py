# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "pandas"]
# ///
"""Plot real daily rainfall: uv run plot.py [--year 2025]."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "rainfall.csv"
OUT = HERE / "out" / "rainfall_plot.png"


def load_rainfall(path=DATA):
    # Two bilingual title lines precede the actual five-column CSV header.
    raw = pd.read_csv(path, skiprows=2, dtype=str, encoding="utf-8-sig")
    raw = raw.iloc[:, :5].copy()
    raw.columns = ["year", "month", "day", "value", "completeness"]
    # Footer legends have no numeric year and are not observations.
    raw = raw[pd.to_numeric(raw["year"], errors="coerce").notna()].copy()
    dates = pd.to_datetime(raw[["year", "month", "day"]].apply(pd.to_numeric), errors="coerce")
    values = raw["value"].str.strip()
    trace = values.eq("Trace")
    rainfall = pd.to_numeric(values.mask(trace, "0.025"), errors="coerce")
    unexpected = rainfall.isna() & ~values.eq("***")
    if unexpected.any():
        raise ValueError(f"Unrecognised rainfall values: {values[unexpected].unique()}")
    if (dates.isna() & rainfall.notna()).any():
        raise ValueError("An invalid calendar date has a rainfall measurement")
    # The archive includes unavailable February 29 placeholders in non-leap years.
    valid_dates = dates.notna()
    dates, rainfall, trace = dates[valid_dates], rainfall[valid_dates], trace[valid_dates]
    # Incomplete observations are not assumed to be dry days.
    rainfall = rainfall.where(raw["completeness"].str.strip().eq("C"))
    result = pd.DataFrame({"date": dates, "rainfall_mm": rainfall, "trace": trace}).set_index("date").sort_index()
    if result.index.has_duplicates:
        raise ValueError("Duplicate observation dates in rainfall CSV")
    if (result["rainfall_mm"].dropna() < 0).any():
        raise ValueError("Rainfall cannot be negative")
    return result


def select_year(data, requested=None):
    if requested is not None:
        if requested not in data.index.year:
            raise ValueError(f"No observations for {requested}")
        return requested
    # The downloaded archive may end partway through a year. Prefer a full year.
    for year in sorted(set(data.index.year), reverse=True):
        expected = pd.date_range(f"{year}-01-01", f"{year}-12-31")
        if expected.isin(data.index).all():
            return year
    raise ValueError("No full calendar year is available; choose --year explicitly")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, help="Calendar year; default: latest year with all dates present")
    args = parser.parse_args()
    if not DATA.exists():
        raise SystemExit("Missing data/rainfall.csv. Run: uv run fetch.py")
    data = load_rainfall()
    year = select_year(data, args.year)
    daily = data.reindex(pd.date_range(f"{year}-01-01", f"{year}-12-31"))
    fig, ax = plt.subplots(figsize=(12, 5), layout="constrained")
    fig.patch.set_facecolor("#fafbfd")
    ax.set_facecolor("#fafbfd")
    ax.bar(daily.index, daily["rainfall_mm"], width=.85, color="#2469a0", zorder=3)
    missing = daily["rainfall_mm"].isna()
    if missing.any():
        ax.scatter(daily.index[missing], [0] * int(missing.sum()), marker="x", color="#b33a3a",
                   label="Unavailable / incomplete", zorder=4)
        ax.legend(frameon=False)
    ax.set(title=f"Hong Kong Observatory: Daily Rainfall ({year})", ylabel="Daily rainfall (mm)", xlabel="Month")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlim(pd.Timestamp(year, 1, 1) - pd.Timedelta(days=.5), pd.Timestamp(year, 12, 31) + pd.Timedelta(days=.5))
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=.2, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("How rainfall changes through the year", fontsize=16, fontweight="bold")
    fig.supxlabel("Source: Hong Kong Observatory daily rainfall archive | Trace <0.05 mm shown as 0.025 mm; missing values are not zero.", fontsize=8)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=180)
    plt.close(fig)
    print(f"Saved out/rainfall_plot.png | year={year}, observed={daily['rainfall_mm'].notna().sum()}, unavailable={missing.sum()}")


if __name__ == "__main__":
    main()
