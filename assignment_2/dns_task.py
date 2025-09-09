#!/usr/bin/env python3
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

LOG_FILE = "dns_queries.log"

def log_line(text: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.utcnow().isoformat()}Z] {text}\n")
    logging.info(text)

def resolve_with_dnspython(domain: str):
    try:
        import dns.resolver
    except ImportError:
        logging.error("dnspython not installed. Install via: pip install dnspython")
        log_line("dnspython not installed.")
        return

    res = dns.resolver.Resolver()
    # A Records
    try:
        answers = res.resolve(domain, 'A')
        for rdata in answers:
            log_line(f"A {domain} -> {rdata.address}")
    except Exception as e:
        log_line(f"A lookup failed: {e}")

    # MX Records
    try:
        answers = res.resolve(domain, 'MX')
        for rdata in answers:
            log_line(f"MX {domain} -> {rdata.exchange.to_text()} (pref {rdata.preference})")
    except Exception as e:
        log_line(f"MX lookup failed: {e}")

    
    try:
        answers = res.resolve(domain, 'CNAME')
        for rdata in answers:
            log_line(f"CNAME {domain} -> {rdata.target.to_text()}")
    except Exception as e:
        log_line(f"CNAME lookup failed: {e}")

def basic_a_lookup(domain: str):
    import socket
    try:
        ip = socket.gethostbyname(domain)
        log_line(f"A {domain} -> {ip}")
    except Exception as e:
        log_line(f"Socket A lookup failed: {e}")

if __name__ == "__main__":
    domain = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    resolve_with_dnspython(domain)
    basic_a_lookup(domain)
    print(f"Results logged to {LOG_FILE}")
