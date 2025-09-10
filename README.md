# Pingwatch

Pingwatch is a Python-based network latency and availability monitoring tool.  
It regularly pings a list of hosts/IPs, logs their availability and response times to CSV,  
and generates visual reports of network performance over time.

**Use cases:**
- Monitor server uptime
- Track internet stability
- Troubleshoot network issues

---

## 📦 Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/IbrahimShadi/pingwatch.git
cd pingwatch

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install in editable mode with dependencies
pip install -e .
```
## Usage

python -m pingwatch run --targets targets.txt --count 5 --interval 3 --timeout 2 --out data/Logs/run.csv

Parameters:

--targets → File with list of hosts/IPs

--count → Number of measurement cycles

--interval → Time (s) between cycles

--timeout → Ping timeout (s)

--out → Output CSV path

Example targets.txt:

8.8.8.8
1.1.1.1

## Generate Latency Plot

python -m pingwatch plot --csv data/Logs/run.csv --out docs/example_plot.png --title "Latency (UTC)"

## Example Output

timestamp,target,reachable,latency_ms
2025-08-15T00:38:02.719374,8.8.8.8,1,13.43
2025-08-15T00:38:02.719374,1.1.1.1,1,15.76
...

## 📦 Project Structure
```
pingwatch/
├─ src/
│  └─ pingwatch/
│     ├─ __init__.py
│     ├─ __main__.py   # CLI entry point
│     ├─ monitor.py    # Core logic
│     └─ visualize.py  # Plotting
├─ data/
│  └─ Logs/            # CSV output
├─ targets.txt         # List of hosts/IPs to monitor
├─ requirements.txt
├─ setup.py
└─ README.md
```
## 🛠 Technologies

Python 3

ping3 → ICMP ping

pandas → CSV processing

matplotlib → Plotting
