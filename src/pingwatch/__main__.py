import argparse
from pathlib import Path
from .monitor import run_monitor

def parse_args():
    p = argparse.ArgumentParser(
        prog="pingwatch",
        description="Network latency & availability monitor (CLI)."
    )
    p.add_argument("--targets", type=Path, required=True,
                   help="Text file with one hostname/IP per line.")
    p.add_argument("--out", type=Path, default=Path("data/logs/run.csv"),
                   help="CSV output path.")
    p.add_argument("--interval", type=float, default=5.0,
                   help="Seconds between measurement rounds.")
    p.add_argument("--count", type=int, default=10,
                   help="Number of rounds (use a large number for longer runs).")
    p.add_argument("--timeout", type=float, default=2.0,
                   help="Ping timeout in seconds.")
    return p.parse_args()

def main():
    args = parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    run_monitor(
        targets_file=args.targets,
        out_csv=args.out,
        interval_s=args.interval,
        count=args.count,
        timeout_s=args.timeout,
    )

if __name__ == "__main__":
    main()
