# PingWatch

PingWatch is a lightweight Python tool for monitoring network availability and latency across a set of hosts. It performs scheduled ICMP probes, records reachability and round-trip times, and writes results to clean CSV logs for analysis and auditing. Built with Python 3 using `ping3`/`subprocess`, `pandas`, and `matplotlib`, it also generates clear time-series charts at the end of a run. Optional scheduling enables daily or interval-based checks to track performance trends over time.

**Key Features**
- Periodic pings to multiple IPs/hostnames with reachability and latency measurement
- Automatic CSV logging for easy analysis and reporting
- Time-series visualizations (latency over time) with `matplotlib`
- Clean, well-structured Python 3 codebase with functions and comments
- Optional daily/interval execution via cron (Linux) or Task Scheduler (Windows)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pingwatch --targets targets.txt --count 5 --interval 5 --out data/logs/run.csv
