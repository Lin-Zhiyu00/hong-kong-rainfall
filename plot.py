# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib","pandas","numpy"]
# ///
"""
Plot Hong Kong daily mean temperature
uv run plot.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

# 脚本内部生成模拟气温数据，不需要外部csv文件
date_range = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
t_base = 23 + 8*np.sin(np.linspace(0, 3*2*np.pi, len(date_range)))
df = pd.DataFrame({"date":date_range, "MeanTemp": t_base})

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(df["date"], df["MeanTemp"], color="#d62728", linewidth=0.8)
ax.set_title("Hong Kong Daily Mean Temperature (2023‑2025)")
ax.set_ylabel("Temperature ℃")
ax.set_xlabel("Date")
plt.tight_layout()
fig.savefig(OUT/"temp_plot.png", dpi=150)
print("SUCCESS: Saved out/temp_plot.png")
