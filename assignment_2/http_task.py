#!/usr/bin/env python3
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def send_get(url: str, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        logging.info("GET %s -> %s", r.url, r.status_code)
        logging.info("Headers: %s", dict(r.headers))
        logging.info("Body: %s", r.text[:1000])
        r.raise_for_status()
    except Exception as e:
        logging.error("GET request failed: %s", e)

def send_post(url: str, data=None, json=None):
    try:
        r = requests.post(url, data=data, json=json, timeout=10)
        logging.info("POST %s -> %s", r.url, r.status_code)
        logging.info("Headers: %s", dict(r.headers))
        logging.info("Body: %s", r.text[:1000])
        r.raise_for_status()
    except Exception as e:
        logging.error("POST request failed: %s", e)

if __name__ == "__main__":
    # Test endpoints (you can replace with your own)
    send_get("https://httpbin.org/get", params={"q": "cn-lab"})
    send_post("https://httpbin.org/post", json={"name": "CN Lab", "msg": "Hello HTTP"})