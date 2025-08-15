# PingWatch — Network Latency & Availability Monitor

PingWatch is a lightweight and extensible Python tool for monitoring network availability and latency across multiple hosts.  
It performs scheduled ICMP probes, records reachability and round-trip times, and stores results in clean CSV logs for analysis.  
Built with Python 3 using `ping3`, `pandas`, and `matplotlib`, it also offers clear time-series visualizations to track performance trends.

---

## ✨ Key Features
- **Multi-target monitoring** — Ping multiple IPs/hostnames in each run  
- **Latency & reachability logging** — CSV output for easy analysis or compliance  
- **Clear visualization** — Time-series charts of latency per host (via `matplotlib`)  
- **Cross-platform** — Works on Windows, macOS, and Linux (with ping fallback)  
- **Configurable schedule** — Control targets, intervals, counts, and timeouts via CLI arguments

---

## 📂 Project Structure ´´´
pingwatch/
├─ src/
│ └─ pingwatch/
│ ├─ init.py
│ ├─ main.py # CLI entry point
│ └─ monitor.py # Core logic
├─ data/
│ └─ logs/ # CSV output
├─ targets.txt # List of hosts/IPs to monitor
├─ requirements.txt
└─ README.md
´´´

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/IbrahimShadi/pingwatch.git
cd pingwatch

python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

python -m pingwatch --targets targets.txt --count 5 --interval 3 --timeout 2 --out data/logs/run.csv

timestamp,target,reachable,latency_ms
2025-08-15T00:38:02.719374,8.8.8.8,1,13.43
2025-08-15T00:38:02.719374,1.1.1.1,1,15.76
