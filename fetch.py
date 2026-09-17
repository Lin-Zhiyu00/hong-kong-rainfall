# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
Fetch Hong Kong daily rainfall data
uv run fetch.py
"""
from pathlib import Path
import requests

URL = ("https://data.weather.gov.hk/weatherAPI/cis/csvfile/HKO/ALL/daily_HKO_RF_ALL.csv") # CHANGE ME
FILE = "daily_HKO_RF_ALL.csv"

HERE = Path(__file__).parent
DATA = HERE / "data"

def fetch(url, path):
    """Ask for the file once. If it is already in data/, do nothing."""
    if path.exists():
        print(f"data/{path.name} is already here ({path.stat().st_size // 1024} KB). "
              "Delete it to fetch again.")
        return path
    DATA.mkdir(exist_ok=True)
    print(f"asking {url}")
    reply = requests.get(url, timeout=60, headers={"User‑Agent": "SD5913 PolyU student"})
    reply.raise_for_status()
    path.write_bytes(reply.content)
    print(f"saved data/{path.name} ({path.stat().st_size // 1024} KB). Now: git add data")
    return path

if __name__ == "__main__":
    fetch(URL, DATA / FILE)
