from pathlib import Path
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt

def plot_latency(csv_path: Path, out_path: Path, title: Optional[str] = None, dpi: int = 160) -> Path:
    """
    Read CSV produced by the monitor and write a latency-over-time plot (PNG).
    - csv_path: path to CSV (with columns: timestamp,target,reachable,latency_ms)
    - out_path: output image path (e.g., docs/example_plot.png)
    - title: optional chart title
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("CSV is empty; nothing to plot.")

    # Parse and clean
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
    # Unreachable → keine Linie zeichnen: NaN statt Wert
    df.loc[df["reachable"] == 0, "latency_ms"] = pd.NA

    # Pivot: Zeitreihen pro Host
    pivot = df.pivot_table(index="timestamp", columns="target", values="latency_ms", aggfunc="mean")

    ax = pivot.plot(figsize=(10, 5))
    ax.set_title(title or "Network Latency Over Time")
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True, which="both", axis="both", linestyle="--", alpha=0.4)

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=dpi)
    plt.close()
    return out_path
