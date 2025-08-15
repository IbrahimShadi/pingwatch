from pathlib import Path
from typing import List, Tuple, Optional
import time, csv, re, platform, subprocess 
from datetime import datetime

def _ping_via_subprocess(host: str, timeout_s: float) -> Tuple[bool, Optional[float]]:
    system = platform.system().lower()
    if system == "windows":
        # -n 1 (1 echo), -w timeout in ms
        cmd = ["ping", "-n", "1", "-w", str(int(timeout_s * 1000)), host]
    else:
        # -c 1 (1 echo), -W timeout in s (Linux); on macOS -W is ms but -t is TTL—timeout not strictly supported
        cmd = ["ping", "-c", "1", "-W", str(int(timeout_s)), host]

    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s + 1)
        out = p.stdout + "\n" + p.stderr
        if p.returncode != 0:
            return (False, None)
        # Try to extract latency like 'time=12.3 ms' or 'time<1 ms'
        m = re.search(r"time[=<]\s*([\d\.]+)\s*ms", out, re.IGNORECASE)
        if m:
            return (True, float(m.group(1)))
        # Windows sometimes shows 'Average = 12ms'—use that as a last resort
        m2 = re.search(r"Average\s*=\s*(\d+)\s*ms", out, re.IGNORECASE)
        return (True, float(m2.group(1))) if m2 else (True, None)
    except Exception:
        return (False, None)

def _ping_host(host: str, timeout_s: float) -> Tuple[bool, Optional[float]]:
    try:
        from ping3 import ping  # lazy import
        # ⬇️ Cast auf int, damit Pylance zufrieden ist
        rtt_ms = ping(host, timeout=int(timeout_s), unit="ms")  # returns float ms or None
        return (True, float(rtt_ms)) if rtt_ms is not None else (False, None)
    except PermissionError:
        return _ping_via_subprocess(host, timeout_s)
    except Exception:
        return (False, None)


def load_targets(targets_file: Path) -> List[str]:
    with targets_file.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def measure_once(targets: List[str], timeout_s: float) -> List[Tuple[str, bool, Optional[float]]]:
    """
    Returns: list of (target, reachable, latency_ms).
    """
    results: List[Tuple[str, bool, Optional[float]]] = []
    for t in targets:
        reachable, latency_ms = _ping_host(t, timeout_s)
        results.append((t, reachable, latency_ms))
    return results

def append_csv(out_csv: Path, timestamp: datetime, rows: List[Tuple[str, bool, Optional[float]]]) -> None:
    is_new = not out_csv.exists()
    with out_csv.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp", "target", "reachable", "latency_ms"])
        for (target, reachable, latency_ms) in rows:
            writer.writerow([timestamp.isoformat(), target, int(reachable), latency_ms if latency_ms is not None else ""])

def run_monitor(targets_file: Path, out_csv: Path, interval_s: float, count: int, timeout_s: float) -> None:
    targets = load_targets(targets_file)
    if not targets:
        raise SystemExit(f"No targets found in {targets_file}")

    for i in range(count):
        ts = datetime.utcnow()
        rows = measure_once(targets, timeout_s)
        append_csv(out_csv, ts, rows)
        if i < count - 1:
            time.sleep(interval_s)
