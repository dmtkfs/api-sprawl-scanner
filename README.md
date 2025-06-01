# API‑Sprawl Scanner (Pure‑Nmap Edition)


Scans any CIDR block with Nmap, fingerprints ports 80/443 (or custom) and writes a collapsible Markdown inventory of every live web service.

Map every web service in a CIDR block with **one command**.

* **Single‑file** Python 3 script (`scan.py`)
* Uses **Nmap** only – no Masscan or raw packet tricks
* Outputs a Markdown report in `reports/`  
  (collapsible http‑enum details for each host)

---

## Why not just copy‑paste raw Nmap output?

* **Clean Markdown reports** – the script converts Nmap XML into a table + collapsible
  `http‑enum` details, ready to drop into GitHub, Confluence, Notion, etc.
* **Repeatable defaults** – ports 80/443, `-sV`, `http-enum`, and timing flags are baked in,
  so every run is apples‑to‑apples.
* **History & diff‑friendly** – each scan writes `reports/YYYYMMDD‑BLOCK.md`; you can track
  service‑drift in Git just by diffing Markdown.
* **Automation‑ready** – exits with a clean 0/1 status and no noisy terminal banners,
  making it trivial to schedule in cron or GitHub Actions.
* **Easy knobs** – adjust `PORTS` or extend `NMAP_OPTS` in two lines; no need for long
  command‑line Kung Fu.

If you just need a one‑off check, plain Nmap is great; when you want a shareable,
version‑controlled inventory, this wrapper saves time.

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
└── 192.168.1.0
    ├─ 80  http    Router Info
    └─ 443 https   Router Info
```

Open the report in VS Code or any Markdown viewer.

## Customize

* **Ports** – edit `PORTS = [80, 443, 8080]` in `scan.py`
* **Nmap timing** – add `-T4` or `-T5` to `NMAP_OPTS`
* **More scripts** – append `--script ssl-cert,http-title` etc.
