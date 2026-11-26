# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""Download the original HKO daily rainfall CSV: uv run fetch.py."""
from pathlib import Path
import requests

URL = "https://data.weather.gov.hk/weatherAPI/cis/csvfile/HKO/ALL/daily_HKO_RF_ALL.csv"
DATA = Path(__file__).resolve().parent / "data"
FILE = "rainfall.csv"


def fetch(url, path):
    """Preserve the checked-in snapshot; delete it explicitly to refresh."""
    if path.exists():
        print(f"Using existing data/{path.name}. Delete it only if you want to download a newer snapshot.")
        return path
    reply = requests.get(url, timeout=60, headers={"User-Agent": "SD5913 PolyU student"})
    reply.raise_for_status()
    if "Daily Total Rainfall" not in reply.content[:1000].decode("utf-8-sig"):
        raise ValueError("The response is not the expected HKO daily rainfall CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(reply.content)
    print(f"Saved data/{path.name} ({len(reply.content):,} bytes)")
    return path


if __name__ == "__main__":
    fetch(URL, DATA / FILE)
