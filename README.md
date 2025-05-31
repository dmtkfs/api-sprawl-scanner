# API‑Sprawl Scanner (Pure‑Nmap Edition)


Scans any CIDR block with Nmap, fingerprints ports 80/443 (or custom) and writes a collapsible Markdown inventory of every live web service.

Map every web service in a CIDR block with **one command**.

* **Single‑file** Python 3 script (`scan.py`)
* Uses **Nmap** only – no Masscan or raw packet tricks
* Outputs a Markdown report in `reports/`  
  (collapsible http‑enum details for each host)

---

## Quick start

```powershell
# Windows
git clone https://github.com/<yourUser>/api-sprawl-scanner.git
cd api-sprawl-scanner
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scan.py 192.168.1.0/24
````

## Sample output

```
reports/xxxxxxxx-xxxx-192.168.1.0_24.md
└── 192.168.0.0
    ├─ 80  http    Router Info
    └─ 443 https   Router Info
```

Open the report in VS Code or any Markdown viewer.

## Customize

* **Ports** – edit `PORTS = [80, 443, 8080]` in `scan.py`
* **Nmap timing** – add `-T4` or `-T5` to `NMAP_OPTS`
* **More scripts** – append `--script ssl-cert,http-title` etc.
