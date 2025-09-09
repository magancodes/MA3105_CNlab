#!/usr/bin/env python3
import os
import ssl
import smtplib
import logging
from email.message import EmailMessage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
MAIL_TO = os.getenv("MAIL_TO", SMTP_USER)

def send_test_email():
    msg = EmailMessage()
    msg["Subject"] = "CN Lab Test Email"
    msg["From"] = SMTP_USER
    msg["To"] = MAIL_TO
    msg.set_content("This is a test email sent from the CN Lab SMTP script.")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
        server.set_debuglevel(1)  # Log the SMTP conversation
        server.ehlo()
        if SMTP_PORT == 587:
            server.starttls(context=context)
            server.ehlo()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        logging.info("Email sent to %s", MAIL_TO)

if __name__ == "__main__":
    if not MAIL_TO:
        logging.error("Set SMTP_USER/SMTP_PASS and MAIL_TO env vars.")
    else:
        send_test_email()