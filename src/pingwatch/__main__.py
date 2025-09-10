import argparse
from pathlib import Path
from .monitor import run_monitor
from .visualize import plot_latency

def _add_run_parser(subparsers):
    p = subparsers.add_parser("run", help="Run the latency/availability monitor.")
    p.add_argument("--targets", type=Path, required=True, help="Text file with one hostname/IP per line.")
    p.add_argument("--out", type=Path, default=Path("data/logs/run.csv"), help="CSV output path.")
    p.add_argument("--interval", type=float, default=5.0, help="Seconds between measurement rounds.")
    p.add_argument("--count", type=int, default=10, help="Number of rounds.")
    p.add_argument("--timeout", type=float, default=2.0, help="Ping timeout in seconds.")
    p.set_defaults(cmd="run")
    return p

def _add_plot_parser(subparsers):
    p = subparsers.add_parser("plot", help="Plot latency over time from a CSV produced by the monitor.")
    p.add_argument("--csv", type=Path, required=True, help="Input CSV path.")
    p.add_argument("--out", type=Path, default=Path("docs/example_plot.png"), help="Output image (PNG).")
    p.add_argument("--title", type=str, default=None, help="Optional chart title.")
    p.set_defaults(cmd="plot")
    return p

def parse_args():
    parser = argparse.ArgumentParser(prog="pingwatch", description="Network latency & availability monitor (CLI).")
    subparsers = parser.add_subparsers(dest="cmd")

    _add_run_parser(subparsers)
    _add_plot_parser(subparsers)

    # Backward-compatibility: if called without subcommand, behave like "run"
    parser.add_argument("--targets", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--out", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--interval", type=float, help=argparse.SUPPRESS)
    parser.add_argument("--count", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=float, help=argparse.SUPPRESS)

    args = parser.parse_args()
    if args.cmd is None:
        # Treat as "run" using direct args (legacy mode)
        args.cmd = "run"
    return args

def main():
    args = parse_args()

    if args.cmd == "run":
        out = getattr(args, "out", None) or Path("data/logs/run.csv")
        out.parent.mkdir(parents=True, exist_ok=True)
        run_monitor(
            targets_file=args.targets,
            out_csv=out,
            interval_s=getattr(args, "interval", 5.0),
            count=getattr(args, "count", 10),
            timeout_s=getattr(args, "timeout", 2.0),
        )
    elif args.cmd == "plot":
        out = args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        plot_latency(csv_path=args.csv, out_path=out, title=args.title)
        print(f"Saved plot → {out}")
    else:
        raise SystemExit("Unknown command")

if __name__ == "__main__":
    main()
