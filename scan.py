#!/usr/bin/env python3
"""
Pure‑Nmap API‑Sprawl Scanner  •  Windows / Python 3.8+
-----------------------------------------------------------------
• One Nmap pass across a CIDR block
• Ports 80 & 443 only (can add more)
• Parses Nmap’s XML and renders a Markdown report
"""

import argparse, datetime, pathlib, subprocess, xml.etree.ElementTree as ET
from jinja2 import Template

# ---------- settings -------------------------------------------------
PORTS = [80, 443]  # modify accordingly
NMAP_OPTS = [
    "-p",
    ",".join(map(str, PORTS)),
    "--open",  # show only hosts with open ports
    "-sV",  # service / version detection
    "--script",
    "http-enum",  # grab common web paths
]
# ---------------------------------------------------------------------

OUT_DIR = pathlib.Path("reports")
OUT_DIR.mkdir(exist_ok=True)


# ---------- helpers --------------------------------------------------
def run_nmap(cidr: str, xml_out: pathlib.Path) -> None:
    cmd = ["nmap", *NMAP_OPTS, "-oX", str(xml_out), cidr]
    print("[i] Running:", " ".join(cmd))
    subprocess.check_call(cmd)


def parse_xml(xml_path: pathlib.Path) -> list[dict]:
    """Return a list of {ip, ports:[{port,service,product,version,script}]}"""
    hosts = []
    tree = ET.parse(xml_path)
    for h in tree.findall("host"):
        addr_el = h.find("address")
        if addr_el is None:
            continue
        ip = addr_el.attrib.get("addr")

        port_details = []
        for p in h.findall("ports/port"):
            state_el = p.find("state")
            if state_el is None or state_el.attrib.get("state") != "open":
                continue

            svc_el = p.find("service")
            port_details.append(
                {
                    "port": int(p.attrib["portid"]),
                    "service": (
                        svc_el.attrib.get("name", "") if svc_el is not None else ""
                    ),
                    "product": (
                        svc_el.attrib.get("product", "") if svc_el is not None else ""
                    ),
                    "version": (
                        svc_el.attrib.get("version", "") if svc_el is not None else ""
                    ),
                    "script": (
                        p.find("script").attrib.get("output", "")
                        if p.find("script") is not None
                        else ""
                    ),
                }
            )

        if port_details:
            hosts.append({"ip": ip, "ports": port_details})
    return hosts


def render_md(cidr: str, hosts: list[dict]) -> str:
    tpl = Template(open("TEMPLATE.md", encoding="utf-8").read())
    ts = datetime.datetime.now().strftime("%Y‑%m‑%d %H:%M")
    return tpl.render(cidr=cidr, hosts=hosts, ports=PORTS, ts=ts)


# ---------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Pure‑Nmap web‑service mapper")
    ap.add_argument("cidr", help="Target block, e.g. 192.168.1.0/24")
    cidr = ap.parse_args().cidr

    xml_path = pathlib.Path("nmap.xml")
    run_nmap(cidr, xml_path)  # run the scan

    hosts = parse_xml(xml_path)  # collect results
    md = render_md(cidr, hosts)  # render Markdown

    out = OUT_DIR / f"{datetime.datetime.now():%Y%m%d-%H%M}-{cidr.replace('/', '_')}.md"
    out.write_text(md, encoding="utf-8")
    print(f"[✓] Report saved → {out}")
    if not hosts:
        print("[i] No web services found.")


if __name__ == "__main__":
    main()
