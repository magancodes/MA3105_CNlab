#!/usr/bin/env python3
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap.forumsys.com")
LDAP_PORT = int(os.getenv("LDAP_PORT", "389"))
LDAP_USER_DN = os.getenv("LDAP_USER_DN", "cn=read-only-admin,dc=example,dc=com")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD", "password")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN", "dc=example,dc=com")
LDAP_SEARCH_FILTER = os.getenv("LDAP_SEARCH_FILTER", "(uid=einstein)")

def ldap_demo():
    try:
        from ldap3 import Server, Connection, ALL
    except ImportError:
        logging.error("ldap3 not installed. Install via: pip install ldap3")
        return

    server = Server(LDAP_SERVER, port=LDAP_PORT, get_info=ALL)
    conn = Connection(server, user=LDAP_USER_DN, password=LDAP_PASSWORD, auto_bind=True)
    logging.info("Connected and bound to LDAP server %s:%s", LDAP_SERVER, LDAP_PORT)

    conn.search(LDAP_BASE_DN, LDAP_SEARCH_FILTER, attributes=["cn","uid","mail"])
    for entry in conn.entries:
        logging.info("LDAP Entry: %s", entry)
    conn.unbind()

if __name__ == "__main__":
    try:
        ldap_demo()
    except Exception as e:
        logging.error("LDAP operation failed: %s", e)